"""Tests for executable script safeguards."""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"


def load_module(script_name: str):
    path = SCRIPTS_DIR / script_name
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def run_script(script_name: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / script_name), *args],
        check=False,
        capture_output=True,
        text=True,
    )


def write_minimal_plugin(root: Path, *, skill_body: str | None = None) -> None:
    manifest_dir = root / ".codex-plugin"
    skill_dir = root / "skills" / "sample-skill"
    agents_dir = skill_dir / "agents"
    manifest_dir.mkdir(parents=True)
    agents_dir.mkdir(parents=True)
    (manifest_dir / "plugin.json").write_text(
        json.dumps(
            {
                "name": "sample-plugin",
                "version": "1.0.0",
                "description": "Sample plugin.",
                "skills": "./skills/",
            }
        ),
        encoding="utf-8",
    )
    (skill_dir / "SKILL.md").write_text(
        skill_body
        or "\n".join(
            [
                "---",
                "name: sample-skill",
                "description: Sample skill for validation.",
                "---",
                "# Sample Skill",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (skill_dir / "README.md").write_text("# sample-skill\n", encoding="utf-8")
    (agents_dir / "openai.yaml").write_text(
        "\n".join(
            [
                "interface:",
                '  display_name: "Sample Skill"',
                '  short_description: "Sample skill for validation."',
                '  default_prompt: "Use sample-skill."',
                "policy:",
                "  allow_implicit_invocation: true",
                "",
            ]
        ),
        encoding="utf-8",
    )


class TestExecutableSafeguards(unittest.TestCase):
    def test_package_excludes_generated_and_vcs_files(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "plugin"
            root.mkdir()
            (root / "keep.txt").write_text("keep", encoding="utf-8")
            (root / "old.zip").write_text("old", encoding="utf-8")
            (root / ".DS_Store").write_text("metadata", encoding="utf-8")
            (root / ".git").mkdir()
            (root / ".git" / "config").write_text("git", encoding="utf-8")
            (root / "__pycache__").mkdir()
            (root / "__pycache__" / "cache.pyc").write_bytes(b"cache")
            (root / ".pytest_cache").mkdir()
            (root / ".pytest_cache" / "state").write_text("cache", encoding="utf-8")
            (root / "dist").mkdir()
            (root / "dist" / "artifact.txt").write_text("dist", encoding="utf-8")
            (root / "build").mkdir()
            (root / "build" / "artifact.txt").write_text("build", encoding="utf-8")
            (root / "coverage").mkdir()
            (root / "coverage" / "summary.txt").write_text("coverage", encoding="utf-8")
            output_path = root / "bundle.zip"

            result = run_script("package_plugin.py", "--root", str(root), "--out", str(output_path))

            self.assertEqual(result.returncode, 0, msg=f"stdout={result.stdout} stderr={result.stderr}")
            with zipfile.ZipFile(output_path) as archive:
                names = archive.namelist()
            self.assertIn(f"{root.name}/keep.txt", names)
            self.assertNotIn(f"{root.name}/bundle.zip", names)
            self.assertFalse(any("/.git/" in name for name in names))
            self.assertFalse(any(name.endswith(".zip") for name in names))
            self.assertFalse(any("__pycache__" in name for name in names))
            self.assertFalse(any(name.endswith(".DS_Store") for name in names))
            self.assertFalse(any(".pytest_cache" in name for name in names))
            self.assertFalse(any("/dist/" in name for name in names))
            self.assertFalse(any("/build/" in name for name in names))
            self.assertFalse(any("/coverage/" in name for name in names))

    def test_package_default_output_uses_manifest_version(self) -> None:
        packager = load_module("package_plugin.py")

        self.assertEqual(
            packager.default_output_path(ROOT).name,
            "scholarly-research-book-plugin-v1.0.0.zip",
        )

    def test_installer_refuses_to_replace_unexpected_destination(self) -> None:
        installer = load_module("install_codex_plugin.py")
        with TemporaryDirectory() as temporary_directory:
            destination = Path(temporary_directory) / "important-folder"
            destination.mkdir()
            sentinel = destination / "keep.txt"
            sentinel.write_text("do not delete", encoding="utf-8")

            with self.assertRaises(ValueError):
                installer.copy_plugin(ROOT, destination, dry_run=False)

            self.assertTrue(sentinel.exists())

    def test_installer_excludes_generated_files(self) -> None:
        installer = load_module("install_codex_plugin.py")
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "source" / "sample-plugin"
            write_minimal_plugin(root)
            (root / ".pytest_cache").mkdir()
            (root / ".pytest_cache" / "state").write_text("cache", encoding="utf-8")
            (root / "dist").mkdir()
            (root / "dist" / "artifact.txt").write_text("dist", encoding="utf-8")
            (root / "debug.log").write_text("log", encoding="utf-8")
            destination = Path(temporary_directory) / "sample-plugin"

            installer.copy_plugin(root, destination, dry_run=False)

            self.assertTrue((destination / ".codex-plugin" / "plugin.json").exists())
            self.assertFalse((destination / ".pytest_cache").exists())
            self.assertFalse((destination / "dist").exists())
            self.assertFalse((destination / "debug.log").exists())

    def test_validate_script_uses_unittest_discovery(self) -> None:
        text = (ROOT / "validate.sh").read_text(encoding="utf-8")
        self.assertIn("-m unittest discover", text)

    def test_validator_requires_skill_readme_and_agent_metadata(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_minimal_plugin(root)
            (root / "skills" / "sample-skill" / "README.md").unlink()
            (root / "skills" / "sample-skill" / "agents" / "openai.yaml").unlink()

            result = run_script("validate_plugin.py", str(root))

            self.assertEqual(result.returncode, 1)
            self.assertIn("missing README.md", result.stdout)
            self.assertIn("missing agents/openai.yaml", result.stdout)

    def test_validator_rejects_broken_local_asset_references(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_minimal_plugin(
                root,
                skill_body="\n".join(
                    [
                        "---",
                        "name: sample-skill",
                        "description: Sample skill for validation.",
                        "---",
                        "# Sample Skill",
                        "",
                        "Use [missing template](assets/missing-template.md).",
                    ]
                ),
            )

            result = run_script("validate_plugin.py", str(root))

            self.assertEqual(result.returncode, 1)
            self.assertIn("broken local reference", result.stdout)

    def test_validator_rejects_any_broken_relative_markdown_link(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_minimal_plugin(
                root,
                skill_body="\n".join(
                    [
                        "---",
                        "name: sample-skill",
                        "description: Sample skill for validation.",
                        "---",
                        "# Sample Skill",
                        "",
                        "Use [missing project doc](docs/missing.md).",
                    ]
                ),
            )

            result = run_script("validate_plugin.py", str(root))

            self.assertEqual(result.returncode, 1)
            self.assertIn("broken local reference", result.stdout)

    def test_validator_rejects_broken_backtick_path_reference(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_minimal_plugin(
                root,
                skill_body="\n".join(
                    [
                        "---",
                        "name: sample-skill",
                        "description: Sample skill for validation.",
                        "---",
                        "# Sample Skill",
                        "",
                        "Read `docs/missing.md` before using this skill.",
                    ]
                ),
            )

            result = run_script("validate_plugin.py", str(root))

            self.assertEqual(result.returncode, 1)
            self.assertIn("broken local reference", result.stdout)

    def test_validator_requires_structured_agent_metadata(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_minimal_plugin(root)
            (root / "skills" / "sample-skill" / "agents" / "openai.yaml").write_text(
                "\n".join(
                    [
                        'short_description: "Sample skill for validation."',
                        'default_prompt: "Use sample-skill."',
                        "allow_implicit_invocation: true",
                        "",
                    ]
                ),
                encoding="utf-8",
            )

            result = run_script("validate_plugin.py", str(root))

            self.assertEqual(result.returncode, 1)
            self.assertIn("missing interface.short_description", result.stdout)

    def test_validator_requires_boolean_agent_invocation_policy(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_minimal_plugin(root)
            (root / "skills" / "sample-skill" / "agents" / "openai.yaml").write_text(
                "\n".join(
                    [
                        "interface:",
                        '  display_name: "Sample Skill"',
                        '  short_description: "Sample skill for validation."',
                        '  default_prompt: "Use sample-skill."',
                        "policy:",
                        '  allow_implicit_invocation: "true"',
                        "",
                    ]
                ),
                encoding="utf-8",
            )

            result = run_script("validate_plugin.py", str(root))

            self.assertEqual(result.returncode, 1)
            self.assertIn("policy.allow_implicit_invocation must be boolean", result.stdout)


if __name__ == "__main__":
    unittest.main()
