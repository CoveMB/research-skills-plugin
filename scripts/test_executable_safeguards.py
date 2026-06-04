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
    skill_description = (
        "Sample skill validates metadata display routing coverage evidence workflow "
        "planning audit chapter argument continuity."
    )
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
                f"description: {skill_description}",
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
                f'  short_description: "{skill_description}"',
                '  default_prompt: "Use sample-skill."',
                *load_module("plugin_utils.py").agent_policy_yaml_lines("sample-skill"),
                "",
            ]
        ),
        encoding="utf-8",
    )


class TestExecutableSafeguards(unittest.TestCase):
    def test_package_excludes_generated_and_vcs_files(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            packager = load_module("package_plugin.py")
            root = Path(temporary_directory) / "plugin"
            write_minimal_plugin(root)
            (root / ".env").write_text("SECRET=1", encoding="utf-8")
            (root / "local-notes.txt").write_text("notes", encoding="utf-8")
            (root / "skills" / "sample-skill" / ".env").write_text("SECRET=2", encoding="utf-8")
            (root / "docs").mkdir()
            (root / "docs" / "local-notes.txt").write_text("notes", encoding="utf-8")
            (root / "skills" / "sample-skill" / "secrets.json").write_text("{}", encoding="utf-8")
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
            archive_prefix = packager.package_archive_prefix(root)
            self.assertEqual(archive_prefix, "sample-plugin")
            self.assertTrue(any(name.startswith(f"{archive_prefix}/") for name in names))
            self.assertFalse(any(name.startswith(f"{root.name}/") for name in names))
            self.assertNotIn(f"{archive_prefix}/.env", names)
            self.assertNotIn(f"{archive_prefix}/local-notes.txt", names)
            self.assertNotIn(f"{archive_prefix}/skills/sample-skill/.env", names)
            self.assertNotIn(f"{archive_prefix}/docs/local-notes.txt", names)
            self.assertNotIn(f"{archive_prefix}/skills/sample-skill/secrets.json", names)
            self.assertNotIn(f"{archive_prefix}/bundle.zip", names)
            self.assertFalse(any("/.git/" in name for name in names))
            self.assertFalse(any(name.endswith(".zip") for name in names))
            self.assertFalse(any("__pycache__" in name for name in names))
            self.assertFalse(any(name.endswith(".DS_Store") for name in names))
            self.assertFalse(any(".pytest_cache" in name for name in names))
            self.assertFalse(any("/dist/" in name for name in names))
            self.assertFalse(any("/build/" in name for name in names))
            self.assertFalse(any("/coverage/" in name for name in names))

    def test_package_and_installer_exclude_symlinked_files(self) -> None:
        installer = load_module("install_codex_plugin.py")
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "plugin"
            write_minimal_plugin(root)
            docs_dir = root / "docs"
            docs_dir.mkdir()
            outside_file = Path(temporary_directory) / "outside-secret.md"
            outside_file.write_text("secret", encoding="utf-8")
            linked_file = docs_dir / "linked-secret.md"
            try:
                linked_file.symlink_to(outside_file)
            except (NotImplementedError, OSError) as error:
                self.skipTest(f"symlink creation unavailable: {error}")

            output_path = Path(temporary_directory) / "bundle.zip"
            result = run_script("package_plugin.py", "--root", str(root), "--out", str(output_path))
            destination = Path(temporary_directory) / "sample-plugin"
            installer.copy_plugin(root, destination, dry_run=False)

            self.assertEqual(result.returncode, 0, msg=f"stdout={result.stdout} stderr={result.stderr}")
            with zipfile.ZipFile(output_path) as archive:
                names = archive.namelist()
            self.assertNotIn("sample-plugin/docs/linked-secret.md", names)
            self.assertFalse((destination / "docs" / "linked-secret.md").exists())

    def test_package_validates_plugin_before_writing_zip(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "plugin"
            write_minimal_plugin(root)
            (root / "skills" / "sample-skill" / "SKILL.md").write_text(
                "\n".join(
                    [
                        "---",
                        "name: wrong-skill",
                        "description: Sample skill for validation.",
                        "---",
                        "# Sample Skill",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            output_path = Path(temporary_directory) / "bundle.zip"

            result = run_script("package_plugin.py", "--root", str(root), "--out", str(output_path))

            self.assertEqual(result.returncode, 1)
            self.assertIn("frontmatter name", result.stdout)
            self.assertFalse(output_path.exists())

    def test_package_default_output_uses_manifest_version(self) -> None:
        packager = load_module("package_plugin.py")

        self.assertEqual(
            packager.default_output_path(ROOT).name,
            "research-skills-plugin-v1.0.0.zip",
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

    def test_installer_refuses_existing_file_destination(self) -> None:
        installer = load_module("install_codex_plugin.py")
        with TemporaryDirectory() as temporary_directory:
            source = Path(temporary_directory) / "source" / "sample-plugin"
            destination = Path(temporary_directory) / "sample-plugin"
            write_minimal_plugin(source)
            destination.write_text("not a directory", encoding="utf-8")

            with self.assertRaises(ValueError):
                installer.copy_plugin(source, destination, dry_run=False)

            self.assertEqual(destination.read_text(encoding="utf-8"), "not a directory")

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
                str(root / "research-skills-plugin"),
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

    def test_marketplace_helpers_normalize_and_replace_entries(self) -> None:
        installer = load_module("install_codex_plugin.py")

        normalized = installer.normalize_marketplace_data({"plugins": "not a list"})
        entry = installer.marketplace_entry("sample-plugin", "./.codex/plugins/sample-plugin")
        updated = installer.replace_marketplace_entry(
            {
                **normalized,
                "plugins": [
                    {"name": "other-plugin"},
                    {"name": "sample-plugin", "source": {"path": "old"}},
                ],
            },
            entry,
        )

        self.assertEqual(normalized["name"], installer.MARKETPLACE_NAME)
        self.assertEqual(normalized["interface"]["displayName"], "Local Personal Plugins")
        self.assertEqual(normalized["plugins"], [])
        self.assertEqual([plugin["name"] for plugin in updated["plugins"]], ["other-plugin", "sample-plugin"])
        self.assertEqual(updated["plugins"][-1]["source"]["path"], "./.codex/plugins/sample-plugin")

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

    def test_plugin_utils_parse_markdown_frontmatter(self) -> None:
        plugin_utils = load_module("plugin_utils.py")

        metadata = plugin_utils.parse_markdown_frontmatter(
            "\n".join(
                [
                    "---",
                    "name: sample-skill",
                    "description: Sample skill for validation.",
                    "metadata:",
                    '  version: "1.0.0"',
                    "---",
                    "# Sample Skill",
                    "",
                ]
            )
        )

        self.assertEqual(metadata["name"], "sample-skill")
        self.assertEqual(metadata["metadata"]["version"], "1.0.0")

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

    def test_plugin_utils_exposes_shared_skill_policy_snippets(self) -> None:
        plugin_utils = load_module("plugin_utils.py")

        self.assertIn("docs/policy/SOURCE_LIMITS.md", plugin_utils.SOURCE_LIMITS_POLICY_SENTENCE)
        self.assertIn("Suggested next step", plugin_utils.SUGGESTED_NEXT_STEP_POLICY_SENTENCE)
        self.assertIn("source_basis", plugin_utils.PROVENANCE_FIELDS)
        self.assertIn("Use `skill-name` to [specific next action].", plugin_utils.SUGGESTED_NEXT_STEP_TEMPLATE_PHRASES)
        self.assertEqual(
            plugin_utils.machine_readable_artifact_sentence("chapter_brief"),
            "When the user explicitly asks for JSON or a contract artifact, use "
            "`shared/contracts/book/book_artifact.schema.json` with `artifact_type: chapter_brief`. "
            "If the output is normal Markdown, do not force the JSON contract. "
            "For durable handoff artifacts, follow `docs/policy/PROCESS_PASSPORT.md`: "
            "set `handoff_artifact: true`, include `process_passport`, and "
            "preserve upstream passport limits instead of upgrading verification.",
        )

    def test_plugin_utils_exposes_shared_agent_policy(self) -> None:
        plugin_utils = load_module("plugin_utils.py")

        self.assertEqual(
            plugin_utils.REQUIRED_AGENT_POLICY["task_type"],
            "research-book-skill",
        )
        self.assertEqual(
            plugin_utils.agent_policy_fields("citation-integrity-auditor")["external_lookup_allowed"],
            "conditional",
        )
        self.assertEqual(
            plugin_utils.agent_policy_fields("research-book-orchestrator")["external_lookup_allowed"],
            "route-only",
        )
        self.assertEqual(
            plugin_utils.agent_policy_fields("chapter-architecture")["external_lookup_allowed"],
            "none",
        )
        self.assertIn(
            '  confidentiality_gate: "required-before-external-lookup"',
            plugin_utils.agent_policy_yaml_lines("citation-integrity-auditor"),
        )
        self.assertIn(
            '  allowed_external_payloads: "public-identifiers-search-terms-and-nonsensitive-short-summaries"',
            plugin_utils.agent_policy_yaml_lines("citation-integrity-auditor"),
        )
        self.assertIn(
            "  lookup_consent_required: true",
            plugin_utils.agent_policy_yaml_lines("citation-integrity-auditor"),
        )

    def test_artifact_boundary_rules_are_shared(self) -> None:
        plugin_utils = load_module("plugin_utils.py")
        checker = load_module("check_book_artifact_contract.py")
        schema = json.loads((ROOT / "shared" / "contracts" / "book" / "book_artifact.schema.json").read_text(encoding="utf-8"))

        self.assertEqual(checker.COMMON_ARTIFACT_FIELDS, plugin_utils.COMMON_ARTIFACT_FIELDS)
        self.assertIn(
            "analysis_provenance",
            checker.artifact_type_field_boundaries(schema)["claim_evidence_ledger"],
        )
        self.assertEqual(
            set(checker.artifact_type_field_boundaries(schema)),
            set(plugin_utils.CONTRACT_ARTIFACT_SKILLS.values()),
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

    def test_gitignore_excludes_real_goldset_pdf_caches(self) -> None:
        text = (ROOT / ".gitignore").read_text(encoding="utf-8")

        self.assertIn("tests/skill_evals/scholar_grade/real_goldsets/intake/*/PDFs/", text)

    def test_validate_script_uses_unittest_discovery(self) -> None:
        text = (ROOT / "validate.sh").read_text(encoding="utf-8")
        self.assertIn("run_package_checks.py", text)
        self.assertIn("--scope full", text)
        self.assertIn("--scope package", text)
        self.assertIn("tests/skill_evals", text)

    def test_package_validation_scope_uses_only_packaged_assets(self) -> None:
        module = load_module("run_package_checks.py")
        package_check_text = "\n".join(" ".join(check) for check in module.checks_for_scope("package"))

        self.assertIn("scripts/validate_plugin.py", package_check_text)
        self.assertIn("scripts/check_book_artifact_contract.py", package_check_text)
        self.assertNotIn("tests/skill_evals", package_check_text)

    def test_full_validation_runner_checks_source_candidates(self) -> None:
        text = (SCRIPTS_DIR / "run_package_checks.py").read_text(encoding="utf-8")
        self.assertIn("check_source_candidates.py", text)
        self.assertIn("tests/skill_evals/source-candidates.json", text)

    def test_full_validation_runner_checks_research_behavior_route_traces(self) -> None:
        text = (SCRIPTS_DIR / "run_package_checks.py").read_text(encoding="utf-8")

        self.assertIn("summarize_research_behavior_evals.py", text)
        self.assertIn("--traces-dir", text)
        self.assertIn("tests/skill_evals/research_behavior/traces", text)

    def test_full_validation_runner_checks_workflow_passport_fixtures(self) -> None:
        text = (SCRIPTS_DIR / "run_package_checks.py").read_text(encoding="utf-8")

        self.assertIn("check_workflow_passport_fixtures.py", text)
        self.assertIn("tests/skill_evals/workflow_passports/fixtures.json", text)

    def test_full_validation_runner_checks_workflow_traceability(self) -> None:
        text = (SCRIPTS_DIR / "run_package_checks.py").read_text(encoding="utf-8")

        self.assertIn("check_workflow_traceability.py", text)
        self.assertIn("tests/skill_evals/workflow_traces/claim-lineage-fixture/workflow-trace.json", text)

    def test_skill_evaluation_assets_live_under_tests(self) -> None:
        expected_paths = [
            ROOT / "tests" / "skill_evals" / "README.md",
            ROOT / "tests" / "skill_evals" / "research_behavior" / "fixtures.json",
            ROOT / "tests" / "skill_evals" / "research_behavior" / "outputs",
            ROOT / "tests" / "skill_evals" / "workflow_passports" / "fixtures.json",
            ROOT / "tests" / "skill_evals" / "workflow_traces" / "claim-lineage-fixture" / "workflow-trace.json",
            ROOT / "tests" / "skill_evals" / "scholar_grade" / "fixtures.json",
            ROOT / "tests" / "skill_evals" / "scholar_grade" / "corpora",
            ROOT / "tests" / "skill_evals" / "scholar_grade" / "outputs",
            ROOT / "tests" / "skill_evals" / "scholar_grade" / "scholar_grade_eval_harness.py",
        ]

        for path in expected_paths:
            with self.subTest(path=path):
                self.assertTrue(path.exists(), msg=f"Missing expected skill eval path: {path}")

    def test_full_validation_runner_checks_scholar_grade_skill_evals(self) -> None:
        text = (SCRIPTS_DIR / "run_package_checks.py").read_text(encoding="utf-8")

        self.assertIn("tests/skill_evals/scholar_grade/scholar_grade_eval_harness.py", text)
        self.assertIn("tests/skill_evals/scholar_grade/fixtures.json", text)
        self.assertIn("tests/skill_evals/scholar_grade/outputs", text)
        self.assertNotIn("examples/evals/scholar-grade-fixtures.json", text)

    def test_live_pilot_v7_scope_points_at_v7_root(self) -> None:
        module = load_module("run_package_checks.py")

        check_text = "\n".join(" ".join(check) for check in module.checks_for_scope("live-pilot-v7"))

        self.assertIn("tests/skill_evals/scholar_grade/live_pilot_v7/outputs", check_text)
        self.assertIn("tests/skill_evals/scholar_grade/live_pilot_v7/manifests", check_text)
        self.assertIn("tests/skill_evals/scholar_grade/live_pilot_v7/scores", check_text)
        self.assertIn("tests/skill_evals/scholar_grade/live_pilot_v7/fixture-ids.json", check_text)

    def test_workflow_passport_live_v1_scope_points_at_live_outputs(self) -> None:
        module = load_module("run_package_checks.py")

        check_text = "\n".join(" ".join(check) for check in module.checks_for_scope("workflow-passport-live-v1"))

        self.assertIn("scripts/check_workflow_passport_fixtures.py", check_text)
        self.assertIn("tests/skill_evals/workflow_passports/fixtures.json", check_text)
        self.assertIn("--actual-output-root", check_text)
        self.assertIn("tests/skill_evals/workflow_passports/live_pilot_v1/outputs", check_text)

    def test_validation_runner_exposes_non_default_live_capture_scope(self) -> None:
        text = (SCRIPTS_DIR / "run_package_checks.py").read_text(encoding="utf-8")

        self.assertIn('"live"', text)
        self.assertIn("--require-live-captures", text)

    def test_validation_runner_exposes_additive_live_pilot_scope(self) -> None:
        text = (SCRIPTS_DIR / "run_package_checks.py").read_text(encoding="utf-8")

        self.assertIn('"live-pilot"', text)
        self.assertIn("tests/skill_evals/scholar_grade/live_pilot_calibration.py", text)
        self.assertIn("tests/skill_evals/scholar_grade/live_pilot/fixture-ids.json", text)
        self.assertIn("tests/skill_evals/scholar_grade/live_pilot", text)
        self.assertIn("markdown", text)

    def test_validation_runner_exposes_additive_live_pilot_v2_scope(self) -> None:
        text = (SCRIPTS_DIR / "run_package_checks.py").read_text(encoding="utf-8")

        self.assertIn('"live-pilot-v2"', text)
        self.assertIn("tests/skill_evals/scholar_grade/live_pilot_v2/outputs", text)
        self.assertIn("tests/skill_evals/scholar_grade/live_pilot_v2/manifests", text)
        self.assertIn("tests/skill_evals/scholar_grade/live_pilot_v2/scores", text)
        self.assertIn("tests/skill_evals/scholar_grade/live_pilot_v2/fixture-ids.json", text)

    def test_validation_runner_exposes_additive_live_pilot_v3_scope(self) -> None:
        module = load_module("run_package_checks.py")
        live_pilot_v3_text = "\n".join(" ".join(check) for check in module.checks_for_scope("live-pilot-v3"))

        self.assertIn("tests/skill_evals/scholar_grade/live_pilot_calibration.py", live_pilot_v3_text)
        self.assertIn("tests/skill_evals/scholar_grade/live_pilot_v3/outputs", live_pilot_v3_text)
        self.assertIn("tests/skill_evals/scholar_grade/live_pilot_v3/manifests", live_pilot_v3_text)
        self.assertIn("tests/skill_evals/scholar_grade/live_pilot_v3/scores", live_pilot_v3_text)
        self.assertIn("tests/skill_evals/scholar_grade/live_pilot_v3/fixture-ids.json", live_pilot_v3_text)
        self.assertIn("tests/skill_evals/scholar_grade/live_pilot_v3", live_pilot_v3_text)
        self.assertIn("--strict", live_pilot_v3_text)

    def test_validation_runner_exposes_additive_live_pilot_v5_and_v6_scopes(self) -> None:
        module = load_module("run_package_checks.py")

        for scope, live_root in [
            ("live-pilot-v5", "live_pilot_v5"),
            ("live-pilot-v6", "live_pilot_v6"),
        ]:
            with self.subTest(scope=scope):
                live_pilot_text = "\n".join(" ".join(check) for check in module.checks_for_scope(scope))

                self.assertIn("tests/skill_evals/scholar_grade/live_pilot_calibration.py", live_pilot_text)
                self.assertIn(f"tests/skill_evals/scholar_grade/{live_root}/outputs", live_pilot_text)
                self.assertIn(f"tests/skill_evals/scholar_grade/{live_root}/manifests", live_pilot_text)
                self.assertIn(f"tests/skill_evals/scholar_grade/{live_root}/scores", live_pilot_text)
                self.assertIn(f"tests/skill_evals/scholar_grade/{live_root}/fixture-ids.json", live_pilot_text)
                self.assertIn(f"tests/skill_evals/scholar_grade/{live_root}", live_pilot_text)
                self.assertIn("--strict", live_pilot_text)

    def test_validation_runner_exposes_scholar_grade_mutation_scope(self) -> None:
        module = load_module("run_package_checks.py")
        mutation_check_text = "\n".join(" ".join(check) for check in module.checks_for_scope("scholar-mutation"))

        self.assertIn("tests/skill_evals/scholar_grade/mutation_tests/run_mutation_tests.py", mutation_check_text)
        self.assertIn("--quiet", mutation_check_text)

    def test_validation_runner_exposes_real_goldset_scope(self) -> None:
        module = load_module("run_package_checks.py")
        real_goldset_check_text = "\n".join(" ".join(check) for check in module.checks_for_scope("real-goldsets"))
        full_check_text = "\n".join(" ".join(check) for check in module.checks_for_scope("full"))

        self.assertIn("tests/skill_evals/scholar_grade/real_goldsets/validate_goldsets.py", real_goldset_check_text)
        self.assertIn("tests/skill_evals/scholar_grade/real_goldsets/live_test_goldsets.py", real_goldset_check_text)
        self.assertIn("tests/skill_evals/scholar_grade/real_goldsets/live_test_goldsets.py", full_check_text)
        self.assertIn("--quiet", real_goldset_check_text)

    def test_full_validation_runner_checks_live_pilot_calibration_report(self) -> None:
        text = (SCRIPTS_DIR / "run_package_checks.py").read_text(encoding="utf-8")

        self.assertIn("tests/skill_evals/scholar_grade/live_pilot_calibration.py", text)
        self.assertIn("--quiet", text)

    def test_full_validation_runner_enforces_completed_live_pilot_v3_without_enforcing_stale_v2(self) -> None:
        module = load_module("run_package_checks.py")
        full_checks = module.checks_for_scope("full")
        full_check_text = "\n".join(" ".join(check) for check in full_checks)
        v3_checks = [
            " ".join(check)
            for check in full_checks
            if "tests/skill_evals/scholar_grade/live_pilot_v3" in " ".join(check)
        ]

        self.assertIn("tests/skill_evals/scholar_grade/live_pilot_v3/fixture-ids.json", full_check_text)
        self.assertIn("tests/skill_evals/scholar_grade/live_pilot_v3", full_check_text)
        self.assertNotIn("tests/skill_evals/scholar_grade/live_pilot_v2/fixture-ids.json", full_check_text)
        self.assertEqual(len(v3_checks), 1)
        self.assertIn("--strict", v3_checks[0])

    def test_live_pilot_plan_matches_validation_runner_fixture_ids(self) -> None:
        plan_path = ROOT / "tests" / "skill_evals" / "scholar_grade" / "live_pilot" / "fixture-ids.json"
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        text = (SCRIPTS_DIR / "run_package_checks.py").read_text(encoding="utf-8")

        self.assertEqual(plan["schema_version"], "scholar-grade-live-pilot-v1")
        self.assertEqual(plan["artifact_root"], "tests/skill_evals/scholar_grade/live_pilot")
        for fixture_id in plan["fixture_ids"]:
            self.assertIn(f'"{fixture_id}"', text)

    def test_live_pilot_v2_plan_matches_validation_runner_fixture_ids(self) -> None:
        plan_path = ROOT / "tests" / "skill_evals" / "scholar_grade" / "live_pilot_v2" / "fixture-ids.json"
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        text = (SCRIPTS_DIR / "run_package_checks.py").read_text(encoding="utf-8")

        self.assertEqual(plan["schema_version"], "scholar-grade-live-pilot-v1")
        self.assertEqual(plan["artifact_root"], "tests/skill_evals/scholar_grade/live_pilot_v2")
        for fixture_id in plan["fixture_ids"]:
            self.assertIn(f'"{fixture_id}"', text)

    def test_live_pilot_v3_plan_matches_validation_runner_fixture_ids(self) -> None:
        plan_path = ROOT / "tests" / "skill_evals" / "scholar_grade" / "live_pilot_v3" / "fixture-ids.json"
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        text = (SCRIPTS_DIR / "run_package_checks.py").read_text(encoding="utf-8")

        self.assertEqual(plan["schema_version"], "scholar-grade-live-pilot-v1")
        self.assertEqual(plan["artifact_root"], "tests/skill_evals/scholar_grade/live_pilot_v3")
        for fixture_id in plan["fixture_ids"]:
            self.assertIn(f'"{fixture_id}"', text)

    def test_live_pilot_v5_and_v6_plans_match_validation_runner_fixture_ids(self) -> None:
        module = load_module("run_package_checks.py")

        for scope, live_root in [
            ("live-pilot-v5", "live_pilot_v5"),
            ("live-pilot-v6", "live_pilot_v6"),
        ]:
            with self.subTest(scope=scope):
                plan_path = ROOT / "tests" / "skill_evals" / "scholar_grade" / live_root / "fixture-ids.json"
                plan = json.loads(plan_path.read_text(encoding="utf-8"))
                live_pilot_text = "\n".join(" ".join(check) for check in module.checks_for_scope(scope))

                self.assertEqual(plan["schema_version"], "scholar-grade-live-pilot-v1")
                for fixture_id in plan["fixture_ids"]:
                    self.assertIn(fixture_id, live_pilot_text)

    def test_readme_describes_skill_evaluation_strategy(self) -> None:
        text = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("## Skill testing", text)
        self.assertIn("tests/skill_evals", text)
        self.assertIn("scholar-grade", text)

    def test_installer_uses_shared_validation_runner(self) -> None:
        text = (SCRIPTS_DIR / "install_codex_plugin.py").read_text(encoding="utf-8")
        self.assertIn("run_package_checks.py", text)
        self.assertIn("--scope", text)
        self.assertIn("install", text)

    def test_validation_workflow_runs_validate_script(self) -> None:
        workflow_path = ROOT / ".github" / "workflows" / "validate.yml"

        self.assertTrue(workflow_path.exists())
        text = workflow_path.read_text(encoding="utf-8")
        self.assertIn("pull_request:", text)
        self.assertIn("push:", text)
        self.assertIn("python-version: '3.10'", text)
        self.assertIn("bash validate.sh", text)

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
            "check_workflow_passport_fixtures.py": [
                "Validate multi-skill workflow process-passport preservation fixtures.",
                "--fixtures",
            ],
            "check_workflow_traceability.py": [
                "Validate deterministic workflow traceability artifacts with content hashes.",
                "--trace",
            ],
            "summarize_research_behavior_evals.py": [
                "Summarize local research behavior fixture coverage, outputs, and traces.",
                "--outputs-dir",
                "--traces-dir",
            ],
            "research_behavior_eval_harness.py": [
                "Build a deterministic research behavior evaluation harness report.",
                "--fixtures",
                "--format",
                "--quiet",
            ],
            "check_citation_metadata.py": [
                "Check local citation metadata exports without private text.",
                "--input",
                "--lookup-provider",
                "--allow-network",
                "--lookup-timeout",
            ],
            "check_source_candidates.py": [
                "Check local source candidate exports",
                "duplicate clusters",
                "--input",
                "--quiet",
            ],
            "check_figure_table_provenance.py": [
                "Check local figure/table provenance records without verifying data truth.",
                "--input",
                "--quiet",
            ],
            "package_plugin.py": [
                "Package this plugin directory as a zip.",
                "--out",
            ],
            "install_codex_plugin.py": [
                "Install Research Book Skills Plugin locally.",
                "--source-path",
                "--dry-run",
            ],
            "run_package_checks.py": [
                "Run package validation checks.",
                "--scope",
                "--root",
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

    def test_validator_shared_reference_checker_reports_missing_and_escaped_paths(self) -> None:
        validator = load_module("validate_plugin.py")
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory).resolve()
            source_path = root / "README.md"
            source_path.write_text("Sample", encoding="utf-8")

            errors = validator.broken_references_from_values(
                root,
                source_path,
                "README.md",
                ["docs/missing.md", "../outside.md"],
            )

            self.assertEqual(
                errors,
                [
                    "README.md: broken local reference: docs/missing.md",
                    "README.md: local reference escapes plugin root: ../outside.md",
                ],
            )

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
            self.assertIn("policy.allowed_external_payloads", result.stdout)
            self.assertIn("policy.lookup_consent_required", result.stdout)
            self.assertIn("policy.private_payloads_external", result.stdout)
            self.assertIn("policy.artifact_sensitivity", result.stdout)

    def test_validator_rejects_wrong_skill_specific_lookup_policy(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_minimal_plugin(root)
            policy_lines = load_module("plugin_utils.py").agent_policy_yaml_lines("citation-integrity-auditor")
            (root / "skills" / "sample-skill" / "agents" / "openai.yaml").write_text(
                "\n".join(
                    [
                        "interface:",
                        '  display_name: "Sample Skill"',
                        (
                            '  short_description: "Sample skill validates metadata display routing '
                            'coverage evidence workflow planning audit chapter argument continuity."'
                        ),
                        '  default_prompt: "Use sample-skill."',
                        *policy_lines,
                        "",
                    ]
                ),
                encoding="utf-8",
            )

            result = run_script("validate_plugin.py", str(root))

            self.assertEqual(result.returncode, 1)
            self.assertIn("policy.external_lookup_allowed must be 'none'", result.stdout)
            self.assertIn("policy.allowed_external_payloads", result.stdout)

    def test_validator_rejects_skill_metadata_version_drift(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "plugin"
            write_minimal_plugin(
                root,
                skill_body="\n".join(
                    [
                        "---",
                        "name: sample-skill",
                        (
                            "description: Sample skill validates metadata display routing "
                            "coverage evidence workflow planning audit chapter argument continuity."
                        ),
                        "metadata:",
                        '  version: "0.9.0"',
                        "---",
                        "# Sample Skill",
                        "",
                    ]
                ),
            )

            result = run_script("validate_plugin.py", str(root))

            self.assertEqual(result.returncode, 1)
            self.assertIn("metadata.version", result.stdout)

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
