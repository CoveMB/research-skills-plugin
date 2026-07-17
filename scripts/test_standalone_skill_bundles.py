"""Tests for portable standalone skill bundles."""
from __future__ import annotations

import importlib.util
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
LIBRARY_PATH = ROOT / "scripts" / "standalone_skill_bundles.py"
REGISTRY_PATH = ROOT / "shared" / "standalone-skill-registry.json"
BUILD_SCRIPT = ROOT / "scripts" / "build_standalone_skill.py"
VALIDATE_SCRIPT = ROOT / "scripts" / "validate_standalone_skill.py"


def load_script_module(
    test_case: unittest.TestCase,
    relative_path: str,
    module_name: str,
):
    path = ROOT / relative_path
    test_case.assertTrue(path.is_file(), f"required package script is missing: {relative_path}")
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_library(test_case: unittest.TestCase):
    return load_script_module(
        test_case,
        "scripts/standalone_skill_bundles.py",
        "standalone_skill_bundles",
    )


def copy_packaged_plugin(test_case: unittest.TestCase, destination: Path) -> None:
    plugin_utils = load_script_module(
        test_case,
        "scripts/plugin_utils.py",
        f"portable_plugin_utils_{id(destination)}",
    )
    plugin_utils.copy_package_tree(ROOT, destination)


class RegistryTests(unittest.TestCase):
    def load_registry_payload(self) -> dict:
        self.assertTrue(REGISTRY_PATH.is_file(), "standalone skill registry is missing")
        payload = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        self.assertIsInstance(payload, dict)
        return payload

    def test_registry_covers_all_source_skills_with_approved_classifications(self) -> None:
        payload = self.load_registry_payload()
        self.assertEqual(payload.get("schema_version"), "standalone-skill-registry-v1")
        entries = payload.get("skills")
        self.assertIsInstance(entries, list)
        names = [entry["name"] for entry in entries]
        source_names = sorted(
            path.name for path in (ROOT / "skills").iterdir() if (path / "SKILL.md").is_file()
        )
        self.assertEqual(names, source_names)
        self.assertEqual(len(names), len(set(names)))

        classifications = {entry["name"]: entry["classification"] for entry in entries}
        self.assertEqual(classifications["research-intent-router"], "route-only")
        self.assertEqual(classifications["research-book-orchestrator"], "full-plugin-only")
        self.assertEqual(
            sum(value == "self-sufficient" for value in classifications.values()),
            27,
        )

    def test_registry_entries_are_complete_sorted_and_match_discovered_direct_dependencies(self) -> None:
        module = load_library(self)
        self.assertEqual(module.registry_errors(ROOT), [])

        entries = module.load_registry(ROOT)
        for entry in entries:
            self.assertTrue(entry.rationale.strip())
            self.assertEqual(list(entry.resources), sorted(set(entry.resources)))
            self.assertEqual(list(entry.runtime_helpers), sorted(set(entry.runtime_helpers)))
            discovered_resources, discovered_helpers = module.discover_direct_dependencies(
                ROOT,
                entry.name,
            )
            self.assertEqual(tuple(discovered_resources), entry.resources)
            self.assertEqual(tuple(discovered_helpers), entry.runtime_helpers)

    def test_registry_validation_rejects_duplicate_missing_and_unsupported_entries(self) -> None:
        module = load_library(self)
        payload = self.load_registry_payload()
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "shared").mkdir()
            (root / "skills").mkdir()
            for skill_name in ("alpha-skill", "beta-skill"):
                skill_root = root / "skills" / skill_name
                skill_root.mkdir()
                (skill_root / "SKILL.md").write_text(
                    f"---\nname: {skill_name}\ndescription: Test skill.\n---\n",
                    encoding="utf-8",
                )
            payload["skills"] = [
                {
                    "name": "alpha-skill",
                    "classification": "unknown",
                    "rationale": "",
                    "resources": [],
                    "runtime_helpers": [],
                },
                {
                    "name": "alpha-skill",
                    "classification": "self-sufficient",
                    "rationale": "Duplicate.",
                    "resources": [],
                    "runtime_helpers": [],
                },
            ]
            registry_path = root / "shared" / "standalone-skill-registry.json"
            registry_path.write_text(json.dumps(payload), encoding="utf-8")

            errors = module.registry_errors(root)

            self.assertTrue(any("duplicate" in error for error in errors))
            self.assertTrue(any("missing" in error and "beta-skill" in error for error in errors))
            self.assertTrue(any("unsupported classification" in error for error in errors))
            self.assertTrue(any("rationale" in error for error in errors))


class DependencyClosureTests(unittest.TestCase):
    def test_all_eligible_skills_have_safe_complete_plans_without_source_readmes(self) -> None:
        module = load_library(self)
        for entry in module.load_registry(ROOT):
            if entry.classification == "full-plugin-only":
                continue
            plan = module.create_bundle_plan(ROOT, entry.name)
            sources = set(plan.source_to_bundle)
            self.assertIn(f"skills/{entry.name}/SKILL.md", sources)
            self.assertIn(f"skills/{entry.name}/agents/openai.yaml", sources)
            self.assertIn("LICENSE", sources)
            self.assertNotIn(f"skills/{entry.name}/README.md", sources)
            destinations = list(plan.source_to_bundle.values())
            self.assertEqual(len(destinations), len(set(destinations)))
            self.assertEqual(len(destinations), len({value.casefold() for value in destinations}))

    def test_dependency_plan_includes_assets_policy_closure_and_python_imports(self) -> None:
        module = load_library(self)

        method_plan = module.create_bundle_plan(ROOT, "methodology-source-auditor")
        self.assertIn(
            "skills/methodology-source-auditor/references/qualitative.md",
            method_plan.source_to_bundle,
        )
        self.assertIn(
            "skills/methodology-source-auditor/assets/source-audit-rubric.md",
            method_plan.source_to_bundle,
        )
        self.assertIn("docs/policy/PROCESS_PASSPORT.md", method_plan.source_to_bundle)

        helper_plan = module.create_bundle_plan(ROOT, "discovery-runner-deduper")
        self.assertIn("scripts/check_source_candidates.py", helper_plan.source_to_bundle)
        self.assertIn("scripts/check_citation_metadata.py", helper_plan.source_to_bundle)
        self.assertIn("scripts/plugin_utils.py", helper_plan.source_to_bundle)
        self.assertEqual(
            helper_plan.source_to_bundle["scripts/plugin_utils.py"],
            "scripts/plugin_utils.py",
        )

        trace_plan = module.create_bundle_plan(ROOT, "claim-evidence-ledger")
        self.assertIn("scripts/check_workflow_traceability.py", trace_plan.source_to_bundle)
        self.assertIn("scripts/check_workflow_passport_fixtures.py", trace_plan.source_to_bundle)

    def test_reference_extraction_ignores_urls_placeholders_directories_and_skill_names(self) -> None:
        module = load_library(self)
        text = """
Use https://example.org/source and `research-intent-router`.
Choose `skills/<skill-name>/` or `assets/` only as labels.
Load `docs/policy/SOURCE_LIMITS.md` and [the schema](shared/contracts/book/book_artifact.schema.json).
"""
        self.assertEqual(
            module.extract_local_references(text),
            (
                "docs/policy/SOURCE_LIMITS.md",
                "shared/contracts/book/book_artifact.schema.json",
            ),
        )

    def test_safe_source_path_rejects_absolute_parent_symlink_and_missing_paths(self) -> None:
        module = load_library(self)
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "safe.txt").write_text("safe", encoding="utf-8")
            outside = root.parent / f"{root.name}-outside.txt"
            outside.write_text("outside", encoding="utf-8")
            self.addCleanup(outside.unlink)
            link = root / "linked.txt"
            try:
                link.symlink_to(outside)
            except (NotImplementedError, OSError) as error:
                self.skipTest(f"symlink creation unavailable: {error}")

            self.assertEqual(module.safe_source_path(root, "safe.txt"), root / "safe.txt")
            for unsafe in (str(outside.resolve()), "../outside.txt", "linked.txt", "missing.txt"):
                with self.subTest(path=unsafe), self.assertRaises(ValueError):
                    module.safe_source_path(root, unsafe)

    def test_python_closure_resolves_from_dot_imports(self) -> None:
        module = load_library(self)
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            scripts = root / "scripts"
            scripts.mkdir()
            (scripts / "main.py").write_text("from . import helper\n", encoding="utf-8")
            (scripts / "helper.py").write_text("VALUE = 1\n", encoding="utf-8")
            self.assertEqual(
                module._local_python_imports(root, "scripts/main.py"),
                ("scripts/helper.py",),
            )

    def test_python_closure_and_validation_preserve_dotted_package_imports(self) -> None:
        module = load_library(self)
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            scripts = root / "scripts"
            package = scripts / "localpkg"
            package.mkdir(parents=True)
            (scripts / "main.py").write_text(
                "import localpkg.submodule\nfrom localpkg import sibling\n",
                encoding="utf-8",
            )
            (package / "__init__.py").write_text("", encoding="utf-8")
            (package / "submodule.py").write_text("VALUE = 1\n", encoding="utf-8")
            (package / "sibling.py").write_text("VALUE = 2\n", encoding="utf-8")

            self.assertEqual(
                module._local_python_imports(root, "scripts/main.py"),
                (
                    "scripts/localpkg/__init__.py",
                    "scripts/localpkg/sibling.py",
                    "scripts/localpkg/submodule.py",
                ),
            )
            mapping = module._destination_mapping(
                "sample-skill",
                {
                    "skills/sample-skill/SKILL.md",
                    "scripts/main.py",
                    "scripts/localpkg/__init__.py",
                    "scripts/localpkg/sibling.py",
                    "scripts/localpkg/submodule.py",
                },
            )
            self.assertEqual(
                mapping["scripts/localpkg/submodule.py"],
                "scripts/localpkg/submodule.py",
            )
            with self.assertRaisesRegex(ValueError, "localpkg.submodule"):
                module._bundle_python_dependencies(
                    "scripts/main.py",
                    b"import localpkg.submodule\n",
                    {"scripts/main.py", "scripts/localpkg/__init__.py"},
                )


def file_bytes(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


class BuilderTests(unittest.TestCase):
    def test_source_commit_requires_a_clean_tracked_plugin_root(self) -> None:
        module = load_library(self)
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository_root = Path(temporary_directory) / "outer-repository"
            tracked_plugin = repository_root / "packages" / "tracked-plugin"
            copy_packaged_plugin(self, tracked_plugin)
            subprocess.run(
                ["git", "init", "--quiet", str(repository_root)],
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                ["git", "-C", str(repository_root), "add", "."],
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(repository_root),
                    "-c",
                    "user.name=Standalone Bundle Tests",
                    "-c",
                    "user.email=standalone-bundle-tests@example.invalid",
                    "commit",
                    "--quiet",
                    "-m",
                    "Add tracked plugin fixture",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            expected_commit = subprocess.run(
                ["git", "-C", str(repository_root), "rev-parse", "HEAD"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()

            self.assertEqual(module.source_commit(tracked_plugin), expected_commit)

            manifest_path = tracked_plugin / ".codex-plugin" / "plugin.json"
            original_manifest = manifest_path.read_bytes()
            manifest_path.write_bytes(original_manifest + b"\n")
            self.assertEqual(module.source_commit(tracked_plugin), "unavailable")
            manifest_path.write_bytes(original_manifest)

            untracked_plugin = repository_root / "packages" / "untracked-plugin"
            copy_packaged_plugin(self, untracked_plugin)
            self.assertEqual(module.source_commit(untracked_plugin), "unavailable")
            self.assertEqual(module.source_commit(tracked_plugin), expected_commit)

    def test_build_emits_standard_rewritten_layout_manifest_and_zip(self) -> None:
        module = load_library(self)
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_root = Path(temporary_directory) / "standalone-skills"
            bundle_directory, bundle_zip = module.build_standalone_skill(
                ROOT,
                "annotation-to-source-note",
                output_root,
            )

            self.assertEqual(
                bundle_directory,
                output_root.resolve() / "annotation-to-source-note",
            )
            self.assertEqual(
                bundle_zip,
                output_root.resolve() / "annotation-to-source-note.zip",
            )
            self.assertTrue((bundle_directory / "SKILL.md").is_file())
            self.assertTrue((bundle_directory / "agents" / "openai.yaml").is_file())
            self.assertTrue((bundle_directory / "LICENSE").is_file())
            self.assertFalse((bundle_directory / "README.md").exists())
            skill_text = (bundle_directory / "SKILL.md").read_text(encoding="utf-8")
            self.assertNotIn("docs/policy/PROCESS_PASSPORT.md", skill_text)
            self.assertIn("references/PROCESS_PASSPORT.md", skill_text)

            manifest_path = bundle_directory / "standalone-bundle.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(manifest["schema_version"], "standalone-skill-bundle-v1")
            self.assertEqual(manifest["skill_name"], "annotation-to-source-note")
            self.assertEqual(manifest["classification"], "self-sufficient")
            self.assertEqual(manifest["plugin_version"], "1.1.0")
            self.assertTrue(manifest["rationale"])
            self.assertIn(manifest["source_commit"], {"unavailable", module.source_commit(ROOT)})
            self.assertEqual(
                set(manifest["sha256"]),
                set(file_bytes(bundle_directory)) - {"standalone-bundle.json"},
            )
            for relative_path, expected_hash in manifest["sha256"].items():
                self.assertEqual(
                    hashlib.sha256((bundle_directory / relative_path).read_bytes()).hexdigest(),
                    expected_hash,
                )
            with zipfile.ZipFile(bundle_zip) as archive:
                members = sorted(name for name in archive.namelist() if not name.endswith("/"))
            self.assertEqual(
                members,
                [
                    f"annotation-to-source-note/{relative_path}"
                    for relative_path in sorted(file_bytes(bundle_directory))
                ],
            )

    def test_repeated_builds_are_byte_identical_and_leave_sources_unchanged(self) -> None:
        module = load_library(self)
        source_paths = [
            ROOT / "skills" / "methodology-source-auditor" / "SKILL.md",
            ROOT / "docs" / "policy" / "PROCESS_PASSPORT.md",
        ]
        source_before = {path: path.read_bytes() for path in source_paths}
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            first_directory, first_zip = module.build_standalone_skill(
                ROOT,
                "methodology-source-auditor",
                temporary_root / "first",
            )
            second_directory, second_zip = module.build_standalone_skill(
                ROOT,
                "methodology-source-auditor",
                temporary_root / "second",
            )
            self.assertEqual(file_bytes(first_directory), file_bytes(second_directory))
            self.assertEqual(first_zip.read_bytes(), second_zip.read_bytes())
        self.assertEqual(source_before, {path: path.read_bytes() for path in source_paths})

    def test_collision_mapping_is_shallow_stable_and_unique(self) -> None:
        module = load_library(self)
        mapping = module._destination_mapping(
            "sample-skill",
            {
                "skills/sample-skill/SKILL.md",
                "docs/one/SAME.md",
                "shared/two/SAME.md",
            },
        )
        external_destinations = {
            mapping["docs/one/SAME.md"],
            mapping["shared/two/SAME.md"],
        }
        self.assertEqual(len(external_destinations), 2)
        self.assertTrue(
            all(destination.startswith("references/SAME-") for destination in external_destinations)
        )
        self.assertTrue(all(destination.endswith(".md") for destination in external_destinations))

    def test_limits_and_full_plugin_refusal_happen_before_publication(self) -> None:
        module = load_library(self)
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            with self.assertRaisesRegex(ValueError, "file count"):
                module.stage_standalone_bundle(
                    ROOT,
                    "annotation-to-source-note",
                    temporary_root / "limited",
                    max_file_count=1,
                )
            output_root = temporary_root / "orchestrator-output"
            with self.assertRaisesRegex(ValueError, "full-plugin-only"):
                module.build_standalone_skill(
                    ROOT,
                    "research-book-orchestrator",
                    output_root,
                )
            self.assertFalse(output_root.exists())

    def test_build_cli_supports_one_skill_and_rejects_conflicting_selection(self) -> None:
        self.assertTrue(BUILD_SCRIPT.is_file(), "standalone build CLI is missing")
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_root = Path(temporary_directory) / "out"
            result = subprocess.run(
                [
                    sys.executable,
                    str(BUILD_SCRIPT),
                    "--root",
                    str(ROOT),
                    "--out",
                    str(output_root),
                    "--skill",
                    "ai-human-workflow-log",
                ],
                check=False,
                capture_output=True,
                text=True,
                env={**dict(__import__("os").environ), "PYTHONDONTWRITEBYTECODE": "1"},
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((output_root / "ai-human-workflow-log" / "SKILL.md").is_file())
            conflict = subprocess.run(
                [
                    sys.executable,
                    str(BUILD_SCRIPT),
                    "--root",
                    str(ROOT),
                    "--out",
                    str(output_root),
                    "--skill",
                    "ai-human-workflow-log",
                    "--all",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(conflict.returncode, 0)

    def test_build_cli_rejects_symlink_output_root(self) -> None:
        self.assertTrue(BUILD_SCRIPT.is_file(), "standalone build CLI is missing")
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            real_output = temporary_root / "real-output"
            real_output.mkdir()
            linked_output = temporary_root / "linked-output"
            try:
                linked_output.symlink_to(real_output, target_is_directory=True)
            except (NotImplementedError, OSError) as error:
                self.skipTest(f"symlink creation unavailable: {error}")

            result = subprocess.run(
                [
                    sys.executable,
                    str(BUILD_SCRIPT),
                    "--root",
                    str(ROOT),
                    "--out",
                    str(linked_output),
                    "--skill",
                    "ai-human-workflow-log",
                ],
                check=False,
                capture_output=True,
                text=True,
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            )

            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn("symlink", result.stderr)
            self.assertEqual(list(real_output.iterdir()), [])

    def test_single_build_rejects_canonical_and_unowned_existing_targets(self) -> None:
        module = load_library(self)
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            packaged_root = temporary_root / "packaged-plugin"
            copy_packaged_plugin(self, packaged_root)
            canonical_skill = packaged_root / "skills" / "ai-human-workflow-log"
            self.assertTrue((canonical_skill / "README.md").is_file())

            with self.assertRaisesRegex(ValueError, "canonical|source|generated output"):
                module.build_standalone_skill(
                    packaged_root,
                    "ai-human-workflow-log",
                    packaged_root / "skills",
                )

            self.assertTrue((canonical_skill / "README.md").is_file())
            self.assertFalse((canonical_skill / "standalone-bundle.json").exists())

            external_output = temporary_root / "external-output"
            raw_target = external_output / "ai-human-workflow-log"
            raw_target.mkdir(parents=True)
            marker = raw_target / "README.md"
            marker.write_text("raw source marker", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "generated bundle|replace"):
                module.build_standalone_skill(
                    packaged_root,
                    "ai-human-workflow-log",
                    external_output,
                )

            self.assertEqual(marker.read_text(encoding="utf-8"), "raw source marker")

    def test_single_build_rejects_symlink_output_root(self) -> None:
        module = load_library(self)
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            real_output = temporary_root / "real-output"
            real_output.mkdir()
            linked_output = temporary_root / "linked-output"
            try:
                linked_output.symlink_to(real_output, target_is_directory=True)
            except (NotImplementedError, OSError) as error:
                self.skipTest(f"symlink creation unavailable: {error}")

            with self.assertRaisesRegex(ValueError, "symlink"):
                module.build_standalone_skill(
                    ROOT,
                    "ai-human-workflow-log",
                    linked_output,
                )

            self.assertEqual(list(real_output.iterdir()), [])

    def test_single_build_reuses_owned_output_without_touching_unrelated_entries(self) -> None:
        module = load_library(self)
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_root = Path(temporary_directory) / "shared-output"
            output_root.mkdir()
            unrelated = output_root / "unrelated.txt"
            unrelated.write_text("keep", encoding="utf-8")

            first_directory, first_zip = module.build_standalone_skill(
                ROOT,
                "ai-human-workflow-log",
                output_root,
            )
            first_manifest = (first_directory / "standalone-bundle.json").read_bytes()
            second_directory, second_zip = module.build_standalone_skill(
                ROOT,
                "ai-human-workflow-log",
                output_root,
            )

            self.assertEqual(second_directory, first_directory)
            self.assertEqual(second_zip, first_zip)
            self.assertEqual(
                (second_directory / "standalone-bundle.json").read_bytes(),
                first_manifest,
            )
            self.assertEqual(unrelated.read_text(encoding="utf-8"), "keep")


class PublicationTests(unittest.TestCase):
    def test_pair_publication_restores_both_previous_targets_on_second_replace_failure(self) -> None:
        module = load_library(self)
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            output_root = temporary_root / "output"
            output_root.mkdir()
            old_directory = output_root / "sample-skill"
            old_directory.mkdir()
            (old_directory / "old.txt").write_text("old directory", encoding="utf-8")
            old_zip = output_root / "sample-skill.zip"
            old_zip.write_bytes(b"old zip")
            staged_directory = temporary_root / "staged" / "sample-skill"
            staged_directory.mkdir(parents=True)
            (staged_directory / "new.txt").write_text("new directory", encoding="utf-8")
            staged_zip = temporary_root / "staged" / "sample-skill.zip"
            staged_zip.write_bytes(b"new zip")

            real_replace = module._replace_path

            def fail_second_publication(source: Path, target: Path) -> None:
                if source == staged_zip and target == old_zip:
                    raise OSError("forced second-target failure")
                real_replace(source, target)

            with self.assertRaisesRegex(OSError, "forced second-target failure"):
                module.publish_bundle_pair(
                    staged_directory,
                    staged_zip,
                    output_root,
                    "sample-skill",
                    replace_function=fail_second_publication,
                )

            self.assertEqual((old_directory / "old.txt").read_text(encoding="utf-8"), "old directory")
            self.assertEqual(old_zip.read_bytes(), b"old zip")

    def test_all_build_stages_complete_catalog_before_replacing_existing_output(self) -> None:
        module = load_library(self)
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_root = Path(temporary_directory) / "catalog"
            existing_directory, existing_archive = module.build_standalone_skill(
                ROOT,
                "ai-human-workflow-log",
                output_root,
            )
            existing_files = file_bytes(existing_directory)
            existing_archive_bytes = existing_archive.read_bytes()
            calls = 0

            def fail_during_staging(root: Path, skill_name: str, catalog_root: Path):
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise OSError("forced catalog staging failure")
                directory = catalog_root / skill_name
                directory.mkdir(parents=True)
                archive = catalog_root / f"{skill_name}.zip"
                archive.write_bytes(b"staged")
                return directory, archive

            with mock.patch.object(module, "stage_bundle_pair", side_effect=fail_during_staging):
                with self.assertRaisesRegex(OSError, "forced catalog staging failure"):
                    module.build_all_standalone_skills(ROOT, output_root)

            self.assertEqual(file_bytes(existing_directory), existing_files)
            self.assertEqual(existing_archive.read_bytes(), existing_archive_bytes)
            self.assertEqual(
                sorted(path.name for path in output_root.iterdir()),
                ["ai-human-workflow-log", "ai-human-workflow-log.zip"],
            )

    def test_all_build_rejects_unowned_nonempty_catalog_without_replacing_it(self) -> None:
        module = load_library(self)
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_root = Path(temporary_directory) / "catalog"
            output_root.mkdir()
            marker = output_root / "unrelated.txt"
            marker.write_text("keep", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "generated catalog|replace"):
                module.build_all_standalone_skills(ROOT, output_root)

            self.assertEqual(marker.read_text(encoding="utf-8"), "keep")
            self.assertEqual(list(output_root.iterdir()), [marker])

    def test_incomplete_pair_rollback_retains_backups_for_manual_recovery(self) -> None:
        module = load_library(self)
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            output_root = temporary_root / "output"
            output_root.mkdir()
            old_directory = output_root / "sample-skill"
            old_directory.mkdir()
            (old_directory / "old.txt").write_text("old directory", encoding="utf-8")
            old_zip = output_root / "sample-skill.zip"
            old_zip.write_bytes(b"old zip")
            staged_directory = temporary_root / "staged" / "sample-skill"
            staged_directory.mkdir(parents=True)
            (staged_directory / "new.txt").write_text("new directory", encoding="utf-8")
            staged_zip = temporary_root / "staged" / "sample-skill.zip"
            staged_zip.write_bytes(b"new zip")
            real_replace = module._replace_path

            def fail_publication_and_recovery(source: Path, target: Path) -> None:
                if source == staged_zip:
                    raise OSError("forced publication failure")
                if ".sample-skill.backup-" in source.parent.name:
                    raise OSError("forced recovery failure")
                real_replace(source, target)

            with self.assertRaisesRegex(RuntimeError, "backups retained"):
                module.publish_bundle_pair(
                    staged_directory,
                    staged_zip,
                    output_root,
                    "sample-skill",
                    replace_function=fail_publication_and_recovery,
                )

            backups = list(temporary_root.glob(".sample-skill.backup-*"))
            self.assertEqual(len(backups), 1)
            self.assertEqual((backups[0] / "sample-skill" / "old.txt").read_text(), "old directory")
            self.assertEqual((backups[0] / "sample-skill.zip").read_bytes(), b"old zip")

    def test_incomplete_catalog_rollback_retains_backup_for_manual_recovery(self) -> None:
        module = load_library(self)
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            output_root = temporary_root / "catalog"
            output_root.mkdir()
            (output_root / "old.txt").write_text("old catalog", encoding="utf-8")
            staged_catalog = temporary_root / "staged-catalog"
            staged_catalog.mkdir()
            (staged_catalog / "new.txt").write_text("new catalog", encoding="utf-8")
            real_replace = module._replace_path

            def fail_publication_and_recovery(source: Path, target: Path) -> None:
                if source == staged_catalog:
                    raise OSError("forced catalog publication failure")
                if ".catalog.backup-" in source.parent.name:
                    raise OSError("forced catalog recovery failure")
                real_replace(source, target)

            with self.assertRaisesRegex(RuntimeError, "backups retained"):
                module._publish_catalog(
                    staged_catalog,
                    output_root,
                    replace_function=fail_publication_and_recovery,
                )

            backups = list(temporary_root.glob(".catalog.backup-*"))
            self.assertEqual(len(backups), 1)
            self.assertEqual((backups[0] / "catalog" / "old.txt").read_text(), "old catalog")


def refresh_manifest_hash(bundle_directory: Path, relative_path: str) -> None:
    manifest_path = bundle_directory / "standalone-bundle.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["sha256"][relative_path] = hashlib.sha256(
        (bundle_directory / relative_path).read_bytes()
    ).hexdigest()
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


class ValidatorTests(unittest.TestCase):
    def test_directory_inventory_rejects_limits_before_reading_files(self) -> None:
        module = load_library(self)
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            oversized = temporary_root / "oversized"
            oversized.mkdir()
            (oversized / "SKILL.md").write_bytes(b"oversized")

            over_count = temporary_root / "over-count"
            over_count.mkdir()
            (over_count / "SKILL.md").write_bytes(b"skill")
            (over_count / "LICENSE").write_bytes(b"license")

            with mock.patch.object(
                Path,
                "open",
                side_effect=AssertionError("over-limit inventory must not read files"),
            ):
                with self.assertRaisesRegex(ValueError, "uncompressed size"):
                    module._directory_inventory(
                        oversized,
                        max_file_count=512,
                        max_total_bytes=1,
                    )
                with self.assertRaisesRegex(ValueError, "file count"):
                    module._directory_inventory(
                        over_count,
                        max_file_count=1,
                        max_total_bytes=1024,
                    )

    def test_directory_and_zip_validate_after_move_outside_source_checkout(self) -> None:
        module = load_library(self)
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            output_root = temporary_root / "built"
            directory, archive = module.build_standalone_skill(
                ROOT,
                "dyslexia-friendly-prose-editor",
                output_root,
            )
            moved_root = temporary_root / "unrelated-location"
            moved_root.mkdir()
            moved_directory = moved_root / directory.name
            moved_archive = moved_root / archive.name
            shutil.move(directory, moved_directory)
            shutil.move(archive, moved_archive)

            directory_manifest = module.validate_bundle_directory(moved_directory)
            archive_manifest = module.validate_bundle_zip(moved_archive)
            self.assertEqual(directory_manifest, archive_manifest)
            self.assertEqual(directory_manifest["skill_name"], moved_directory.name)

    def test_directory_validation_rejects_tampering_missing_refs_policy_and_unsafe_files(self) -> None:
        module = load_library(self)
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            source_directory, _ = module.build_standalone_skill(
                ROOT,
                "annotation-to-source-note",
                temporary_root / "source",
            )

            def fixture(name: str) -> Path:
                target = temporary_root / name / "annotation-to-source-note"
                shutil.copytree(source_directory, target)
                return target

            tampered = fixture("tampered")
            (tampered / "SKILL.md").write_text("tampered", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "hash mismatch"):
                module.validate_bundle_directory(tampered)

            missing_reference = fixture("missing-reference")
            skill_path = missing_reference / "SKILL.md"
            skill_path.write_text(
                skill_path.read_text(encoding="utf-8")
                + "\nUse `DOES_NOT_EXIST.md`.\n",
                encoding="utf-8",
            )
            refresh_manifest_hash(missing_reference, "SKILL.md")
            with self.assertRaisesRegex(ValueError, "missing local reference"):
                module.validate_bundle_directory(missing_reference)

            invalid_frontmatter = fixture("invalid-frontmatter")
            frontmatter_path = invalid_frontmatter / "SKILL.md"
            frontmatter_path.write_text(
                frontmatter_path.read_text(encoding="utf-8").replace(
                    "name: annotation-to-source-note",
                    "name: wrong-skill",
                    1,
                ),
                encoding="utf-8",
            )
            refresh_manifest_hash(invalid_frontmatter, "SKILL.md")
            with self.assertRaisesRegex(ValueError, "frontmatter name"):
                module.validate_bundle_directory(invalid_frontmatter)

            invalid_policy = fixture("invalid-policy")
            policy_path = invalid_policy / "agents" / "openai.yaml"
            policy_path.write_text(
                policy_path.read_text(encoding="utf-8").replace(
                    '  confidentiality_gate: "required-before-external-lookup"\n',
                    "",
                ),
                encoding="utf-8",
            )
            refresh_manifest_hash(invalid_policy, "agents/openai.yaml")
            with self.assertRaisesRegex(ValueError, "confidentiality_gate"):
                module.validate_bundle_directory(invalid_policy)

            forbidden = fixture("forbidden")
            (forbidden / ".env").write_text("SECRET=value", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "forbidden"):
                module.validate_bundle_directory(forbidden)

            symlinked = fixture("symlinked")
            try:
                (symlinked / "linked.md").symlink_to(symlinked / "SKILL.md")
            except (NotImplementedError, OSError) as error:
                self.skipTest(f"symlink creation unavailable: {error}")
            with self.assertRaisesRegex(ValueError, "symlink"):
                module.validate_bundle_directory(symlinked)

    def test_directory_validation_rejects_weakened_misnested_or_untyped_agent_policy(self) -> None:
        module = load_library(self)
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            source_directory, _ = module.build_standalone_skill(
                ROOT,
                "research-intent-router",
                temporary_root / "source",
            )
            mutations = {
                "missing-lookup-mode": (
                    '  external_lookup_allowed: "conditional"\n',
                    "",
                ),
                "unsafe-private-payload": (
                    '  allowed_external_payloads: "public-identifiers-search-terms-and-nonsensitive-short-summaries"\n',
                    '  allowed_external_payloads: "unrestricted-private-manuscript"\n',
                ),
                "misnested-lookup-mode": (
                    '  external_lookup_allowed: "conditional"\n',
                    'external_lookup_allowed: "conditional"\n',
                ),
                "string-invocation-flag": (
                    "  allow_implicit_invocation: true\n",
                    '  allow_implicit_invocation: "true"\n',
                ),
            }
            for fixture_name, (original, replacement) in mutations.items():
                with self.subTest(fixture=fixture_name):
                    target = temporary_root / fixture_name / "research-intent-router"
                    shutil.copytree(source_directory, target)
                    policy_path = target / "agents" / "openai.yaml"
                    policy_text = policy_path.read_text(encoding="utf-8")
                    self.assertIn(original, policy_text)
                    policy_path.write_text(
                        policy_text.replace(original, replacement, 1),
                        encoding="utf-8",
                    )
                    refresh_manifest_hash(target, "agents/openai.yaml")

                    with self.assertRaisesRegex(ValueError, "agents/openai.yaml|policy"):
                        module.validate_bundle_directory(target)

    def test_archive_validation_rejects_unsafe_members_before_extraction(self) -> None:
        module = load_library(self)
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            fixtures: list[tuple[str, str]] = []

            traversal = temporary_root / "traversal.zip"
            with zipfile.ZipFile(traversal, "w") as archive:
                archive.writestr("../escape.txt", "escape")
            fixtures.append(("parent traversal", str(traversal)))

            absolute = temporary_root / "absolute.zip"
            with zipfile.ZipFile(absolute, "w") as archive:
                archive.writestr("/absolute.txt", "absolute")
            fixtures.append(("absolute", str(absolute)))

            collision = temporary_root / "collision.zip"
            with zipfile.ZipFile(collision, "w") as archive:
                archive.writestr("collision/SKILL.md", "one")
                archive.writestr("collision/skill.md", "two")
            fixtures.append(("case-colliding", str(collision)))

            symlink_archive = temporary_root / "symlink.zip"
            with zipfile.ZipFile(symlink_archive, "w") as archive:
                info = zipfile.ZipInfo("symlink/link")
                info.create_system = 3
                info.external_attr = (0o120777 << 16)
                archive.writestr(info, "target")
            fixtures.append(("symlink", str(symlink_archive)))

            noncanonical = temporary_root / "noncanonical.zip"
            with zipfile.ZipFile(noncanonical, "w") as archive:
                archive.writestr("noncanonical/references//SOURCE_LIMITS.md", "one")
                archive.writestr("noncanonical/references/SOURCE_LIMITS.md", "two")
            fixtures.append(("non-canonical", str(noncanonical)))

            for expected_error, archive_path in fixtures:
                with self.subTest(expected_error=expected_error), self.assertRaisesRegex(
                    ValueError,
                    expected_error,
                ):
                    module.validate_bundle_zip(Path(archive_path))

            self.assertFalse((temporary_root / "escape.txt").exists())

    def test_zip_directory_equivalence_and_catalog_completeness_are_enforced(self) -> None:
        module = load_library(self)
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            output_root = temporary_root / "catalog"
            directory, archive = module.build_standalone_skill(
                ROOT,
                "ai-human-workflow-log",
                output_root,
            )
            module.validate_bundle_pair(directory, archive)

            rewritten_archive = temporary_root / "different.zip"
            with zipfile.ZipFile(archive) as source, zipfile.ZipFile(rewritten_archive, "w") as target:
                for info in source.infolist():
                    content = source.read(info.filename)
                    if info.filename.endswith("SKILL.md"):
                        content += b"\nchanged\n"
                    target.writestr(info, content)
            with self.assertRaisesRegex(ValueError, "equivalence|hash mismatch"):
                module.validate_bundle_pair(directory, rewritten_archive)

            with self.assertRaisesRegex(ValueError, "missing catalog bundle"):
                module.validate_catalog(output_root, REGISTRY_PATH)

    def test_validation_cli_accepts_directory_and_zip(self) -> None:
        self.assertTrue(VALIDATE_SCRIPT.is_file(), "standalone validation CLI is missing")
        module = load_library(self)
        with tempfile.TemporaryDirectory() as temporary_directory:
            directory, archive = module.build_standalone_skill(
                ROOT,
                "ai-human-workflow-log",
                Path(temporary_directory) / "output",
            )
            for path in (directory, archive):
                result = subprocess.run(
                    [sys.executable, str(VALIDATE_SCRIPT), str(path)],
                    check=False,
                    capture_output=True,
                    text=True,
                    env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                )
                self.assertEqual(result.returncode, 0, result.stderr)


class ParityTests(unittest.TestCase):
    def test_representative_skill_text_preserves_content_except_rewrites_and_route_boundary(self) -> None:
        module = load_library(self)
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_root = Path(temporary_directory) / "output"
            method_directory, _ = module.build_standalone_skill(
                ROOT,
                "methodology-source-auditor",
                output_root,
            )
            method_plan = module.create_bundle_plan(ROOT, "methodology-source-auditor")
            canonical_method = (
                ROOT / "skills" / "methodology-source-auditor" / "SKILL.md"
            ).read_text(encoding="utf-8")
            expected_method = module._rewrite_text_source(
                canonical_method,
                "skills/methodology-source-auditor/SKILL.md",
                method_plan,
            )
            self.assertEqual(
                (method_directory / "SKILL.md").read_text(encoding="utf-8"),
                expected_method,
            )
            self.assertTrue((method_directory / "assets" / "source-audit-rubric.md").is_file())
            self.assertEqual(
                len(list((method_directory / "references").glob("*.md"))) >= 8,
                True,
            )

            router_directory, _ = module.build_standalone_skill(
                ROOT,
                "research-intent-router",
                output_root,
            )
            router_text = (router_directory / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("This generated bundle is route-only", router_text)
            self.assertIn("must not claim that an absent specialist skill was run", router_text)
            self.assertIn("Do not invent citations or source support", router_text)

    def test_helpers_and_transitive_imports_run_from_isolated_bundle(self) -> None:
        module = load_library(self)
        with tempfile.TemporaryDirectory() as temporary_directory:
            directory, _ = module.build_standalone_skill(
                ROOT,
                "discovery-runner-deduper",
                Path(temporary_directory) / "output",
            )
            scripts_directory = directory / "scripts"
            expected_scripts = {
                "check_source_candidates.py",
                "check_citation_metadata.py",
                "plugin_utils.py",
            }
            self.assertTrue(expected_scripts.issubset({path.name for path in scripts_directory.glob("*.py")}))
            for script_name in sorted(expected_scripts):
                result = subprocess.run(
                    [sys.executable, script_name, "--help"],
                    cwd=scripts_directory,
                    check=False,
                    capture_output=True,
                    text=True,
                    env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                )
                self.assertEqual(result.returncode, 0, f"{script_name}: {result.stderr}")


class PackageIntegrationTests(unittest.TestCase):
    def load_script_module(self, relative_path: str, module_name: str):
        return load_script_module(self, relative_path, module_name)

    def test_package_inventory_ships_registry_and_all_standalone_runtime_scripts(self) -> None:
        plugin_utils = self.load_script_module("scripts/plugin_utils.py", "portable_plugin_utils")
        packaged = {path.relative_to(ROOT).as_posix() for path in plugin_utils.package_files(ROOT)}
        self.assertTrue(
            {
                "shared/standalone-skill-registry.json",
                "scripts/standalone_skill_bundles.py",
                "scripts/build_standalone_skill.py",
                "scripts/validate_standalone_skill.py",
                "scripts/check_standalone_skills.py",
            }.issubset(packaged)
        )

    def test_package_scope_includes_standalone_catalog_check(self) -> None:
        package_checks = self.load_script_module(
            "scripts/run_package_checks.py",
            "portable_run_package_checks",
        )
        self.assertIn(("scripts/check_standalone_skills.py",), package_checks.PACKAGE_CHECKS)
        self.assertIn(("scripts/check_standalone_skills.py",), package_checks.FULL_CHECKS)

    def test_project_reference_scan_ignores_control_plane_but_keeps_package_docs(self) -> None:
        validator = self.load_script_module(
            "scripts/validate_plugin.py",
            "portable_validate_plugin",
        )
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            package_document = root / "docs" / "package.md"
            package_document.parent.mkdir()
            package_document.write_text(
                "[missing package reference](docs/missing.md)\n",
                encoding="utf-8",
            )
            control_document = root / ".recursive" / "run" / "control.md"
            control_document.parent.mkdir(parents=True)
            control_document.write_text(
                "[missing control reference](docs/control-missing.md)\n",
                encoding="utf-8",
            )

            errors = validator.validate_project_references(root)

            self.assertTrue(any("docs/package.md" in error for error in errors))
            self.assertFalse(any(".recursive" in error for error in errors))

    def test_package_checker_builds_and_validates_complete_catalog_without_residue(self) -> None:
        plugin_utils = self.load_script_module("scripts/plugin_utils.py", "portable_copy_plugin_utils")
        with tempfile.TemporaryDirectory() as temporary_directory:
            packaged_root = Path(temporary_directory) / "packaged-plugin"
            plugin_utils.copy_package_tree(ROOT, packaged_root)
            checker = packaged_root / "scripts" / "check_standalone_skills.py"
            self.assertTrue(checker.is_file(), "package-safe standalone checker is missing")
            result = subprocess.run(
                [sys.executable, str(checker)],
                cwd=packaged_root,
                check=False,
                capture_output=True,
                text=True,
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Validated 28 standalone bundle pairs", result.stdout)
            self.assertFalse((packaged_root / "dist").exists())
            self.assertEqual(list(packaged_root.rglob("__pycache__")), [])
            self.assertEqual(list(packaged_root.rglob("*.pyc")), [])


class DocumentationTests(unittest.TestCase):
    def load_public_docs(self) -> dict[str, str]:
        paths = {
            "readme": ROOT / "README.md",
            "installation": ROOT / "docs" / "user" / "INSTALLATION.md",
            "architecture": ROOT / "docs" / "reference" / "ARCHITECTURE.md",
            "scripts": ROOT / "docs" / "reference" / "SCRIPTS.md",
        }
        return {name: path.read_text(encoding="utf-8") for name, path in paths.items()}

    def test_docs_replace_raw_copy_and_raw_zip_instructions_with_generated_outputs(self) -> None:
        docs = self.load_public_docs()
        public_text = "\n".join(docs.values())
        self.assertNotIn("cp -R skills/*", public_text)
        self.assertNotIn("zip an individual folder under `skills/<skill-name>/`", public_text)
        self.assertNotIn("`docs/superpowers/`", docs["scripts"])
        self.assertIn(
            "python3 scripts/build_standalone_skill.py --skill <skill-name>",
            docs["installation"],
        )
        self.assertIn(
            "python3 scripts/build_standalone_skill.py --all",
            docs["installation"],
        )
        self.assertIn("generated directory", docs["installation"].lower())
        self.assertIn("generated zip", docs["installation"].lower())

    def test_docs_cover_validation_python_boundaries_classification_and_rebuild_guidance(self) -> None:
        docs = self.load_public_docs()
        installation = docs["installation"]
        scripts = docs["scripts"]
        architecture = docs["architecture"]
        self.assertIn(
            "python3 scripts/validate_standalone_skill.py dist/standalone-skills/<skill-name>",
            installation,
        )
        self.assertIn(
            "python3 scripts/validate_standalone_skill.py dist/standalone-skills/<skill-name>.zip",
            installation,
        )
        self.assertIn("--require-catalog-complete", scripts)
        self.assertIn("Python 3.10", installation)
        self.assertIn("instruction-only", installation)
        self.assertIn("No pip packages", installation)
        for classification in ("self-sufficient", "route-only", "full-plugin-only"):
            self.assertIn(classification, architecture)
        self.assertIn("same skill name", installation)
        self.assertIn("replace", installation.lower())

    def test_docs_state_canonical_ownership_output_behavior_and_full_plugin_recommendation(self) -> None:
        docs = self.load_public_docs()
        public_text = "\n".join(docs.values())
        self.assertIn("canonical source", public_text)
        self.assertIn("generated", docs["architecture"].lower())
        self.assertIn("dependency closure", docs["architecture"].lower())
        self.assertIn("dist/standalone-skills", docs["scripts"])
        self.assertIn("deterministic", docs["scripts"].lower())
        self.assertIn("existing valid output", docs["scripts"].lower())
        self.assertIn("recommend", docs["readme"].lower())
        self.assertIn("full plugin", docs["readme"].lower())


if __name__ == "__main__":
    unittest.main()
