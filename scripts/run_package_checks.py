#!/usr/bin/env python3
"""Run package validation checks."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from plugin_utils import print_completed_process_output


ROOT = Path(__file__).resolve().parents[1]


INSTALL_CHECKS = (
    ("scripts/validate_plugin.py", "."),
    ("scripts/check_book_artifact_contract.py", "--path", "."),
)

PILOT_FIXTURE_IDS = (
    "unsupported-causal-claim",
    "private-manuscript-search-consent",
    "quote-without-locator",
    "chart-without-data-provenance",
    "compact-output-hides-blocker",
    "prose-edit-changes-meaning",
    "literature-map-overstates-consensus",
    "ai-workflow-missing-verification-record",
    "hallucinated-result-without-run-log",
    "methodology-fabrication-run-config",
    "annotation-source-note-mixed-evidence",
    "book-comps-stale-mismatch",
    "claim-traceability-nearby-citation",
    "discovery-dedupe-fuzzy-export",
    "extraction-table-uneven-source-notes",
)


def fixture_id_args(fixture_ids: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(argument for fixture_id in fixture_ids for argument in ("--fixture-id", fixture_id))


LIVE_PILOT_CALIBRATION_CHECK = (
    "tests/skill_evals/scholar_grade/live_pilot_calibration.py",
    "--quiet",
)

LIVE_PILOT_REPORT_CHECK = (
    "tests/skill_evals/scholar_grade/live_pilot_calibration.py",
    "--pilot-plan",
    "tests/skill_evals/scholar_grade/live_pilot/fixture-ids.json",
    "--live-root",
    "tests/skill_evals/scholar_grade/live_pilot",
    "--format",
    "markdown",
)

LIVE_PILOT_V2_CALIBRATION_CHECK = (
    "tests/skill_evals/scholar_grade/live_pilot_calibration.py",
    "--pilot-plan",
    "tests/skill_evals/scholar_grade/live_pilot_v2/fixture-ids.json",
    "--live-root",
    "tests/skill_evals/scholar_grade/live_pilot_v2",
    "--strict",
    "--quiet",
)

LIVE_PILOT_V3_CALIBRATION_CHECK = (
    "tests/skill_evals/scholar_grade/live_pilot_calibration.py",
    "--pilot-plan",
    "tests/skill_evals/scholar_grade/live_pilot_v3/fixture-ids.json",
    "--live-root",
    "tests/skill_evals/scholar_grade/live_pilot_v3",
    "--quiet",
)

LIVE_PILOT_V3_REPORT_CHECK = (
    "tests/skill_evals/scholar_grade/live_pilot_calibration.py",
    "--pilot-plan",
    "tests/skill_evals/scholar_grade/live_pilot_v3/fixture-ids.json",
    "--live-root",
    "tests/skill_evals/scholar_grade/live_pilot_v3",
    "--format",
    "markdown",
)

SCHOLAR_MUTATION_CHECKS = (
    (
        "tests/skill_evals/scholar_grade/mutation_tests/run_mutation_tests.py",
        "--quiet",
    ),
)

REAL_GOLDSET_CHECKS = (
    ("tests/skill_evals/scholar_grade/real_goldsets/validate_goldsets.py",),
    (
        "tests/skill_evals/scholar_grade/real_goldsets/live_test_goldsets.py",
        "--quiet",
    ),
)

PACKAGE_CHECKS = INSTALL_CHECKS


FULL_CHECKS = (
    *INSTALL_CHECKS,
    (
        "scripts/check_research_behavior_fixtures.py",
        "--fixtures",
        "tests/skill_evals/research_behavior/fixtures.json",
        "--outputs-dir",
        "tests/skill_evals/research_behavior/outputs",
        "--traces-dir",
        "tests/skill_evals/research_behavior/traces",
    ),
    (
        "scripts/research_behavior_eval_harness.py",
        "--fixtures",
        "tests/skill_evals/research_behavior/fixtures.json",
        "--outputs-dir",
        "tests/skill_evals/research_behavior/outputs",
        "--traces-dir",
        "tests/skill_evals/research_behavior/traces",
        "--quiet",
    ),
    (
        "scripts/summarize_research_behavior_evals.py",
        "--fixtures",
        "tests/skill_evals/research_behavior/fixtures.json",
        "--outputs-dir",
        "tests/skill_evals/research_behavior/outputs",
        "--traces-dir",
        "tests/skill_evals/research_behavior/traces",
    ),
    (
        "scripts/check_workflow_passport_fixtures.py",
        "--fixtures",
        "tests/skill_evals/workflow_passports/fixtures.json",
    ),
    (
        "scripts/check_workflow_traceability.py",
        "--trace",
        "tests/skill_evals/workflow_traces/claim-lineage-fixture/workflow-trace.json",
    ),
    (
        "tests/skill_evals/scholar_grade/scholar_grade_eval_harness.py",
        "--fixtures",
        "tests/skill_evals/scholar_grade/fixtures.json",
        "--outputs-dir",
        "tests/skill_evals/scholar_grade/outputs",
        "--manifests-dir",
        "tests/skill_evals/scholar_grade/manifests",
        "--scores-dir",
        "tests/skill_evals/scholar_grade/scores",
        "--quiet",
    ),
    (
        "tests/skill_evals/scholar_grade/live_capture_protocol.py",
        "--fixtures",
        "tests/skill_evals/scholar_grade/fixtures.json",
        "--root",
        ".",
        "--check",
    ),
    LIVE_PILOT_CALIBRATION_CHECK,
    LIVE_PILOT_V3_CALIBRATION_CHECK,
    *REAL_GOLDSET_CHECKS,
    (
        "scripts/check_source_candidates.py",
        "--input",
        "tests/skill_evals/source-candidates.json",
        "--quiet",
    ),
    (
        "scripts/check_figure_table_provenance.py",
        "--input",
        "examples/figure_table_provenance/valid-provenance.json",
        "--quiet",
    ),
    ("-m", "unittest", "discover", "-s", "scripts", "-p", "test_*.py"),
    ("-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"),
)

LIVE_CHECKS = (
    (
        "tests/skill_evals/scholar_grade/scholar_grade_eval_harness.py",
        "--fixtures",
        "tests/skill_evals/scholar_grade/fixtures.json",
        "--outputs-dir",
        "tests/skill_evals/scholar_grade/outputs",
        "--manifests-dir",
        "tests/skill_evals/scholar_grade/manifests",
        "--scores-dir",
        "tests/skill_evals/scholar_grade/scores",
        "--require-live-captures",
        "--quiet",
    ),
)

LIVE_PILOT_CHECKS = (
    LIVE_PILOT_REPORT_CHECK,
)

LIVE_PILOT_V2_CHECKS = (
    (
        "tests/skill_evals/scholar_grade/scholar_grade_eval_harness.py",
        "--fixtures",
        "tests/skill_evals/scholar_grade/fixtures.json",
        "--outputs-dir",
        "tests/skill_evals/scholar_grade/live_pilot_v2/outputs",
        "--manifests-dir",
        "tests/skill_evals/scholar_grade/live_pilot_v2/manifests",
        "--scores-dir",
        "tests/skill_evals/scholar_grade/live_pilot_v2/scores",
        *fixture_id_args(PILOT_FIXTURE_IDS),
        "--require-live-captures",
        "--quiet",
    ),
    LIVE_PILOT_V2_CALIBRATION_CHECK,
)

LIVE_PILOT_V3_CHECKS = (
    LIVE_PILOT_V3_REPORT_CHECK,
)


PackageCheck = tuple[str, ...]


def checks_for_scope(scope: str) -> tuple[PackageCheck, ...]:
    checks_by_scope = {
        "install": INSTALL_CHECKS,
        "package": PACKAGE_CHECKS,
        "full": FULL_CHECKS,
        "live": LIVE_CHECKS,
        "live-pilot": LIVE_PILOT_CHECKS,
        "live-pilot-v2": LIVE_PILOT_V2_CHECKS,
        "live-pilot-v3": LIVE_PILOT_V3_CHECKS,
        "scholar-mutation": SCHOLAR_MUTATION_CHECKS,
        "real-goldsets": REAL_GOLDSET_CHECKS,
    }
    return checks_by_scope[scope]


def command_with_python(check: PackageCheck) -> list[str]:
    return [sys.executable, *check]


def run_check(check: PackageCheck, root: Path) -> int:
    result = subprocess.run(
        command_with_python(check),
        cwd=root,
        check=False,
        text=True,
        capture_output=True,
    )
    print_completed_process_output(result)
    return result.returncode


def run_checks(scope: str, root: Path) -> int:
    for check in checks_for_scope(scope):
        returncode = run_check(check, root)
        if returncode != 0:
            return returncode
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--scope",
        choices=[
            "install",
            "package",
            "full",
            "live",
            "live-pilot",
            "live-pilot-v2",
            "live-pilot-v3",
            "scholar-mutation",
            "real-goldsets",
        ],
        default="full",
        help=(
            "Use install for pre-install checks, full for source-checkout validation, "
            "package for validation that works from a packaged or installed copy without repo-only tests, "
            "live-pilot for the original pilot report, live-pilot-v2 for the strict calibrated pilot, "
            "live-pilot-v3 for the planned recapture report, "
            "scholar-mutation for evaluator sensitivity mutations, "
            "real-goldsets for active real-source gold-set live-test readiness, "
            "or live for recorded live skill captures."
        ),
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=ROOT,
        help="Plugin root to validate. Defaults to the repository root.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    return run_checks(args.scope, args.root.resolve())


if __name__ == "__main__":
    raise SystemExit(main())
