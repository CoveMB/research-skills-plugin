#!/usr/bin/env python3
"""Check local source candidate exports and duplicate clusters without network access."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

from check_citation_metadata import normalize_identifier, normalize_title
from plugin_utils import (
    PRIVATE_SOURCE_TEXT_FIELDS,
    normalized_field_name,
    normalized_private_fields,
    private_payload_field_errors,
    read_csv_records as read_csv_record_objects,
    read_json_or_csv_records,
    read_json_records as read_json_record_objects,
    validate_record_objects,
)


PRIVATE_FIELDS = set(PRIVATE_SOURCE_TEXT_FIELDS)
JSON_RECORD_ERROR = "JSON input must be a list or an object with a records or candidates list"
EMPTY_RECORD_ERROR = "input must contain at least one source candidate record"
COMPLETED_SEARCH_STATUSES = {"complete", "completed", "completed_search", "executed", "searched"}
STABLE_IDENTIFIER_FIELDS = {
    "arxiv_id": "arxiv",
    "corpus_id": "semantic_scholar",
    "isbn": "isbn",
    "oclc": "oclc",
    "openalex_id": "openalex",
    "pmid": "pmid",
    "semantic_scholar_id": "semantic_scholar",
    "stable_id": "stable",
}
LIMITS = [
    "This checker parses local JSON or CSV candidate exports only.",
    "It does not run searches, call APIs, verify source truth, or add records to a bibliography.",
    "Duplicate clusters are screening aids, not verified citation records.",
]


def read_json_records(path: Path) -> list[dict[str, Any]]:
    return read_json_record_objects(
        path,
        container_keys=("records", "candidates"),
        json_error_message=JSON_RECORD_ERROR,
        empty_error_message=EMPTY_RECORD_ERROR,
    )


def read_csv_records(path: Path) -> list[dict[str, Any]]:
    return read_csv_record_objects(path, empty_error_message=EMPTY_RECORD_ERROR)


def validate_candidate_records(records: list[Any]) -> list[dict[str, Any]]:
    return validate_record_objects(records, empty_error_message=EMPTY_RECORD_ERROR)


def read_records(path: Path) -> list[dict[str, Any]]:
    return read_json_or_csv_records(
        path,
        json_container_keys=("records", "candidates"),
        json_error_message=JSON_RECORD_ERROR,
        empty_error_message=EMPTY_RECORD_ERROR,
    )


NORMALIZED_PRIVATE_FIELDS = normalized_private_fields(PRIVATE_FIELDS)


def is_private_field(field: str) -> bool:
    return normalized_field_name(field) in NORMALIZED_PRIVATE_FIELDS


def candidate_identifier(record: dict[str, Any], index: int = 0) -> str:
    for key in ["candidate_id", "id", "source_id", "record_id", "reference_id"]:
        value = record.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
        if isinstance(value, int):
            return str(value)
    return f"candidate-{index + 1}"


def private_field_errors(records: list[dict[str, Any]]) -> list[str]:
    return private_payload_field_errors(
        records,
        private_fields=PRIVATE_FIELDS,
        record_identifier=candidate_identifier,
    )


def text_value(record: dict[str, Any], keys: Iterable[str]) -> str:
    for key in keys:
        value = record.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
        if isinstance(value, int):
            return str(value)
        if isinstance(value, list):
            strings = [item.strip() for item in value if isinstance(item, str) and item.strip()]
            if strings:
                return "; ".join(strings)
    return ""


def year_value(record: dict[str, Any]) -> str:
    value = text_value(record, ["year", "publication_year", "date", "published"])
    return value[:4] if len(value) >= 4 and value[:4].isdigit() else value


def normalized_search_status(record: dict[str, Any]) -> str:
    return text_value(record, ["search_status", "status"]).casefold().replace("-", " ").strip()


def has_completed_search_status(record: dict[str, Any]) -> bool:
    return normalized_search_status(record).replace(" ", "_") in COMPLETED_SEARCH_STATUSES


def completed_search_has_evidence(record: dict[str, Any]) -> bool:
    return all(
        text_value(record, [key])
        for key in ["search_venue", "query", "date_searched"]
    )


def search_status_errors(records: list[dict[str, Any]]) -> list[str]:
    return [
        f"{candidate_identifier(record, index)}: completed search records require search_venue, query, and date_searched"
        for index, record in enumerate(records)
        if has_completed_search_status(record) and not completed_search_has_evidence(record)
    ]


def normalized_doi(record: dict[str, Any]) -> str:
    return normalize_identifier(text_value(record, ["doi", "DOI", "claimed_doi"]))


def stable_identifiers(record: dict[str, Any]) -> list[str]:
    identifiers: list[str] = []
    for field, prefix in sorted(STABLE_IDENTIFIER_FIELDS.items()):
        value = text_value(record, [field])
        if value:
            identifiers.append(f"{prefix}:{value}")
    return identifiers


def metadata_confidence(candidate: dict[str, Any]) -> str:
    if candidate["doi"] or candidate["stable_identifiers"]:
        return "high"
    if candidate["title"] and (candidate["authors"] or candidate["year"]):
        return "medium"
    return "low"


def normalized_candidate(record: dict[str, Any], index: int) -> dict[str, Any]:
    candidate = {
        "candidate_id": candidate_identifier(record, index),
        "title": text_value(record, ["title", "name", "work_title"]),
        "authors": text_value(record, ["authors", "author", "creators"]),
        "year": year_value(record),
        "venue": text_value(record, ["venue", "journal", "publisher", "source"]),
        "doi": normalized_doi(record),
        "url": text_value(record, ["url", "link"]),
        "stable_identifiers": stable_identifiers(record),
        "source_export": text_value(record, ["source_export", "export_source", "search_export"]),
        "search_status": normalized_search_status(record) or "unknown",
    }
    return {**candidate, "metadata_confidence": metadata_confidence(candidate)}


def duplicate_keys(candidate: dict[str, Any]) -> list[tuple[str, str]]:
    keys: list[tuple[str, str]] = []
    if candidate["doi"]:
        keys.append(("doi", candidate["doi"]))
    for identifier in candidate["stable_identifiers"]:
        keys.append(("stable_identifier", identifier.casefold()))
    title_key = normalize_title(candidate["title"])
    if title_key:
        keys.append(("normalized_title", title_key))
    return keys


def grouped_duplicate_candidates(candidates: list[dict[str, Any]]) -> dict[tuple[str, str], list[dict[str, Any]]]:
    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for candidate in candidates:
        for basis, key in duplicate_keys(candidate):
            groups[(basis, key)].append(candidate)
    return {key: value for key, value in groups.items() if len(value) > 1}


def cluster_priority(match_basis: str) -> int:
    priorities = {"doi": 0, "stable_identifier": 1, "normalized_title": 2}
    return priorities.get(match_basis, 99)


def candidate_completeness(candidate: dict[str, Any]) -> int:
    scored_fields = ["title", "authors", "year", "venue", "doi", "url", "source_export"]
    return sum(1 for field in scored_fields if candidate.get(field)) + len(candidate["stable_identifiers"])


def preferred_candidate_id(candidates: list[dict[str, Any]]) -> str:
    preferred = max(candidates, key=candidate_completeness)
    return str(preferred["candidate_id"])


def duplicate_clusters(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups = grouped_duplicate_candidates(candidates)
    clusters: list[dict[str, Any]] = []
    assigned: set[str] = set()
    for (match_basis, _), duplicate_candidates in sorted(groups.items(), key=lambda item: cluster_priority(item[0][0])):
        unassigned_candidates = [
            candidate for candidate in duplicate_candidates if candidate["candidate_id"] not in assigned
        ]
        if len(unassigned_candidates) < 2:
            continue
        candidate_ids = [candidate["candidate_id"] for candidate in unassigned_candidates]
        assigned.update(candidate_ids)
        clusters.append(
            {
                "cluster_id": f"cluster-{len(clusters) + 1}",
                "candidate_ids": candidate_ids,
                "match_basis": match_basis,
                "confidence": "high" if match_basis in {"doi", "stable_identifier"} else "medium",
                "preferred_record": preferred_candidate_id(unassigned_candidates),
                "review_needed": match_basis == "normalized_title",
            }
        )
    return clusters


def search_status_summary(candidates: list[dict[str, Any]], validation_errors: list[str]) -> dict[str, Any]:
    counts = dict(sorted(Counter(candidate["search_status"] for candidate in candidates).items()))
    return {
        "status_counts": counts,
        "validation_errors": validation_errors,
    }


def build_candidate_report(path: Path) -> dict[str, Any]:
    records = read_records(path)
    candidates = [normalized_candidate(record, index) for index, record in enumerate(records)]
    search_errors = search_status_errors(records)
    errors = [*private_field_errors(records), *search_errors]
    return {
        "schema_version": "source-candidate-check-v1",
        "execution_mode": "deterministic-local",
        "source": {"input": str(path)},
        "limits": LIMITS,
        "records": candidates,
        "duplicate_clusters": duplicate_clusters(candidates),
        "search_status": search_status_summary(candidates, search_errors),
        "errors": errors,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Local JSON or CSV source candidate export.")
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress the report and return only the validation exit code.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        report = build_candidate_report(args.input)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"errors": [str(error)]}, indent=2))
        return 1

    if not args.quiet:
        print(json.dumps(report, indent=2))
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
