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
    evaluate_records,
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
    }


class TestCitationMetadataChecks(unittest.TestCase):
    def test_matching_metadata_is_low_risk(self) -> None:
        results = evaluate_records([matching_record()])

        self.assertEqual(results[0]["status"], "metadata_match")
        self.assertEqual(results[0]["risk"], "low")
        self.assertEqual(results[0]["doi_status"], "match")
        self.assertEqual(results[0]["title_status"], "match")

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


if __name__ == "__main__":
    unittest.main()
