"""Tests for deterministic figure/table provenance checks."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_figure_table_provenance as checker


SCRIPT = Path(__file__).resolve().parent / "check_figure_table_provenance.py"
ROOT = Path(__file__).resolve().parents[1]
VALID_EXAMPLE = ROOT / "examples" / "figure_table_provenance" / "valid-provenance.json"
INVALID_EXAMPLE = ROOT / "examples" / "figure_table_provenance" / "invalid-provenance.json"


def valid_record() -> dict[str, object]:
    return {
        "object_id": "fig-1",
        "object_type": "figure",
        "title": "Fixture trend chart",
        "caption": "Fixture trend chart using the 2026 fixture dataset.",
        "claim_supported": "The fixture rate increased from 2020 to 2025.",
        "data_source": "2026 fixture dataset",
        "source_access_level": "public dataset",
        "dataset_version": "v1.0",
        "transformation_notes": "Calculated annual rates from raw counts divided by eligible population.",
        "denominator": "eligible population, n=1,250",
        "sample_size": "1,250 records",
        "aggregation_level": "annual city-level rate",
        "x_axis_label": "Year",
        "y_axis_label": "Rate per 1,000 residents",
        "units": "rate per 1,000 residents",
        "caption_source_consistency": "consistent",
        "uncertainty_notes": "95% confidence intervals shown.",
        "rights_status": "cc-by-4.0",
        "origin": "original",
        "human_review_required": False,
    }


def report_for(records: list[dict[str, object]]) -> dict[str, object]:
    with TemporaryDirectory() as temporary_directory:
        input_path = Path(temporary_directory) / "provenance.json"
        input_path.write_text(json.dumps({"records": records}), encoding="utf-8")
        return checker.build_provenance_report(input_path)


def issue_codes(record_result: dict[str, object]) -> set[str]:
    return {
        issue["code"]
        for issue in record_result["issues"]
        if isinstance(issue, dict) and isinstance(issue.get("code"), str)
    }


class TestFigureTableProvenanceChecks(unittest.TestCase):
    def test_valid_example_passes(self) -> None:
        report = checker.build_provenance_report(VALID_EXAMPLE)

        self.assertEqual(report["schema_version"], "figure-table-provenance-check-v1")
        self.assertEqual(report["execution_mode"], "deterministic-local")
        self.assertEqual(report["records"][0]["provenance_status"], "provenance_complete")
        self.assertFalse(report["records"][0]["human_review_required"])
        self.assertEqual(report["errors"], [])

    def test_non_chart_figure_does_not_require_axis_labels(self) -> None:
        record = {
            "object_id": "fig-photo",
            "object_type": "figure",
            "title": "Archive site photograph",
            "caption": "Archive photograph of the fixture site.",
            "claim_supported": "The fixture site existed before redevelopment.",
            "data_source": "City archive photo collection",
            "source_access_level": "public archive",
            "dataset_version": "collection v1",
            "transformation_notes": "Cropped for layout; no data calculation performed.",
            "aggregation_level": "single image",
            "caption_source_consistency": "consistent",
            "rights_status": "public-domain",
            "origin": "reproduced",
            "human_review_required": False,
        }

        result = report_for([record])["records"][0]

        self.assertEqual(result["provenance_status"], "provenance_complete")
        self.assertNotIn("missing_x_axis_label", issue_codes(result))
        self.assertNotIn("missing_y_axis_label", issue_codes(result))

    def test_missing_denominator_is_flagged_for_rate_claim(self) -> None:
        record = valid_record()
        record.pop("denominator")
        record["caption"] = "Fixture rate by year."

        result = report_for([record])["records"][0]

        self.assertEqual(result["provenance_status"], "provenance_gaps")
        self.assertIn("missing_denominator_or_sample_size", issue_codes(result))
        self.assertTrue(result["human_review_required"])

    def test_missing_sample_size_is_flagged_when_declared_relevant(self) -> None:
        record = valid_record()
        record.pop("sample_size")
        record["requires_sample_size"] = True

        result = report_for([record])["records"][0]

        self.assertEqual(result["provenance_status"], "provenance_gaps")
        self.assertIn("missing_denominator_or_sample_size", issue_codes(result))
        self.assertTrue(result["human_review_required"])

    def test_missing_source_is_blocker(self) -> None:
        record = valid_record()
        record.pop("data_source")

        result = report_for([record])["records"][0]

        self.assertEqual(result["risk"], "high")
        self.assertIn("missing_data_source", issue_codes(result))
        self.assertTrue(result["human_review_required"])

    def test_misleading_axis_caption_mismatch_is_flagged(self) -> None:
        record = valid_record()
        record["caption_source_consistency"] = "mismatch: caption says national, source is city-only"

        result = report_for([record])["records"][0]

        self.assertEqual(result["risk"], "high")
        self.assertIn("caption_source_mismatch", issue_codes(result))
        self.assertIn("Caption/source consistency is reported as mismatch", result["notes"])

    def test_unknown_rights_are_flagged(self) -> None:
        record = valid_record()
        record["rights_status"] = "unknown"

        result = report_for([record])["records"][0]

        self.assertIn("unknown_rights_or_license", issue_codes(result))
        self.assertTrue(result["human_review_required"])

    def test_invalid_human_review_requirement_is_flagged(self) -> None:
        record = valid_record()
        record["human_review_required"] = "definitely complete"

        result = report_for([record])["records"][0]

        self.assertEqual(result["provenance_status"], "provenance_gaps")
        self.assertIn("invalid_human_review_requirement", issue_codes(result))
        self.assertTrue(result["human_review_required"])

    def test_generated_table_without_provenance_is_flagged(self) -> None:
        record = {
            "object_id": "table-generated",
            "object_type": "table",
            "caption": "Generated summary table of fixture rates.",
            "origin": "generated",
            "source_access_level": "none",
            "rights_status": "unknown",
        }

        result = report_for([record])["records"][0]

        codes = issue_codes(result)
        self.assertIn("generated_without_provenance", codes)
        self.assertIn("missing_data_source", codes)
        self.assertIn("missing_transformation_notes", codes)
        self.assertEqual(result["risk"], "high")
        self.assertTrue(result["human_review_required"])

    def test_invalid_example_fails_with_expected_gaps(self) -> None:
        report = checker.build_provenance_report(INVALID_EXAMPLE)

        self.assertEqual(report["records"][0]["provenance_status"], "provenance_gaps")
        self.assertIn("missing_data_source", issue_codes(report["records"][0]))
        self.assertIn("generated_without_provenance", issue_codes(report["records"][0]))

    def test_cli_returns_nonzero_for_invalid_example(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--input", str(INVALID_EXAMPLE)],
            check=False,
            text=True,
            capture_output=True,
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("generated_without_provenance", result.stdout)


if __name__ == "__main__":
    unittest.main()
