#!/usr/bin/env python3
"""Validate book artifact schema and shipped examples."""
from __future__ import annotations

import argparse
import json
import sys
from json import JSONDecodeError
from pathlib import Path
from typing import Any


SCHEMA_RELATIVE_PATH = Path("shared/contracts/book/book_artifact.schema.json")
EXAMPLES_RELATIVE_DIR = Path("examples/book_artifacts")


def load_json(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except JSONDecodeError as exc:
        return None, f"{path}: malformed JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"
    except OSError as exc:
        return None, f"{path}: unable to read file: {exc}"

    if not isinstance(payload, dict):
        return None, f"{path}: JSON root must be an object"
    return payload, None


def location(path_parts: list[str]) -> str:
    return "/".join(path_parts) if path_parts else "<root>"


def resolve_reference(schema: dict[str, Any], reference: str) -> dict[str, Any] | None:
    if not reference.startswith("#/"):
        return None

    value: Any = schema
    for part in reference[2:].split("/"):
        if not isinstance(value, dict) or part not in value:
            return None
        value = value[part]
    return value if isinstance(value, dict) else None


def value_matches_type(value: Any, expected_type: str) -> bool:
    type_checkers = {
        "object": lambda item: isinstance(item, dict),
        "array": lambda item: isinstance(item, list),
        "string": lambda item: isinstance(item, str),
        "integer": lambda item: isinstance(item, int) and not isinstance(item, bool),
        "boolean": lambda item: isinstance(item, bool),
    }
    checker = type_checkers.get(expected_type)
    return True if checker is None else checker(value)


def condition_matches(schema: dict[str, Any], condition: dict[str, Any], value: Any) -> bool:
    return validate_value(schema, condition, value, []) == []


def validate_string(value: str, subschema: dict[str, Any], path_parts: list[str]) -> list[str]:
    minimum_length = subschema.get("minLength")
    if isinstance(minimum_length, int) and len(value) < minimum_length:
        return [f"string shorter than minLength {minimum_length} at {location(path_parts)}"]
    return []


def validate_number(value: int, subschema: dict[str, Any], path_parts: list[str]) -> list[str]:
    minimum = subschema.get("minimum")
    if isinstance(minimum, int | float) and value < minimum:
        return [f"number below minimum {minimum} at {location(path_parts)}"]
    return []


def validate_array(
    schema: dict[str, Any],
    subschema: dict[str, Any],
    value: list[Any],
    path_parts: list[str],
) -> list[str]:
    errors: list[str] = []
    minimum_items = subschema.get("minItems")
    if isinstance(minimum_items, int) and len(value) < minimum_items:
        errors.append(f"array shorter than minItems {minimum_items} at {location(path_parts)}")

    items_schema = subschema.get("items")
    if isinstance(items_schema, dict):
        for index, item in enumerate(value):
            errors.extend(validate_value(schema, items_schema, item, [*path_parts, str(index)]))
    return errors


def validate_object(
    schema: dict[str, Any],
    subschema: dict[str, Any],
    value: dict[str, Any],
    path_parts: list[str],
) -> list[str]:
    errors: list[str] = []
    properties = subschema.get("properties")
    properties = properties if isinstance(properties, dict) else {}

    required = subschema.get("required")
    if isinstance(required, list):
        for key in required:
            if isinstance(key, str) and key not in value:
                errors.append(f"missing required property {key!r} at {location(path_parts)}")

    for key, property_schema in properties.items():
        if key in value and isinstance(property_schema, dict):
            errors.extend(validate_value(schema, property_schema, value[key], [*path_parts, key]))

    if subschema.get("additionalProperties") is False:
        allowed = set(properties.keys())
        for key in value:
            if key not in allowed:
                errors.append(f"unexpected property {key!r} at {location(path_parts)}")

    return errors


def validate_conditionals(
    schema: dict[str, Any],
    subschema: dict[str, Any],
    value: Any,
    path_parts: list[str],
) -> list[str]:
    errors: list[str] = []
    all_of = subschema.get("allOf")
    if not isinstance(all_of, list):
        return errors

    for branch in all_of:
        if not isinstance(branch, dict):
            continue
        condition = branch.get("if")
        then_schema = branch.get("then")
        if isinstance(condition, dict) and isinstance(then_schema, dict):
            if condition_matches(schema, condition, value):
                errors.extend(validate_value(schema, then_schema, value, path_parts))
        else:
            errors.extend(validate_value(schema, branch, value, path_parts))
    return errors


def validate_value(
    schema: dict[str, Any],
    subschema: dict[str, Any],
    value: Any,
    path_parts: list[str],
) -> list[str]:
    reference = subschema.get("$ref")
    if isinstance(reference, str):
        resolved = resolve_reference(schema, reference)
        if resolved is None:
            return [f"unresolved schema reference {reference!r} at {location(path_parts)}"]
        return validate_value(schema, resolved, value, path_parts)

    errors: list[str] = []
    expected_type = subschema.get("type")
    if isinstance(expected_type, str) and not value_matches_type(value, expected_type):
        return [f"expected {expected_type} at {location(path_parts)}"]

    if "const" in subschema and value != subschema["const"]:
        errors.append(f"expected const {subschema['const']!r} at {location(path_parts)}")

    enum = subschema.get("enum")
    if isinstance(enum, list) and value not in enum:
        errors.append(f"expected one of {enum!r} at {location(path_parts)}")

    if isinstance(value, str):
        errors.extend(validate_string(value, subschema, path_parts))
    if isinstance(value, int) and not isinstance(value, bool):
        errors.extend(validate_number(value, subschema, path_parts))
    if isinstance(value, list):
        errors.extend(validate_array(schema, subschema, value, path_parts))
    if isinstance(value, dict):
        errors.extend(validate_object(schema, subschema, value, path_parts))

    errors.extend(validate_conditionals(schema, subschema, value, path_parts))
    return errors


def validate_schema(schema_path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    if not schema_path.is_file():
        return None, [f"{schema_path}: missing book_artifact.schema.json"]

    schema, error = load_json(schema_path)
    if error is not None:
        return None, [error]
    assert schema is not None

    properties = schema.get("properties")
    if not isinstance(properties, dict) or "artifact_type" not in properties:
        return None, [f"{schema_path}: missing artifact_type schema property"]
    return schema, []


def example_files(examples_dir: Path) -> tuple[list[Path], list[str]]:
    if not examples_dir.is_dir():
        return [], [f"{examples_dir}: missing book artifact examples directory"]

    files = sorted(examples_dir.glob("*.json"))
    if not files:
        return [], [f"{examples_dir}: no book artifact examples found"]
    return files, []


def validate_examples(schema: dict[str, Any], files: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in files:
        payload, error = load_json(path)
        if error is not None:
            errors.append(error)
            continue
        assert payload is not None
        for validation_error in validate_value(schema, schema, payload, []):
            errors.append(f"{path}: {validation_error}")
    return errors


def check(root: Path) -> list[str]:
    schema, errors = validate_schema(root / SCHEMA_RELATIVE_PATH)
    if schema is None:
        return errors

    files, example_errors = example_files(root / EXAMPLES_RELATIVE_DIR)
    errors.extend(example_errors)
    if example_errors:
        return errors

    errors.extend(validate_examples(schema, files))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()

    errors = check(args.path.resolve())
    if errors:
        print("Book artifact contract check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("OK: book artifact contract schema and examples are valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
