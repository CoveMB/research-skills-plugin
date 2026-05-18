"""Tests for synthetic retrieval/synthesis scholar-grade controls."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from scholar_grade_eval_harness import (
    validate_scholar_grade_fixture_document,
    validate_scholar_grade_outputs,
)


ROOT = Path(__file__).resolve().parents[3]
CONTROL_ROOT = ROOT / "tests" / "skill_evals" / "scholar_grade" / "retrieval_synthesis_controls"
FIXTURES = CONTROL_ROOT / "fixtures.json"
OUTPUTS = CONTROL_ROOT / "outputs"


class TestRetrievalSynthesisControls(unittest.TestCase):
    def test_control_fixtures_validate_with_reference_outputs(self) -> None:
        self.assertEqual(validate_scholar_grade_fixture_document(FIXTURES), [])
        self.assertEqual(validate_scholar_grade_outputs(FIXTURES, OUTPUTS), [])

    def test_control_fixtures_are_bounded_synthetic_examples(self) -> None:
        document = json.loads(FIXTURES.read_text(encoding="utf-8"))
        fixture_ids = {fixture["id"] for fixture in document["fixtures"]}

        self.assertEqual(
            fixture_ids,
            {
                "retrieval-reject-decoy-sources",
                "synthesis-preserve-disagreement-uncertainty",
            },
        )
        for fixture in document["fixtures"]:
            self.assertEqual(fixture["source_access_level"], "controlled-packet")
            self.assertIn("synthetic", fixture["prompt"].casefold())


if __name__ == "__main__":
    unittest.main()
