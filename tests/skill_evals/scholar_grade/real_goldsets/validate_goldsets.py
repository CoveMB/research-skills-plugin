#!/usr/bin/env python3
"""Validate real-source scholar-grade gold-set templates and cases."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


GOLDSET_SCHEMA_VERSION = "real-source-goldset-v1"
VALID_TASK_TYPES = {
    "retrieval",
    "synthesis",
    "citation-audit",
    "literature-map",
    "mixed",
}
VALID_STATUSES = {
    "inactive-template",
    "draft",
    "active",
    "retired",
}
REQUIRED_GOLDSET_FIELDS = (
    "schema_version",
    "status",
    "goldset_id",
    "domain",
    "task_type",
    "visible_prompt",
    "allowed_tools",
    "network_policy",
    "gold_sources",
    "acceptable_sources",
    "decoy_sources",
    "disallowed_sources",
    "required_distinctions",
    "must_support",
    "must_reject",
    "must_remain_uncertain",
    "citation_audit_expectations",
    "field_state_note",
    "human_review_required",
    "reviewer_notes",
    "last_reviewed_date",
    "source_access_notes",
)
SOURCE_LIST_FIELDS = (
    "gold_sources",
    "acceptable_sources",
    "decoy_sources",
    "disallowed_sources",
)
SOURCE_REQUIRED_FIELDS = (
    "title",
    "year",
    "locator_or_access_note",
    "role",
)
EXPECTATION_LIST_FIELDS = (
    "required_distinctions",
    "must_support",
    "must_reject",
    "must_remain_uncertain",
    "citation_audit_expectations",
)
EXPECTATION_REQUIRED_FIELDS = (
    "id",
    "expectation",
    "evidence_basis",
)
MINIMUM_FAILURE_CHECK_REQUIRED_FIELDS = (
    "id",
    "question",
    "failure_if",
    "passes_if",
    "evidence_basis",
)
CANDIDATE_OUTPUT_SCORECARD_REQUIRED_FIELDS = (
    "output_id",
    "output_label",
    "output_text",
    "score_basis",
)
CANDIDATE_CHECK_RESULT_REQUIRED_FIELDS = (
    "check_id",
    "outcome",
    "rationale",
    "evidence_basis",
)
SEARCH_LOG_SCOPE_WAIVER_REQUIRED_FIELDS = (
    "waiver_status",
    "approved_by",
    "approval_date",
    "waived_requirement",
    "scope_limit",
    "residual_risk",
)
VALID_CANDIDATE_CHECK_OUTCOMES = {
    "pass",
    "fail",
}
ACTIVE_PLACEHOLDER_RE = re.compile(
    r"\b(?:TODO|TBD|PLACEHOLDER|FILL[_ -]?ME|REPLACE[_ -]?ME)\b",
    flags=re.IGNORECASE,
)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PRIVATE_MANUSCRIPT_RE = re.compile(
    r"\b(?:private|confidential|unpublished)\b.{0,80}\b(?:manuscript|draft|source text|notes)\b"
    r"|\b(?:manuscript|draft)\b.{0,80}\b(?:excerpt|full text|raw text)\b",
    flags=re.IGNORECASE,
)
FORBIDDEN_TEXT_FIELD_PARTS = (
    "copyrighted_excerpt",
    "excerpt",
    "full_text",
    "private_manuscript_text",
    "quoted_text",
    "raw_text",
    "source_text",
)
MAX_ACTIVE_STRING_LENGTH = 1500
IGNORED_JSON_FILENAMES = {"goldset.schema.json"}


def path_label(parts: tuple[str, ...]) -> str:
    if not parts:
        return "<root>"
    return ".".join(parts)


def is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def string_list_errors(value: Any, parts: tuple[str, ...]) -> list[str]:
    label = path_label(parts)
    if not isinstance(value, list):
        return [f"{label} must be a list"]
    errors: list[str] = []
    for index, item in enumerate(value):
        if not is_non_empty_string(item):
            errors.append(f"{label}[{index}] must be a non-empty string")
    return errors


def has_author_or_authoring_body(source: dict[str, Any]) -> bool:
    authors = source.get("authors")
    if isinstance(authors, list) and any(is_non_empty_string(author) for author in authors):
        return True
    return is_non_empty_string(source.get("authoring_body"))


def has_usable_year(source: dict[str, Any]) -> bool:
    if "year" not in source:
        return False
    year = source.get("year")
    if isinstance(year, int):
        return True
    return is_non_empty_string(year)


def has_required_source_field(source: dict[str, Any], field: str) -> bool:
    if field == "year":
        return has_usable_year(source)
    return is_non_empty_string(source.get(field))


def is_active_goldset(document: dict[str, Any]) -> bool:
    return document.get("status") == "active"


def is_placeholder_value(value: str) -> bool:
    return bool(ACTIVE_PLACEHOLDER_RE.search(value))


def validate_required_fields(document: dict[str, Any]) -> list[str]:
    return [f"{field} is required" for field in REQUIRED_GOLDSET_FIELDS if field not in document]


def validate_top_level_fields(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if document.get("schema_version") != GOLDSET_SCHEMA_VERSION:
        errors.append(f"schema_version must be {GOLDSET_SCHEMA_VERSION!r}")

    status = document.get("status")
    if status not in VALID_STATUSES:
        errors.append(f"status must be one of {sorted(VALID_STATUSES)}")

    task_type = document.get("task_type")
    if task_type not in VALID_TASK_TYPES:
        errors.append(f"task_type must be one of {sorted(VALID_TASK_TYPES)}")

    for field in (
        "goldset_id",
        "domain",
        "visible_prompt",
        "network_policy",
        "field_state_note",
        "reviewer_notes",
        "last_reviewed_date",
        "source_access_notes",
    ):
        if field in document and not is_non_empty_string(document[field]):
            errors.append(f"{field} must be a non-empty string")

    if "allowed_tools" in document:
        errors.extend(string_list_errors(document["allowed_tools"], ("allowed_tools",)))

    if "human_review_required" in document and not isinstance(document["human_review_required"], bool):
        errors.append("human_review_required must be a boolean")

    if document.get("status") == "active" and not DATE_RE.fullmatch(str(document.get("last_reviewed_date", ""))):
        errors.append("active gold set last_reviewed_date must use YYYY-MM-DD")

    return errors


def validate_source_entry(source: Any, parts: tuple[str, ...]) -> list[str]:
    label = path_label(parts)
    if not isinstance(source, dict):
        return [f"{label} must be an object"]

    errors = [
        f"{label}.{field} is required"
        for field in SOURCE_REQUIRED_FIELDS
        if field not in source or not has_required_source_field(source, field)
    ]
    if not has_author_or_authoring_body(source):
        errors.append(f"{label} must include non-empty authors or authoring_body")
    if parts and parts[0] == "decoy_sources" and not is_non_empty_string(source.get("decoy_reason")):
        errors.append(f"{label}.decoy_reason is required for decoy sources")
    return errors


def validate_source_list(document: dict[str, Any], field: str) -> list[str]:
    value = document.get(field)
    if not isinstance(value, list):
        return [f"{field} must be a list"]
    errors: list[str] = []
    for index, source in enumerate(value):
        errors.extend(validate_source_entry(source, (field, str(index))))
    return errors


def validate_expectation_entry(expectation: Any, parts: tuple[str, ...]) -> list[str]:
    label = path_label(parts)
    if not isinstance(expectation, dict):
        return [f"{label} must be an object"]
    return missing_string_field_errors(expectation, EXPECTATION_REQUIRED_FIELDS, label)


def validate_expectation_list(document: dict[str, Any], field: str) -> list[str]:
    value = document.get(field)
    if not isinstance(value, list):
        return [f"{field} must be a list"]
    errors: list[str] = []
    for index, expectation in enumerate(value):
        errors.extend(validate_expectation_entry(expectation, (field, str(index))))
    return errors


def missing_string_field_errors(
    value: dict[str, Any],
    required_fields: tuple[str, ...],
    label: str,
) -> list[str]:
    return [
        f"{label}.{field} is required"
        for field in required_fields
        if not is_non_empty_string(value.get(field))
    ]


def duplicate_values(values: list[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return sorted(duplicates)


def validate_minimum_failure_check_entry(check: Any, index: int) -> list[str]:
    label = f"minimum_failure_checks[{index}]"
    if not isinstance(check, dict):
        return [f"{label} must be an object"]
    return missing_string_field_errors(check, MINIMUM_FAILURE_CHECK_REQUIRED_FIELDS, label)


def validate_minimum_failure_checks(document: dict[str, Any]) -> list[str]:
    checks = document.get("minimum_failure_checks")
    if checks is None:
        return []
    if not isinstance(checks, list):
        return ["minimum_failure_checks must be a list"]

    errors: list[str] = []
    check_identifiers: list[str] = []
    for index, check in enumerate(checks):
        errors.extend(validate_minimum_failure_check_entry(check, index))
        if isinstance(check, dict) and is_non_empty_string(check.get("id")):
            check_identifiers.append(check["id"])

    for identifier in duplicate_values(check_identifiers):
        errors.append(f"minimum_failure_checks contains duplicate id: {identifier}")
    return errors


def minimum_failure_check_ids(document: dict[str, Any]) -> list[str]:
    checks = document.get("minimum_failure_checks")
    if not isinstance(checks, list):
        return []
    return [
        check["id"]
        for check in checks
        if isinstance(check, dict) and is_non_empty_string(check.get("id"))
    ]


def validate_candidate_check_result_entry(result: Any, label: str) -> list[str]:
    if not isinstance(result, dict):
        return [f"{label} must be an object"]

    errors = missing_string_field_errors(result, CANDIDATE_CHECK_RESULT_REQUIRED_FIELDS, label)
    outcome = result.get("outcome")
    if is_non_empty_string(outcome) and outcome not in VALID_CANDIDATE_CHECK_OUTCOMES:
        errors.append(f"{label}.outcome must be one of {sorted(VALID_CANDIDATE_CHECK_OUTCOMES)}")
    return errors


def validate_candidate_check_results(
    scorecard: dict[str, Any],
    label: str,
    expected_check_identifiers: list[str],
) -> list[str]:
    results = scorecard.get("check_results")
    if not isinstance(results, list):
        return [f"{label}.check_results must be a list"]

    errors: list[str] = []
    result_identifiers: list[str] = []
    for index, result in enumerate(results):
        result_label = f"{label}.check_results[{index}]"
        errors.extend(validate_candidate_check_result_entry(result, result_label))
        if isinstance(result, dict) and is_non_empty_string(result.get("check_id")):
            result_identifiers.append(result["check_id"])

    for identifier in duplicate_values(result_identifiers):
        errors.append(f"{label} contains duplicate check result: {identifier}")

    expected_identifiers = set(expected_check_identifiers)
    actual_identifiers = set(result_identifiers)
    missing_identifiers = sorted(expected_identifiers - actual_identifiers)
    unknown_identifiers = sorted(actual_identifiers - expected_identifiers)
    if missing_identifiers:
        errors.append(
            f"{label} is missing check results for minimum_failure_checks: "
            f"{', '.join(missing_identifiers)}"
        )
    if unknown_identifiers:
        errors.append(
            f"{label} contains check results not listed in minimum_failure_checks: "
            f"{', '.join(unknown_identifiers)}"
        )
    return errors


def validate_candidate_output_scorecard_entry(
    scorecard: Any,
    index: int,
    expected_check_identifiers: list[str],
) -> list[str]:
    label = f"candidate_output_scorecards[{index}]"
    if not isinstance(scorecard, dict):
        return [f"{label} must be an object"]

    errors = missing_string_field_errors(
        scorecard,
        CANDIDATE_OUTPUT_SCORECARD_REQUIRED_FIELDS,
        label,
    )
    errors.extend(validate_candidate_check_results(scorecard, label, expected_check_identifiers))
    return errors


def validate_candidate_output_scorecards(document: dict[str, Any]) -> list[str]:
    scorecards = document.get("candidate_output_scorecards")
    if scorecards is None:
        return []
    if not isinstance(scorecards, list):
        return ["candidate_output_scorecards must be a list"]

    check_identifiers = minimum_failure_check_ids(document)
    if not check_identifiers:
        return ["candidate_output_scorecards require minimum_failure_checks"]

    errors: list[str] = []
    output_identifiers: list[str] = []
    for index, scorecard in enumerate(scorecards):
        errors.extend(validate_candidate_output_scorecard_entry(scorecard, index, check_identifiers))
        if isinstance(scorecard, dict) and is_non_empty_string(scorecard.get("output_id")):
            output_identifiers.append(scorecard["output_id"])

    for identifier in duplicate_values(output_identifiers):
        errors.append(f"candidate_output_scorecards contains duplicate output_id: {identifier}")
    return errors


def validate_search_log_scope_waiver(document: dict[str, Any]) -> list[str]:
    waiver = document.get("search_log_scope_waiver")
    if waiver is None:
        return []
    if not isinstance(waiver, dict):
        return ["search_log_scope_waiver must be an object"]

    errors = missing_string_field_errors(
        waiver,
        SEARCH_LOG_SCOPE_WAIVER_REQUIRED_FIELDS,
        "search_log_scope_waiver",
    )
    if is_active_goldset(document) and waiver.get("waiver_status") != "approved":
        errors.append("active gold set search_log_scope_waiver.waiver_status must be 'approved'")
    if is_non_empty_string(waiver.get("approval_date")) and not DATE_RE.fullmatch(waiver["approval_date"]):
        errors.append("search_log_scope_waiver.approval_date must use YYYY-MM-DD")
    return errors


def validate_human_review_gate(document: dict[str, Any]) -> list[str]:
    if document.get("human_review_required") is True:
        return []
    rationale = document.get("human_review_waiver_rationale")
    if is_non_empty_string(rationale) and not is_placeholder_value(rationale):
        return []
    return ["human_review_required must be true unless human_review_waiver_rationale is explicit"]


def walk_json_values(value: Any, parts: tuple[str, ...] = ()) -> list[tuple[tuple[str, ...], Any]]:
    walked = [(parts, value)]
    if isinstance(value, dict):
        for key, child in value.items():
            walked.extend(walk_json_values(child, (*parts, str(key))))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            walked.extend(walk_json_values(child, (*parts, str(index))))
    return walked


def validate_active_placeholders(document: dict[str, Any]) -> list[str]:
    if not is_active_goldset(document):
        return []
    errors: list[str] = []
    for parts, value in walk_json_values(document):
        if isinstance(value, str) and is_placeholder_value(value):
            errors.append(f"active gold set contains placeholder at {path_label(parts)}")
    return errors


def validate_stored_text_limits(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for parts, value in walk_json_values(document):
        key = parts[-1].lower() if parts else ""
        if any(part in key for part in FORBIDDEN_TEXT_FIELD_PARTS):
            errors.append(f"{path_label(parts)} must not store source excerpts or full text")
        if isinstance(value, str) and PRIVATE_MANUSCRIPT_RE.search(value):
            errors.append(f"{path_label(parts)} appears to include private unpublished manuscript text")
        if is_active_goldset(document) and isinstance(value, str) and len(value) > MAX_ACTIVE_STRING_LENGTH:
            errors.append(f"{path_label(parts)} is too long for gold-set metadata or review notes")
    return errors


def validate_goldset_document(document: Any) -> list[str]:
    if not isinstance(document, dict):
        return ["gold set file must contain a JSON object"]

    errors: list[str] = []
    errors.extend(validate_required_fields(document))
    errors.extend(validate_top_level_fields(document))
    for field in SOURCE_LIST_FIELDS:
        if field in document:
            errors.extend(validate_source_list(document, field))
    for field in EXPECTATION_LIST_FIELDS:
        if field in document:
            errors.extend(validate_expectation_list(document, field))
    errors.extend(validate_minimum_failure_checks(document))
    errors.extend(validate_candidate_output_scorecards(document))
    errors.extend(validate_search_log_scope_waiver(document))
    errors.extend(validate_human_review_gate(document))
    errors.extend(validate_active_placeholders(document))
    errors.extend(validate_stored_text_limits(document))
    return errors


def load_json_object(path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        return None, [f"{path}: invalid JSON: {error}"]
    if not isinstance(data, dict):
        return None, [f"{path}: JSON document must be an object"]
    return data, []


def candidate_goldset_paths(root: Path) -> list[Path]:
    if root.is_file():
        return [root]
    return sorted(
        path
        for path in root.glob("*.json")
        if path.name not in IGNORED_JSON_FILENAMES and not path.name.startswith("test_")
    )


def validate_goldset_path(path: Path) -> list[str]:
    document, errors = load_json_object(path)
    if errors:
        return errors
    assert document is not None
    return [f"{path}: {error}" for error in validate_goldset_document(document)]


def validate_goldset_paths(paths: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in paths:
        errors.extend(validate_goldset_path(path))
    return errors


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Gold-set JSON files or directories to validate. Defaults to this directory.",
    )
    return parser.parse_args(argv)


def expanded_candidate_paths(paths: list[Path]) -> list[Path]:
    candidates: list[Path] = []
    for path in paths:
        candidates.extend(candidate_goldset_paths(path))
    return sorted(dict.fromkeys(candidates))


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    roots = args.paths or [Path(__file__).resolve().parent]
    paths = expanded_candidate_paths([path.resolve() for path in roots])
    errors = validate_goldset_paths(paths)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"Validated {len(paths)} real-source gold-set file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
