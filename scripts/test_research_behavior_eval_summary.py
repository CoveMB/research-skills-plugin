"""Tests for local research behavior evaluation summary reports."""
from __future__ import annotations

import json
import hashlib
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parent))
from research_behavior_reports import output_summary, trace_summary
from summarize_research_behavior_evals import build_calibration_report


SCRIPT = Path(__file__).resolve().parent / "summarize_research_behavior_evals.py"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def fixture_document() -> dict[str, object]:
    return {
        "schema_version": "research-skill-behavior-fixtures-v1",
        "fixtures": [
            {
                "id": "route-one",
                "prompt": "Check route one.",
                "expected_route": "citation-integrity-auditor",
                "risk_covered": "metadata lookup consent",
                "required_output_markers": ["Source basis"],
                "forbidden_claims": ["invented verification"],
            },
            {
                "id": "route-two",
                "prompt": "Use compact output.",
                "expected_route": "reading-load-reducer",
                "risk_covered": "compact routing",
                "required_output_markers": ["How to use this result", "Next action"],
                "forbidden_claims": ["multiple next actions"],
            },
        ],
    }


class TestResearchBehaviorEvalSummary(unittest.TestCase):
    def test_shared_output_summary_reports_present_missing_and_errors(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            fixtures = fixture_document()["fixtures"]
            (outputs_dir / "route-one.md").write_text(
                "Selected skill: citation-integrity-auditor\n## Source basis\n",
                encoding="utf-8",
            )

            summary = output_summary(outputs_dir, fixtures)

            self.assertTrue(summary["checked"])
            self.assertEqual(summary["present"], ["route-one"])
            self.assertEqual(summary["missing"], ["route-two"])
            self.assertEqual(summary["validation_errors"], ["route-two: missing output file route-two.md"])

    def test_shared_trace_summary_reports_present_missing_and_errors(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            traces_dir = root / "traces"
            traces_dir.mkdir()
            fixtures = fixture_document()["fixtures"]
            (traces_dir / "route-one.json").write_text(
                json.dumps(
                    {
                        "schema_version": "research-behavior-route-trace-v2",
                        "fixture_id": "route-one",
                        "selected_skill": "citation-integrity-auditor",
                        "prompt_sha256": sha256_text("Check route one."),
                        "output_sha256": sha256_text(""),
                        "skill_invoked": True,
                        "prompt_supplied": True,
                        "output_captured": True,
                    }
                ),
                encoding="utf-8",
            )

            summary = trace_summary(traces_dir, fixtures)

            self.assertTrue(summary["checked"])
            self.assertEqual(summary["present"], ["route-one"])
            self.assertEqual(summary["missing"], ["route-two"])
            self.assertEqual(summary["validation_errors"], ["route-two: missing trace file route-two.json"])

    def test_report_counts_routes_risks_and_captured_outputs(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = root / "fixtures.json"
            outputs_dir = root / "outputs"
            traces_dir = root / "traces"
            outputs_dir.mkdir()
            traces_dir.mkdir()
            fixture_path.write_text(json.dumps(fixture_document()), encoding="utf-8")
            route_one_output = "Selected skill: citation-integrity-auditor\n## Source basis\n"
            (outputs_dir / "route-one.md").write_text(route_one_output, encoding="utf-8")
            (traces_dir / "route-one.json").write_text(
                json.dumps(
                    {
                        "schema_version": "research-behavior-route-trace-v2",
                        "fixture_id": "route-one",
                        "selected_skill": "citation-integrity-auditor",
                        "prompt_sha256": sha256_text("Check route one."),
                        "output_sha256": sha256_text(route_one_output),
                        "skill_invoked": True,
                        "prompt_supplied": True,
                        "output_captured": True,
                    }
                ),
                encoding="utf-8",
            )

            report = build_calibration_report(fixture_path, outputs_dir, traces_dir)

            self.assertEqual(report["schema_version"], "research-skill-behavior-calibration-v1")
            self.assertEqual(report["fixtures"]["total"], 2)
            self.assertEqual(report["fixtures"]["compact_total"], 1)
            self.assertEqual(
                report["fixtures"]["expected_route_counts"],
                {"citation-integrity-auditor": 1, "reading-load-reducer": 1},
            )
            self.assertEqual(
                report["fixtures"]["covered_risks"],
                ["compact routing", "metadata lookup consent"],
            )
            self.assertEqual(report["outputs"]["present"], ["route-one"])
            self.assertEqual(report["outputs"]["missing"], ["route-two"])
            self.assertEqual(report["outputs"]["validation_errors"], ["route-two: missing output file route-two.md"])
            self.assertEqual(report["traces"]["present"], ["route-one"])
            self.assertEqual(report["traces"]["missing"], ["route-two"])
            self.assertEqual(report["traces"]["validation_errors"], ["route-two: missing trace file route-two.json"])

    def test_cli_prints_json_report(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = root / "fixtures.json"
            fixture_path.write_text(json.dumps(fixture_document()), encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--fixtures", str(fixture_path)],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["fixtures"]["total"], 2)
            self.assertFalse(payload["outputs"]["checked"])
            self.assertFalse(payload["traces"]["checked"])

    def test_cli_fails_on_trace_validation_errors(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = root / "fixtures.json"
            traces_dir = root / "traces"
            traces_dir.mkdir()
            fixture_path.write_text(json.dumps(fixture_document()), encoding="utf-8")
            (traces_dir / "route-one.json").write_text(
                json.dumps(
                    {
                        "schema_version": "research-behavior-route-trace-v2",
                        "fixture_id": "route-one",
                        "selected_skill": "wrong-skill",
                        "prompt_sha256": sha256_text("Check route one."),
                        "output_sha256": sha256_text(""),
                        "skill_invoked": True,
                        "prompt_supplied": True,
                        "output_captured": True,
                    }
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--fixtures",
                    str(fixture_path),
                    "--traces-dir",
                    str(traces_dir),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 1)
            payload = json.loads(result.stdout)
            self.assertIn(
                "route-one: trace selected_skill must match expected_route 'citation-integrity-auditor'",
                payload["traces"]["validation_errors"],
            )


if __name__ == "__main__":
    unittest.main()
