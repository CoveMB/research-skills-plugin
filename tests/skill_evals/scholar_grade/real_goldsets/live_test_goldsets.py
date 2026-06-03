#!/usr/bin/env python3
"""Validate active real-source gold sets for automated live-test readiness."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from validate_goldsets import (
    candidate_goldset_paths,
    is_active_goldset,
    load_json_object,
    minimum_failure_check_ids,
    validate_goldset_document,
)


DEFAULT_ROOT = Path(__file__).resolve().parent
SOURCE_GROUPS = (
    ("gold_sources", "Gold Sources"),
    ("acceptable_sources", "Acceptable Sources"),
    ("decoy_sources", "Decoy Sources"),
    ("disallowed_sources", "Disallowed Sources"),
)
HIDDEN_PROMPT_MARKERS = (
    "candidate_output_scorecards",
    "minimum_failure_checks",
    "check_results",
    "score_basis",
    "required_distinctions",
    "must_support",
    "must_reject",
    "must_remain_uncertain",
    "citation_audit_expectations",
    "answer key",
    "ground truth for evaluation",
)


def as_string(value: Any) -> str:
    return value if isinstance(value, str) else ""


def string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str) and item.strip()]


def source_identifier(source: dict[str, Any]) -> str:
    return as_string(source.get("source_id")) or as_string(source.get("title")) or "<missing source id>"


def source_author_label(source: dict[str, Any]) -> str:
    authors = source.get("authors")
    if isinstance(authors, list):
        author_names = [author for author in authors if isinstance(author, str) and author.strip()]
        if author_names:
            return ", ".join(author_names)
    return as_string(source.get("authoring_body"))


def source_lines(document: dict[str, Any], field: str) -> list[str]:
    sources = document.get(field)
    if not isinstance(sources, list):
        return []

    lines: list[str] = []
    for source in sources:
        if not isinstance(source, dict):
            continue
        parts = [
            f"`{source_identifier(source)}`",
            as_string(source.get("title")),
            f"year: {source.get('year')}",
            f"authors/body: {source_author_label(source)}",
            f"role: {as_string(source.get('role'))}",
            f"access: {as_string(source.get('locator_or_access_note'))}",
        ]
        decoy_reason = as_string(source.get("decoy_reason"))
        if decoy_reason:
            parts.append(f"decoy reason: {decoy_reason}")
        lines.append(f"- {'; '.join(part for part in parts if str(part).strip())}")
    return lines


def scope_note_lines(document: dict[str, Any]) -> list[str]:
    lines = [
        f"- Field state note: {as_string(document.get('field_state_note'))}",
        f"- Source access notes: {as_string(document.get('source_access_notes'))}",
    ]
    mvp_scope = as_string(document.get("mvp_scope"))
    if mvp_scope:
        lines.append(f"- MVP scope: {mvp_scope}")

    waiver = document.get("search_log_scope_waiver")
    if isinstance(waiver, dict):
        scope_limit = as_string(waiver.get("scope_limit"))
        residual_risk = as_string(waiver.get("residual_risk"))
        lines.append(f"- Search-log waiver: {scope_limit}")
        lines.append(f"- Search-log residual risk: {residual_risk}")
    return [line for line in lines if line.strip() and not line.endswith(": ")]


def build_live_prompt_packet(path: Path, document: dict[str, Any]) -> str:
    lines = [
        f"# Real-Source Live Test Prompt: {as_string(document.get('goldset_id'))}",
        "",
        f"Gold-set file: `{path}`",
        f"Status: `{as_string(document.get('status'))}`",
        f"Task type: `{as_string(document.get('task_type'))}`",
        f"Human review required: `{document.get('human_review_required')}`",
        "",
        "## Operator Rules",
        "",
        "- Use this packet as the reviewed local source-role basis for the run.",
        "- Do not treat public-facing decoys as scholarly evidence.",
        "- Do not add source claims, locators, page numbers, or consensus statements beyond the reviewed packet.",
        "- Keep clinical usefulness separate from mechanism validation.",
        "",
        "## Prompt",
        "",
        as_string(document.get("visible_prompt")),
        "",
        "## Allowed Tools",
        "",
        *[f"- {tool}" for tool in string_list(document.get("allowed_tools"))],
        "",
        "## Network Policy",
        "",
        as_string(document.get("network_policy")),
        "",
        "## Scope Notes",
        "",
        *scope_note_lines(document),
    ]

    for field, title in SOURCE_GROUPS:
        group_lines = source_lines(document, field)
        if group_lines:
            lines.extend(["", f"## {title}", "", *group_lines])

    return "\n".join(lines).rstrip() + "\n"


def check_results(scorecard: dict[str, Any]) -> list[dict[str, Any]]:
    results = scorecard.get("check_results")
    if not isinstance(results, list):
        return []
    return [result for result in results if isinstance(result, dict)]


def outcome_by_check(scorecard: dict[str, Any]) -> dict[str, str]:
    outcomes: dict[str, str] = {}
    for result in check_results(scorecard):
        check_id = as_string(result.get("check_id"))
        outcome = as_string(result.get("outcome"))
        if check_id and outcome:
            outcomes[check_id] = outcome
    return outcomes


def expected_result(scorecard: dict[str, Any]) -> str:
    outcomes = list(outcome_by_check(scorecard).values())
    if any(outcome == "fail" for outcome in outcomes):
        return "fail"
    if outcomes and all(outcome == "pass" for outcome in outcomes):
        return "pass"
    return "invalid"


def candidate_output_cases(document: dict[str, Any]) -> list[dict[str, Any]]:
    scorecards = document.get("candidate_output_scorecards")
    if not isinstance(scorecards, list):
        return []

    cases: list[dict[str, Any]] = []
    for scorecard in scorecards:
        if not isinstance(scorecard, dict):
            continue
        outcomes = outcome_by_check(scorecard)
        cases.append(
            {
                "output_id": as_string(scorecard.get("output_id")),
                "output_label": as_string(scorecard.get("output_label")),
                "output_text": as_string(scorecard.get("output_text")),
                "expected_result": expected_result(scorecard),
                "failed_check_ids": sorted(
                    check_id for check_id, outcome in outcomes.items() if outcome == "fail"
                ),
                "passed_check_ids": sorted(
                    check_id for check_id, outcome in outcomes.items() if outcome == "pass"
                ),
            }
        )
    return cases


def validate_live_prompt_packet(path: Path, document: dict[str, Any], packet: str) -> list[str]:
    errors: list[str] = []
    for field in ("goldset_id", "visible_prompt", "network_policy"):
        value = as_string(document.get(field))
        if value and value not in packet:
            errors.append(f"{path}: live prompt packet is missing {field}")

    for field, _title in SOURCE_GROUPS:
        for source in document.get(field, []):
            if isinstance(source, dict):
                identifier = source_identifier(source)
                if identifier not in packet:
                    errors.append(f"{path}: live prompt packet is missing source {identifier}")

    folded_packet = packet.lower()
    for marker in HIDDEN_PROMPT_MARKERS:
        if marker in folded_packet:
            errors.append(f"{path}: live prompt packet exposes hidden marker {marker!r}")
    return errors


def validate_candidate_cases(path: Path, document: dict[str, Any]) -> list[str]:
    cases = candidate_output_cases(document)
    if not cases:
        return [f"{path}: active live test requires candidate_output_scorecards"]

    expected_results = {as_string(case.get("expected_result")) for case in cases}
    errors: list[str] = []
    if "pass" not in expected_results:
        errors.append(f"{path}: active live test requires at least one passing candidate output")
    if "fail" not in expected_results:
        errors.append(f"{path}: active live test requires at least one failing candidate output")
    if "invalid" in expected_results:
        errors.append(f"{path}: candidate output scorecards contain invalid expected results")

    check_ids = set(minimum_failure_check_ids(document))
    passed_by_check = {
        check_id
        for case in cases
        for check_id in case.get("passed_check_ids", [])
        if isinstance(check_id, str)
    }
    failed_by_check = {
        check_id
        for case in cases
        for check_id in case.get("failed_check_ids", [])
        if isinstance(check_id, str)
    }
    missing_pass_cases = sorted(check_ids - passed_by_check)
    missing_fail_cases = sorted(check_ids - failed_by_check)
    if missing_pass_cases:
        errors.append(
            f"{path}: checks lack a passing candidate case: {', '.join(missing_pass_cases)}"
        )
    if missing_fail_cases:
        errors.append(
            f"{path}: checks lack a failing candidate case: {', '.join(missing_fail_cases)}"
        )
    return errors


def validate_active_goldset_live_test(path: Path) -> list[str]:
    document, load_errors = load_json_object(path)
    if load_errors:
        return load_errors
    assert document is not None

    errors = [f"{path}: {error}" for error in validate_goldset_document(document)]
    if not is_active_goldset(document):
        errors.append(f"{path}: gold set must be active for live-test validation")
        return errors

    packet = build_live_prompt_packet(path, document)
    errors.extend(validate_live_prompt_packet(path, document, packet))
    errors.extend(validate_candidate_cases(path, document))
    return errors


def active_goldset_paths(root: Path) -> list[Path]:
    paths: list[Path] = []
    for path in candidate_goldset_paths(root):
        document, load_errors = load_json_object(path)
        if load_errors or document is None:
            continue
        if is_active_goldset(document):
            paths.append(path)
    return paths


def validate_active_goldset_live_tests(root: Path) -> list[str]:
    if root.is_file():
        return validate_active_goldset_live_test(root)

    paths = active_goldset_paths(root)
    if not paths:
        return [f"{root}: no active real-source gold sets found"]

    errors: list[str] = []
    for path in paths:
        errors.extend(validate_active_goldset_live_test(path))
    return errors


def expanded_roots(paths: list[Path]) -> list[Path]:
    return paths or [DEFAULT_ROOT]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Gold-set JSON files or directories. Defaults to this directory.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress success output.",
    )
    parser.add_argument(
        "--print-prompt-packets",
        action="store_true",
        help="Print rendered prompt packets for active cases after validation.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    errors: list[str] = []
    roots = expanded_roots(args.paths)
    for root in roots:
        errors.extend(validate_active_goldset_live_tests(root))

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    active_paths = [
        path
        for root in roots
        for path in active_goldset_paths(root)
    ]
    if args.print_prompt_packets:
        for path in active_paths:
            document, load_errors = load_json_object(path)
            if load_errors or document is None:
                continue
            print(build_live_prompt_packet(path, document))
    elif not args.quiet:
        print(f"Validated {len(active_paths)} active real-source live-test gold set(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
