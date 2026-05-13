"""Shared helpers for plugin maintenance scripts."""
from __future__ import annotations

import json
import re
import shutil
from json import JSONDecodeError
from pathlib import Path
from typing import Any

ALLOWED_PACKAGE_DIRECTORIES = {
    ".codex-plugin",
    "assets",
    "docs",
    "examples",
    "scripts",
    "shared",
    "skills",
}
ALLOWED_PACKAGE_ROOT_FILES = {
    ".gitignore",
    "AGENTS.md",
    "CHANGELOG.md",
    "LICENSE",
    "MODE_REGISTRY.md",
    "README.md",
    "install.ps1",
    "install.sh",
    "marketplace.sample.json",
    "validate.sh",
}
EXCLUDED_DIRECTORIES = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "htmlcov",
    "node_modules",
    "venv",
}
EXCLUDED_FILE_NAMES = {".DS_Store", ".env", "local-notes.txt", "secrets.json"}
EXCLUDED_SUFFIXES = {".log", ".pyc", ".zip", ".tmp"}
DESCRIPTION_STOPWORDS = {
    "after",
    "before",
    "books",
    "book",
    "from",
    "grade",
    "needs",
    "need",
    "nonfiction",
    "research",
    "scholarly",
    "skill",
    "source",
    "sources",
    "that",
    "this",
    "when",
    "while",
    "with",
}
MIN_SHARED_DESCRIPTION_TERMS = 8
REQUIRED_AGENT_POLICY = {
    "task_type": "research-book-skill",
    "data_access_level": "user-provided-or-public-metadata",
    "external_lookup_allowed": "conditional",
    "confidentiality_gate": "required-before-external-lookup",
}
CONTRACT_ARTIFACT_SKILLS = {
    "scholarly-research-agenda": "book_research_agenda",
    "systematic-source-discovery": "source_discovery_log",
    "annotation-to-source-note": "source_note",
    "extraction-table-builder": "extraction_table",
    "annotated-bibliography-builder": "annotated_bibliography",
    "methodology-source-auditor": "methodology_source_audit",
    "literature-review-mapper": "literature_map",
    "argument-architecture": "thesis_tree",
    "counterargument-peer-review": "peer_review_report",
    "chapter-architecture": "chapter_brief",
    "claim-evidence-ledger": "claim_evidence_ledger",
    "claim-traceability-graph": "claim_traceability_graph",
    "citation-integrity-auditor": "citation_integrity_audit",
    "rights-privacy-release-auditor": "rights_privacy_release_audit",
    "book-comps-verifier": "comps_verification",
    "scholarly-integrity-gate": "scholarly_integrity_audit",
    "ai-human-workflow-log": "ai_human_workflow_log",
    "figure-table-integrity-auditor": "figure_table_integrity_audit",
    "case-study-integration": "case_study_dossier",
    "manuscript-continuity-editor": "continuity_review",
    "scholarly-prose-editor": "style_sheet",
    "book-proposal-scholarship": "book_proposal",
}
COMMON_ARTIFACT_FIELDS = {
    "schema_version",
    "artifact_type",
    "project_title",
    "created_at",
    "source_basis",
    "what_i_can_verify",
    "what_remains_uncertain",
    "user_verification_needed",
    "process_passport",
}
ARTIFACT_TYPE_FIELDS = {
    "book_research_agenda": {
        "central_research_question",
        "subquestions",
        "provisional_thesis",
        "contribution_claim",
        "scope_boundaries",
        "evidence_plan",
        "risks_and_mitigation",
    },
    "source_discovery_log": {
        "search_families",
        "query_bank",
        "priority_venues",
        "inclusion_criteria",
        "exclusion_criteria",
        "citation_chaining_plan",
        "source_targets",
        "opposing_literature_targets",
        "search_log",
        "systematic_review",
    },
    "literature_map": {
        "field_overview",
        "fields_and_subfields",
        "schools_of_thought",
        "major_debates",
        "consensus_controversy_map",
        "development_map",
        "gaps_in_literature",
        "thesis_implications",
        "sources_still_needed",
    },
    "thesis_tree": {
        "main_thesis",
        "thesis_variants",
        "thesis_claims",
        "hidden_assumptions",
        "chapter_argument_sequence",
        "weak_links",
    },
    "chapter_brief": {
        "chapter_title",
        "chapter_purpose",
        "central_question",
        "chapter_thesis",
        "key_concepts",
        "section_outline",
        "counterarguments_to_include",
        "opening_options",
        "ending_bridge",
        "research_still_needed",
        "revision_risks",
    },
    "claim_evidence_ledger": {
        "claims",
        "high_risk_claims",
        "analysis_provenance",
        "source_priorities",
    },
    "source_note": {"source_notes"},
    "extraction_table": {"extraction_rows"},
    "annotated_bibliography": {"bibliography_annotations"},
    "methodology_source_audit": {"source_audit_rows"},
    "claim_traceability_graph": {"traceability_links"},
    "peer_review_report": {
        "charitable_restatement",
        "review_objections",
        "rival_explanations",
        "missing_literatures",
        "claims_to_narrow",
        "revision_priorities",
    },
    "citation_integrity_audit": {"citation_audit_rows"},
    "rights_privacy_release_audit": {"release_issues"},
    "comps_verification": {"comps_verification_rows"},
    "scholarly_integrity_audit": {"integrity_checks"},
    "ai_human_workflow_log": {"workflow_decisions"},
    "figure_table_integrity_audit": {"figure_table_checks"},
    "case_study_dossier": {
        "claim_needing_case",
        "case_selection_logic",
        "case_dossiers",
        "counter_cases",
        "safer_case_claims",
    },
    "continuity_review": {
        "global_thesis",
        "chapter_function_map",
        "repetition_map",
        "concept_tracking",
        "contradictions_or_tensions",
        "tone_and_audience_consistency",
        "suggested_restructuring",
        "priority_revision_list",
    },
    "style_sheet": {
        "style_rules",
        "voice_constraints",
        "terms_to_preserve",
        "claim_language_guidance",
        "new_factual_claims_policy",
    },
    "book_proposal": {
        "title_options",
        "premise",
        "core_thesis",
        "contribution_to_field",
        "audience",
        "source_base",
        "chapter_summaries",
        "comparable_titles",
        "author_positioning",
        "status_and_timeline",
        "sample_material_plan",
    },
}


def agent_policy_yaml_lines(*, allow_implicit_invocation: bool = True) -> list[str]:
    return [
        "policy:",
        f"  allow_implicit_invocation: {str(allow_implicit_invocation).lower()}",
        *(f'  {field_name}: "{value}"' for field_name, value in REQUIRED_AGENT_POLICY.items()),
    ]


def load_json_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} root must be an object")
    return payload


def load_json_object_result(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        payload = load_json_object(path)
    except JSONDecodeError as exc:
        return None, f"{path}: malformed JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"
    except OSError as exc:
        return None, f"{path}: unable to read file: {exc}"
    except ValueError as exc:
        return None, str(exc)
    return payload, None


def plugin_manifest_path(root: Path) -> Path:
    return root / ".codex-plugin" / "plugin.json"


def load_plugin_manifest(root: Path) -> dict[str, Any]:
    return load_json_object(plugin_manifest_path(root))


def parse_simple_yaml_mapping(text: str) -> dict[str, Any]:
    data: dict[str, Any] = {}
    current_section = ""
    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        key, separator, value = raw_line.strip().partition(":")
        if not separator:
            continue
        parsed_value = parse_yaml_scalar(value.strip())
        if indent == 0:
            if value.strip():
                data[key] = parsed_value
                current_section = ""
            else:
                data[key] = {}
                current_section = key
            continue
        if indent == 2 and current_section and isinstance(data.get(current_section), dict):
            data[current_section][key] = parsed_value
    return data


def parse_markdown_frontmatter(text: str) -> dict[str, Any]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening YAML frontmatter delimiter")

    frontmatter_lines: list[str] = []
    for line in lines[1:]:
        if line.strip() == "---":
            return parse_simple_yaml_mapping("\n".join(frontmatter_lines))
        frontmatter_lines.append(line)
    raise ValueError("missing closing YAML frontmatter delimiter")


def parse_yaml_scalar(value: str) -> Any:
    if value in {"true", "false"}:
        return value == "true"
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    return value


def nested_mapping(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    return value if isinstance(value, dict) else {}


def nested_string(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    return value if isinstance(value, str) else ""


def significant_description_terms(description: str) -> set[str]:
    return {
        term
        for term in re.findall(r"[a-z0-9]+", description.lower())
        if len(term) >= 5 and term not in DESCRIPTION_STOPWORDS
    }


def plugin_name(root: Path) -> str:
    return str(load_plugin_manifest(root).get("name", ""))


def plugin_version(root: Path) -> str:
    return str(load_plugin_manifest(root).get("version", ""))


def generated_file_patterns() -> list[str]:
    return [
        *sorted(EXCLUDED_DIRECTORIES),
        *sorted(EXCLUDED_FILE_NAMES),
        *(f"*{suffix}" for suffix in sorted(EXCLUDED_SUFFIXES)),
    ]


def is_generated_path(relative_path: Path) -> bool:
    return (
        bool(EXCLUDED_DIRECTORIES.intersection(relative_path.parts))
        or relative_path.name in EXCLUDED_FILE_NAMES
        or relative_path.suffix in EXCLUDED_SUFFIXES
    )


def is_allowed_package_path(relative_path: Path) -> bool:
    if not relative_path.parts:
        return False
    if len(relative_path.parts) == 1:
        return relative_path.name in ALLOWED_PACKAGE_ROOT_FILES
    return relative_path.parts[0] in ALLOWED_PACKAGE_DIRECTORIES


def should_include_package_file(root: Path, path: Path) -> bool:
    if not path.is_file():
        return False
    relative_path = path.relative_to(root)
    return is_allowed_package_path(relative_path) and not is_generated_path(relative_path)


def package_files(root: Path) -> list[Path]:
    return [
        path
        for path in sorted(root.rglob("*"))
        if should_include_package_file(root, path)
    ]


def copy_package_tree(src: Path, dest: Path) -> None:
    for path in package_files(src):
        target_path = dest / path.relative_to(src)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target_path)
