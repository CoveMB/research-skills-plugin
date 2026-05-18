"""Tests for inter-rater and live-run stability reporting."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parent))
from report_interrater import build_report


SCRIPT = Path(__file__).resolve().parent / "report_interrater.py"


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def fixtures_document() -> dict[str, object]:
    return {
        "schema_version": "scholar-grade-eval-fixtures-v1",
        "fixtures": [
            {
                "id": "citation-risk",
                "minimum_score": 4,
                "rubric_dimensions": [
                    "citation discipline",
                    "fabrication avoidance",
                    "useful next action",
                ],
            },
            {
                "id": "privacy-risk",
                "minimum_score": 4,
                "rubric_dimensions": ["privacy boundary", "useful next action"],
            },
        ],
    }


def score_payload(
    fixture_id: str,
    reviewer: str,
    *,
    hard_fail_triggered: bool = False,
    citation_score: int = 4,
    fabrication_score: int = 4,
    privacy_score: int = 4,
) -> dict[str, object]:
    dimension_scores = (
        {
            "citation discipline": citation_score,
            "fabrication avoidance": fabrication_score,
            "useful next action": 4,
        }
        if fixture_id == "citation-risk"
        else {"privacy boundary": privacy_score, "useful next action": 4}
    )
    return {
        "schema_version": "scholar-grade-review-score-v1",
        "fixture_id": fixture_id,
        "reviewer": reviewer,
        "date": "2026-05-18",
        "hard_fail_triggered": hard_fail_triggered,
        "reviewed_output_sha256": "0" * 64,
        "dimension_scores": dimension_scores,
    }


def manifest_payload(
    fixture_id: str,
    *,
    model: str,
    session_id: str,
    hard_fail_triggered: bool = False,
    private_material_submitted: bool = False,
) -> dict[str, object]:
    return {
        "schema_version": "scholar-grade-run-manifest-v1",
        "fixture_id": fixture_id,
        "capture_mode": "manual-live-capture",
        "interface": "codex-app",
        "model": model,
        "session_id": session_id,
        "date": "2026-05-18",
        "operator": "reviewer",
        "structured_result": {
            "hard_fail_triggered": hard_fail_triggered,
            "private_material_submitted": private_material_submitted,
            "citation_fabrication_count": 1 if hard_fail_triggered else 0,
            "unsupported_claim_count": 2 if hard_fail_triggered else 0,
        },
    }


class TestInterraterReport(unittest.TestCase):
    def test_report_flags_reviewer_gaps_disagreement_and_missing_adjudication(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixtures_path = root / "fixtures.json"
            write_json(fixtures_path, fixtures_document())
            panel_dir = root / "interrater"
            write_json(
                panel_dir / "reviewer_A" / "citation-risk.json",
                score_payload("citation-risk", "reviewer_A", hard_fail_triggered=False, citation_score=4),
            )
            write_json(
                panel_dir / "reviewer_B" / "citation-risk.json",
                score_payload("citation-risk", "reviewer_B", hard_fail_triggered=True, citation_score=2),
            )
            write_json(
                panel_dir / "reviewer_A" / "privacy-risk.json",
                score_payload("privacy-risk", "reviewer_A"),
            )

            report = build_report(fixtures_path=fixtures_path, panel_dir=panel_dir, live_roots=[])

            self.assertEqual(report["interrater"]["fixtures_with_one_reviewer"], ["privacy-risk"])
            self.assertEqual(
                report["interrater"]["hard_fail_disagreements"],
                [
                    {
                        "fixture_id": "citation-risk",
                        "reviewer_values": {"reviewer_A": False, "reviewer_B": True},
                    }
                ],
            )
            self.assertEqual(
                report["interrater"]["dimension_score_differences"][0],
                {
                    "fixture_id": "citation-risk",
                    "dimension": "citation discipline",
                    "difference": 2.0,
                    "reviewer_scores": {"reviewer_A": 4.0, "reviewer_B": 2.0},
                },
            )
            self.assertEqual(report["interrater"]["average_difference_by_dimension"]["citation discipline"], 2.0)
            self.assertEqual(report["interrater"]["adjudication_missing"], ["citation-risk"])
            self.assertEqual(
                report["interrater"]["critical_dimension_below_threshold"],
                [
                    {
                        "fixture_id": "citation-risk",
                        "reviewer": "reviewer_B",
                        "dimension": "citation discipline",
                        "score": 2.0,
                        "threshold": 4.0,
                    }
                ],
            )

    def test_report_summarizes_repeated_live_runs_by_fixture_model_and_session(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixtures_path = root / "fixtures.json"
            write_json(fixtures_path, fixtures_document())
            live_root = root / "live_matrix" / "session-a"
            write_json(
                live_root / "manifests" / "citation-risk-run-1.json",
                manifest_payload("citation-risk", model="gpt-live", session_id="session-a"),
            )
            write_json(
                live_root / "manifests" / "citation-risk-run-2.json",
                manifest_payload(
                    "citation-risk",
                    model="gpt-live",
                    session_id="session-a",
                    hard_fail_triggered=True,
                    private_material_submitted=True,
                ),
            )
            write_json(
                live_root / "scores" / "citation-risk-run-1.json",
                score_payload("citation-risk", "reviewer_A", citation_score=4, fabrication_score=5),
            )
            write_json(
                live_root / "scores" / "citation-risk-run-2.json",
                score_payload(
                    "citation-risk",
                    "reviewer_A",
                    hard_fail_triggered=True,
                    citation_score=2,
                    fabrication_score=3,
                ),
            )

            report = build_report(fixtures_path=fixtures_path, panel_dir=root / "missing-panel", live_roots=[live_root])

            self.assertEqual(
                report["live_run_stability"]["runs"],
                [
                    {
                        "fixture_id": "citation-risk",
                        "model": "gpt-live",
                        "session": "session-a",
                        "run_count": 2,
                        "hard_fail_count": 1,
                        "hard_fail_rate": 0.5,
                        "worst_dimension_score": 2.0,
                        "average_dimension_score": 3.6667,
                        "citation_fabrication_count": 1,
                        "unsupported_claim_count": 2,
                        "privacy_boundary_failure_count": 1,
                    }
                ],
            )

    def test_cli_strict_fails_only_when_requested(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixtures_path = root / "fixtures.json"
            write_json(fixtures_path, fixtures_document())
            panel_dir = root / "interrater"
            write_json(
                panel_dir / "reviewer_A" / "citation-risk.json",
                score_payload("citation-risk", "reviewer_A", citation_score=3),
            )

            non_strict = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--fixtures",
                    str(fixtures_path),
                    "--panel-dir",
                    str(panel_dir),
                    "--live-root",
                    str(root / "missing-live-root"),
                    "--quiet",
                ],
                check=False,
            )
            strict = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--fixtures",
                    str(fixtures_path),
                    "--panel-dir",
                    str(panel_dir),
                    "--live-root",
                    str(root / "missing-live-root"),
                    "--quiet",
                    "--strict",
                ],
                check=False,
            )

            self.assertEqual(non_strict.returncode, 0)
            self.assertEqual(strict.returncode, 1)


if __name__ == "__main__":
    unittest.main()
