#!/usr/bin/env python3
"""Check research behavior fixture documents and captured local outputs."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


REQUIRED_FIXTURE_KEYS = {
    "id",
    "prompt",
    "expected_route",
    "risk_covered",
    "required_output_markers",
    "forbidden_claims",
}
COMPACT_RESULT_MARKERS = [
    "How to use this result",
    "Next action",
]
HIGH_RISK_OVERSTATEMENT_ROUTES = frozenset(
    [
        "claim-evidence-ledger",
        "literature-review-mapper",
        "methodology-source-auditor",
        "systematic-source-discovery",
        "citation-integrity-auditor",
        "scholarly-integrity-gate",
        "book-proposal-scholarship",
        "book-comps-verifier",
    ]
)
OVERSTATEMENT_POLICY_REQUIRED_MARKERS = [
    "Source basis",
    "What I can verify",
    "What remains uncertain",
    "User verification needed",
]
OVERSTATEMENT_POLICY_FORBIDDEN_CLAIMS = [
    "field consensus is established",
    "field consensus is settled",
    "the field agrees",
    "the literature proves",
    "abstract proves causation",
    "abstract confirms causation",
    "abstract establishes causality",
    "citation-only record supports the claim",
    "source support verified from citation only",
    "submission-ready",
    "verified and cleared",
    "cleared for submission",
    "Gate decision: pass",
    "verification passed",
    "upstream uncertainty is resolved",
    "unverified claim is now verified",
    "novelty established",
    "no prior work exists",
    "absence of evidence proves",
]
OPTIONAL_REGEX_LIST_KEYS = {
    "required_output_patterns",
    "forbidden_output_patterns",
}
FIXTURE_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REQUIRED_TRACE_KEYS = {
    "schema_version",
    "fixture_id",
    "prompt_sha256",
    "output_sha256",
    "selected_skill",
    "skill_invoked",
    "prompt_supplied",
    "output_captured",
}
REQUIRED_TRUE_TRACE_KEYS = {
    "skill_invoked",
    "prompt_supplied",
    "output_captured",
}
TRACE_SCHEMA_VERSION = "research-behavior-route-trace-v2"


def read_json_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} root must be an object")
    return payload


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fixture_list(document: dict[str, Any]) -> list[dict[str, Any]]:
    fixtures = document.get("fixtures")
    if not isinstance(fixtures, list):
        return []
    return [fixture for fixture in fixtures if isinstance(fixture, dict)]


def string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def is_compact_fixture(fixture: dict[str, Any]) -> bool:
    risk = str(fixture.get("risk_covered", ""))
    required_markers = string_list(fixture.get("required_output_markers"))
    return risk.startswith("compact ") or all(marker in required_markers for marker in COMPACT_RESULT_MARKERS)


def is_high_risk_overstatement_fixture(fixture: dict[str, Any]) -> bool:
    return str(fixture.get("expected_route", "")) in HIGH_RISK_OVERSTATEMENT_ROUTES


def normalized_contains(text: str, phrase: str) -> bool:
    return phrase.casefold() in text.casefold()


def normalized_count(text: str, phrase: str) -> int:
    return text.casefold().count(phrase.casefold())


def fixture_identifier(fixture: dict[str, Any]) -> str:
    value = fixture.get("id")
    return value if isinstance(value, str) and value else "<missing id>"


def invalid_fixture_id_errors(fixture: dict[str, Any]) -> list[str]:
    identifier = fixture_identifier(fixture)
    return [] if FIXTURE_ID_RE.match(identifier) else [f"{identifier}: id must be lowercase kebab-case"]


def output_filename_for_fixture(fixture: dict[str, Any]) -> str:
    identifier = fixture_identifier(fixture)
    return f"{identifier}.md" if FIXTURE_ID_RE.match(identifier) else "invalid-fixture-id.md"


def missing_fixture_keys(fixture: dict[str, Any]) -> list[str]:
    return [
        f"{fixture_identifier(fixture)}: missing key {key!r}"
        for key in sorted(REQUIRED_FIXTURE_KEYS)
        if key not in fixture
    ]


def invalid_fixture_lists(fixture: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key in ["required_output_markers", "forbidden_claims"]:
        value = fixture.get(key)
        if not isinstance(value, list) or not value or len(string_list(value)) != len(value):
            errors.append(f"{fixture_identifier(fixture)}: {key} must be a non-empty string list")
    return errors


def missing_overstatement_policy_marker_errors(fixture: dict[str, Any]) -> list[str]:
    if not is_high_risk_overstatement_fixture(fixture):
        return []

    required_markers = string_list(fixture.get("required_output_markers"))
    return [
        (
            f"{fixture_identifier(fixture)}: high-risk overstatement policy "
            f"requires required marker {marker!r}"
        )
        for marker in OVERSTATEMENT_POLICY_REQUIRED_MARKERS
        if marker not in required_markers
    ]


def invalid_optional_boolean_errors(fixture: dict[str, Any]) -> list[str]:
    if "should_trigger" not in fixture or isinstance(fixture.get("should_trigger"), bool):
        return []
    return [f"{fixture_identifier(fixture)}: should_trigger must be a boolean"]


def invalid_optional_regex_list_errors(fixture: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key in sorted(OPTIONAL_REGEX_LIST_KEYS):
        if key not in fixture:
            continue
        value = fixture.get(key)
        patterns = string_list(value)
        if not isinstance(value, list) or len(patterns) != len(value):
            errors.append(f"{fixture_identifier(fixture)}: {key} must be a string list when present")
            continue
        for pattern in patterns:
            try:
                re.compile(pattern)
            except re.error:
                errors.append(f"{fixture_identifier(fixture)}: invalid {key} regex {pattern!r}")
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
    if document.get("schema_version") != "research-skill-behavior-fixtures-v1":
        errors.append("schema_version must be research-skill-behavior-fixtures-v1")
    if not fixtures:
        errors.append("fixtures must be a non-empty list of objects")

    errors.extend(duplicate_fixture_id_errors(fixtures))
    for fixture in fixtures:
        errors.extend(missing_fixture_keys(fixture))
        errors.extend(invalid_fixture_id_errors(fixture))
        errors.extend(invalid_fixture_lists(fixture))
        errors.extend(missing_overstatement_policy_marker_errors(fixture))
        errors.extend(invalid_optional_boolean_errors(fixture))
        errors.extend(invalid_optional_regex_list_errors(fixture))
    return errors


def output_path_for_fixture(outputs_dir: Path, fixture: dict[str, Any]) -> Path:
    return outputs_dir / output_filename_for_fixture(fixture)


def trace_filename_for_fixture(fixture: dict[str, Any]) -> str:
    identifier = fixture_identifier(fixture)
    return f"{identifier}.json" if FIXTURE_ID_RE.match(identifier) else "invalid-fixture-id.json"


def trace_path_for_fixture(traces_dir: Path, fixture: dict[str, Any]) -> Path:
    return traces_dir / trace_filename_for_fixture(fixture)


def required_marker_errors(fixture: dict[str, Any], output_text: str) -> list[str]:
    return [
        f"{fixture_identifier(fixture)}: missing required marker {marker!r}"
        for marker in string_list(fixture.get("required_output_markers"))
        if not normalized_contains(output_text, marker)
    ]


def forbidden_claims_for_fixture(fixture: dict[str, Any]) -> list[str]:
    fixture_claims = string_list(fixture.get("forbidden_claims"))
    if not is_high_risk_overstatement_fixture(fixture):
        return fixture_claims
    return list(dict.fromkeys([*fixture_claims, *OVERSTATEMENT_POLICY_FORBIDDEN_CLAIMS]))


def forbidden_claim_errors(fixture: dict[str, Any], output_text: str) -> list[str]:
    return [
        f"{fixture_identifier(fixture)}: contains forbidden claim {claim!r}"
        for claim in forbidden_claims_for_fixture(fixture)
        if normalized_contains(output_text, claim)
    ]


def required_output_pattern_errors(fixture: dict[str, Any], output_text: str) -> list[str]:
    return [
        f"{fixture_identifier(fixture)}: missing required output pattern {pattern!r}"
        for pattern in string_list(fixture.get("required_output_patterns"))
        if re.search(pattern, output_text) is None
    ]


def forbidden_output_pattern_errors(fixture: dict[str, Any], output_text: str) -> list[str]:
    return [
        f"{fixture_identifier(fixture)}: matches forbidden output pattern {pattern!r}"
        for pattern in string_list(fixture.get("forbidden_output_patterns"))
        if re.search(pattern, output_text) is not None
    ]


def compact_marker_count_errors(fixture: dict[str, Any], output_text: str) -> list[str]:
    if not is_compact_fixture(fixture):
        return []

    errors: list[str] = []
    for marker in COMPACT_RESULT_MARKERS:
        count = normalized_count(output_text, marker)
        if count != 1:
            errors.append(f"{fixture_identifier(fixture)}: expected exactly 1 {marker!r}, found {count}")
    return errors


def selected_skill_route_errors(fixture: dict[str, Any], output_text: str) -> list[str]:
    expected_route = str(fixture.get("expected_route", ""))
    if not expected_route or normalized_contains(output_text, expected_route):
        return []
    return [
        f"{fixture_identifier(fixture)}: missing selected skill route evidence {expected_route!r}"
    ]


def validate_output_for_fixture(outputs_dir: Path, fixture: dict[str, Any]) -> list[str]:
    identifier_errors = invalid_fixture_id_errors(fixture)
    if identifier_errors:
        return identifier_errors
    output_path = output_path_for_fixture(outputs_dir, fixture)
    if not output_path.exists():
        return [f"{fixture_identifier(fixture)}: missing output file {output_path.name}"]

    output_text = output_path.read_text(encoding="utf-8")
    return [
        *selected_skill_route_errors(fixture, output_text),
        *required_marker_errors(fixture, output_text),
        *required_output_pattern_errors(fixture, output_text),
        *forbidden_claim_errors(fixture, output_text),
        *forbidden_output_pattern_errors(fixture, output_text),
        *compact_marker_count_errors(fixture, output_text),
    ]


def validate_fixture_outputs(fixture_path: Path, outputs_dir: Path) -> list[str]:
    document_errors = validate_fixture_document(fixture_path)
    if document_errors:
        return document_errors

    document = read_json_object(fixture_path)
    return [
        error
        for fixture in fixture_list(document)
        for error in validate_output_for_fixture(outputs_dir, fixture)
    ]


def trace_missing_key_errors(fixture: dict[str, Any], trace_document: dict[str, Any]) -> list[str]:
    return [
        f"{fixture_identifier(fixture)}: trace missing key {key!r}"
        for key in sorted(REQUIRED_TRACE_KEYS)
        if key not in trace_document
    ]


def trace_identity_errors(fixture: dict[str, Any], trace_document: dict[str, Any]) -> list[str]:
    identifier = fixture_identifier(fixture)
    expected_route = str(fixture.get("expected_route", ""))
    expected_prompt_sha256 = sha256_text(str(fixture.get("prompt", "")))
    checks = [
        ("schema_version", TRACE_SCHEMA_VERSION, f"schema_version {TRACE_SCHEMA_VERSION!r}"),
        ("fixture_id", identifier, f"fixture_id {identifier!r}"),
        ("selected_skill", expected_route, f"selected_skill must match expected_route {expected_route!r}"),
        ("prompt_sha256", expected_prompt_sha256, "prompt_sha256 does not match fixture prompt"),
    ]
    return [
        f"{identifier}: trace {message}"
        for key, expected_value, message in checks
        if key in trace_document and trace_document.get(key) != expected_value
    ]


def trace_output_hash_errors(
    outputs_dir: Path | None,
    fixture: dict[str, Any],
    trace_document: dict[str, Any],
) -> list[str]:
    if outputs_dir is None or "output_sha256" not in trace_document:
        return []

    output_path = output_path_for_fixture(outputs_dir, fixture)
    if not output_path.exists():
        return [
            f"{fixture_identifier(fixture)}: cannot validate trace output_sha256 without output file {output_path.name}"
        ]
    if trace_document.get("output_sha256") != sha256_file(output_path):
        return [f"{fixture_identifier(fixture)}: trace output_sha256 does not match captured output"]
    return []


def trace_boolean_errors(fixture: dict[str, Any], trace_document: dict[str, Any]) -> list[str]:
    errors = [
        f"{fixture_identifier(fixture)}: trace {key} must be true"
        for key in sorted(REQUIRED_TRUE_TRACE_KEYS - {"skill_invoked"})
        if trace_document.get(key) is not True
    ]
    should_trigger = fixture.get("should_trigger", True)
    if should_trigger is False:
        if trace_document.get("skill_invoked") is not False:
            errors.append(f"{fixture_identifier(fixture)}: trace skill_invoked must be false")
    elif trace_document.get("skill_invoked") is not True:
        errors.append(f"{fixture_identifier(fixture)}: trace skill_invoked must be true")
    return errors


def validate_trace_for_fixture(
    traces_dir: Path,
    fixture: dict[str, Any],
    outputs_dir: Path | None = None,
) -> list[str]:
    identifier_errors = invalid_fixture_id_errors(fixture)
    if identifier_errors:
        return identifier_errors
    trace_path = trace_path_for_fixture(traces_dir, fixture)
    if not trace_path.exists():
        return [f"{fixture_identifier(fixture)}: missing trace file {trace_path.name}"]
    try:
        trace_document = read_json_object(trace_path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return [f"{fixture_identifier(fixture)}: trace {error}"]
    return [
        *trace_missing_key_errors(fixture, trace_document),
        *trace_identity_errors(fixture, trace_document),
        *trace_output_hash_errors(outputs_dir, fixture, trace_document),
        *trace_boolean_errors(fixture, trace_document),
    ]


def validate_fixture_traces(
    fixture_path: Path,
    traces_dir: Path,
    outputs_dir: Path | None = None,
) -> list[str]:
    document_errors = validate_fixture_document(fixture_path)
    if document_errors:
        return document_errors

    document = read_json_object(fixture_path)
    return [
        error
        for fixture in fixture_list(document)
        for error in validate_trace_for_fixture(traces_dir, fixture, outputs_dir)
    ]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", type=Path, required=True, help="Fixture JSON file to check.")
    parser.add_argument(
        "--outputs-dir",
        type=Path,
        help="Directory containing one captured output markdown file per fixture id.",
    )
    parser.add_argument(
        "--traces-dir",
        type=Path,
        help="Directory containing one route trace JSON file per fixture id.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    errors = validate_fixture_document(args.fixtures)
    if not errors and args.outputs_dir:
        errors.extend(validate_fixture_outputs(args.fixtures, args.outputs_dir))
    if not errors and args.traces_dir:
        errors.extend(validate_fixture_traces(args.fixtures, args.traces_dir, args.outputs_dir))
    if errors:
        print("Research behavior fixture check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("OK: research behavior fixtures are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
