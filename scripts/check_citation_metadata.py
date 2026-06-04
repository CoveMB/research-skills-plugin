#!/usr/bin/env python3
"""Check local citation metadata exports without private text."""
from __future__ import annotations

import argparse
import json
import re
import string
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path
from typing import Any, Callable, NamedTuple

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

PRIVATE_FIELDS = {
    "abstract",
    *PRIVATE_SOURCE_TEXT_FIELDS,
}
JSON_RECORD_ERROR = "JSON input must be a list or an object with a records list"
EMPTY_RECORD_ERROR = "input must contain at least one metadata record"
DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$", re.IGNORECASE)
ARXIV_NEW_RE = re.compile(r"^\d{4}\.\d{4,5}$")
ARXIV_OLD_RE = re.compile(r"^[a-z-]+(?:\.[a-z]{2})?/\d{7}$")
PMID_RE = re.compile(r"^\d{1,9}$")
OCLC_RE = re.compile(r"^\d+$")
LCCN_RE = re.compile(r"^[a-z]{0,3}\d{6,10}$")
LOOKUP_PROVIDERS = {"none", "crossref"}
CROSSREF_WORKS_ENDPOINT = "https://api.crossref.org/v1/works/"
CROSSREF_USER_AGENT = "research-skills-plugin/1.0 (public metadata lookup)"
MAX_CROSSREF_RESPONSE_BYTES = 1_000_000
MAX_LOOKUP_TIMEOUT_SECONDS = 60.0
MIN_PLAUSIBLE_PUBLICATION_YEAR = 1450
FUTURE_PUBLICATION_YEAR_GRACE = 1
SUSPICIOUS_PAGE_RANGE_LENGTH = 1000
NO_EXTERNAL_VERIFICATION_NOTE = "DOI format is syntactically valid only; source existence is not verified"
CLAIM_SUPPORT_NOT_CHECKED = "not_checked"
CITATION_ONLY_NOTE = "citation-only access does not verify source-claim support"
ABSTRACT_ONLY_NOTE = "abstract-only access cannot verify full-text source-claim support"


SOURCE_ACCESS_ALIASES = (
    "source_access_level",
    "source_access",
    "access_level",
    "annotation_basis",
)
CITATION_ONLY_ACCESS_VALUES = {
    "citation only",
    "citation_only",
    "bibliography only",
    "bibliography_only",
    "reference only",
    "reference_only",
}
ABSTRACT_ONLY_ACCESS_VALUES = {
    "abstract only",
    "abstract_only",
}
PUBLIC_METADATA_ACCESS_VALUES = {
    "public metadata only",
    "public_metadata_only",
    "metadata only",
    "metadata_only",
    "citation metadata only",
    "citation_metadata_only",
}
FULL_TEXT_ACCESS_VALUES = {
    "full text",
    "full_text",
    "user provided full text",
    "user_provided_full_text",
}
KNOWN_SOURCE_ACCESS_STATUSES = {
    "abstract_only",
    "citation_only",
    "full_text_label",
    "not_specified",
    "public_metadata_only",
}

TITLE_ALIASES = ("claimed_title", "title", "authoritative_title")
AUTHOR_EDITOR_ALIASES = (
    "author",
    "authors",
    "editor",
    "editors",
    "claimed_author_year",
    "authoritative_author_year",
)
YEAR_ALIASES = ("publication_year", "year", "issued_year", "date", "claimed_author_year", "authoritative_author_year")
DOI_ALIASES = ("doi", "DOI", "claimed_doi", "authoritative_doi")
VENUE_ALIASES = ("venue", "journal", "container_title", "container-title", "claimed_venue", "authoritative_venue")
PUBLISHER_ALIASES = ("publisher", "claimed_publisher", "authoritative_publisher")
PAGE_RANGE_ALIASES = ("pages", "page_range", "page-range")
LOCATOR_CLAIM_ALIASES = ("locator_claim", "quote_locator_claim", "page_claim")
LOCATOR_SUPPORT_ALIASES = (
    "page",
    "pages",
    "page_range",
    "section",
    "paragraph",
    "locator",
    "stable_locator",
)
SOURCE_TYPES_REQUIRING_AUTHOR_OR_EDITOR = {
    "",
    "article",
    "journal_article",
    "book",
    "book_chapter",
    "chapter",
    "conference_paper",
    "report",
    "thesis",
}


class ValidationIssue(NamedTuple):
    code: str
    severity: str
    note: str


class PublicLookupState(NamedTuple):
    attempted: bool
    metadata_returned: bool


class MetadataPairSpec(NamedTuple):
    claimed_key: str
    authoritative_key: str
    status_key: str
    mismatch_note: str
    comparator: Callable[[str, str], str]


NO_PUBLIC_LOOKUP = PublicLookupState(attempted=False, metadata_returned=False)


def read_json_records(path: Path) -> list[dict[str, Any]]:
    return read_json_record_objects(
        path,
        container_keys=("records",),
        json_error_message=JSON_RECORD_ERROR,
        empty_error_message=EMPTY_RECORD_ERROR,
    )


def read_csv_records(path: Path) -> list[dict[str, Any]]:
    return read_csv_record_objects(path, empty_error_message=EMPTY_RECORD_ERROR)


def validate_metadata_records(records: list[Any]) -> list[dict[str, Any]]:
    return validate_record_objects(records, empty_error_message=EMPTY_RECORD_ERROR)


def read_records(path: Path) -> list[dict[str, Any]]:
    return read_json_or_csv_records(
        path,
        json_container_keys=("records",),
        json_error_message=JSON_RECORD_ERROR,
        empty_error_message=EMPTY_RECORD_ERROR,
    )


def record_id(record: dict[str, Any], index: int = 0) -> str:
    value = record.get("reference_id") or record.get("id") or record.get("citation_key")
    return str(value) if value else f"record-{index + 1}"


NORMALIZED_PRIVATE_FIELDS = normalized_private_fields(PRIVATE_FIELDS)


def is_private_field(field: str) -> bool:
    return normalized_field_name(field) in NORMALIZED_PRIVATE_FIELDS


def private_field_errors(records: list[dict[str, Any]]) -> list[str]:
    return private_payload_field_errors(
        records,
        private_fields=PRIVATE_FIELDS,
        record_identifier=record_id,
    )


def text_value(record: dict[str, Any], key: str) -> str:
    value = record.get(key)
    return value.strip() if isinstance(value, str) else ""


def public_text_value(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, int):
        return str(value)
    if isinstance(value, list):
        parts = [public_text_value(item) for item in value]
        return " ".join(part for part in parts if part).strip()
    if isinstance(value, dict):
        parts = [public_text_value(value.get(key)) for key in ("family", "given", "name", "literal")]
        return " ".join(part for part in parts if part).strip()
    return ""


def first_public_text(record: dict[str, Any], keys: tuple[str, ...]) -> str:
    for key in keys:
        value = public_text_value(record.get(key))
        if value:
            return value
    return ""


def public_text_values(record: dict[str, Any], keys: tuple[str, ...]) -> list[str]:
    values = [public_text_value(record.get(key)) for key in keys]
    return [value for value in values if value]


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


def normalize_lower_words(value: str) -> str:
    return " ".join(value.lower().split())


def normalize_access_level(value: str) -> str:
    return normalize_lower_words(value).replace("-", "_")


def access_value_matches(normalized: str, values: set[str]) -> bool:
    return normalized in {normalize_access_level(value) for value in values}


def citation_key(record: dict[str, Any]) -> str:
    return first_public_text(record, ("citation_key", "citekey"))


def visible_title(record: dict[str, Any]) -> str:
    return first_public_text(record, TITLE_ALIASES)


def visible_doi(record: dict[str, Any]) -> str:
    for value in public_text_values(record, DOI_ALIASES):
        normalized = normalize_identifier(value)
        if DOI_RE.match(normalized):
            return normalized
    return ""


def publication_type(record: dict[str, Any]) -> str:
    return normalize_access_level(first_public_text(record, ("publication_type", "source_type", "type")))


def source_access_status(record: dict[str, Any]) -> str:
    source_access = first_public_text(record, SOURCE_ACCESS_ALIASES)
    if not source_access:
        return "not_specified"
    normalized = normalize_access_level(source_access)
    if access_value_matches(normalized, CITATION_ONLY_ACCESS_VALUES):
        return "citation_only"
    if access_value_matches(normalized, ABSTRACT_ONLY_ACCESS_VALUES):
        return "abstract_only"
    if access_value_matches(normalized, PUBLIC_METADATA_ACCESS_VALUES):
        return "public_metadata_only"
    if access_value_matches(normalized, FULL_TEXT_ACCESS_VALUES):
        return "full_text_label"
    return normalized.replace(" ", "_")


def current_publication_year_limit() -> int:
    return date.today().year + FUTURE_PUBLICATION_YEAR_GRACE


def publication_year(record: dict[str, Any]) -> int | None:
    for value in public_text_values(record, YEAR_ALIASES):
        match = re.search(r"\b(1[4-9]\d{2}|20\d{2}|21\d{2}|22\d{2}|23\d{2}|24\d{2}|25\d{2})\b", value)
        if match:
            return int(match.group(1))
    return None


def has_author_or_editor(record: dict[str, Any]) -> bool:
    return bool(first_public_text(record, AUTHOR_EDITOR_ALIASES))


def normalized_non_empty_values(values: list[str], *, normalizer: Callable[[str], str]) -> set[str]:
    return {normalizer(value) for value in values if normalizer(value)}


def doi_field_variants_disagree(record: dict[str, Any]) -> bool:
    normalized_values = normalized_non_empty_values(
        public_text_values(record, DOI_ALIASES),
        normalizer=normalize_identifier,
    )
    return len(normalized_values) > 1


def venue_or_publisher_fields_disagree(record: dict[str, Any]) -> bool:
    venue_values = normalized_non_empty_values(public_text_values(record, VENUE_ALIASES), normalizer=normalize_title)
    publisher_values = normalized_non_empty_values(
        public_text_values(record, PUBLISHER_ALIASES),
        normalizer=normalize_title,
    )
    return len(venue_values) > 1 or len(publisher_values) > 1


def page_range_warnings(record: dict[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for value in public_text_values(record, PAGE_RANGE_ALIASES):
        match = re.search(r"\b(\d{1,6})\s*[-–—]\s*(\d{1,6})\b", value)
        if not match:
            continue
        start_page = int(match.group(1))
        end_page = int(match.group(2))
        if start_page > end_page:
            issues.append(ValidationIssue("suspicious_page_range", "medium", "page range start exceeds end"))
        elif end_page - start_page > SUSPICIOUS_PAGE_RANGE_LENGTH:
            issues.append(ValidationIssue("suspicious_page_range", "medium", "page range is unusually long"))
    return issues


def locator_claim_without_support(record: dict[str, Any]) -> bool:
    has_locator_claim = any(public_text_value(record.get(key)) for key in LOCATOR_CLAIM_ALIASES)
    has_locator_support = any(public_text_value(record.get(key)) for key in LOCATOR_SUPPORT_ALIASES)
    return has_locator_claim and not has_locator_support


def source_access_notes(record: dict[str, Any]) -> list[ValidationIssue]:
    status = source_access_status(record)
    if status == "not_specified":
        return [ValidationIssue("missing_source_access_level", "medium", "source access level missing")]
    if status == "citation_only":
        return [ValidationIssue("citation_only_source", "low", CITATION_ONLY_NOTE)]
    if status == "abstract_only":
        return [ValidationIssue("abstract_only_source", "low", ABSTRACT_ONLY_NOTE)]
    if status not in KNOWN_SOURCE_ACCESS_STATUSES:
        return [
            ValidationIssue(
                "unknown_source_access_level",
                "medium",
                f"unknown source access level {status!r}",
            )
        ]
    return []


def structural_metadata_issues(record: dict[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if not first_public_text(record, ("reference_id", "id", "citation_key")):
        issues.append(ValidationIssue("missing_record_identifier", "medium", "stable record identifier missing"))
    if not visible_title(record):
        issues.append(ValidationIssue("missing_title", "medium", "title missing"))
    if publication_type(record) in SOURCE_TYPES_REQUIRING_AUTHOR_OR_EDITOR and not has_author_or_editor(record):
        issues.append(ValidationIssue("missing_author_or_editor", "medium", "author/editor missing for source type"))
    year = publication_year(record)
    if year is None:
        issues.append(ValidationIssue("missing_publication_year", "medium", "publication year missing"))
    elif year < MIN_PLAUSIBLE_PUBLICATION_YEAR:
        issues.append(ValidationIssue("suspicious_publication_year", "medium", "publication year is suspiciously early"))
    elif year > current_publication_year_limit():
        issues.append(ValidationIssue("impossible_publication_year", "medium", "publication year is in the future"))
    if doi_field_variants_disagree(record):
        issues.append(ValidationIssue("inconsistent_doi_strings", "medium", "DOI field variants disagree"))
    if venue_or_publisher_fields_disagree(record):
        issues.append(ValidationIssue("inconsistent_venue_or_publisher", "medium", "venue or publisher field variants disagree"))
    issues.extend(page_range_warnings(record))
    if locator_claim_without_support(record):
        issues.append(
            ValidationIssue(
                "locator_claim_without_support",
                "medium",
                "locator claim lacks page, section, paragraph, or locator support",
            )
        )
    issues.extend(source_access_notes(record))
    return issues


def has_medium_or_high_issue(issues: list[ValidationIssue]) -> bool:
    return any(issue.severity in {"medium", "high"} for issue in issues)


def merged_status_and_risk(status: str, risk: str, issues: list[ValidationIssue]) -> tuple[str, str]:
    if risk == "high" or any(issue.severity == "high" for issue in issues):
        return status, "high"
    if has_medium_or_high_issue(issues):
        if status == "metadata_match":
            return "metadata_validation_warning", "medium"
        return status, "medium"
    return status, risk


def metadata_consistency_status(status: str) -> str:
    if status == "metadata_match":
        return "internally_consistent"
    if status in {"metadata_partly_unchecked", "metadata_format_warning"}:
        return "partly_unchecked"
    return "issues_found"


def external_verification_status(public_lookup_state: PublicLookupState = NO_PUBLIC_LOOKUP) -> str:
    if public_lookup_state.metadata_returned:
        return "metadata_lookup_performed"
    if public_lookup_state.attempted:
        return "metadata_lookup_no_record_returned"
    return "not_verified"


def source_existence_status(public_lookup_state: PublicLookupState = NO_PUBLIC_LOOKUP) -> str:
    if public_lookup_state.metadata_returned:
        return "public_metadata_record_returned"
    return "not_verified"


def verification_limit_notes(
    record: dict[str, Any],
    statuses: dict[str, str],
    public_lookup_state: PublicLookupState = NO_PUBLIC_LOOKUP,
) -> list[str]:
    notes: list[str] = []
    if (
        statuses["doi_status"] == "unchecked"
        and normalize_identifier(text_value(record, "claimed_doi"))
        and not public_lookup_state.metadata_returned
    ):
        notes.append(NO_EXTERNAL_VERIFICATION_NOTE)
    return notes


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


def normalize_isbn(value: str) -> str:
    normalized = value.strip().lower()
    normalized = re.sub(r"^isbn(?:-1[03])?:?", "", normalized).strip()
    return "".join(character for character in normalized if character.isdigit() or character == "x").upper()


def isbn10_is_valid(value: str) -> bool:
    if len(value) != 10 or not value[:9].isdigit() or not (value[9].isdigit() or value[9] == "X"):
        return False
    digits = [10 if character == "X" else int(character) for character in value]
    return sum((10 - index) * digit for index, digit in enumerate(digits)) % 11 == 0


def isbn13_is_valid(value: str) -> bool:
    if len(value) != 13 or not value.isdigit():
        return False
    total = sum((1 if index % 2 == 0 else 3) * int(digit) for index, digit in enumerate(value))
    return total % 10 == 0


def isbn_is_valid(value: str) -> bool:
    return isbn10_is_valid(value) or isbn13_is_valid(value)


def normalize_arxiv_id(value: str) -> str:
    normalized = value.strip().lower()
    for prefix in ["https://arxiv.org/abs/", "http://arxiv.org/abs/", "arxiv:"]:
        if normalized.startswith(prefix):
            normalized = normalized[len(prefix):]
            break
    return re.sub(r"v\d+$", "", normalized)


def arxiv_id_is_valid(value: str) -> bool:
    return bool(ARXIV_NEW_RE.match(value) or ARXIV_OLD_RE.match(value))


def normalize_pmid(value: str) -> str:
    normalized = value.strip().lower()
    if normalized.startswith("pmid:"):
        normalized = normalized[len("pmid:"):]
    return normalized.strip().replace(" ", "")


def normalize_oclc(value: str) -> str:
    normalized = value.strip().lower()
    for prefix in ["oclc:", "oclc", "ocm", "ocn", "on"]:
        if normalized.startswith(prefix):
            normalized = normalized[len(prefix):]
            break
    return normalized.strip().replace(" ", "")


def normalize_lccn(value: str) -> str:
    normalized = value.strip().lower()
    if normalized.startswith("lccn:"):
        normalized = normalized[len("lccn:"):]
    return "".join(character for character in normalized if character.isalnum())


PUBLIC_IDENTIFIER_SPECS = {
    "isbn": (normalize_isbn, isbn_is_valid),
    "arxiv_id": (normalize_arxiv_id, arxiv_id_is_valid),
    "pmid": (normalize_pmid, lambda value: bool(PMID_RE.match(value))),
    "oclc": (normalize_oclc, lambda value: bool(OCLC_RE.match(value))),
    "lccn": (normalize_lccn, lambda value: bool(LCCN_RE.match(value))),
}


def public_identifier_status(identifier_name: str, claimed: str, authoritative: str) -> str:
    normalizer, validator = PUBLIC_IDENTIFIER_SPECS[identifier_name]
    normalized_claimed = normalizer(claimed)
    normalized_authoritative = normalizer(authoritative)
    if claimed.strip() and not normalized_claimed:
        return "format_warning"
    if authoritative.strip() and not normalized_authoritative:
        return "format_warning"
    if normalized_claimed and not validator(normalized_claimed):
        return "format_warning"
    if normalized_authoritative and not validator(normalized_authoritative):
        return "format_warning"
    return compare_pair(normalized_claimed, normalized_authoritative, normalizer=lambda value: value)


METADATA_PAIR_SPECS = (
    MetadataPairSpec("claimed_doi", "authoritative_doi", "doi_status", "DOI mismatch", doi_status),
    MetadataPairSpec(
        "claimed_isbn",
        "authoritative_isbn",
        "isbn_status",
        "ISBN mismatch",
        lambda claimed, authoritative: public_identifier_status("isbn", claimed, authoritative),
    ),
    MetadataPairSpec(
        "claimed_arxiv_id",
        "authoritative_arxiv_id",
        "arxiv_id_status",
        "arXiv ID mismatch",
        lambda claimed, authoritative: public_identifier_status("arxiv_id", claimed, authoritative),
    ),
    MetadataPairSpec(
        "claimed_pmid",
        "authoritative_pmid",
        "pmid_status",
        "PMID mismatch",
        lambda claimed, authoritative: public_identifier_status("pmid", claimed, authoritative),
    ),
    MetadataPairSpec(
        "claimed_oclc",
        "authoritative_oclc",
        "oclc_status",
        "OCLC mismatch",
        lambda claimed, authoritative: public_identifier_status("oclc", claimed, authoritative),
    ),
    MetadataPairSpec(
        "claimed_lccn",
        "authoritative_lccn",
        "lccn_status",
        "LCCN mismatch",
        lambda claimed, authoritative: public_identifier_status("lccn", claimed, authoritative),
    ),
    MetadataPairSpec(
        "claimed_title",
        "authoritative_title",
        "title_status",
        "title mismatch",
        lambda claimed, authoritative: compare_pair(claimed, authoritative, normalizer=normalize_title),
    ),
    MetadataPairSpec(
        "claimed_author_year",
        "authoritative_author_year",
        "author_year_status",
        "author-year mismatch",
        lambda claimed, authoritative: compare_pair(claimed, authoritative, normalizer=normalize_lower_words),
    ),
    MetadataPairSpec(
        "claimed_venue",
        "authoritative_venue",
        "venue_status",
        "venue mismatch",
        lambda claimed, authoritative: compare_pair(claimed, authoritative, normalizer=normalize_title),
    ),
)
FORMAT_WARNING_NOTES = {
    "doi_status": "DOI format warning",
    "isbn_status": "ISBN format warning",
    "arxiv_id_status": "arXiv ID format warning",
    "pmid_status": "PMID format warning",
    "oclc_status": "OCLC format warning",
    "lccn_status": "LCCN format warning",
}
OPTIONAL_IDENTIFIER_STATUS_KEYS = {
    "isbn_status",
    "arxiv_id_status",
    "pmid_status",
    "oclc_status",
    "lccn_status",
}


def mismatch_notes(statuses: dict[str, str]) -> list[str]:
    return [
        spec.mismatch_note
        for spec in METADATA_PAIR_SPECS
        if statuses[spec.status_key] == "mismatch"
    ]


def status_and_risk(statuses: dict[str, str]) -> tuple[str, str]:
    notes = mismatch_notes(statuses)
    if {"DOI mismatch", "title mismatch"}.issubset(set(notes)):
        return "identifier_hijack_risk", "high"
    if notes:
        return "metadata_mismatch", "medium"
    if "format_warning" in statuses.values():
        return "metadata_format_warning", "medium"
    required_statuses = [
        status
        for status_key, status in statuses.items()
        if status_key not in OPTIONAL_IDENTIFIER_STATUS_KEYS
    ]
    optional_statuses = [
        status
        for status_key, status in statuses.items()
        if status_key in OPTIONAL_IDENTIFIER_STATUS_KEYS
    ]
    if any(status in {"not_provided", "unchecked"} for status in required_statuses):
        return "metadata_partly_unchecked", "medium"
    if any(status == "unchecked" for status in optional_statuses):
        return "metadata_partly_unchecked", "medium"
    return "metadata_match", "low"


def trusted_lookup_states(
    records: list[dict[str, Any]],
    lookup_states: list[PublicLookupState] | None,
) -> list[PublicLookupState]:
    if lookup_states is None:
        return [NO_PUBLIC_LOOKUP for _record in records]
    if len(lookup_states) != len(records):
        raise ValueError("lookup state count must match record count")
    return lookup_states


def evaluate_record(
    record: dict[str, Any],
    index: int,
    public_lookup_state: PublicLookupState = NO_PUBLIC_LOOKUP,
) -> dict[str, Any]:
    statuses = {
        spec.status_key: spec.comparator(
            text_value(record, spec.claimed_key),
            text_value(record, spec.authoritative_key),
        )
        for spec in METADATA_PAIR_SPECS
    }
    status, risk = status_and_risk(statuses)
    issues = structural_metadata_issues(record)
    status, risk = merged_status_and_risk(status, risk, issues)
    notes = mismatch_notes(statuses)
    notes.extend(
        note
        for status_key, note in FORMAT_WARNING_NOTES.items()
        if statuses.get(status_key) == "format_warning"
    )
    if status == "metadata_partly_unchecked":
        notes.append("metadata pair missing or unchecked")
    notes.extend(issue.note for issue in issues)
    notes.extend(note for note in verification_limit_notes(record, statuses, public_lookup_state) if note not in notes)
    return {
        "reference_id": record_id(record, index),
        "status": status,
        "risk": risk,
        "metadata_consistency_status": metadata_consistency_status(status),
        "external_verification_status": external_verification_status(public_lookup_state),
        "source_existence_status": source_existence_status(public_lookup_state),
        "source_claim_support_status": CLAIM_SUPPORT_NOT_CHECKED,
        "source_access_status": source_access_status(record),
        **statuses,
        "notes": notes,
    }


def evaluate_records(
    records: list[dict[str, Any]],
    lookup_states: list[PublicLookupState] | None = None,
) -> list[dict[str, Any]]:
    states = trusted_lookup_states(records, lookup_states)
    return [
        evaluate_record(record, index, public_lookup_state)
        for index, (record, public_lookup_state) in enumerate(zip(records, states))
    ]


def work_identity(record: dict[str, Any]) -> tuple[str, str, str, str]:
    return (
        visible_doi(record),
        normalize_title(visible_title(record)),
        normalize_lower_words(first_public_text(record, AUTHOR_EDITOR_ALIASES)),
        str(publication_year(record) or ""),
    )


def record_ids(records: list[tuple[int, dict[str, Any]]]) -> list[str]:
    return [record_id(record, index) for index, record in records]


def records_point_to_different_works(records: list[dict[str, Any]]) -> bool:
    identities = {work_identity(record) for record in records}
    return len(identities) > 1


def group_records_by_value(
    records: list[dict[str, Any]],
    value_for_record: Callable[[dict[str, Any]], str],
) -> dict[str, list[tuple[int, dict[str, Any]]]]:
    grouped_records: dict[str, list[tuple[int, dict[str, Any]]]] = {}
    for index, record in enumerate(records):
        value = value_for_record(record)
        if not value:
            continue
        grouped_records.setdefault(value, []).append((index, record))
    return grouped_records


def citation_key_conflict_warnings(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    warnings: list[dict[str, Any]] = []
    for key, grouped_records in group_records_by_value(records, citation_key).items():
        if len(grouped_records) < 2:
            continue
        records_for_key = [record for _index, record in grouped_records]
        if not records_point_to_different_works(records_for_key):
            continue
        warnings.append(
            {
                "code": "citation_key_conflicting_works",
                "severity": "high",
                "citation_key": key,
                "record_ids": record_ids(grouped_records),
                "message": "repeated citation key points to records with different DOI, title, author, or year metadata",
                "human_review_required": True,
                "verification_limit": "internal conflict only; this does not prove which record is correct",
            }
        )
    return warnings


def same_doi_conflicting_title_warnings(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    warnings: list[dict[str, Any]] = []
    for doi, grouped_records in group_records_by_value(records, visible_doi).items():
        if len(grouped_records) < 2:
            continue
        normalized_titles = {
            normalize_title(visible_title(record))
            for _index, record in grouped_records
            if normalize_title(visible_title(record))
        }
        if len(normalized_titles) < 2:
            continue
        warnings.append(
            {
                "code": "same_doi_conflicting_titles",
                "severity": "high",
                "doi": doi,
                "record_ids": record_ids(grouped_records),
                "message": "same DOI is attached to different normalized titles",
                "human_review_required": True,
                "verification_limit": "internal conflict only; DOI ownership is not externally verified",
            }
        )
    return warnings


def same_title_conflicting_metadata_warnings(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    warnings: list[dict[str, Any]] = []
    for title, grouped_records in group_records_by_value(records, lambda record: normalize_title(visible_title(record))).items():
        if len(grouped_records) < 2:
            continue
        dois = {visible_doi(record) for _index, record in grouped_records if visible_doi(record)}
        years = {publication_year(record) for _index, record in grouped_records if publication_year(record)}
        authors = {
            normalize_lower_words(first_public_text(record, AUTHOR_EDITOR_ALIASES))
            for _index, record in grouped_records
            if normalize_lower_words(first_public_text(record, AUTHOR_EDITOR_ALIASES))
        }
        if max(len(dois), len(years), len(authors)) < 2:
            continue
        warnings.append(
            {
                "code": "same_title_conflicting_metadata",
                "severity": "medium",
                "title": title,
                "record_ids": record_ids(grouped_records),
                "message": "same normalized title is attached to conflicting DOI, author, or year metadata",
                "human_review_required": True,
                "verification_limit": "internal conflict only; title match is not source-claim verification",
            }
        )
    return warnings


def collection_warnings(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    warnings: list[dict[str, Any]] = []
    warnings.extend(citation_key_conflict_warnings(records))
    warnings.extend(same_doi_conflicting_title_warnings(records))
    warnings.extend(same_title_conflicting_metadata_warnings(records))
    return sorted(warnings, key=lambda warning: (warning["severity"] != "high", warning["code"], warning["record_ids"]))


def evaluate_metadata_report(
    records: list[dict[str, Any]],
    lookup_states: list[PublicLookupState] | None = None,
) -> dict[str, Any]:
    warnings = collection_warnings(records)
    return {
        "records": evaluate_records(records, lookup_states),
        "collection_warnings": warnings,
        "validation_scope": "local metadata consistency only",
        "verification_limits": [
            "metadata internally consistent does not mean source exists",
            "source existence does not mean the source supports a manuscript claim",
            "external metadata lookup is not performed unless an allowed lookup provider is explicitly consented",
        ],
    }


def metadata_lookup_consent_errors(*, lookup_provider: str, allow_network: bool) -> list[str]:
    if lookup_provider not in LOOKUP_PROVIDERS:
        return [f"unsupported lookup provider {lookup_provider!r}"]
    if lookup_provider != "none" and not allow_network:
        return ["public metadata lookup requires --allow-network with --lookup-provider crossref"]
    return []


def bounded_lookup_timeout(value: str) -> float:
    try:
        timeout = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("lookup timeout must be a number") from exc
    if timeout <= 0 or timeout > MAX_LOOKUP_TIMEOUT_SECONDS:
        raise argparse.ArgumentTypeError(
            f"lookup timeout must be greater than 0 and at most {MAX_LOOKUP_TIMEOUT_SECONDS:g} seconds"
        )
    return timeout


def crossref_work_url(doi: str) -> str:
    encoded_doi = urllib.parse.quote(normalize_identifier(doi), safe="")
    return f"{CROSSREF_WORKS_ENDPOINT}{encoded_doi}"


def first_string(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        for item in value:
            if isinstance(item, str) and item.strip():
                return item.strip()
    return ""


def crossref_year(message: dict[str, Any]) -> str:
    for key in ["published-print", "published-online", "published", "issued", "created"]:
        value = message.get(key)
        if not isinstance(value, dict):
            continue
        date_parts = value.get("date-parts")
        if not isinstance(date_parts, list) or not date_parts:
            continue
        first_part = date_parts[0]
        if isinstance(first_part, list) and first_part:
            year = first_part[0]
            if isinstance(year, int):
                return str(year)
            if isinstance(year, str) and year.isdigit():
                return year
    return ""


def crossref_author_label(message: dict[str, Any]) -> str:
    authors = message.get("author")
    if not isinstance(authors, list):
        return ""

    family_names = [
        family.strip()
        for author in authors
        if isinstance(author, dict)
        for family in [str(author.get("family", ""))]
        if family.strip()
    ]
    if not family_names:
        return ""
    if len(family_names) == 1:
        return family_names[0]
    if len(family_names) == 2:
        return f"{family_names[0]} and {family_names[1]}"
    return f"{family_names[0]} et al."


def crossref_author_year(message: dict[str, Any]) -> str:
    author_label = crossref_author_label(message)
    year = crossref_year(message)
    return " ".join(part for part in [author_label, year] if part)


def public_metadata_from_crossref_message(message: dict[str, Any]) -> dict[str, str]:
    metadata = {
        "authoritative_doi": first_string(message.get("DOI")),
        "authoritative_title": first_string(message.get("title")),
        "authoritative_author_year": crossref_author_year(message),
        "authoritative_venue": first_string(message.get("container-title")),
    }
    return {key: value for key, value in metadata.items() if value}


def fetch_crossref_metadata(doi: str, timeout: float) -> dict[str, str]:
    request = urllib.request.Request(
        crossref_work_url(doi),
        headers={"Accept": "application/json", "User-Agent": CROSSREF_USER_AGENT},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        response_body = response.read(MAX_CROSSREF_RESPONSE_BYTES + 1)
    if len(response_body) > MAX_CROSSREF_RESPONSE_BYTES:
        raise ValueError(f"Crossref response exceeded {MAX_CROSSREF_RESPONSE_BYTES} bytes")
    payload = json.loads(response_body.decode("utf-8"))
    message = payload.get("message") if isinstance(payload, dict) else None
    return public_metadata_from_crossref_message(message) if isinstance(message, dict) else {}


def enrich_record_with_public_metadata(record: dict[str, Any], metadata: dict[str, str]) -> dict[str, Any]:
    enriched_record = dict(record)
    for key, value in metadata.items():
        if not text_value(enriched_record, key):
            enriched_record[key] = value
    return enriched_record


def enrich_records_with_public_lookup_result(
    records: list[dict[str, Any]], *, lookup_provider: str, timeout: float
) -> tuple[list[dict[str, Any]], list[PublicLookupState]]:
    if lookup_provider == "none":
        return records, [NO_PUBLIC_LOOKUP for _record in records]

    enriched_records: list[dict[str, Any]] = []
    lookup_states: list[PublicLookupState] = []
    for record in records:
        claimed_doi = normalize_identifier(text_value(record, "claimed_doi"))
        if not claimed_doi or not DOI_RE.match(claimed_doi):
            enriched_records.append(record)
            lookup_states.append(NO_PUBLIC_LOOKUP)
            continue
        metadata = fetch_crossref_metadata(claimed_doi, timeout)
        enriched_records.append(enrich_record_with_public_metadata(record, metadata))
        lookup_states.append(PublicLookupState(attempted=True, metadata_returned=bool(metadata)))
    return enriched_records, lookup_states


def enrich_records_with_public_lookup(
    records: list[dict[str, Any]], *, lookup_provider: str, timeout: float
) -> list[dict[str, Any]]:
    enriched_records, _lookup_states = enrich_records_with_public_lookup_result(
        records,
        lookup_provider=lookup_provider,
        timeout=timeout,
    )
    return enriched_records


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Local JSON or CSV metadata export.")
    parser.add_argument(
        "--lookup-provider",
        choices=sorted(LOOKUP_PROVIDERS),
        default="none",
        help="Optional public metadata provider. Default is local no-network mode.",
    )
    parser.add_argument(
        "--allow-network",
        action="store_true",
        help="Required before any public metadata lookup. The lookup submits DOI identifiers only.",
    )
    parser.add_argument(
        "--lookup-timeout",
        type=bounded_lookup_timeout,
        default=10.0,
        help="Network timeout in seconds for explicit public metadata lookup.",
    )
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

    consent_errors = metadata_lookup_consent_errors(
        lookup_provider=args.lookup_provider,
        allow_network=args.allow_network,
    )
    if consent_errors:
        print(json.dumps({"errors": consent_errors}, indent=2))
        return 1

    try:
        checked_records, lookup_states = enrich_records_with_public_lookup_result(
            records,
            lookup_provider=args.lookup_provider,
            timeout=args.lookup_timeout,
        )
    except (OSError, urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"errors": [f"public metadata lookup failed: {error}"]}, indent=2))
        return 1

    report = evaluate_metadata_report(checked_records, lookup_states)
    print(json.dumps(report, indent=2))
    record_has_risk = any(result["risk"] in {"medium", "high"} for result in report["records"])
    collection_has_risk = any(warning["severity"] in {"medium", "high"} for warning in report["collection_warnings"])
    return 1 if record_has_risk or collection_has_risk else 0


if __name__ == "__main__":
    raise SystemExit(main())
