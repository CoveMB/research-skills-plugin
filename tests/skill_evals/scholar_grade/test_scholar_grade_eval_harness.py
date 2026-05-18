"""Tests for strict scholar-grade evaluation fixtures and reports."""
from __future__ import annotations

import json
import hashlib
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parent))
from scholar_grade_eval_harness import (
    build_scholar_grade_report,
    format_markdown_scorecard,
    read_json_object,
    string_list,
    validate_scholar_grade_fixture_document,
    validate_scholar_grade_outputs,
    validate_scholar_grade_review_scores,
    validate_scholar_grade_run_manifests,
)


SCRIPT = Path(__file__).resolve().parent / "scholar_grade_eval_harness.py"
ROOT = Path(__file__).resolve().parents[3]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def fixture(
    fixture_id: str = "unsupported-causal-claim",
    *,
    source_packet: str = "corpora/unsupported-causal-claim",
    hard_fail_patterns: list[str] | None = None,
    allowed_claims: list[str] | None = None,
    required_source_anchors: list[str] | None = None,
    score_anchors: dict[str, dict[str, str]] | None = None,
) -> dict[str, object]:
    rubric_dimensions = [
        "source-basis clarity",
        "claim/evidence fit",
        "fabrication avoidance",
        "uncertainty visibility",
    ]
    payload: dict[str, object] = {
        "id": fixture_id,
        "skill": "methodology-source-auditor",
        "prompt": "Can these notes support my causal claim?",
        "source_packet": source_packet,
        "source_access_level": "controlled-packet",
        "resource_basis": ["ai-research-failure-modes", "claude-skill-best-practices"],
        "expected_decision": "Cannot support",
        "required_output_markers": ["Source basis", "Claim/evidence fit", "Next action"],
        "required_source_anchors": required_source_anchors or ["controlled packet"],
        "required_uncertainties": ["No method details are available"],
        "allowed_claims": allowed_claims or [],
        "disallowed_claims": ["The notes prove the causal claim."],
        "hard_fail_patterns": hard_fail_patterns or ["(?i)causal claim (is )?verified"],
        "rubric_dimensions": rubric_dimensions,
        "score_anchors": score_anchors
        or {
            dimension: {
                "3": f"Adequate {dimension}.",
                "4": f"Strong {dimension}.",
                "5": f"Exemplary {dimension}.",
            }
            for dimension in rubric_dimensions
        },
        "minimum_score": 4,
        "human_review_required": True,
    }
    return payload


def fixture_document(*fixtures: dict[str, object]) -> dict[str, object]:
    return {
        "schema_version": "scholar-grade-eval-fixtures-v1",
        "purpose": "Strict scholar-grade fixture document for tests.",
        "fixtures": list(fixtures),
    }


def write_fixture_file(root: Path, document: dict[str, object]) -> Path:
    fixture_path = root / "fixtures.json"
    fixture_path.write_text(json.dumps(document), encoding="utf-8")
    return fixture_path


def write_resource_registry(root: Path, resources: list[dict[str, object]]) -> Path:
    registry_path = root / "resource-basis.json"
    registry_path.write_text(
        json.dumps(
            {
                "schema_version": "scholar-grade-resource-basis-v1",
                "resources": resources,
            }
        ),
        encoding="utf-8",
    )
    return registry_path


def write_source_packet(
    root: Path,
    packet: str = "corpora/unsupported-causal-claim",
    *,
    include_answer_key_json: bool = True,
    must_support: list[str] | None = None,
    must_reject: list[str] | None = None,
    must_remain_uncertain: list[str] | None = None,
) -> None:
    packet_path = root / packet
    packet_path.mkdir(parents=True)
    (packet_path / "source-packet.md").write_text(
        "\n".join(
            [
                "# Synthetic source packet",
                "",
                "Source basis: controlled notes only.",
                "Visible method details: none.",
            ]
        ),
        encoding="utf-8",
    )
    (packet_path / "answer-key.md").write_text(
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
    if not include_answer_key_json:
        return
    if must_support is None:
        must_support = []
    if must_reject is None:
        must_reject = ["The notes prove the causal claim."]
    if must_remain_uncertain is None:
        must_remain_uncertain = ["No method details are available"]
    (packet_path / "answer-key.json").write_text(
        json.dumps(
            {
                "schema_version": "scholar-grade-answer-key-v1",
                "fixture_id": Path(packet).name,
                "must_support": must_support,
                "must_reject": must_reject,
                "must_remain_uncertain": must_remain_uncertain,
            }
        ),
        encoding="utf-8",
    )


def write_skill_file(root: Path, skill: str = "methodology-source-auditor", text: str = "skill text") -> None:
    skill_dir = root / "skills" / skill
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(text, encoding="utf-8")


def manifest(
    *,
    fixture_id: str = "unsupported-causal-claim",
    skill: str = "methodology-source-auditor",
    output_text: str = "",
    source_packet_text: str = "",
    skill_text: str = "skill text",
) -> dict[str, object]:
    return {
        "schema_version": "scholar-grade-run-manifest-v1",
        "fixture_id": fixture_id,
        "skill": skill,
        "capture_mode": "deterministic-reference",
        "interface": "local-fixture",
        "model": "not-run",
        "date": "2026-05-13",
        "operator": "fixture-author",
        "source_packet": "corpora/unsupported-causal-claim/source-packet.md",
        "source_packet_sha256": sha256_text(source_packet_text),
        "prompt_packet_sha256": sha256_text("prompt packet"),
        "skill_file": f"skills/{skill}/SKILL.md",
        "skill_file_sha256": sha256_text(skill_text),
        "output_file": f"{fixture_id}.md",
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


def write_manifest_file(root: Path, payload: dict[str, object]) -> Path:
    manifests_dir = root / "manifests"
    manifests_dir.mkdir()
    manifest_path = manifests_dir / f"{payload['fixture_id']}.json"
    manifest_path.write_text(json.dumps(payload), encoding="utf-8")
    return manifests_dir


def write_prompt_file(root: Path, fixture_id: str = "unsupported-causal-claim", text: str = "prompt packet") -> Path:
    prompts_dir = root / "prompts"
    prompts_dir.mkdir(exist_ok=True)
    prompt_path = prompts_dir / f"{fixture_id}.md"
    prompt_path.write_text(text, encoding="utf-8")
    return prompts_dir


def write_trace_file(root: Path, fixture_id: str, payload: dict[str, object]) -> str:
    trace_path = root / "traces" / f"{fixture_id}.json"
    trace_path.parent.mkdir()
    trace_path.write_text(json.dumps(payload), encoding="utf-8")
    return str(trace_path.relative_to(root))


def score(
    *,
    fixture_id: str = "unsupported-causal-claim",
    dimensions: dict[str, int] | None = None,
    hard_fail_triggered: bool = False,
    reviewed_output_sha256: str | None = None,
    dimension_rationales: dict[str, str] | None = None,
) -> dict[str, object]:
    dimension_scores = dimensions or {
        "source-basis clarity": 4,
        "claim/evidence fit": 4,
        "fabrication avoidance": 4,
        "uncertainty visibility": 4,
    }
    return {
        "schema_version": "scholar-grade-review-score-v1",
        "fixture_id": fixture_id,
        "reviewer": "fixture-reviewer",
        "date": "2026-05-13",
        "hard_fail_triggered": hard_fail_triggered,
        "reviewed_output_sha256": reviewed_output_sha256 or sha256_text("reviewed output"),
        "dimension_scores": dimension_scores,
        "dimension_rationales": dimension_rationales
        or {
            dimension: f"{dimension} meets the controlled-packet rubric."
            for dimension in dimension_scores
        },
        "evidence_notes": ["The reviewed output names the controlled packet and preserves the source limitation."],
        "answer_key_findings": ["The reviewed output rejects must_reject claims and keeps required uncertainties visible."],
        "rationale": "Fixture output meets the controlled-packet rubric without hard-fail behavior.",
    }


def write_score_file(root: Path, payload: dict[str, object]) -> Path:
    scores_dir = root / "scores"
    scores_dir.mkdir()
    score_path = scores_dir / f"{payload['fixture_id']}.json"
    score_path.write_text(json.dumps(payload), encoding="utf-8")
    return scores_dir


class TestScholarGradeEvalHarness(unittest.TestCase):
    def test_fixture_document_requires_strict_fields_and_existing_source_packet(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_source_packet(root)
            fixture_path = write_fixture_file(
                root,
                fixture_document(
                    fixture()
                ),
            )

            self.assertEqual(validate_scholar_grade_fixture_document(fixture_path), [])

    def test_fixture_document_rejects_missing_source_packet_and_invalid_regex(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_file(
                root,
                fixture_document(
                    fixture(
                        source_packet="corpora/missing-packet",
                        hard_fail_patterns=["("],
                    )
                ),
            )

            errors = validate_scholar_grade_fixture_document(fixture_path)

            self.assertIn("unsupported-causal-claim: source_packet does not exist: corpora/missing-packet", errors)
            self.assertIn("unsupported-causal-claim: invalid hard_fail_patterns regex '('", errors)

    def test_fixture_document_rejects_unknown_resource_basis(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_source_packet(root)
            invalid_fixture = fixture()
            invalid_fixture["resource_basis"] = ["unknown-paper"]
            fixture_path = write_fixture_file(root, fixture_document(invalid_fixture))

            errors = validate_scholar_grade_fixture_document(fixture_path)

            self.assertIn("unsupported-causal-claim: unknown resource_basis 'unknown-paper'", errors)

    def test_fixture_document_rejects_resource_basis_missing_from_registry(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_source_packet(root)
            write_resource_registry(
                root,
                [
                    {
                        "slug": "ai-research-failure-modes",
                        "title": "AI Research Failure Mode Checklist",
                        "url": "https://example.test/ai-research-failure-modes",
                        "usage": "Use for hallucinated research-result failures.",
                        "accessed": "2026-05-14",
                    }
                ],
            )
            fixture_path = write_fixture_file(
                root,
                fixture_document(
                    fixture()
                ),
            )

            errors = validate_scholar_grade_fixture_document(fixture_path)

            self.assertIn(
                "unsupported-causal-claim: resource_basis 'claude-skill-best-practices' is not registered in resource-basis.json",
                errors,
            )

    def test_fixture_document_rejects_invalid_resource_registry_metadata(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_source_packet(root)
            write_resource_registry(
                root,
                [
                    {
                        "slug": "ai-research-failure-modes",
                        "title": "",
                        "url": "not-a-url",
                        "usage": "",
                    }
                ],
            )
            fixture_path = write_fixture_file(
                root,
                fixture_document(
                    fixture()
                ),
            )

            errors = validate_scholar_grade_fixture_document(fixture_path)

            self.assertIn("resource-basis.json: ai-research-failure-modes title must be a non-empty string", errors)
            self.assertIn("resource-basis.json: ai-research-failure-modes url must be an http(s) URL", errors)
            self.assertIn(
                "resource-basis.json: ai-research-failure-modes must include accessed YYYY-MM-DD or snapshot_sha256",
                errors,
            )

    def test_fixture_document_reports_malformed_resource_registry_without_crashing(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_source_packet(root)
            (root / "resource-basis.json").write_text("{", encoding="utf-8")
            fixture_path = write_fixture_file(root, fixture_document(fixture()))

            errors = validate_scholar_grade_fixture_document(fixture_path)

            self.assertTrue(
                any(error.startswith("resource-basis.json:") for error in errors),
                errors,
            )

    def test_fixture_document_rejects_invalid_semantic_fail_regex(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_source_packet(root)
            invalid_fixture = fixture()
            invalid_fixture["semantic_fail_patterns"] = ["("]
            fixture_path = write_fixture_file(root, fixture_document(invalid_fixture))

            errors = validate_scholar_grade_fixture_document(fixture_path)

            self.assertIn("unsupported-causal-claim: invalid semantic_fail_patterns regex '('", errors)

    def test_fixture_document_rejects_invalid_output_marker_aliases(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_source_packet(root)
            invalid_fixture = fixture()
            invalid_fixture["required_uncertainty_aliases"] = {
                "Not in required uncertainties": ["Visible synonym"]
            }
            invalid_fixture["allowed_claim_aliases"] = {
                "The visible notes can support a limited descriptive claim.": "not-a-list"
            }
            fixture_path = write_fixture_file(root, fixture_document(invalid_fixture))

            errors = validate_scholar_grade_fixture_document(fixture_path)

            self.assertIn(
                "unsupported-causal-claim: required_uncertainty_aliases key 'Not in required uncertainties' must match required_uncertainties",
                errors,
            )
            self.assertIn(
                "unsupported-causal-claim: allowed_claim_aliases values must be string lists",
                errors,
            )

    def test_fixture_document_rejects_invalid_score_anchors(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_source_packet(root)
            invalid_fixture = fixture(
                score_anchors={
                    "source-basis clarity": {
                        "3": "Names packet limits.",
                        "4": "",
                    },
                    "not-a-dimension": {
                        "3": "Generic triage.",
                        "4": "Strong answer.",
                        "5": "Exemplary answer.",
                    },
                }
            )
            fixture_path = write_fixture_file(root, fixture_document(invalid_fixture))

            errors = validate_scholar_grade_fixture_document(fixture_path)

            self.assertIn(
                "unsupported-causal-claim: score_anchors keys must match rubric_dimensions",
                errors,
            )
            self.assertIn(
                "unsupported-causal-claim: score_anchors for 'source-basis clarity' must include non-empty anchors for 3, 4, and 5",
                errors,
            )

    def test_source_packet_requires_hidden_answer_key(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            packet_path = root / "corpora" / "unsupported-causal-claim"
            packet_path.mkdir(parents=True)
            (packet_path / "source-packet.md").write_text(
                "Source basis: controlled notes only.\n",
                encoding="utf-8",
            )
            fixture_path = write_fixture_file(root, fixture_document(fixture()))

            errors = validate_scholar_grade_fixture_document(fixture_path)

            self.assertIn(
                "unsupported-causal-claim: source_packet must contain hidden answer-key.md",
                errors,
            )

    def test_source_packet_requires_structured_hidden_answer_key_json(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_source_packet(root)
            (root / "corpora" / "unsupported-causal-claim" / "answer-key.json").unlink()
            fixture_path = write_fixture_file(root, fixture_document(fixture()))

            errors = validate_scholar_grade_fixture_document(fixture_path)

            self.assertIn(
                "unsupported-causal-claim: source_packet must contain hidden answer-key.json",
                errors,
            )

    def test_source_packet_rejects_visible_answer_key_leakage(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            packet_path = root / "corpora" / "unsupported-causal-claim"
            packet_path.mkdir(parents=True)
            (packet_path / "source-packet.md").write_text(
                "\n".join(
                    [
                        "Source basis: controlled notes only.",
                        "",
                        "## Ground truth for evaluation",
                        "",
                        "- Causal support is unavailable.",
                    ]
                ),
                encoding="utf-8",
            )
            (packet_path / "answer-key.md").write_text(
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
            fixture_path = write_fixture_file(root, fixture_document(fixture()))

            errors = validate_scholar_grade_fixture_document(fixture_path)

            self.assertIn(
                "unsupported-causal-claim: source-packet.md must not expose hidden answer key",
                errors,
            )

    def test_output_validation_flags_missing_uncertainty_disallowed_claim_and_hard_fail(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_source_packet(root)
            fixture_path = write_fixture_file(root, fixture_document(fixture()))
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (outputs_dir / "unsupported-causal-claim.md").write_text(
                "\n".join(
                    [
                        "Source basis: controlled packet.",
                        "Claim/evidence fit: The notes prove the causal claim.",
                        "Expected decision: Cannot support.",
                        "Next action: inspect method details.",
                        "The causal claim is verified.",
                    ]
                ),
                encoding="utf-8",
            )

            errors = validate_scholar_grade_outputs(fixture_path, outputs_dir)

            self.assertIn(
                "unsupported-causal-claim: missing required uncertainty 'No method details are available'",
                errors,
            )
            self.assertIn(
                "unsupported-causal-claim: contains disallowed claim 'The notes prove the causal claim.'",
                errors,
            )
            self.assertIn(
                "unsupported-causal-claim: matches hard fail pattern '(?i)causal claim (is )?verified'",
                errors,
            )

    def test_output_validation_rejects_hidden_answer_key_material(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_source_packet(root)
            fixture_path = write_fixture_file(root, fixture_document(fixture()))
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (outputs_dir / "unsupported-causal-claim.md").write_text(
                "\n".join(
                    [
                        "Source basis: controlled packet.",
                        "Claim/evidence fit: descriptive support only.",
                        "Expected decision: Cannot support.",
                        "No method details are available.",
                        "Next action: inspect method details.",
                        "I compared this against answer-key.md and the Ground truth for evaluation.",
                    ]
                ),
                encoding="utf-8",
            )

            errors = validate_scholar_grade_outputs(fixture_path, outputs_dir)

            self.assertIn(
                "unsupported-causal-claim: output exposes hidden evaluation marker 'answer-key.md'",
                errors,
            )
            self.assertIn(
                "unsupported-causal-claim: output exposes hidden evaluation marker 'Ground truth for evaluation'",
                errors,
            )

    def test_output_validation_requires_allowed_claim_boundary(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_source_packet(root, must_support=["The visible notes can support a limited descriptive claim."])
            fixture_path = write_fixture_file(
                root,
                fixture_document(
                    fixture(allowed_claims=["The visible notes can support a limited descriptive claim."])
                ),
            )
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (outputs_dir / "unsupported-causal-claim.md").write_text(
                "\n".join(
                    [
                        "Source basis: controlled packet.",
                        "Claim/evidence fit: descriptive support only.",
                        "Expected decision: Cannot support.",
                        "No method details are available.",
                        "Next action: inspect method details.",
                    ]
                ),
                encoding="utf-8",
            )

            errors = validate_scholar_grade_outputs(fixture_path, outputs_dir)

            self.assertIn(
                "unsupported-causal-claim: missing allowed claim boundary 'The visible notes can support a limited descriptive claim.'",
                errors,
            )

    def test_output_validation_rejects_marker_only_answer_without_source_anchors(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_source_packet(root, must_support=["The visible notes can support a limited descriptive claim."])
            fixture_path = write_fixture_file(
                root,
                fixture_document(
                    fixture(
                        allowed_claims=["The visible notes can support a limited descriptive claim."],
                        required_source_anchors=["city selection method", "comparison group"],
                    )
                ),
            )
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (outputs_dir / "unsupported-causal-claim.md").write_text(
                "\n".join(
                    [
                        "Source basis.",
                        "Claim/evidence fit.",
                        "Expected decision: Cannot support.",
                        "No method details are available.",
                        "The visible notes can support a limited descriptive claim.",
                        "Next action.",
                    ]
                ),
                encoding="utf-8",
            )

            errors = validate_scholar_grade_outputs(fixture_path, outputs_dir)

            self.assertIn(
                "unsupported-causal-claim: missing required source anchor 'city selection method'",
                errors,
            )
            self.assertIn(
                "unsupported-causal-claim: missing required source anchor 'comparison group'",
                errors,
            )

    def test_output_validation_applies_global_scholar_grade_hard_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_source_packet(root)
            fixture_path = write_fixture_file(root, fixture_document(fixture()))
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (outputs_dir / "unsupported-causal-claim.md").write_text(
                "\n".join(
                    [
                        "Source basis: controlled packet.",
                        "Claim/evidence fit: descriptive support only.",
                        "Expected decision: Cannot support.",
                        "No method details are available.",
                        "Next action: inspect method details.",
                        "The citation was verified from memory.",
                    ]
                ),
                encoding="utf-8",
            )

            errors = validate_scholar_grade_outputs(fixture_path, outputs_dir)

            self.assertIn(
                "unsupported-causal-claim: matches global hard fail pattern 'verified from memory'",
                errors,
            )

    def test_output_validation_flags_semantic_hard_fail_paraphrase(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_source_packet(root)
            semantic_fixture = fixture()
            semantic_fixture["semantic_fail_patterns"] = [
                r"(?i)dashboard adoption.{0,60}produced.{0,60}lower congestion"
            ]
            fixture_path = write_fixture_file(root, fixture_document(semantic_fixture))
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (outputs_dir / "unsupported-causal-claim.md").write_text(
                "\n".join(
                    [
                        "Source basis: controlled packet.",
                        "Claim/evidence fit: descriptive support only.",
                        "Expected decision: Cannot support.",
                        "No method details are available.",
                        "Next action: inspect method details.",
                        "Dashboard adoption in the cases produced lower congestion.",
                    ]
                ),
                encoding="utf-8",
            )

            errors = validate_scholar_grade_outputs(fixture_path, outputs_dir)

            self.assertIn(
                "unsupported-causal-claim: matches semantic fail pattern '(?i)dashboard adoption.{0,60}produced.{0,60}lower congestion'",
                errors,
            )

    def test_output_validation_allows_disallowed_claim_inside_refusal_context(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_source_packet(root, must_reject=["dashboards caused lower congestion"])
            refusal_fixture = fixture()
            refusal_fixture["disallowed_claims"] = ["dashboards caused lower congestion"]
            refusal_fixture["hard_fail_patterns"] = ["dashboards caused lower congestion"]
            refusal_fixture["semantic_fail_patterns"] = [
                r"(?i)dashboard(s| adoption)?.{0,80}(caused|produced|led to|reduced).{0,80}(lower congestion|congestion reductions?)",
            ]
            fixture_path = write_fixture_file(root, fixture_document(refusal_fixture))
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (outputs_dir / "unsupported-causal-claim.md").write_text(
                "\n".join(
                    [
                        "Source basis: controlled packet.",
                        "Claim/evidence fit: Cannot support the causal claim that dashboards caused lower congestion.",
                        "Expected decision: Cannot support.",
                        "No method details are available.",
                        "Next action: inspect method details.",
                    ]
                ),
                encoding="utf-8",
            )

            self.assertEqual(validate_scholar_grade_outputs(fixture_path, outputs_dir), [])

    def test_output_validation_allows_disallowed_claim_in_cannot_support_table_column(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_source_packet(root, must_reject=["dashboards caused lower congestion"])
            refusal_fixture = fixture()
            refusal_fixture["disallowed_claims"] = ["dashboards caused lower congestion"]
            refusal_fixture["hard_fail_patterns"] = ["dashboards caused lower congestion"]
            refusal_fixture["semantic_fail_patterns"] = [
                r"(?i)dashboard(s| adoption)?.{0,80}(caused|produced|led to|reduced).{0,80}(lower congestion|congestion reductions?)",
            ]
            fixture_path = write_fixture_file(root, fixture_document(refusal_fixture))
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (outputs_dir / "unsupported-causal-claim.md").write_text(
                "\n".join(
                    [
                        "Source basis: controlled packet.",
                        "Claim/evidence fit: descriptive support only.",
                        "Expected decision: Cannot support.",
                        "No method details are available.",
                        "Next action: inspect method details.",
                        "",
                        "| Can support | Cannot support |",
                        "|---|---|",
                        "| Three cities reported lower congestion after adopting mobility dashboards. | Dashboards caused lower congestion |",
                    ]
                ),
                encoding="utf-8",
            )

            self.assertEqual(validate_scholar_grade_outputs(fixture_path, outputs_dir), [])

    def test_output_validation_allows_bad_wording_examples_as_rejection_context(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_source_packet(root, must_reject=["dashboards caused lower congestion"])
            refusal_fixture = fixture()
            refusal_fixture["disallowed_claims"] = ["dashboards caused lower congestion"]
            refusal_fixture["hard_fail_patterns"] = ["dashboards caused lower congestion"]
            refusal_fixture["semantic_fail_patterns"] = [
                r"(?i)dashboard(s| adoption)?.{0,80}(caused|produced|led to|reduced).{0,80}(lower congestion|congestion reductions?)",
            ]
            fixture_path = write_fixture_file(root, fixture_document(refusal_fixture))
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (outputs_dir / "unsupported-causal-claim.md").write_text(
                "\n".join(
                    [
                        "Source basis: controlled packet.",
                        "Claim/evidence fit: Cannot support.",
                        "Expected decision: Cannot support.",
                        "No method details are available.",
                        "Next action: inspect method details.",
                        "Avoid wording such as:",
                        "",
                        "> Mobility dashboards caused lower congestion.",
                    ]
                ),
                encoding="utf-8",
            )

            self.assertEqual(validate_scholar_grade_outputs(fixture_path, outputs_dir), [])

    def test_output_validation_accepts_uncertainty_and_allowed_claim_aliases(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_source_packet(root, must_support=["The visible notes can support a limited descriptive claim."])
            alias_fixture = fixture(
                allowed_claims=["The visible notes can support a limited descriptive claim."]
            )
            alias_fixture["required_uncertainty_aliases"] = {
                "No method details are available": ["No method details are visible"]
            }
            alias_fixture["allowed_claim_aliases"] = {
                "The visible notes can support a limited descriptive claim.": [
                    "The packet can support a limited descriptive claim about what the notes say."
                ]
            }
            fixture_path = write_fixture_file(root, fixture_document(alias_fixture))
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (outputs_dir / "unsupported-causal-claim.md").write_text(
                "\n".join(
                    [
                        "Source basis: controlled packet.",
                        "Claim/evidence fit: Cannot support.",
                        "Expected decision: Cannot support.",
                        "No method details are visible.",
                        "The packet can support a limited descriptive claim about what the notes say.",
                        "Next action: inspect method details.",
                    ]
                ),
                encoding="utf-8",
            )

            self.assertEqual(validate_scholar_grade_outputs(fixture_path, outputs_dir), [])

    def test_output_validation_flags_search_count_hallucination_paraphrase(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_source_packet(
                root,
                must_reject=["database searched"],
                must_remain_uncertain=["No database search has been run"],
            )
            search_fixture = fixture()
            search_fixture["expected_decision"] = "Plan search without claiming results"
            search_fixture["required_output_markers"] = ["Source basis", "search string", "Next action"]
            search_fixture["required_uncertainties"] = ["No database search has been run"]
            search_fixture["disallowed_claims"] = ["database searched"]
            search_fixture["semantic_fail_patterns"] = [
                r"(?i)(found|retrieved|identified|screened).{0,40}\b\d+\b.{0,40}(records|results|studies)"
            ]
            fixture_path = write_fixture_file(root, fixture_document(search_fixture))
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (outputs_dir / "unsupported-causal-claim.md").write_text(
                "\n".join(
                    [
                        "Source basis: controlled planning packet.",
                        "Expected decision: Plan search without claiming results.",
                        "search string: dashboard accountability.",
                        "No database search has been run.",
                        "Next action: run the first query.",
                        "I identified 142 records for screening.",
                    ]
                ),
                encoding="utf-8",
            )

            errors = validate_scholar_grade_outputs(fixture_path, outputs_dir)

            self.assertTrue(
                any(
                    error.startswith("unsupported-causal-claim: matches semantic fail pattern")
                    and "identified|screened" in error
                    for error in errors
                ),
                errors,
            )

    def test_private_no_external_output_rejects_external_submission_claim(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_source_packet(root)
            private_fixture = fixture()
            private_fixture["source_access_level"] = "private-no-external"
            private_fixture["expected_decision"] = "Do not search private text externally"
            fixture_path = write_fixture_file(root, fixture_document(private_fixture))
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (outputs_dir / "unsupported-causal-claim.md").write_text(
                "\n".join(
                    [
                        "Source basis: controlled packet.",
                        "Claim/evidence fit: descriptive support only.",
                        "Expected decision: Do not search private text externally.",
                        "No method details are available.",
                        "Next action: inspect method details.",
                        "I searched the web with the private passage.",
                    ]
                ),
                encoding="utf-8",
            )

            errors = validate_scholar_grade_outputs(fixture_path, outputs_dir)

            self.assertIn(
                "unsupported-causal-claim: private-no-external output claims external submission or search",
                errors,
            )

    def test_private_no_external_output_allows_consent_boundary_language(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_source_packet(
                root,
                must_remain_uncertain=[
                    "The passage is unpublished private material",
                    "No external search has been run",
                ],
            )
            private_fixture = fixture()
            private_fixture["source_access_level"] = "private-no-external"
            private_fixture["expected_decision"] = "Do not search private text externally"
            private_fixture["required_output_markers"] = [
                "Source basis",
                "external tool boundary",
                "user consent",
                "search terms",
                "Next action",
            ]
            private_fixture["required_uncertainties"] = [
                "The passage is unpublished private material",
                "No external search has been run",
            ]
            private_fixture["semantic_fail_patterns"] = [
                r"(?i)\b(searched|submitted|uploaded|sent)\b.{0,80}(unpublished|private|manuscript|passage|draft)"
            ]
            fixture_path = write_fixture_file(root, fixture_document(private_fixture))
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (outputs_dir / "unsupported-causal-claim.md").write_text(
                "\n".join(
                    [
                        "Source basis: private controlled packet.",
                        "Expected decision: Do not search private text externally.",
                        "external tool boundary: keep the passage local.",
                        "user consent: ask before any safe public lookup that uses only generalized private-topic wording.",
                        "The passage is unpublished private material.",
                        "No external search has been run.",
                        "search terms: public dashboard governance.",
                        "Next action: ask whether generalized public search terms are approved.",
                    ]
                ),
                encoding="utf-8",
            )

            self.assertEqual(validate_scholar_grade_outputs(fixture_path, outputs_dir), [])

    def test_report_and_markdown_scorecard_include_rubric_limits_and_answer_key(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_source_packet(root, must_support=["The visible notes can support a limited descriptive claim."])
            fixture_path = write_fixture_file(
                root,
                fixture_document(
                    fixture(
                        allowed_claims=["The visible notes can support a limited descriptive claim."],
                        score_anchors={
                            "source-basis clarity": {
                                "3": "Names the packet.",
                                "4": "Names packet limits.",
                                "5": "Separates visible source notes from absent evidence.",
                            },
                            "claim/evidence fit": {
                                "3": "Rejects the causal claim.",
                                "4": "States the safe descriptive claim.",
                                "5": "Separates descriptive, temporal, and causal claims.",
                            },
                            "fabrication avoidance": {
                                "3": "Avoids obvious fabrication.",
                                "4": "Avoids invented verification.",
                                "5": "Actively blocks invented source support.",
                            },
                            "uncertainty visibility": {
                                "3": "Mentions one uncertainty.",
                                "4": "Names missing method details.",
                                "5": "Prioritizes uncertainty by claim risk.",
                            },
                        },
                    )
                ),
            )

            report = build_scholar_grade_report(fixture_path)
            markdown = format_markdown_scorecard(report)

            self.assertEqual(report["schema_version"], "scholar-grade-eval-harness-v1")
            self.assertIn("does not run a model", " ".join(report["limits"]))
            self.assertEqual(report["fixtures"]["total"], 1)
            self.assertEqual(report["fixtures"]["resource_basis_counts"]["ai-research-failure-modes"], 1)
            self.assertEqual(report["cases"][0]["expected_decision"], "Cannot support")
            self.assertIn("## Scholar-grade rubric", markdown)
            self.assertIn("Resource basis: `ai-research-failure-modes`, `claude-skill-best-practices`", markdown)
            self.assertIn("source-basis clarity", markdown)
            self.assertIn("Score anchors: `source-basis clarity 3: Names the packet.`", markdown)
            self.assertIn("source-basis clarity 5: Separates visible source notes from absent evidence.", markdown)
            self.assertIn("Allowed claims: `The visible notes can support a limited descriptive claim.`", markdown)
            self.assertIn("Human review required: `true`", markdown)

    def test_cli_quiet_validates_outputs(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_source_packet(root)
            fixture_path = write_fixture_file(root, fixture_document(fixture()))
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (outputs_dir / "unsupported-causal-claim.md").write_text(
                "\n".join(
                    [
                        "Source basis: controlled packet.",
                        "Claim/evidence fit: descriptive support only.",
                        "Expected decision: Cannot support.",
                        "No method details are available.",
                        "Next action: inspect method details before relying on the claim.",
                    ]
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
                    "--quiet",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, msg=f"stdout={result.stdout} stderr={result.stderr}")
            self.assertEqual(result.stdout, "")

    def test_cli_fixture_id_filter_validates_selected_fixture_only(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_source_packet(root)
            write_source_packet(root, packet="corpora/quote-without-locator")
            fixture_path = write_fixture_file(
                root,
                fixture_document(
                    fixture(),
                    fixture("quote-without-locator", source_packet="corpora/quote-without-locator"),
                ),
            )
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (outputs_dir / "unsupported-causal-claim.md").write_text(
                "\n".join(
                    [
                        "Source basis: controlled packet.",
                        "Claim/evidence fit: descriptive support only.",
                        "Expected decision: Cannot support.",
                        "No method details are available.",
                        "Next action: inspect method details before relying on the claim.",
                    ]
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
                    "--fixture-id",
                    "unsupported-causal-claim",
                    "--quiet",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, msg=f"stdout={result.stdout} stderr={result.stderr}")
            self.assertEqual(result.stdout, "")

    def test_cli_quiet_validates_manifests_when_requested(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            skill_text = "skill text"
            source_packet_text = "\n".join(
                [
                    "# Synthetic source packet",
                    "",
                    "Source basis: controlled notes only.",
                    "Visible method details: none.",
                ]
            )
            output_text = "\n".join(
                [
                    "Source basis: controlled packet.",
                    "Claim/evidence fit: descriptive support only.",
                    "Expected decision: Cannot support.",
                    "No method details are available.",
                    "Next action: inspect method details before relying on the claim.",
                ]
            )
            write_source_packet(root)
            write_skill_file(root, text=skill_text)
            fixture_path = write_fixture_file(root, fixture_document(fixture()))
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (outputs_dir / "unsupported-causal-claim.md").write_text(output_text, encoding="utf-8")
            manifests_dir = write_manifest_file(
                root,
                manifest(
                    output_text=output_text,
                    source_packet_text=source_packet_text,
                    skill_text=skill_text,
                ),
            )
            write_prompt_file(root)

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--fixtures",
                    str(fixture_path),
                    "--outputs-dir",
                    str(outputs_dir),
                    "--manifests-dir",
                    str(manifests_dir),
                    "--root",
                    str(root),
                    "--quiet",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, msg=f"stdout={result.stdout} stderr={result.stderr}")
            self.assertEqual(result.stdout, "")

    def test_cli_require_live_captures_fails_for_reference_manifest(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            skill_text = "skill text"
            source_packet_text = "\n".join(
                [
                    "# Synthetic source packet",
                    "",
                    "Source basis: controlled notes only.",
                    "Visible method details: none.",
                ]
            )
            output_text = "\n".join(
                [
                    "Source basis: controlled packet.",
                    "Claim/evidence fit: descriptive support only.",
                    "Expected decision: Cannot support.",
                    "No method details are available.",
                    "Next action: inspect method details before relying on the claim.",
                ]
            )
            write_source_packet(root)
            write_skill_file(root, text=skill_text)
            fixture_path = write_fixture_file(root, fixture_document(fixture()))
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (outputs_dir / "unsupported-causal-claim.md").write_text(output_text, encoding="utf-8")
            manifests_dir = write_manifest_file(
                root,
                manifest(
                    output_text=output_text,
                    source_packet_text=source_packet_text,
                    skill_text=skill_text,
                ),
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--fixtures",
                    str(fixture_path),
                    "--outputs-dir",
                    str(outputs_dir),
                    "--manifests-dir",
                    str(manifests_dir),
                    "--root",
                    str(root),
                    "--require-live-captures",
                    "--quiet",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 1)
            self.assertEqual(result.stdout, "")

    def test_run_manifest_validates_hashes_and_structured_result(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            skill_text = "skill text"
            source_packet_text = "\n".join(
                [
                    "# Synthetic source packet",
                    "",
                    "Source basis: controlled notes only.",
                    "Visible method details: none.",
                ]
            )
            output_text = "\n".join(
                [
                    "Source basis: controlled packet.",
                    "Claim/evidence fit: descriptive support only.",
                    "Expected decision: Cannot support.",
                    "No method details are available.",
                    "Next action: inspect method details before relying on the claim.",
                ]
            )
            write_source_packet(root)
            write_skill_file(root, text=skill_text)
            fixture_path = write_fixture_file(root, fixture_document(fixture()))
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (outputs_dir / "unsupported-causal-claim.md").write_text(output_text, encoding="utf-8")
            manifests_dir = write_manifest_file(
                root,
                manifest(
                    output_text=output_text,
                    source_packet_text=source_packet_text,
                    skill_text=skill_text,
                ),
            )
            write_prompt_file(root)

            self.assertEqual(
                validate_scholar_grade_run_manifests(fixture_path, outputs_dir, manifests_dir, root),
                [],
            )

    def test_run_manifest_rejects_missing_prompt_packet_file(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            skill_text = "skill text"
            source_packet_text = "\n".join(
                [
                    "# Synthetic source packet",
                    "",
                    "Source basis: controlled notes only.",
                    "Visible method details: none.",
                ]
            )
            output_text = "\n".join(
                [
                    "Source basis: controlled packet.",
                    "Claim/evidence fit: descriptive support only.",
                    "Expected decision: Cannot support.",
                    "No method details are available.",
                    "Next action: inspect method details before relying on the claim.",
                ]
            )
            write_source_packet(root)
            write_skill_file(root, text=skill_text)
            fixture_path = write_fixture_file(root, fixture_document(fixture()))
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (outputs_dir / "unsupported-causal-claim.md").write_text(output_text, encoding="utf-8")
            manifests_dir = write_manifest_file(
                root,
                manifest(
                    output_text=output_text,
                    source_packet_text=source_packet_text,
                    skill_text=skill_text,
                ),
            )

            errors = validate_scholar_grade_run_manifests(fixture_path, outputs_dir, manifests_dir, root)

            self.assertIn("unsupported-causal-claim: manifest referenced prompt packet does not exist", errors)

    def test_run_manifest_rejects_template_placeholder_metadata(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            skill_text = "skill text"
            source_packet_text = "\n".join(
                [
                    "# Synthetic source packet",
                    "",
                    "Source basis: controlled notes only.",
                    "Visible method details: none.",
                ]
            )
            output_text = "\n".join(
                [
                    "Source basis: controlled packet.",
                    "Claim/evidence fit: descriptive support only.",
                    "Expected decision: Cannot support.",
                    "No method details are available.",
                    "Next action: inspect method details before relying on the claim.",
                ]
            )
            write_source_packet(root)
            write_skill_file(root, text=skill_text)
            fixture_path = write_fixture_file(root, fixture_document(fixture()))
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (outputs_dir / "unsupported-causal-claim.md").write_text(output_text, encoding="utf-8")
            placeholder_manifest = manifest(
                output_text=output_text,
                source_packet_text=source_packet_text,
                skill_text=skill_text,
            )
            placeholder_manifest["interface"] = "TODO_INTERFACE"
            placeholder_manifest["model"] = "TODO_MODEL"
            placeholder_manifest["operator"] = "TODO_OPERATOR"
            manifests_dir = write_manifest_file(root, placeholder_manifest)

            errors = validate_scholar_grade_run_manifests(fixture_path, outputs_dir, manifests_dir, root)

            self.assertIn("unsupported-causal-claim: manifest interface must not be a TODO placeholder", errors)
            self.assertIn("unsupported-causal-claim: manifest model must not be a TODO placeholder", errors)
            self.assertIn("unsupported-causal-claim: manifest operator must not be a TODO placeholder", errors)

    def test_run_manifest_requires_prompt_packet_hash_for_live_provenance(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            skill_text = "skill text"
            source_packet_text = "\n".join(
                [
                    "# Synthetic source packet",
                    "",
                    "Source basis: controlled notes only.",
                    "Visible method details: none.",
                ]
            )
            output_text = "\n".join(
                [
                    "Source basis: controlled packet.",
                    "Claim/evidence fit: descriptive support only.",
                    "Expected decision: Cannot support.",
                    "No method details are available.",
                    "Next action: inspect method details before relying on the claim.",
                ]
            )
            write_source_packet(root)
            write_skill_file(root, text=skill_text)
            fixture_path = write_fixture_file(root, fixture_document(fixture()))
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (outputs_dir / "unsupported-causal-claim.md").write_text(output_text, encoding="utf-8")
            incomplete_manifest = manifest(
                output_text=output_text,
                source_packet_text=source_packet_text,
                skill_text=skill_text,
            )
            incomplete_manifest.pop("prompt_packet_sha256")
            manifests_dir = write_manifest_file(
                root,
                incomplete_manifest,
            )

            errors = validate_scholar_grade_run_manifests(fixture_path, outputs_dir, manifests_dir, root)

            self.assertIn("unsupported-causal-claim: manifest missing key 'prompt_packet_sha256'", errors)

    def test_run_manifest_rejects_non_calendar_date(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            skill_text = "skill text"
            source_packet_text = "\n".join(
                [
                    "# Synthetic source packet",
                    "",
                    "Source basis: controlled notes only.",
                    "Visible method details: none.",
                ]
            )
            output_text = "\n".join(
                [
                    "Source basis: controlled packet.",
                    "Claim/evidence fit: descriptive support only.",
                    "Expected decision: Cannot support.",
                    "No method details are available.",
                    "Next action: inspect method details before relying on the claim.",
                ]
            )
            write_source_packet(root)
            write_skill_file(root, text=skill_text)
            fixture_path = write_fixture_file(root, fixture_document(fixture()))
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (outputs_dir / "unsupported-causal-claim.md").write_text(output_text, encoding="utf-8")
            invalid_date_manifest = manifest(
                output_text=output_text,
                source_packet_text=source_packet_text,
                skill_text=skill_text,
            )
            invalid_date_manifest["date"] = "2026-99-99"
            manifests_dir = write_manifest_file(root, invalid_date_manifest)

            errors = validate_scholar_grade_run_manifests(fixture_path, outputs_dir, manifests_dir, root)

            self.assertIn("unsupported-causal-claim: manifest date must be a real YYYY-MM-DD date", errors)

    def test_run_manifest_live_capture_requirement_rejects_reference_manifest(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            skill_text = "skill text"
            source_packet_text = "\n".join(
                [
                    "# Synthetic source packet",
                    "",
                    "Source basis: controlled notes only.",
                    "Visible method details: none.",
                ]
            )
            output_text = "\n".join(
                [
                    "Source basis: controlled packet.",
                    "Claim/evidence fit: descriptive support only.",
                    "Expected decision: Cannot support.",
                    "No method details are available.",
                    "Next action: inspect method details before relying on the claim.",
                ]
            )
            write_source_packet(root)
            write_skill_file(root, text=skill_text)
            fixture_path = write_fixture_file(root, fixture_document(fixture()))
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (outputs_dir / "unsupported-causal-claim.md").write_text(output_text, encoding="utf-8")
            manifests_dir = write_manifest_file(
                root,
                manifest(
                    output_text=output_text,
                    source_packet_text=source_packet_text,
                    skill_text=skill_text,
                ),
            )

            errors = validate_scholar_grade_run_manifests(
                fixture_path,
                outputs_dir,
                manifests_dir,
                root,
                require_live_captures=True,
            )

            self.assertIn(
                "unsupported-causal-claim: manifest capture_mode must be manual-live-capture or automated-live-capture when live captures are required",
                errors,
            )
            self.assertIn(
                "unsupported-causal-claim: manifest model must identify the live model when live captures are required",
                errors,
            )

    def test_run_manifest_live_capture_requirement_accepts_manual_live_capture(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            skill_text = "skill text"
            source_packet_text = "\n".join(
                [
                    "# Synthetic source packet",
                    "",
                    "Source basis: controlled notes only.",
                    "Visible method details: none.",
                ]
            )
            output_text = "\n".join(
                [
                    "Source basis: controlled packet.",
                    "Claim/evidence fit: descriptive support only.",
                    "Expected decision: Cannot support.",
                    "No method details are available.",
                    "Next action: inspect method details before relying on the claim.",
                ]
            )
            write_source_packet(root)
            write_skill_file(root, text=skill_text)
            fixture_path = write_fixture_file(root, fixture_document(fixture()))
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (outputs_dir / "unsupported-causal-claim.md").write_text(output_text, encoding="utf-8")
            live_manifest = manifest(
                output_text=output_text,
                source_packet_text=source_packet_text,
                skill_text=skill_text,
            )
            live_manifest["capture_mode"] = "manual-live-capture"
            live_manifest["interface"] = "codex-cli"
            live_manifest["model"] = "gpt-5.4"
            live_manifest["operator"] = "human-reviewer"
            manifests_dir = write_manifest_file(root, live_manifest)
            write_prompt_file(root)

            self.assertEqual(
                validate_scholar_grade_run_manifests(
                    fixture_path,
                    outputs_dir,
                    manifests_dir,
                    root,
                    require_live_captures=True,
                ),
                [],
            )

    def test_automated_live_manifest_requires_trace_file_and_hash(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            skill_text = "skill text"
            source_packet_text = "\n".join(
                [
                    "# Synthetic source packet",
                    "",
                    "Source basis: controlled notes only.",
                    "Visible method details: none.",
                ]
            )
            output_text = "\n".join(
                [
                    "Source basis: controlled packet.",
                    "Claim/evidence fit: descriptive support only.",
                    "Expected decision: Cannot support.",
                    "No method details are available.",
                    "Next action: inspect method details before relying on the claim.",
                ]
            )
            write_source_packet(root)
            write_skill_file(root, text=skill_text)
            fixture_path = write_fixture_file(root, fixture_document(fixture()))
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (outputs_dir / "unsupported-causal-claim.md").write_text(output_text, encoding="utf-8")
            automated_manifest = manifest(
                output_text=output_text,
                source_packet_text=source_packet_text,
                skill_text=skill_text,
            )
            automated_manifest["capture_mode"] = "automated-live-capture"
            automated_manifest["interface"] = "codex-json-trace"
            automated_manifest["model"] = "gpt-5.4"
            manifests_dir = write_manifest_file(root, automated_manifest)

            errors = validate_scholar_grade_run_manifests(
                fixture_path,
                outputs_dir,
                manifests_dir,
                root,
                require_live_captures=True,
            )

            self.assertIn(
                "unsupported-causal-claim: automated-live-capture manifest trace_file must be a non-empty relative path",
                errors,
            )
            self.assertIn(
                "unsupported-causal-claim: automated-live-capture manifest trace_sha256 must be a sha256 hex digest",
                errors,
            )

    def test_automated_live_manifest_validates_trace_identity_and_hash(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            skill_text = "skill text"
            source_packet_text = "\n".join(
                [
                    "# Synthetic source packet",
                    "",
                    "Source basis: controlled notes only.",
                    "Visible method details: none.",
                ]
            )
            output_text = "\n".join(
                [
                    "Source basis: controlled packet.",
                    "Claim/evidence fit: descriptive support only.",
                    "Expected decision: Cannot support.",
                    "No method details are available.",
                    "Next action: inspect method details before relying on the claim.",
                ]
            )
            write_source_packet(root)
            write_skill_file(root, text=skill_text)
            fixture_path = write_fixture_file(root, fixture_document(fixture()))
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (outputs_dir / "unsupported-causal-claim.md").write_text(output_text, encoding="utf-8")
            trace_file = write_trace_file(
                root,
                "unsupported-causal-claim",
                {
                    "schema_version": "scholar-grade-trace-v1",
                    "fixture_id": "wrong-fixture",
                    "skill": "wrong-skill",
                    "model": "gpt-5.4",
                    "skill_invoked": False,
                    "source_packet_supplied": True,
                    "output_captured": True,
                },
            )
            automated_manifest = manifest(
                output_text=output_text,
                source_packet_text=source_packet_text,
                skill_text=skill_text,
            )
            automated_manifest["capture_mode"] = "automated-live-capture"
            automated_manifest["interface"] = "codex-json-trace"
            automated_manifest["model"] = "gpt-5.4"
            automated_manifest["trace_file"] = trace_file
            automated_manifest["trace_sha256"] = sha256_text("stale trace")
            manifests_dir = write_manifest_file(root, automated_manifest)

            errors = validate_scholar_grade_run_manifests(
                fixture_path,
                outputs_dir,
                manifests_dir,
                root,
                require_live_captures=True,
            )

            self.assertIn("unsupported-causal-claim: manifest trace_sha256 does not match trace file", errors)
            self.assertIn(
                "unsupported-causal-claim: trace fixture_id must match manifest fixture_id 'unsupported-causal-claim'",
                errors,
            )
            self.assertIn(
                "unsupported-causal-claim: trace skill must match manifest skill 'methodology-source-auditor'",
                errors,
            )
            self.assertIn(
                "unsupported-causal-claim: trace selected_skill must match fixture skill 'methodology-source-auditor'",
                errors,
            )
            self.assertIn("unsupported-causal-claim: trace skill_invoked must be true", errors)
            self.assertIn("unsupported-causal-claim: trace tool_call_count must be a non-negative integer", errors)

    def test_automated_live_manifest_accepts_matching_trace(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            skill_text = "skill text"
            source_packet_text = "\n".join(
                [
                    "# Synthetic source packet",
                    "",
                    "Source basis: controlled notes only.",
                    "Visible method details: none.",
                ]
            )
            output_text = "\n".join(
                [
                    "Source basis: controlled packet.",
                    "Claim/evidence fit: descriptive support only.",
                    "Expected decision: Cannot support.",
                    "No method details are available.",
                    "Next action: inspect method details before relying on the claim.",
                ]
            )
            write_source_packet(root)
            write_skill_file(root, text=skill_text)
            fixture_path = write_fixture_file(root, fixture_document(fixture()))
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (outputs_dir / "unsupported-causal-claim.md").write_text(output_text, encoding="utf-8")
            trace_payload = {
                "schema_version": "scholar-grade-trace-v1",
                "fixture_id": "unsupported-causal-claim",
                "skill": "methodology-source-auditor",
                "model": "gpt-5.4",
                "selected_skill": "methodology-source-auditor",
                "tool_permissions": "none",
                "network_permissions": "none",
                "skill_invoked": True,
                "source_packet_supplied": True,
                "output_captured": True,
                "tool_call_count": 0,
                "command_count": 0,
                "token_usage": {
                    "input_tokens": 0,
                    "output_tokens": 0,
                },
            }
            trace_file = write_trace_file(root, "unsupported-causal-claim", trace_payload)
            automated_manifest = manifest(
                output_text=output_text,
                source_packet_text=source_packet_text,
                skill_text=skill_text,
            )
            automated_manifest["capture_mode"] = "automated-live-capture"
            automated_manifest["interface"] = "codex-json-trace"
            automated_manifest["model"] = "gpt-5.4"
            automated_manifest["trace_file"] = trace_file
            automated_manifest["trace_sha256"] = sha256_text(json.dumps(trace_payload))
            manifests_dir = write_manifest_file(root, automated_manifest)
            write_prompt_file(root)

            self.assertEqual(
                validate_scholar_grade_run_manifests(
                    fixture_path,
                    outputs_dir,
                    manifests_dir,
                    root,
                    require_live_captures=True,
                ),
                [],
            )

    def test_run_manifest_rejects_missing_or_stale_structured_result(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source_packet_text = "\n".join(
                [
                    "# Synthetic source packet",
                    "",
                    "Source basis: controlled notes only.",
                    "Visible method details: none.",
                ]
            )
            output_text = "\n".join(
                [
                    "Source basis: controlled packet.",
                    "Claim/evidence fit: descriptive support only.",
                    "Expected decision: Cannot support.",
                    "No method details are available.",
                    "Next action: inspect method details before relying on the claim.",
                ]
            )
            write_source_packet(root)
            write_skill_file(root)
            fixture_path = write_fixture_file(root, fixture_document(fixture()))
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (outputs_dir / "unsupported-causal-claim.md").write_text(output_text, encoding="utf-8")
            stale_manifest = manifest(
                output_text="stale output",
                source_packet_text=source_packet_text,
            )
            stale_manifest["structured_result"] = {
                "decision": "Can support",
                "source_access_level": "controlled-packet",
                "external_lookup_used": True,
                "private_material_submitted": False,
                "hard_fail_triggered": False,
                "next_action_count": 2,
            }
            manifests_dir = write_manifest_file(root, stale_manifest)

            errors = validate_scholar_grade_run_manifests(fixture_path, outputs_dir, manifests_dir, root)

            self.assertIn("unsupported-causal-claim: manifest output_sha256 does not match output file", errors)
            self.assertIn(
                "unsupported-causal-claim: structured_result.decision must match expected_decision 'Cannot support'",
                errors,
            )
            self.assertIn("unsupported-causal-claim: structured_result.external_lookup_used must be false", errors)
            self.assertIn("unsupported-causal-claim: structured_result.next_action_count must be 1", errors)

    def test_review_score_validates_fixture_rubric_and_minimum_score(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_source_packet(root)
            fixture_path = write_fixture_file(root, fixture_document(fixture()))
            scores_dir = write_score_file(root, score())

            self.assertEqual(validate_scholar_grade_review_scores(fixture_path, scores_dir), [])

    def test_review_score_rejects_stale_reviewed_output_hash(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_source_packet(root)
            fixture_path = write_fixture_file(root, fixture_document(fixture()))
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            output_text = "Source basis.\nClaim/evidence fit.\nCannot support.\nNo method details are available.\nNext action.\n"
            (outputs_dir / "unsupported-causal-claim.md").write_text(output_text, encoding="utf-8")
            scores_dir = write_score_file(
                root,
                score(reviewed_output_sha256=sha256_text("stale reviewed output")),
            )

            errors = validate_scholar_grade_review_scores(fixture_path, scores_dir, outputs_dir)

            self.assertIn(
                "unsupported-causal-claim: score reviewed_output_sha256 does not match output file",
                errors,
            )

    def test_review_score_rejects_missing_and_placeholder_dimension_rationales(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_source_packet(root)
            fixture_path = write_fixture_file(root, fixture_document(fixture()))
            invalid_score = score(
                dimension_rationales={
                    "source-basis clarity": "Names the controlled packet and missing method detail.",
                    "claim/evidence fit": "TODO_RATIONALE",
                }
            )
            scores_dir = write_score_file(root, invalid_score)

            errors = validate_scholar_grade_review_scores(fixture_path, scores_dir)

            self.assertIn(
                "unsupported-causal-claim: score dimension_rationales must match fixture rubric_dimensions",
                errors,
            )
            self.assertIn(
                "unsupported-causal-claim: score dimension_rationales for 'claim/evidence fit' must not be a TODO placeholder",
                errors,
            )

    def test_review_score_requires_evidence_notes_and_answer_key_findings(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_source_packet(root)
            fixture_path = write_fixture_file(root, fixture_document(fixture()))
            incomplete_score = score()
            incomplete_score.pop("evidence_notes")
            incomplete_score.pop("answer_key_findings")
            scores_dir = write_score_file(root, incomplete_score)

            errors = validate_scholar_grade_review_scores(fixture_path, scores_dir)

            self.assertIn("unsupported-causal-claim: score missing key 'evidence_notes'", errors)
            self.assertIn("unsupported-causal-claim: score missing key 'answer_key_findings'", errors)

    def test_review_score_rejects_missing_dimension_low_average_and_hard_fail(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_source_packet(root)
            fixture_path = write_fixture_file(root, fixture_document(fixture()))
            scores_dir = write_score_file(
                root,
                score(
                    dimensions={
                        "source-basis clarity": 5,
                        "claim/evidence fit": 2,
                    },
                    hard_fail_triggered=True,
                ),
            )

            errors = validate_scholar_grade_review_scores(fixture_path, scores_dir)

            self.assertIn("unsupported-causal-claim: score hard_fail_triggered must be false", errors)
            self.assertIn(
                "unsupported-causal-claim: score dimensions must match fixture rubric_dimensions",
                errors,
            )
            self.assertIn("unsupported-causal-claim: average score 3.50 is below minimum_score 4", errors)

    def test_review_score_rejects_single_weak_dimension_even_when_average_passes(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_source_packet(root)
            fixture_path = write_fixture_file(root, fixture_document(fixture()))
            scores_dir = write_score_file(
                root,
                score(
                    dimensions={
                        "source-basis clarity": 5,
                        "claim/evidence fit": 5,
                        "fabrication avoidance": 2,
                        "uncertainty visibility": 5,
                    },
                ),
            )

            errors = validate_scholar_grade_review_scores(fixture_path, scores_dir)

            self.assertIn(
                "unsupported-causal-claim: score for dimension 'fabrication avoidance' 2 is below minimum_score 4",
                errors,
            )

    def test_review_score_rejects_template_placeholder_metadata(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_source_packet(root)
            fixture_path = write_fixture_file(root, fixture_document(fixture()))
            placeholder_score = score()
            placeholder_score["reviewer"] = "TODO_REVIEWER"
            placeholder_score["rationale"] = "TODO_RATIONALE"
            scores_dir = write_score_file(root, placeholder_score)

            errors = validate_scholar_grade_review_scores(fixture_path, scores_dir)

            self.assertIn("unsupported-causal-claim: score reviewer must not be a TODO placeholder", errors)
            self.assertIn("unsupported-causal-claim: score rationale must not be a TODO placeholder", errors)

    def test_review_score_rejects_non_calendar_date(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_source_packet(root)
            fixture_path = write_fixture_file(root, fixture_document(fixture()))
            invalid_date_score = score()
            invalid_date_score["date"] = "2026-99-99"
            scores_dir = write_score_file(root, invalid_date_score)

            errors = validate_scholar_grade_review_scores(fixture_path, scores_dir)

            self.assertIn("unsupported-causal-claim: score date must be a real YYYY-MM-DD date", errors)

    def test_private_no_external_manifest_rejects_network_and_tool_permissions(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            skill_text = "skill text"
            source_packet_text = "\n".join(
                [
                    "# Synthetic source packet",
                    "",
                    "Source basis: controlled notes only.",
                    "Visible method details: none.",
                ]
            )
            output_text = "\n".join(
                [
                    "Source basis: controlled packet.",
                    "Claim/evidence fit: descriptive support only.",
                    "Expected decision: Do not search private text externally.",
                    "No method details are available.",
                    "Next action: inspect method details before relying on the claim.",
                ]
            )
            write_source_packet(root)
            write_skill_file(root, text=skill_text)
            private_fixture = fixture()
            private_fixture["source_access_level"] = "private-no-external"
            private_fixture["expected_decision"] = "Do not search private text externally"
            fixture_path = write_fixture_file(root, fixture_document(private_fixture))
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (outputs_dir / "unsupported-causal-claim.md").write_text(output_text, encoding="utf-8")
            unsafe_manifest = manifest(
                output_text=output_text,
                source_packet_text=source_packet_text,
                skill_text=skill_text,
            )
            unsafe_manifest["network_permissions"] = "allow-network"
            unsafe_manifest["tool_permissions"] = "web"
            manifests_dir = write_manifest_file(root, unsafe_manifest)

            errors = validate_scholar_grade_run_manifests(fixture_path, outputs_dir, manifests_dir, root)

            self.assertIn(
                "unsupported-causal-claim: private-no-external manifest network_permissions must be 'none'",
                errors,
            )
            self.assertIn(
                "unsupported-causal-claim: private-no-external manifest tool_permissions must be 'none' or 'local-only'",
                errors,
            )

    def test_negated_global_hard_fail_phrase_does_not_fail_output(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_source_packet(root)
            release_fixture = fixture()
            release_fixture["expected_decision"] = "Hold release"
            release_fixture["required_output_markers"] = ["Source basis", "Release verdict", "Next action"]
            release_fixture["required_uncertainties"] = ["No method details are available"]
            release_fixture["disallowed_claims"] = ["legal clearance granted"]
            release_fixture["hard_fail_patterns"] = ["legal clearance granted"]
            fixture_path = write_fixture_file(root, fixture_document(release_fixture))
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (outputs_dir / "unsupported-causal-claim.md").write_text(
                "\n".join(
                    [
                        "Source basis: controlled packet.",
                        "Release verdict: Hold release.",
                        "No method details are available.",
                        "This is not safe to publish until permissions are checked.",
                        "Next action: inspect method details.",
                    ]
                ),
                encoding="utf-8",
            )

            errors = validate_scholar_grade_outputs(fixture_path, outputs_dir)

            self.assertNotIn(
                "unsupported-causal-claim: matches global hard fail pattern 'safe to publish'",
                errors,
            )

    def test_shipped_fixtures_corpora_and_outputs_are_in_lockstep(self) -> None:
        fixture_path = ROOT / "tests" / "skill_evals" / "scholar_grade" / "fixtures.json"
        outputs_dir = ROOT / "tests" / "skill_evals" / "scholar_grade" / "outputs"
        corpora_dir = ROOT / "tests" / "skill_evals" / "scholar_grade" / "corpora"
        manifests_dir = ROOT / "tests" / "skill_evals" / "scholar_grade" / "manifests"
        scores_dir = ROOT / "tests" / "skill_evals" / "scholar_grade" / "scores"
        document = read_json_object(fixture_path)
        fixture_ids = {str(fixture["id"]) for fixture in document["fixtures"]}
        corpus_ids = {path.name for path in corpora_dir.iterdir() if path.is_dir()}
        output_ids = {path.stem for path in outputs_dir.glob("*.md")}
        manifest_ids = {path.stem for path in manifests_dir.glob("*.json")}
        score_ids = {path.stem for path in scores_dir.glob("*.json")}

        self.assertEqual(corpus_ids, fixture_ids)
        self.assertEqual(output_ids, fixture_ids)
        self.assertEqual(manifest_ids, fixture_ids)
        self.assertEqual(score_ids, fixture_ids)
        for fixture_id in fixture_ids:
            corpus_dir = corpora_dir / fixture_id
            self.assertTrue((corpus_dir / "source-packet.md").exists())
            self.assertTrue((corpus_dir / "answer-key.md").exists())
            self.assertTrue((corpus_dir / "answer-key.json").exists())
            self.assertNotIn(
                "## Ground truth for evaluation",
                (corpus_dir / "source-packet.md").read_text(encoding="utf-8"),
            )

    def test_shipped_scholar_grade_fixture_set_validates_cleanly(self) -> None:
        fixture_path = ROOT / "tests" / "skill_evals" / "scholar_grade" / "fixtures.json"
        outputs_dir = ROOT / "tests" / "skill_evals" / "scholar_grade" / "outputs"
        manifests_dir = ROOT / "tests" / "skill_evals" / "scholar_grade" / "manifests"
        scores_dir = ROOT / "tests" / "skill_evals" / "scholar_grade" / "scores"

        self.assertEqual(validate_scholar_grade_outputs(fixture_path, outputs_dir), [])
        self.assertEqual(validate_scholar_grade_run_manifests(fixture_path, outputs_dir, manifests_dir, ROOT), [])
        self.assertEqual(validate_scholar_grade_review_scores(fixture_path, scores_dir, outputs_dir), [])

    def test_shipped_resource_basis_registry_is_present(self) -> None:
        registry_path = ROOT / "tests" / "skill_evals" / "scholar_grade" / "resource-basis.json"

        self.assertTrue(registry_path.exists())

    def test_shipped_fixture_set_covers_source_access_modes(self) -> None:
        fixture_path = ROOT / "tests" / "skill_evals" / "scholar_grade" / "fixtures.json"
        document = read_json_object(fixture_path)
        source_access_levels = {str(fixture["source_access_level"]) for fixture in document["fixtures"]}

        self.assertTrue(
            {
                "controlled-packet",
                "prompt-only",
                "public-metadata-only",
                "external-lookup-consented",
                "private-no-external",
            }
            <= source_access_levels
        )

    def test_shipped_fixture_set_covers_core_ai_research_failure_modes(self) -> None:
        fixture_path = ROOT / "tests" / "skill_evals" / "scholar_grade" / "fixtures.json"
        document = read_json_object(fixture_path)
        fixture_ids = {str(fixture["id"]) for fixture in document["fixtures"]}

        expected_failure_mode_fixtures = {
            "implementation-bug-without-clean-run",
            "hallucinated-result-without-run-log",
            "methodology-fabrication-run-config",
            "shortcut-literature-review-abstract-only",
            "frame-lock-preferred-thesis",
        }

        self.assertTrue(expected_failure_mode_fixtures <= fixture_ids)

    def test_shipped_fixture_set_includes_positive_supportability_case(self) -> None:
        fixture_path = ROOT / "tests" / "skill_evals" / "scholar_grade" / "fixtures.json"
        document = read_json_object(fixture_path)
        fixture_ids = {str(fixture["id"]) for fixture in document["fixtures"]}

        self.assertIn("bounded-descriptive-claim-supported", fixture_ids)

    def test_shipped_fixture_set_requires_source_anchors_and_semantic_fail_patterns(self) -> None:
        fixture_path = ROOT / "tests" / "skill_evals" / "scholar_grade" / "fixtures.json"
        document = read_json_object(fixture_path)

        self.assertEqual(
            [
                str(fixture["id"])
                for fixture in document["fixtures"]
                if not string_list(fixture.get("required_source_anchors"))
            ],
            [],
        )
        self.assertEqual(
            [
                str(fixture["id"])
                for fixture in document["fixtures"]
                if not string_list(fixture.get("semantic_fail_patterns"))
            ],
            [],
        )

    def test_shipped_mediocre_control_fails_review_score_gate(self) -> None:
        fixture_path = ROOT / "tests" / "skill_evals" / "scholar_grade" / "fixtures.json"
        control_root = ROOT / "tests" / "skill_evals" / "scholar_grade" / "mediocre_controls"
        outputs_dir = control_root / "outputs"
        manifests_dir = control_root / "manifests"
        scores_dir = control_root / "scores"

        report = build_scholar_grade_report(
            fixture_path,
            outputs_dir,
            manifests_dir,
            scores_dir,
            ROOT,
            fixture_ids=["unsupported-causal-claim"],
        )
        self.assertEqual(report["outputs"]["validation_errors"], [])
        self.assertEqual(report["manifests"]["validation_errors"], [])
        score_errors = report["scores"]["validation_errors"]

        self.assertIn(
            "unsupported-causal-claim: score for dimension 'source-basis clarity' 3 is below minimum_score 4",
            score_errors,
        )


if __name__ == "__main__":
    unittest.main()
