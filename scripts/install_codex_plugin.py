#!/usr/bin/env python3
"""Install this plugin into a local Codex personal marketplace.

Default behavior:
- validate plugin
- copy plugin to ~/.codex/plugins/scholarly-research-book
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

sys.path.insert(0, str(Path(__file__).resolve().parent))
from plugin_utils import generated_file_patterns, load_plugin_manifest, plugin_name

MARKETPLACE_NAME = "local-personal-plugins"
VALIDATION_SCRIPTS = [
    "validate_plugin.py",
    "check_book_artifact_contract.py",
]


def home() -> Path:
    return Path.home()


def plugin_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def run_script(script: Path, root: Path) -> None:
    command = [sys.executable, str(script)]
    if script.name == "check_book_artifact_contract.py":
        command.extend(["--path", str(root)])
    else:
        command.append(str(root))
    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        raise SystemExit(result.returncode)
    print(result.stdout.strip())


def run_validation(root: Path) -> None:
    for script_name in VALIDATION_SCRIPTS:
        run_script(root / "scripts" / script_name, root)


def load_json(path: Path) -> dict:
    if not path.exists():
        return {
            "name": MARKETPLACE_NAME,
            "interface": {"displayName": "Local Personal Plugins"},
            "plugins": [],
        }
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        backup = path.with_suffix(path.suffix + f".backup-{timestamp}")
        shutil.copy2(path, backup)
        print(f"Existing marketplace JSON could not be parsed; backed up to {backup}")
        return {
            "name": MARKETPLACE_NAME,
            "interface": {"displayName": "Local Personal Plugins"},
            "plugins": [],
        }


def update_marketplace(path: Path, plugin_name_value: str, plugin_source_path: str, dry_run: bool) -> None:
    data = load_json(path)
    data.setdefault("name", MARKETPLACE_NAME)
    data.setdefault("interface", {"displayName": "Local Personal Plugins"})
    data.setdefault("plugins", [])
    entry = {
        "name": plugin_name_value,
        "source": {"source": "local", "path": plugin_source_path},
        "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
        "category": "Productivity",
    }
    plugins = [p for p in data["plugins"] if p.get("name") != plugin_name_value]
    plugins.append(entry)
    data["plugins"] = plugins
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
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
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


def copy_plugin(src: Path, dest: Path, dry_run: bool) -> None:
    expected_plugin_name = plugin_name(src)
    ensure_safe_destination(dest, expected_plugin_name)
    if dry_run:
        print(f"Would copy plugin from {src} to {dest}")
        return
    if dest.exists():
        shutil.rmtree(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    ignore = shutil.ignore_patterns(*generated_file_patterns())
    shutil.copytree(src, dest, ignore=ignore)
    print(f"Copied plugin to {dest}")


def print_dry_run_plan(root: Path, dest: Path, marketplace: Path, source_path: str) -> None:
    print("Dry run: no files will be copied or written.")
    print(f"Plugin root: {root}")
    print(f"Destination: {dest}")
    print(f"Marketplace: {marketplace}")
    print(f"Marketplace source path: {source_path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Install Research Book Skills Plugin locally for Codex.")
    parser.add_argument("--plugin-root", type=Path, default=plugin_root_from_script(), help="Path to this plugin root")
    parser.add_argument("--dest", type=Path, help="Destination plugin directory")
    parser.add_argument(
        "--marketplace",
        type=Path,
        default=home() / ".agents" / "plugins" / "marketplace.json",
        help="Marketplace JSON path",
    )
    parser.add_argument("--source-path", help="source.path to write in marketplace.json")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    root = args.plugin_root.expanduser().resolve()
    if not (root / ".codex-plugin" / "plugin.json").exists():
        print(f"Not a plugin root: {root}", file=sys.stderr)
        return 1
    try:
        plugin_name_value = str(load_plugin_manifest(root)["name"])
    except Exception as exc:
        print(f"Unable to read plugin manifest: {exc}", file=sys.stderr)
        return 1
    dest = (
        args.dest.expanduser()
        if args.dest is not None
        else home() / ".codex" / "plugins" / plugin_name_value
    )
    marketplace = args.marketplace.expanduser()
    source_path = args.source_path or f"./.codex/plugins/{plugin_name_value}"
    if args.dry_run:
        print_dry_run_plan(root, dest, marketplace, source_path)
    try:
        run_validation(root)
        copy_plugin(root, dest, args.dry_run)
        update_marketplace(marketplace, plugin_name_value, source_path, args.dry_run)
    except ValueError as exc:
        print(f"Install failed: {exc}", file=sys.stderr)
        return 1
    print("Done. Restart the app, then open the plugin directory and install/enable 'Research Book Skills'.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
