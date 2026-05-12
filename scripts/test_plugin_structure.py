"""Structure tests for plugin skill routing and naming."""
from __future__ import annotations

import json
import re
import sys
import unittest
from functools import cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from plugin_utils import (
    CONTRACT_ARTIFACT_SKILLS,
    MIN_SHARED_DESCRIPTION_TERMS,
    significant_description_terms,
)

SKILLS_DIR = ROOT / "skills"
REQUIRED_SKILL_HEADINGS = [
    "## Purpose",
    "## When to use",
    "## Inputs expected",
    "## Procedure",
    "## Output format",
    "## Quality checks",
    "## Failure modes",
    "## Files/folders it may read",
    "## Files/folders it may write",
    "## What it must not do",
]
REQUIRED_README_HEADINGS = [
    "## Procedure",
    "## Quality checks",
    "## Failure modes",
    "## Files/folders it may read",
    "## Files/folders it may write",
    "## What it must not do",
    "## Best next steps",
]
SUGGESTED_NEXT_STEP_TEMPLATE_PHRASES = [
    "Use `skill-name` to [specific next action].",
    "Why this helps scholarship: [named risk reduced].",
    "Use only if: [condition].",
    "Skip if: [reason it would add noise now].",
]
PROVENANCE_FIELDS = [
    "source_basis",
    "what_i_can_verify",
    "what_remains_uncertain",
    "user_verification_needed",
]


@cache
def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read_text(path))


def skill_markdown(skill_dir: Path) -> str:
    return read_text(skill_dir / "SKILL.md")


def skill_readme(skill_dir: Path) -> str:
    return read_text(skill_dir / "README.md")


def read_text_files() -> list[tuple[Path, str]]:
    files: list[tuple[Path, str]] = []
    for path in sorted(ROOT.rglob("*")):
        if ".git" in path.parts or path.is_dir():
            continue
        if path == Path(__file__).resolve():
            continue
        if path.suffix in {".md", ".json", ".yaml", ".yml", ".sh", ".py"}:
            files.append((path, read_text(path)))
    return files


def frontmatter_name(skill_markdown: str) -> str:
    return frontmatter_field(skill_markdown, "name")


def frontmatter_field(skill_markdown: str, field_name: str) -> str:
    match = re.search(rf"^{re.escape(field_name)}:\s*(.+?)\s*$", skill_markdown, re.MULTILINE)
    return match.group(1).strip().strip('"').strip("'") if match else ""


def metadata_field(metadata_text: str, field_name: str) -> str:
    match = re.search(rf"^\s*{re.escape(field_name)}:\s*(.+?)\s*$", metadata_text, re.MULTILINE)
    return match.group(1).strip().strip('"').strip("'") if match else ""


def missing_phrases(text: str, phrases: list[str]) -> list[str]:
    return [phrase for phrase in phrases if phrase not in text]


def missing_labeled_phrases(label: str, text: str, phrases: list[str]) -> list[str]:
    return [f"{label}: {phrase}" for phrase in missing_phrases(text, phrases)]


def schema_conditionals(schema_node: object) -> list[dict]:
    conditionals: list[dict] = []
    if isinstance(schema_node, dict):
        if isinstance(schema_node.get("if"), dict):
            conditionals.append(schema_node)
        for value in schema_node.values():
            conditionals.extend(schema_conditionals(value))
    elif isinstance(schema_node, list):
        for value in schema_node:
            conditionals.extend(schema_conditionals(value))
    return conditionals


def const_condition_keys(condition: dict) -> list[str]:
    properties = condition.get("properties")
    if not isinstance(properties, dict):
        return []
    return [
        key
        for key, property_schema in properties.items()
        if isinstance(key, str) and isinstance(property_schema, dict) and "const" in property_schema
    ]


class TestPluginStructure(unittest.TestCase):
    def skill_dirs(self) -> list[Path]:
        return sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir())

    def test_research_book_orchestrator_replaces_old_skill_name(self) -> None:
        old_skill_name = "-".join(["scholar" + "ly", "book", "orchestrator"])
        skill_path = SKILLS_DIR / "research-book-orchestrator" / "SKILL.md"
        self.assertTrue(skill_path.is_file())
        self.assertFalse((SKILLS_DIR / old_skill_name).exists())
        self.assertEqual(frontmatter_name(read_text(skill_path)), "research-book-orchestrator")

        stale_references = [
            str(path.relative_to(ROOT))
            for path, text in read_text_files()
            if old_skill_name in text
        ]
        self.assertEqual(stale_references, [])

    def test_each_skill_has_operational_sections(self) -> None:
        missing: list[str] = []
        for skill_dir in self.skill_dirs():
            text = skill_markdown(skill_dir)
            for heading in REQUIRED_SKILL_HEADINGS:
                if heading not in text:
                    missing.append(f"{skill_dir.name}: {heading}")
        self.assertEqual(missing, [])

    def test_each_skill_readme_documents_operational_boundaries(self) -> None:
        missing: list[str] = []
        for skill_dir in self.skill_dirs():
            text = skill_readme(skill_dir)
            for heading in REQUIRED_README_HEADINGS:
                if heading not in text:
                    missing.append(f"{skill_dir.name}: {heading}")
        self.assertEqual(missing, [])

    def test_skill_readmes_defer_common_operational_boundaries_to_shared_doc(self) -> None:
        shared_doc = ROOT / "docs" / "SKILL_OPERATIONAL_BOUNDARIES.md"
        self.assertTrue(shared_doc.is_file())
        shared_text = read_text(shared_doc)
        for heading in REQUIRED_README_HEADINGS[:-1]:
            self.assertIn(heading, shared_text)

        missing_references = [
            skill_dir.name
            for skill_dir in self.skill_dirs()
            if "docs/SKILL_OPERATIONAL_BOUNDARIES.md" not in skill_readme(skill_dir)
        ]
        self.assertEqual(missing_references, [])

    def test_skill_readmes_do_not_duplicate_shared_operational_bullets(self) -> None:
        duplicated_phrases = [
            "State the source basis and source access level.",
            "Fabricated citations, quotes, page numbers, source metadata, datasets, market facts, or field consensus.",
            "Bundled skill instructions, metadata, and assets if available",
        ]
        offenders = [
            f"{skill_dir.name}: {phrase}"
            for skill_dir in self.skill_dirs()
            for phrase in duplicated_phrases
            if phrase in skill_readme(skill_dir)
        ]
        self.assertEqual(offenders, [])

    def test_each_skill_has_ai_safety_rules(self) -> None:
        missing: list[str] = []
        required_phrases = [
            "source access level",
            "What I can verify",
            "What remains uncertain",
            "User verification needed",
            "Do not invent citations",
        ]
        for skill_dir in self.skill_dirs():
            text = skill_markdown(skill_dir)
            missing.extend(missing_labeled_phrases(skill_dir.name, text, required_phrases))
        self.assertEqual(missing, [])

    def test_agent_short_descriptions_track_skill_descriptions(self) -> None:
        stale_metadata: list[str] = []
        for skill_dir in self.skill_dirs():
            skill_description = frontmatter_field(
                skill_markdown(skill_dir),
                "description",
            )
            short_description = metadata_field(
                read_text(skill_dir / "agents" / "openai.yaml"),
                "short_description",
            )
            skill_terms = significant_description_terms(skill_description)
            short_description_terms = significant_description_terms(short_description)
            shared_terms = skill_terms & short_description_terms
            if len(shared_terms) < MIN_SHARED_DESCRIPTION_TERMS:
                stale_metadata.append(f"{skill_dir.name}: {len(shared_terms)} shared terms")
        self.assertEqual(stale_metadata, [])

    def test_shared_source_limits_are_documented_and_referenced(self) -> None:
        source_limits_path = ROOT / "docs" / "SOURCE_LIMITS.md"
        self.assertTrue(source_limits_path.is_file())
        source_limits = read_text(source_limits_path)
        required_policy_phrases = [
            "source access level",
            "Do not invent citations",
            "Separate verified facts, interpretation, speculation, and recommendation",
        ]
        self.assertEqual(missing_phrases(source_limits, required_policy_phrases), [])

        missing_references = [
            skill_dir.name
            for skill_dir in self.skill_dirs()
            if "docs/SOURCE_LIMITS.md" not in skill_markdown(skill_dir)
        ]
        self.assertEqual(missing_references, [])

    def test_shared_auto_selection_guardrails_are_documented_and_referenced(self) -> None:
        guardrails_path = ROOT / "docs" / "AUTO_SELECTION_GUARDRAILS.md"
        self.assertTrue(guardrails_path.is_file())
        guardrails = read_text(guardrails_path)
        required_policy_phrases = [
            "High-signal triggers",
            "Light-route behavior",
            "Deep-work gate",
            "Noise and slowdown guard",
        ]
        self.assertEqual(missing_phrases(guardrails, required_policy_phrases), [])

        missing_references = [
            skill_dir.name
            for skill_dir in self.skill_dirs()
            if "docs/AUTO_SELECTION_GUARDRAILS.md" not in skill_markdown(skill_dir)
        ]
        self.assertEqual(missing_references, [])

    def test_each_skill_documents_next_step_routing(self) -> None:
        missing: list[str] = []
        for skill_dir in self.skill_dirs():
            readme = skill_readme(skill_dir)
            skill_text = skill_markdown(skill_dir)
            if "## Best next steps" not in readme and "## Suggested next step" not in skill_text:
                missing.append(skill_dir.name)
        self.assertEqual(missing, [])

    def test_shared_suggested_next_step_policy_is_documented(self) -> None:
        guardrails = read_text(ROOT / "docs" / "AUTO_SELECTION_GUARDRAILS.md")
        required_phrases = [
            "## Suggested next step policy",
            "optional, risk-gated",
            "One suggested skill max",
            "named scholarly risk",
            "Do not suggest `citation-integrity-auditor` before citations, quotes, page numbers, bibliography entries, or cited claims exist.",
            "Omit the section when it would add noise",
        ]
        self.assertEqual(missing_phrases(guardrails, required_phrases), [])

    def test_routing_matrix_documents_suggested_next_step_gates(self) -> None:
        routing_matrix = read_text(ROOT / "docs" / "ROUTING_MATRIX.md")
        required_phrases = [
            "## Suggested next step gates",
            "| Risk or prerequisite | Allowed next skill | Blocked early suggestion |",
            "High-level topic with unstable scope",
            "Cited draft, direct quotes, page numbers, bibliography entries, or cited claims",
            "No unresolved scholarly risk remains",
        ]
        self.assertEqual(missing_phrases(routing_matrix, required_phrases), [])

    def test_router_output_allows_optional_suggested_next_step(self) -> None:
        router = read_text(SKILLS_DIR / "research-intent-router" / "SKILL.md")
        output_section = router.split("## Output format", maxsplit=1)[1]
        self.assertIn("## Suggested next step", output_section)
        self.assertIn("optional", output_section)
        self.assertIn("docs/AUTO_SELECTION_GUARDRAILS.md", output_section)

    def test_suggested_next_step_wording_requires_named_risk(self) -> None:
        missing: list[str] = []
        required_phrases = [
            "optional Suggested next step policy",
            "named scholarly risk",
            "may be omitted",
        ]
        for skill_dir in self.skill_dirs():
            text = skill_markdown(skill_dir)
            if "## Suggested next step" in text:
                missing.extend(missing_labeled_phrases(skill_dir.name, text, required_phrases))
        self.assertEqual(missing, [])

    def test_suggested_next_step_template_lives_only_in_shared_policy(self) -> None:
        policy = read_text(ROOT / "docs" / "AUTO_SELECTION_GUARDRAILS.md")
        self.assertEqual(missing_phrases(policy, SUGGESTED_NEXT_STEP_TEMPLATE_PHRASES), [])

        duplicated_templates = [
            str(path.relative_to(ROOT))
            for path in SKILLS_DIR.glob("*/SKILL.md")
            if any(phrase in read_text(path) for phrase in SUGGESTED_NEXT_STEP_TEMPLATE_PHRASES)
        ]
        self.assertEqual(duplicated_templates, [])

    def test_skill_markdowns_do_not_duplicate_shared_source_or_followup_policy(self) -> None:
        duplicated_policy_phrases = [
            "Use the package source-access policy if available (including, but not limited to,",
            "Use the optional Suggested next step policy if available (including, but not limited to,",
            "Suggested next step must reduce a named scholarly risk, not promote a skill because it exists.",
        ]
        offenders = [
            f"{path.relative_to(ROOT)}: {phrase}"
            for path in SKILLS_DIR.glob("*/SKILL.md")
            for phrase in duplicated_policy_phrases
            if phrase in read_text(path)
        ]
        self.assertEqual(offenders, [])

    def test_citation_audit_suggestion_is_blocked_before_cited_material_exists(self) -> None:
        files = [
            ROOT / "docs" / "AUTO_SELECTION_GUARDRAILS.md",
            ROOT / "docs" / "ROUTING_MATRIX.md",
            SKILLS_DIR / "research-intent-router" / "SKILL.md",
        ]
        required_phrase = (
            "Do not suggest `citation-integrity-auditor` before citations, quotes, page numbers, "
            "bibliography entries, or cited claims exist."
        )
        missing = [
            str(path.relative_to(ROOT))
            for path in files
            if required_phrase not in read_text(path)
        ]
        self.assertEqual(missing, [])

    def test_no_generic_suggested_next_step_promotion_phrases(self) -> None:
        disallowed_phrases = [
            "you could also use",
            "consider using another skill",
            "Next best skill",
            "recommended next skill",
        ]
        offenders = [
            f"{path.relative_to(ROOT)}: {phrase}"
            for path, text in read_text_files()
            if path.suffix == ".md"
            for phrase in disallowed_phrases
            if phrase in text
        ]
        self.assertEqual(offenders, [])

    def test_suggested_next_step_policy_allows_omission(self) -> None:
        guardrails = read_text(ROOT / "docs" / "AUTO_SELECTION_GUARDRAILS.md")
        required_phrases = [
            "Omit the section when no specific unresolved scholarly risk remains.",
            "Omit the section when no one skill clearly reduces the remaining risk.",
            "Omit the section for grammar-only edits, casual answers, finished narrow tasks, or when the user asks to just answer.",
        ]
        self.assertEqual(missing_phrases(guardrails, required_phrases), [])

    def test_research_intent_router_documents_automatic_selection_rules(self) -> None:
        router_path = SKILLS_DIR / "research-intent-router" / "SKILL.md"
        self.assertTrue(router_path.is_file())
        router = read_text(router_path)
        required_phrases = [
            "auto-detect research intent",
            "light routing first",
            "Normal mode lookup gate",
            "user asks to find or check sources",
            "source existence or metadata is central",
            "citation, page, or quote verification is requested",
            "high-risk claim would otherwise be unsupported",
            "Do not trigger for pure fiction",
            "Do not trigger for grammar-only edits with no research claims",
            "## Per-skill routing rules",
        ]
        self.assertEqual(missing_phrases(router, required_phrases), [])

    def test_research_intent_router_documents_modes(self) -> None:
        router = read_text(SKILLS_DIR / "research-intent-router" / "SKILL.md")
        required_phrases = [
            "## Research modes",
            "Normal mode is the default",
            "| Mode | Default action | Lookup rule | Failure behavior |",
            "Normal mode lookup gate",
            "Deep mode lookup policy",
            "Deep mode always attempts deep lookup",
            "`research normal mode`",
            "`research deep mode`",
            "Mode persistence",
            "Mode persistence is conversation-scoped",
            "Restate the active mode in every output",
            "If the mode is ambiguous, use normal mode",
            "Deep mode does not override source limits",
            "If lookup tools, source access, or full text are unavailable, say so and mark the result unverified.",
        ]
        self.assertEqual(missing_phrases(router, required_phrases), [])

    def test_research_intent_router_bounds_deep_lookup(self) -> None:
        router = read_text(SKILLS_DIR / "research-intent-router" / "SKILL.md")
        required_phrases = [
            "## Deep lookup bounds",
            "Lookup order",
            "Candidate cap",
            "Depth cap",
            "Stop conditions",
            "max 12 candidate sources",
            "max two lookup passes",
        ]
        self.assertEqual(missing_phrases(router, required_phrases), [])

    def test_router_route_is_documented_as_non_contract_output(self) -> None:
        files = [
            ROOT / "docs" / "ARCHITECTURE.md",
            ROOT / "MODE_REGISTRY.md",
            ROOT / "skills" / "research-intent-router" / "SKILL.md",
        ]
        missing = [
            str(path.relative_to(ROOT))
            for path in files
            if "non-contract routing output" not in read_text(path)
        ]
        self.assertEqual(missing, [])

    def test_each_skill_documents_auto_selection_guardrails(self) -> None:
        missing: list[str] = []
        required_phrases = [
            "## Automatic selection guidance",
            "High-signal triggers",
            "Light-route behavior",
            "Deep-work gate",
            "Noise and slowdown guard",
        ]
        for skill_dir in self.skill_dirs():
            if skill_dir.name == "research-intent-router":
                continue
            text = skill_markdown(skill_dir)
            missing.extend(missing_labeled_phrases(skill_dir.name, text, required_phrases))
        self.assertEqual(missing, [])

    def test_lookup_capable_skills_allow_router_deep_mode(self) -> None:
        lookup_capable_skills = [
            "annotated-bibliography-builder",
            "book-proposal-scholarship",
            "citation-integrity-auditor",
            "counterargument-peer-review",
            "literature-review-mapper",
            "methodology-source-auditor",
            "systematic-source-discovery",
        ]
        missing = []
        for skill_name in lookup_capable_skills:
            text = read_text(SKILLS_DIR / skill_name / "SKILL.md")
            if "router deep mode" not in text:
                missing.append(skill_name)
        self.assertEqual(missing, [])

    def test_router_deep_mode_policy_pairs_attempt_with_limits(self) -> None:
        router = read_text(SKILLS_DIR / "research-intent-router" / "SKILL.md")
        deep_mode_position = router.find("Deep mode lookup policy:")
        source_limit_position = router.find("Deep mode does not override source limits")
        bounds_position = router.find("## Deep lookup bounds")
        self.assertGreaterEqual(deep_mode_position, 0)
        self.assertGreaterEqual(source_limit_position, 0)
        self.assertGreaterEqual(bounds_position, 0)
        self.assertLess(source_limit_position, deep_mode_position)
        self.assertLess(deep_mode_position, bounds_position)
        self.assertIn("never treat failed or unavailable lookup as verified evidence", router)

    def test_router_output_requires_mode_and_verification_limits(self) -> None:
        router = read_text(SKILLS_DIR / "research-intent-router" / "SKILL.md")
        output_section = router.split("## Output format", maxsplit=1)[1]
        self.assertIn("## Research mode", output_section)
        self.assertIn("## What I can verify", output_section)
        self.assertIn("## What remains uncertain", output_section)
        self.assertIn("## User verification needed", output_section)

    def test_router_is_registered_in_user_facing_docs(self) -> None:
        files = [
            ROOT / "docs" / "SKILL_INDEX.md",
            ROOT / "MODE_REGISTRY.md",
            ROOT / "docs" / "ARCHITECTURE.md",
            ROOT / "docs" / "WORKFLOW_PLAYBOOK.md",
        ]
        missing = [
            str(path.relative_to(ROOT))
            for path in files
            if "research-intent-router" not in read_text(path)
        ]
        self.assertEqual(missing, [])

    def test_routing_matrix_is_canonical_and_referenced(self) -> None:
        routing_matrix_path = ROOT / "docs" / "ROUTING_MATRIX.md"
        self.assertTrue(routing_matrix_path.is_file())
        routing_matrix = read_text(routing_matrix_path)
        required_routes = [
            "research-book-orchestrator",
            "scholarly-research-agenda",
            "systematic-source-discovery",
            "citation-integrity-auditor",
            "book-proposal-scholarship",
        ]
        self.assertEqual(missing_phrases(routing_matrix, required_routes), [])

        files = [
            ROOT / "skills" / "research-intent-router" / "SKILL.md",
            ROOT / "docs" / "SKILL_INDEX.md",
            ROOT / "MODE_REGISTRY.md",
        ]
        missing_references = [
            str(path.relative_to(ROOT))
            for path in files
            if "docs/ROUTING_MATRIX.md" not in read_text(path)
        ]
        self.assertEqual(missing_references, [])

    def test_skill_index_and_routing_matrix_cover_all_skills(self) -> None:
        skill_names = [skill_dir.name for skill_dir in self.skill_dirs()]
        skill_index = read_text(ROOT / "docs" / "SKILL_INDEX.md")
        routing_matrix = read_text(ROOT / "docs" / "ROUTING_MATRIX.md")

        missing = [
            f"docs/SKILL_INDEX.md: {skill_name}"
            for skill_name in skill_names
            if f"`{skill_name}`" not in skill_index
        ]
        missing.extend(
            f"docs/ROUTING_MATRIX.md: {skill_name}"
            for skill_name in skill_names
            if f"`{skill_name}`" not in routing_matrix
        )
        self.assertEqual(missing, [])

    def test_contract_schema_conditionals_require_discriminating_properties(self) -> None:
        schema = read_json(ROOT / "shared" / "contracts" / "book" / "book_artifact.schema.json")
        missing: list[str] = []
        for conditional in schema_conditionals(schema):
            condition = conditional["if"]
            required = condition.get("required")
            required = required if isinstance(required, list) else []
            for key in const_condition_keys(condition):
                if key not in required:
                    missing.append(key)
        self.assertEqual(missing, [])

    def test_contract_artifacts_require_provenance_fields(self) -> None:
        schema = read_json(ROOT / "shared" / "contracts" / "book" / "book_artifact.schema.json")
        required = schema.get("required")
        required = required if isinstance(required, list) else []
        properties = schema.get("properties")
        properties = properties if isinstance(properties, dict) else {}
        missing = [
            field
            for field in PROVENANCE_FIELDS
            if field not in required or field not in properties
        ]
        self.assertEqual(missing, [])

        examples_missing = [
            f"{path.name}: {field}"
            for path in sorted((ROOT / "examples" / "book_artifacts").glob("*.json"))
            for field in PROVENANCE_FIELDS
            if field not in read_json(path)
        ]
        self.assertEqual(examples_missing, [])

    def test_markdown_asset_templates_include_provenance_block(self) -> None:
        missing = [
            f"{path.relative_to(ROOT)}: {heading}"
            for path in sorted(SKILLS_DIR.glob("*/assets/*.md"))
            for heading in [
                "## Source basis",
                "## What I can verify",
                "## What remains uncertain",
                "## User verification needed",
            ]
            if heading not in read_text(path)
        ]
        self.assertEqual(missing, [])

    def test_contract_skills_document_machine_readable_artifact_mode(self) -> None:
        missing: list[str] = []
        for skill_name, artifact_type in CONTRACT_ARTIFACT_SKILLS.items():
            text = read_text(SKILLS_DIR / skill_name / "SKILL.md")
            missing.extend(missing_labeled_phrases(
                skill_name,
                text,
                [
                    "## Machine-readable artifacts",
                    "shared/contracts/book/book_artifact.schema.json",
                    f"`artifact_type: {artifact_type}`",
                ],
            ))
        self.assertEqual(missing, [])

    def test_public_readme_defers_route_tables_to_canonical_docs(self) -> None:
        readme = read_text(ROOT / "README.md")
        self.assertNotIn("| Mode | Primary skill |", readme)
        self.assertNotIn("## Recommended paths", readme)
        self.assertIn("docs/SKILL_INDEX.md", readme)
        self.assertIn("docs/ROUTING_MATRIX.md", readme)

    def test_manifest_version_matches_public_docs(self) -> None:
        manifest = read_json(ROOT / ".codex-plugin" / "plugin.json")
        version = manifest["version"]
        readme = read_text(ROOT / "README.md")
        changelog = read_text(ROOT / "CHANGELOG.md")

        self.assertIn(f"Version: {version}", readme)
        self.assertIn(f"## {version}", changelog)

    def test_skill_readmes_use_risk_gated_followup_language(self) -> None:
        disallowed_phrases = [
            "next best skill",
            "next best skill or repair step",
        ]
        offenders = [
            f"{path.relative_to(ROOT)}: {phrase}"
            for path in SKILLS_DIR.glob("*/README.md")
            for phrase in disallowed_phrases
            if phrase in read_text(path)
        ]
        self.assertEqual(offenders, [])

    def test_router_modes_are_registered_in_user_facing_docs(self) -> None:
        files = [
            ROOT / "README.md",
            ROOT / "docs" / "SKILL_INDEX.md",
            ROOT / "MODE_REGISTRY.md",
            ROOT / "docs" / "WORKFLOW_PLAYBOOK.md",
        ]
        required_phrases = [
            "research-route-normal",
            "research-route-deep",
        ]
        missing = [
            missing
            for path in files
            for missing in missing_labeled_phrases(
                str(path.relative_to(ROOT)),
                read_text(path),
                required_phrases,
            )
        ]
        self.assertEqual(missing, [])

    def test_public_docs_defer_mode_details_to_mode_registry(self) -> None:
        public_docs = [
            ROOT / "README.md",
            ROOT / "docs" / "SKILL_INDEX.md",
            ROOT / "docs" / "WORKFLOW_PLAYBOOK.md",
        ]
        missing_registry_reference = [
            str(path.relative_to(ROOT))
            for path in public_docs
            if "See `MODE_REGISTRY.md`" not in read_text(path)
        ]
        self.assertEqual(missing_registry_reference, [])

        repeated_details = [
            str(path.relative_to(ROOT))
            for path in public_docs
            if "Route first, then always attempt deep lookup" in read_text(path)
            or "Default plan-first routing" in read_text(path)
        ]
        self.assertEqual(repeated_details, [])

    def test_generic_research_route_is_documented_as_normal_alias(self) -> None:
        registry = read_text(ROOT / "MODE_REGISTRY.md")
        self.assertIn("`research-route` is an alias for `research-route-normal`", registry)

    def test_router_references_mode_registry_as_canonical_modes(self) -> None:
        router = read_text(SKILLS_DIR / "research-intent-router" / "SKILL.md")
        self.assertIn("MODE_REGISTRY.md is canonical for mode names and aliases", router)
        self.assertIn("MODE_REGISTRY.md", router)

    def test_readme_uses_router_when_next_skill_is_unclear(self) -> None:
        readme = read_text(ROOT / "README.md")
        self.assertIn("Use `research-intent-router` when the next skill is unclear", readme)

    def test_readme_install_summary_matches_installation_options(self) -> None:
        readme = read_text(ROOT / "README.md")
        self.assertNotIn("repo marketplace install", readme)

    def test_architecture_uses_compact_router_graph_edges(self) -> None:
        architecture = read_text(ROOT / "docs" / "ARCHITECTURE.md")
        self.assertLessEqual(architecture.count("Router -->"), 3)
        self.assertLessEqual(architecture.count("T -->"), 3)
        self.assertIn("Specialists", architecture)


if __name__ == "__main__":
    unittest.main()
