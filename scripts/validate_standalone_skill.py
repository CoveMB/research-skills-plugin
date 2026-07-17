#!/usr/bin/env python3
"""Validate a generated standalone skill directory, zip, or catalog."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from standalone_skill_bundles import validate_standalone_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a standalone skill directory, zip, or catalog."
    )
    parser.add_argument("target", type=Path, help="Bundle directory, bundle zip, or catalog.")
    parser.add_argument(
        "--registry",
        type=Path,
        help="Registry used for catalog classification and completeness checks.",
    )
    parser.add_argument(
        "--require-catalog-complete",
        action="store_true",
        help="Require every eligible registry skill when validating a catalog.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result = validate_standalone_path(
            args.target,
            registry_path=args.registry,
            require_catalog_complete=args.require_catalog_complete,
        )
    except (OSError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    if isinstance(result, list):
        print(f"Validated {len(result)} standalone bundle pairs in {args.target}")
    else:
        print(f"Validated {args.target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
