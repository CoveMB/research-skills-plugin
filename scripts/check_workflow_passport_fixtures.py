#!/usr/bin/env python3
"""Validate multi-skill workflow process-passport preservation fixtures."""
from __future__ import annotations

import argparse
import copy
import json
import re
from pathlib import Path
from typing import Any, Iterable


DEFAULT_FIXTURES = Path("tests/skill_evals/workflow_passports/fixtures.json")
FIXTURE_SCHEMA_VERSION = "workflow-passport-fixtures-v1"
FIXTURE_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REQUIRED_FIXTURE_KEYS = {
    "id",
    "from_skill",
    "to_skill",
    "handoff",
    "input_artifact",
    "expected_output_artifact",
    "forbidden_behavior",
}
PROCESS_PASSPORT_REQUIRED_FIELDS = {
    "artifact_id",
    "source_basis",
    "source_access_level",
    "corpus_coverage",
    "evidence_status",
    "tool_use",
    "human_verification_status",
    "unresolved_risks",
    "handoff_limits",
    "generated_or_updated_at",
    "producing_skill",
    "intended_next_skill_or_use",
}
PROCESS_PASSPORT_REQUIRED_LIST_FIELDS = {
    "tool_use",
    "unresolved_risks",
    "handoff_limits",
}
PROCESS_PASSPORT_REQUIRED_SCALAR_FIELDS = (
    PROCESS_PASSPORT_REQUIRED_FIELDS - PROCESS_PASSPORT_REQUIRED_LIST_FIELDS
)
PARTIAL_SOURCE_MARKERS = (
    "abstract only",
    "citation only",
    "controlled-packet",
    "excerpt only",
    "fixture only",
    "metadata only",
    "no full text",
    "partial",
    "private-no-external",
    "prompt only",
)
FULL_TEXT_VERIFICATION_MARKERS = (
    "full text verified",
    "full-text verified",
    "full text access verified",
    "verified against full text",
)
UNVERIFIED_EVIDENCE_STATUSES = {
    "abstract_only_unverified",
    "citation_only_unverified",
    "fixture_unverified",
    "hold_for_verification",
    "partial_unverified",
    "unsupported_in_provided_material",
    "verification_needed",
}
VERIFIED_EVIDENCE_STATUSES = {
    "verified",
    "full_text_verified",
    "source_verified",
    "verification_complete",
}
HUMAN_REVIEW_REQUIRED_MARKERS = (
    "human review",
    "needed",
    "required",
    "partial",
    "unavailable",
    "before",
)


def read_json_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} root must be an object")
    return payload


def fixture_list(document: dict[str, Any]) -> list[dict[str, Any]]:
    fixtures = document.get("fixtures")
    if not isinstance(fixtures, list):
        return []
    return [fixture for fixture in fixtures if isinstance(fixture, dict)]


def object_list_item_errors(document: dict[str, Any], key: str, *, prefix: str = "") -> list[str]:
    values = document.get(key)
    if not isinstance(values, list):
        return []
    return [
        f"{prefix}{key}[{index}] must be an object"
        for index, value in enumerate(values)
        if not isinstance(value, dict)
    ]


def fixture_identifier(fixture: dict[str, Any]) -> str:
    value = fixture.get("id")
    return value if isinstance(value, str) and value else "<missing id>"


def string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str) and item.strip()]


def all_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for nested_value in value.values():
            yield from all_strings(nested_value)
    elif isinstance(value, list):
        for item in value:
            yield from all_strings(item)


def normalized_text(value: Any) -> str:
    return "\n".join(all_strings(value)).casefold()


def contains_any(text: str, markers: Iterable[str]) -> bool:
    normalized = text.casefold()
    return any(marker in normalized for marker in markers)


def required_key_errors(identifier: str, payload: dict[str, Any], required_keys: set[str], label: str) -> list[str]:
    return [
        f"{identifier}: {label} missing key {key!r}"
        for key in sorted(required_keys)
        if key not in payload
    ]


def non_empty_string_field_errors(
    identifier: str,
    payload: dict[str, Any],
    field_names: set[str],
    label: str,
) -> list[str]:
    return [
        f"{identifier}: {label} {field_name!r} must be a non-empty string"
        for field_name in sorted(field_names)
        for value in [payload.get(field_name)]
        if field_name in payload and (not isinstance(value, str) or not value.strip())
    ]


def non_empty_string_list_field_errors(
    identifier: str,
    payload: dict[str, Any],
    field_names: set[str],
    label: str,
) -> list[str]:
    errors: list[str] = []
    for field_name in sorted(field_names):
        value = payload.get(field_name)
        if not isinstance(value, list) or not string_list(value):
            errors.append(f"{identifier}: {label} {field_name!r} must be a non-empty string list")
        elif len(string_list(value)) != len(value):
            errors.append(f"{identifier}: {label} {field_name!r} must contain only non-empty strings")
    return errors


def validate_passport_shape(identifier: str, artifact: Any, label: str) -> list[str]:
    if not isinstance(artifact, dict):
        return [f"{identifier}: {label} must be an object"]
    if artifact.get("handoff_artifact") is not True:
        return [f"{identifier}: {label} must set handoff_artifact true"]
    passport = artifact.get("process_passport")
    if not isinstance(passport, dict):
        return [f"{identifier}: {label} must include process_passport object"]

    errors = required_key_errors(identifier, passport, PROCESS_PASSPORT_REQUIRED_FIELDS, f"{label} process_passport")
    errors.extend(
        non_empty_string_field_errors(
            identifier,
            passport,
            PROCESS_PASSPORT_REQUIRED_SCALAR_FIELDS,
            f"{label} process_passport",
        )
    )
    errors.extend(
        non_empty_string_list_field_errors(
            identifier,
            passport,
            PROCESS_PASSPORT_REQUIRED_LIST_FIELDS,
            f"{label} process_passport",
        )
    )
    return errors


def process_passport(artifact: dict[str, Any]) -> dict[str, Any]:
    passport = artifact.get("process_passport")
    return passport if isinstance(passport, dict) else {}


def has_partial_source_access(passport: dict[str, Any]) -> bool:
    return contains_any(str(passport.get("source_access_level", "")), PARTIAL_SOURCE_MARKERS)


def has_full_text_verification_claim(passport: dict[str, Any]) -> bool:
    return contains_any(str(passport.get("source_access_level", "")), FULL_TEXT_VERIFICATION_MARKERS)


def has_unverified_evidence_status(passport: dict[str, Any]) -> bool:
    return str(passport.get("evidence_status", "")).casefold() in UNVERIFIED_EVIDENCE_STATUSES


def has_verified_evidence_status(passport: dict[str, Any]) -> bool:
    return str(passport.get("evidence_status", "")).casefold() in VERIFIED_EVIDENCE_STATUSES


def needs_human_review(passport: dict[str, Any]) -> bool:
    return contains_any(str(passport.get("human_verification_status", "")), HUMAN_REVIEW_REQUIRED_MARKERS)


def has_unverified_claim_or_locator_gap(artifact: dict[str, Any]) -> bool:
    text = normalized_text(artifact)
    markers = (
        "locator gap",
        "locator_gap",
        "page gap",
        "quote not verified",
        "unverified",
        "unsupported_in_provided_material",
        "verification_needed",
    )
    return contains_any(text, markers)


def list_contains_exact(values: Any, expected_value: str) -> bool:
    return expected_value in string_list(values)


def justified_resolution_markers(fixture: dict[str, Any], risk: str) -> list[str]:
    markers: list[str] = []
    resolutions = fixture.get("justified_resolutions")
    if not isinstance(resolutions, list):
        return markers
    for resolution in resolutions:
        if not isinstance(resolution, dict) or resolution.get("risk") != risk:
            continue
        marker = resolution.get("verification_marker")
        if isinstance(marker, str) and marker:
            markers.append(marker)
    return markers


def risk_is_justifiably_resolved(fixture: dict[str, Any], output_passport: dict[str, Any], risk: str) -> bool:
    output_text = normalized_text(output_passport)
    return any(marker.casefold() in output_text for marker in justified_resolution_markers(fixture, risk))


def preservation_errors_for_lists(
    fixture: dict[str, Any],
    *,
    field_name: str,
    noun: str,
    input_passport: dict[str, Any],
    output_passport: dict[str, Any],
) -> list[str]:
    identifier = fixture_identifier(fixture)
    errors: list[str] = []
    for value in string_list(input_passport.get(field_name)):
        if list_contains_exact(output_passport.get(field_name), value):
            continue
        if field_name == "unresolved_risks" and risk_is_justifiably_resolved(fixture, output_passport, value):
            continue
        errors.append(f"{identifier}: expected output missing {noun} {value!r}")
    return errors


def validate_handoff_preservation(fixture: dict[str, Any], output_artifact: dict[str, Any]) -> list[str]:
    identifier = fixture_identifier(fixture)
    input_artifact = fixture.get("input_artifact")
    if not isinstance(input_artifact, dict):
        return [f"{identifier}: input_artifact must be an object"]

    input_passport = process_passport(input_artifact)
    output_passport = process_passport(output_artifact)
    errors: list[str] = []

    if has_partial_source_access(input_passport) and has_full_text_verification_claim(output_passport):
        errors.append(f"{identifier}: expected output must not upgrade partial source access to full-text verification")
    if has_unverified_evidence_status(input_passport) and has_verified_evidence_status(output_passport):
        errors.append(f"{identifier}: expected output must not upgrade unverified evidence status to verified")
    if needs_human_review(input_passport) and not needs_human_review(output_passport):
        errors.append(f"{identifier}: expected output must preserve human-review requirement")

    errors.extend(
        preservation_errors_for_lists(
            fixture,
            field_name="unresolved_risks",
            noun="unresolved risk",
            input_passport=input_passport,
            output_passport=output_passport,
        )
    )
    errors.extend(
        preservation_errors_for_lists(
            fixture,
            field_name="handoff_limits",
            noun="handoff limit",
            input_passport=input_passport,
            output_passport=output_passport,
        )
    )
    return errors


def invalid_fixture_id_errors(fixture: dict[str, Any]) -> list[str]:
    identifier = fixture_identifier(fixture)
    return [] if FIXTURE_ID_RE.match(identifier) else [f"{identifier}: id must be lowercase kebab-case"]


def invalid_string_list_errors(fixture: dict[str, Any]) -> list[str]:
    identifier = fixture_identifier(fixture)
    value = fixture.get("forbidden_behavior")
    if not isinstance(value, list) or not string_list(value):
        return [f"{identifier}: forbidden_behavior must be a non-empty string list"]
    if len(string_list(value)) != len(value):
        return [f"{identifier}: forbidden_behavior must contain only strings"]
    return []


def validate_fixture(fixture: dict[str, Any]) -> list[str]:
    identifier = fixture_identifier(fixture)
    errors = required_key_errors(identifier, fixture, REQUIRED_FIXTURE_KEYS, "fixture")
    errors.extend(invalid_fixture_id_errors(fixture))
    errors.extend(invalid_string_list_errors(fixture))

    input_artifact = fixture.get("input_artifact")
    output_artifact = fixture.get("expected_output_artifact")
    errors.extend(validate_passport_shape(identifier, input_artifact, "input_artifact"))
    errors.extend(validate_passport_shape(identifier, output_artifact, "expected_output_artifact"))
    if isinstance(input_artifact, dict) and not has_partial_source_access(process_passport(input_artifact)):
        errors.append(f"{identifier}: input artifact must include a partial-source access label")
    if isinstance(input_artifact, dict) and not has_unverified_claim_or_locator_gap(input_artifact):
        errors.append(f"{identifier}: input artifact must include an unverified claim or locator gap")
    if isinstance(input_artifact, dict) and isinstance(output_artifact, dict):
        errors.extend(validate_handoff_preservation(fixture, output_artifact))
        errors.extend(validate_forbidden_mutation_coverage(fixture))
    return errors


def mutate_without_first_unresolved_risk(artifact: dict[str, Any]) -> dict[str, Any]:
    mutated = copy.deepcopy(artifact)
    passport = process_passport(mutated)
    risks = string_list(passport.get("unresolved_risks"))
    passport["unresolved_risks"] = risks[1:] or ["Downstream-only risk."]
    return mutated


def mutate_to_full_text_verified(artifact: dict[str, Any]) -> dict[str, Any]:
    mutated = copy.deepcopy(artifact)
    passport = process_passport(mutated)
    passport["source_access_level"] = "full text verified"
    passport["evidence_status"] = "verified"
    return mutated


def mutate_to_drop_human_review(artifact: dict[str, Any]) -> dict[str, Any]:
    mutated = copy.deepcopy(artifact)
    passport = process_passport(mutated)
    passport["human_verification_status"] = "completed"
    return mutated


def validate_forbidden_mutation_coverage(fixture: dict[str, Any]) -> list[str]:
    output_artifact = fixture.get("expected_output_artifact")
    if not isinstance(output_artifact, dict):
        return []
    mutation_checks = [
        (
            "drops-unresolved-risk",
            mutate_without_first_unresolved_risk,
            "missing unresolved risk",
        ),
        (
            "upgrades-partial-source-access",
            mutate_to_full_text_verified,
            "full-text verification",
        ),
        (
            "drops-human-review-requirement",
            mutate_to_drop_human_review,
            "human-review requirement",
        ),
    ]
    errors: list[str] = []
    identifier = fixture_identifier(fixture)
    for mutation_id, mutate, expected_error in mutation_checks:
        mutation_errors = validate_handoff_preservation(fixture, mutate(output_artifact))
        if not any(expected_error in error for error in mutation_errors):
            errors.append(f"{identifier}: forbidden mutation {mutation_id!r} was not rejected")
    return errors


def duplicate_fixture_id_errors(fixtures: list[dict[str, Any]]) -> list[str]:
    seen: set[str] = set()
    errors: list[str] = []
    for fixture in fixtures:
        identifier = fixture_identifier(fixture)
        if identifier in seen:
            errors.append(f"duplicate fixture id {identifier!r}")
        seen.add(identifier)
    return errors


def validate_fixture_document(fixture_path: Path) -> list[str]:
    try:
        document = read_json_object(fixture_path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return [str(error)]

    fixtures = fixture_list(document)
    errors: list[str] = []
    if document.get("schema_version") != FIXTURE_SCHEMA_VERSION:
        errors.append(f"schema_version must be {FIXTURE_SCHEMA_VERSION}")
    if not fixtures:
        errors.append("fixtures must be a non-empty list of objects")
    errors.extend(object_list_item_errors(document, "fixtures"))
    errors.extend(duplicate_fixture_id_errors(fixtures))
    for fixture in fixtures:
        errors.extend(validate_fixture(fixture))
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fixtures",
        type=Path,
        default=DEFAULT_FIXTURES,
        help="Workflow passport fixture JSON document.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors = validate_fixture_document(args.fixtures)
    if errors:
        print("Workflow passport fixture check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("OK: workflow passport fixtures are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
