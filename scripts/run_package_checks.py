#!/usr/bin/env python3
"""Run package validation checks."""
from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class PackageCheck:
    label: str
    command: tuple[str, ...]


INSTALL_CHECKS = (
    PackageCheck("plugin structure", ("scripts/validate_plugin.py", ".")),
    PackageCheck("book artifact contract", ("scripts/check_book_artifact_contract.py", "--path", ".")),
)

FULL_CHECKS = (
    *INSTALL_CHECKS,
    PackageCheck(
        "research behavior fixtures",
        (
            "scripts/check_research_behavior_fixtures.py",
            "--fixtures",
            "examples/evals/research-skill-behavior-fixtures.json",
            "--outputs-dir",
            "examples/evals/outputs",
        ),
    ),
    PackageCheck(
        "research behavior harness",
        (
            "scripts/research_behavior_eval_harness.py",
            "--fixtures",
            "examples/evals/research-skill-behavior-fixtures.json",
            "--outputs-dir",
            "examples/evals/outputs",
            "--quiet",
        ),
    ),
    PackageCheck(
        "source candidate helper",
        (
            "scripts/check_source_candidates.py",
            "--input",
            "examples/evals/source-candidates.json",
            "--quiet",
        ),
    ),
    PackageCheck("unit tests", ("-m", "unittest", "discover", "-s", "scripts", "-p", "test_*.py")),
)


def checks_for_scope(scope: str) -> tuple[PackageCheck, ...]:
    return INSTALL_CHECKS if scope == "install" else FULL_CHECKS


def command_with_python(check: PackageCheck) -> list[str]:
    return [sys.executable, *check.command]


def run_check(check: PackageCheck, root: Path) -> int:
    result = subprocess.run(
        command_with_python(check),
        cwd=root,
        check=False,
        text=True,
        capture_output=True,
    )
    if result.stdout:
        print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
    if result.stderr:
        print(result.stderr, file=sys.stderr, end="" if result.stderr.endswith("\n") else "\n")
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
        choices=["install", "full"],
        default="full",
        help="Use install for pre-install checks or full for the complete validation suite.",
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
