"""Tests for recording scholar-grade live/manual captures."""
from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_live_capture import (
    CaptureMetadata,
    build_record_plan,
    record_live_capture,
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


def write_fixture_environment(root: Path) -> Path:
    fixture_path = root / "fixtures.json"
    fixture_path.write_text(
        json.dumps(
            {
                "schema_version": "scholar-grade-eval-fixtures-v1",
                "purpose": "test fixtures",
                "fixtures": [fixture()],
            }
        ),
        encoding="utf-8",
    )
    corpus_dir = root / "corpora" / "unsupported-causal-claim"
    corpus_dir.mkdir(parents=True)
    (corpus_dir / "source-packet.md").write_text(
        "# Synthetic source packet\n\nVisible method details: none.\n",
        encoding="utf-8",
    )
    (corpus_dir / "answer-key.md").write_text(
        "# Hidden answer key\n\n## Ground truth for evaluation\n\n- Causal support is unavailable.\n",
        encoding="utf-8",
    )
    skill_dir = root / "skills" / "methodology-source-auditor"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("skill text", encoding="utf-8")
    return fixture_path


def write_captured_output(root: Path) -> Path:
    output_path = root / "captured-output.md"
    output_path.write_text(
        "\n".join(
            [
                "Source basis: controlled-packet source notes only.",
                "Claim/evidence fit: Cannot support the causal claim.",
                "Required uncertainty: No method details are available.",
                "Next action: request method details before using the claim.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return output_path


def metadata(capture_mode: str = "manual-live-capture") -> CaptureMetadata:
    return CaptureMetadata(
        capture_mode=capture_mode,
        interface="codex-cli",
        model="gpt-test-scholar",
        date="2026-05-14",
        operator="test operator",
        decision="Cannot support",
        tool_permissions="none",
        network_permissions="none",
        external_lookup_permitted=False,
        external_lookup_used=False,
        private_material_submitted=False,
        hard_fail_triggered=False,
        next_action_count=1,
    )


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class TestRunLiveCapture(unittest.TestCase):
    def test_build_record_plan_reports_selected_artifacts_without_writing(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_environment(root)

            plan = build_record_plan(
                fixture_path=fixture_path,
                root=root,
                output_root=root / "captures",
                fixture_ids=["unsupported-causal-claim"],
            )

            self.assertEqual(plan["schema_version"], "scholar-grade-live-capture-record-plan-v1")
            self.assertEqual(plan["capture_count"], 1)
            artifact_paths = plan["captures"][0]["artifact_paths"]
            self.assertEqual(
                artifact_paths["prompt_packet"],
                str(root / "captures" / "prompts" / "unsupported-causal-claim.md"),
            )
            self.assertFalse((root / "captures").exists())

    def test_record_manual_capture_writes_artifacts_with_hashes(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_environment(root)
            captured_output = write_captured_output(root)
            output_root = root / "captures"

            result = record_live_capture(
                fixture_path=fixture_path,
                root=root,
                output_root=output_root,
                fixture_id="unsupported-causal-claim",
                captured_output=captured_output,
                metadata=metadata(),
                overwrite=False,
            )

            self.assertEqual(result["errors"], [])
            output_path = output_root / "outputs" / "unsupported-causal-claim.md"
            manifest_path = output_root / "manifests" / "unsupported-causal-claim.json"
            prompt_path = output_root / "prompts" / "unsupported-causal-claim.md"
            score_template_path = output_root / "score-templates" / "unsupported-causal-claim.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            score_template = json.loads(score_template_path.read_text(encoding="utf-8"))
            prompt_packet = prompt_path.read_text(encoding="utf-8")

            self.assertEqual(output_path.read_text(encoding="utf-8"), captured_output.read_text(encoding="utf-8"))
            self.assertEqual(manifest["capture_mode"], "manual-live-capture")
            self.assertEqual(manifest["model"], "gpt-test-scholar")
            self.assertEqual(manifest["output_sha256"], sha256_file(output_path))
            self.assertEqual(score_template["reviewed_output_sha256"], sha256_file(output_path))
            self.assertEqual(manifest["source_packet"], "corpora/unsupported-causal-claim/source-packet.md")
            self.assertEqual(manifest["structured_result"]["decision"], "Cannot support")
            self.assertEqual(manifest["structured_result"]["selected_skill"], "methodology-source-auditor")
            self.assertIs(manifest["structured_result"]["skill_invoked"], True)
            self.assertIs(manifest["structured_result"]["source_packet_supplied"], True)
            self.assertIs(manifest["structured_result"]["output_captured"], True)
            self.assertNotIn("trace_file", manifest)
            self.assertIn("Can these notes support my causal claim?", prompt_packet)
            self.assertIn("Visible method details: none.", prompt_packet)
            self.assertNotIn("answer-key.md", prompt_packet)
            self.assertTrue(score_template_path.exists())

    def test_record_capture_refuses_to_overwrite_existing_artifacts(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_environment(root)
            captured_output = write_captured_output(root)
            output_root = root / "captures"

            first_result = record_live_capture(
                fixture_path=fixture_path,
                root=root,
                output_root=output_root,
                fixture_id="unsupported-causal-claim",
                captured_output=captured_output,
                metadata=metadata(),
                overwrite=False,
            )
            second_result = record_live_capture(
                fixture_path=fixture_path,
                root=root,
                output_root=output_root,
                fixture_id="unsupported-causal-claim",
                captured_output=captured_output,
                metadata=metadata(),
                overwrite=False,
            )

            self.assertEqual(first_result["errors"], [])
            self.assertIn("refusing to overwrite existing artifact", "\n".join(second_result["errors"]))

    def test_record_automated_capture_requires_trace_source(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_environment(root)
            captured_output = write_captured_output(root)

            result = record_live_capture(
                fixture_path=fixture_path,
                root=root,
                output_root=root / "captures",
                fixture_id="unsupported-causal-claim",
                captured_output=captured_output,
                metadata=metadata("automated-live-capture"),
                overwrite=False,
            )

            self.assertIn("automated-live-capture requires --trace-source", result["errors"])

    def test_record_capture_rejects_non_calendar_date(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_environment(root)
            captured_output = write_captured_output(root)
            invalid_metadata = metadata()
            invalid_metadata = CaptureMetadata(
                capture_mode=invalid_metadata.capture_mode,
                interface=invalid_metadata.interface,
                model=invalid_metadata.model,
                date="2026-99-99",
                operator=invalid_metadata.operator,
                decision=invalid_metadata.decision,
                tool_permissions=invalid_metadata.tool_permissions,
                network_permissions=invalid_metadata.network_permissions,
                external_lookup_permitted=invalid_metadata.external_lookup_permitted,
                external_lookup_used=invalid_metadata.external_lookup_used,
                private_material_submitted=invalid_metadata.private_material_submitted,
                hard_fail_triggered=invalid_metadata.hard_fail_triggered,
                next_action_count=invalid_metadata.next_action_count,
            )

            result = record_live_capture(
                fixture_path=fixture_path,
                root=root,
                output_root=root / "captures",
                fixture_id="unsupported-causal-claim",
                captured_output=captured_output,
                metadata=invalid_metadata,
                overwrite=False,
            )

            self.assertIn("date must be a real YYYY-MM-DD date", result["errors"])

    def test_record_automated_capture_copies_trace_and_manifest_hash(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_environment(root)
            captured_output = write_captured_output(root)
            trace_source = root / "trace-source.json"
            trace_source.write_text(
                json.dumps(
                    {
                        "schema_version": "scholar-grade-trace-v1",
                        "fixture_id": "unsupported-causal-claim",
                        "skill": "methodology-source-auditor",
                        "model": "gpt-test-scholar",
                        "skill_invoked": True,
                        "source_packet_supplied": True,
                        "output_captured": True,
                    }
                ),
                encoding="utf-8",
            )

            result = record_live_capture(
                fixture_path=fixture_path,
                root=root,
                output_root=root / "captures",
                fixture_id="unsupported-causal-claim",
                captured_output=captured_output,
                metadata=metadata("automated-live-capture"),
                overwrite=False,
                trace_source=trace_source,
            )

            trace_path = root / "captures" / "traces" / "unsupported-causal-claim.json"
            manifest = json.loads(
                (root / "captures" / "manifests" / "unsupported-causal-claim.json").read_text(encoding="utf-8")
            )
            self.assertEqual(result["errors"], [])
            self.assertEqual(trace_path.read_text(encoding="utf-8"), trace_source.read_text(encoding="utf-8"))
            self.assertEqual(manifest["trace_file"], "captures/traces/unsupported-causal-claim.json")
            self.assertEqual(manifest["trace_sha256"], sha256_file(trace_path))


if __name__ == "__main__":
    unittest.main()
