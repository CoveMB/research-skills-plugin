"""Tests for active real-source gold-set live-test readiness."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from live_test_goldsets import (
    active_goldset_paths,
    build_live_prompt_packet,
    candidate_output_cases,
    validate_active_goldset_live_test,
    validate_active_goldset_live_tests,
)


ROOT = Path(__file__).resolve().parent
POLYVAGAL_GOLDSET = ROOT / "polyvagal-theory-consensus-overstatement.draft.json"


def load_polyvagal_goldset() -> dict[str, object]:
    return json.loads(POLYVAGAL_GOLDSET.read_text(encoding="utf-8"))


class RealGoldsetLiveTestTests(unittest.TestCase):
    def test_active_goldset_paths_include_polyvagal_fixture(self) -> None:
        paths = active_goldset_paths(ROOT)

        self.assertIn(POLYVAGAL_GOLDSET, paths)

    def test_live_prompt_packet_exposes_context_without_scorecard_answers(self) -> None:
        document = load_polyvagal_goldset()

        packet = build_live_prompt_packet(POLYVAGAL_GOLDSET, document)

        self.assertIn(str(document["visible_prompt"]), packet)
        self.assertIn("Search-log waiver", packet)
        self.assertIn("candidate-grossman-2023-five-premises", packet)
        self.assertIn("candidate-decoy-khiron-ladder", packet)
        self.assertNotIn("candidate_output_scorecards", packet)
        self.assertNotIn("minimum_failure_checks", packet)
        self.assertNotIn("check_results", packet)
        self.assertNotIn("must_support", packet)
        self.assertNotIn("must_reject", packet)
        self.assertNotIn("must_remain_uncertain", packet)
        self.assertNotIn("required_distinctions", packet)
        self.assertNotIn("citation_audit_expectations", packet)
        self.assertNotIn("outcome", packet.lower())
        self.assertNotIn("answer key", packet.lower())

    def test_candidate_output_cases_split_expected_pass_and_fail(self) -> None:
        document = load_polyvagal_goldset()

        cases = candidate_output_cases(document)
        expected_results = {
            case["output_id"]: case["expected_result"]
            for case in cases
        }

        self.assertEqual(expected_results["overstated-consensus-candidate"], "fail")
        self.assertEqual(expected_results["bounded-claim-map-candidate"], "pass")

    def test_active_goldset_live_test_validates_polyvagal_fixture(self) -> None:
        errors = validate_active_goldset_live_test(POLYVAGAL_GOLDSET)

        self.assertEqual(errors, [])

    def test_active_goldset_live_tests_validate_directory(self) -> None:
        errors = validate_active_goldset_live_tests(ROOT)

        self.assertEqual(errors, [])

    def test_active_goldset_live_tests_validate_file_path(self) -> None:
        errors = validate_active_goldset_live_tests(POLYVAGAL_GOLDSET)

        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
