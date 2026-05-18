#!/usr/bin/env python3
"""Build live/manual capture runbooks for scholar-grade skill evaluations."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]


def read_json_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} root must be an object")
    return payload


def fixture_list(document: dict[str, Any]) -> list[dict[str, Any]]:
    fixtures = document.get("fixtures")
    if not isinstance(fixtures, list):
        return []
    return [fixture for fixture in fixtures if isinstance(fixture, dict)]


def fixture_identifier(fixture: dict[str, Any]) -> str:
    value = fixture.get("id")
    return value if isinstance(value, str) and value else "<missing id>"


def string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def selected_fixture_ids(fixture_ids: list[str] | None) -> set[str] | None:
    if not fixture_ids:
        return None
    return {fixture_id for fixture_id in fixture_ids if fixture_id}


def select_fixtures(document: dict[str, Any], fixture_ids: list[str] | None) -> tuple[list[dict[str, Any]], list[str]]:
    fixtures = fixture_list(document)
    requested = selected_fixture_ids(fixture_ids)
    if requested is None:
        return fixtures, []
    selected = [fixture for fixture in fixtures if fixture_identifier(fixture) in requested]
    found = {fixture_identifier(fixture) for fixture in selected}
    missing = sorted(requested - found)
    return selected, [f"unknown fixture id: {fixture_id}" for fixture_id in missing]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def source_packet_path(fixture_path: Path, fixture: dict[str, Any]) -> Path:
    source_packet = str(fixture.get("source_packet", ""))
    return fixture_path.parent / source_packet / "source-packet.md"


def skill_file_path(root: Path, fixture: dict[str, Any]) -> Path:
    return root / "skills" / str(fixture.get("skill", "")) / "SKILL.md"


def output_file_name(fixture: dict[str, Any]) -> str:
    return f"{fixture_identifier(fixture)}.md"


def trace_file_path(fixture_path: Path, root: Path, fixture: dict[str, Any]) -> Path:
    return fixture_path.parent / "traces" / f"{fixture_identifier(fixture)}.json"


def relative_to_root_or_absolute(path: Path, root: Path) -> str:
    return str(path.relative_to(root) if path.is_relative_to(root) else path)


def capture_from_fixture(fixture_path: Path, root: Path, fixture: dict[str, Any]) -> dict[str, Any]:
    source_packet = source_packet_path(fixture_path, fixture)
    skill_file = skill_file_path(root, fixture)
    trace_file = trace_file_path(fixture_path, root, fixture)
    return {
        "fixture_id": fixture_identifier(fixture),
        "skill": str(fixture.get("skill", "")),
        "prompt": str(fixture.get("prompt", "")),
        "source_access_level": str(fixture.get("source_access_level", "")),
        "source_packet": relative_to_root_or_absolute(source_packet, root),
        "source_packet_sha256": sha256_file(source_packet),
        "source_packet_text": source_packet.read_text(encoding="utf-8"),
        "skill_file": relative_to_root_or_absolute(skill_file, root),
        "skill_file_sha256": sha256_file(skill_file),
        "output_file": output_file_name(fixture),
        "trace_file": relative_to_root_or_absolute(trace_file, root),
        "manifest_file": f"{fixture_identifier(fixture)}.json",
        "score_file": f"{fixture_identifier(fixture)}.json",
        "rubric_dimensions": string_list(fixture.get("rubric_dimensions")),
        "minimum_score": fixture.get("minimum_score"),
    }


def build_capture_plan(
    fixture_path: Path,
    root: Path = ROOT,
    fixture_ids: list[str] | None = None,
) -> dict[str, Any]:
    document = read_json_object(fixture_path)
    fixtures, selection_errors = select_fixtures(document, fixture_ids)
    if selection_errors:
        raise ValueError("; ".join(selection_errors))
    captures = [
        capture_from_fixture(fixture_path, root, fixture)
        for fixture in fixtures
    ]
    return {
        "schema_version": "scholar-grade-live-capture-plan-v1",
        "purpose": "Operator-facing plan for live or manual skill captures. Hidden answer keys and expected decisions are intentionally excluded.",
        "fixtures": str(fixture_path),
        "fixture_ids": [fixture_identifier(fixture) for fixture in fixtures],
        "capture_count": len(captures),
        "operator_rules": [
            "Provide only the rendered prompt packet and visible source-packet.md material to the skill.",
            "Do not provide answer-key.md, expected_decision, required_uncertainties, disallowed_claims, hard-fail patterns, or rubric scores during capture.",
            "After capture, save one Markdown output, complete one run manifest, then score against the hidden answer key and rubric.",
        ],
        "captures": captures,
    }


def prompt_packet_lines(capture: dict[str, Any]) -> list[str]:
    return [
        f"# Live Capture Prompt: {capture['fixture_id']}",
        "",
        f"Skill: `{capture['skill']}`",
        f"Source access level: `{capture['source_access_level']}`",
        f"Visible source packet: `{capture['source_packet']}`",
        "",
        "## Operator Rules",
        "",
        "- Use only the visible source packet below.",
        "- Do not use hidden answer keys or fixture expectation fields during the skill run.",
        "- Save the live skill response as Markdown before scoring.",
        "",
        "## Prompt",
        "",
        str(capture["prompt"]),
        "",
        "## Visible Source Packet",
        "",
        str(capture["source_packet_text"]),
    ]


def render_prompt_packet(capture: dict[str, Any]) -> str:
    return "\n".join(prompt_packet_lines(capture)).rstrip() + "\n"


def build_manifest_template(capture: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "scholar-grade-run-manifest-v1",
        "fixture_id": capture["fixture_id"],
        "skill": capture["skill"],
        "capture_mode": "manual-live-capture",
        "interface": "TODO_INTERFACE",
        "model": "TODO_MODEL",
        "date": "TODO_YYYY-MM-DD",
        "operator": "TODO_OPERATOR",
        "source_packet": capture["source_packet"],
        "source_packet_sha256": capture["source_packet_sha256"],
        "prompt_packet_sha256": sha256_text(render_prompt_packet(capture)),
        "skill_file": capture["skill_file"],
        "skill_file_sha256": capture["skill_file_sha256"],
        "output_file": capture["output_file"],
        "output_sha256": "TODO_AFTER_CAPTURE",
        "trace_file": capture["trace_file"],
        "trace_sha256": "TODO_FOR_AUTOMATED_CAPTURE",
        "tool_permissions": "TODO_TOOL_PERMISSIONS",
        "network_permissions": "TODO_NETWORK_PERMISSIONS",
        "external_lookup_permitted": "TODO_BOOLEAN",
        "structured_result": {
            "decision": "TODO_DECISION_AFTER_CAPTURE",
            "source_access_level": capture["source_access_level"],
            "selected_skill": "TODO_SELECTED_SKILL",
            "skill_invoked": "TODO_BOOLEAN",
            "source_packet_supplied": "TODO_BOOLEAN",
            "output_captured": "TODO_BOOLEAN",
            "external_lookup_used": "TODO_BOOLEAN",
            "private_material_submitted": "TODO_BOOLEAN",
            "hard_fail_triggered": "TODO_BOOLEAN",
            "next_action_count": "TODO_INTEGER",
        },
    }


def build_score_template(capture: dict[str, Any], reviewed_output_sha256: str = "TODO_AFTER_CAPTURE") -> dict[str, Any]:
    return {
        "schema_version": "scholar-grade-review-score-v1",
        "fixture_id": capture["fixture_id"],
        "reviewer": "TODO_REVIEWER",
        "date": "TODO_YYYY-MM-DD",
        "hard_fail_triggered": "TODO_BOOLEAN",
        "reviewed_output_sha256": reviewed_output_sha256,
        "dimension_scores": {
            dimension: "TODO_0_TO_5"
            for dimension in capture["rubric_dimensions"]
        },
        "dimension_rationales": {
            dimension: "TODO_RATIONALE"
            for dimension in capture["rubric_dimensions"]
        },
        "evidence_notes": ["TODO_EVIDENCE_NOTE"],
        "answer_key_findings": ["TODO_ANSWER_KEY_FINDING"],
        "minimum_score": capture["minimum_score"],
        "rationale": "TODO_RATIONALE",
    }


def build_trace_template(capture: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "scholar-grade-trace-v1",
        "fixture_id": capture["fixture_id"],
        "skill": capture["skill"],
        "model": "TODO_MODEL",
        "selected_skill": "TODO_SELECTED_SKILL",
        "tool_permissions": "TODO_TOOL_PERMISSIONS",
        "network_permissions": "TODO_NETWORK_PERMISSIONS",
        "skill_invoked": "TODO_BOOLEAN",
        "source_packet_supplied": "TODO_BOOLEAN",
        "output_captured": "TODO_BOOLEAN",
        "tool_call_count": "TODO_NON_NEGATIVE_INTEGER",
        "command_count": "TODO_NON_NEGATIVE_INTEGER",
        "token_usage": {
            "input_tokens": "TODO_NON_NEGATIVE_INTEGER",
            "output_tokens": "TODO_NON_NEGATIVE_INTEGER",
        },
        "trace_notes": "TODO_CAPTURE_INTERFACE_AND_TRACE_SOURCE",
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_capture_protocol(
    fixture_path: Path,
    output_dir: Path,
    root: Path = ROOT,
    fixture_ids: list[str] | None = None,
) -> dict[str, Any]:
    plan = build_capture_plan(fixture_path, root, fixture_ids)
    write_json(output_dir / "capture-plan.json", plan)
    write_text(output_dir / "README.md", render_protocol_readme(plan))
    for capture in plan["captures"]:
        fixture_id = str(capture["fixture_id"])
        write_text(output_dir / "prompts" / f"{fixture_id}.md", render_prompt_packet(capture))
        write_json(output_dir / "manifest-templates" / f"{fixture_id}.json", build_manifest_template(capture))
        write_json(output_dir / "score-templates" / f"{fixture_id}.json", build_score_template(capture))
        write_json(output_dir / "trace-templates" / f"{fixture_id}.json", build_trace_template(capture))
    return plan


def render_protocol_readme(plan: dict[str, Any]) -> str:
    lines = [
        "# Scholar-Grade Live Capture Protocol",
        "",
        "Use one prompt packet per fixture. Do not provide hidden answer keys or fixture expectation fields during the live skill run.",
        "",
        "After each run:",
        "",
        "1. Save the model response as Markdown.",
        "2. Complete the run manifest template.",
        "3. Score the output against the hidden answer key and rubric.",
        "4. For automated-live-capture, complete the matching trace-templates JSON, save it at the manifest trace_file path, and record trace_sha256.",
        "5. Run the scholar-grade harness with outputs, manifests, and scores.",
        "",
        "Automated trace templates are written under trace-templates/ for each fixture.",
        "",
        f"Capture count: {plan['capture_count']}",
        "",
    ]
    return "\n".join(lines)


def hidden_value_fields(fixture: dict[str, Any]) -> list[tuple[str, str]]:
    values: list[tuple[str, str]] = []
    expected_decision = fixture.get("expected_decision")
    if isinstance(expected_decision, str) and expected_decision:
        values.append(("expected_decision", expected_decision))
    for key in [
        "required_uncertainties",
        "disallowed_claims",
        "hard_fail_patterns",
        "semantic_fail_patterns",
        "rubric_dimensions",
    ]:
        values.extend((key, value) for value in string_list(fixture.get(key)) if value)
    return values


def leakage_errors_for_capture(capture: dict[str, Any]) -> list[str]:
    prompt_packet = render_prompt_packet(capture)
    banned_fragments = [
        "answer-key.md",
        "Ground truth for evaluation",
        "expected_decision",
        "required_uncertainties",
        "disallowed_claims",
        "hard_fail_patterns",
    ]
    return [
        f"{capture['fixture_id']}: prompt packet leaks {fragment!r}"
        for fragment in banned_fragments
        if fragment in prompt_packet
    ]


def hidden_value_leakage_errors(fixture: dict[str, Any], capture: dict[str, Any]) -> list[str]:
    prompt_packet = render_prompt_packet(capture)
    prompt = str(capture.get("prompt", ""))
    source_packet = str(capture.get("source_packet_text", ""))
    errors: list[str] = []
    prompt_visible_fields = {"disallowed_claims", "hard_fail_patterns", "semantic_fail_patterns"}
    for key, value in hidden_value_fields(fixture):
        if value not in prompt_packet or value in source_packet:
            continue
        if key in prompt_visible_fields and value in prompt:
            continue
        errors.append(f"{capture['fixture_id']}: prompt packet leaks {key} value {value!r}")
    return errors


def validate_capture_plan(
    fixture_path: Path,
    root: Path = ROOT,
    fixture_ids: list[str] | None = None,
) -> list[str]:
    try:
        document = read_json_object(fixture_path)
        fixtures, selection_errors = select_fixtures(document, fixture_ids)
        if selection_errors:
            return selection_errors
        plan = build_capture_plan(fixture_path, root, fixture_ids)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return [str(error)]
    errors: list[str] = []
    for fixture, capture in zip(fixtures, plan["captures"]):
        errors.extend(leakage_errors_for_capture(capture))
        errors.extend(hidden_value_leakage_errors(fixture, capture))
    return errors


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", type=Path, required=True, help="Scholar-grade fixture JSON file.")
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository root used for skill-file hashes.")
    parser.add_argument("--out-dir", type=Path, help="Directory where capture protocol files should be written.")
    parser.add_argument("--fixture-id", action="append", help="Limit protocol generation to one fixture id. Repeat for a pilot subset.")
    parser.add_argument("--check", action="store_true", help="Validate the protocol without writing files.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    root = args.root.resolve()
    errors = validate_capture_plan(args.fixtures, root, args.fixture_id)
    if errors:
        print("Live capture protocol check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    if args.check:
        print("OK: live capture protocol is valid.")
        return 0
    if args.out_dir is None:
        print("--out-dir is required unless --check is used")
        return 2
    write_capture_protocol(args.fixtures, args.out_dir, root, args.fixture_id)
    print(f"Wrote live capture protocol to {args.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
