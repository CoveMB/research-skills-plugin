#!/usr/bin/env python3
"""Create an inactive Markdown intake packet for a real-source gold set."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = SCRIPT_DIR / "templates"
DEFAULT_OUTPUT_ROOT = SCRIPT_DIR / "intake"
TEMPLATE_FILENAMES = (
    "goldset_intake.md",
    "source_appraisal.md",
    "reviewer_checklist.md",
)
GOLDSET_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$")


def validate_goldset_id(goldset_id: str) -> None:
    if not GOLDSET_ID_RE.fullmatch(goldset_id):
        raise ValueError("goldset_id must be lowercase kebab-case with letters, numbers, and hyphens")


def rendered_template(template_text: str, *, goldset_id: str, title: str) -> str:
    return (
        template_text.replace("{{goldset_id}}", goldset_id)
        .replace("{{goldset_title}}", title)
        .rstrip()
        + "\n"
    )


def create_intake_packet(goldset_id: str, title: str, output_root: Path = DEFAULT_OUTPUT_ROOT) -> Path:
    validate_goldset_id(goldset_id)
    if not title.strip():
        raise ValueError("title must be non-empty")

    packet_dir = output_root / goldset_id
    packet_dir.mkdir(parents=True, exist_ok=False)
    for filename in TEMPLATE_FILENAMES:
        template_path = TEMPLATE_DIR / filename
        template_text = template_path.read_text(encoding="utf-8")
        (packet_dir / filename).write_text(
            rendered_template(template_text, goldset_id=goldset_id, title=title.strip()),
            encoding="utf-8",
        )
    return packet_dir


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--goldset-id", required=True, help="Lowercase kebab-case intake identifier.")
    parser.add_argument("--title", required=True, help="Human-readable gold-set title.")
    parser.add_argument(
        "--output-root",
        type=Path,
        default=DEFAULT_OUTPUT_ROOT,
        help="Directory where the intake packet directory will be created.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        packet_dir = create_intake_packet(args.goldset_id, args.title, args.output_root)
    except (FileExistsError, OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"Created inactive gold-set intake packet: {packet_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
