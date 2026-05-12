"""Shared helpers for plugin maintenance scripts."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

EXCLUDED_DIRECTORIES = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "htmlcov",
    "node_modules",
    "venv",
}
EXCLUDED_FILE_NAMES = {".DS_Store"}
EXCLUDED_SUFFIXES = {".log", ".pyc", ".zip", ".tmp"}


def load_json_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} root must be an object")
    return payload


def plugin_manifest_path(root: Path) -> Path:
    return root / ".codex-plugin" / "plugin.json"


def load_plugin_manifest(root: Path) -> dict[str, Any]:
    return load_json_object(plugin_manifest_path(root))


def plugin_name(root: Path) -> str:
    return str(load_plugin_manifest(root).get("name", ""))


def plugin_version(root: Path) -> str:
    return str(load_plugin_manifest(root).get("version", ""))


def generated_file_patterns() -> list[str]:
    return [
        *sorted(EXCLUDED_DIRECTORIES),
        *sorted(EXCLUDED_FILE_NAMES),
        *(f"*{suffix}" for suffix in sorted(EXCLUDED_SUFFIXES)),
    ]
