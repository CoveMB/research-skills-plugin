"""Tests for the versioned Git marketplace contract."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check_marketplace import validate_marketplace


def write_manifest(root: Path, version: str = "1.1.0") -> None:
    manifest_path = root / ".codex-plugin" / "plugin.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(
            {
                "name": "research-skills-plugin",
                "version": version,
                "description": "Research skills.",
                "skills": "./skills/",
                "interface": {"category": "Productivity"},
            }
        ),
        encoding="utf-8",
    )


def marketplace_payload(version: str = "1.1.0") -> dict:
    return {
        "name": "covemb-research-skills",
        "interface": {"displayName": "CoveMB Research Skills"},
        "plugins": [
            {
                "name": "research-skills-plugin",
                "source": {
                    "source": "url",
                    "url": "https://github.com/CoveMB/research-skills-plugin.git",
                    "ref": f"v{version}",
                },
                "policy": {
                    "installation": "AVAILABLE",
                    "authentication": "ON_INSTALL",
                },
                "category": "Productivity",
            }
        ],
    }


def write_marketplace(root: Path, payload: dict) -> None:
    path = root / ".agents" / "plugins" / "marketplace.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


class TestMarketplace(unittest.TestCase):
    def test_repository_marketplace_is_valid(self) -> None:
        self.assertEqual(validate_marketplace(ROOT), [])

    def test_valid_versioned_git_marketplace(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_manifest(root)
            write_marketplace(root, marketplace_payload())

            self.assertEqual(validate_marketplace(root), [])

    def test_marketplace_ref_must_match_manifest_version(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_manifest(root)
            payload = marketplace_payload()
            payload["plugins"][0]["source"]["ref"] = "v1.0.0"
            write_marketplace(root, payload)

            errors = validate_marketplace(root)

            self.assertTrue(any("must equal 'v1.1.0'" in error for error in errors), errors)

    def test_marketplace_rejects_mutable_plugin_ref(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_manifest(root)
            payload = marketplace_payload()
            payload["plugins"][0]["source"]["ref"] = "main"
            write_marketplace(root, payload)

            errors = validate_marketplace(root)

            self.assertTrue(any("must equal 'v1.1.0'" in error for error in errors), errors)

    def test_marketplace_rejects_unexpected_repository(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_manifest(root)
            payload = marketplace_payload()
            payload["plugins"][0]["source"]["url"] = "https://example.com/plugin.git"
            write_marketplace(root, payload)

            errors = validate_marketplace(root)

            self.assertTrue(any("repository URL" in error for error in errors), errors)

    def test_marketplace_requires_install_policy(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_manifest(root)
            payload = marketplace_payload()
            del payload["plugins"][0]["policy"]["installation"]
            write_marketplace(root, payload)

            errors = validate_marketplace(root)

            self.assertTrue(any("policy.installation" in error for error in errors), errors)

    def test_manifest_version_must_be_semver(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_manifest(root, version="next")
            write_marketplace(root, marketplace_payload(version="next"))

            errors = validate_marketplace(root)

            self.assertTrue(any("valid semantic version" in error for error in errors), errors)

    def test_marketplace_rejects_duplicate_json_keys(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_manifest(root)
            path = root / ".agents" / "plugins" / "marketplace.json"
            path.parent.mkdir(parents=True)
            path.write_text(
                '{"name":"first","name":"second","interface":{},"plugins":[]}',
                encoding="utf-8",
            )

            errors = validate_marketplace(root)

            self.assertTrue(any("duplicate JSON key" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
