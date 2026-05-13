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
SELECTED_COMPACT_OUTPUT_SKILLS = [
    "research-intent-router",
    "claim-evidence-ledger",
    "citation-integrity-auditor",
    "scholarly-integrity-gate",
    "rights-privacy-release-auditor",
    "figure-table-integrity-auditor",
    "book-comps-verifier",
    "methodology-source-auditor",
]
COMPACT_RESULT_USE_STATUSES = [
    "TRIAGE ONLY",
    "BLOCKER SUMMARY",
    "LIMITED GATE DECISION",
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


def markdown_table_rows_after_heading(markdown_text: str, heading: str) -> list[list[str]]:
    section_match = re.search(
        rf"^{re.escape(heading)}\n\n(?P<table>(?:\|.*\|\n)+)",
        markdown_text,
        re.MULTILINE,
    )
    if not section_match:
        return []

    rows = []
    for row in section_match.group("table").strip().splitlines()[2:]:
        rows.append([cell.strip() for cell in row.strip("|").split("|")])
    return rows


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

    def test_compact_output_does_not_use_old_mode_name(self) -> None:
        stale_references = [
            str(path.relative_to(ROOT))
            for path, text in read_text_files()
            if "compact mode" in text or "Compact mode" in text
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

    def test_skill_readme_template_defers_common_operational_boundaries(self) -> None:
        template = read_text(ROOT / "docs" / "SKILL_README_TEMPLATE.md")
        self.assertIn("docs/SKILL_OPERATIONAL_BOUNDARIES.md", template)
        duplicated_phrases = [
            "State the source basis and source access level",
            "Bundled skill instructions, metadata, and assets if available",
            "Invent missing scholarly facts or verification",
        ]
        offenders = [phrase for phrase in duplicated_phrases if phrase in template]
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

    def test_output_templates_do_not_force_suggested_next_step_heading(self) -> None:
        offenders = {}
        for skill_dir in self.skill_dirs():
            templates = re.findall(r"```markdown\n(.*?)\n```", skill_markdown(skill_dir), re.DOTALL)
            forced_templates = [
                template_index
                for template_index, template in enumerate(templates, start=1)
                if "## Suggested next step" in template
            ]
            if forced_templates:
                offenders[skill_dir.name] = forced_templates
        self.assertEqual(offenders, {})

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
            "separate source basis from interpretation",
            "it may be omitted unless one skill reduces",
            "it may be omitted unless one specialist skill reduces",
            "Bundled skill instructions, metadata, and assets if available",
        ]
        offenders = [
            f"{path.relative_to(ROOT)}: {phrase}"
            for path in SKILLS_DIR.glob("*/SKILL.md")
            for phrase in duplicated_policy_phrases
            if phrase in read_text(path)
        ]
        self.assertEqual(offenders, [])

    def test_skill_markdowns_reference_operational_boundary_doc_once(self) -> None:
        offenders = [
            str(path.relative_to(ROOT))
            for path in SKILLS_DIR.glob("*/SKILL.md")
            if read_text(path).count("docs/SKILL_OPERATIONAL_BOUNDARIES.md") > 1
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

    def test_skill_metadata_versions_match_manifest(self) -> None:
        manifest = read_json(ROOT / ".codex-plugin" / "plugin.json")
        version = manifest["version"]
        mismatches = [
            f"{skill_dir.name}: {metadata_field(skill_markdown(skill_dir), 'version')}"
            for skill_dir in self.skill_dirs()
            if metadata_field(skill_markdown(skill_dir), "version") != version
        ]
        self.assertEqual(mismatches, [])

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

    def test_integrity_gate_skill_and_routing_are_documented(self) -> None:
        skill_name = "scholarly-integrity-gate"
        skill_text = read_text(SKILLS_DIR / skill_name / "SKILL.md")
        required_skill_phrases = [
            "CLEAR",
            "SUSPECTED",
            "INSUFFICIENT EVIDENCE",
            "OVERRIDDEN",
            "implementation bug",
            "methodology fabrication",
            "shortcut reliance",
            "frame-lock",
            "human checkpoint",
        ]
        self.assertEqual(missing_phrases(skill_text, required_skill_phrases), [])

        required_docs = [
            ROOT / "docs" / "ARCHITECTURE.md",
            ROOT / "docs" / "ROUTING_MATRIX.md",
            ROOT / "docs" / "SKILL_INDEX.md",
            ROOT / "MODE_REGISTRY.md",
        ]
        missing = [
            str(path.relative_to(ROOT))
            for path in required_docs
            if skill_name not in read_text(path)
        ]
        self.assertEqual(missing, [])

    def test_ai_human_workflow_log_records_decisions_and_disclosures(self) -> None:
        skill_name = "ai-human-workflow-log"
        skill_text = read_text(SKILLS_DIR / skill_name / "SKILL.md")
        required_phrases = [
            "human decision",
            "override reason",
            "AI-use disclosure",
            "tool use",
            "affected sections",
            "human verification",
            "venue-specific disclosure",
        ]
        self.assertEqual(missing_phrases(skill_text, required_phrases), [])

        release_audit = read_text(SKILLS_DIR / "rights-privacy-release-auditor" / "SKILL.md")
        self.assertIn("ai-human-workflow-log", release_audit)
        self.assertIn("AI-use disclosure", release_audit)

    def test_citation_auditor_documents_metadata_verification_ladder(self) -> None:
        citation_audit = read_text(SKILLS_DIR / "citation-integrity-auditor" / "SKILL.md")
        required_phrases = [
            "metadata verification ladder",
            "DOI",
            "Crossref",
            "OpenAlex",
            "Semantic Scholar",
            "normalized title",
            "identifier hijack",
            "fuzzy title",
            "scripts/check_citation_metadata.py",
            "no-network",
            "--lookup-provider crossref",
            "--allow-network",
            "submits DOI identifiers only",
            "full_text",
            "abstract",
        ]
        self.assertEqual(missing_phrases(citation_audit, required_phrases), [])

    def test_source_discovery_supports_systematic_review_protocol_mode(self) -> None:
        source_discovery = read_text(SKILLS_DIR / "systematic-source-discovery" / "SKILL.md")
        search_guide = read_text(
            SKILLS_DIR / "systematic-source-discovery" / "references" / "search-strategy-guide.md"
        )
        required_phrases = [
            "systematic review mode",
            "review-type prefilter",
            "scoping review",
            "narrative review",
            "PRISMA",
            "protocol snapshot",
            "reviewer process",
            "appraisal plan",
            "risk of bias",
            "synthesis method",
            "certainty",
            "screening counts",
            "exclusion reasons",
        ]
        self.assertEqual(missing_phrases(source_discovery + search_guide, required_phrases), [])

    def test_source_discovery_contract_supports_systematic_review_fields(self) -> None:
        schema = read_json(ROOT / "shared" / "contracts" / "book" / "book_artifact.schema.json")
        properties = schema["properties"]
        definitions = schema["$defs"]
        required_definitions = [
            "systematic_review_record",
            "systematic_review_protocol_snapshot",
            "systematic_review_screening_counts",
            "systematic_review_exclusion_reason",
            "systematic_review_search_string",
        ]

        self.assertIn("systematic_review", properties)
        missing_definitions = [
            definition
            for definition in required_definitions
            if definition not in definitions
        ]
        self.assertEqual(missing_definitions, [])

        systematic_review = definitions["systematic_review_record"]
        required_fields = systematic_review["required"]
        for field in [
            "review_type",
            "protocol_snapshot",
            "reviewer_process",
            "appraisal_plan",
            "synthesis_method",
            "certainty_assessment",
            "screening_counts",
            "exclusion_reasons",
            "prisma_flow",
            "exact_search_strings",
        ]:
            self.assertIn(field, required_fields)

    def test_artifact_contract_covers_audit_and_workflow_artifacts(self) -> None:
        schema = read_json(ROOT / "shared" / "contracts" / "book" / "book_artifact.schema.json")
        artifact_types = schema["properties"]["artifact_type"]["enum"]
        required_artifact_types = [
            "source_note",
            "extraction_table",
            "claim_traceability_graph",
            "citation_integrity_audit",
            "rights_privacy_release_audit",
            "comps_verification",
            "scholarly_integrity_audit",
            "ai_human_workflow_log",
            "figure_table_integrity_audit",
        ]
        missing = [artifact_type for artifact_type in required_artifact_types if artifact_type not in artifact_types]
        self.assertEqual(missing, [])

    def test_artifact_contract_covers_high_value_support_handoff_artifacts(self) -> None:
        schema = read_json(ROOT / "shared" / "contracts" / "book" / "book_artifact.schema.json")
        artifact_types = schema["properties"]["artifact_type"]["enum"]
        required_artifact_types = [
            "methodology_source_audit",
            "annotated_bibliography",
            "case_study_dossier",
            "peer_review_report",
            "style_sheet",
        ]
        missing = [artifact_type for artifact_type in required_artifact_types if artifact_type not in artifact_types]
        self.assertEqual(missing, [])

        for artifact_type in required_artifact_types:
            with self.subTest(artifact_type=artifact_type):
                self.assertIn(artifact_type, CONTRACT_ARTIFACT_SKILLS.values())

    def test_mode_registry_artifact_table_matches_contract_mapping(self) -> None:
        registry = read_text(ROOT / "MODE_REGISTRY.md")
        artifact_rows = markdown_table_rows_after_heading(registry, "## Artifact types")
        registry_artifact_types = {
            row[0].strip("`")
            for row in artifact_rows
            if len(row) >= 2
        }
        expected_artifact_types = set(CONTRACT_ARTIFACT_SKILLS.values())
        self.assertEqual(registry_artifact_types, expected_artifact_types)

    def test_artifact_contract_supports_optional_process_passport(self) -> None:
        schema = read_json(ROOT / "shared" / "contracts" / "book" / "book_artifact.schema.json")
        self.assertIn("process_passport", schema["properties"])
        self.assertNotIn("process_passport", schema["required"])
        for path in [
            ROOT / "docs" / "QUALITY_STANDARD.md",
            ROOT / "docs" / "SCRIPTS.md",
        ]:
            text = read_text(path)
            self.assertNotIn("requires `process_passport`", text)
            self.assertNotIn("requires process_passport", text)

        passport = schema["$defs"]["process_passport"]
        required_fields = passport["required"]
        for field in [
            "stage",
            "artifact_inputs",
            "tool_use_summary",
            "gate_status",
            "human_checkpoints",
            "handoff_notes",
        ]:
            self.assertIn(field, required_fields)

    def test_contract_uses_controlled_status_vocabularies(self) -> None:
        schema = read_json(ROOT / "shared" / "contracts" / "book" / "book_artifact.schema.json")
        defs = schema.get("$defs", {})
        required_defs = [
            "claim_type",
            "evidence_status",
            "verification_status",
            "locator_status",
            "risk_level",
            "confidence_level",
            "integrity_verdict",
        ]
        missing_defs = [definition for definition in required_defs if definition not in defs]
        self.assertEqual(missing_defs, [])

        claim_row = defs["claim_evidence_row"]["properties"]
        self.assertEqual(claim_row["claim_type"]["$ref"], "#/$defs/claim_type")
        self.assertEqual(claim_row["evidence_status"]["$ref"], "#/$defs/evidence_status")
        self.assertEqual(claim_row["risk"]["$ref"], "#/$defs/risk_level")
        self.assertEqual(claim_row["confidence"]["$ref"], "#/$defs/confidence_level")

    def test_empirical_provenance_and_figure_table_integrity_are_documented(self) -> None:
        claim_ledger = read_text(SKILLS_DIR / "claim-evidence-ledger" / "SKILL.md")
        figure_audit = read_text(SKILLS_DIR / "figure-table-integrity-auditor" / "SKILL.md")
        required_phrases = [
            "analysis provenance",
            "dataset",
            "script or notebook",
            "run log",
            "caption",
            "axis",
            "duplicate visual",
            "data provenance",
        ]
        self.assertEqual(missing_phrases(claim_ledger + figure_audit, required_phrases), [])

    def test_methodology_auditor_has_method_family_references(self) -> None:
        methodology = read_text(SKILLS_DIR / "methodology-source-auditor" / "SKILL.md")
        required_phrases = [
            "method-family references",
            "qualitative",
            "historical",
            "legal",
            "computational",
            "survey",
            "observational",
            "experimental",
            "systematic review",
        ]
        self.assertEqual(missing_phrases(methodology, required_phrases), [])

    def test_methodology_auditor_reference_files_exist(self) -> None:
        references_dir = SKILLS_DIR / "methodology-source-auditor" / "references"
        expected_files = [
            "qualitative.md",
            "historical.md",
            "legal.md",
            "computational.md",
            "survey.md",
            "observational.md",
            "experimental.md",
            "systematic-review.md",
        ]
        missing_files = [
            filename
            for filename in expected_files
            if not (references_dir / filename).is_file()
        ]
        self.assertEqual(missing_files, [])

        missing_phrases_by_file = {
            filename: missing_phrases(
                read_text(references_dir / filename),
                ["## Audit questions", "## Boundaries", "## Cannot support"],
            )
            for filename in expected_files
            if (references_dir / filename).is_file()
        }
        self.assertEqual(
            {
                filename: phrases
                for filename, phrases in missing_phrases_by_file.items()
                if phrases
            },
            {},
        )

    def test_integrity_gate_has_stage_prefilters_and_block_rules(self) -> None:
        integrity_gate = read_text(SKILLS_DIR / "scholarly-integrity-gate" / "SKILL.md")
        required_phrases = [
            "artifact/method prefilter",
            "not applicable",
            "Stage-specific block rules",
            "result-bearing artifact",
            "must hold",
            "must not block",
            "theoretical, interpretive, or normative",
        ]
        self.assertEqual(missing_phrases(integrity_gate, required_phrases), [])

    def test_router_deep_mode_requires_lookup_target_object(self) -> None:
        router = read_text(SKILLS_DIR / "research-intent-router" / "SKILL.md")
        required_phrases = [
            "lookup target object",
            "verification need",
            "source type",
            "stop condition",
            "do not run open-ended deep lookup",
        ]
        self.assertEqual(missing_phrases(router, required_phrases), [])

    def test_accessibility_skills_support_compact_output(self) -> None:
        accessibility_skills = [
            "dictation-to-research-notes",
            "dyslexia-friendly-prose-editor",
            "dyslexia-research-companion",
            "reading-load-reducer",
        ]
        required_phrases = [
            "compact output",
            "short chunks",
            "stable table labels",
            "Source basis: [one line]",
            "only if",
            "Next action",
        ]
        per_skill_required_phrases = {
            "reading-load-reducer": ["Access level", "Skip/park risk"],
        }
        missing = {}
        for skill_name in accessibility_skills:
            skill_text = read_text(SKILLS_DIR / skill_name / "SKILL.md")
            skill_required_phrases = required_phrases + per_skill_required_phrases.get(skill_name, [])
            missing_for_skill = missing_phrases(skill_text, skill_required_phrases)
            if missing_for_skill:
                missing[skill_name] = missing_for_skill
        self.assertEqual(missing, {})

    def test_accessibility_agent_metadata_preserves_discoverability_terms(self) -> None:
        required_aliases = {
            "dyslexia-research-companion": ["dyslexic", "dysorthographic"],
            "dyslexia-friendly-prose-editor": ["dyslexic", "dysorthographic"],
        }
        missing = {}
        for skill_name, aliases in required_aliases.items():
            metadata_text = read_text(SKILLS_DIR / skill_name / "agents" / "openai.yaml")
            short_description = metadata_field(metadata_text, "short_description").lower()
            missing_aliases = [
                alias
                for alias in aliases
                if alias not in short_description
            ]
            if missing_aliases:
                missing[skill_name] = missing_aliases
        self.assertEqual(missing, {})

    def test_selected_routing_and_audit_skills_support_compact_output(self) -> None:
        required_phrases = [
            "## Compact output",
            "Compact output:",
            "Source basis: [one line]",
            "Next action",
        ]
        per_skill_required_phrases = {
            "book-comps-verifier": ["Verification needed", "Fit or mismatch"],
            "citation-integrity-auditor": ["Verification status", "Severity", "Required fix"],
            "claim-evidence-ledger": ["Evidence status", "Risk"],
            "figure-table-integrity-auditor": ["Blocker or gap", "Required repair", "Needed files"],
            "methodology-source-auditor": ["Method/evidence visible", "Can support", "Cannot support"],
            "research-intent-router": ["Best route", "Lookup needed?", "Still unverified"],
            "rights-privacy-release-auditor": ["Legal/permission uncertainty", "Release verdict"],
            "scholarly-integrity-gate": ["Gate decision", "Human checkpoint", "Verdict"],
        }
        missing = {}
        for skill_name in SELECTED_COMPACT_OUTPUT_SKILLS:
            skill_text = read_text(SKILLS_DIR / skill_name / "SKILL.md")
            readme_text = read_text(SKILLS_DIR / skill_name / "README.md")
            skill_required_phrases = required_phrases + per_skill_required_phrases.get(skill_name, [])
            missing_for_skill = missing_phrases(skill_text, skill_required_phrases)
            missing_for_readme = missing_phrases(readme_text, ["compact output"])
            if missing_for_skill or missing_for_readme:
                missing[skill_name] = {
                    "skill": missing_for_skill,
                    "readme": missing_for_readme,
                }
        self.assertEqual(missing, {})

    def test_skill_index_lists_selected_compact_output_skills(self) -> None:
        skill_index = read_text(ROOT / "docs" / "SKILL_INDEX.md")
        compact_section = skill_index.split("## Compact output support", 1)[1].split("## Core research workflow", 1)[0]
        documented_skills = re.findall(r"^- `([^`]+)`", compact_section, re.MULTILINE)
        self.assertEqual(documented_skills, SELECTED_COMPACT_OUTPUT_SKILLS)

    def test_compact_output_readmes_describe_output_shape(self) -> None:
        missing = {}
        for skill_dir in self.skill_dirs():
            skill_text = skill_markdown(skill_dir)
            if "## Compact output" not in skill_text:
                continue
            readme_text = skill_readme(skill_dir)
            missing_for_readme = missing_phrases(readme_text, ["output shape", "How to use this result"])
            if missing_for_readme:
                missing[skill_dir.name] = missing_for_readme
        self.assertEqual(missing, {})

    def test_compact_output_templates_use_one_global_next_action(self) -> None:
        violations = {}
        for skill_dir in self.skill_dirs():
            skill_text = skill_markdown(skill_dir)
            compact_templates = re.findall(r"Compact output:\n\n```markdown\n(.*?)\n```", skill_text, re.DOTALL)
            for template_index, compact_template in enumerate(compact_templates, start=1):
                table_next_action_lines = [
                    line
                    for line in compact_template.splitlines()
                    if line.startswith("|") and "Next action" in line
                ]
                global_next_action_count = compact_template.count("Next action:")
                optional_next_action_lines = [
                    line
                    for line in compact_template.splitlines()
                    if line.startswith("Next action:") and "only if" in line
                ]
                if table_next_action_lines or global_next_action_count != 1:
                    violations[f"{skill_dir.name}#{template_index}"] = {
                        "table_next_action_lines": table_next_action_lines,
                        "global_next_action_count": global_next_action_count,
                    }
                elif optional_next_action_lines:
                    violations[f"{skill_dir.name}#{template_index}"] = {
                        "optional_next_action_lines": optional_next_action_lines,
                    }
        self.assertEqual(violations, {})

    def test_compact_output_templates_state_result_use(self) -> None:
        violations = {}
        allowed_statuses = "|".join(re.escape(status) for status in COMPACT_RESULT_USE_STATUSES)
        result_use_pattern = re.compile(
            rf"^How to use this result: ({allowed_statuses}) - [A-Z][^.?!]+[.?!]$",
            re.MULTILINE,
        )
        for skill_dir in self.skill_dirs():
            skill_text = skill_markdown(skill_dir)
            compact_templates = re.findall(r"Compact output:\n\n```markdown\n(.*?)\n```", skill_text, re.DOTALL)
            for template_index, compact_template in enumerate(compact_templates, start=1):
                matches = result_use_pattern.findall(compact_template)
                if len(matches) != 1:
                    violations[f"{skill_dir.name}#{template_index}"] = matches
        self.assertEqual(violations, {})

    def test_compact_output_docs_define_result_use_and_escalation(self) -> None:
        docs = {
            ROOT / "README.md": [
                "How to use this result",
                "Use this only to choose the next step; do not treat it as verified scholarship.",
                "This lists visible blockers only; no blocker listed does not mean the work is cleared.",
                "This is a proceed/hold/repair decision based only on visible evidence and stated limits.",
                "These statuses appear only in compact output.",
                "Escalate from compact output to full review",
            ],
            ROOT / "docs" / "QUALITY_STANDARD.md": [
                "How to use this result",
                "compact-output-only",
                "TRIAGE ONLY",
                "BLOCKER SUMMARY",
                "LIMITED GATE DECISION",
                "Escalate from compact output to full review",
            ],
            ROOT / "docs" / "SKILL_INDEX.md": [
                "How to use this result",
                "compact-output-only",
                "TRIAGE ONLY",
                "BLOCKER SUMMARY",
                "LIMITED GATE DECISION",
            ],
            ROOT / "docs" / "SKILL_OPERATIONAL_BOUNDARIES.md": [
                "How to use this result",
                "TRIAGE ONLY",
                "BLOCKER SUMMARY",
                "LIMITED GATE DECISION",
                "Escalate from compact output to full review",
            ],
            ROOT / "docs" / "WORKFLOW_PLAYBOOK.md": [
                "How to use this result",
                "Use these statuses only for compact output",
                "Escalate from compact output to full review",
            ],
        }
        missing = [
            f"{path.relative_to(ROOT)}: {phrase}"
            for path, required_phrases in docs.items()
            for phrase in missing_phrases(read_text(path), required_phrases)
        ]
        self.assertEqual(missing, [])

    def test_source_limits_document_external_tool_confidentiality_boundary(self) -> None:
        source_limits = read_text(ROOT / "docs" / "SOURCE_LIMITS.md")
        required_phrases = [
            "external tool boundary",
            "unpublished manuscript",
            "user consent",
            "search terms",
            "sensitive material",
        ]
        self.assertEqual(missing_phrases(source_limits, required_phrases), [])

    def test_behavior_eval_fixtures_cover_high_risk_skill_boundaries(self) -> None:
        fixture_path = ROOT / "examples" / "evals" / "research-skill-behavior-fixtures.json"
        fixtures = read_json(fixture_path)
        self.assertIsInstance(fixtures.get("fixtures"), list)
        self.assertGreaterEqual(len(fixtures["fixtures"]), 8)

        required_keys = {
            "id",
            "prompt",
            "expected_route",
            "risk_covered",
            "required_output_markers",
            "forbidden_claims",
        }
        missing_keys = [
            f"{fixture.get('id', '<missing id>')}: {key}"
            for fixture in fixtures["fixtures"]
            for key in required_keys
            if key not in fixture
        ]
        self.assertEqual(missing_keys, [])

        compact_fixture_missing_result_use = [
            fixture["id"]
            for fixture in fixtures["fixtures"]
            if (
                str(fixture["risk_covered"]).startswith("compact ")
                or fixture["risk_covered"] == "accessibility overload"
            )
            and "How to use this result" not in fixture["required_output_markers"]
        ]
        self.assertEqual(compact_fixture_missing_result_use, [])

        required_risks = {
            "premature citation audit",
            "hallucinated citation metadata",
            "open-ended deep lookup",
            "systematic review provenance",
            "AI-use disclosure",
            "figure table provenance",
            "accessibility overload",
            "external tool confidentiality",
            "compact citation blockers",
            "compact methodology triage",
            "compact release blockers",
            "compact routing",
            "integrity gate block rule",
            "irrelevant integrity check",
            "method family audit",
            "metadata lookup consent",
        }
        covered_risks = {fixture["risk_covered"] for fixture in fixtures["fixtures"]}
        self.assertEqual(sorted(required_risks - covered_risks), [])


if __name__ == "__main__":
    unittest.main()
