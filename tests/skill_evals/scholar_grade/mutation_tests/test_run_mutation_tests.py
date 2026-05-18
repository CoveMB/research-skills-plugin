"""Tests for scholar-grade mutation sensitivity checks."""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


SCRIPT = Path(__file__).resolve().parent / "run_mutation_tests.py"
ROOT = Path(__file__).resolve().parents[4]
SCHOLAR_GRADE_ROOT = ROOT / "tests" / "skill_evals" / "scholar_grade"
ADVERSARIAL_PRESSURE_FIXTURE_IDS = {
    "pressure-definitive-weak-evidence",
    "pressure-placeholder-citations",
    "pressure-hide-limitations",
    "pressure-private-manuscript-online",
    "pressure-exact-pages-unprovided",
    "pressure-claim-consensus",
    "pressure-compress-publication-ready",
    "pressure-prose-repair-strengthen-claim",
}


def load_runner_module():
    spec = importlib.util.spec_from_file_location("scholar_grade_mutation_runner", SCRIPT)
    if spec is None or spec.loader is None:
        raise AssertionError(f"Could not load mutation runner from {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class TestScholarGradeMutationRunner(unittest.TestCase):
    def test_cli_observes_expected_mutation_failures(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--quiet"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, msg=f"stdout={result.stdout} stderr={result.stderr}")
        self.assertEqual(result.stdout, "")

    def test_runner_reports_unexpected_pass_for_identity_mutation(self) -> None:
        runner = load_runner_module()
        identity_case = runner.MutationCase(
            fixture_id="unsupported-causal-claim",
            source_output_path=runner.reference_output_path("unsupported-causal-claim"),
            mutation_name="identity-mutation",
            mutation_function=lambda text: text,
            expected_failure_type="missing required uncertainty",
            expected_hard_fail=False,
        )

        with TemporaryDirectory() as temporary_directory:
            results = runner.evaluate_mutation_cases([identity_case], Path(temporary_directory))

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].status, "unexpected-pass")
        self.assertIn("unexpectedly passed", results[0].message)

    def test_shipped_adversarial_pressure_fixtures_have_mutation_coverage(self) -> None:
        runner = load_runner_module()
        fixture_document = json.loads((SCHOLAR_GRADE_ROOT / "fixtures.json").read_text(encoding="utf-8"))
        pressure_fixture_ids = {
            fixture["id"]
            for fixture in fixture_document["fixtures"]
            if str(fixture.get("source_packet", "")).startswith("adversarial_pressure/")
        }
        mutation_fixture_ids = {case.fixture_id for case in runner.default_mutation_cases()}

        self.assertEqual(pressure_fixture_ids, ADVERSARIAL_PRESSURE_FIXTURE_IDS)
        self.assertTrue(ADVERSARIAL_PRESSURE_FIXTURE_IDS <= mutation_fixture_ids)


if __name__ == "__main__":
    unittest.main()
