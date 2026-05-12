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
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

PLUGIN_NAME = "scholarly-research-book"
MARKETPLACE_NAME = "local-personal-plugins"


def home() -> Path:
    return Path.home()


def plugin_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def run_validation(root: Path) -> None:
    script = root / "scripts" / "validate_plugin.py"
    result = subprocess.run([sys.executable, str(script), str(root)], text=True, capture_output=True)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        raise SystemExit(result.returncode)
    print(result.stdout.strip())


def load_json(path: Path) -> dict:
    if not path.exists():
        return {"name": MARKETPLACE_NAME, "interface": {"displayName": "Local Personal Plugins"}, "plugins": []}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        backup = path.with_suffix(path.suffix + f".backup-{datetime.now().strftime('%Y%m%d%H%M%S')}")
        shutil.copy2(path, backup)
        print(f"Existing marketplace JSON could not be parsed; backed up to {backup}")
        return {"name": MARKETPLACE_NAME, "interface": {"displayName": "Local Personal Plugins"}, "plugins": []}


def update_marketplace(path: Path, plugin_source_path: str, dry_run: bool) -> None:
    data = load_json(path)
    data.setdefault("name", MARKETPLACE_NAME)
    data.setdefault("interface", {"displayName": "Local Personal Plugins"})
    data.setdefault("plugins", [])
    entry = {
        "name": PLUGIN_NAME,
        "source": {"source": "local", "path": plugin_source_path},
        "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
        "category": "Productivity",
    }
    plugins = [p for p in data["plugins"] if p.get("name") != PLUGIN_NAME]
    plugins.append(entry)
    data["plugins"] = plugins
    if dry_run:
        print(f"Would write marketplace: {path}")
        print(json.dumps(data, indent=2))
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        backup = path.with_suffix(path.suffix + f".backup-{datetime.now().strftime('%Y%m%d%H%M%S')}")
        shutil.copy2(path, backup)
        print(f"Backed up existing marketplace to {backup}")
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"Updated marketplace: {path}")


def copy_plugin(src: Path, dest: Path, dry_run: bool) -> None:
    if dry_run:
        print(f"Would copy plugin from {src} to {dest}")
        return
    if dest.exists():
        shutil.rmtree(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    ignore = shutil.ignore_patterns("*.zip", "__pycache__", ".DS_Store")
    shutil.copytree(src, dest, ignore=ignore)
    print(f"Copied plugin to {dest}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Install Scholarly Research Book Skills Plugin locally for Codex.")
    parser.add_argument("--plugin-root", type=Path, default=plugin_root_from_script(), help="Path to this plugin root")
    parser.add_argument("--dest", type=Path, default=home() / ".codex" / "plugins" / PLUGIN_NAME, help="Destination plugin directory")
    parser.add_argument("--marketplace", type=Path, default=home() / ".agents" / "plugins" / "marketplace.json", help="Marketplace JSON path")
    parser.add_argument("--source-path", default=f"./.codex/plugins/{PLUGIN_NAME}", help="source.path to write in marketplace.json")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    root = args.plugin_root.expanduser().resolve()
    if not (root / ".codex-plugin" / "plugin.json").exists():
        print(f"Not a plugin root: {root}", file=sys.stderr)
        return 1
    run_validation(root)
    copy_plugin(root, args.dest.expanduser(), args.dry_run)
    update_marketplace(args.marketplace.expanduser(), args.source_path, args.dry_run)
    print("Done. Restart Codex, then open the plugin directory and install/enable 'Scholarly Research Book Skills'.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
