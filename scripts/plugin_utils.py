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
EXCLUDED_FILE_NAMES = {".DS_Store"}
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
CONTRACT_ARTIFACT_SKILLS = {
    "scholarly-research-agenda": "book_research_agenda",
    "systematic-source-discovery": "source_discovery_log",
    "annotation-to-source-note": "source_note",
    "extraction-table-builder": "extraction_table",
    "literature-review-mapper": "literature_map",
    "argument-architecture": "thesis_tree",
    "chapter-architecture": "chapter_brief",
    "claim-evidence-ledger": "claim_evidence_ledger",
    "claim-traceability-graph": "claim_traceability_graph",
    "citation-integrity-auditor": "citation_integrity_audit",
    "rights-privacy-release-auditor": "rights_privacy_release_audit",
    "book-comps-verifier": "comps_verification",
    "scholarly-integrity-gate": "scholarly_integrity_audit",
    "ai-human-workflow-log": "ai_human_workflow_log",
    "figure-table-integrity-auditor": "figure_table_integrity_audit",
    "manuscript-continuity-editor": "continuity_review",
    "book-proposal-scholarship": "book_proposal",
}


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
