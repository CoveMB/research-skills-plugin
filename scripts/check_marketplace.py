#!/usr/bin/env python3
"""Validate the repository's versioned Git marketplace metadata."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


MARKETPLACE_PATH = Path(".agents/plugins/marketplace.json")
MANIFEST_PATH = Path(".codex-plugin/plugin.json")
EXPECTED_MARKETPLACE_NAME = "covemb-research-skills"
EXPECTED_MARKETPLACE_DISPLAY_NAME = "CoveMB Research Skills"
EXPECTED_REPOSITORY_URL = "https://github.com/CoveMB/research-skills-plugin.git"
EXPECTED_INSTALLATION_POLICY = "AVAILABLE"
EXPECTED_AUTHENTICATION_POLICY = "ON_INSTALL"
SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\."
    r"(0|[1-9]\d*)\."
    r"(0|[1-9]\d*)"
    r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$"
)


def load_json_with_unique_keys(path: Path) -> Any:
    def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"{path}: duplicate JSON key {key!r}")
            result[key] = value
        return result

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)


def load_json_object(path: Path, errors: list[str]) -> dict[str, Any] | None:
    if not path.is_file():
        errors.append(f"missing required file: {path}")
        return None
    try:
        payload = load_json_with_unique_keys(path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        errors.append(str(error))
        return None
    if not isinstance(payload, dict):
        errors.append(f"{path}: JSON root must be an object")
        return None
    return payload


def nested_mapping(payload: dict[str, Any], key: str) -> dict[str, Any]:
    value = payload.get(key)
    return value if isinstance(value, dict) else {}


def validate_manifest(root: Path, errors: list[str]) -> dict[str, Any] | None:
    manifest = load_json_object(root / MANIFEST_PATH, errors)
    if manifest is None:
        return None
    version = manifest.get("version")
    if not isinstance(version, str) or not SEMVER_RE.fullmatch(version):
        errors.append(f"{MANIFEST_PATH}: version must be a valid semantic version")
    return manifest


def validate_marketplace_entry(
    entry: dict[str, Any],
    manifest: dict[str, Any],
    errors: list[str],
) -> None:
    plugin_name = manifest.get("name")
    plugin_version = manifest.get("version")
    if entry.get("name") != plugin_name:
        errors.append(f"{MARKETPLACE_PATH}: plugin name must match plugin.json name {plugin_name!r}")

    source = nested_mapping(entry, "source")
    if source.get("source") != "url":
        errors.append(f"{MARKETPLACE_PATH}: plugin source.source must be 'url'")
    if source.get("url") != EXPECTED_REPOSITORY_URL:
        errors.append(
            f"{MARKETPLACE_PATH}: plugin repository URL must be {EXPECTED_REPOSITORY_URL!r}"
        )
    expected_ref = f"v{plugin_version}"
    if source.get("ref") != expected_ref:
        errors.append(f"{MARKETPLACE_PATH}: plugin source.ref must equal {expected_ref!r}")
    unexpected_source_fields = sorted(set(source) - {"source", "url", "ref"})
    if unexpected_source_fields:
        errors.append(
            f"{MARKETPLACE_PATH}: unsupported plugin source fields: {unexpected_source_fields!r}"
        )

    policy = nested_mapping(entry, "policy")
    if policy.get("installation") != EXPECTED_INSTALLATION_POLICY:
        errors.append(
            f"{MARKETPLACE_PATH}: policy.installation must be "
            f"{EXPECTED_INSTALLATION_POLICY!r}"
        )
    if policy.get("authentication") != EXPECTED_AUTHENTICATION_POLICY:
        errors.append(
            f"{MARKETPLACE_PATH}: policy.authentication must be "
            f"{EXPECTED_AUTHENTICATION_POLICY!r}"
        )

    manifest_category = nested_mapping(manifest, "interface").get("category")
    if entry.get("category") != manifest_category:
        errors.append(
            f"{MARKETPLACE_PATH}: plugin category must match plugin.json interface.category"
        )


def validate_marketplace(root: Path) -> list[str]:
    root = root.expanduser().resolve()
    errors: list[str] = []
    manifest = validate_manifest(root, errors)
    marketplace = load_json_object(root / MARKETPLACE_PATH, errors)
    if manifest is None or marketplace is None:
        return errors

    if marketplace.get("name") != EXPECTED_MARKETPLACE_NAME:
        errors.append(
            f"{MARKETPLACE_PATH}: name must be {EXPECTED_MARKETPLACE_NAME!r}"
        )
    display_name = nested_mapping(marketplace, "interface").get("displayName")
    if display_name != EXPECTED_MARKETPLACE_DISPLAY_NAME:
        errors.append(
            f"{MARKETPLACE_PATH}: interface.displayName must be "
            f"{EXPECTED_MARKETPLACE_DISPLAY_NAME!r}"
        )

    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list):
        errors.append(f"{MARKETPLACE_PATH}: plugins must be an array")
        return errors
    if len(plugins) != 1 or not isinstance(plugins[0], dict):
        errors.append(f"{MARKETPLACE_PATH}: plugins must contain exactly one plugin object")
        return errors
    validate_marketplace_entry(plugins[0], manifest, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root. Defaults to this script's repository.",
    )
    args = parser.parse_args()
    errors = validate_marketplace(args.root)
    if errors:
        print("Marketplace validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Marketplace validation passed: {args.root.expanduser().resolve() / MARKETPLACE_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
