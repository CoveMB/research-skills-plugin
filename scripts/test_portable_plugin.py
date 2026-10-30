"""Behavioral checks for full-catalog portable exports and safe publication."""
from __future__ import annotations

import importlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from plugin_utils import copy_package_tree, package_files, parse_markdown_frontmatter
from standalone_skill_bundles import discover_direct_dependencies

ROOT = Path(__file__).resolve().parents[1]
SKILL = "skills/research-intent-router/SKILL.md"


def write_files(root: Path, files: dict[str, bytes]) -> None:
    for name, data in files.items():
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)


class PortableFixture(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name).resolve()
        self.source = self.directory / "source"
        copy_package_tree(ROOT, self.source)
        self.portable = importlib.import_module("portable_plugin")

    def append_reference(self, text: str) -> None:
        with (self.source / SKILL).open("a") as stream:
            stream.write("\n" + text + "\n")


class PortableRenderingTests(PortableFixture):
    def test_full_catalog_preserves_discovery_and_canonical_bytes(self) -> None:
        before = {p.relative_to(self.source).as_posix(): p.read_bytes() for p in package_files(self.source)}
        rendered = self.portable.render_portable_files(self.source)
        names = {p for p in rendered if p.startswith("skills/") and p.endswith("/SKILL.md")}
        self.assertEqual(names, {p for p in before if p.startswith("skills/") and p.endswith("/SKILL.md")})
        self.assertEqual(len(names), 29)
        self.assertIn("skills/research-book-orchestrator/SKILL.md", names)
        self.assertIn(SKILL, names)
        for name in names:
            self.assertEqual(parse_markdown_frontmatter(rendered[name].decode()), parse_markdown_frontmatter(before[name].decode()))
        for name in before:
            if name.endswith("agents/openai.yaml") or name == ".codex-plugin/plugin.json":
                self.assertEqual(rendered[name], before[name])
        self.assertEqual({p: (self.source / p).read_bytes() for p in before}, before)

    def test_rendered_references_resolve_without_root_fallback(self) -> None:
        files = self.portable.render_portable_files(self.source)
        self.assertIn("../../docs/policy/SOURCE_LIMITS.md", files[SKILL].decode())
        self.assertIn("../../MODE_REGISTRY.md", files[SKILL].decode())
        installed = self.directory / "installed"
        write_files(installed, files)
        self.assertEqual(self.portable.validate_portable_tree(installed), [])
        target = installed / SKILL
        target.write_text(target.read_text().replace("../../MODE_REGISTRY.md", "MODE_REGISTRY.md"))
        self.assertTrue(self.portable.validate_portable_tree(installed))
        target.write_bytes(files[SKILL])
        (installed / "skills/research-book-orchestrator/SKILL.md").unlink()
        self.assertTrue(self.portable.validate_portable_tree(installed))

    def test_reference_occurrences_preserve_urls_examples_and_user_paths(self) -> None:
        unchanged = "https://example.invalid/docs/policy/SOURCE_LIMITS.md path/to/docs/policy/SOURCE_LIMITS.md"
        illustration = "```text\ndocs/policy/SOURCE_LIMITS.md\n```"
        self.append_reference(unchanged + "\n" + illustration + "\n[policy](docs/policy/SOURCE_LIMITS.md#limits)\n`docs/policy/SOURCE_LIMITS.md`\n`python3 scripts/check_source_candidates.py --input path/to/source-candidates.json`")
        text = self.portable.render_portable_files(self.source)[SKILL].decode()
        self.assertIn(unchanged, text)
        self.assertIn(illustration, text)
        self.assertIn("[policy](../../docs/policy/SOURCE_LIMITS.md#limits)", text)
        self.assertIn("`../../docs/policy/SOURCE_LIMITS.md`", text)
        self.assertIn("python3 ../../scripts/check_source_candidates.py --input path/to/source-candidates.json", text)

    def test_relative_helper_command_stays_discoverable(self) -> None:
        installed = self.directory / "installed"
        write_files(installed, self.portable.render_portable_files(self.source))
        resources, helpers = discover_direct_dependencies(installed, "discovery-runner-deduper")
        self.assertIn("scripts/check_source_candidates.py", helpers)
        self.assertIn("docs/policy/SOURCE_LIMITS.md", resources)

    def test_router_bare_registry_reference_preserves_nonresource_spans(self) -> None:
        preserved = [
            '[External](https://example.invalid/manual?file=MODE_REGISTRY.md)',
            '<https://example.invalid/manual?file=MODE_REGISTRY.md>',
            'https://example.invalid/manual?file=MODE_REGISTRY.md',
            '`example_function("MODE_REGISTRY.md")`',
            'example_function("MODE_REGISTRY.md")',
            "example_function('MODE_REGISTRY.md')",
            '`tool --input MODE_REGISTRY.md`',
            'tool --input MODE_REGISTRY.md',
            'tool --input=MODE_REGISTRY.md',
            'path/to/MODE_REGISTRY.md',
            '[MODE_REGISTRY.md](https://example.invalid/manual)',
            '`[Registry](MODE_REGISTRY.md)`',
        ]
        self.append_reference("\n".join(preserved) + '\nMODE_REGISTRY.md is canonical.\nUse `MODE_REGISTRY.md`.\n[Registry](MODE_REGISTRY.md#routes)' + "\nThe package's MODE_REGISTRY.md preserves the user's choices.")
        text = self.portable.render_portable_files(self.source)[SKILL].decode()
        for value in preserved:
            with self.subTest(value=value):
                self.assertTrue(value in text, f"nonresource span changed: {value}")
        self.assertIn('../../MODE_REGISTRY.md is canonical.', text)
        self.assertIn('Use `../../MODE_REGISTRY.md`.', text)
        self.assertIn('[Registry](../../MODE_REGISTRY.md#routes)', text)
        self.assertTrue("The package's ../../MODE_REGISTRY.md preserves the user's choices." in text)

    def test_explicit_resources_survive_apostrophes_and_formatted_link_labels(self) -> None:
        cases = (
            "Follow the package's `docs/policy/SOURCE_LIMITS.md` so the user's consent is preserved.",
            '[Policy `reference`](docs/policy/SOURCE_LIMITS.md)',
        )
        self.append_reference("\n".join(cases))
        files = self.portable.render_portable_files(self.source)
        text = files[SKILL].decode()
        installed = self.directory / "installed"
        write_files(installed, files)
        self.assertEqual(self.portable.validate_portable_tree(installed), [])
        for original in cases:
            with self.subTest(reference=original):
                rewritten = original.replace('docs/policy/', '../../docs/policy/')
                self.assertTrue(rewritten in text, f"explicit resource was not rewritten: {original}")
                (installed / SKILL).write_text(text.replace(rewritten, original))
                self.assertTrue(self.portable.validate_portable_tree(installed), "checker missed a root-relative resource operand")

    def test_missing_skill_helper_command_is_rejected(self) -> None:
        self.append_reference("Run `python3 scripts/missing_helper.py --input path/to/user.json`.")
        with self.assertRaises(ValueError):
            self.portable.render_portable_files(self.source)

    def test_missing_transitive_python_dependency_is_rejected(self) -> None:
        helper = self.source / "scripts/check_source_candidates.py"
        with helper.open("a") as stream:
            stream.write("\nimport missing_portable_dependency\n")
        with self.assertRaises(ValueError):
            self.portable.render_portable_files(self.source)

    def test_checker_rejects_broken_nested_resources_and_registry(self) -> None:
        files = self.portable.render_portable_files(self.source)
        installed = self.directory / "installed"
        write_files(installed, files)
        policy = installed / "docs/policy/CORPUS_REPRESENTATIVENESS_TAXONOMY.md"
        policy.unlink()
        self.assertTrue(self.portable.validate_portable_tree(installed))
        policy.write_bytes(files["docs/policy/CORPUS_REPRESENTATIVENESS_TAXONOMY.md"])
        registry_path = installed / "shared/standalone-skill-registry.json"
        registry = json.loads(registry_path.read_text())
        for entry in registry["skills"]:
            if entry["name"] == "research-book-orchestrator":
                entry["classification"] = "self-sufficient"
        registry_path.write_text(json.dumps(registry))
        self.assertTrue(self.portable.validate_portable_tree(installed))

    def test_rejects_missing_ambiguous_excluded_and_symlinked_dependencies(self) -> None:
        cases = ("missing", "ambiguous", "excluded", "file-alias", "directory-alias", "escape")
        for case in cases:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary) / "plugin"
                copy_package_tree(ROOT, root)
                reference = "docs/policy/SOURCE_LIMITS.md"
                if case == "missing":
                    reference = "docs/missing.md"
                elif case == "ambiguous":
                    write_files(root, {"skills/research-intent-router/docs/policy/SOURCE_LIMITS.md": b"conflicting"})
                elif case == "excluded":
                    reference = "docs/secrets.json"
                    write_files(root, {reference: b"{}"})
                elif case == "file-alias":
                    reference = "docs/alias.md"
                    (root / reference).symlink_to(root / "docs/policy/SOURCE_LIMITS.md")
                elif case == "directory-alias":
                    reference = "docs/alias/SOURCE_LIMITS.md"
                    (root / "docs/alias").symlink_to(root / "docs/policy", target_is_directory=True)
                elif case == "escape":
                    outside = Path(temporary) / "outside.md"
                    outside.write_text("outside")
                    reference = "../../../outside.md"
                with (root / SKILL).open("a") as stream:
                    stream.write(f"\nUse `{reference}`.\n")
                with self.assertRaises(ValueError):
                    self.portable.render_portable_files(root)

    def test_portable_exclusions_omit_credentials_and_reject_references(self) -> None:
        write_files(self.source, {"docs/credentials.json": b"private sentinel"})
        self.assertNotIn("docs/credentials.json", self.portable.render_portable_files(self.source))
        self.append_reference("Use `docs/credentials.json`.")
        with self.assertRaises(ValueError):
            self.portable.render_portable_files(self.source)

    def test_adapter_projects_only_supported_fields(self) -> None:
        manifest = json.loads((self.source / ".codex-plugin/plugin.json").read_text())
        projected = self.portable.project_antigravity_manifest(manifest)
        self.assertEqual(set(projected), {"$schema", "name", "version", "description", "author", "license", "displayName", "logo", "suggestedPrompts"})
        self.assertEqual(projected["name"], "research-skills-plugin")
        self.assertEqual(projected["version"], "1.1.0")
        self.assertEqual(projected["suggestedPrompts"], manifest["interface"]["defaultPrompt"][:3])
        minimal = self.portable.project_antigravity_manifest({"name": "sample"})
        self.assertEqual(minimal, {"$schema": "https://antigravity.google/schemas/v1/plugin.json", "name": "sample"})
        for field, value in (("version", 1), ("author", []), ("interface", []), ("interface", {"logo": 1}), ("interface", {"defaultPrompt": [1]})):
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                self.portable.project_antigravity_manifest({**manifest, field: value})
        manifest["interface"]["logo"] = "../outside.svg"
        (self.source / ".codex-plugin/plugin.json").write_text(json.dumps(manifest))
        with self.assertRaises(ValueError):
            self.portable.render_portable_files(self.source)

    def test_adapter_accepts_documented_author_forms(self) -> None:
        for author in ("Publisher", {"name": "Publisher", "url": "https://example.invalid"}):
            with self.subTest(author=author):
                self.assertEqual(self.portable.project_antigravity_manifest({"name": "sample", "author": author})["author"], author)
        for author in ("", {"name": "Publisher", "url": "http://example.invalid"}):
            with self.subTest(author=author), self.assertRaises(ValueError):
                self.portable.project_antigravity_manifest({"name": "sample", "author": author})


class PortablePublicationTests(PortableFixture):
    def setUp(self) -> None:
        super().setUp()
        self.packager = importlib.import_module("package_plugin")

    def test_default_packaging_is_unchanged(self) -> None:
        output = self.directory / "ordinary.zip"
        self.packager.write_package(self.source, output)
        self.assertEqual(self.packager.default_output_path(self.source), Path("research-skills-plugin-v1.1.0.zip"))
        with zipfile.ZipFile(output) as archive:
            self.assertEqual(archive.read("research-skills-plugin/" + SKILL), (self.source / SKILL).read_bytes())
            self.assertNotIn("research-skills-plugin/.antigravity-plugin/plugin.json", archive.namelist())

    def test_portable_cli_uses_separate_default_and_full_prefix(self) -> None:
        result = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/package_plugin.py"), "--portable", "--root", str(self.source)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        output = self.source / "dist/portable-plugin/research-skills-plugin-v1.1.0-portable.zip"
        with zipfile.ZipFile(output) as archive:
            names = archive.namelist()
            self.assertTrue(all(name.startswith("research-skills-plugin/") for name in names))
            self.assertEqual(sum(name.endswith("/SKILL.md") for name in names), 29)
            self.assertIn("research-skills-plugin/.antigravity-plugin/plugin.json", names)
            self.assertTrue(archive.getinfo("research-skills-plugin/validate.sh").external_attr >> 16 & 0o111)

    def test_existing_output_and_symlink_targets_are_refused(self) -> None:
        sentinel = self.directory / "sentinel"
        sentinel.write_bytes(b"preserve me")
        link = self.directory / "link.zip"
        link.symlink_to(sentinel)
        parent_link = self.directory / "parent-link"
        parent_link.symlink_to(self.directory, target_is_directory=True)
        for output in (sentinel, link, parent_link / "new.zip", self.source / "docs/new.zip"):
            with self.subTest(output=output), self.assertRaises((ValueError, OSError)):
                self.packager.write_portable_package(self.source, output)
        self.assertEqual(sentinel.read_bytes(), b"preserve me")
        self.assertFalse((self.directory / "new.zip").exists())
        self.assertFalse((self.source / "docs/new.zip").exists())

    def test_validation_or_write_failure_leaves_no_partial_archive(self) -> None:
        output = self.directory / "new.zip"
        unrelated = self.directory / "new.zip.tmp"
        unrelated.write_bytes(b"unrelated")
        for target in ("render_portable_files", "validate_portable_archive"):
            with self.subTest(target=target), patch.object(self.packager, target, side_effect=ValueError("injected failure")):
                with self.assertRaises(ValueError):
                    self.packager.write_portable_package(self.source, output)
            self.assertFalse(output.exists())
            self.assertEqual(unrelated.read_bytes(), b"unrelated")
            self.assertEqual(sorted(p.name for p in self.directory.iterdir()), ["new.zip.tmp", "source"])
        with patch.object(zipfile.ZipFile, "writestr", side_effect=OSError("disk full")):
            with self.assertRaises(OSError):
                self.packager.write_portable_package(self.source, output)
        self.assertFalse(output.exists())
        self.assertEqual(unrelated.read_bytes(), b"unrelated")
        self.assertEqual(sorted(p.name for p in self.directory.iterdir()), ["new.zip.tmp", "source"])
        real_link = os.link

        def collide(source: str, destination: str, **options: object) -> None:
            descriptor = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600, dir_fd=options["dst_dir_fd"])
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(b"concurrent writer")
            real_link(source, destination, **options)

        with patch.object(self.packager.os, "link", side_effect=collide):
            with self.assertRaises(FileExistsError):
                self.packager.write_portable_package(self.source, output)
        self.assertEqual(output.read_bytes(), b"concurrent writer")
        self.assertEqual(unrelated.read_bytes(), b"unrelated")

    def test_generated_export_cannot_be_packaged_again(self) -> None:
        installed = self.directory / "installed"
        write_files(installed, self.portable.render_portable_files(self.source))
        output = self.directory / "recursive.zip"
        with self.assertRaises(ValueError):
            self.packager.write_portable_package(installed, output)
        self.assertFalse(output.exists())

    def test_parent_replacement_preserves_sentinel_and_cleans_original_staging(self) -> None:
        real_validator = self.packager.validate_portable_archive
        for replacement_kind in ("symlink", "directory"):
            with self.subTest(replacement_kind=replacement_kind):
                parent = self.directory / replacement_kind
                parent.mkdir()
                output = parent / "candidate.zip"
                moved_parent = self.directory / (replacement_kind + "-moved")
                unrelated = self.directory / (replacement_kind + "-unrelated")
                unrelated.mkdir()
                sentinel = None

                def replace_parent(archive: object, prefix: str) -> None:
                    nonlocal sentinel
                    real_validator(archive, prefix)
                    staging_name = next(parent.glob(".*.tmp")).name
                    parent.rename(moved_parent)
                    if replacement_kind == "symlink":
                        parent.symlink_to(unrelated, target_is_directory=True)
                    else:
                        parent.mkdir()
                    sentinel = parent / staging_name
                    sentinel.write_bytes(b"unrelated sentinel")

                with patch.object(self.packager, "validate_portable_archive", side_effect=replace_parent):
                    with self.assertRaises((ValueError, OSError)):
                        self.packager.write_portable_package(self.source, output)
                self.assertIsNotNone(sentinel)
                self.assertTrue(sentinel.is_file(), "cleanup deleted the unrelated sentinel")
                self.assertEqual(sentinel.read_bytes(), b"unrelated sentinel")
                self.assertEqual(list(moved_parent.iterdir()), [], "owned staging archive was left behind")
                self.assertFalse(output.exists())

    def test_replaced_staging_file_is_neither_published_nor_deleted(self) -> None:
        parent = self.directory / "publication"
        parent.mkdir()
        output = parent / "candidate.zip"
        retained = parent / "moved-owned-archive"
        real_validator = self.packager.validate_portable_archive
        sentinel = None

        def replace_staging(archive: object, prefix: str) -> None:
            nonlocal sentinel
            real_validator(archive, prefix)
            sentinel = next(parent.glob(".*.tmp"))
            sentinel.rename(retained)
            sentinel.write_bytes(b"replacement sentinel")

        with patch.object(self.packager, "validate_portable_archive", side_effect=replace_staging):
            with self.assertRaises((ValueError, OSError)):
                self.packager.write_portable_package(self.source, output)
        self.assertIsNotNone(sentinel)
        self.assertEqual(sentinel.read_bytes(), b"replacement sentinel")
        self.assertTrue(retained.is_file())
        self.assertFalse(output.exists())

    def test_missing_safe_filesystem_primitives_refuse_publication(self) -> None:
        output = self.directory / "unsupported.zip"
        before = set(self.directory.iterdir())
        with patch.object(self.packager, "DIRECTORY_OPERATIONS_SUPPORTED", False, create=True):
            with self.assertRaisesRegex(OSError, "directory.*operations"):
                self.packager.write_portable_package(self.source, output)
        self.assertEqual(set(self.directory.iterdir()), before)

    def test_normal_validation_checks_adapter_when_present(self) -> None:
        installed = self.directory / "installed"
        write_files(installed, self.portable.render_portable_files(self.source))
        adapter = installed / ".antigravity-plugin/plugin.json"
        adapter.write_text('{"name": "wrong"}')
        result = subprocess.run([sys.executable, "-B", str(installed / "scripts/validate_plugin.py"), str(installed)], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("adapter", result.stdout.lower())
        adapter.unlink()
        self.assertTrue(self.portable.validate_portable_tree(installed))

    def test_archive_checker_rejects_unsafe_or_incomplete_members(self) -> None:
        for name, mode in (("../escape", 0o100644), ("research-skills-plugin/link", 0o120777), ("/absolute", 0o100644), ("other-root/file", 0o100644)):
            with self.subTest(name=name):
                archive_path = self.directory / "invalid.zip"
                with zipfile.ZipFile(archive_path, "w") as archive:
                    info = zipfile.ZipInfo(name)
                    info.external_attr = mode << 16
                    archive.writestr(info, b"invalid")
                with self.assertRaises(ValueError):
                    self.packager.validate_portable_archive(archive_path, "research-skills-plugin")
        with zipfile.ZipFile(archive_path, "w") as archive:
            archive.writestr("research-skills-plugin/file", b"a")
            archive.writestr("research-skills-plugin/FILE", b"b")
        with self.assertRaises(ValueError):
            self.packager.validate_portable_archive(archive_path, "research-skills-plugin")


class PortableInstalledRuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        temporary = tempfile.TemporaryDirectory()
        cls.addClassCleanup(temporary.cleanup)
        cls.directory = Path(temporary.name).resolve()
        cls.source = cls.directory / "source copy"
        cls.workspace = cls.directory / "unrelated user workspace"
        cls.workspace.mkdir()
        copy_package_tree(ROOT, cls.source)
        cls.expected_names = {path.relative_to(cls.source).as_posix() for path in package_files(cls.source)} | {".antigravity-plugin/plugin.json"}
        cls.excluded_names = (".env", "docs/credentials.json", "docs/secrets.json", ".git/config", "scripts/__pycache__/private.pyc", "dist/private.txt", "docs/superpowers/private-plan.md")
        write_files(cls.source, {name: b"PRIVATE_TEST_SENTINEL" for name in cls.excluded_names})
        cls.archive_path = cls.directory / "portable.zip"
        cls.environment = {key: value for key, value in os.environ.items() if key not in {"PYTHONPATH", "PYTHONHOME"}}
        cls.environment["PYTHONDONTWRITEBYTECODE"] = "1"
        result = subprocess.run([sys.executable, "-B", str(cls.source / "scripts/package_plugin.py"), "--portable", "--out", str(cls.archive_path)], cwd=cls.workspace, env=cls.environment, capture_output=True, text=True)
        if result.returncode:
            raise AssertionError(result.stdout + result.stderr)
        with zipfile.ZipFile(cls.archive_path) as archive:
            archive.extractall(cls.directory / "relocated installation")
        cls.installed = cls.directory / "relocated installation/research-skills-plugin"
        shutil.rmtree(cls.source)  # Only this fixture-owned copy, never the real checkout.

    def run_installed(self, script: str, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, "-B", str(self.installed / "scripts" / script), *arguments], cwd=self.workspace, env=self.environment, capture_output=True, text=True)

    def test_relocated_full_runtime_and_helper_with_spaces(self) -> None:
        self.assertFalse(self.source.exists())
        result = self.run_installed("portable_plugin.py", "--check", str(self.installed))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        fixture = self.workspace / "synthetic candidates.json"
        fixture.write_text(json.dumps([{"candidate_id": "synthetic-a", "title": "Synthetic relocation fixture", "search_status": "planned"}]))
        bad_fixture = self.workspace / "malformed candidates.json"
        bad_fixture.write_text('{"records": [1]}')
        before = {p.name: p.read_bytes() for p in self.workspace.iterdir()}
        help_result = self.run_installed("check_source_candidates.py", "--help")
        self.assertEqual(help_result.returncode, 0, help_result.stderr)
        result = self.run_installed("check_source_candidates.py", "--input", fixture.name)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["source"]["input"], fixture.name)
        self.assertEqual(report["records"][0]["candidate_id"], "synthetic-a")
        result = self.run_installed("check_source_candidates.py", "--input", bad_fixture.name)
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(json.loads(result.stdout)["errors"])
        self.assertEqual({p.name: p.read_bytes() for p in self.workspace.iterdir()}, before)

    def test_extracted_package_rebuilds_all_28_standalones(self) -> None:
        result = self.run_installed("run_package_checks.py", "--scope", "package")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Validated 28 standalone bundle pairs", result.stdout)
        self.assertFalse((self.installed / "dist").exists())
        self.assertEqual(list(self.installed.rglob("__pycache__")), [])

    def test_actual_archive_excludes_private_and_planning_material(self) -> None:
        with zipfile.ZipFile(self.archive_path) as archive:
            files = {name.removeprefix("research-skills-plugin/"): archive.read(name) for name in archive.namelist()}
        self.assertEqual(set(files), self.expected_names)
        self.assertFalse(set(self.excluded_names).intersection(files))
        for name, data in files.items():
            with self.subTest(name=name):
                self.assertNotIn(str(self.source).encode(), data)
                self.assertNotIn(str(self.workspace).encode(), data)
                if not name.startswith("scripts/test_"):
                    self.assertNotIn(b"PRIVATE_TEST_SENTINEL", data)


if __name__ == "__main__":
    unittest.main()
