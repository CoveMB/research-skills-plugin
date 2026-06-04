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
            self.assertEqual(cluster["duplicate_status"], "exact_duplicate")
            self.assertEqual(cluster["match_reasons"], ["normalized DOI match"])
            self.assertEqual(cluster["confidence"], "high")
            self.assertFalse(cluster["review_needed"])
            self.assertFalse(cluster["human_review_required"])
            self.assertTrue(cluster["preserve_records"])
            self.assertEqual(report["errors"], [])

    def test_exact_doi_match_is_labeled_separately_from_normalized_doi_match(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory) / "candidates.json"
            input_path.write_text(
                json.dumps(
                    {
                        "records": [
                            {
                                "candidate_id": "first",
                                "title": "Exact DOI Fixture",
                                "authors": "Example Author",
                                "year": "2026",
                                "doi": "10.0000/exact-fixture",
                            },
                            {
                                "candidate_id": "second",
                                "title": "Exact DOI Fixture",
                                "authors": "Example Author",
                                "year": "2026",
                                "doi": "10.0000/exact-fixture",
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )

            cluster = build_candidate_report(input_path)["duplicate_clusters"][0]

            self.assertEqual(cluster["duplicate_status"], "exact_duplicate")
            self.assertEqual(cluster["match_basis"], "exact_doi")
            self.assertEqual(cluster["match_reasons"], ["exact DOI match"])
            self.assertFalse(cluster["human_review_required"])

    def test_same_doi_with_conflicting_titles_requires_human_review(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory) / "candidates.json"
            input_path.write_text(
                json.dumps(
                    [
                        {
                            "id": "first-work",
                            "title": "First Fixture Work",
                            "doi": "10.0000/shared-fixture",
                        },
                        {
                            "id": "different-work",
                            "title": "Different Fixture Work",
                            "doi": "10.0000/shared-fixture",
                        },
                    ]
                ),
                encoding="utf-8",
            )

            cluster = build_candidate_report(input_path)["duplicate_clusters"][0]

            self.assertEqual(cluster["duplicate_status"], "related_but_distinct")
            self.assertTrue(cluster["human_review_required"])
            self.assertIn("conflicting title metadata", cluster["false_merge_warnings"])

    def test_same_stable_identifier_with_conflicting_titles_requires_human_review(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory) / "candidates.json"
            input_path.write_text(
                json.dumps(
                    [
                        {
                            "id": "first-record",
                            "title": "First Fixture Work",
                            "openalex_id": "W000000001",
                        },
                        {
                            "id": "second-record",
                            "title": "Different Fixture Work",
                            "openalex_id": "W000000001",
                        },
                    ]
                ),
                encoding="utf-8",
            )

            cluster = build_candidate_report(input_path)["duplicate_clusters"][0]

            self.assertEqual(cluster["duplicate_status"], "related_but_distinct")
            self.assertTrue(cluster["human_review_required"])
            self.assertIn("conflicting title metadata", cluster["false_merge_warnings"])

    def test_invalid_doi_placeholder_does_not_create_exact_duplicate(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory) / "candidates.json"
            input_path.write_text(
                json.dumps(
                    [
                        {
                            "id": "placeholder-a",
                            "title": "One fixture article",
                            "authors": "First Author",
                            "year": "2024",
                            "doi": "unknown",
                        },
                        {
                            "id": "placeholder-b",
                            "title": "Different fixture article",
                            "authors": "Second Author",
                            "year": "2025",
                            "doi": "unknown",
                        },
                    ]
                ),
                encoding="utf-8",
            )

            report = build_candidate_report(input_path)

            self.assertEqual(report["duplicate_clusters"], [])
            warnings_by_id = {
                warning["candidate_id"]: warning["warnings"]
                for warning in report["metadata_warnings"]
            }
            self.assertEqual(
                warnings_by_id,
                {
                    "placeholder-a": ["invalid DOI format", "missing DOI or stable identifier"],
                    "placeholder-b": ["invalid DOI format", "missing DOI or stable identifier"],
                },
            )

    def test_stable_identifier_placeholders_do_not_create_exact_duplicate(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory) / "candidates.json"
            input_path.write_text(
                json.dumps(
                    [
                        {
                            "id": "stable-placeholder-a",
                            "title": "Migration in Coastal Cities",
                            "openalex_id": "unknown",
                            "pmid": "tbd",
                            "semantic_scholar_id": "-",
                            "stable_id": "N/A",
                        },
                        {
                            "id": "stable-placeholder-b",
                            "title": "Publishing Rights Clearance",
                            "openalex_id": "unknown",
                            "pmid": "tbd",
                            "semantic_scholar_id": "-",
                            "stable_id": "N/A",
                        },
                    ]
                ),
                encoding="utf-8",
            )

            report = build_candidate_report(input_path)

            self.assertEqual(report["duplicate_clusters"], [])
            self.assertEqual(report["records"][0]["stable_identifiers"], [])
            self.assertEqual(report["records"][1]["stable_identifiers"], [])
            warnings_by_id = {
                warning["candidate_id"]: warning["warnings"]
                for warning in report["metadata_warnings"]
            }
            self.assertEqual(
                warnings_by_id,
                {
                    "stable-placeholder-a": ["missing DOI or stable identifier"],
                    "stable-placeholder-b": ["missing DOI or stable identifier"],
                },
            )

    def test_stable_identifier_matching_is_case_insensitive(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory) / "candidates.json"
            input_path.write_text(
                json.dumps(
                    [
                        {
                            "id": "openalex-upper",
                            "title": "Fixture work",
                            "openalex_id": "W000000001",
                        },
                        {
                            "id": "openalex-lower",
                            "title": "Fixture work",
                            "openalex_id": "w000000001",
                        },
                    ]
                ),
                encoding="utf-8",
            )

            cluster = build_candidate_report(input_path)["duplicate_clusters"][0]

            self.assertEqual(cluster["candidate_ids"], ["openalex-upper", "openalex-lower"])
            self.assertEqual(cluster["match_basis"], "stable_identifier")
            self.assertEqual(cluster["duplicate_status"], "exact_duplicate")
            self.assertEqual(cluster["confidence"], "high")
            self.assertFalse(cluster["human_review_required"])

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
            self.assertEqual(report["duplicate_clusters"][0]["duplicate_status"], "probable_duplicate")
            self.assertEqual(report["duplicate_clusters"][0]["confidence"], "medium")
            self.assertTrue(report["duplicate_clusters"][0]["review_needed"])
            self.assertTrue(report["duplicate_clusters"][0]["human_review_required"])

    def test_author_year_title_similarity_flags_probable_duplicate(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory) / "candidates.json"
            input_path.write_text(
                json.dumps(
                    [
                        {
                            "id": "article-a",
                            "title": "Urban Climate Adaptation and Public Health",
                            "authors": "Rivera and Singh",
                            "year": "2024",
                        },
                        {
                            "id": "article-b",
                            "title": "Urban climate adaptation & public health",
                            "authors": "Rivera and Singh",
                            "year": "2024",
                        },
                    ]
                ),
                encoding="utf-8",
            )

            cluster = build_candidate_report(input_path)["duplicate_clusters"][0]

            self.assertEqual(cluster["duplicate_status"], "probable_duplicate")
            self.assertEqual(cluster["match_basis"], "author_year_title_similarity")
            self.assertIn("author-year-title similarity", cluster["match_reasons"])
            self.assertTrue(cluster["human_review_required"])

    def test_title_only_near_duplicate_requires_human_review(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory) / "candidates.json"
            input_path.write_text(
                json.dumps(
                    [
                        {"id": "title-a", "title": "Climate adaptation in coastal cities"},
                        {"id": "title-b", "title": "Climate adaptation for coastal cities"},
                    ]
                ),
                encoding="utf-8",
            )

            cluster = build_candidate_report(input_path)["duplicate_clusters"][0]

            self.assertEqual(cluster["duplicate_status"], "possible_duplicate")
            self.assertEqual(cluster["match_basis"], "title_similarity")
            self.assertTrue(cluster["human_review_required"])
            self.assertIn("title-only near duplicate", cluster["match_reasons"])

    def test_preprint_published_pair_is_related_but_distinct(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory) / "candidates.json"
            input_path.write_text(
                json.dumps(
                    [
                        {
                            "id": "preprint",
                            "title": "Measuring adaptation policy uptake",
                            "authors": "Example Author",
                            "year": "2025",
                            "venue": "arXiv",
                            "arxiv_id": "2501.00001",
                        },
                        {
                            "id": "published",
                            "title": "Measuring adaptation policy uptake",
                            "authors": "Example Author",
                            "year": "2025",
                            "venue": "Journal of Climate Policy",
                            "doi": "10.0000/published-fixture",
                        },
                    ]
                ),
                encoding="utf-8",
            )

            cluster = build_candidate_report(input_path)["duplicate_clusters"][0]

            self.assertEqual(cluster["duplicate_status"], "related_but_distinct")
            self.assertTrue(cluster["human_review_required"])
            self.assertIn("preprint and published version distinction", cluster["false_merge_warnings"])

    def test_edition_distinction_is_not_silently_merged(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory) / "candidates.json"
            input_path.write_text(
                json.dumps(
                    [
                        {
                            "id": "first-edition",
                            "title": "Handbook of Urban Resilience",
                            "authors": "Example Editor",
                            "year": "2018",
                            "edition": "First edition",
                        },
                        {
                            "id": "second-edition",
                            "title": "Handbook of Urban Resilience",
                            "authors": "Example Editor",
                            "year": "2024",
                            "edition": "Second edition",
                        },
                    ]
                ),
                encoding="utf-8",
            )

            cluster = build_candidate_report(input_path)["duplicate_clusters"][0]

            self.assertEqual(cluster["duplicate_status"], "related_but_distinct")
            self.assertTrue(cluster["human_review_required"])
            self.assertIn("edition or version distinction", cluster["false_merge_warnings"])

    def test_conflicting_metadata_adds_false_merge_warning(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory) / "candidates.json"
            input_path.write_text(
                json.dumps(
                    [
                        {
                            "id": "city-report",
                            "title": "Cities and Adaptation",
                            "authors": "Ada Researcher",
                            "year": "2020",
                        },
                        {
                            "id": "different-work",
                            "title": "Cities and Adaptation",
                            "authors": "Ben Scholar",
                            "year": "2024",
                        },
                    ]
                ),
                encoding="utf-8",
            )

            cluster = build_candidate_report(input_path)["duplicate_clusters"][0]

            self.assertEqual(cluster["duplicate_status"], "related_but_distinct")
            self.assertIn("conflicting author metadata", cluster["false_merge_warnings"])
            self.assertIn("conflicting year metadata", cluster["false_merge_warnings"])

    def test_missing_metadata_is_reported_without_duplicate_cluster(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory) / "candidates.json"
            input_path.write_text(json.dumps([{"id": "thin-record", "search_status": "planned"}]), encoding="utf-8")

            report = build_candidate_report(input_path)

            self.assertEqual(report["duplicate_clusters"], [])
            self.assertEqual(
                report["metadata_warnings"],
                [
                    {
                        "candidate_id": "thin-record",
                        "duplicate_status": "insufficient_metadata",
                        "human_review_required": True,
                        "warnings": ["missing title", "missing DOI or stable identifier"],
                    }
                ],
            )

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
