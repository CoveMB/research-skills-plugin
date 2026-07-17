#!/usr/bin/env python3
"""Build and validate every eligible standalone skill in temporary storage."""
from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from standalone_skill_bundles import (
    build_all_standalone_skills,
    load_registry,
    validate_catalog,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Plugin root. Defaults to this script's package root.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    registry_path = root / "shared" / "standalone-skill-registry.json"
    try:
        eligible_count = sum(
            entry.classification != "full-plugin-only" for entry in load_registry(root)
        )
        with tempfile.TemporaryDirectory(prefix="standalone-skill-check-") as temporary_directory:
            catalog_root = Path(temporary_directory) / "standalone-skills"
            outputs = build_all_standalone_skills(root, catalog_root)
            manifests = validate_catalog(catalog_root, registry_path)
            if len(outputs) != eligible_count or len(manifests) != eligible_count:
                raise ValueError(
                    "eligible standalone catalog count changed during build or validation"
                )
    except (OSError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Validated {eligible_count} standalone bundle pairs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
