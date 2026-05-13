#!/usr/bin/env python3
"""Install this plugin into a local personal marketplace.

Default behavior:
- validate plugin
- copy plugin to the local plugin directory
- create/update ~/.agents/plugins/marketplace.json

Use --dry-run to preview actions.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, NamedTuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
from plugin_utils import copy_package_tree, load_plugin_manifest, plugin_manifest_path, plugin_name

MARKETPLACE_NAME = "local-personal-plugins"
MARKETPLACE_DISPLAY_NAME = "Local Personal Plugins"
VALIDATION_RUNNER = Path(__file__).resolve().parent / "run_package_checks.py"


class InstallPlan(NamedTuple):
    root: Path
    plugin_name_value: str
    dest: Path
    marketplace: Path
    source_path: str


def home() -> Path:
    return Path.home()


def plugin_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def run_validation(root: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(VALIDATION_RUNNER), "--scope", "install", "--root", str(root)],
        text=True,
        capture_output=True,
    )
    if result.stdout:
        print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
    if result.stderr:
        print(result.stderr, file=sys.stderr, end="" if result.stderr.endswith("\n") else "\n")
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def build_install_plan(
    plugin_root: Path,
    dest: Path | None,
    marketplace: Path,
    source_path: str | None,
) -> InstallPlan:
    root = plugin_root.expanduser().resolve()
    if not plugin_manifest_path(root).exists():
        raise ValueError(f"Not a plugin root: {root}")
    try:
        plugin_name_value = str(load_plugin_manifest(root)["name"])
    except Exception as exc:
        raise ValueError(f"Unable to read plugin manifest: {exc}") from exc
    destination = (
        dest.expanduser()
        if dest is not None
        else home() / ".codex" / "plugins" / plugin_name_value
    )
    marketplace_path = marketplace.expanduser()
    marketplace_source_path = source_path or f"./.codex/plugins/{plugin_name_value}"
    return InstallPlan(
        root=root,
        plugin_name_value=plugin_name_value,
        dest=destination,
        marketplace=marketplace_path,
        source_path=marketplace_source_path,
    )


def default_marketplace_data() -> dict[str, Any]:
    return {
        "name": MARKETPLACE_NAME,
        "interface": {"displayName": MARKETPLACE_DISPLAY_NAME},
        "plugins": [],
    }


def normalize_marketplace_data(data: object) -> dict[str, Any]:
    if not isinstance(data, dict):
        return default_marketplace_data()

    normalized = dict(data)
    if not isinstance(normalized.get("name"), str) or not normalized["name"]:
        normalized["name"] = MARKETPLACE_NAME

    interface = normalized.get("interface")
    interface_data = dict(interface) if isinstance(interface, dict) else {}
    if not isinstance(interface_data.get("displayName"), str) or not interface_data["displayName"]:
        interface_data["displayName"] = MARKETPLACE_DISPLAY_NAME
    normalized["interface"] = interface_data

    plugins = normalized.get("plugins")
    normalized["plugins"] = [
        plugin for plugin in plugins if isinstance(plugin, dict)
    ] if isinstance(plugins, list) else []
    return normalized


def marketplace_entry(plugin_name_value: str, plugin_source_path: str) -> dict[str, Any]:
    return {
        "name": plugin_name_value,
        "source": {"source": "local", "path": plugin_source_path},
        "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
        "category": "Productivity",
    }


def replace_marketplace_entry(data: object, entry: dict[str, Any]) -> dict[str, Any]:
    normalized = normalize_marketplace_data(data)
    plugins = [
        plugin for plugin in normalized["plugins"] if plugin.get("name") != entry.get("name")
    ]
    return {
        **normalized,
        "plugins": [*plugins, entry],
    }


def load_json(path: Path, dry_run: bool) -> dict:
    if not path.exists():
        return default_marketplace_data()
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        backup = path.with_suffix(path.suffix + f".backup-{timestamp}")
        if dry_run:
            print(f"Existing marketplace JSON could not be parsed; would back up to {backup}")
        else:
            shutil.copy2(path, backup)
            print(f"Existing marketplace JSON could not be parsed; backed up to {backup}")
        return default_marketplace_data()


def update_marketplace(path: Path, plugin_name_value: str, plugin_source_path: str, dry_run: bool) -> None:
    data = replace_marketplace_entry(
        load_json(path, dry_run),
        marketplace_entry(plugin_name_value, plugin_source_path),
    )
    if dry_run:
        print(f"Would write marketplace: {path}")
        print(json.dumps(data, indent=2))
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        backup = path.with_suffix(path.suffix + f".backup-{timestamp}")
        shutil.copy2(path, backup)
        print(f"Backed up existing marketplace to {backup}")
    write_text_atomic(path, json.dumps(data, indent=2) + "\n")
    print(f"Updated marketplace: {path}")


def plugin_manifest_name(path: Path) -> str:
    manifest_path = path / ".codex-plugin" / "plugin.json"
    if not manifest_path.exists():
        return ""
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception:
        return ""
    return str(payload.get("name", "")) if isinstance(payload, dict) else ""


def is_safe_destination(dest: Path, expected_plugin_name: str) -> bool:
    if not dest.exists():
        return dest.name == expected_plugin_name
    if plugin_manifest_name(dest) == expected_plugin_name:
        return True
    return dest.name == expected_plugin_name and not any(dest.iterdir())


def ensure_safe_destination(dest: Path, expected_plugin_name: str) -> None:
    if not is_safe_destination(dest, expected_plugin_name):
        raise ValueError(
            f"Refusing to replace destination outside expected plugin path: {dest}"
        )


def temporary_sibling_path(dest: Path, label: str) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    return dest.parent / f".{dest.name}.{label}-{timestamp}"


def write_text_atomic(path: Path, text: str) -> None:
    temporary_path = temporary_sibling_path(path, "write")
    try:
        temporary_path.write_text(text, encoding="utf-8")
        temporary_path.replace(path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def replace_directory(source: Path, destination: Path) -> None:
    previous_path = temporary_sibling_path(destination, "previous")
    destination_exists = destination.exists()
    if destination_exists:
        destination.replace(previous_path)
    try:
        source.replace(destination)
    except Exception:
        if destination_exists and previous_path.exists() and not destination.exists():
            previous_path.replace(destination)
        raise
    if previous_path.exists():
        shutil.rmtree(previous_path)


def copy_plugin(src: Path, dest: Path, dry_run: bool) -> None:
    if src.resolve() == dest.resolve():
        raise ValueError(f"Refusing to copy plugin onto itself: {dest}")
    expected_plugin_name = plugin_name(src)
    ensure_safe_destination(dest, expected_plugin_name)
    if dry_run:
        print(f"Would copy plugin from {src} to {dest}")
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    temporary_destination = temporary_sibling_path(dest, "copy")
    try:
        copy_package_tree(src, temporary_destination)
        replace_directory(temporary_destination, dest)
    finally:
        if temporary_destination.exists():
            shutil.rmtree(temporary_destination)
    print(f"Copied plugin to {dest}")


def print_dry_run_plan(root: Path, dest: Path, marketplace: Path, source_path: str) -> None:
    print("Dry run: no files will be copied or written.")
    print(f"Plugin root: {root}")
    print(f"Destination: {dest}")
    print(f"Marketplace: {marketplace}")
    print(f"Marketplace source path: {source_path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Install Research Book Skills Plugin locally.")
    parser.add_argument(
        "--plugin-root",
        type=Path,
        default=plugin_root_from_script(),
        help="Plugin root to validate and install. Defaults to this repository root.",
    )
    parser.add_argument(
        "--dest",
        type=Path,
        help="Destination plugin directory. Defaults to the local plugin directory for this package.",
    )
    parser.add_argument(
        "--marketplace",
        type=Path,
        default=home() / ".agents" / "plugins" / "marketplace.json",
        help="Marketplace JSON path",
    )
    parser.add_argument("--source-path", help="source.path to write in marketplace.json")
    parser.add_argument("--dry-run", action="store_true", help="Print the install plan without writing files.")
    args = parser.parse_args()

    try:
        plan = build_install_plan(args.plugin_root, args.dest, args.marketplace, args.source_path)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    if args.dry_run:
        print_dry_run_plan(plan.root, plan.dest, plan.marketplace, plan.source_path)
    try:
        run_validation(plan.root)
        copy_plugin(plan.root, plan.dest, args.dry_run)
        update_marketplace(
            plan.marketplace,
            plan.plugin_name_value,
            plan.source_path,
            args.dry_run,
        )
    except ValueError as exc:
        print(f"Install failed: {exc}", file=sys.stderr)
        return 1
    print("Done. Restart the app, then open the plugin directory and install/enable 'Research Book Skills'.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
