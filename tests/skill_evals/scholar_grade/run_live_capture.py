#!/usr/bin/env python3
"""Record auditable live-capture artifacts for scholar-grade skill evaluations."""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from live_capture_protocol import (
    ROOT,
    build_capture_plan,
    build_score_template,
    fixture_identifier,
    fixture_list,
    read_json_object,
    render_prompt_packet,
    sha256_file,
    write_json,
    write_text,
)


VALID_CAPTURE_MODES = {"manual-live-capture", "automated-live-capture"}
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@dataclass(frozen=True)
class CaptureMetadata:
    capture_mode: str
    interface: str
    model: str
    date: str
    operator: str
    decision: str
    tool_permissions: str
    network_permissions: str
    external_lookup_permitted: bool
    external_lookup_used: bool
    private_material_submitted: bool
    hard_fail_triggered: bool
    next_action_count: int


def output_file_name(fixture_id: str) -> str:
    return f"{fixture_id}.md"


def artifact_paths(output_root: Path, fixture_id: str, capture_mode: str = "manual-live-capture") -> dict[str, Path]:
    paths = {
        "prompt_packet": output_root / "prompts" / f"{fixture_id}.md",
        "output": output_root / "outputs" / output_file_name(fixture_id),
        "manifest": output_root / "manifests" / f"{fixture_id}.json",
        "score_template": output_root / "score-templates" / f"{fixture_id}.json",
    }
    if capture_mode == "automated-live-capture":
        paths["trace"] = output_root / "traces" / f"{fixture_id}.json"
    return paths


def relative_to_root(path: Path, root: Path) -> str:
    resolved_path = path.resolve()
    resolved_root = root.resolve()
    return str(resolved_path.relative_to(resolved_root))


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
    return selected, missing


def capture_lookup(fixture_path: Path, root: Path) -> dict[str, dict[str, Any]]:
    plan = build_capture_plan(fixture_path, root)
    return {str(capture["fixture_id"]): capture for capture in plan["captures"]}


def build_record_plan(
    fixture_path: Path,
    root: Path = ROOT,
    output_root: Path | None = None,
    fixture_ids: list[str] | None = None,
    capture_mode: str = "manual-live-capture",
) -> dict[str, Any]:
    output_root = output_root or fixture_path.parent
    document = read_json_object(fixture_path)
    fixtures, missing = select_fixtures(document, fixture_ids)
    captures = capture_lookup(fixture_path, root)
    records = [
        {
            "fixture_id": fixture_identifier(fixture),
            "skill": str(fixture.get("skill", "")),
            "source_packet": f"{fixture.get('source_packet', '')}/source-packet.md",
            "artifact_paths": {
                name: str(path)
                for name, path in artifact_paths(output_root, fixture_identifier(fixture), capture_mode).items()
            },
        }
        for fixture in fixtures
        if fixture_identifier(fixture) in captures
    ]
    return {
        "schema_version": "scholar-grade-live-capture-record-plan-v1",
        "purpose": "Dry-run plan for recording captured skill output, manifest metadata, prompt packet, and review templates.",
        "fixtures": str(fixture_path),
        "output_root": str(output_root),
        "capture_count": len(records),
        "missing_fixture_ids": missing,
        "captures": records,
    }


def existing_artifact_errors(paths: dict[str, Path], overwrite: bool) -> list[str]:
    if overwrite:
        return []
    return [
        f"refusing to overwrite existing artifact: {path}"
        for path in paths.values()
        if path.exists()
    ]


def validate_metadata(metadata: CaptureMetadata) -> list[str]:
    errors: list[str] = []
    if metadata.capture_mode not in VALID_CAPTURE_MODES:
        errors.append(f"capture_mode must be one of {sorted(VALID_CAPTURE_MODES)}")
    for field_name in ["interface", "model", "date", "operator", "decision", "tool_permissions", "network_permissions"]:
        value = getattr(metadata, field_name)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{field_name} is required")
    if metadata.date and DATE_PATTERN.fullmatch(metadata.date) is None:
        errors.append("date must use YYYY-MM-DD")
    elif metadata.date:
        try:
            date.fromisoformat(metadata.date)
        except ValueError:
            errors.append("date must be a real YYYY-MM-DD date")
    if not isinstance(metadata.next_action_count, int) or metadata.next_action_count < 0:
        errors.append("next_action_count must be a non-negative integer")
    return errors


def source_packet_manifest_path(fixture: dict[str, Any]) -> str:
    return f"{fixture.get('source_packet', '')}/source-packet.md"


def skill_manifest_path(fixture: dict[str, Any]) -> str:
    return f"skills/{fixture.get('skill', '')}/SKILL.md"


def build_run_manifest(
    fixture: dict[str, Any],
    capture: dict[str, Any],
    metadata: CaptureMetadata,
    output_sha256: str,
    prompt_packet_sha256: str,
    trace_sha256: str | None,
    trace_file: str | None,
) -> dict[str, Any]:
    fixture_id = fixture_identifier(fixture)
    manifest = {
        "schema_version": "scholar-grade-run-manifest-v1",
        "fixture_id": fixture_id,
        "skill": str(fixture.get("skill", "")),
        "capture_mode": metadata.capture_mode,
        "interface": metadata.interface,
        "model": metadata.model,
        "date": metadata.date,
        "operator": metadata.operator,
        "source_packet": source_packet_manifest_path(fixture),
        "source_packet_sha256": capture["source_packet_sha256"],
        "prompt_packet_sha256": prompt_packet_sha256,
        "skill_file": skill_manifest_path(fixture),
        "skill_file_sha256": capture["skill_file_sha256"],
        "output_file": output_file_name(fixture_id),
        "output_sha256": output_sha256,
        "tool_permissions": metadata.tool_permissions,
        "network_permissions": metadata.network_permissions,
        "external_lookup_permitted": metadata.external_lookup_permitted,
        "structured_result": {
            "decision": metadata.decision,
            "source_access_level": str(fixture.get("source_access_level", "")),
            "selected_skill": str(fixture.get("skill", "")),
            "skill_invoked": True,
            "source_packet_supplied": True,
            "output_captured": True,
            "external_lookup_used": metadata.external_lookup_used,
            "private_material_submitted": metadata.private_material_submitted,
            "hard_fail_triggered": metadata.hard_fail_triggered,
            "next_action_count": metadata.next_action_count,
        },
    }
    if metadata.capture_mode == "automated-live-capture":
        manifest["trace_file"] = trace_file
        manifest["trace_sha256"] = trace_sha256
    return manifest


def record_result(written: list[Path], errors: list[str]) -> dict[str, Any]:
    return {
        "written": [str(path) for path in written],
        "errors": errors,
    }


def matching_fixture_and_capture(
    fixture_path: Path,
    root: Path,
    fixture_id: str,
) -> tuple[dict[str, Any] | None, dict[str, Any] | None, list[str]]:
    try:
        document = read_json_object(fixture_path)
        fixtures, missing = select_fixtures(document, [fixture_id])
        captures = capture_lookup(fixture_path, root)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return None, None, [str(error)]
    if missing or not fixtures:
        return None, None, [f"unknown fixture id: {fixture_id}"]
    capture = captures.get(fixture_id)
    if capture is None:
        return fixtures[0], None, [f"unable to build capture plan for fixture id: {fixture_id}"]
    return fixtures[0], capture, []


def validate_record_inputs(
    paths: dict[str, Path],
    root: Path,
    captured_output: Path,
    metadata: CaptureMetadata,
    overwrite: bool,
    trace_source: Path | None,
) -> list[str]:
    errors = validate_metadata(metadata)
    if not captured_output.is_file():
        errors.append(f"captured output does not exist: {captured_output}")
    if metadata.capture_mode == "automated-live-capture":
        if trace_source is None:
            errors.append("automated-live-capture requires --trace-source")
        elif not trace_source.is_file():
            errors.append(f"trace source does not exist: {trace_source}")
        try:
            relative_to_root(paths["trace"], root)
        except ValueError:
            errors.append(f"automated trace artifact must stay inside root: {paths['trace']}")
    errors.extend(existing_artifact_errors(paths, overwrite))
    return errors


def record_live_capture(
    fixture_path: Path,
    root: Path,
    output_root: Path,
    fixture_id: str,
    captured_output: Path,
    metadata: CaptureMetadata,
    overwrite: bool,
    trace_source: Path | None = None,
) -> dict[str, Any]:
    fixture, capture, fixture_errors = matching_fixture_and_capture(fixture_path, root, fixture_id)
    if fixture_errors or fixture is None or capture is None:
        return record_result([], fixture_errors)
    paths = artifact_paths(output_root, fixture_id, metadata.capture_mode)
    input_errors = validate_record_inputs(paths, root, captured_output, metadata, overwrite, trace_source)
    if input_errors:
        return record_result([], input_errors)

    written: list[Path] = []
    write_text(paths["prompt_packet"], render_prompt_packet(capture))
    written.append(paths["prompt_packet"])
    prompt_packet_sha256 = sha256_file(paths["prompt_packet"])
    write_text(paths["output"], captured_output.read_text(encoding="utf-8"))
    written.append(paths["output"])
    output_sha256 = sha256_file(paths["output"])
    write_json(paths["score_template"], build_score_template(capture, output_sha256))
    written.append(paths["score_template"])

    trace_sha256: str | None = None
    if metadata.capture_mode == "automated-live-capture" and trace_source is not None:
        write_text(paths["trace"], trace_source.read_text(encoding="utf-8"))
        trace_sha256 = sha256_file(paths["trace"])
        written.append(paths["trace"])
    trace_file = relative_to_root(paths["trace"], root) if metadata.capture_mode == "automated-live-capture" else None

    manifest = build_run_manifest(
        fixture=fixture,
        capture=capture,
        metadata=metadata,
        output_sha256=output_sha256,
        prompt_packet_sha256=prompt_packet_sha256,
        trace_sha256=trace_sha256,
        trace_file=trace_file,
    )
    write_json(paths["manifest"], manifest)
    written.append(paths["manifest"])
    return record_result(written, [])


def parse_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "y"}:
        return True
    if normalized in {"0", "false", "no", "n"}:
        return False
    raise argparse.ArgumentTypeError(f"expected boolean, got {value!r}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", type=Path, required=True, help="Scholar-grade fixture JSON file.")
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository root used for skill-file hashes.")
    parser.add_argument("--out-root", type=Path, help="Artifact root. Defaults to the fixture file directory.")
    parser.add_argument("--fixture-id", action="append", help="Fixture id to record. Repeat only with --dry-run.")
    parser.add_argument("--captured-output", type=Path, help="Markdown file containing the captured skill response.")
    parser.add_argument("--trace-source", type=Path, help="Completed automated trace JSON to copy into traces/.")
    parser.add_argument("--capture-mode", choices=sorted(VALID_CAPTURE_MODES), default="manual-live-capture")
    parser.add_argument("--interface", help="Capture interface, such as codex-cli or codex-app.")
    parser.add_argument("--model", help="Model identifier used for the live run.")
    parser.add_argument("--date", help="Capture date in YYYY-MM-DD format.")
    parser.add_argument("--operator", help="Human operator who ran the capture.")
    parser.add_argument("--decision", help="Structured reviewer decision after the capture.")
    parser.add_argument("--tool-permissions", default="none")
    parser.add_argument("--network-permissions", default="none")
    parser.add_argument("--external-lookup-permitted", type=parse_bool, default=False)
    parser.add_argument("--external-lookup-used", type=parse_bool, default=False)
    parser.add_argument("--private-material-submitted", type=parse_bool, default=False)
    parser.add_argument("--hard-fail-triggered", type=parse_bool, default=False)
    parser.add_argument("--next-action-count", type=int, default=1)
    parser.add_argument("--overwrite", action="store_true", help="Allow replacing existing artifact files.")
    parser.add_argument("--dry-run", action="store_true", help="Print artifact paths without writing files.")
    return parser.parse_args(argv)


def metadata_from_args(args: argparse.Namespace) -> CaptureMetadata:
    return CaptureMetadata(
        capture_mode=args.capture_mode,
        interface=args.interface or "",
        model=args.model or "",
        date=args.date or "",
        operator=args.operator or "",
        decision=args.decision or "",
        tool_permissions=args.tool_permissions or "",
        network_permissions=args.network_permissions or "",
        external_lookup_permitted=args.external_lookup_permitted,
        external_lookup_used=args.external_lookup_used,
        private_material_submitted=args.private_material_submitted,
        hard_fail_triggered=args.hard_fail_triggered,
        next_action_count=args.next_action_count,
    )


def print_errors(header: str, errors: list[str]) -> None:
    print(header)
    for error in errors:
        print(f"- {error}")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    fixture_path = args.fixtures.resolve()
    root = args.root.resolve()
    output_root = (args.out_root or fixture_path.parent).resolve()
    if args.dry_run:
        try:
            plan = build_record_plan(fixture_path, root, output_root, args.fixture_id, args.capture_mode)
        except (OSError, ValueError, json.JSONDecodeError) as error:
            print_errors("Live capture record plan failed:", [str(error)])
            return 1
        print(json.dumps(plan, indent=2, sort_keys=True))
        return 1 if plan["missing_fixture_ids"] else 0

    if not args.fixture_id or len(args.fixture_id) != 1:
        print("--fixture-id is required exactly once unless --dry-run is used")
        return 2
    if args.captured_output is None:
        print("--captured-output is required unless --dry-run is used")
        return 2

    result = record_live_capture(
        fixture_path=fixture_path,
        root=root,
        output_root=output_root,
        fixture_id=args.fixture_id[0],
        captured_output=args.captured_output.resolve(),
        metadata=metadata_from_args(args),
        overwrite=args.overwrite,
        trace_source=args.trace_source.resolve() if args.trace_source else None,
    )
    if result["errors"]:
        print_errors("Live capture record failed:", result["errors"])
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
