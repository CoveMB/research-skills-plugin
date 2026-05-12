#!/usr/bin/env python3
"""Package this plugin directory as a zip."""
from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from plugin_utils import (
    EXCLUDED_DIRECTORIES,
    EXCLUDED_FILE_NAMES,
    EXCLUDED_SUFFIXES,
    plugin_version,
)


def should_package_file(path: Path, output_path: Path, temporary_output_path: Path) -> bool:
    if path.resolve() in {output_path.resolve(), temporary_output_path.resolve()}:
        return False
    if EXCLUDED_DIRECTORIES.intersection(path.parts):
        return False
    if path.name in EXCLUDED_FILE_NAMES:
        return False
    if path.suffix in EXCLUDED_SUFFIXES:
        return False
    return path.is_file()


def package_files(root: Path, output_path: Path, temporary_output_path: Path) -> list[Path]:
    return [
        path
        for path in sorted(root.rglob("*"))
        if should_package_file(path, output_path, temporary_output_path)
    ]


def write_package(root: Path, output_path: Path) -> None:
    temporary_output_path = output_path.with_suffix(output_path.suffix + ".tmp")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if temporary_output_path.exists():
        temporary_output_path.unlink()
    with zipfile.ZipFile(temporary_output_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in package_files(root, output_path, temporary_output_path):
            archive.write(path, root.name + "/" + str(path.relative_to(root)))
    temporary_output_path.replace(output_path)


def default_output_path(root: Path) -> Path:
    return Path(f"{root.name}-v{plugin_version(root)}.zip")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    out = (args.out if args.out is not None else default_output_path(root)).resolve()
    write_package(root, out)
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
