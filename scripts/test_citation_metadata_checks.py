"""Tests for local citation metadata checks."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_citation_metadata import (
    METADATA_PAIR_SPECS,
    crossref_work_url,
    evaluate_records,
    metadata_lookup_consent_errors,
    public_identifier_status,
    private_field_errors,
)


SCRIPT = Path(__file__).resolve().parent / "check_citation_metadata.py"


def matching_record() -> dict[str, str]:
    return {
        "reference_id": "fixture-reference",
        "claimed_doi": "10.0000/fixture-only",
        "authoritative_doi": "https://doi.org/10.0000/fixture-only",
        "claimed_title": "Fixture Metadata Check",
        "authoritative_title": "Fixture metadata check",
        "claimed_author_year": "Fixture 2026",
        "authoritative_author_year": "Fixture 2026",
        "claimed_venue": "Fixture Venue",
        "authoritative_venue": "Fixture Venue",
        "claimed_isbn": "978-0-306-40615-7",
        "authoritative_isbn": "9780306406157",
        "claimed_arxiv_id": "2604.05018",
        "authoritative_arxiv_id": "arXiv:2604.05018v1",
        "claimed_pmid": "12345678",
        "authoritative_pmid": "PMID:12345678",
        "claimed_oclc": "ocm12345678",
        "authoritative_oclc": "12345678",
        "claimed_lccn": "2002022641",
        "authoritative_lccn": " 2002022641 ",
    }


class TestCitationMetadataChecks(unittest.TestCase):
    def test_metadata_pair_specs_drive_output_statuses(self) -> None:
        status_keys = [spec.status_key for spec in METADATA_PAIR_SPECS]
        results = evaluate_records([matching_record()])

        self.assertEqual(
            status_keys,
            [
                "doi_status",
                "isbn_status",
                "arxiv_id_status",
                "pmid_status",
                "oclc_status",
                "lccn_status",
                "title_status",
                "author_year_status",
                "venue_status",
            ],
        )
        self.assertTrue(all(status_key in results[0] for status_key in status_keys))

    def test_matching_metadata_is_low_risk(self) -> None:
        results = evaluate_records([matching_record()])

        self.assertEqual(results[0]["status"], "metadata_match")
        self.assertEqual(results[0]["risk"], "low")
        self.assertEqual(results[0]["doi_status"], "match")
        self.assertEqual(results[0]["isbn_status"], "match")
        self.assertEqual(results[0]["arxiv_id_status"], "match")
        self.assertEqual(results[0]["pmid_status"], "match")
        self.assertEqual(results[0]["oclc_status"], "match")
        self.assertEqual(results[0]["lccn_status"], "match")
        self.assertEqual(results[0]["title_status"], "match")

    def test_absent_optional_identifiers_do_not_downgrade_complete_core_metadata(self) -> None:
        record = {
            key: value
            for key, value in matching_record().items()
            if key
            not in {
                "claimed_isbn",
                "authoritative_isbn",
                "claimed_arxiv_id",
                "authoritative_arxiv_id",
                "claimed_pmid",
                "authoritative_pmid",
                "claimed_oclc",
                "authoritative_oclc",
                "claimed_lccn",
                "authoritative_lccn",
            }
        }

        results = evaluate_records([record])

        self.assertEqual(results[0]["status"], "metadata_match")
        self.assertEqual(results[0]["risk"], "low")
        self.assertEqual(results[0]["isbn_status"], "not_provided")

    def test_public_identifier_mismatch_is_reported(self) -> None:
        record = matching_record()
        record["authoritative_isbn"] = "9780306406164"

        results = evaluate_records([record])

        self.assertEqual(results[0]["isbn_status"], "mismatch")
        self.assertEqual(results[0]["status"], "metadata_mismatch")
        self.assertEqual(results[0]["risk"], "medium")
        self.assertIn("ISBN mismatch", results[0]["notes"])

    def test_public_identifier_format_warnings_are_reported(self) -> None:
        record = matching_record()
        record["claimed_isbn"] = "9780306406158"
        record["claimed_arxiv_id"] = "not arxiv"
        record["claimed_pmid"] = "PMID:abc"
        record["claimed_oclc"] = "oclc:abc"
        record["claimed_lccn"] = "bad/lccn"

        results = evaluate_records([record])

        self.assertEqual(results[0]["isbn_status"], "format_warning")
        self.assertEqual(results[0]["arxiv_id_status"], "format_warning")
        self.assertEqual(results[0]["pmid_status"], "format_warning")
        self.assertEqual(results[0]["oclc_status"], "format_warning")
        self.assertEqual(results[0]["lccn_status"], "format_warning")
        self.assertEqual(results[0]["status"], "metadata_format_warning")
        self.assertIn("ISBN format warning", results[0]["notes"])
        self.assertIn("arXiv ID format warning", results[0]["notes"])
        self.assertIn("PMID format warning", results[0]["notes"])
        self.assertIn("OCLC format warning", results[0]["notes"])
        self.assertIn("LCCN format warning", results[0]["notes"])

    def test_public_identifier_status_normalizes_known_public_prefixes(self) -> None:
        self.assertEqual(public_identifier_status("isbn", "ISBN 978-0-306-40615-7", "9780306406157"), "match")
        self.assertEqual(public_identifier_status("arxiv_id", "arXiv:2604.05018v1", "2604.05018"), "match")
        self.assertEqual(public_identifier_status("pmid", "PMID:12345678", "12345678"), "match")
        self.assertEqual(public_identifier_status("oclc", "ocm12345678", "12345678"), "match")
        self.assertEqual(public_identifier_status("lccn", " 2002022641 ", "2002022641"), "match")
        self.assertEqual(public_identifier_status("isbn", "ISBN unknown", ""), "format_warning")

    def test_identifier_and_title_mismatch_flags_hijack_risk(self) -> None:
        record = matching_record()
        record["authoritative_doi"] = "10.0000/different-fixture"
        record["authoritative_title"] = "Different Fixture Title"

        results = evaluate_records([record])

        self.assertEqual(results[0]["status"], "identifier_hijack_risk")
        self.assertEqual(results[0]["risk"], "high")
        self.assertIn("DOI mismatch", results[0]["notes"])
        self.assertIn("title mismatch", results[0]["notes"])

    def test_private_fields_are_rejected(self) -> None:
        record = matching_record()
        record["abstract"] = "Private or full-text-like material does not belong in this helper."

        errors = private_field_errors([record])

        self.assertEqual(errors, ["fixture-reference: remove private field 'abstract'"])

    def test_private_field_aliases_are_rejected(self) -> None:
        record = matching_record()
        record["Full Text"] = "Private source text does not belong in this helper."

        errors = private_field_errors([record])

        self.assertEqual(errors, ["fixture-reference: remove private field 'Full Text'"])

    def test_invalid_doi_format_is_reported(self) -> None:
        record = matching_record()
        record["claimed_doi"] = "fixture-only"

        results = evaluate_records([record])

        self.assertEqual(results[0]["doi_status"], "format_warning")
        self.assertEqual(results[0]["risk"], "medium")

    def test_absent_metadata_is_not_treated_as_low_risk(self) -> None:
        results = evaluate_records([{"reference_id": "empty-fixture"}])

        self.assertEqual(results[0]["status"], "metadata_partly_unchecked")
        self.assertEqual(results[0]["risk"], "medium")
        self.assertIn("metadata pair missing or unchecked", results[0]["notes"])

    def test_cli_outputs_json_and_fails_on_private_fields(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            input_path = root / "metadata.json"
            record = matching_record()
            record["full_text"] = "Do not pass source text to this helper."
            input_path.write_text(json.dumps({"records": [record]}), encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--input", str(input_path)],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn("remove private field", result.stdout)

    def test_cli_fails_on_non_object_json_records(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            input_path = root / "metadata.json"
            input_path.write_text(json.dumps({"records": [matching_record(), "not a record"]}), encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--input", str(input_path)],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn("record 2 must be an object", result.stdout)

    def test_cli_fails_on_empty_record_set(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            input_path = root / "metadata.json"
            input_path.write_text(json.dumps({"records": []}), encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--input", str(input_path)],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn("at least one metadata record", result.stdout)

    def test_public_lookup_requires_explicit_network_consent(self) -> None:
        errors = metadata_lookup_consent_errors(lookup_provider="crossref", allow_network=False)

        self.assertEqual(
            errors,
            ["public metadata lookup requires --allow-network with --lookup-provider crossref"],
        )

    def test_public_lookup_consent_not_required_for_local_mode(self) -> None:
        errors = metadata_lookup_consent_errors(lookup_provider="none", allow_network=False)

        self.assertEqual(errors, [])

    def test_crossref_lookup_url_uses_encoded_public_doi_only(self) -> None:
        url = crossref_work_url("https://doi.org/10.0000/Fixture Case")

        self.assertEqual(url, "https://api.crossref.org/v1/works/10.0000%2Ffixture%20case")

    def test_cli_rejects_lookup_without_network_consent(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            input_path = root / "metadata.json"
            input_path.write_text(json.dumps({"records": [matching_record()]}), encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--input",
                    str(input_path),
                    "--lookup-provider",
                    "crossref",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn("requires --allow-network", result.stdout)


if __name__ == "__main__":
    unittest.main()
