#!/usr/bin/env python3
"""Check local source candidate exports and duplicate clusters without network access."""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

from check_citation_metadata import normalize_identifier, normalize_title


PRIVATE_FIELDS = {
    "excerpt",
    "full text",
    "full_text",
    "manuscript_text",
    "manuscript text",
    "notes",
    "private_notes",
    "private notes",
    "source_text",
    "source text",
}
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
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        records = payload
    elif isinstance(payload, dict) and isinstance(payload.get("records"), list):
        records = payload["records"]
    elif isinstance(payload, dict) and isinstance(payload.get("candidates"), list):
        records = payload["candidates"]
    else:
        raise ValueError("JSON input must be a list or an object with a records or candidates list")
    return validate_candidate_records(records)


def read_csv_records(path: Path) -> list[dict[str, Any]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return validate_candidate_records([dict(row) for row in csv.DictReader(handle)])


def validate_candidate_records(records: list[Any]) -> list[dict[str, Any]]:
    if not records:
        raise ValueError("input must contain at least one source candidate record")

    valid_records: list[dict[str, Any]] = []
    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            raise ValueError(f"record {index} must be an object")
        valid_records.append(record)
    return valid_records


def read_records(path: Path) -> list[dict[str, Any]]:
    suffix = path.suffix.lower()
    if suffix == ".json":
        return read_json_records(path)
    if suffix == ".csv":
        return read_csv_records(path)
    raise ValueError("input must be .json or .csv")


def normalized_field_name(field: str) -> str:
    return " ".join(field.replace("_", " ").casefold().split())


NORMALIZED_PRIVATE_FIELDS = {normalized_field_name(private_field) for private_field in PRIVATE_FIELDS}


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
    errors: list[str] = []
    for index, record in enumerate(records):
        identifier = candidate_identifier(record, index)
        for field in sorted(record.keys()):
            if is_private_field(field) and str(record.get(field, "")).strip():
                errors.append(f"{identifier}: remove private field {field!r}")
    return errors


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


def duplicate_keys(candidate: dict[str, Any]) -> list[tuple[str, str, str, str, bool]]:
    keys: list[tuple[str, str, str, str, bool]] = []
    if candidate["doi"]:
        keys.append(("doi", candidate["doi"], "doi", "high", False))
    for identifier in candidate["stable_identifiers"]:
        keys.append(("stable_identifier", identifier.casefold(), "stable_identifier", "high", False))
    title_key = normalize_title(candidate["title"])
    if title_key:
        keys.append(("normalized_title", title_key, "normalized_title", "medium", True))
    return keys


def grouped_duplicate_candidates(candidates: list[dict[str, Any]]) -> dict[tuple[str, str], list[dict[str, Any]]]:
    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for candidate in candidates:
        for _, key, basis, _, _ in duplicate_keys(candidate):
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


def search_status_summary(candidates: list[dict[str, Any]], records: list[dict[str, Any]]) -> dict[str, Any]:
    counts = dict(sorted(Counter(candidate["search_status"] for candidate in candidates).items()))
    return {
        "status_counts": counts,
        "validation_errors": search_status_errors(records),
    }


def build_candidate_report(path: Path) -> dict[str, Any]:
    records = read_records(path)
    candidates = [normalized_candidate(record, index) for index, record in enumerate(records)]
    errors = [*private_field_errors(records), *search_status_errors(records)]
    return {
        "schema_version": "source-candidate-check-v1",
        "execution_mode": "deterministic-local",
        "source": {"input": str(path)},
        "limits": LIMITS,
        "records": candidates,
        "duplicate_clusters": duplicate_clusters(candidates),
        "search_status": search_status_summary(candidates, records),
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
