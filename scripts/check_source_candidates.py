#!/usr/bin/env python3
"""Check local source candidate exports and duplicate clusters without network access."""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

from check_citation_metadata import DOI_RE, PUBLIC_IDENTIFIER_SPECS, normalize_identifier, normalize_title
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
AUTHOR_YEAR_TITLE_SIMILARITY_THRESHOLD = 0.86
TITLE_ONLY_SIMILARITY_THRESHOLD = 0.82
PREPRINT_MARKERS = {"arxiv", "biorxiv", "medrxiv", "preprint", "ssrn"}
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
STABLE_IDENTIFIER_PLACEHOLDERS = {
    "-",
    "--",
    "?",
    "missing",
    "n/a",
    "na",
    "none",
    "not applicable",
    "not available",
    "not provided",
    "not specified",
    "null",
    "pending",
    "tba",
    "tbd",
    "todo",
    "unclear",
    "unknown",
}
OPENALEX_ID_RE = re.compile(r"^[a-z]\d+$", re.IGNORECASE)
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


def doi_is_valid(value: str) -> bool:
    return bool(DOI_RE.match(normalize_identifier(value)))


def normalized_doi(record: dict[str, Any]) -> str:
    value = text_value(record, ["doi", "DOI", "claimed_doi"])
    return normalize_identifier(value) if doi_is_valid(value) else ""


def raw_doi(record: dict[str, Any]) -> str:
    return text_value(record, ["doi", "DOI", "claimed_doi"]).strip()


def placeholder_identifier(value: str) -> bool:
    normalized = normalize_identifier(value).strip().casefold()
    normalized_words = normalized.replace("_", " ").replace("-", " ")
    normalized_words = " ".join(normalized_words.split())
    return normalized in STABLE_IDENTIFIER_PLACEHOLDERS or normalized_words in STABLE_IDENTIFIER_PLACEHOLDERS


def normalize_openalex_id(value: str) -> str:
    normalized = value.strip()
    folded = normalized.casefold()
    for prefix in ("https://openalex.org/", "http://openalex.org/", "openalex:"):
        if folded.startswith(prefix):
            return normalized[len(prefix):].strip()
    return normalized


def normalize_corpus_id(value: str) -> str:
    return "".join(value.strip().split())


def validated_public_identifier(field: str, value: str) -> str:
    normalizer, validator = PUBLIC_IDENTIFIER_SPECS[field]
    normalized = normalizer(value)
    return normalized if normalized and validator(normalized) else ""


def normalized_stable_identifier_value(field: str, value: str) -> str:
    if not value or placeholder_identifier(value):
        return ""
    if field in PUBLIC_IDENTIFIER_SPECS:
        return validated_public_identifier(field, value)
    if field == "corpus_id":
        normalized = normalize_corpus_id(value)
        return normalized if normalized.isdigit() else ""
    if field == "openalex_id":
        normalized = normalize_openalex_id(value)
        return normalized if OPENALEX_ID_RE.match(normalized) else ""
    return value.strip()


def stable_identifiers(record: dict[str, Any]) -> list[str]:
    identifiers: list[str] = []
    for field, prefix in sorted(STABLE_IDENTIFIER_FIELDS.items()):
        value = normalized_stable_identifier_value(field, text_value(record, [field]))
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
        "raw_doi": raw_doi(record),
        "doi": normalized_doi(record),
        "url": text_value(record, ["url", "link"]),
        "stable_identifiers": stable_identifiers(record),
        "edition": text_value(record, ["edition", "version", "book_edition"]),
        "publication_type": text_value(record, ["publication_type", "record_type", "type", "source_type"]),
        "alternate_title": text_value(record, ["alternate_title", "translated_title", "original_title"]),
        "source_export": text_value(record, ["source_export", "export_source", "search_export"]),
        "search_status": normalized_search_status(record) or "unknown",
    }
    return {**candidate, "metadata_confidence": metadata_confidence(candidate)}


def cluster_priority(match_basis: str) -> int:
    priorities = {
        "exact_doi": 0,
        "doi": 1,
        "stable_identifier": 2,
        "normalized_title": 3,
        "author_year_title_similarity": 4,
        "title_similarity": 5,
    }
    return priorities.get(match_basis, 99)


def candidate_completeness(candidate: dict[str, Any]) -> int:
    scored_fields = ["title", "authors", "year", "venue", "doi", "url", "source_export"]
    return sum(1 for field in scored_fields if candidate.get(field)) + len(candidate["stable_identifiers"])


def preferred_candidate_id(candidates: list[dict[str, Any]]) -> str:
    preferred = max(candidates, key=candidate_completeness)
    return str(preferred["candidate_id"])


def normalized_authors(candidate: dict[str, Any]) -> str:
    return normalize_title(candidate["authors"])


def normalized_candidate_title(candidate: dict[str, Any]) -> str:
    return normalize_title(candidate["title"])


def stable_identifier_overlap(first: dict[str, Any], second: dict[str, Any]) -> list[str]:
    first_identifiers = {identifier.casefold() for identifier in first["stable_identifiers"]}
    second_identifiers = {identifier.casefold() for identifier in second["stable_identifiers"]}
    return sorted(first_identifiers & second_identifiers)


def same_available_authors(first: dict[str, Any], second: dict[str, Any]) -> bool:
    first_authors = normalized_authors(first)
    second_authors = normalized_authors(second)
    return bool(first_authors and second_authors and first_authors == second_authors)


def same_available_year(first: dict[str, Any], second: dict[str, Any]) -> bool:
    return bool(first["year"] and second["year"] and first["year"] == second["year"])


def conflicting_available_titles(first: dict[str, Any], second: dict[str, Any]) -> bool:
    first_title = normalized_candidate_title(first)
    second_title = normalized_candidate_title(second)
    return bool(first_title and second_title and first_title != second_title)


def title_similarity(first: dict[str, Any], second: dict[str, Any]) -> float:
    first_title = normalized_candidate_title(first)
    second_title = normalized_candidate_title(second)
    if not first_title or not second_title:
        return 0.0
    return difflib.SequenceMatcher(None, first_title, second_title).ratio()


def candidate_has_preprint_marker(candidate: dict[str, Any]) -> bool:
    text = " ".join(
        [
            candidate["venue"],
            candidate["publication_type"],
            " ".join(candidate["stable_identifiers"]),
            candidate["source_export"],
        ]
    ).casefold()
    return any(marker in text for marker in PREPRINT_MARKERS)


def preprint_published_distinction(first: dict[str, Any], second: dict[str, Any]) -> bool:
    first_preprint = candidate_has_preprint_marker(first)
    second_preprint = candidate_has_preprint_marker(second)
    if first_preprint == second_preprint:
        return False
    first_published = bool(first["doi"] or first["venue"])
    second_published = bool(second["doi"] or second["venue"])
    return first_published and second_published


def exact_identifier_match(match_basis: str) -> bool:
    return match_basis in {"exact_doi", "doi", "stable_identifier"}


def false_merge_warnings(first: dict[str, Any], second: dict[str, Any], match_basis: str) -> list[str]:
    warnings: list[str] = []
    if exact_identifier_match(match_basis) and conflicting_available_titles(first, second):
        warnings.append("conflicting title metadata")
    if first["authors"] and second["authors"] and not same_available_authors(first, second):
        warnings.append("conflicting author metadata")
    if first["year"] and second["year"] and not same_available_year(first, second):
        warnings.append("conflicting year metadata")
    if first["edition"] and second["edition"] and normalize_title(first["edition"]) != normalize_title(second["edition"]):
        warnings.append("edition or version distinction")
    if preprint_published_distinction(first, second):
        warnings.append("preprint and published version distinction")
    if first["alternate_title"] or second["alternate_title"]:
        warnings.append("translated or alternate title caution")
    return warnings


def relation_status(match_basis: str, warnings: list[str]) -> str:
    if warnings:
        return "related_but_distinct"
    if match_basis in {"exact_doi", "doi", "stable_identifier"}:
        return "exact_duplicate"
    if match_basis in {"normalized_title", "author_year_title_similarity"}:
        return "probable_duplicate"
    return "possible_duplicate"


def relation_confidence(status: str, match_basis: str) -> str:
    if status == "exact_duplicate":
        return "high"
    if status == "probable_duplicate":
        return "medium"
    if match_basis == "title_similarity":
        return "low"
    return "low"


def relation_reason_for_basis(match_basis: str) -> str:
    reasons = {
        "exact_doi": "exact DOI match",
        "doi": "normalized DOI match",
        "stable_identifier": "stable identifier match",
        "normalized_title": "normalized title match",
        "author_year_title_similarity": "author-year-title similarity",
        "title_similarity": "title-only near duplicate",
    }
    return reasons[match_basis]


def match_basis_for_pair(first: dict[str, Any], second: dict[str, Any]) -> str:
    if (
        first["raw_doi"]
        and second["raw_doi"]
        and doi_is_valid(first["raw_doi"])
        and doi_is_valid(second["raw_doi"])
        and first["raw_doi"].casefold() == second["raw_doi"].casefold()
    ):
        return "exact_doi"
    if first["doi"] and second["doi"] and first["doi"] == second["doi"]:
        return "doi"
    if stable_identifier_overlap(first, second):
        return "stable_identifier"

    first_title = normalized_candidate_title(first)
    second_title = normalized_candidate_title(second)
    if first_title and first_title == second_title:
        return "normalized_title"

    similarity = title_similarity(first, second)
    if same_available_authors(first, second) and same_available_year(first, second):
        if similarity >= AUTHOR_YEAR_TITLE_SIMILARITY_THRESHOLD:
            return "author_year_title_similarity"
    if similarity >= TITLE_ONLY_SIMILARITY_THRESHOLD:
        return "title_similarity"
    return ""


def duplicate_relation(first: dict[str, Any], second: dict[str, Any]) -> dict[str, Any] | None:
    match_basis = match_basis_for_pair(first, second)
    if not match_basis:
        return None

    warnings = false_merge_warnings(first, second, match_basis)
    duplicate_status = relation_status(match_basis, warnings)
    review_required = duplicate_status != "exact_duplicate" or bool(warnings)
    candidates = [first, second]
    return {
        "candidate_ids": [candidate["candidate_id"] for candidate in candidates],
        "match_basis": match_basis,
        "duplicate_status": duplicate_status,
        "match_reasons": [relation_reason_for_basis(match_basis)],
        "confidence": relation_confidence(duplicate_status, match_basis),
        "preferred_record": preferred_candidate_id(candidates),
        "review_needed": review_required,
        "human_review_required": review_required,
        "preserve_records": True,
        "false_merge_warnings": warnings,
    }


def duplicate_clusters(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    clusters = [
        relation
        for first_index, first_candidate in enumerate(candidates)
        for second_candidate in candidates[first_index + 1 :]
        for relation in [duplicate_relation(first_candidate, second_candidate)]
        if relation is not None
    ]
    clusters.sort(key=lambda cluster: cluster_priority(cluster["match_basis"]))
    for index, cluster in enumerate(clusters, start=1):
        cluster["cluster_id"] = f"cluster-{index}"
    return clusters


def metadata_warnings(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    warnings: list[dict[str, Any]] = []
    for candidate in candidates:
        candidate_warnings: list[str] = []
        if not candidate["title"]:
            candidate_warnings.append("missing title")
        if candidate["raw_doi"] and not candidate["doi"]:
            candidate_warnings.append("invalid DOI format")
        if not candidate["doi"] and not candidate["stable_identifiers"]:
            candidate_warnings.append("missing DOI or stable identifier")
        if candidate_warnings:
            warnings.append(
                {
                    "candidate_id": candidate["candidate_id"],
                    "duplicate_status": "insufficient_metadata",
                    "human_review_required": True,
                    "warnings": candidate_warnings,
                }
            )
    return warnings


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
        "metadata_warnings": metadata_warnings(candidates),
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
