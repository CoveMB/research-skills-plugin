"""Tests for local source candidate parsing and deduping."""
from __future__ import annotations

import csv
import json
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_source_candidates import (
    build_candidate_report,
    private_field_errors,
    search_status_errors,
)


SCRIPT = Path(__file__).resolve().parent / "check_source_candidates.py"


def candidate_fixture() -> list[dict[str, str]]:
    return [
        {
            "candidate_id": "candidate-a",
            "title": "Fixture Candidate on Research Workflows",
            "authors": "Example Author",
            "year": "2026",
            "venue": "Fixture Export",
            "doi": "https://doi.org/10.0000/fixture-workflow",
            "source_export": "fixture-search",
            "search_status": "completed",
            "search_venue": "Fixture Database",
            "query": '"fixture workflow"',
            "date_searched": "2026-05-13",
        },
        {
            "candidate_id": "candidate-b",
            "title": "Fixture Candidate on Research Workflows",
            "authors": "Example Author",
            "year": "2026",
            "venue": "Fixture Export",
            "doi": "10.0000/fixture-workflow",
            "source_export": "fixture-search",
            "search_status": "completed",
            "search_venue": "Fixture Database",
            "query": '"fixture workflow"',
            "date_searched": "2026-05-13",
        },
        {
            "candidate_id": "candidate-c",
            "title": "Distinct Fixture Candidate",
            "authors": "Different Author",
            "year": "2025",
            "venue": "Fixture Export",
            "openalex_id": "W000000001",
            "search_status": "planned",
        },
    ]


class TestSourceCandidateChecks(unittest.TestCase):
    def test_json_report_normalizes_candidates_and_clusters_duplicates(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory) / "candidates.json"
            input_path.write_text(json.dumps({"records": candidate_fixture()}), encoding="utf-8")

            report = build_candidate_report(input_path)

            self.assertEqual(report["schema_version"], "source-candidate-check-v1")
            self.assertEqual(report["execution_mode"], "deterministic-local")
            self.assertIn("does not run searches", " ".join(report["limits"]))
            self.assertEqual(len(report["records"]), 3)
            self.assertEqual(report["records"][0]["candidate_id"], "candidate-a")
            self.assertEqual(report["records"][0]["doi"], "10.0000/fixture-workflow")
            self.assertEqual(report["records"][0]["stable_identifiers"], [])
            self.assertEqual(report["records"][2]["stable_identifiers"], ["openalex:W000000001"])
            self.assertEqual(len(report["duplicate_clusters"]), 1)
            cluster = report["duplicate_clusters"][0]
            self.assertEqual(cluster["candidate_ids"], ["candidate-a", "candidate-b"])
            self.assertEqual(cluster["match_basis"], "doi")
            self.assertEqual(cluster["confidence"], "high")
            self.assertFalse(cluster["review_needed"])
            self.assertEqual(report["errors"], [])

    def test_csv_input_detects_normalized_title_duplicate(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory) / "candidates.csv"
            with input_path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=["id", "title", "authors", "year"])
                writer.writeheader()
                writer.writerow({"id": "one", "title": "The Same Fixture Title", "authors": "A. Author", "year": "2026"})
                writer.writerow({"id": "two", "title": "The same fixture title!", "authors": "A Author", "year": "2026"})

            report = build_candidate_report(input_path)

            self.assertEqual(report["duplicate_clusters"][0]["match_basis"], "normalized_title")
            self.assertEqual(report["duplicate_clusters"][0]["confidence"], "medium")
            self.assertTrue(report["duplicate_clusters"][0]["review_needed"])

    def test_json_author_lists_are_normalized_for_candidate_matrix(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory) / "candidates.json"
            input_path.write_text(
                json.dumps(
                    [
                        {
                            "id": "candidate-list-authors",
                            "title": "Fixture Candidate With Author List",
                            "authors": ["First Author", "Second Author"],
                            "publication_year": 2026,
                        }
                    ]
                ),
                encoding="utf-8",
            )

            report = build_candidate_report(input_path)

            self.assertEqual(report["records"][0]["authors"], "First Author; Second Author")
            self.assertEqual(report["records"][0]["year"], "2026")

    def test_private_fields_are_rejected(self) -> None:
        records = [candidate_fixture()[0] | {"source_text": "Do not pass private source text."}]

        errors = private_field_errors(records)

        self.assertEqual(errors, ["candidate-a: remove private field 'source_text'"])

    def test_completed_search_requires_evidence_fields(self) -> None:
        records = [
            {
                "candidate_id": "candidate-a",
                "title": "Fixture Candidate",
                "search_status": "completed search",
                "search_venue": "Fixture Database",
            }
        ]

        errors = search_status_errors(records)

        self.assertEqual(
            errors,
            ["candidate-a: completed search records require search_venue, query, and date_searched"],
        )

    def test_cli_outputs_json_and_fails_on_private_fields(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory) / "candidates.json"
            records = [candidate_fixture()[0] | {"private_notes": "Internal screening notes."}]
            input_path.write_text(json.dumps(records), encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--input", str(input_path)],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn("remove private field", result.stdout)

    def test_cli_quiet_validates_clean_input_without_printing_report(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory) / "candidates.json"
            input_path.write_text(json.dumps({"records": candidate_fixture()}), encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--input", str(input_path), "--quiet"],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
