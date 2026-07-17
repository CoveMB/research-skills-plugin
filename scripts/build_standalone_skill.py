#!/usr/bin/env python3
"""Build dependency-closed standalone skill bundles."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from standalone_skill_bundles import build_all_standalone_skills, build_standalone_skill


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build one standalone skill bundle or the complete eligible catalog."
    )
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--skill", help="Source skill name to bundle.")
    selection.add_argument(
        "--all",
        action="store_true",
        help="Build every self-sufficient and route-only skill.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Plugin root. Defaults to this script's repository root.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        help="Output catalog directory. Defaults to <root>/dist/standalone-skills.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    output_root = (
        args.out if args.out is not None else root / "dist" / "standalone-skills"
    )
    try:
        if args.all:
            outputs = build_all_standalone_skills(root, output_root)
            print(f"Built {len(outputs)} standalone skill bundles in {output_root.resolve()}")
        else:
            bundle_directory, bundle_zip = build_standalone_skill(
                root,
                args.skill,
                output_root,
            )
            print(f"Built {bundle_directory}")
            print(f"Built {bundle_zip}")
    except (OSError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
