"""Consistency checks for manuscript-preparation skill instructions and docs."""
from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class TestManuscriptPreparationDocs(unittest.TestCase):
    def assert_file_contains_all(self, relative_path: str, snippets: list[str]) -> None:
        path = ROOT / relative_path
        text = path.read_text(encoding="utf-8")
        for snippet in snippets:
            with self.subTest(path=relative_path, snippet=snippet):
                self.assertIn(snippet, text)

    def test_orchestrator_raw_materials_lane_is_documented(self) -> None:
        self.assert_file_contains_all(
            "skills/research-book-orchestrator/SKILL.md",
            [
                "## Raw materials to manuscript lane",
                "A raw-materials bundle is an inventory, not source verification.",
                "Planned searches are not completed searches.",
                "Do not skip directly to drafting",
            ],
        )
        self.assert_file_contains_all(
            "skills/research-book-orchestrator/assets/workflow-plan-template.md",
            [
                "## Raw materials inventory",
                "## Stop conditions",
                "Hold if source discovery is only planned",
                "Hold if refinement removes unresolved risks",
            ],
        )

    def test_outline_derived_source_planning_boundaries_are_documented(self) -> None:
        self.assert_file_contains_all(
            "skills/systematic-source-discovery/SKILL.md",
            [
                "## Outline-derived source discovery",
                "Mark the result as `planned_search`",
                "A section search task is not evidence that sources exist",
            ],
        )
        self.assert_file_contains_all(
            "skills/chapter-architecture/SKILL.md",
            [
                "create an outline-derived search task",
                "Keep planned source types separate from verified sources",
            ],
        )

    def test_visual_planning_and_clearance_boundaries_are_documented(self) -> None:
        self.assert_file_contains_all(
            "skills/figure-table-integrity-auditor/SKILL.md",
            [
                "## Visual evidence planning",
                "A visual evidence plan is not figure/table clearance.",
                "Do not mark an object ready for manuscript reliance",
            ],
        )
        self.assert_file_contains_all(
            "docs/user/WORKFLOW_PLAYBOOK.md",
            [
                "Use a visual evidence plan before making or accepting a figure",
                "Run `figure-table-integrity-auditor` again after the actual object exists.",
            ],
        )

    def test_review_refinement_risk_preservation_is_documented(self) -> None:
        self.assert_file_contains_all(
            "skills/counterargument-peer-review/SKILL.md",
            [
                "## Review loop handoff",
                "include a short repair queue",
                "Do not present critique resolution as completed",
            ],
        )
        self.assert_file_contains_all(
            "skills/scholarly-prose-editor/SKILL.md",
            [
                "preserve claim strength, source-access labels, unresolved risks, and claim IDs",
                "mark the evidence problem instead of making the prose sound more confident",
            ],
        )
        self.assert_file_contains_all(
            "skills/manuscript-continuity-editor/SKILL.md",
            [
                "check whether earlier critique, claim-ledger, traceability, citation, figure/table, or integrity-gate risks were preserved",
                "Treat silent risk removal as a continuity problem.",
            ],
        )

    def test_routing_and_user_docs_include_new_lane(self) -> None:
        self.assert_file_contains_all(
            "MODE_REGISTRY.md",
            [
                "`manuscript-preparation`",
                "raw-materials inventory and staged manuscript workflow plan",
            ],
        )
        self.assert_file_contains_all(
            "docs/policy/ROUTING_MATRIX.md",
            [
                "Raw materials such as idea summaries",
                "outline-derived source task",
                "Planned or generated visual",
                "Review findings need a repair queue",
            ],
        )
        self.assert_file_contains_all(
            "docs/user/RAW_MATERIALS_TO_MANUSCRIPT.md",
            [
                "A planned search is not a completed search.",
                "A generated visual is not cleared evidence",
                "revision removes claim IDs, unresolved risks, or source limits",
            ],
        )
        self.assert_file_contains_all(
            "docs/templates/RAW_MATERIALS_BUNDLE_TEMPLATE.md",
            [
                "This bundle is an inventory.",
                "Do not paste private manuscripts",
                "Process passport, if this bundle is saved or handed downstream",
            ],
        )

    def test_integrity_gate_manuscript_prefilter_is_documented(self) -> None:
        self.assert_file_contains_all(
            "skills/scholarly-integrity-gate/SKILL.md",
            [
                "manuscript-preparation workflow: raw materials, outline, source plan, generated or revised prose, visuals, and review-loop artifacts",
                "broken claim lineage",
                "A manuscript-preparation workflow must hold when review, refinement, or drafting removes source-access labels",
                "visual/table provenance gaps without a visible verification step",
            ],
        )

    def test_architecture_documents_visual_evidence_planning_gate(self) -> None:
        self.assert_file_contains_all(
            "docs/reference/ARCHITECTURE.md",
            [
                "The raw-materials-to-manuscript lane starts when a user has notes, logs, source notes, outline fragments, tables, figures, or draft prose.",
                "Visual evidence planning gate",
                "Planned visuals, generated visuals, or draft tables are treated as evidence before data, source basis, caption limits, rights, and human review are visible",
                "Prevents planned or generated visuals from becoming unsupported manuscript evidence",
            ],
        )

    def test_skill_index_preserves_new_lane_boundaries(self) -> None:
        self.assert_file_contains_all(
            "docs/user/SKILL_INDEX.md",
            [
                "Use for raw-materials-to-manuscript planning when idea summaries, research logs, source notes, outlines, draft visuals, or draft fragments need a staged path toward manuscript work.",
                "Preserve source-access labels, privacy limits, planned-search status, visual-plan limits, and process-passport unresolved risks.",
                "Use for outline-derived source tasks from chapter outlines or manuscript plans, with planned searches labeled `planned_search` until a completed search log or source packet exists.",
                "planning does not clear figures or tables for evidentiary, citation, or rights use.",
                "Use as a manuscript-preparation prefilter when raw materials, review loops, or generated visuals may have lost source labels",
            ],
        )


if __name__ == "__main__":
    unittest.main()
