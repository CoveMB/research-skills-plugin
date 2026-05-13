#!/usr/bin/env python3
"""Validate a local skills plugin package.

Checks:
- .codex-plugin/plugin.json exists and points to skills
- every skills/<name>/SKILL.md has valid frontmatter
- skill name matches folder name
- required name/description fields are present
- names satisfy Agent Skills naming constraints
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from plugin_utils import (
    load_json_object_result,
    MIN_SHARED_DESCRIPTION_TERMS,
    nested_mapping,
    nested_string,
    parse_simple_yaml_mapping,
    significant_description_terms,
)

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REQUIRED_AGENT_POLICY_STRINGS = {
    "task_type": "research-book-skill",
    "data_access_level": "user-provided-or-public-metadata",
    "external_lookup_allowed": "conditional",
    "confidentiality_gate": "required-before-external-lookup",
}
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)")
BACKTICK_REFERENCE_RE = re.compile(r"`([^`\n]+)`")
LOCAL_REFERENCE_PREFIXES = (
    ".codex-plugin/",
    "assets/",
    "docs/",
    "examples/",
    "references/",
    "scripts/",
    "shared/",
    "skills/",
)
LOCAL_REFERENCE_ROOT_FILES = {
    "AGENTS.md",
    "CHANGELOG.md",
    "LICENSE",
    "MODE_REGISTRY.md",
    "README.md",
    "marketplace.sample.json",
    "validate.sh",
}
REFERENCE_FILE_SUFFIXES = {".md", ".yaml", ".yml"}
def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening YAML frontmatter delimiter")
    data: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return data
        if not line.strip() or line.startswith("  "):
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip().strip('"').strip("'")
    raise ValueError("missing closing YAML frontmatter delimiter")


def is_external_reference(reference: str) -> bool:
    return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", reference))


def is_path_like_reference(reference: str) -> bool:
    if not reference or any(token in reference for token in [" ", "*", "<", ">", "|"]):
        return False
    if reference in {"assets/", "references/", "scripts/"}:
        return False
    if reference.startswith(("/", "~", "#")) or is_external_reference(reference):
        return False
    return (
        reference.startswith(("./", "../"))
        or reference.startswith(LOCAL_REFERENCE_PREFIXES)
        or reference in LOCAL_REFERENCE_ROOT_FILES
    )


def reference_candidates(root: Path, path: Path, reference: str) -> list[Path]:
    return [
        (path.parent / reference).resolve(),
        (root / reference).resolve(),
    ]


def reference_exists_inside_root(root: Path, candidates: list[Path]) -> tuple[bool, bool]:
    escaped = False
    for candidate in candidates:
        try:
            candidate.relative_to(root.resolve())
        except ValueError:
            escaped = True
            continue
        if candidate.exists():
            return True, False
    return False, escaped


def clean_reference(reference: str) -> str:
    return reference.strip().split("#", 1)[0]


def broken_local_references(root: Path, path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    references = [*MARKDOWN_LINK_RE.findall(text), *BACKTICK_REFERENCE_RE.findall(text)]
    for reference in references:
        normalized = clean_reference(reference)
        if not is_path_like_reference(normalized):
            continue
        exists, escaped = reference_exists_inside_root(
            root,
            reference_candidates(root, path, normalized),
        )
        if escaped:
            errors.append(f"{path.name}: local reference escapes plugin root: {normalized}")
            continue
        if not exists:
            errors.append(f"{path.name}: broken local reference: {normalized}")
    return errors


def string_values(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [item for child in value for item in string_values(child)]
    if isinstance(value, dict):
        return [item for child in value.values() for item in string_values(child)]
    return []


def broken_manifest_references(root: Path, manifest_path: Path, manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for reference in string_values(manifest):
        normalized = clean_reference(reference)
        if not is_path_like_reference(normalized):
            continue
        exists, escaped = reference_exists_inside_root(
            root,
            reference_candidates(root, manifest_path, normalized),
        )
        if escaped:
            errors.append(f"plugin.json: local reference escapes plugin root: {normalized}")
            continue
        if not exists:
            errors.append(f"plugin.json: broken local reference: {normalized}")
    return errors


def broken_yaml_references(root: Path, path: Path) -> list[str]:
    try:
        data = parse_simple_yaml_mapping(path.read_text(encoding="utf-8"))
    except Exception:
        return []
    errors: list[str] = []
    for reference in string_values(data):
        normalized = clean_reference(reference)
        if not is_path_like_reference(normalized):
            continue
        exists, escaped = reference_exists_inside_root(
            root,
            reference_candidates(root, path, normalized),
        )
        if escaped:
            errors.append(f"{path.name}: local reference escapes plugin root: {normalized}")
            continue
        if not exists:
            errors.append(f"{path.name}: broken local reference: {normalized}")
    return errors


def broken_reference_file_errors(root: Path, path: Path) -> list[str]:
    errors = broken_local_references(root, path)
    if path.suffix in {".yaml", ".yml"}:
        errors.extend(broken_yaml_references(root, path))
    return errors


def skill_reference_files(skill_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in skill_dir.rglob("*")
        if path.is_file() and path.suffix in REFERENCE_FILE_SUFFIXES
    )


def skill_name_terms(skill_name: str) -> set[str]:
    return significant_description_terms(skill_name.replace("-", " "))


def manifest_errors(root: Path) -> tuple[dict | None, Path, list[str]]:
    errors: list[str] = []
    manifest_path = root / ".codex-plugin" / "plugin.json"
    if not manifest_path.exists():
        return None, root / "skills", ["Missing .codex-plugin/plugin.json"]

    manifest, error = load_json_object_result(manifest_path)
    if error is not None:
        return None, root / "skills", [error]
    assert manifest is not None

    for field in ["name", "version", "description", "skills"]:
        if field not in manifest:
            errors.append(f"plugin.json missing required/recommended field: {field}")
    if not NAME_RE.match(str(manifest.get("name", ""))):
        errors.append("plugin.json name should be kebab-case lowercase")

    skills_value = manifest.get("skills", "skills")
    if not isinstance(skills_value, str) or not skills_value.strip():
        errors.append("plugin.json skills must be a non-empty relative path")
        return manifest, root / "skills", errors
    skills_path = Path(skills_value)
    if skills_path.is_absolute():
        errors.append("plugin.json skills must be a relative path")
        return manifest, root / "skills", errors

    skills_dir = (root / skills_path).resolve()
    try:
        skills_dir.relative_to(root)
    except ValueError:
        errors.append("plugin.json skills path must stay inside plugin root")
    if not skills_dir.exists():
        errors.append(f"plugin.json skills path does not exist: {skills_value}")
    errors.extend(broken_manifest_references(root, manifest_path, manifest))
    return manifest, skills_dir, errors


def validate_agent_metadata(
    skill_dir: Path,
    skill_name: str,
    skill_description: str,
) -> tuple[str, list[str]]:
    errors: list[str] = []
    agent_path = skill_dir / "agents" / "openai.yaml"
    if not agent_path.exists():
        return "", [f"{skill_name}: missing agents/openai.yaml"]
    text = agent_path.read_text(encoding="utf-8")
    metadata = parse_simple_yaml_mapping(text)
    interface = nested_mapping(metadata, "interface")
    policy = nested_mapping(metadata, "policy")
    display_name = nested_string(interface, "display_name")
    short_description = nested_string(interface, "short_description")
    default_prompt = nested_string(interface, "default_prompt")
    if not short_description:
        errors.append(f"{skill_name}: agents/openai.yaml missing interface.short_description")
    if not default_prompt:
        errors.append(f"{skill_name}: agents/openai.yaml missing interface.default_prompt")
    if not display_name:
        errors.append(f"{skill_name}: agents/openai.yaml missing interface.display_name")
    elif not (skill_name_terms(skill_name) & significant_description_terms(display_name)):
        errors.append(f"{skill_name}: agents/openai.yaml display_name appears stale")
    if not isinstance(policy.get("allow_implicit_invocation"), bool):
        errors.append(
            f"{skill_name}: agents/openai.yaml policy.allow_implicit_invocation must be boolean"
        )
    for field_name, expected_value in REQUIRED_AGENT_POLICY_STRINGS.items():
        value = nested_string(policy, field_name)
        if value != expected_value:
            errors.append(
                f"{skill_name}: agents/openai.yaml policy.{field_name} must be {expected_value!r}"
            )
    if short_description and skill_description:
        shared_terms = significant_description_terms(short_description) & significant_description_terms(
            skill_description
        )
        if len(shared_terms) < MIN_SHARED_DESCRIPTION_TERMS:
            errors.append(
                f"{skill_name}: agents/openai.yaml short_description appears stale "
                f"({len(shared_terms)} shared significant terms)"
            )
    return default_prompt, errors


def validate_skill_dir(root: Path, skill_dir: Path, seen_names: set[str]) -> tuple[str, str, list[str]]:
    errors: list[str] = []
    skill_name = skill_dir.name
    skill_path = skill_dir / "SKILL.md"
    readme_path = skill_dir / "README.md"

    if not skill_path.exists():
        return skill_name, "", [f"{skill_name}: missing SKILL.md"]

    if not readme_path.exists():
        errors.append(f"{skill_name}: missing README.md")

    try:
        frontmatter = parse_frontmatter(skill_path)
    except Exception as exc:
        return skill_name, "", [*errors, f"{skill_name}: frontmatter error: {exc}"]

    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    if not name:
        errors.append(f"{skill_name}: missing name")
    if not description:
        errors.append(f"{skill_name}: missing description")
    if len(description) > 1024:
        errors.append(f"{skill_name}: description exceeds 1024 characters")
    if name != skill_name:
        errors.append(f"{skill_name}: frontmatter name '{name}' does not match folder")
    if not NAME_RE.match(name):
        errors.append(f"{skill_name}: invalid skill name '{name}'")
    if name in seen_names:
        errors.append(f"duplicate skill name: {name}")
    seen_names.add(name)

    default_prompt, agent_errors = validate_agent_metadata(skill_dir, skill_name, description)
    errors.extend(agent_errors)
    for path in skill_reference_files(skill_dir):
        errors.extend(f"{skill_name}: {error}" for error in broken_reference_file_errors(root, path))
    return skill_name, default_prompt, errors


def validate_project_references(root: Path) -> list[str]:
    errors: list[str] = []
    for path in sorted(root.rglob("*")):
        if ".git" in path.parts or path.is_dir():
            continue
        if path.relative_to(root).parts[:1] == ("skills",):
            continue
        if path.suffix in {".md", ".yaml", ".yml"}:
            errors.extend(
                f"{path.relative_to(root)}: {error}"
                for error in broken_local_references(root, path)
            )
    return errors


def validate_skills(root: Path, skills_dir: Path) -> list[str]:
    errors: list[str] = []
    if not skills_dir.exists():
        return ["Missing skills/ directory"]

    skill_dirs = sorted(path for path in skills_dir.iterdir() if path.is_dir())
    if not skill_dirs:
        return ["skills/ directory contains no skill folders"]

    seen_names: set[str] = set()
    seen_prompts: dict[str, str] = {}
    for skill_dir in skill_dirs:
        skill_name, default_prompt, skill_errors = validate_skill_dir(root, skill_dir, seen_names)
        errors.extend(skill_errors)
        if default_prompt:
            previous_skill = seen_prompts.get(default_prompt)
            if previous_skill is not None:
                errors.append(f"duplicate default_prompt in {previous_skill} and {skill_name}")
            seen_prompts[default_prompt] = skill_name
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a local skills plugin package.")
    parser.add_argument(
        "plugin_root",
        nargs="?",
        default=".",
        help="Plugin root to validate. Defaults to the current directory.",
    )
    args = parser.parse_args()

    root = Path(args.plugin_root).expanduser().resolve()
    _, skills_dir, errors = manifest_errors(root)
    errors.extend(validate_skills(root, skills_dir))
    errors.extend(validate_project_references(root))

    if errors:
        print("Validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1
    print(f"Validation passed: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
