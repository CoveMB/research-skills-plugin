#!/usr/bin/env python3
"""Build a deterministic research behavior evaluation harness report."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from check_research_behavior_fixtures import (
    fixture_identifier,
    fixture_list,
    forbidden_claims_for_fixture,
    output_path_for_fixture,
    read_json_object,
    string_list,
    trace_filename_for_fixture,
    trace_path_for_fixture,
    validate_fixture_document,
    validate_output_for_fixture,
    validate_trace_for_fixture,
)
from research_behavior_reports import fixture_summary, output_summary, trace_summary


MANUAL_OR_LIVE_RUN_EXPECTATIONS = [
    "Run each fixture prompt against the intended skill, model, or agent configuration.",
    "Capture exactly one Markdown output and one hash-linked route trace JSON per fixture id.",
    "Record the interface, model, date, operator, and any tool/network permissions outside the captured output.",
    "Do not submit private manuscripts, notes, source text, or unpublished data to external tools without explicit consent.",
    "Treat captured outputs as behavior samples, not as proof of source truth or scholarly correctness.",
]
LIMITS = [
    "This harness does not run a model or call external services.",
    "It checks fixture coverage, captured-output presence, route-trace presence, selected skill evidence, trace hashes, required markers, forbidden claims, and compact-output boundaries.",
    "For high-risk research fixtures, it checks structural overstatement and uncertainty markers plus reusable forbidden overclaim phrases.",
    "It does not verify source truth, citation accuracy, methodological validity, or scholarly correctness.",
]


def fixture_case_report(
    fixture: dict[str, Any],
    outputs_dir: Path | None,
    traces_dir: Path | None,
) -> dict[str, Any]:
    output_path = output_path_for_fixture(outputs_dir, fixture) if outputs_dir else None
    trace_path = trace_path_for_fixture(traces_dir, fixture) if traces_dir else None
    validation_errors = validate_output_for_fixture(outputs_dir, fixture) if outputs_dir else []
    trace_validation_errors = validate_trace_for_fixture(traces_dir, fixture, outputs_dir) if traces_dir else []
    return {
        "id": fixture_identifier(fixture),
        "prompt": str(fixture.get("prompt", "")),
        "expected_route": str(fixture.get("expected_route", "")),
        "risk_covered": str(fixture.get("risk_covered", "")),
        "required_output_markers": string_list(fixture.get("required_output_markers")),
        "forbidden_claims": forbidden_claims_for_fixture(fixture),
        "output_file": f"{fixture_identifier(fixture)}.md",
        "output_path": str(output_path) if output_path else None,
        "captured_output_checked": bool(output_path and output_path.exists()),
        "validation_errors": validation_errors,
        "trace_file": trace_filename_for_fixture(fixture),
        "trace_path": str(trace_path) if trace_path else None,
        "route_trace_checked": bool(trace_path and trace_path.exists()),
        "trace_validation_errors": trace_validation_errors,
    }


def build_harness_report(
    fixture_path: Path,
    outputs_dir: Path | None = None,
    traces_dir: Path | None = None,
) -> dict[str, Any]:
    document_errors = validate_fixture_document(fixture_path)
    document = read_json_object(fixture_path) if not document_errors else {"fixtures": []}
    fixtures = fixture_list(document)
    return {
        "schema_version": "research-skill-behavior-harness-v1",
        "execution_mode": "deterministic-local",
        "source": {
            "fixtures": str(fixture_path),
            "outputs_dir": str(outputs_dir) if outputs_dir else None,
            "traces_dir": str(traces_dir) if traces_dir else None,
        },
        "fixtures": {
            **fixture_summary(fixtures),
            "validation_errors": document_errors,
        },
        "outputs": output_summary(outputs_dir, fixtures),
        "traces": trace_summary(traces_dir, fixtures, outputs_dir),
        "manual_or_live_run_expectations": MANUAL_OR_LIVE_RUN_EXPECTATIONS,
        "limits": LIMITS,
        "cases": [fixture_case_report(fixture, outputs_dir, traces_dir) for fixture in fixtures],
    }


def inline_code(value: str) -> str:
    delimiter = "``" if "`" in value else "`"
    return f"{delimiter}{value}{delimiter}"


def inline_code_list(values: list[str]) -> str:
    return ", ".join(inline_code(value) for value in values) if values else "None"


def quote_markdown(text: str) -> list[str]:
    lines = text.splitlines() or [""]
    return [f"> {line}" for line in lines]


def format_markdown_runbook(report: dict[str, Any]) -> str:
    lines = [
        "# Research Behavior Evaluation Harness",
        "",
        f"Execution mode: `{report['execution_mode']}`",
        "",
        "## Limits",
        *[f"- {limit}" for limit in report["limits"]],
        "",
        "## Manual/live capture expectations",
        *[f"- {expectation}" for expectation in report["manual_or_live_run_expectations"]],
        "",
        "## Coverage",
        f"- Fixture count: {report['fixtures']['total']}",
        f"- Compact fixture count: {report['fixtures']['compact_total']}",
        f"- Expected routes: {json.dumps(report['fixtures']['expected_route_counts'], sort_keys=True)}",
        "",
        "## Captured outputs",
        f"- Checked: {str(report['outputs']['checked']).lower()}",
        f"- Present: {', '.join(report['outputs']['present']) or 'None'}",
        f"- Missing: {', '.join(report['outputs']['missing']) or 'None'}",
        "",
        "## Route traces",
        f"- Checked: {str(report['traces']['checked']).lower()}",
        f"- Present: {', '.join(report['traces']['present']) or 'None'}",
        f"- Missing: {', '.join(report['traces']['missing']) or 'None'}",
        "",
        "## Fixture runbook",
    ]
    for case in report["cases"]:
        lines.extend(
            [
                "",
                f"### {case['id']}",
                f"- Expected route: `{case['expected_route']}`",
                f"- Risk covered: {case['risk_covered']}",
                f"- Output file: `{case['output_file']}`",
                f"- Route trace file: `{case['trace_file']}`",
                f"- Required markers: {inline_code_list(case['required_output_markers'])}",
                f"- Forbidden claims: {inline_code_list(case['forbidden_claims'])}",
                f"- Validation errors: {inline_code_list(case['validation_errors'])}",
                f"- Trace validation errors: {inline_code_list(case['trace_validation_errors'])}",
                "",
                "Prompt:",
                *quote_markdown(case["prompt"]),
            ]
        )
    return "\n".join(lines) + "\n"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", type=Path, required=True, help="Fixture JSON file to turn into a harness report.")
    parser.add_argument(
        "--outputs-dir",
        type=Path,
        help="Optional directory containing one captured Markdown output per fixture id.",
    )
    parser.add_argument(
        "--traces-dir",
        type=Path,
        help="Optional directory containing one route trace JSON file per fixture id.",
    )
    parser.add_argument(
        "--format",
        choices=["json", "markdown"],
        default="json",
        help="Output JSON for automation or Markdown for a manual/live capture runbook.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress the report and return only the validation exit code.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        report = build_harness_report(args.fixtures, args.outputs_dir, args.traces_dir)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"errors": [str(error)]}, indent=2))
        return 1

    if not args.quiet:
        if args.format == "markdown":
            print(format_markdown_runbook(report), end="")
        else:
            print(json.dumps(report, indent=2))

    has_errors = bool(
        report["fixtures"]["validation_errors"]
        or report["outputs"]["validation_errors"]
        or report["traces"]["validation_errors"]
    )
    return 1 if has_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
