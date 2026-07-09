# Manuscript Preparation Test Coverage Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add focused tests for the uncommitted manuscript-preparation lane, outline-derived source planning, visual evidence planning, and review/refinement boundary changes.

**Architecture:** Keep this test-only. Add deterministic assertions around the shipped research-behavior fixtures, add a focused scholar-grade fixture family test, and add a lightweight documentation/instruction consistency test for the secondary skill changes that do not have their own fixture yet. Do not change schemas or production behavior.

**Tech Stack:** Python `unittest`, JSON fixture files, Markdown skill instructions, existing eval harnesses.

---

## Source Basis

- Repository state fetched with `git fetch --all --prune`.
- Current branch during planning: `main`.
- Relevant baseline command passed: `python3 -m unittest scripts.test_research_behavior_fixtures tests.skill_evals.test_skill_eval_coverage tests.skill_evals.scholar_grade.test_scholar_grade_eval_harness`.
- Current uncommitted changes add manuscript-preparation behavior to skill instructions, docs, research-behavior fixtures, scholar-grade fixtures, corpora, prompts, outputs, manifests, and scores.

## Assumptions

- This pass adds tests only. It should not change skill behavior, fixture semantics, schema contracts, or generated outputs.
- Backward compatibility is required. Do not add a `raw_materials_bundle` schema type in this test pass.
- Treat `main` as the intended branch only because no other target branch was supplied. If that is wrong, switch to the intended branch before executing.
- Caveman Ultra is not appropriate for this work because the plan depends on evidence, tradeoffs, and test coverage mapping.

## File Structure

Modify:

- `scripts/test_research_behavior_fixtures.py`: add direct assertions that the three new research-behavior fixtures carry the required route, marker, and forbidden-claim boundaries.

Create:

- `tests/skill_evals/scholar_grade/test_manuscript_preparation_fixtures.py`: validate the three new scholar-grade fixtures and their artifact files as one fixture family.
- `tests/skill_evals/test_manuscript_preparation_docs.py`: assert the secondary instruction and docs changes remain present and aligned.

No production files should change.

---

### Task 1: Add Research-Behavior Fixture Family Assertions

**Files:**
- Modify: `scripts/test_research_behavior_fixtures.py`
- Test: `python3 -m unittest scripts.test_research_behavior_fixtures.TestResearchBehaviorFixtures.test_shipped_manuscript_preparation_fixtures_cover_required_boundaries`

- [ ] **Step 1: Add the fixture-family constant**

In `scripts/test_research_behavior_fixtures.py`, add this constant after `CERTIFICATION_BOUNDARY_ADVERSARIAL_FIXTURES`:

```python
MANUSCRIPT_PREPARATION_FIXTURES = {
    "raw-materials-to-manuscript-route": {
        "expected_route": "research-book-orchestrator",
        "required_markers": {
            "raw materials",
            "Source basis",
            "What I can verify",
            "What remains uncertain",
            "User verification needed",
            "planned search",
            "human checkpoint",
        },
        "forbidden_claims": {
            "submission-ready manuscript",
            "sources verified",
            "figures cleared",
            "human verification complete",
        },
    },
    "outline-derived-source-plan-boundary": {
        "expected_route": "systematic-source-discovery",
        "required_markers": {
            "outline-derived",
            "planned_search",
            "Source basis",
            "Search status",
            "What I can verify",
            "What remains uncertain",
            "User verification needed",
        },
        "forbidden_claims": {
            "database searched",
            "completed search",
            "field coverage verified",
        },
    },
    "visual-evidence-plan-not-clearance": {
        "expected_route": "figure-table-integrity-auditor",
        "required_markers": {
            "visual evidence plan",
            "not figure/table clearance",
            "data provenance",
            "caption",
            "rights",
            "human review",
        },
        "forbidden_claims": {
            "ready for manuscript reliance",
            "figure verified",
            "rights cleared",
        },
    },
}
```

- [ ] **Step 2: Add the shipped-fixture test**

In `TestResearchBehaviorFixtures`, add this method after `test_shipped_certification_boundary_fixtures_cover_required_boundaries`:

```python
    def test_shipped_manuscript_preparation_fixtures_cover_required_boundaries(self) -> None:
        document = json.loads(SHIPPED_RESEARCH_BEHAVIOR_FIXTURES.read_text(encoding="utf-8"))
        fixtures_by_id = {fixture["id"]: fixture for fixture in document["fixtures"]}

        for fixture_id, expected in MANUSCRIPT_PREPARATION_FIXTURES.items():
            with self.subTest(fixture_id=fixture_id):
                fixture_payload = fixtures_by_id[fixture_id]
                required_markers = set(fixture_payload["required_output_markers"])
                forbidden_claims = set(fixture_payload["forbidden_claims"])

                self.assertEqual(fixture_payload["expected_route"], expected["expected_route"])
                self.assertTrue(
                    expected["required_markers"].issubset(required_markers),
                    msg=f"{fixture_id} is missing required markers: "
                    f"{sorted(expected['required_markers'] - required_markers)}",
                )
                self.assertTrue(
                    expected["forbidden_claims"].issubset(forbidden_claims),
                    msg=f"{fixture_id} is missing forbidden claims: "
                    f"{sorted(expected['forbidden_claims'] - forbidden_claims)}",
                )
```

- [ ] **Step 3: Run the focused test**

Run:

```bash
python3 -m unittest scripts.test_research_behavior_fixtures.TestResearchBehaviorFixtures.test_shipped_manuscript_preparation_fixtures_cover_required_boundaries
```

Expected: `OK`.

---

### Task 2: Add Scholar-Grade Fixture Family Tests

**Files:**
- Create: `tests/skill_evals/scholar_grade/test_manuscript_preparation_fixtures.py`
- Test: `python3 -m unittest tests.skill_evals.scholar_grade.test_manuscript_preparation_fixtures`

- [ ] **Step 1: Create the scholar-grade fixture test file**

Create `tests/skill_evals/scholar_grade/test_manuscript_preparation_fixtures.py` with this content:

```python
"""Focused tests for manuscript-preparation scholar-grade fixtures."""
from __future__ import annotations

import json
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
FIXTURES_PATH = ROOT / "tests" / "skill_evals" / "scholar_grade" / "fixtures.json"
PROMPTS_DIR = ROOT / "tests" / "skill_evals" / "scholar_grade" / "prompts"
OUTPUTS_DIR = ROOT / "tests" / "skill_evals" / "scholar_grade" / "outputs"
MANIFESTS_DIR = ROOT / "tests" / "skill_evals" / "scholar_grade" / "manifests"
SCORES_DIR = ROOT / "tests" / "skill_evals" / "scholar_grade" / "scores"
CORPORA_DIR = ROOT / "tests" / "skill_evals" / "scholar_grade" / "corpora"


MANUSCRIPT_PREPARATION_FIXTURES = {
    "raw-materials-manuscript-boundary": {
        "skill": "research-book-orchestrator",
        "expected_decision": "Hold before drafting",
        "required_markers": {
            "Source basis",
            "raw materials",
            "What I can verify",
            "What remains uncertain",
            "User verification needed",
            "human checkpoint",
        },
        "required_source_anchors": {
            "three city planning reports",
            "no full citations or page locators",
            "No dataset is supplied",
        },
        "required_uncertainties": {
            "source-claim fit is not verified",
            "figure data provenance is missing",
            "human verification is needed",
        },
        "disallowed_claims": {
            "the reports support the draft claim",
            "the draft figure is ready",
            "the manuscript is submission-ready",
        },
    },
    "outline-derived-search-boundary": {
        "skill": "systematic-source-discovery",
        "expected_decision": "planned_search",
        "required_markers": {
            "Search status",
            "planned_search",
            "outline-derived",
            "What remains uncertain",
            "User verification needed",
        },
        "required_source_anchors": {
            "Maintenance labor as adaptation infrastructure",
            "one city",
            "Opposing literature",
        },
        "required_uncertainties": {
            "No search logs are available",
            "No candidate sources are available",
            "Corpus coverage is not verified",
        },
        "disallowed_claims": {
            "the literature was searched",
            "field consensus is visible",
            "candidate sources were found",
        },
    },
    "visual-plan-not-clearance": {
        "skill": "figure-table-integrity-auditor",
        "expected_decision": "Not cleared",
        "required_markers": {
            "visual evidence plan",
            "not figure/table clearance",
            "data provenance",
            "caption",
            "rights",
            "human review",
        },
        "required_source_anchors": {
            "No data file is supplied",
            "No transformation notes are supplied",
            "No rights or source-file status is supplied",
        },
        "required_uncertainties": {
            "Data provenance is missing",
            "Transformation logic is missing",
            "Rights status is missing",
            "Human review is needed",
        },
        "disallowed_claims": {
            "the chart is cleared for manuscript reliance",
            "numbers can be inferred",
            "rights are cleared",
        },
    },
}


def read_json_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} root must be an object")
    return payload


class TestManuscriptPreparationScholarGradeFixtures(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        document = read_json_object(FIXTURES_PATH)
        cls.fixtures_by_id = {
            fixture["id"]: fixture
            for fixture in document["fixtures"]
            if isinstance(fixture, dict)
        }

    def test_fixture_family_has_required_boundaries(self) -> None:
        for fixture_id, expected in MANUSCRIPT_PREPARATION_FIXTURES.items():
            with self.subTest(fixture_id=fixture_id):
                fixture = self.fixtures_by_id[fixture_id]

                self.assertEqual(fixture["skill"], expected["skill"])
                self.assertEqual(fixture["expected_decision"], expected["expected_decision"])
                self.assertEqual(fixture["source_access_level"], "controlled-packet")
                self.assertGreaterEqual(fixture["minimum_score"], 4)
                self.assertIs(fixture["human_review_required"], True)
                self.assertIn("paperorchestra", fixture["resource_basis"])
                self.assertTrue(
                    expected["required_markers"].issubset(set(fixture["required_output_markers"]))
                )
                self.assertTrue(
                    expected["required_source_anchors"].issubset(set(fixture["required_source_anchors"]))
                )
                self.assertTrue(
                    expected["required_uncertainties"].issubset(set(fixture["required_uncertainties"]))
                )
                self.assertTrue(
                    expected["disallowed_claims"].issubset(set(fixture["disallowed_claims"]))
                )
                self.assertTrue(fixture["hard_fail_patterns"])
                self.assertTrue(fixture["semantic_fail_patterns"])
                self.assertEqual(set(fixture["score_anchors"]), set(fixture["rubric_dimensions"]))

    def test_fixture_family_artifacts_are_present_and_aligned(self) -> None:
        for fixture_id, expected in MANUSCRIPT_PREPARATION_FIXTURES.items():
            with self.subTest(fixture_id=fixture_id):
                prompt_path = PROMPTS_DIR / f"{fixture_id}.md"
                output_path = OUTPUTS_DIR / f"{fixture_id}.md"
                manifest_path = MANIFESTS_DIR / f"{fixture_id}.json"
                score_path = SCORES_DIR / f"{fixture_id}.json"
                corpus_path = CORPORA_DIR / fixture_id

                self.assertTrue(prompt_path.is_file(), msg=f"missing prompt for {fixture_id}")
                self.assertTrue(output_path.is_file(), msg=f"missing output for {fixture_id}")
                self.assertTrue(manifest_path.is_file(), msg=f"missing manifest for {fixture_id}")
                self.assertTrue(score_path.is_file(), msg=f"missing score for {fixture_id}")
                self.assertTrue((corpus_path / "source-packet.md").is_file())
                self.assertTrue((corpus_path / "answer-key.md").is_file())
                self.assertTrue((corpus_path / "answer-key.json").is_file())

                manifest = read_json_object(manifest_path)
                structured_result = manifest["structured_result"]
                self.assertEqual(manifest["fixture_id"], fixture_id)
                self.assertEqual(manifest["skill"], expected["skill"])
                self.assertEqual(manifest["capture_mode"], "deterministic-reference")
                self.assertIs(manifest["external_lookup_permitted"], False)
                self.assertEqual(structured_result["decision"], expected["expected_decision"])
                self.assertEqual(structured_result["source_access_level"], "controlled-packet")
                self.assertIs(structured_result["external_lookup_used"], False)
                self.assertIs(structured_result["private_material_submitted"], False)
                self.assertIs(structured_result["hard_fail_triggered"], False)

                answer_key = read_json_object(corpus_path / "answer-key.json")
                self.assertEqual(answer_key["schema_version"], "scholar-grade-answer-key-v1")
                self.assertEqual(answer_key["fixture_id"], fixture_id)
                self.assertTrue(answer_key["must_reject"])
                self.assertTrue(answer_key["must_remain_uncertain"])

                score = read_json_object(score_path)
                self.assertEqual(score["fixture_id"], fixture_id)
                self.assertIs(score["hard_fail_triggered"], False)
                self.assertEqual(
                    set(score["dimension_scores"]),
                    set(self.fixtures_by_id[fixture_id]["rubric_dimensions"]),
                )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the focused test**

Run:

```bash
python3 -m unittest tests.skill_evals.scholar_grade.test_manuscript_preparation_fixtures
```

Expected: `OK`.

---

### Task 3: Add Instruction and Docs Consistency Tests

**Files:**
- Create: `tests/skill_evals/test_manuscript_preparation_docs.py`
- Test: `python3 -m unittest tests.skill_evals.test_manuscript_preparation_docs`

- [ ] **Step 1: Create the docs consistency test**

Create `tests/skill_evals/test_manuscript_preparation_docs.py` with this content:

```python
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


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the focused test**

Run:

```bash
python3 -m unittest tests.skill_evals.test_manuscript_preparation_docs
```

Expected: `OK`.

---

### Task 4: Run the Regression Set

**Files:**
- No file changes.
- Test: existing unit and validation commands.

- [ ] **Step 1: Run the relevant unit tests**

Run:

```bash
python3 -m unittest scripts.test_research_behavior_fixtures tests.skill_evals.test_skill_eval_coverage tests.skill_evals.test_manuscript_preparation_docs tests.skill_evals.scholar_grade.test_scholar_grade_eval_harness tests.skill_evals.scholar_grade.test_manuscript_preparation_fixtures
```

Expected: all tests pass.

- [ ] **Step 2: Run plugin validation**

Run:

```bash
python3 scripts/validate_plugin.py .
```

Expected: exits with status 0.

- [ ] **Step 3: Run the research-behavior fixture checker**

Run:

```bash
python3 scripts/check_research_behavior_fixtures.py --fixtures tests/skill_evals/research_behavior/fixtures.json --outputs-dir tests/skill_evals/research_behavior/outputs --traces-dir tests/skill_evals/research_behavior/traces
```

Expected: exits with status 0.

- [ ] **Step 4: Run the scholar-grade harness on recorded outputs**

Run:

```bash
python3 tests/skill_evals/scholar_grade/scholar_grade_eval_harness.py --fixtures tests/skill_evals/scholar_grade/fixtures.json --outputs-dir tests/skill_evals/scholar_grade/outputs --manifests-dir tests/skill_evals/scholar_grade/manifests --scores-dir tests/skill_evals/scholar_grade/scores --quiet
```

Expected: exits with status 0.

- [ ] **Step 5: Run the full package check if time allows**

Run:

```bash
python3 scripts/run_package_checks.py --scope full
```

Expected: exits with status 0. If this fails in unrelated live-calibration or environment-sensitive areas, record the failing command and rerun the focused commands above before changing code.

## Self-Review

- The plan covers the three new research-behavior fixtures added in the current diff.
- The plan covers the three new scholar-grade fixtures, their corpora, prompts, outputs, manifests, scores, and hidden answer-key files.
- The plan covers the secondary skill and documentation changes for raw-materials routing, outline-derived source planning, visual evidence planning, review/refinement repair queues, prose risk preservation, continuity checks, and integrity-gate holds.
- The plan does not add schema changes, new dependencies, network calls, branch changes, commits, or pull requests.
