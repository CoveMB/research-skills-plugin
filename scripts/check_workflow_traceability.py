#!/usr/bin/env python3
"""Validate deterministic workflow traceability artifacts with content hashes."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from check_workflow_passport_fixtures import (
    FULL_TEXT_VERIFICATION_MARKERS,
    HUMAN_REVIEW_REQUIRED_MARKERS,
    PARTIAL_SOURCE_MARKERS,
    PROCESS_PASSPORT_REQUIRED_FIELDS,
    PROCESS_PASSPORT_REQUIRED_LIST_FIELDS,
    PROCESS_PASSPORT_REQUIRED_SCALAR_FIELDS,
    UNVERIFIED_EVIDENCE_STATUSES,
    VERIFIED_EVIDENCE_STATUSES,
    contains_any,
    non_empty_string_field_errors,
    non_empty_string_list_field_errors,
    object_list_item_errors,
    required_key_errors,
    string_list,
)


DEFAULT_TRACE = Path("tests/skill_evals/workflow_traces/claim-lineage-fixture/workflow-trace.json")
TRACE_SCHEMA_VERSION = "workflow-trace-v1"
TRACE_ARTIFACT_SCHEMA_VERSION = "workflow-trace-artifact-v1"
REQUIRED_TRACE_KEYS = {"schema_version", "scenario_id", "tracked_claim_ids", "stages"}
REQUIRED_STAGE_KEYS = {"stage_id", "skill", "artifact_id", "artifact_path", "artifact_sha256"}
CLAIM_LOCATOR_GAP_MARKERS = ("locator gap", "locator_gap", "page gap", "quote not verified")
CLAIM_LOCATOR_VERIFIED_MARKERS = ("locator verified", "verified locator", "verified page", "page verified")
CLAIM_LOCATOR_VERIFIED_STATUSES = {"verified_locator", "locator_verified", "verified_page", "page_verified"}
HUMAN_VERIFICATION_COMPLETE_STATUSES = {
    "complete",
    "completed",
    "human_verified",
    "verified_by_human",
    "verification_complete",
}
CLAIM_TEXT_KEYS = ("claim", "claim_text", "text")
CLAIM_TYPE_KEYS = ("claim_type", "type")
CLAIM_VERSION_NOTE_KEYS = (
    "version_note",
    "claim_version_note",
    "revision_note",
    "change_note",
    "change_explanation",
)
CLAIM_STATUS_JUSTIFICATION_KEYS = (
    "status_change_justification",
    "evidence_upgrade_justification",
    "verification_note",
    *CLAIM_VERSION_NOTE_KEYS,
)
CLAIM_SOURCE_LOCATOR_KEYS = (
    "source_locator",
    "locator",
    "page",
    "pages",
    "section",
    "paragraph",
    "archive_locator",
)
CLAIM_SOURCE_BASIS_KEYS = (
    "source_basis",
    "annotation_basis",
    "source_access_level",
    "verification_basis",
)
CLAIM_SOURCE_POINTER_KEYS = (
    "source_id",
    "source_pointer",
    "source_note_id",
    "citekey",
    "citation_key",
)
SOURCE_CLAIM_FIT_NOTE_KEYS = (
    "source_claim_fit_note",
    "source_fit_note",
    "claim_fit_note",
    "source_use_note",
)
TRACEABILITY_LINK_COLLECTION_KEYS = (
    "traceability_links",
    "claim_links",
    "source_links",
    "claim_references",
)
VERIFICATION_EVENT_REQUIRED_KEYS = ("event_type", "verified_at", "verification_basis", "verified_by_or_tool")
VERIFICATION_EVENT_FIELD_KEYS = ("verified_fields", "resolved_fields", "verification_scope", "status_fields")
VERIFICATION_EVENT_CLAIM_ID_KEYS = ("claim_ids", "resolved_claim_ids", "verified_claim_ids")
VERIFICATION_EVENT_RESOLVED_RISK_KEYS = ("resolved_risks", "risk_resolutions")
VERIFICATION_EVENT_RESOLVED_LIMIT_KEYS = ("resolved_handoff_limits", "resolved_limits", "handoff_limit_resolutions")
VERIFICATION_EVENT_FIELD_MARKERS = {
    "source_access_level": ("source_access_level", "source access", "full_text", "full text"),
    "evidence_status": ("evidence_status", "evidence status", "source support", "claim support"),
    "human_verification_status": ("human_verification_status", "human verification", "human review"),
    "locator_status": ("locator_status", "locator", "page", "quote"),
}


def read_json_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} root must be an object")
    return payload


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def process_passport(artifact: dict[str, Any]) -> dict[str, Any]:
    passport = artifact.get("process_passport")
    return passport if isinstance(passport, dict) else {}


def stage_identifier(stage: dict[str, Any]) -> str:
    stage_id = stage.get("stage_id")
    return stage_id if isinstance(stage_id, str) and stage_id else "<missing stage_id>"


def stage_list(document: dict[str, Any]) -> list[dict[str, Any]]:
    stages = document.get("stages")
    if not isinstance(stages, list):
        return []
    return [stage for stage in stages if isinstance(stage, dict)]


def tracked_claim_ids(document: dict[str, Any]) -> list[str]:
    return string_list(document.get("tracked_claim_ids"))


def safe_artifact_path(trace_path: Path, artifact_path_value: Any) -> Path | None:
    if not isinstance(artifact_path_value, str) or not artifact_path_value:
        return None
    artifact_path = Path(artifact_path_value)
    if artifact_path.is_absolute() or ".." in artifact_path.parts:
        return None
    trace_root = trace_path.parent.resolve()
    resolved_path = (trace_root / artifact_path).resolve()
    try:
        resolved_path.relative_to(trace_root)
    except ValueError:
        return None
    return resolved_path


def claim_id(claim: Any) -> str | None:
    if not isinstance(claim, dict):
        return None
    value = claim.get("claim_id")
    return value if isinstance(value, str) and value else None


def claim_list(artifact: dict[str, Any]) -> list[dict[str, Any]]:
    claims = artifact.get("claims")
    if not isinstance(claims, list):
        return []
    return [claim for claim in claims if isinstance(claim, dict)]


def claims_by_id(artifact: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        identifier: claim
        for claim in claim_list(artifact)
        for identifier in [claim_id(claim)]
        if identifier is not None
    }


def first_string_value(record: dict[str, Any], keys: tuple[str, ...]) -> str:
    for key in keys:
        value = record.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def string_value_present(record: dict[str, Any], keys: tuple[str, ...]) -> bool:
    return bool(first_string_value(record, keys))


def all_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [
            nested_string
            for nested_value in value.values()
            for nested_string in all_strings(nested_value)
        ]
    if isinstance(value, list):
        return [nested_string for item in value for nested_string in all_strings(item)]
    return []


def normalized_text(value: Any) -> str:
    return " ".join(str(value).strip().casefold().split())


def normalized_strings(value: Any) -> list[str]:
    return [normalized_text(text) for text in all_strings(value) if normalized_text(text)]


def claim_text(claim: dict[str, Any]) -> str:
    return first_string_value(claim, CLAIM_TEXT_KEYS)


def claim_type(claim: dict[str, Any]) -> str:
    return normalized_status(first_string_value(claim, CLAIM_TYPE_KEYS))


def source_pointer(claim: dict[str, Any]) -> str:
    return first_string_value(claim, CLAIM_SOURCE_POINTER_KEYS)


def has_version_note(claim: dict[str, Any]) -> bool:
    return string_value_present(claim, CLAIM_VERSION_NOTE_KEYS)


def has_claim_status_justification(claim: dict[str, Any]) -> bool:
    return string_value_present(claim, CLAIM_STATUS_JUSTIFICATION_KEYS)


def has_source_claim_fit_note(claim: dict[str, Any]) -> bool:
    return string_value_present(claim, SOURCE_CLAIM_FIT_NOTE_KEYS)


def has_explanation_value(value: Any) -> bool:
    return bool(normalized_strings(value))


def event_records_from_value(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, dict):
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    return []


def verification_events(artifact: dict[str, Any]) -> list[dict[str, Any]]:
    passport = process_passport(artifact)
    return [
        event
        for source in (artifact.get("verification_events"), passport.get("verification_events"))
        for event in event_records_from_value(source)
    ]


def valid_verification_event(event: dict[str, Any]) -> bool:
    return all(string_value_present(event, (key,)) for key in VERIFICATION_EVENT_REQUIRED_KEYS)


def field_markers(field_name: str) -> tuple[str, ...]:
    return VERIFICATION_EVENT_FIELD_MARKERS.get(field_name, (field_name,))


def event_mentions_field(event: dict[str, Any], field_name: str) -> bool:
    scope_text = " ".join(
        string
        for key in VERIFICATION_EVENT_FIELD_KEYS
        for string in normalized_strings(event.get(key))
    )
    return contains_any(scope_text, field_markers(field_name))


def event_mentions_claim(event: dict[str, Any], claim_identifier: str) -> bool:
    claim_identifiers = {
        value
        for key in VERIFICATION_EVENT_CLAIM_ID_KEYS
        for value in string_list(event.get(key))
    }
    return claim_identifier in claim_identifiers or "all_claims" in claim_identifiers


def event_resolves_value(event: dict[str, Any], keys: tuple[str, ...], value: str) -> bool:
    expected = normalized_text(value)
    return any(
        expected == normalized_text(candidate)
        for key in keys
        for candidate in string_list(event.get(key))
    )


def has_verification_event_for_field(artifact: dict[str, Any], field_name: str) -> bool:
    return any(
        valid_verification_event(event) and event_mentions_field(event, field_name)
        for event in verification_events(artifact)
    )


def has_verification_event_for_claim_field(
    artifact: dict[str, Any],
    claim_identifier: str,
    field_name: str,
) -> bool:
    return any(
        valid_verification_event(event)
        and event_mentions_claim(event, claim_identifier)
        and event_mentions_field(event, field_name)
        for event in verification_events(artifact)
    )


def has_verification_event_resolving_risk(artifact: dict[str, Any], risk: str) -> bool:
    return any(
        valid_verification_event(event)
        and event_resolves_value(event, VERIFICATION_EVENT_RESOLVED_RISK_KEYS, risk)
        for event in verification_events(artifact)
    )


def has_verification_event_resolving_limit(artifact: dict[str, Any], handoff_limit: str) -> bool:
    return any(
        valid_verification_event(event)
        and event_resolves_value(event, VERIFICATION_EVENT_RESOLVED_LIMIT_KEYS, handoff_limit)
        for event in verification_events(artifact)
    )


def claim_identifier_counts(artifact: dict[str, Any]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for claim in claim_list(artifact):
        identifier = claim_id(claim)
        if identifier is not None:
            counts[identifier] = counts.get(identifier, 0) + 1
    return counts


def referenced_claim_ids(artifact: dict[str, Any]) -> set[str]:
    identifiers: set[str] = set()
    for key in TRACEABILITY_LINK_COLLECTION_KEYS:
        value = artifact.get(key)
        if not isinstance(value, list):
            continue
        for item in value:
            identifier = claim_id(item)
            if identifier is not None:
                identifiers.add(identifier)
    identifiers.update(string_list(artifact.get("referenced_claim_ids")))
    return identifiers


def has_partial_source_access(passport: dict[str, Any]) -> bool:
    return contains_any(str(passport.get("source_access_level", "")), PARTIAL_SOURCE_MARKERS)


def has_full_text_verification_claim(passport: dict[str, Any]) -> bool:
    return contains_any(str(passport.get("source_access_level", "")), FULL_TEXT_VERIFICATION_MARKERS)


def has_unverified_evidence_status(value: Any) -> bool:
    return str(value).casefold() in UNVERIFIED_EVIDENCE_STATUSES or contains_any(str(value), ("unverified", "needed"))


def has_verified_evidence_status(value: Any) -> bool:
    return str(value).casefold() in VERIFIED_EVIDENCE_STATUSES


def needs_human_review(value: Any) -> bool:
    return contains_any(str(value), HUMAN_REVIEW_REQUIRED_MARKERS)


def marks_human_verification_complete(value: Any) -> bool:
    return normalized_status(value) in HUMAN_VERIFICATION_COMPLETE_STATUSES


def normalized_status(value: Any) -> str:
    return str(value).strip().casefold().replace("-", "_").replace(" ", "_")


def has_verified_locator(value: Any) -> bool:
    return normalized_status(value) in CLAIM_LOCATOR_VERIFIED_STATUSES or contains_any(
        str(value),
        CLAIM_LOCATOR_VERIFIED_MARKERS,
    )


def exact_list_missing(values: Any, expected_value: str) -> bool:
    return expected_value not in string_list(values)


def validate_passport_shape(stage: dict[str, Any], artifact: dict[str, Any]) -> list[str]:
    identifier = stage_identifier(stage)
    passport = process_passport(artifact)
    errors: list[str] = []
    if artifact.get("schema_version") != TRACE_ARTIFACT_SCHEMA_VERSION:
        errors.append(f"{identifier}: artifact schema_version must be {TRACE_ARTIFACT_SCHEMA_VERSION}")
    if artifact.get("handoff_artifact") is not True:
        errors.append(f"{identifier}: artifact must set handoff_artifact true")
    if not passport:
        errors.append(f"{identifier}: artifact must include process_passport object")
        return errors

    errors.extend(required_key_errors(identifier, passport, PROCESS_PASSPORT_REQUIRED_FIELDS, "process_passport"))
    errors.extend(
        non_empty_string_field_errors(
            identifier,
            passport,
            PROCESS_PASSPORT_REQUIRED_SCALAR_FIELDS,
            "process_passport",
        )
    )
    if passport.get("artifact_id") != stage.get("artifact_id"):
        errors.append(f"{identifier}: process_passport artifact_id must match trace artifact_id")
    errors.extend(
        non_empty_string_list_field_errors(
            identifier,
            passport,
            PROCESS_PASSPORT_REQUIRED_LIST_FIELDS,
            "process_passport",
        )
    )
    return errors


def load_stage_artifact(trace_path: Path, stage: dict[str, Any]) -> tuple[dict[str, Any] | None, str | None, list[str]]:
    identifier = stage_identifier(stage)
    artifact_path = safe_artifact_path(trace_path, stage.get("artifact_path"))
    if artifact_path is None:
        return None, None, [f"{identifier}: artifact_path must be a relative path inside the trace directory"]
    if not artifact_path.exists():
        return None, None, [f"{identifier}: artifact file does not exist"]

    computed_hash = sha256_file(artifact_path)
    errors: list[str] = []
    if stage.get("artifact_sha256") != computed_hash:
        errors.append(f"{identifier}: artifact_sha256 does not match artifact file")
    try:
        artifact = read_json_object(artifact_path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return None, computed_hash, [*errors, f"{identifier}: {error}"]
    return artifact, computed_hash, errors


def parent_trace_errors(
    stage: dict[str, Any],
    previous_stage: dict[str, Any],
    previous_hash: str,
) -> list[str]:
    identifier = stage_identifier(stage)
    errors: list[str] = []
    previous_artifact_id = previous_stage.get("artifact_id")
    if isinstance(previous_artifact_id, str) and exact_list_missing(stage.get("parent_artifact_ids"), previous_artifact_id):
        errors.append(f"{identifier}: parent_artifact_ids does not include previous artifact_id")
    if exact_list_missing(stage.get("parent_artifact_sha256"), previous_hash):
        errors.append(f"{identifier}: parent_artifact_sha256 does not match previous stage hash")
    return errors


def parent_passport_errors(
    stage: dict[str, Any],
    artifact: dict[str, Any],
    previous_stage: dict[str, Any],
    previous_hash: str,
) -> list[str]:
    identifier = stage_identifier(stage)
    passport = process_passport(artifact)
    errors: list[str] = []
    previous_artifact_id = previous_stage.get("artifact_id")
    if isinstance(previous_artifact_id, str) and exact_list_missing(passport.get("parent_artifact_ids"), previous_artifact_id):
        errors.append(f"{identifier}: process_passport parent_artifact_ids missing previous artifact_id")
    if exact_list_missing(passport.get("input_artifact_hashes"), previous_hash):
        errors.append(f"{identifier}: process_passport input_artifact_hashes missing previous artifact hash")
    return errors


def tracked_claim_errors(stage: dict[str, Any], artifact: dict[str, Any], identifiers: list[str]) -> list[str]:
    identifier = stage_identifier(stage)
    claims = claims_by_id(artifact)
    return [
        f"{identifier}: missing tracked claim_id {claim_identifier!r}"
        for claim_identifier in identifiers
        if claim_identifier not in claims
    ]


def claim_reference_integrity_errors(
    stage: dict[str, Any],
    artifact: dict[str, Any],
    tracked_identifiers: list[str],
) -> list[str]:
    stage_name = stage_identifier(stage)
    claim_counts = claim_identifier_counts(artifact)
    defined_identifiers = set(claim_counts)
    referenced_identifiers = referenced_claim_ids(artifact)
    acceptable_unlinked_identifiers = set(tracked_identifiers) | referenced_identifiers
    errors: list[str] = []

    for identifier, count in sorted(claim_counts.items()):
        if count > 1:
            errors.append(f"{stage_name}: duplicate claim_id {identifier!r}")

    for identifier in sorted(referenced_identifiers):
        if identifier not in defined_identifiers:
            errors.append(f"{stage_name}: referenced claim_id {identifier!r} is not defined in claims")

    for identifier in sorted(defined_identifiers):
        if identifier not in acceptable_unlinked_identifiers:
            errors.append(f"{stage_name}: defined claim_id {identifier!r} is never referenced")

    return errors


def source_claim_fit_errors(stage: dict[str, Any], artifact: dict[str, Any]) -> list[str]:
    stage_name = stage_identifier(stage)
    claims_by_source: dict[str, list[dict[str, Any]]] = {}
    for claim in claim_list(artifact):
        source = source_pointer(claim)
        if source:
            claims_by_source.setdefault(source, []).append(claim)

    errors: list[str] = []
    for source, claims in sorted(claims_by_source.items()):
        claim_types = {claim_type(claim) for claim in claims if claim_type(claim)}
        if len(claim_types) < 2:
            continue
        if any(not has_source_claim_fit_note(claim) for claim in claims):
            errors.append(f"{stage_name}: source {source!r} supports multiple claim types without source-claim-fit note")
    return errors


def claim_graph_errors(stage: dict[str, Any], artifact: dict[str, Any], tracked_identifiers: list[str]) -> list[str]:
    errors = claim_reference_integrity_errors(stage, artifact, tracked_identifiers)
    errors.extend(source_claim_fit_errors(stage, artifact))
    return errors


def passport_preservation_errors(
    stage: dict[str, Any],
    previous_artifact: dict[str, Any],
    artifact: dict[str, Any],
) -> list[str]:
    identifier = stage_identifier(stage)
    previous_passport = process_passport(previous_artifact)
    passport = process_passport(artifact)
    errors: list[str] = []

    if (
        has_partial_source_access(previous_passport)
        and has_full_text_verification_claim(passport)
        and not has_verification_event_for_field(artifact, "source_access_level")
    ):
        errors.append(f"{identifier}: must not upgrade partial source access to full-text verification")
    if (
        has_unverified_evidence_status(previous_passport.get("evidence_status"))
        and has_verified_evidence_status(passport.get("evidence_status"))
        and not has_verification_event_for_field(artifact, "evidence_status")
    ):
        errors.append(f"{identifier}: must not upgrade unverified passport evidence status to verified")
    if (
        needs_human_review(previous_passport.get("human_verification_status"))
        and marks_human_verification_complete(passport.get("human_verification_status"))
        and not has_verification_event_for_field(artifact, "human_verification_status")
    ):
        errors.append(f"{identifier}: must not mark human verification complete without verification event")

    for risk in string_list(previous_passport.get("unresolved_risks")):
        if (
            exact_list_missing(passport.get("unresolved_risks"), risk)
            and not has_verification_event_resolving_risk(artifact, risk)
        ):
            errors.append(f"{identifier}: missing unresolved risk from prior stage {risk!r}")
    for handoff_limit in string_list(previous_passport.get("handoff_limits")):
        if (
            exact_list_missing(passport.get("handoff_limits"), handoff_limit)
            and not has_verification_event_resolving_limit(artifact, handoff_limit)
        ):
            errors.append(f"{identifier}: missing handoff limit from prior stage {handoff_limit!r}")
    return errors


def claim_preservation_errors(
    stage: dict[str, Any],
    previous_artifact: dict[str, Any],
    artifact: dict[str, Any],
    identifiers: list[str],
) -> list[str]:
    stage_name = stage_identifier(stage)
    previous_claims = claims_by_id(previous_artifact)
    claims = claims_by_id(artifact)
    errors: list[str] = []

    for identifier in identifiers:
        previous_claim = previous_claims.get(identifier)
        claim = claims.get(identifier)
        if previous_claim is None or claim is None:
            continue
        if (
            normalized_text(claim_text(previous_claim))
            and normalized_text(claim_text(claim))
            and normalized_text(claim_text(previous_claim)) != normalized_text(claim_text(claim))
            and not has_version_note(claim)
        ):
            errors.append(f"{stage_name}: claim {identifier!r} text changed without version note")
        if (
            has_unverified_evidence_status(previous_claim.get("evidence_status"))
            and has_verified_evidence_status(claim.get("evidence_status"))
            and not has_verification_event_for_claim_field(artifact, identifier, "evidence_status")
            and not has_claim_status_justification(claim)
        ):
            errors.append(f"{stage_name}: claim {identifier!r} must not upgrade evidence status to verified")
        if (
            contains_any(str(previous_claim.get("locator_status", "")), CLAIM_LOCATOR_GAP_MARKERS)
            and has_verified_locator(claim.get("locator_status"))
            and not has_verification_event_for_claim_field(artifact, identifier, "locator_status")
            and not has_claim_status_justification(claim)
        ):
            errors.append(f"{stage_name}: claim {identifier!r} must not upgrade locator gap to verified")
        if (
            needs_human_review(previous_claim.get("human_verification_status"))
            and marks_human_verification_complete(claim.get("human_verification_status"))
            and not has_verification_event_for_claim_field(artifact, identifier, "human_verification_status")
        ):
            errors.append(f"{stage_name}: claim {identifier!r} must not mark human verification complete without verification event")
        if string_value_present(previous_claim, CLAIM_SOURCE_LOCATOR_KEYS) and not string_value_present(
            claim,
            CLAIM_SOURCE_LOCATOR_KEYS,
        ):
            errors.append(f"{stage_name}: claim {identifier!r} removed source locator")
        if string_value_present(previous_claim, CLAIM_SOURCE_BASIS_KEYS) and not string_value_present(
            claim,
            CLAIM_SOURCE_BASIS_KEYS,
        ):
            errors.append(f"{stage_name}: claim {identifier!r} removed source-basis label")
        if claim_type(previous_claim) and claim_type(claim) and claim_type(previous_claim) != claim_type(claim) and not has_version_note(claim):
            errors.append(f"{stage_name}: claim {identifier!r} type changed without explanation")
    return errors


def validate_loaded_stages(
    trace_path: Path,
    document: dict[str, Any],
    stages: list[dict[str, Any]],
) -> list[str]:
    claim_identifiers = tracked_claim_ids(document)
    loaded_artifacts: list[dict[str, Any]] = []
    stage_hashes: list[str] = []
    errors: list[str] = []

    for index, stage in enumerate(stages):
        identifier = stage_identifier(stage)
        errors.extend(required_key_errors(identifier, stage, REQUIRED_STAGE_KEYS, "stage"))
        artifact, computed_hash, load_errors = load_stage_artifact(trace_path, stage)
        errors.extend(load_errors)
        if artifact is None or computed_hash is None:
            continue
        errors.extend(validate_passport_shape(stage, artifact))
        errors.extend(tracked_claim_errors(stage, artifact, claim_identifiers))
        errors.extend(claim_graph_errors(stage, artifact, claim_identifiers))

        if index > 0 and loaded_artifacts and stage_hashes:
            previous_stage = stages[index - 1]
            previous_artifact = loaded_artifacts[-1]
            previous_hash = stage_hashes[-1]
            errors.extend(parent_trace_errors(stage, previous_stage, previous_hash))
            errors.extend(parent_passport_errors(stage, artifact, previous_stage, previous_hash))
            errors.extend(passport_preservation_errors(stage, previous_artifact, artifact))
            errors.extend(claim_preservation_errors(stage, previous_artifact, artifact, claim_identifiers))

        loaded_artifacts.append(artifact)
        stage_hashes.append(computed_hash)
    return errors


def validate_trace_file(trace_path: Path) -> list[str]:
    try:
        document = read_json_object(trace_path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return [str(error)]

    stages = stage_list(document)
    errors = required_key_errors("trace", document, REQUIRED_TRACE_KEYS, "trace")
    if document.get("schema_version") != TRACE_SCHEMA_VERSION:
        errors.append(f"trace: schema_version must be {TRACE_SCHEMA_VERSION}")
    claim_identifiers = document.get("tracked_claim_ids")
    if not isinstance(claim_identifiers, list) or not tracked_claim_ids(document):
        errors.append("trace: tracked_claim_ids must be a non-empty string list")
    elif len(tracked_claim_ids(document)) != len(claim_identifiers):
        errors.append("trace: tracked_claim_ids must contain only non-empty strings")
    if not stages:
        errors.append("trace: stages must be a non-empty list of objects")
    errors.extend(object_list_item_errors(document, "stages", prefix="trace: "))
    errors.extend(validate_loaded_stages(trace_path, document, stages))
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--trace",
        type=Path,
        default=DEFAULT_TRACE,
        help="Workflow trace JSON document.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors = validate_trace_file(args.trace)
    if errors:
        print("Workflow trace check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("OK: workflow trace is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
