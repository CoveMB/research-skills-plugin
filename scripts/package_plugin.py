#!/usr/bin/env python3
"""Package this plugin directory as a zip."""
from __future__ import annotations

import argparse
import subprocess
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from plugin_utils import (
    package_files as included_package_files,
    print_completed_process_output,
    plugin_name,
    plugin_version,
)


VALIDATION_SCRIPT = Path(__file__).resolve().parent / "validate_plugin.py"


def package_output_files(root: Path, output_path: Path, temporary_output_path: Path) -> list[Path]:
    return [
        path
        for path in included_package_files(root)
        if path.resolve() not in {output_path.resolve(), temporary_output_path.resolve()}
    ]


def package_archive_prefix(root: Path) -> str:
    return plugin_name(root) or root.name


def write_package(root: Path, output_path: Path) -> None:
    temporary_output_path = output_path.with_suffix(output_path.suffix + ".tmp")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if temporary_output_path.exists():
        temporary_output_path.unlink()
    archive_prefix = package_archive_prefix(root)
    with zipfile.ZipFile(temporary_output_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in package_output_files(root, output_path, temporary_output_path):
            archive.write(path, archive_prefix + "/" + str(path.relative_to(root)))
    temporary_output_path.replace(output_path)


def default_output_path(root: Path) -> Path:
    return Path(f"{plugin_name(root)}-v{plugin_version(root)}.zip")


def run_validation(root: Path) -> int:
    result = subprocess.run(
        [sys.executable, str(VALIDATION_SCRIPT), str(root)],
        check=False,
        capture_output=True,
        text=True,
    )
    print_completed_process_output(result)
    return result.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Package this plugin directory as a zip.")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Plugin root to package. Defaults to this repository root.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        help="Zip file to write. Defaults to <manifest-name>-v<manifest-version>.zip.",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    out = (args.out if args.out is not None else default_output_path(root)).resolve()
    validation_status = run_validation(root)
    if validation_status != 0:
        return validation_status
    write_package(root, out)
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
