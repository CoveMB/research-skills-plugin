"""Focused tests for manuscript-preparation scholar-grade fixtures."""
from __future__ import annotations

import hashlib
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
    "review-repair-queue-preservation": {
        "skill": "scholarly-prose-editor",
        "expected_decision": "Hold: repair queue remains open",
        "required_markers": {
            "Source basis",
            "claim IDs",
            "repair queue",
            "source-access label",
            "unresolved risks",
            "human checkpoint",
            "What remains uncertain",
            "User verification needed",
        },
        "required_source_anchors": {
            "C-101",
            "C-203",
            "source-access label: controlled packet; source notes only; locators incomplete",
            "repair queue item RQ-1",
        },
        "required_uncertainties": {
            "unresolved risks preserved",
            "source-access label preserved",
            "human checkpoint required",
            "locator/source-basis gaps remain",
        },
        "disallowed_claims": {
            "critique resolved",
            "submission-ready",
            "evidence verified",
            "objections answered",
        },
    },
}


def read_json_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} root must be an object")
    return payload


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_text(encoding="utf-8").encode("utf-8")).hexdigest()


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
                self.assertEqual(fixture["source_packet"], f"corpora/{fixture_id}")
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
                self.assertEqual(manifest["output_file"], f"{fixture_id}.md")
                self.assertEqual(manifest["skill_file"], f"skills/{expected['skill']}/SKILL.md")
                self.assertEqual(manifest["source_packet"], f"corpora/{fixture_id}/source-packet.md")
                self.assertIs(manifest["external_lookup_permitted"], False)
                self.assertEqual(structured_result["decision"], expected["expected_decision"])
                self.assertEqual(structured_result["source_access_level"], "controlled-packet")
                self.assertIs(structured_result["external_lookup_used"], False)
                self.assertIs(structured_result["private_material_submitted"], False)
                self.assertIs(structured_result["hard_fail_triggered"], False)
                self.assertEqual(manifest["prompt_packet_sha256"], sha256_file(prompt_path))
                self.assertEqual(manifest["output_sha256"], sha256_file(output_path))
                self.assertEqual(
                    manifest["skill_file_sha256"],
                    sha256_file(ROOT / f"skills/{expected['skill']}/SKILL.md"),
                )
                self.assertEqual(
                    manifest["source_packet_sha256"],
                    sha256_file(corpus_path / "source-packet.md"),
                )

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

    def test_recorded_outputs_preserve_boundaries(self) -> None:
        for fixture_id, expected in MANUSCRIPT_PREPARATION_FIXTURES.items():
            with self.subTest(fixture_id=fixture_id):
                output_text = (OUTPUTS_DIR / f"{fixture_id}.md").read_text(encoding="utf-8")

                self.assertIn(f"Expected decision: {expected['expected_decision']}", output_text)
                for marker in expected["required_markers"]:
                    self.assertIn(marker, output_text)
                for disallowed_claim in expected["disallowed_claims"]:
                    self.assertNotIn(disallowed_claim.lower(), output_text.lower())


if __name__ == "__main__":
    unittest.main()
