#!/usr/bin/env python3
"""Report additive live-pilot score calibration status."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from scholar_grade_eval_harness import build_scholar_grade_report, read_json_object


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_FIXTURES = ROOT / "tests" / "skill_evals" / "scholar_grade" / "fixtures.json"
DEFAULT_PILOT_PLAN = ROOT / "tests" / "skill_evals" / "scholar_grade" / "live_pilot" / "fixture-ids.json"
DEFAULT_LIVE_ROOT = ROOT / "tests" / "skill_evals" / "scholar_grade" / "live_pilot"
DEFAULT_BASELINE_SCORES = ROOT / "tests" / "skill_evals" / "scholar_grade" / "scores"


def string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def pilot_fixture_ids(pilot_plan_path: Path) -> list[str]:
    plan = read_json_object(pilot_plan_path)
    if plan.get("schema_version") != "scholar-grade-live-pilot-v1":
        raise ValueError("pilot plan schema_version must be scholar-grade-live-pilot-v1")
    fixture_ids = string_list(plan.get("fixture_ids"))
    if not fixture_ids:
        raise ValueError("pilot plan fixture_ids must be a non-empty string list")
    return fixture_ids


def score_path(scores_dir: Path, fixture_id: str) -> Path:
    return scores_dir / f"{fixture_id}.json"


def numeric_dimension_scores(score_document: dict[str, Any]) -> dict[str, float]:
    dimension_scores = score_document.get("dimension_scores")
    if not isinstance(dimension_scores, dict):
        return {}
    return {
        str(dimension): float(score)
        for dimension, score in dimension_scores.items()
        if isinstance(dimension, str) and isinstance(score, (int, float)) and not isinstance(score, bool)
    }


def score_regressions_for_fixture(
    fixture_id: str,
    live_scores_dir: Path,
    baseline_scores_dir: Path,
) -> list[dict[str, Any]]:
    live_score_path = score_path(live_scores_dir, fixture_id)
    baseline_score_path = score_path(baseline_scores_dir, fixture_id)
    if not live_score_path.exists() or not baseline_score_path.exists():
        return []

    live_score = read_json_object(live_score_path)
    baseline_score = read_json_object(baseline_score_path)
    live_dimensions = numeric_dimension_scores(live_score)
    baseline_dimensions = numeric_dimension_scores(baseline_score)
    regressions = [
        {
            "fixture_id": fixture_id,
            "dimension": dimension,
            "baseline_score": baseline_score_value,
            "live_score": live_score_value,
        }
        for dimension, live_score_value in sorted(live_dimensions.items())
        for baseline_score_value in [baseline_dimensions.get(dimension)]
        if baseline_score_value is not None and live_score_value < baseline_score_value
    ]
    baseline_hard_fail = baseline_score.get("hard_fail_triggered")
    if live_score.get("hard_fail_triggered") is True and baseline_hard_fail is not True:
        regressions.append(
            {
                "fixture_id": fixture_id,
                "dimension": "hard_fail_triggered",
                "baseline_score": baseline_hard_fail,
                "live_score": True,
            }
        )
    return regressions


def score_regressions(
    fixture_ids: list[str],
    live_scores_dir: Path,
    baseline_scores_dir: Path,
) -> list[dict[str, Any]]:
    return [
        regression
        for fixture_id in fixture_ids
        for regression in score_regressions_for_fixture(fixture_id, live_scores_dir, baseline_scores_dir)
    ]


def missing_baseline_score_actions(fixture_ids: list[str], baseline_scores_dir: Path) -> list[dict[str, str]]:
    return [
        {
            "fixture_id": fixture_id,
            "action": "record-baseline-review-score",
            "reason": "baseline review score is missing",
        }
        for fixture_id in fixture_ids
        if not score_path(baseline_scores_dir, fixture_id).exists()
    ]


def baseline_score_validation_errors(
    fixture_path: Path,
    fixture_ids: list[str],
    baseline_scores_dir: Path,
    root: Path,
) -> list[str]:
    baseline_report = build_scholar_grade_report(
        fixture_path=fixture_path,
        scores_dir=baseline_scores_dir,
        root=root,
        fixture_ids=fixture_ids,
    )
    return [
        error.replace(": score ", ": baseline score ", 1)
        for error in baseline_report["scores"]["validation_errors"]
        if ": missing review score " not in error
    ]


def baseline_score_validation_actions(validation_errors: list[str]) -> list[dict[str, str]]:
    return [
        {
            "fixture_id": error.split(":", 1)[0] if ":" in error else "suite",
            "action": "repair-baseline-review-score",
            "reason": error,
        }
        for error in validation_errors
    ]


def missing_artifact_fixture_ids(validation: dict[str, Any]) -> set[str]:
    return {
        fixture_id
        for key in ["outputs", "manifests", "scores"]
        for fixture_id in validation[key]["missing"]
    }


def missing_artifact_actions(validation: dict[str, Any]) -> list[dict[str, str]]:
    missing_fixture_ids = sorted(missing_artifact_fixture_ids(validation))
    return [
        {
            "fixture_id": fixture_id,
            "action": "record-live-capture-artifacts",
            "reason": "pilot output, manifest, or review score is missing",
        }
        for fixture_id in missing_fixture_ids
    ]


def validation_error_actions(validation: dict[str, Any], suppressed_fixture_ids: set[str]) -> list[dict[str, str]]:
    errors = [
        error
        for key in ["fixtures", "outputs", "manifests", "scores"]
        for error in validation[key]["validation_errors"]
    ]
    return [
        validation_error_action(error)
        for error in errors
        if (error.split(":", 1)[0] if ":" in error else "suite") not in suppressed_fixture_ids
    ]


def validation_error_action(error: str) -> dict[str, str]:
    fixture_id = error.split(":", 1)[0] if ":" in error else "suite"
    action = (
        "record-new-live-capture-after-skill-change"
        if "manifest skill_file_sha256 does not match skill file" in error
        else "repair-live-capture-validation-error"
    )
    return {
        "fixture_id": fixture_id,
        "action": action,
        "reason": error,
    }


def regression_actions(regressions: list[dict[str, Any]]) -> list[dict[str, str]]:
    return [
        {
            "fixture_id": str(regression["fixture_id"]),
            "action": "review-score-calibration",
            "reason": (
                f"{regression['dimension']} live score {regression['live_score']} "
                f"is below baseline {regression['baseline_score']}"
            ),
        }
        for regression in regressions
    ]


def build_calibration_report(
    fixture_path: Path = DEFAULT_FIXTURES,
    pilot_plan_path: Path = DEFAULT_PILOT_PLAN,
    live_root: Path = DEFAULT_LIVE_ROOT,
    baseline_scores_dir: Path = DEFAULT_BASELINE_SCORES,
    root: Path = ROOT,
) -> dict[str, Any]:
    fixture_ids = pilot_fixture_ids(pilot_plan_path)
    live_outputs_dir = live_root / "outputs"
    live_manifests_dir = live_root / "manifests"
    live_scores_dir = live_root / "scores"
    harness_report = build_scholar_grade_report(
        fixture_path=fixture_path,
        outputs_dir=live_outputs_dir,
        manifests_dir=live_manifests_dir,
        scores_dir=live_scores_dir,
        root=root,
        require_live_captures=True,
        fixture_ids=fixture_ids,
    )
    validation = {
        "fixtures": harness_report["fixtures"],
        "outputs": harness_report["outputs"],
        "manifests": harness_report["manifests"],
        "scores": harness_report["scores"],
    }
    regressions = score_regressions(fixture_ids, live_scores_dir, baseline_scores_dir)
    baseline_validation_errors = baseline_score_validation_errors(
        fixture_path=fixture_path,
        fixture_ids=fixture_ids,
        baseline_scores_dir=baseline_scores_dir,
        root=root,
    )
    missing_fixture_ids = missing_artifact_fixture_ids(validation)
    actions = [
        *missing_artifact_actions(validation),
        *validation_error_actions(validation, missing_fixture_ids),
        *missing_baseline_score_actions(fixture_ids, baseline_scores_dir),
        *baseline_score_validation_actions(baseline_validation_errors),
        *regression_actions(regressions),
    ]
    return {
        "schema_version": "scholar-grade-live-pilot-calibration-v1",
        "source": {
            "fixtures": str(fixture_path),
            "pilot_plan": str(pilot_plan_path),
            "live_root": str(live_root),
            "baseline_scores_dir": str(baseline_scores_dir),
        },
        "pilot": {
            "fixture_ids": fixture_ids,
            "fixture_count": len(fixture_ids),
        },
        "validation": validation,
        "regressions": {
            "checked": True,
            "items": regressions,
        },
        "baseline_scores": {
            "checked": True,
            "validation_errors": baseline_validation_errors,
        },
        "actions": actions,
        "ready": not actions,
        "limits": [
            "This report calibrates recorded live-pilot artifacts against local deterministic baselines.",
            "It does not run a model, score outputs automatically, or certify source truth.",
        ],
    }


def format_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Live Pilot Calibration",
        "",
        f"Ready: `{str(report['ready']).lower()}`",
        f"Pilot fixtures: `{report['pilot']['fixture_count']}`",
        "",
        "## Actions",
    ]
    if report["actions"]:
        lines.extend(
            f"- `{action['fixture_id']}`: {action['action']} - {action['reason']}"
            for action in report["actions"]
        )
    else:
        lines.append("- None")
    lines.extend(
        [
            "",
            "## Regressions",
        ]
    )
    if report["regressions"]["items"]:
        lines.extend(
            (
                f"- `{item['fixture_id']}` `{item['dimension']}`: "
                f"live `{item['live_score']}` vs baseline `{item['baseline_score']}`"
            )
            for item in report["regressions"]["items"]
        )
    else:
        lines.append("- None")
    return "\n".join(lines) + "\n"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", type=Path, default=DEFAULT_FIXTURES)
    parser.add_argument("--pilot-plan", type=Path, default=DEFAULT_PILOT_PLAN)
    parser.add_argument("--live-root", type=Path, default=DEFAULT_LIVE_ROOT)
    parser.add_argument("--baseline-scores-dir", type=Path, default=DEFAULT_BASELINE_SCORES)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    parser.add_argument("--strict", action="store_true", help="Exit nonzero when calibration is not ready.")
    parser.add_argument("--quiet", action="store_true", help="Suppress report output and return only status.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        report = build_calibration_report(
            fixture_path=args.fixtures.resolve(),
            pilot_plan_path=args.pilot_plan.resolve(),
            live_root=args.live_root.resolve(),
            baseline_scores_dir=args.baseline_scores_dir.resolve(),
            root=args.root.resolve(),
        )
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"errors": [str(error)]}, indent=2))
        return 1

    if not args.quiet:
        if args.format == "markdown":
            print(format_markdown(report), end="")
        else:
            print(json.dumps(report, indent=2))
    return 1 if args.strict and not report["ready"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
