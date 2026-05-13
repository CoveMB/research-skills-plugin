"""Shared research behavior fixture reporting helpers."""
from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from check_research_behavior_fixtures import (
    fixture_identifier,
    is_compact_fixture,
    output_path_for_fixture,
    validate_output_for_fixture,
)


def sorted_counts(values: list[str]) -> dict[str, int]:
    return dict(sorted(Counter(values).items()))


def fixture_identifiers(fixtures: list[dict[str, Any]]) -> list[str]:
    return [fixture_identifier(fixture) for fixture in fixtures]


def present_output_identifiers(outputs_dir: Path, fixtures: list[dict[str, Any]]) -> list[str]:
    return [
        fixture_identifier(fixture)
        for fixture in fixtures
        if output_path_for_fixture(outputs_dir, fixture).exists()
    ]


def missing_output_identifiers(outputs_dir: Path, fixtures: list[dict[str, Any]]) -> list[str]:
    return [
        fixture_identifier(fixture)
        for fixture in fixtures
        if not output_path_for_fixture(outputs_dir, fixture).exists()
    ]


def output_validation_errors(outputs_dir: Path, fixtures: list[dict[str, Any]]) -> list[str]:
    return [
        error
        for fixture in fixtures
        for error in validate_output_for_fixture(outputs_dir, fixture)
    ]


def fixture_summary(fixtures: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "total": len(fixtures),
        "ids": fixture_identifiers(fixtures),
        "compact_total": sum(1 for fixture in fixtures if is_compact_fixture(fixture)),
        "expected_route_counts": sorted_counts(
            [
                str(fixture.get("expected_route", ""))
                for fixture in fixtures
                if fixture.get("expected_route")
            ]
        ),
        "covered_risks": sorted(
            {
                str(fixture.get("risk_covered", ""))
                for fixture in fixtures
                if fixture.get("risk_covered")
            }
        ),
    }


def output_summary(outputs_dir: Path | None, fixtures: list[dict[str, Any]]) -> dict[str, Any]:
    if outputs_dir is None:
        return {
            "checked": False,
            "present": [],
            "missing": [],
            "validation_errors": [],
        }

    return {
        "checked": True,
        "directory": str(outputs_dir),
        "present": present_output_identifiers(outputs_dir, fixtures),
        "missing": missing_output_identifiers(outputs_dir, fixtures),
        "validation_errors": output_validation_errors(outputs_dir, fixtures),
    }
