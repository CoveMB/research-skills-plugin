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

    def test_package_excludes_repository_only_docs(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "plugin"
            write_minimal_plugin(root)
            repository_only_path = root / "docs" / "superpowers" / "plans" / "future-plan.md"
            public_documentation_path = root / "docs" / "user" / "guide.md"
            repository_only_path.parent.mkdir(parents=True)
            public_documentation_path.parent.mkdir(parents=True)
            repository_only_path.write_text("internal plan", encoding="utf-8")
            public_documentation_path.write_text("public guide", encoding="utf-8")
            output_path = Path(temporary_directory) / "bundle.zip"

            result = run_script("package_plugin.py", "--root", str(root), "--out", str(output_path))
            self.assertEqual(result.returncode, 0, msg=f"stdout={result.stdout} stderr={result.stderr}")
            with zipfile.ZipFile(output_path) as archive:
                names = archive.namelist()
            self.assertNotIn("sample-plugin/docs/superpowers/plans/future-plan.md", names)
            self.assertIn("sample-plugin/docs/user/guide.md", names)

    def test_package_excludes_symlinked_files(self) -> None:
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
            self.assertEqual(result.returncode, 0, msg=f"stdout={result.stdout} stderr={result.stderr}")
            with zipfile.ZipFile(output_path) as archive:
                names = archive.namelist()
            self.assertNotIn("sample-plugin/docs/linked-secret.md", names)

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
            "research-skills-plugin-v1.1.0.zip",
        )

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

    def test_validation_workflow_runs_validate_script(self) -> None:
        workflow_path = ROOT / ".github" / "workflows" / "validate.yml"

        self.assertTrue(workflow_path.exists())
        text = workflow_path.read_text(encoding="utf-8")
        self.assertIn("pull_request:", text)
        self.assertIn("push:", text)
        self.assertIn("python-version: '3.10'", text)
        self.assertIn("bash validate.sh", text)

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
            "check_marketplace.py": [
                "Validate the repository's versioned Git marketplace metadata.",
                "--root",
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
