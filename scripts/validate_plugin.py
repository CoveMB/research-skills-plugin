#!/usr/bin/env python3
"""Validate a Codex/Agent Skills plugin package.

Checks:
- .codex-plugin/plugin.json exists and points to skills
- every skills/<name>/SKILL.md has valid frontmatter
- skill name matches folder name
- required name/description fields are present
- names satisfy Agent Skills naming constraints
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from plugin_utils import load_json_object

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
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


def load_json(path: Path) -> tuple[dict | None, str | None]:
    try:
        payload = load_json_object(path)
    except Exception as exc:
        return None, f"{path.name} parse error: {exc}"
    return payload, None


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


def manifest_errors(root: Path) -> tuple[dict | None, Path, list[str]]:
    errors: list[str] = []
    manifest_path = root / ".codex-plugin" / "plugin.json"
    if not manifest_path.exists():
        return None, root / "skills", ["Missing .codex-plugin/plugin.json"]

    manifest, error = load_json(manifest_path)
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
    return manifest, skills_dir, errors


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
    short_description = nested_string(interface, "short_description")
    default_prompt = nested_string(interface, "default_prompt")
    if not short_description:
        errors.append(f"{skill_name}: agents/openai.yaml missing interface.short_description")
    if not default_prompt:
        errors.append(f"{skill_name}: agents/openai.yaml missing interface.default_prompt")
    if not nested_string(interface, "display_name"):
        errors.append(f"{skill_name}: agents/openai.yaml missing interface.display_name")
    if not isinstance(policy.get("allow_implicit_invocation"), bool):
        errors.append(
            f"{skill_name}: agents/openai.yaml policy.allow_implicit_invocation must be boolean"
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
    for path in [skill_path, readme_path]:
        if path.exists():
            errors.extend(f"{skill_name}: {error}" for error in broken_local_references(root, path))
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
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").expanduser().resolve()
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
