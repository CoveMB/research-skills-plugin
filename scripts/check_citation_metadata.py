#!/usr/bin/env python3
"""Check local citation metadata exports without network lookup or private text."""
from __future__ import annotations

import argparse
import csv
import json
import re
import string
import sys
import unicodedata
from pathlib import Path
from typing import Any


PRIVATE_FIELDS = {
    "abstract",
    "excerpt",
    "full_text",
    "manuscript_text",
    "notes",
    "private_notes",
    "source_text",
}
DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$", re.IGNORECASE)


def read_json_records(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        records = payload
    elif isinstance(payload, dict) and isinstance(payload.get("records"), list):
        records = payload["records"]
    else:
        raise ValueError("JSON input must be a list or an object with a records list")
    return [record for record in records if isinstance(record, dict)]


def read_csv_records(path: Path) -> list[dict[str, Any]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def read_records(path: Path) -> list[dict[str, Any]]:
    suffix = path.suffix.lower()
    if suffix == ".json":
        return read_json_records(path)
    if suffix == ".csv":
        return read_csv_records(path)
    raise ValueError("input must be .json or .csv")


def record_id(record: dict[str, Any], index: int = 0) -> str:
    value = record.get("reference_id") or record.get("id") or record.get("citation_key")
    return str(value) if value else f"record-{index + 1}"


def private_field_errors(records: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for index, record in enumerate(records):
        identifier = record_id(record, index)
        for field in sorted(PRIVATE_FIELDS & set(record.keys())):
            if str(record.get(field, "")).strip():
                errors.append(f"{identifier}: remove private field {field!r}")
    return errors


def text_value(record: dict[str, Any], key: str) -> str:
    value = record.get(key)
    return value.strip() if isinstance(value, str) else ""


def normalize_identifier(value: str) -> str:
    value = value.strip().lower()
    for prefix in ["https://doi.org/", "http://doi.org/", "doi:"]:
        if value.startswith(prefix):
            return value[len(prefix):]
    return value


def normalize_title(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    without_punctuation = normalized.translate(str.maketrans("", "", string.punctuation))
    return " ".join(without_punctuation.lower().split())


def compare_pair(claimed: str, authoritative: str, *, normalizer) -> str:
    if not claimed and not authoritative:
        return "not_provided"
    if not claimed or not authoritative:
        return "unchecked"
    return "match" if normalizer(claimed) == normalizer(authoritative) else "mismatch"


def doi_status(claimed_doi: str, authoritative_doi: str) -> str:
    claimed = normalize_identifier(claimed_doi)
    authoritative = normalize_identifier(authoritative_doi)
    if claimed and not DOI_RE.match(claimed):
        return "format_warning"
    if authoritative and not DOI_RE.match(authoritative):
        return "format_warning"
    return compare_pair(claimed, authoritative, normalizer=lambda value: value)


def mismatch_notes(statuses: dict[str, str]) -> list[str]:
    labels = {
        "doi_status": "DOI mismatch",
        "title_status": "title mismatch",
        "author_year_status": "author-year mismatch",
        "venue_status": "venue mismatch",
    }
    return [label for key, label in labels.items() if statuses[key] == "mismatch"]


def status_and_risk(statuses: dict[str, str]) -> tuple[str, str]:
    notes = mismatch_notes(statuses)
    if {"DOI mismatch", "title mismatch"}.issubset(set(notes)):
        return "identifier_hijack_risk", "high"
    if notes:
        return "metadata_mismatch", "medium"
    if "format_warning" in statuses.values():
        return "metadata_format_warning", "medium"
    if any(status in {"not_provided", "unchecked"} for status in statuses.values()):
        return "metadata_partly_unchecked", "medium"
    return "metadata_match", "low"


def evaluate_record(record: dict[str, Any], index: int) -> dict[str, Any]:
    statuses = {
        "doi_status": doi_status(text_value(record, "claimed_doi"), text_value(record, "authoritative_doi")),
        "title_status": compare_pair(
            text_value(record, "claimed_title"),
            text_value(record, "authoritative_title"),
            normalizer=normalize_title,
        ),
        "author_year_status": compare_pair(
            text_value(record, "claimed_author_year"),
            text_value(record, "authoritative_author_year"),
            normalizer=lambda value: " ".join(value.lower().split()),
        ),
        "venue_status": compare_pair(
            text_value(record, "claimed_venue"),
            text_value(record, "authoritative_venue"),
            normalizer=normalize_title,
        ),
    }
    status, risk = status_and_risk(statuses)
    notes = mismatch_notes(statuses)
    if "format_warning" in statuses.values():
        notes.append("DOI format warning")
    if status == "metadata_partly_unchecked":
        notes.append("metadata pair missing or unchecked")
    return {
        "reference_id": record_id(record, index),
        "status": status,
        "risk": risk,
        **statuses,
        "notes": notes,
    }


def evaluate_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [evaluate_record(record, index) for index, record in enumerate(records)]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Local JSON or CSV metadata export.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        records = read_records(args.input)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"errors": [str(error)]}, indent=2))
        return 1

    errors = private_field_errors(records)
    if errors:
        print(json.dumps({"errors": errors}, indent=2))
        return 1

    results = evaluate_records(records)
    print(json.dumps({"records": results}, indent=2))
    return 1 if any(result["risk"] in {"medium", "high"} for result in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
