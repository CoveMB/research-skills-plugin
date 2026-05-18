"""Tests for scholar-grade live/manual capture protocol generation."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parent))
from live_capture_protocol import (
    build_capture_plan,
    build_manifest_template,
    build_score_template,
    render_prompt_packet,
    select_fixtures,
    validate_capture_plan,
    write_capture_protocol,
)


def fixture() -> dict[str, object]:
    return {
        "id": "unsupported-causal-claim",
        "skill": "methodology-source-auditor",
        "prompt": "Can these notes support my causal claim?",
        "source_packet": "corpora/unsupported-causal-claim",
        "source_access_level": "controlled-packet",
        "resource_basis": ["ai-research-failure-modes"],
        "expected_decision": "Cannot support",
        "required_output_markers": ["Source basis", "Claim/evidence fit", "Next action"],
        "required_uncertainties": ["No method details are available"],
        "allowed_claims": ["The visible notes can support a limited descriptive claim."],
        "disallowed_claims": ["The notes prove the causal claim."],
        "hard_fail_patterns": ["(?i)causal claim (is )?verified"],
        "rubric_dimensions": ["source-basis clarity", "claim/evidence fit"],
        "minimum_score": 4,
        "human_review_required": True,
    }


def reading_fixture() -> dict[str, object]:
    return {
        **fixture(),
        "id": "reading-load-abstract-only",
        "skill": "reading-load-reducer",
        "prompt": "Tell me what to skim first.",
        "source_packet": "corpora/reading-load-abstract-only",
    }


def write_fixture_environment(root: Path) -> Path:
    fixture_path = root / "fixtures.json"
    fixture_path.write_text(
        json.dumps(
            {
                "schema_version": "scholar-grade-eval-fixtures-v1",
                "purpose": "test fixtures",
                "fixtures": [fixture(), reading_fixture()],
            }
        ),
        encoding="utf-8",
    )
    for test_fixture in [fixture(), reading_fixture()]:
        corpus_dir = root / str(test_fixture["source_packet"])
        corpus_dir.mkdir(parents=True)
        (corpus_dir / "source-packet.md").write_text(
            "\n".join(
                [
                    "# Synthetic source packet",
                    "",
                    "Visible method details: none.",
                ]
            ),
            encoding="utf-8",
        )
        (corpus_dir / "answer-key.md").write_text(
            "\n".join(
                [
                    "# Hidden answer key",
                    "",
                    "## Ground truth for evaluation",
                    "",
                    "- Causal support is unavailable.",
                ]
            ),
            encoding="utf-8",
        )
        skill_dir = root / "skills" / str(test_fixture["skill"])
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text("skill text", encoding="utf-8")
    return fixture_path


class TestLiveCaptureProtocol(unittest.TestCase):
    def test_prompt_packet_excludes_hidden_answer_key_and_expected_decision(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_environment(root)
            plan = build_capture_plan(fixture_path, root)

            prompt_packet = render_prompt_packet(plan["captures"][0])

            self.assertIn("Can these notes support my causal claim?", prompt_packet)
            self.assertIn("Visible method details: none.", prompt_packet)
            self.assertIn("source-packet.md", prompt_packet)
            self.assertNotIn("answer-key.md", prompt_packet)
            self.assertNotIn("Ground truth for evaluation", prompt_packet)
            self.assertNotIn("Cannot support", prompt_packet)

    def test_capture_plan_can_target_live_pilot_fixture_subset(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_environment(root)

            plan = build_capture_plan(fixture_path, root, ["reading-load-abstract-only"])

            self.assertEqual(plan["capture_count"], 1)
            self.assertEqual(plan["captures"][0]["fixture_id"], "reading-load-abstract-only")
            self.assertEqual(plan["fixture_ids"], ["reading-load-abstract-only"])

    def test_select_fixtures_reports_unknown_live_pilot_id(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_environment(root)
            document = json.loads(fixture_path.read_text(encoding="utf-8"))

            selected, errors = select_fixtures(document, ["missing-fixture"])

            self.assertEqual(selected, [])
            self.assertEqual(errors, ["unknown fixture id: missing-fixture"])

    def test_validate_capture_plan_rejects_fixture_specific_hidden_value_leakage(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_environment(root)
            document = json.loads(fixture_path.read_text(encoding="utf-8"))
            document["fixtures"][0]["prompt"] = "Tell the model the hidden decision is Cannot support."
            fixture_path.write_text(json.dumps(document), encoding="utf-8")

            errors = validate_capture_plan(fixture_path, root)

            self.assertIn(
                "unsupported-causal-claim: prompt packet leaks expected_decision value 'Cannot support'",
                errors,
            )

    def test_validate_capture_plan_allows_hidden_value_already_visible_in_source_packet(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_environment(root)
            source_packet_path = root / "corpora" / "unsupported-causal-claim" / "source-packet.md"
            source_packet_path.write_text(
                "\n".join(
                    [
                        "# Synthetic source packet",
                        "",
                        "No method details are available.",
                    ]
                ),
                encoding="utf-8",
            )

            self.assertEqual(validate_capture_plan(fixture_path, root), [])

    def test_validate_capture_plan_allows_disallowed_claim_already_visible_in_user_prompt(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_environment(root)
            document = json.loads(fixture_path.read_text(encoding="utf-8"))
            document["fixtures"][0]["prompt"] = "Can I write this sentence: The notes prove the causal claim.?"
            fixture_path.write_text(json.dumps(document), encoding="utf-8")

            self.assertEqual(validate_capture_plan(fixture_path, root), [])

    def test_manifest_template_records_live_capture_placeholders_and_hashes(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_environment(root)
            capture = build_capture_plan(fixture_path, root)["captures"][0]

            manifest = build_manifest_template(capture)

            self.assertEqual(manifest["schema_version"], "scholar-grade-run-manifest-v1")
            self.assertEqual(manifest["capture_mode"], "manual-live-capture")
            self.assertEqual(manifest["model"], "TODO_MODEL")
            self.assertEqual(manifest["output_sha256"], "TODO_AFTER_CAPTURE")
            self.assertEqual(manifest["structured_result"]["selected_skill"], "TODO_SELECTED_SKILL")
            self.assertEqual(manifest["structured_result"]["skill_invoked"], "TODO_BOOLEAN")
            self.assertEqual(manifest["structured_result"]["source_packet_supplied"], "TODO_BOOLEAN")
            self.assertEqual(manifest["structured_result"]["output_captured"], "TODO_BOOLEAN")
            self.assertRegex(str(manifest["source_packet_sha256"]), r"^[0-9a-f]{64}$")
            self.assertRegex(str(manifest["skill_file_sha256"]), r"^[0-9a-f]{64}$")
            self.assertEqual(manifest["trace_file"], "traces/unsupported-causal-claim.json")
            self.assertEqual(manifest["trace_sha256"], "TODO_FOR_AUTOMATED_CAPTURE")

    def test_score_template_matches_fixture_rubric_without_prefilled_scores(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_environment(root)
            capture = build_capture_plan(fixture_path, root)["captures"][0]

            score = build_score_template(capture)

            self.assertEqual(score["schema_version"], "scholar-grade-review-score-v1")
            self.assertEqual(score["hard_fail_triggered"], "TODO_BOOLEAN")
            self.assertEqual(score["reviewed_output_sha256"], "TODO_AFTER_CAPTURE")
            self.assertEqual(
                score["dimension_rationales"],
                {
                    "source-basis clarity": "TODO_RATIONALE",
                    "claim/evidence fit": "TODO_RATIONALE",
                },
            )
            self.assertEqual(
                score["dimension_scores"],
                {
                    "source-basis clarity": "TODO_0_TO_5",
                    "claim/evidence fit": "TODO_0_TO_5",
                },
            )

    def test_write_capture_protocol_creates_automated_trace_template(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_environment(root)
            output_dir = root / "live-capture"

            write_capture_protocol(fixture_path, output_dir, root, ["unsupported-causal-claim"])

            trace_template_path = output_dir / "trace-templates" / "unsupported-causal-claim.json"
            trace_template = json.loads(trace_template_path.read_text(encoding="utf-8"))
            readme = (output_dir / "README.md").read_text(encoding="utf-8")

            self.assertEqual(trace_template["schema_version"], "scholar-grade-trace-v1")
            self.assertEqual(trace_template["fixture_id"], "unsupported-causal-claim")
            self.assertEqual(trace_template["skill"], "methodology-source-auditor")
            self.assertEqual(trace_template["model"], "TODO_MODEL")
            self.assertEqual(trace_template["skill_invoked"], "TODO_BOOLEAN")
            self.assertEqual(trace_template["source_packet_supplied"], "TODO_BOOLEAN")
            self.assertEqual(trace_template["output_captured"], "TODO_BOOLEAN")
            self.assertIn("trace-templates", readme)
            self.assertIn("trace_sha256", readme)
            self.assertFalse((output_dir / "trace-templates" / "reading-load-abstract-only.json").exists())

    def test_write_capture_protocol_creates_prompt_manifest_and_score_templates(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_environment(root)
            output_dir = root / "live-capture"

            write_capture_protocol(fixture_path, output_dir, root)

            self.assertTrue((output_dir / "capture-plan.json").exists())
            self.assertTrue((output_dir / "prompts" / "unsupported-causal-claim.md").exists())
            self.assertTrue((output_dir / "manifest-templates" / "unsupported-causal-claim.json").exists())
            self.assertTrue((output_dir / "score-templates" / "unsupported-causal-claim.json").exists())
            self.assertTrue((output_dir / "trace-templates" / "unsupported-causal-claim.json").exists())
            self.assertEqual(validate_capture_plan(fixture_path, root), [])


if __name__ == "__main__":
    unittest.main()
