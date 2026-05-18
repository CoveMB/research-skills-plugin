"""Tests for additive live-pilot calibration reports."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parent))
from live_pilot_calibration import build_calibration_report, score_regressions_for_fixture


SCRIPT = Path(__file__).resolve().parent / "live_pilot_calibration.py"
ROOT = Path(__file__).resolve().parents[3]

REQUIRED_V2_PILOT_FIXTURES = {
    "claim-traceability-nearby-citation",
    "discovery-dedupe-fuzzy-export",
    "chart-without-data-provenance",
    "literature-map-overstates-consensus",
    "annotation-source-note-mixed-evidence",
    "extraction-table-uneven-source-notes",
    "book-comps-stale-mismatch",
}


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def fixture_document() -> dict[str, object]:
    return {
        "schema_version": "scholar-grade-eval-fixtures-v1",
        "purpose": "Live pilot calibration test fixtures.",
        "fixtures": [
            {
                "id": "unsupported-causal-claim",
                "skill": "methodology-source-auditor",
                "prompt": "Can these notes support my causal claim?",
                "source_packet": "corpora/unsupported-causal-claim",
                "source_access_level": "controlled-packet",
                "resource_basis": ["ai-research-failure-modes"],
                "expected_decision": "Cannot support",
                "required_output_markers": ["Source basis", "Claim/evidence fit", "Next action"],
                "required_source_anchors": ["controlled notes only"],
                "required_uncertainties": ["No method details are available"],
                "allowed_claims": ["The visible notes can support a limited descriptive claim."],
                "disallowed_claims": ["The notes prove the causal claim."],
                "hard_fail_patterns": ["(?i)causal claim (is )?verified"],
                "semantic_fail_patterns": [
                    "(?i)notes.{0,80}(prove|verify|establish).{0,80}causal claim"
                ],
                "rubric_dimensions": ["source-basis clarity", "claim/evidence fit", "fabrication avoidance"],
                "score_anchors": {
                    "source-basis clarity": {
                        "3": "Names the controlled notes.",
                        "4": "Names the controlled notes and their visible limits.",
                        "5": "Separates visible source notes, hidden keys, and absent evidence.",
                    },
                    "claim/evidence fit": {
                        "3": "Rejects the broad causal claim.",
                        "4": "Rejects the causal claim while preserving the bounded descriptive claim.",
                        "5": "Separates descriptive, temporal, and causal support with source anchors.",
                    },
                    "fabrication avoidance": {
                        "3": "Avoids obvious invented verification.",
                        "4": "Avoids invented verification and provenance.",
                        "5": "Actively blocks invented verification, provenance, and locators.",
                    },
                },
                "minimum_score": 4,
                "human_review_required": True,
            }
        ],
    }


def write_fixture_environment(root: Path) -> Path:
    fixture_path = root / "fixtures.json"
    fixture_path.write_text(json.dumps(fixture_document()), encoding="utf-8")
    corpus_dir = root / "corpora" / "unsupported-causal-claim"
    corpus_dir.mkdir(parents=True)
    (corpus_dir / "source-packet.md").write_text(
        "Source basis: controlled notes only.\nNo method details are available.\n",
        encoding="utf-8",
    )
    (corpus_dir / "answer-key.md").write_text(
        "## Ground truth for evaluation\nCausal support is unavailable.\n",
        encoding="utf-8",
    )
    (corpus_dir / "answer-key.json").write_text(
        json.dumps(
            {
                "schema_version": "scholar-grade-answer-key-v1",
                "fixture_id": "unsupported-causal-claim",
                "must_support": ["The visible notes can support a limited descriptive claim."],
                "must_reject": ["The notes prove the causal claim."],
                "must_remain_uncertain": ["No method details are available"],
            }
        ),
        encoding="utf-8",
    )
    skill_dir = root / "skills" / "methodology-source-auditor"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("skill text", encoding="utf-8")
    return fixture_path


def write_pilot_plan(root: Path) -> Path:
    plan_path = root / "pilot.json"
    plan_path.write_text(
        json.dumps(
            {
                "schema_version": "scholar-grade-live-pilot-v1",
                "artifact_root": "live_pilot",
                "fixture_ids": ["unsupported-causal-claim"],
            }
        ),
        encoding="utf-8",
    )
    return plan_path


def score_payload(*, dimension_score: int = 4, hard_fail_triggered: bool = False) -> dict[str, object]:
    return {
        "schema_version": "scholar-grade-review-score-v1",
        "fixture_id": "unsupported-causal-claim",
        "reviewer": "reviewer",
        "date": "2026-05-17",
        "hard_fail_triggered": hard_fail_triggered,
        "reviewed_output_sha256": sha256_text(""),
        "dimension_scores": {
            "source-basis clarity": 4,
            "claim/evidence fit": dimension_score,
            "fabrication avoidance": 4,
        },
        "dimension_rationales": {
            "source-basis clarity": "The output names the controlled notes and visible limits.",
            "claim/evidence fit": "The output rejects the unsupported causal claim.",
            "fabrication avoidance": "The output does not invent verification or provenance.",
        },
        "evidence_notes": ["Reviewer checked the exact captured output against the controlled source packet."],
        "answer_key_findings": ["The output rejects must_reject claims and keeps must_remain_uncertain items visible."],
        "rationale": "Reviewer rationale.",
    }


def write_baseline_score(root: Path) -> Path:
    scores_dir = root / "baseline-scores"
    scores_dir.mkdir()
    (scores_dir / "unsupported-causal-claim.json").write_text(json.dumps(score_payload()), encoding="utf-8")
    return scores_dir


def write_live_artifacts(root: Path, fixture_path: Path, *, dimension_score: int = 4) -> Path:
    live_root = root / "live_pilot"
    prompts_dir = live_root / "prompts"
    outputs_dir = live_root / "outputs"
    manifests_dir = live_root / "manifests"
    scores_dir = live_root / "scores"
    prompts_dir.mkdir(parents=True)
    outputs_dir.mkdir()
    manifests_dir.mkdir()
    scores_dir.mkdir()

    output_text = "\n".join(
        [
            "Source basis: controlled notes only.",
            "Claim/evidence fit: Cannot support the causal claim.",
            "Required uncertainty: No method details are available.",
            "Allowed claim: The visible notes can support a limited descriptive claim.",
            "Next action: request method details.",
            "",
        ]
    )
    prompt_text = "prompt packet"
    (prompts_dir / "unsupported-causal-claim.md").write_text(prompt_text, encoding="utf-8")
    output_path = outputs_dir / "unsupported-causal-claim.md"
    output_path.write_text(output_text, encoding="utf-8")
    source_text = (fixture_path.parent / "corpora" / "unsupported-causal-claim" / "source-packet.md").read_text(
        encoding="utf-8"
    )
    manifest = {
        "schema_version": "scholar-grade-run-manifest-v1",
        "fixture_id": "unsupported-causal-claim",
        "skill": "methodology-source-auditor",
        "capture_mode": "manual-live-capture",
        "interface": "codex-app",
        "model": "gpt-live-test",
        "date": "2026-05-17",
        "operator": "reviewer",
        "source_packet": "corpora/unsupported-causal-claim/source-packet.md",
        "source_packet_sha256": sha256_text(source_text),
        "prompt_packet_sha256": sha256_text(prompt_text),
        "skill_file": "skills/methodology-source-auditor/SKILL.md",
        "skill_file_sha256": sha256_text("skill text"),
        "output_file": "unsupported-causal-claim.md",
        "output_sha256": sha256_text(output_text),
        "tool_permissions": "none",
        "network_permissions": "none",
        "external_lookup_permitted": False,
        "structured_result": {
            "decision": "Cannot support",
            "source_access_level": "controlled-packet",
            "external_lookup_used": False,
            "private_material_submitted": False,
            "hard_fail_triggered": False,
            "next_action_count": 1,
        },
    }
    (manifests_dir / "unsupported-causal-claim.json").write_text(json.dumps(manifest), encoding="utf-8")
    live_score = score_payload(dimension_score=dimension_score)
    live_score["reviewed_output_sha256"] = sha256_text(output_text)
    (scores_dir / "unsupported-causal-claim.json").write_text(json.dumps(live_score), encoding="utf-8")
    return live_root


class TestLivePilotCalibration(unittest.TestCase):
    def test_shipped_v2_pilot_covers_high_risk_skill_families(self) -> None:
        pilot_plan_path = ROOT / "tests" / "skill_evals" / "scholar_grade" / "live_pilot_v2" / "fixture-ids.json"
        pilot_plan = json.loads(pilot_plan_path.read_text(encoding="utf-8"))
        fixture_ids = set(pilot_plan["fixture_ids"])

        self.assertEqual(sorted(REQUIRED_V2_PILOT_FIXTURES - fixture_ids), [])

    def test_report_lists_missing_live_artifacts_as_record_actions(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_environment(root)
            pilot_plan = write_pilot_plan(root)
            baseline_scores = write_baseline_score(root)

            report = build_calibration_report(
                fixture_path=fixture_path,
                pilot_plan_path=pilot_plan,
                live_root=root / "live_pilot",
                baseline_scores_dir=baseline_scores,
                root=root,
            )

            self.assertFalse(report["ready"])
            self.assertEqual(report["pilot"]["fixture_ids"], ["unsupported-causal-claim"])
            self.assertIn("unsupported-causal-claim", report["validation"]["outputs"]["missing"])
            self.assertIn("unsupported-causal-claim", report["validation"]["manifests"]["missing"])
            self.assertIn("unsupported-causal-claim", report["validation"]["scores"]["missing"])
            self.assertEqual(
                [action["action"] for action in report["actions"]],
                ["record-live-capture-artifacts"],
            )

    def test_report_flags_live_score_regression_against_baseline(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_environment(root)
            pilot_plan = write_pilot_plan(root)
            baseline_scores = write_baseline_score(root)
            live_root = write_live_artifacts(root, fixture_path, dimension_score=3)

            report = build_calibration_report(
                fixture_path=fixture_path,
                pilot_plan_path=pilot_plan,
                live_root=live_root,
                baseline_scores_dir=baseline_scores,
                root=root,
            )

            self.assertFalse(report["ready"])
            self.assertEqual(report["regressions"]["items"][0]["fixture_id"], "unsupported-causal-claim")
            self.assertEqual(report["regressions"]["items"][0]["dimension"], "claim/evidence fit")
            self.assertEqual(report["regressions"]["items"][0]["baseline_score"], 4)
            self.assertEqual(report["regressions"]["items"][0]["live_score"], 3)
            self.assertIn("review-score-calibration", {action["action"] for action in report["actions"]})

    def test_report_flags_missing_baseline_score_as_calibration_action(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_environment(root)
            pilot_plan = write_pilot_plan(root)
            live_root = write_live_artifacts(root, fixture_path)
            baseline_scores = root / "missing-baseline-scores"

            report = build_calibration_report(
                fixture_path=fixture_path,
                pilot_plan_path=pilot_plan,
                live_root=live_root,
                baseline_scores_dir=baseline_scores,
                root=root,
            )

            self.assertFalse(report["ready"])
            self.assertIn(
                {
                    "fixture_id": "unsupported-causal-claim",
                    "action": "record-baseline-review-score",
                    "reason": "baseline review score is missing",
                },
                report["actions"],
            )

    def test_report_flags_invalid_baseline_score_as_calibration_action(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_environment(root)
            pilot_plan = write_pilot_plan(root)
            live_root = write_live_artifacts(root, fixture_path)
            baseline_scores = write_baseline_score(root)
            baseline_score_path = baseline_scores / "unsupported-causal-claim.json"
            baseline_score = json.loads(baseline_score_path.read_text(encoding="utf-8"))
            baseline_score["dimension_scores"].pop("claim/evidence fit")
            baseline_score["dimension_rationales"].pop("claim/evidence fit")
            baseline_score_path.write_text(json.dumps(baseline_score), encoding="utf-8")

            report = build_calibration_report(
                fixture_path=fixture_path,
                pilot_plan_path=pilot_plan,
                live_root=live_root,
                baseline_scores_dir=baseline_scores,
                root=root,
            )

            self.assertFalse(report["ready"])
            self.assertIn(
                {
                    "fixture_id": "unsupported-causal-claim",
                    "action": "repair-baseline-review-score",
                    "reason": "unsupported-causal-claim: baseline score dimensions must match fixture rubric_dimensions",
                },
                report["actions"],
            )

    def test_score_regression_ignores_hard_fail_when_baseline_already_hard_failed(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            live_scores = root / "live-scores"
            baseline_scores = root / "baseline-scores"
            live_scores.mkdir()
            baseline_scores.mkdir()
            (live_scores / "unsupported-causal-claim.json").write_text(
                json.dumps(score_payload(hard_fail_triggered=True)),
                encoding="utf-8",
            )
            (baseline_scores / "unsupported-causal-claim.json").write_text(
                json.dumps(score_payload(hard_fail_triggered=True)),
                encoding="utf-8",
            )

            regressions = score_regressions_for_fixture(
                "unsupported-causal-claim",
                live_scores,
                baseline_scores,
            )

            self.assertEqual(regressions, [])

    def test_report_classifies_stale_skill_hash_as_new_capture_action(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_environment(root)
            pilot_plan = write_pilot_plan(root)
            baseline_scores = write_baseline_score(root)
            live_root = write_live_artifacts(root, fixture_path)
            (root / "skills" / "methodology-source-auditor" / "SKILL.md").write_text(
                "updated skill text",
                encoding="utf-8",
            )

            report = build_calibration_report(
                fixture_path=fixture_path,
                pilot_plan_path=pilot_plan,
                live_root=live_root,
                baseline_scores_dir=baseline_scores,
                root=root,
            )

            self.assertIn(
                {
                    "fixture_id": "unsupported-causal-claim",
                    "action": "record-new-live-capture-after-skill-change",
                    "reason": "unsupported-causal-claim: manifest skill_file_sha256 does not match skill file",
                },
                report["actions"],
            )

    def test_cli_strict_fails_when_pilot_is_not_ready(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_environment(root)
            pilot_plan = write_pilot_plan(root)
            baseline_scores = write_baseline_score(root)

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--fixtures",
                    str(fixture_path),
                    "--pilot-plan",
                    str(pilot_plan),
                    "--live-root",
                    str(root / "live_pilot"),
                    "--baseline-scores-dir",
                    str(baseline_scores),
                    "--root",
                    str(root),
                    "--strict",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 1)
            payload = json.loads(result.stdout)
            self.assertFalse(payload["ready"])


if __name__ == "__main__":
    unittest.main()
