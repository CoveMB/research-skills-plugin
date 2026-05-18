"""Tests for the deterministic research behavior evaluation harness."""
from __future__ import annotations

import json
import hashlib
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parent))
from research_behavior_eval_harness import build_harness_report, format_markdown_runbook


SCRIPT = Path(__file__).resolve().parent / "research_behavior_eval_harness.py"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def fixture_document() -> dict[str, object]:
    return {
        "schema_version": "research-skill-behavior-fixtures-v1",
        "purpose": "Fixture document for harness tests.",
        "fixtures": [
            {
                "id": "route-one",
                "prompt": "Check this bibliography for possible fake DOIs.",
                "expected_route": "citation-integrity-auditor",
                "risk_covered": "hallucinated citation metadata",
                "required_output_markers": ["metadata verification ladder", "DOI"],
                "forbidden_claims": ["metadata verified from memory"],
            },
            {
                "id": "route-two",
                "prompt": "Use compact output for a routing triage.",
                "expected_route": "research-intent-router",
                "risk_covered": "compact routing",
                "required_output_markers": ["How to use this result", "Next action"],
                "forbidden_claims": ["multiple next actions"],
            },
        ],
    }


class TestResearchBehaviorEvalHarness(unittest.TestCase):
    def test_report_documents_manual_capture_output_and_trace_validation(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = root / "fixtures.json"
            outputs_dir = root / "outputs"
            traces_dir = root / "traces"
            outputs_dir.mkdir()
            traces_dir.mkdir()
            fixture_path.write_text(json.dumps(fixture_document()), encoding="utf-8")
            route_one_output = "Selected skill: citation-integrity-auditor\nmetadata verification ladder\nDOI\n"
            (outputs_dir / "route-one.md").write_text(
                route_one_output,
                encoding="utf-8",
            )
            (traces_dir / "route-one.json").write_text(
                json.dumps(
                    {
                        "schema_version": "research-behavior-route-trace-v2",
                        "fixture_id": "route-one",
                        "selected_skill": "citation-integrity-auditor",
                        "prompt_sha256": sha256_text("Check this bibliography for possible fake DOIs."),
                        "output_sha256": sha256_text(route_one_output),
                        "skill_invoked": True,
                        "prompt_supplied": True,
                        "output_captured": True,
                    }
                ),
                encoding="utf-8",
            )

            report = build_harness_report(fixture_path, outputs_dir, traces_dir)

            self.assertEqual(report["schema_version"], "research-skill-behavior-harness-v1")
            self.assertEqual(report["execution_mode"], "deterministic-local")
            self.assertIn("does not run a model", " ".join(report["limits"]))
            self.assertIn(
                "Capture exactly one Markdown output and one hash-linked route trace JSON per fixture id.",
                report["manual_or_live_run_expectations"],
            )
            self.assertEqual(report["fixtures"]["total"], 2)
            self.assertEqual(report["outputs"]["missing"], ["route-two"])
            self.assertEqual(report["traces"]["missing"], ["route-two"])
            self.assertEqual(report["cases"][0]["id"], "route-one")
            self.assertEqual(report["cases"][0]["expected_route"], "citation-integrity-auditor")
            self.assertTrue(report["cases"][0]["captured_output_checked"])
            self.assertTrue(report["cases"][0]["route_trace_checked"])
            self.assertEqual(report["cases"][0]["validation_errors"], [])
            self.assertEqual(report["cases"][0]["trace_validation_errors"], [])
            self.assertEqual(report["cases"][1]["output_file"], "route-two.md")
            self.assertEqual(report["cases"][1]["validation_errors"], ["route-two: missing output file route-two.md"])
            self.assertEqual(report["cases"][1]["trace_file"], "route-two.json")
            self.assertEqual(report["cases"][1]["trace_validation_errors"], ["route-two: missing trace file route-two.json"])

    def test_markdown_runbook_includes_fixture_prompts_and_boundaries(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = root / "fixtures.json"
            fixture_path.write_text(json.dumps(fixture_document()), encoding="utf-8")

            markdown = format_markdown_runbook(build_harness_report(fixture_path))

            self.assertIn("# Research Behavior Evaluation Harness", markdown)
            self.assertIn("This harness does not run a model", markdown)
            self.assertIn("## Manual/live capture expectations", markdown)
            self.assertIn("### route-one", markdown)
            self.assertIn("Expected route: `citation-integrity-auditor`", markdown)
            self.assertIn("> Check this bibliography for possible fake DOIs.", markdown)
            self.assertIn("Required markers: `metadata verification ladder`, `DOI`", markdown)
            self.assertIn("Forbidden claims: `metadata verified from memory`", markdown)

    def test_markdown_runbook_handles_markers_with_backticks(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = root / "fixtures.json"
            document = fixture_document()
            document["fixtures"][0]["required_output_markers"].append(
                "Do not suggest `citation-integrity-auditor` before citations."
            )
            fixture_path.write_text(json.dumps(document), encoding="utf-8")

            markdown = format_markdown_runbook(build_harness_report(fixture_path))

            self.assertIn("``Do not suggest `citation-integrity-auditor` before citations.``", markdown)

    def test_cli_can_print_markdown_runbook(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = root / "fixtures.json"
            fixture_path.write_text(json.dumps(fixture_document()), encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--fixtures",
                    str(fixture_path),
                    "--format",
                    "markdown",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0)
            self.assertIn("# Research Behavior Evaluation Harness", result.stdout)
            self.assertIn("route-one", result.stdout)

    def test_cli_quiet_validates_without_printing_report(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = root / "fixtures.json"
            outputs_dir = root / "outputs"
            traces_dir = root / "traces"
            outputs_dir.mkdir()
            traces_dir.mkdir()
            fixture_path.write_text(json.dumps(fixture_document()), encoding="utf-8")
            route_one_output = "Selected skill: citation-integrity-auditor\nmetadata verification ladder\nDOI\n"
            route_two_output = "Selected skill: research-intent-router\nHow to use this result\nNext action\n"
            (outputs_dir / "route-one.md").write_text(
                route_one_output,
                encoding="utf-8",
            )
            (outputs_dir / "route-two.md").write_text(
                route_two_output,
                encoding="utf-8",
            )
            for fixture_id, selected_skill, prompt, output_text in [
                (
                    "route-one",
                    "citation-integrity-auditor",
                    "Check this bibliography for possible fake DOIs.",
                    route_one_output,
                ),
                (
                    "route-two",
                    "research-intent-router",
                    "Use compact output for a routing triage.",
                    route_two_output,
                ),
            ]:
                (traces_dir / f"{fixture_id}.json").write_text(
                    json.dumps(
                        {
                            "schema_version": "research-behavior-route-trace-v2",
                            "fixture_id": fixture_id,
                            "selected_skill": selected_skill,
                            "prompt_sha256": sha256_text(prompt),
                            "output_sha256": sha256_text(output_text),
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
                    "--outputs-dir",
                    str(outputs_dir),
                    "--traces-dir",
                    str(traces_dir),
                    "--quiet",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
