#!/usr/bin/env python3
"""Check research behavior fixture documents and captured local outputs."""
from __future__ import annotations

import argparse
import json
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


def string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def is_compact_fixture(fixture: dict[str, Any]) -> bool:
    risk = str(fixture.get("risk_covered", ""))
    required_markers = string_list(fixture.get("required_output_markers"))
    return risk.startswith("compact ") or all(marker in required_markers for marker in COMPACT_RESULT_MARKERS)


def normalized_contains(text: str, phrase: str) -> bool:
    return phrase.casefold() in text.casefold()


def normalized_count(text: str, phrase: str) -> int:
    return text.casefold().count(phrase.casefold())


def fixture_identifier(fixture: dict[str, Any]) -> str:
    value = fixture.get("id")
    return value if isinstance(value, str) and value else "<missing id>"


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
        errors.extend(invalid_fixture_lists(fixture))
    return errors


def output_path_for_fixture(outputs_dir: Path, fixture: dict[str, Any]) -> Path:
    return outputs_dir / f"{fixture_identifier(fixture)}.md"


def required_marker_errors(fixture: dict[str, Any], output_text: str) -> list[str]:
    return [
        f"{fixture_identifier(fixture)}: missing required marker {marker!r}"
        for marker in string_list(fixture.get("required_output_markers"))
        if not normalized_contains(output_text, marker)
    ]


def forbidden_claim_errors(fixture: dict[str, Any], output_text: str) -> list[str]:
    return [
        f"{fixture_identifier(fixture)}: contains forbidden claim {claim!r}"
        for claim in string_list(fixture.get("forbidden_claims"))
        if normalized_contains(output_text, claim)
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


def validate_output_for_fixture(outputs_dir: Path, fixture: dict[str, Any]) -> list[str]:
    output_path = output_path_for_fixture(outputs_dir, fixture)
    if not output_path.exists():
        return [f"{fixture_identifier(fixture)}: missing output file {output_path.name}"]

    output_text = output_path.read_text(encoding="utf-8")
    return [
        *required_marker_errors(fixture, output_text),
        *forbidden_claim_errors(fixture, output_text),
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


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", type=Path, required=True, help="Fixture JSON file to check.")
    parser.add_argument(
        "--outputs-dir",
        type=Path,
        help="Directory containing one captured output markdown file per fixture id.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    errors = (
        validate_fixture_outputs(args.fixtures, args.outputs_dir)
        if args.outputs_dir
        else validate_fixture_document(args.fixtures)
    )
    if errors:
        print("Research behavior fixture check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("OK: research behavior fixtures are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
