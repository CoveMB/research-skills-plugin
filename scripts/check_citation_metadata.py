#!/usr/bin/env python3
"""Check local citation metadata exports without private text."""
from __future__ import annotations

import argparse
import csv
import json
import re
import string
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Callable, NamedTuple


PRIVATE_FIELDS = {
    "abstract",
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
DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$", re.IGNORECASE)
ARXIV_NEW_RE = re.compile(r"^\d{4}\.\d{4,5}$")
ARXIV_OLD_RE = re.compile(r"^[a-z-]+(?:\.[a-z]{2})?/\d{7}$")
PMID_RE = re.compile(r"^\d{1,9}$")
OCLC_RE = re.compile(r"^\d+$")
LCCN_RE = re.compile(r"^[a-z]{0,3}\d{6,10}$")
LOOKUP_PROVIDERS = {"none", "crossref"}
CROSSREF_WORKS_ENDPOINT = "https://api.crossref.org/v1/works/"
CROSSREF_USER_AGENT = "scholarly-research-book-plugin/1.0 (public metadata lookup)"


class MetadataPairSpec(NamedTuple):
    claimed_key: str
    authoritative_key: str
    status_key: str
    mismatch_note: str
    comparator: Callable[[str, str], str]


def read_json_records(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        records = payload
    elif isinstance(payload, dict) and isinstance(payload.get("records"), list):
        records = payload["records"]
    else:
        raise ValueError("JSON input must be a list or an object with a records list")
    return validate_metadata_records(records)


def read_csv_records(path: Path) -> list[dict[str, Any]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return validate_metadata_records([dict(row) for row in csv.DictReader(handle)])


def validate_metadata_records(records: list[Any]) -> list[dict[str, Any]]:
    if not records:
        raise ValueError("input must contain at least one metadata record")

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


def record_id(record: dict[str, Any], index: int = 0) -> str:
    value = record.get("reference_id") or record.get("id") or record.get("citation_key")
    return str(value) if value else f"record-{index + 1}"


def normalized_field_name(field: str) -> str:
    return " ".join(field.replace("_", " ").casefold().split())


NORMALIZED_PRIVATE_FIELDS = {normalized_field_name(private_field) for private_field in PRIVATE_FIELDS}


def is_private_field(field: str) -> bool:
    return normalized_field_name(field) in NORMALIZED_PRIVATE_FIELDS


def private_field_errors(records: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for index, record in enumerate(records):
        identifier = record_id(record, index)
        for field in sorted(record.keys()):
            if not is_private_field(field):
                continue
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


def normalize_lower_words(value: str) -> str:
    return " ".join(value.lower().split())


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


def evaluate_record(record: dict[str, Any], index: int) -> dict[str, Any]:
    statuses = {
        spec.status_key: spec.comparator(
            text_value(record, spec.claimed_key),
            text_value(record, spec.authoritative_key),
        )
        for spec in METADATA_PAIR_SPECS
    }
    status, risk = status_and_risk(statuses)
    notes = mismatch_notes(statuses)
    notes.extend(
        note
        for status_key, note in FORMAT_WARNING_NOTES.items()
        if statuses.get(status_key) == "format_warning"
    )
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


def metadata_lookup_consent_errors(*, lookup_provider: str, allow_network: bool) -> list[str]:
    if lookup_provider not in LOOKUP_PROVIDERS:
        return [f"unsupported lookup provider {lookup_provider!r}"]
    if lookup_provider != "none" and not allow_network:
        return ["public metadata lookup requires --allow-network with --lookup-provider crossref"]
    return []


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
        payload = json.loads(response.read().decode("utf-8"))
    message = payload.get("message") if isinstance(payload, dict) else None
    return public_metadata_from_crossref_message(message) if isinstance(message, dict) else {}


def enrich_record_with_public_metadata(record: dict[str, Any], metadata: dict[str, str]) -> dict[str, Any]:
    enriched_record = dict(record)
    for key, value in metadata.items():
        if not text_value(enriched_record, key):
            enriched_record[key] = value
    return enriched_record


def enrich_records_with_public_lookup(
    records: list[dict[str, Any]], *, lookup_provider: str, timeout: float
) -> list[dict[str, Any]]:
    if lookup_provider == "none":
        return records

    enriched_records: list[dict[str, Any]] = []
    for record in records:
        claimed_doi = normalize_identifier(text_value(record, "claimed_doi"))
        if not claimed_doi or not DOI_RE.match(claimed_doi):
            enriched_records.append(record)
            continue
        metadata = fetch_crossref_metadata(claimed_doi, timeout)
        enriched_records.append(enrich_record_with_public_metadata(record, metadata))
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
        type=float,
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
        checked_records = enrich_records_with_public_lookup(
            records,
            lookup_provider=args.lookup_provider,
            timeout=args.lookup_timeout,
        )
    except (OSError, urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"errors": [f"public metadata lookup failed: {error}"]}, indent=2))
        return 1

    results = evaluate_records(checked_records)
    print(json.dumps({"records": results}, indent=2))
    return 1 if any(result["risk"] in {"medium", "high"} for result in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
