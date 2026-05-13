"""Tests for executable script safeguards."""
from __future__ import annotations

import importlib.util
import json
import os
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
                '  task_type: "research-book-skill"',
                '  data_access_level: "user-provided-or-public-metadata"',
                '  external_lookup_allowed: "conditional"',
                '  confidentiality_gate: "required-before-external-lookup"',
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
            (root / ".env").write_text("SECRET=1", encoding="utf-8")
            (root / "local-notes.txt").write_text("notes", encoding="utf-8")
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
            self.assertNotIn(f"{root.name}/.env", names)
            self.assertNotIn(f"{root.name}/local-notes.txt", names)
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

    def test_installer_refuses_to_copy_plugin_onto_itself(self) -> None:
        installer = load_module("install_codex_plugin.py")
        with TemporaryDirectory() as temporary_directory:
            source = Path(temporary_directory) / "sample-plugin"
            write_minimal_plugin(source)

            with self.assertRaises(ValueError):
                installer.copy_plugin(source, source, dry_run=False)

            self.assertTrue((source / ".codex-plugin" / "plugin.json").exists())

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
            (root / ".env").write_text("SECRET=1", encoding="utf-8")
            (root / "local-notes.txt").write_text("notes", encoding="utf-8")
            destination = Path(temporary_directory) / "sample-plugin"

            installer.copy_plugin(root, destination, dry_run=False)

            self.assertTrue((destination / ".codex-plugin" / "plugin.json").exists())
            self.assertFalse((destination / ".pytest_cache").exists())
            self.assertFalse((destination / "dist").exists())
            self.assertFalse((destination / "debug.log").exists())
            self.assertFalse((destination / ".env").exists())
            self.assertFalse((destination / "local-notes.txt").exists())

    def test_installer_builds_plan_without_writing(self) -> None:
        installer = load_module("install_codex_plugin.py")
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "sample-plugin"
            write_minimal_plugin(root)
            marketplace = Path(temporary_directory) / "marketplace.json"

            plan = installer.build_install_plan(
                plugin_root=root,
                dest=None,
                marketplace=marketplace,
                source_path=None,
            )

            self.assertEqual(plan.root, root.resolve())
            self.assertEqual(plan.plugin_name_value, "sample-plugin")
            self.assertEqual(plan.dest, installer.home() / ".codex" / "plugins" / "sample-plugin")
            self.assertEqual(plan.marketplace, marketplace)
            self.assertEqual(plan.source_path, "./.codex/plugins/sample-plugin")
            self.assertFalse(marketplace.exists())

    def test_installer_keeps_existing_destination_when_copy_fails(self) -> None:
        installer = load_module("install_codex_plugin.py")
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "source" / "sample-plugin"
            destination = root / "sample-plugin"
            write_minimal_plugin(source)
            write_minimal_plugin(destination)
            sentinel = destination / "keep.txt"
            sentinel.write_text("keep", encoding="utf-8")

            original_copy_package_tree = installer.copy_package_tree

            def fail_copy_package_tree(*_args, **_kwargs):
                raise RuntimeError("copy failed")

            installer.copy_package_tree = fail_copy_package_tree
            try:
                with self.assertRaises(RuntimeError):
                    installer.copy_plugin(source, destination, dry_run=False)
            finally:
                installer.copy_package_tree = original_copy_package_tree

            self.assertTrue(sentinel.exists())

    def test_installer_dry_run_does_not_backup_malformed_marketplace(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            marketplace = root / "marketplace.json"
            marketplace.write_text("{not valid json", encoding="utf-8")

            result = run_script(
                "install_codex_plugin.py",
                "--plugin-root",
                str(ROOT),
                "--dest",
                str(root / "scholarly-research-book"),
                "--marketplace",
                str(marketplace),
                "--dry-run",
            )

            self.assertEqual(result.returncode, 0, msg=f"stdout={result.stdout} stderr={result.stderr}")
            self.assertEqual(marketplace.read_text(encoding="utf-8"), "{not valid json")
            self.assertEqual(list(root.glob("marketplace.json.backup-*")), [])

    def test_marketplace_write_failure_keeps_existing_file(self) -> None:
        installer = load_module("install_codex_plugin.py")
        with TemporaryDirectory() as temporary_directory:
            marketplace = Path(temporary_directory) / "marketplace.json"
            original_text = json.dumps(
                {
                    "name": "local-personal-plugins",
                    "interface": {"displayName": "Local Personal Plugins"},
                    "plugins": [],
                },
                indent=2,
            ) + "\n"
            marketplace.write_text(original_text, encoding="utf-8")
            original_write_text = Path.write_text

            def fail_write_text(self, *_args, **_kwargs):
                original_write_text(self, "partial", encoding="utf-8")
                raise RuntimeError("write failed")

            Path.write_text = fail_write_text
            try:
                with self.assertRaises(RuntimeError):
                    installer.update_marketplace(
                        marketplace,
                        "sample-plugin",
                        "./.codex/plugins/sample-plugin",
                        dry_run=False,
                    )
            finally:
                Path.write_text = original_write_text

            self.assertEqual(marketplace.read_text(encoding="utf-8"), original_text)

    def test_marketplace_sample_matches_installer_defaults(self) -> None:
        installer = load_module("install_codex_plugin.py")
        sample = json.loads((ROOT / "marketplace.sample.json").read_text(encoding="utf-8"))

        self.assertEqual(sample["name"], installer.MARKETPLACE_NAME)
        self.assertEqual(sample["interface"]["displayName"], "Local Personal Plugins")

    def test_plugin_utils_parse_nested_metadata_yaml(self) -> None:
        plugin_utils = load_module("plugin_utils.py")

        metadata = plugin_utils.parse_simple_yaml_mapping(
            "\n".join(
                [
                    "interface:",
                    '  display_name: "Sample Skill"',
                    "policy:",
                    "  allow_implicit_invocation: true",
                    "",
                ]
            )
        )

        self.assertEqual(
            plugin_utils.nested_string(plugin_utils.nested_mapping(metadata, "interface"), "display_name"),
            "Sample Skill",
        )
        self.assertIs(
            plugin_utils.nested_mapping(metadata, "policy")["allow_implicit_invocation"],
            True,
        )

    def test_plugin_utils_reports_malformed_json_location(self) -> None:
        plugin_utils = load_module("plugin_utils.py")
        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "broken.json"
            path.write_text("{broken", encoding="utf-8")

            payload, error = plugin_utils.load_json_object_result(path)

            self.assertIsNone(payload)
            self.assertIn("malformed JSON at line 1, column 2", error)

    def test_plugin_utils_scores_significant_description_terms(self) -> None:
        plugin_utils = load_module("plugin_utils.py")

        terms = plugin_utils.significant_description_terms(
            "Scholarly research skill maps chapter evidence, argument continuity, and citation gaps."
        )

        self.assertNotIn("skill", terms)
        self.assertNotIn("research", terms)
        self.assertIn("chapter", terms)
        self.assertIn("evidence", terms)
        self.assertGreater(plugin_utils.MIN_SHARED_DESCRIPTION_TERMS, 0)

    def test_plugin_utils_exposes_contract_artifact_skill_map(self) -> None:
        plugin_utils = load_module("plugin_utils.py")

        self.assertEqual(
            plugin_utils.CONTRACT_ARTIFACT_SKILLS["chapter-architecture"],
            "chapter_brief",
        )
        self.assertEqual(
            plugin_utils.CONTRACT_ARTIFACT_SKILLS["claim-evidence-ledger"],
            "claim_evidence_ledger",
        )

    def test_gitignore_tracks_generated_file_exclusions(self) -> None:
        plugin_utils = load_module("plugin_utils.py")
        ignored_patterns = {
            line.strip().rstrip("/")
            for line in (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        }
        expected_patterns = [
            pattern
            for pattern in plugin_utils.generated_file_patterns()
            if pattern != ".git"
        ]

        missing = [
            pattern
            for pattern in expected_patterns
            if pattern.rstrip("/") not in ignored_patterns
        ]
        self.assertEqual(missing, [])

    def test_validate_script_uses_unittest_discovery(self) -> None:
        text = (ROOT / "validate.sh").read_text(encoding="utf-8")
        self.assertIn("-m unittest discover", text)

    def test_install_shell_requires_python_310_or_newer(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            fake_bin = Path(temporary_directory)
            fake_python = fake_bin / "python3"
            fake_python.write_text(
                "\n".join(
                    [
                        "#!/usr/bin/env sh",
                        'if [ "$1" = "-c" ]; then',
                        "  exit 1",
                        "fi",
                        "exit 0",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            fake_python.chmod(0o755)
            env = {**os.environ, "PATH": f"{fake_bin}{os.pathsep}{os.environ['PATH']}"}

            result = subprocess.run(
                ["bash", str(ROOT / "install.sh"), "--dry-run"],
                check=False,
                capture_output=True,
                text=True,
                env=env,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Python 3.10", result.stderr)

    def test_install_powershell_has_python_version_preflight(self) -> None:
        text = (ROOT / "install.ps1").read_text(encoding="utf-8")
        self.assertIn("Python 3.10", text)
        self.assertIn("sys.version_info", text)

    def test_executable_scripts_explain_help(self) -> None:
        expected_help = {
            "validate_plugin.py": [
                "Validate a local skills plugin package.",
                "plugin_root",
            ],
            "check_book_artifact_contract.py": [
                "Validate book artifact schema and shipped examples.",
                "--path",
            ],
            "check_research_behavior_fixtures.py": [
                "Check research behavior fixture documents and captured local outputs.",
                "--fixtures",
            ],
            "check_citation_metadata.py": [
                "Check local citation metadata exports without network lookup or private text.",
                "--input",
            ],
            "package_plugin.py": [
                "Package this plugin directory as a zip.",
                "--out",
            ],
            "install_codex_plugin.py": [
                "Install Research Book Skills Plugin locally.",
                "--dry-run",
            ],
        }

        for script_name, expected_snippets in expected_help.items():
            with self.subTest(script_name=script_name):
                result = run_script(script_name, "--help")

                self.assertEqual(result.returncode, 0, msg=f"stdout={result.stdout} stderr={result.stderr}")
                self.assertIn("usage:", result.stdout)
                for expected_snippet in expected_snippets:
                    self.assertIn(expected_snippet, result.stdout)

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

    def test_validator_rejects_missing_manifest_asset_references(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_minimal_plugin(root)
            manifest_path = root / ".codex-plugin" / "plugin.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["interface"] = {
                "composerIcon": "./assets/missing-icon.svg",
                "logo": "./assets/missing-logo.svg",
            }
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            result = run_script("validate_plugin.py", str(root))

            self.assertEqual(result.returncode, 1)
            self.assertIn("plugin.json: broken local reference", result.stdout)

    def test_validator_rejects_broken_local_references_in_skill_assets(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_minimal_plugin(root)
            assets_dir = root / "skills" / "sample-skill" / "assets"
            assets_dir.mkdir()
            (assets_dir / "template.md").write_text(
                "See [missing guidance](docs/missing.md).",
                encoding="utf-8",
            )

            result = run_script("validate_plugin.py", str(root))

            self.assertEqual(result.returncode, 1)
            self.assertIn("template.md: broken local reference", result.stdout)

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

    def test_validator_requires_source_privacy_policy_metadata(self) -> None:
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
                        "  allow_implicit_invocation: true",
                        "",
                    ]
                ),
                encoding="utf-8",
            )

            result = run_script("validate_plugin.py", str(root))

            self.assertEqual(result.returncode, 1)
            self.assertIn("policy.data_access_level", result.stdout)
            self.assertIn("policy.external_lookup_allowed", result.stdout)
            self.assertIn("policy.confidentiality_gate", result.stdout)

    def test_validator_rejects_stale_agent_display_name(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            description = (
                "Sample skill validates metadata display routing coverage source evidence "
                "workflow planning audit chapter argument continuity."
            )
            write_minimal_plugin(
                root,
                skill_body="\n".join(
                    [
                        "---",
                        "name: sample-skill",
                        f"description: {description}",
                        "---",
                        "# Sample Skill",
                        "",
                    ]
                ),
            )
            (root / "skills" / "sample-skill" / "agents" / "openai.yaml").write_text(
                "\n".join(
                    [
                        "interface:",
                        '  display_name: "Unrelated Metadata"',
                        f'  short_description: "{description}"',
                        '  default_prompt: "Use sample-skill."',
                        "policy:",
                        "  allow_implicit_invocation: true",
                        "",
                    ]
                ),
                encoding="utf-8",
            )

            result = run_script("validate_plugin.py", str(root))

            self.assertEqual(result.returncode, 1)
            self.assertIn("display_name appears stale", result.stdout)


if __name__ == "__main__":
    unittest.main()
