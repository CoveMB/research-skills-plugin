#!/usr/bin/env python3
"""Render and check a derived, document-relative full research plugin."""
from __future__ import annotations

import argparse
import json
import re
from collections import deque
from pathlib import Path
from typing import Any, NamedTuple
from urllib.parse import urlsplit

from plugin_utils import (
    agent_policy_fields,
    load_plugin_manifest,
    package_files,
    parse_markdown_frontmatter,
    parse_simple_yaml_mapping,
)
from standalone_skill_bundles import (
    BACKTICK_REFERENCE_RE,
    FORBIDDEN_SOURCE_DIRECTORIES,
    FORBIDDEN_SOURCE_NAMES,
    FORBIDDEN_SOURCE_SUFFIXES,
    MARKDOWN_LINK_RE,
    extract_local_references,
    local_python_imports,
    relative_resource_reference,
    registry_errors,
    resolve_source_reference,
    safe_source_path,
)

ADAPTER_PATH = ".antigravity-plugin/plugin.json"
REGISTRY_PATH = "shared/standalone-skill-registry.json"
DOCUMENT_SUFFIXES = {".md", ".yaml", ".yml"}
RESOURCE_NOTE = (
    "Resolve bundled resource paths relative to the file containing them. Before running a "
    "bundled helper, resolve its script path to an absolute path and invoke it with Python "
    "3.10 or newer from the user's workspace. Keep user input and output paths relative to "
    "that workspace. If a required resource or capability is unavailable, report the "
    "blocker; do not invent verification."
)
PYTHON_COMMAND_RE = re.compile(r"\bpython3\s+((?:\.\./|\./)*scripts/[A-Za-z0-9_./-]+\.py)(?=\s|`|$)")
NONRESOURCE_SPAN_RE = re.compile(
    r"<[^>\n]*>|[A-Za-z][A-Za-z0-9+.-]*:[^\s<>`]+"
    r'|"(?:\\.|[^"\\])*"|(?<!\w)\'(?:\\.|[^\'\\])*\'(?!\w)'
    r"|(?<!\S)--?[\w-]+(?:=|\s+)[^\s]+"
)


class Occurrence(NamedTuple):
    start: int
    end: int
    reference: str


def project_antigravity_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {"$schema": "https://antigravity.google/schemas/v1/plugin.json"}
    for name in ("name", "version", "description", "license"):
        if name in manifest:
            value = manifest[name]
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"manifest {name} must be a nonempty string")
            result[name] = value
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", result.get("name", "")):
        raise ValueError("manifest name must be lowercase kebab-case")
    if "author" in manifest:
        author = manifest["author"]
        if isinstance(author, str) and author.strip():
            result["author"] = author
        elif isinstance(author, dict) and isinstance(author.get("name"), str) and author["name"].strip():
            if any(key not in {"name", "email", "url"} or not isinstance(value, str) or not value.strip() for key, value in author.items()):
                raise ValueError("manifest author fields must be nonempty name/email/url strings")
            if "url" in author:
                url = urlsplit(author["url"])
                if url.scheme != "https" or not url.netloc:
                    raise ValueError("manifest author.url must be an HTTPS URL")
            result["author"] = dict(author)
        else:
            raise ValueError("manifest author must be a nonempty string or an object with a name")
    interface = manifest.get("interface", {})
    if not isinstance(interface, dict):
        raise ValueError("manifest interface must be an object")
    for source, destination in (("displayName", "displayName"), ("logo", "logo")):
        if source in interface:
            value = interface[source]
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"manifest interface.{source} must be a nonempty string")
            result[destination] = value
    if "defaultPrompt" in interface:
        prompts = interface["defaultPrompt"]
        if not isinstance(prompts, list) or any(not isinstance(value, str) or not value.strip() for value in prompts):
            raise ValueError("manifest interface.defaultPrompt must be a list of nonempty strings")
        result["suggestedPrompts"] = prompts[:3]
    return result


def reject_symlink_components(path: Path) -> None:
    """Check lexical components, including aliases before a following '..'."""
    for candidate in (*reversed(path.parents), path):
        if candidate.is_symlink():
            raise ValueError(f"symlinked path is not allowed: {candidate}")


def portable_inventory(root: Path) -> dict[str, Path]:
    inventory: dict[str, Path] = {}
    for path in package_files(root):
        relative = path.relative_to(root)
        if (FORBIDDEN_SOURCE_DIRECTORIES.intersection(relative.parts)
                or relative.name in FORBIDDEN_SOURCE_NAMES
                or relative.suffix in FORBIDDEN_SOURCE_SUFFIXES):
            continue
        inventory[relative.as_posix()] = safe_source_path(root, relative.as_posix())
    return inventory


def resource_occurrences(text: str, source: str, helpers: set[str]) -> list[Occurrence]:
    """Locate resource operands; leave examples, URLs, arguments and prose alone."""
    occurrences: list[Occurrence] = []
    offset = 0
    frontmatter = text.startswith("---\n") and source.endswith("/SKILL.md")
    fence = ""
    for index, line in enumerate(text.splitlines(keepends=True)):
        stripped = line.strip()
        if frontmatter:
            if index and stripped == "---":
                frontmatter = False
            offset += len(line)
            continue
        fence_match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if fence_match:
            marker = fence_match.group(1)
            if not fence:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = ""
            offset += len(line)
            continue
        line_occurrences: list[Occurrence] = []
        if not fence:
            context_spans = [match.span() for match in NONRESOURCE_SPAN_RE.finditer(line)]
            code_spans = [match.span() for match in BACKTICK_REFERENCE_RE.finditer(line)]
            link_spans = [match.span() for match in MARKDOWN_LINK_RE.finditer(line)]
            for pattern in (MARKDOWN_LINK_RE, BACKTICK_REFERENCE_RE):
                for match in pattern.finditer(line):
                    # A code example can enclose a link; formatting in its label cannot.
                    if pattern is MARKDOWN_LINK_RE and any(start <= match.start() and match.end() <= end for start, end in code_spans):
                        continue
                    raw = match.group(1)
                    reference = raw.split("#", 1)[0]
                    if reference in extract_local_references(f"`{reference}`"):
                        start = offset + match.start(1)
                        line_occurrences.append(Occurrence(start, start + len(reference), reference))
            if source == "skills/research-intent-router/SKILL.md":
                protected_spans = context_spans + code_spans + link_spans
                for match in re.finditer(r"(?<![\w./-])MODE_REGISTRY\.md(?![\w./-])", line):
                    if not any(match.start() < end and match.end() > start for start, end in protected_spans):
                        line_occurrences.append(Occurrence(offset + match.start(), offset + match.end(), match.group()))
        # Skill commands are runtime dependencies, including missing/undeclared helpers.
        # Shared maintenance documents only declare runtime helper commands via the registry.
        for match in PYTHON_COMMAND_RE.finditer(line):
            reference = match.group(1)
            if source.startswith("skills/") or reference.lstrip("./") in helpers:
                line_occurrences.append(Occurrence(offset + match.start(1), offset + match.end(1), reference))
        for occurrence in sorted(set(line_occurrences)):
            if not occurrences or occurrence.start >= occurrences[-1].end:
                occurrences.append(occurrence)
        offset += len(line)
    return occurrences


def resolve_portable_reference(root: Path, source: str, reference: str, inventory: dict[str, Path], *, installed: bool) -> str:
    candidate = root / source
    candidates = [candidate.parent / reference]
    if not installed:
        candidates.append(root / reference)
    for path in candidates:
        reject_symlink_components(path)
    if installed:
        try:
            target = candidates[0].resolve().relative_to(root.resolve()).as_posix()
        except ValueError as error:
            raise ValueError(f"{source}: resource escapes plugin: {reference}") from error
    else:
        target = resolve_source_reference(root, source, reference)
    if target not in inventory:
        raise ValueError(f"{source}: missing or excluded resource: {reference}")
    safe_source_path(root, target)
    return target


def runtime_documents(root: Path, inventory: dict[str, Path], *, installed: bool) -> dict[str, list[tuple[Occurrence, str]]]:
    registry = json.loads(safe_source_path(root, REGISTRY_PATH).read_text(encoding="utf-8"))
    entries = registry["skills"]
    helpers = {name for entry in entries for name in entry["runtime_helpers"]}
    seeds = {name for name in inventory if name.startswith("skills/")}
    seeds.update(name for entry in entries for name in (*entry["resources"], *entry["runtime_helpers"]))
    pending = deque(sorted(seeds))
    visited: set[str] = set()
    documents: dict[str, list[tuple[Occurrence, str]]] = {}
    while pending:
        name = pending.popleft()
        if name in visited:
            continue
        visited.add(name)
        if name not in inventory:
            raise ValueError(f"missing or excluded runtime resource: {name}")
        if Path(name).suffix == ".py":
            pending.extend(local_python_imports(root, name))
        if Path(name).suffix not in DOCUMENT_SUFFIXES:
            continue
        text = inventory[name].read_text(encoding="utf-8")
        edges = []
        for occurrence in resource_occurrences(text, name, helpers):
            target = resolve_portable_reference(root, name, occurrence.reference, inventory, installed=installed)
            edges.append((occurrence, target))
            pending.append(target)
        documents[name] = edges
    return documents


def checked_adapter(root: Path, inventory: dict[str, Path]) -> dict[str, Any]:
    adapter = project_antigravity_manifest(load_plugin_manifest(root))
    if "logo" in adapter:
        logo = adapter["logo"]
        safe_source_path(root, logo)
        if Path(logo).as_posix() not in inventory:
            raise ValueError(f"missing or excluded manifest logo: {logo}")
    return adapter


def render_portable_files(root: Path) -> dict[str, bytes]:
    root = root.resolve()
    if (root / ADAPTER_PATH).exists():
        raise ValueError("portable exports cannot be used as source for another export")
    inventory = portable_inventory(root)
    adapter = checked_adapter(root, inventory)
    documents = runtime_documents(root, inventory, installed=False)
    files = {name: path.read_bytes() for name, path in inventory.items()}
    for name, edges in documents.items():
        text = files[name].decode("utf-8")
        for occurrence, target in reversed(edges):
            replacement = relative_resource_reference(name, target)
            # Keep same-directory resources recognizable to existing dependency scanners.
            if "/" not in replacement:
                replacement = "./" + replacement
            text = text[:occurrence.start] + replacement + text[occurrence.end:]
        if name.endswith("/SKILL.md"):
            text, count = re.subn(r"(?m)^(# .+\n)", lambda match: match.group(1) + "\n" + RESOURCE_NOTE + "\n", text, count=1)
            if count != 1:
                raise ValueError(f"missing skill heading: {name}")
        files[name] = text.encode("utf-8")
    files[ADAPTER_PATH] = (json.dumps(adapter, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    return files


def validate_portable_tree(root: Path) -> list[str]:
    try:
        root = root.resolve()
        for path in root.rglob("*"):
            if path.is_symlink():
                raise ValueError(f"symlinked portable member is not allowed: {path.relative_to(root)}")
        inventory = portable_inventory(root)
        adapter_path = root / ADAPTER_PATH
        reject_symlink_components(adapter_path)
        adapter = json.loads(adapter_path.read_text(encoding="utf-8"))
        if adapter != checked_adapter(root, inventory):
            raise ValueError("Antigravity adapter does not match canonical metadata")
        registry = json.loads(safe_source_path(root, REGISTRY_PATH).read_text(encoding="utf-8"))
        expected = {entry["name"] for entry in registry["skills"]}
        actual = {path.parent.name for path in (root / "skills").glob("*/SKILL.md")}
        if len(expected) != 29 or expected != actual:
            raise ValueError("portable catalog must contain all 29 registered skills")
        for name in sorted(expected):
            skill_text = safe_source_path(root, f"skills/{name}/SKILL.md").read_text(encoding="utf-8")
            metadata = parse_markdown_frontmatter(skill_text)
            if metadata.get("name") != name or not metadata.get("description"):
                raise ValueError(f"{name}: invalid discovery metadata")
            if RESOURCE_NOTE not in skill_text:
                raise ValueError(f"{name}: missing generated resource guidance")
            agent = parse_simple_yaml_mapping(safe_source_path(root, f"skills/{name}/agents/openai.yaml").read_text(encoding="utf-8"))
            policy = agent.get("policy", {})
            if not isinstance(policy.get("allow_implicit_invocation"), bool) or any(policy.get(key) != value for key, value in agent_policy_fields(name).items()):
                raise ValueError(f"{name}: invalid agent policy metadata")
        runtime_documents(root, inventory, installed=True)
        errors = registry_errors(root)
        if errors:
            return errors
    except (OSError, ValueError, KeyError, TypeError) as error:
        return [str(error)]
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path, required=True, help="Check an extracted portable plugin without building or installing it.")
    args = parser.parse_args()
    errors = validate_portable_tree(args.check)
    if errors:
        print("Portable validation failed:\n- " + "\n- ".join(errors))
        return 1
    print("Portable validation passed: 29 skills and bundled runtime resources")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
