#!/usr/bin/env python3
"""Summarize local research behavior fixture coverage, outputs, and traces."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from check_research_behavior_fixtures import (
    fixture_list,
    read_json_object,
    validate_fixture_document,
)
from research_behavior_reports import fixture_summary, output_summary, trace_summary


def build_calibration_report(
    fixture_path: Path,
    outputs_dir: Path | None = None,
    traces_dir: Path | None = None,
) -> dict[str, Any]:
    document_errors = validate_fixture_document(fixture_path)
    document = read_json_object(fixture_path) if not document_errors else {"fixtures": []}
    fixtures = fixture_list(document)
    return {
        "schema_version": "research-skill-behavior-calibration-v1",
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
        "limits": [
            "This report checks local fixture coverage, captured output markers, and route trace hashes only.",
            "It does not run a model, verify source truth, or certify scholarly correctness.",
        ],
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", type=Path, required=True, help="Fixture JSON file to summarize.")
    parser.add_argument(
        "--outputs-dir",
        type=Path,
        help="Optional directory containing one captured output markdown file per fixture id.",
    )
    parser.add_argument(
        "--traces-dir",
        type=Path,
        help="Optional directory containing one route trace JSON file per fixture id.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        report = build_calibration_report(args.fixtures, args.outputs_dir, args.traces_dir)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"errors": [str(error)]}, indent=2))
        return 1

    print(json.dumps(report, indent=2))
    has_errors = bool(
        report["fixtures"]["validation_errors"]
        or report["outputs"]["validation_errors"]
        or report["traces"]["validation_errors"]
    )
    return 1 if has_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
