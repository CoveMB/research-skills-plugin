#!/usr/bin/env python3
"""Package this plugin directory as a zip."""
from __future__ import annotations

import argparse
import os
import stat
import subprocess
import sys
import tempfile
import uuid
import zipfile
from pathlib import Path, PurePosixPath
from typing import BinaryIO

sys.path.insert(0, str(Path(__file__).resolve().parent))
from plugin_utils import (
    package_files as included_package_files,
    print_completed_process_output,
    plugin_name,
    plugin_version,
)
from portable_plugin import (
    ADAPTER_PATH,
    portable_inventory,
    reject_symlink_components,
    render_portable_files,
    validate_portable_tree,
)


VALIDATION_SCRIPT = Path(__file__).resolve().parent / "validate_plugin.py"
DIRECTORY_OPERATIONS_SUPPORTED = (
    all(operation in os.supports_dir_fd for operation in (os.open, os.stat, os.link, os.unlink))
    and all(operation in os.supports_follow_symlinks for operation in (os.stat, os.link))
    and hasattr(os, "O_DIRECTORY")
    and hasattr(os, "O_NOFOLLOW")
)


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


def default_portable_output_path(root: Path) -> Path:
    return root / "dist" / "portable-plugin" / f"{plugin_name(root)}-v{plugin_version(root)}-portable.zip"


def validate_portable_archive(archive_path: Path | BinaryIO, prefix: str) -> None:
    """Inspect actual members before extracting into a new, private scratch tree."""
    with zipfile.ZipFile(archive_path) as archive, tempfile.TemporaryDirectory() as temporary:
        names: set[str] = set()
        folded_names: set[str] = set()
        for member in archive.infolist():
            path = PurePosixPath(member.filename)
            if (path.is_absolute() or ".." in path.parts or "\\" in member.filename
                    or len(path.parts) < 2 or path.parts[0] != prefix
                    or path.as_posix() != member.filename or member.is_dir()
                    or stat.S_ISLNK(member.external_attr >> 16)):
                raise ValueError(f"unsafe portable archive member: {member.filename}")
            if member.filename in names or member.filename.casefold() in folded_names:
                raise ValueError(f"duplicate portable archive member: {member.filename}")
            names.add(member.filename)
            folded_names.add(member.filename.casefold())
        archive.extractall(temporary)
        root = Path(temporary) / prefix
        expected_names = {f"{prefix}/{name}" for name in (*portable_inventory(root), ADAPTER_PATH)}
        if names != expected_names:
            raise ValueError("portable archive contains excluded or unexpected members")
        errors = validate_portable_tree(root)
        if errors:
            raise ValueError("invalid portable archive:\n- " + "\n- ".join(errors))


def require_staging_identity(directory_descriptor: int, name: str, identity: os.stat_result) -> None:
    current = os.stat(name, dir_fd=directory_descriptor, follow_symlinks=False)
    if not stat.S_ISREG(current.st_mode) or not os.path.samestat(current, identity):
        raise ValueError("portable staging entry changed; refusing publication or cleanup of its replacement")


def write_portable_package(root: Path, output_path: Path) -> None:
    if not DIRECTORY_OPERATIONS_SUPPORTED:
        raise OSError("portable publication requires safe directory-relative filesystem operations")
    root = root.resolve()
    # Do not resolve away a user-supplied symlink or an alias in its parents.
    reject_symlink_components(output_path.absolute())
    output_path = output_path.absolute()
    if output_path.exists():
        raise ValueError(f"portable output already exists: {output_path}; choose a new --out")
    try:
        relative_output = output_path.resolve().relative_to(root)
    except ValueError:
        relative_output = None
    if relative_output is not None and (not relative_output.parts or relative_output.parts[0] != "dist"):
        raise ValueError("portable output inside the source is allowed only under dist/")
    if run_validation(root) != 0:
        raise ValueError("source validation failed; portable output was not written")
    files = render_portable_files(root)
    prefix = package_archive_prefix(root)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    directory_descriptor = os.open(output_path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        reject_symlink_components(output_path)
        directory_identity = os.fstat(directory_descriptor)
        temporary_name = f".{output_path.name}.{uuid.uuid4().hex}.tmp"
        descriptor = os.open(
            temporary_name, os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
            0o600, dir_fd=directory_descriptor,
        )
        identity = os.fstat(descriptor)
        try:
            with os.fdopen(descriptor, "w+b", closefd=False) as stream:
                with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                    for name, data in files.items():
                        info = zipfile.ZipInfo(f"{prefix}/{name}")
                        info.create_system = 3
                        mode = (root / name).stat().st_mode if name != ADAPTER_PATH else stat.S_IFREG | 0o644
                        info.external_attr = mode << 16
                        info.compress_type = zipfile.ZIP_DEFLATED
                        archive.writestr(info, data)
                stream.flush()
                stream.seek(0)
                validate_portable_archive(stream, prefix)
            reject_symlink_components(output_path)
            if not os.path.samestat(directory_identity, os.stat(output_path.parent, follow_symlinks=False)):
                raise ValueError("portable output directory changed during validation")
            require_staging_identity(directory_descriptor, temporary_name, identity)
            # Both names stay relative to the original directory, even if it is renamed.
            # Hard-link publication cannot replace an existing destination.
            os.link(
                temporary_name, output_path.name, src_dir_fd=directory_descriptor,
                dst_dir_fd=directory_descriptor, follow_symlinks=False,
            )
        finally:
            try:
                try:
                    require_staging_identity(directory_descriptor, temporary_name, identity)
                except FileNotFoundError:
                    pass  # A removed/moved name gives us no owned entry to unlink.
                else:
                    os.unlink(temporary_name, dir_fd=directory_descriptor)
            finally:
                os.close(descriptor)
    except NotImplementedError as error:
        raise OSError("portable publication requires safe directory-relative filesystem operations") from error
    finally:
        os.close(directory_descriptor)


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
        help="Zip file to write. Portable mode requires a new destination; defaults under dist/portable-plugin/.",
    )
    parser.add_argument("--portable", action="store_true", help="Export all 29 skills with portable resources and an Antigravity adapter; never overwrite output.")
    args = parser.parse_args()
    root = args.root.resolve()
    if args.portable:
        out = args.out if args.out is not None else default_portable_output_path(root)
        try:
            write_portable_package(root, out)
        except (OSError, ValueError, zipfile.BadZipFile) as error:
            print(f"Portable packaging failed: {error}", file=sys.stderr)
            return 1
        print(f"Wrote {out.absolute()}")
        return 0
    out = (args.out if args.out is not None else default_output_path(root)).resolve()
    validation_status = run_validation(root)
    if validation_status != 0:
        return validation_status
    write_package(root, out)
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
