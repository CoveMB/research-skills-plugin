"""Build and validate dependency-closed standalone skill bundles."""
from __future__ import annotations

import ast
import hashlib
import json
import posixpath
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile
from collections import deque
from pathlib import Path, PurePosixPath
from typing import Any, Callable, NamedTuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
from plugin_utils import (
    ALLOWED_PACKAGE_DIRECTORIES,
    ALLOWED_PACKAGE_ROOT_FILES,
    agent_policy_fields,
    nested_mapping,
    parse_simple_yaml_mapping,
)


REGISTRY_PATH = Path("shared/standalone-skill-registry.json")
REGISTRY_SCHEMA_VERSION = "standalone-skill-registry-v1"
BUNDLE_SCHEMA_VERSION = "standalone-skill-bundle-v1"
SUPPORTED_CLASSIFICATIONS = {"self-sufficient", "route-only", "full-plugin-only"}
DEFAULT_MAX_FILE_COUNT = 512
DEFAULT_MAX_TOTAL_BYTES = 16 * 1024 * 1024
FIXED_ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
TEXT_SUFFIXES = {".csv", ".json", ".md", ".py", ".txt", ".yaml", ".yml"}
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)")
BACKTICK_REFERENCE_RE = re.compile(r"`([^`\n]+)`")
INLINE_PATH_TOKEN_RE = re.compile(
    r"(?<![A-Za-z0-9_./-])"
    r"((?:\.codex-plugin|assets|docs|examples|references|scripts|shared|skills)/"
    r"[A-Za-z0-9_./-]+)"
)
EXTERNAL_SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
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
    "validate.sh",
}
FORBIDDEN_SOURCE_DIRECTORIES = {
    ".agent",
    ".codex",
    ".git",
    ".recursive",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "tests",
}
FORBIDDEN_SOURCE_NAMES = {
    ".DS_Store",
    ".env",
    "credentials.json",
    "local-notes.txt",
    "secrets.json",
}
FORBIDDEN_SOURCE_SUFFIXES = {".log", ".pyc", ".tmp", ".zip"}
STANDARD_LIBRARY_MODULES = set(getattr(sys, "stdlib_module_names", ())) | {
    "__future__",
}


class RegistryEntry(NamedTuple):
    name: str
    classification: str
    rationale: str
    resources: tuple[str, ...]
    runtime_helpers: tuple[str, ...]


class DependencyEdge(NamedTuple):
    source: str
    raw_reference: str
    target: str


class BundlePlan(NamedTuple):
    skill_name: str
    classification: str
    rationale: str
    source_to_bundle: dict[str, str]
    dependency_edges: tuple[DependencyEdge, ...]


def _load_json_with_unique_keys(path: Path) -> Any:
    def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"{path}: duplicate JSON key {key!r}")
            result[key] = value
        return result

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)


def _registry_payload(root: Path) -> dict[str, Any]:
    path = root / REGISTRY_PATH
    payload = _load_json_with_unique_keys(path)
    if not isinstance(payload, dict):
        raise ValueError(f"{REGISTRY_PATH}: JSON root must be an object")
    return payload


def _source_skill_names(root: Path) -> list[str]:
    skills_root = root / "skills"
    if not skills_root.is_dir():
        return []
    return sorted(
        path.name for path in skills_root.iterdir() if path.is_dir() and (path / "SKILL.md").is_file()
    )


def _string_list(value: Any, field: str, skill_name: str, errors: list[str]) -> tuple[str, ...]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
        errors.append(f"{skill_name}: {field} must be a list of non-empty paths")
        return ()
    normalized = tuple(item.strip().replace("\\", "/") for item in value)
    if list(normalized) != sorted(set(normalized)):
        errors.append(f"{skill_name}: {field} must be sorted and unique")
    return normalized


def _parse_registry_entries(root: Path, errors: list[str]) -> list[RegistryEntry]:
    try:
        payload = _registry_payload(root)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        errors.append(str(error))
        return []

    if payload.get("schema_version") != REGISTRY_SCHEMA_VERSION:
        errors.append(f"{REGISTRY_PATH}: schema_version must be {REGISTRY_SCHEMA_VERSION!r}")
    raw_entries = payload.get("skills")
    if not isinstance(raw_entries, list):
        errors.append(f"{REGISTRY_PATH}: skills must be a list")
        return []

    entries: list[RegistryEntry] = []
    seen_names: set[str] = set()
    for index, raw_entry in enumerate(raw_entries, start=1):
        if not isinstance(raw_entry, dict):
            errors.append(f"registry entry {index} must be an object")
            continue
        name = raw_entry.get("name")
        classification = raw_entry.get("classification")
        rationale = raw_entry.get("rationale")
        if not isinstance(name, str) or not name.strip():
            errors.append(f"registry entry {index}: name must be non-empty")
            continue
        name = name.strip()
        if name in seen_names:
            errors.append(f"duplicate registry skill entry: {name}")
        seen_names.add(name)
        if classification not in SUPPORTED_CLASSIFICATIONS:
            errors.append(f"{name}: unsupported classification {classification!r}")
        if not isinstance(rationale, str) or not rationale.strip():
            errors.append(f"{name}: rationale must be non-empty")
        resources = _string_list(raw_entry.get("resources"), "resources", name, errors)
        runtime_helpers = _string_list(
            raw_entry.get("runtime_helpers"),
            "runtime_helpers",
            name,
            errors,
        )
        entries.append(
            RegistryEntry(
                name=name,
                classification=str(classification),
                rationale=rationale.strip() if isinstance(rationale, str) else "",
                resources=resources,
                runtime_helpers=runtime_helpers,
            )
        )
    if [entry.name for entry in entries] != sorted(entry.name for entry in entries):
        errors.append("registry skill entries must be sorted by name")
    return entries


def registry_errors(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    entries = _parse_registry_entries(root, errors)
    source_names = _source_skill_names(root)
    registry_names = [entry.name for entry in entries]
    for name in sorted(set(source_names) - set(registry_names)):
        errors.append(f"missing registry entry for source skill: {name}")
    for name in sorted(set(registry_names) - set(source_names)):
        errors.append(f"extra registry entry without source skill: {name}")

    classifications = {entry.name: entry.classification for entry in entries}
    if "research-intent-router" in source_names:
        if classifications.get("research-intent-router") != "route-only":
            errors.append("research-intent-router must be classified route-only")
        if classifications.get("research-book-orchestrator") != "full-plugin-only":
            errors.append("research-book-orchestrator must be classified full-plugin-only")
        self_sufficient_count = sum(
            entry.classification == "self-sufficient" for entry in entries
        )
        if self_sufficient_count != 27:
            errors.append("registry must classify exactly 27 skills as self-sufficient")

    for entry in entries:
        if entry.name not in source_names:
            continue
        for path_value in (*entry.resources, *entry.runtime_helpers):
            try:
                safe_source_path(root, path_value)
            except ValueError as error:
                errors.append(f"{entry.name}: {error}")
        if any(not value.startswith("scripts/") or not value.endswith(".py") for value in entry.runtime_helpers):
            errors.append(f"{entry.name}: runtime_helpers must contain scripts/*.py paths")
        if any(value.startswith("scripts/") for value in entry.resources):
            errors.append(f"{entry.name}: scripts belong in runtime_helpers, not resources")
        try:
            discovered_resources, discovered_helpers = discover_direct_dependencies(root, entry.name)
        except ValueError as error:
            errors.append(f"{entry.name}: {error}")
            continue
        if entry.resources != discovered_resources:
            errors.append(
                f"{entry.name}: declared resources do not match discovered direct resources "
                f"(declared={list(entry.resources)!r}, discovered={list(discovered_resources)!r})"
            )
        if entry.runtime_helpers != discovered_helpers:
            errors.append(
                f"{entry.name}: declared runtime_helpers do not match discovered direct helpers "
                f"(declared={list(entry.runtime_helpers)!r}, discovered={list(discovered_helpers)!r})"
            )
    return sorted(set(errors))


def load_registry(root: Path) -> list[RegistryEntry]:
    errors = registry_errors(root)
    if errors:
        raise ValueError("invalid standalone skill registry:\n- " + "\n- ".join(errors))
    parse_errors: list[str] = []
    return _parse_registry_entries(root.resolve(), parse_errors)


def safe_source_path(root: Path, relative_value: str) -> Path:
    lexical_root = root
    root = root.resolve()
    relative_path = Path(relative_value)
    if relative_path.is_absolute() or ".." in relative_path.parts:
        raise ValueError(f"source path must stay inside the plugin: {relative_value}")
    if not relative_path.parts:
        raise ValueError("source path must not be empty")
    if FORBIDDEN_SOURCE_DIRECTORIES.intersection(relative_path.parts):
        raise ValueError(f"development-only source path is not allowed: {relative_value}")
    if relative_path.name in FORBIDDEN_SOURCE_NAMES or relative_path.suffix in FORBIDDEN_SOURCE_SUFFIXES:
        raise ValueError(f"private or generated source file is not allowed: {relative_value}")

    current = root
    for part in relative_path.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"symlinked source is not allowed: {relative_value}")
    try:
        current.resolve().relative_to(root)
    except ValueError as error:
        raise ValueError(f"source path escapes the plugin: {relative_value}") from error
    if not current.is_file():
        raise ValueError(f"source file is missing: {relative_value}")
    return lexical_root / relative_path


def _clean_reference(reference: str) -> str:
    return reference.strip().split("#", 1)[0]


def _is_path_like_reference(reference: str) -> bool:
    if not reference or any(token in reference for token in (" ", "*", "<", ">", "|")):
        return False
    if reference.endswith("/") or reference in {"assets", "references", "scripts", "skills"}:
        return False
    if reference.startswith(("/", "~", "#")) or EXTERNAL_SCHEME_RE.match(reference):
        return False
    is_local_prefix = (
        reference.startswith(("./", "../"))
        or reference.startswith(LOCAL_REFERENCE_PREFIXES)
        or reference in LOCAL_REFERENCE_ROOT_FILES
    )
    return is_local_prefix and (
        reference in LOCAL_REFERENCE_ROOT_FILES or bool(PurePosixPath(reference).suffix)
    )


def extract_local_references(text: str) -> tuple[str, ...]:
    markdown_values = MARKDOWN_LINK_RE.findall(text)
    inline_values = BACKTICK_REFERENCE_RE.findall(text)
    references = [
        *markdown_values,
        *(
            value
            for value in inline_values
            if value.startswith(("./", "../", *LOCAL_REFERENCE_PREFIXES))
            or value == "MODE_REGISTRY.md"
        ),
        *INLINE_PATH_TOKEN_RE.findall(text),
    ]
    return tuple(
        sorted(
            {
                cleaned
                for reference in references
                if (cleaned := _clean_reference(reference)) and _is_path_like_reference(cleaned)
            }
        )
    )


def _plugin_relative(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError as error:
        raise ValueError(f"source path escapes the plugin: {path}") from error


def _resolve_reference(root: Path, source_relative: str, raw_reference: str) -> str:
    source_path = safe_source_path(root, source_relative)
    candidates: list[Path] = []
    for candidate in (source_path.parent / raw_reference, root / raw_reference):
        try:
            relative_candidate = candidate.resolve().relative_to(root.resolve()).as_posix()
        except ValueError:
            continue
        if relative_candidate not in {path.as_posix() for path in candidates}:
            candidates.append(Path(relative_candidate))

    matches: list[str] = []
    for relative_candidate in candidates:
        try:
            safe_source_path(root, relative_candidate.as_posix())
        except ValueError:
            continue
        matches.append(relative_candidate.as_posix())
    matches = sorted(set(matches))
    if not matches:
        raise ValueError(f"{source_relative}: missing local reference: {raw_reference}")
    if len(matches) > 1:
        raise ValueError(
            f"{source_relative}: ambiguous local reference {raw_reference!r}: {matches!r}"
        )
    return matches[0]


def _skill_runtime_sources(root: Path, skill_name: str) -> list[str]:
    skill_root = root / "skills" / skill_name
    if not (skill_root / "SKILL.md").is_file():
        raise ValueError(f"unknown source skill: {skill_name}")
    sources = [f"skills/{skill_name}/SKILL.md"]
    agent_path = skill_root / "agents" / "openai.yaml"
    if not agent_path.is_file():
        raise ValueError(f"{skill_name}: missing agents/openai.yaml")
    sources.append(f"skills/{skill_name}/agents/openai.yaml")
    for directory_name in ("assets", "references", "scripts"):
        directory = skill_root / directory_name
        if not directory.exists():
            continue
        for path in sorted(directory.rglob("*")):
            if path.is_symlink():
                raise ValueError(f"{skill_name}: symlinked skill source is not allowed: {path}")
            if path.is_file():
                sources.append(_plugin_relative(root, path))
    return sorted(set(sources))


def discover_direct_dependencies(root: Path, skill_name: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
    root = root.resolve()
    skill_prefix = f"skills/{skill_name}/"
    resources: set[str] = set()
    helpers: set[str] = set()
    for source_relative in _skill_runtime_sources(root, skill_name):
        source_path = safe_source_path(root, source_relative)
        if source_path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = source_path.read_text(encoding="utf-8")
        for raw_reference in extract_local_references(text):
            target = _resolve_reference(root, source_relative, raw_reference)
            if target.startswith(skill_prefix):
                continue
            if target.startswith("scripts/") and target.endswith(".py"):
                helpers.add(target)
            else:
                resources.add(target)
    return tuple(sorted(resources)), tuple(sorted(helpers))


def _local_python_imports(root: Path, source_relative: str) -> tuple[str, ...]:
    source_path = safe_source_path(root, source_relative)
    try:
        tree = ast.parse(source_path.read_text(encoding="utf-8"), filename=source_relative)
    except SyntaxError as error:
        raise ValueError(f"{source_relative}: invalid Python syntax: {error.msg}") from error

    dependencies: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                dependencies.update(_resolve_python_module(root, source_path, alias.name, 0))
            continue
        if not isinstance(node, ast.ImportFrom):
            continue
        module_name = node.module or ""
        if module_name:
            dependencies.update(
                _resolve_python_module(root, source_path, module_name, node.level)
            )
            for alias in node.names:
                if alias.name == "*":
                    continue
                dependencies.update(
                    _resolve_python_module(
                        root,
                        source_path,
                        f"{module_name}.{alias.name}",
                        node.level,
                        required=False,
                    )
                )
        elif node.level:
            for alias in node.names:
                if alias.name == "*":
                    continue
                dependencies.update(
                    _resolve_python_module(
                        root,
                        source_path,
                        alias.name,
                        node.level,
                    )
                )
    return tuple(sorted(dependencies))


def _resolve_python_module(
    root: Path,
    source_path: Path,
    module_name: str,
    level: int,
    *,
    required: bool = True,
) -> tuple[str, ...]:
    if not module_name:
        return ()
    module_parts = tuple(part for part in module_name.split(".") if part)
    top_level = module_parts[0]
    if level == 0 and top_level in STANDARD_LIBRARY_MODULES:
        return ()
    search_roots = [source_path.parent]
    if level > 0:
        base = source_path.parent
        for _ in range(level - 1):
            base = base.parent
        search_roots = [base]
    elif (root / "scripts") not in search_roots:
        search_roots.append(root / "scripts")

    matches: dict[str, Path] = {}
    for search_root in search_roots:
        module_path = search_root.joinpath(*module_parts)
        for candidate in (module_path.with_suffix(".py"), module_path / "__init__.py"):
            if not candidate.is_file():
                continue
            relative_candidate = _plugin_relative(root, candidate)
            safe_source_path(root, relative_candidate)
            matches[relative_candidate] = search_root
    if len(matches) > 1:
        raise ValueError(f"{_plugin_relative(root, source_path)}: ambiguous local import {module_name!r}")
    if matches:
        dependencies = set(matches)
        matched_root = next(iter(matches.values()))
        for index in range(1, len(module_parts)):
            initializer = matched_root.joinpath(*module_parts[:index], "__init__.py")
            if initializer.is_file():
                relative_initializer = _plugin_relative(root, initializer)
                safe_source_path(root, relative_initializer)
                dependencies.add(relative_initializer)
        return tuple(sorted(dependencies))
    if required and (level > 0 or top_level not in STANDARD_LIBRARY_MODULES):
        raise ValueError(
            f"{_plugin_relative(root, source_path)}: unresolved non-standard Python import {module_name!r}"
        )
    return ()


def _destination_mapping(skill_name: str, sources: set[str]) -> dict[str, str]:
    skill_prefix = f"skills/{skill_name}/"
    external_references = sorted(
        source
        for source in sources
        if not source.startswith(skill_prefix)
        and source != "LICENSE"
        and not source.startswith("scripts/")
    )
    basename_counts: dict[str, int] = {}
    for source in external_references:
        key = PurePosixPath(source).name.casefold()
        basename_counts[key] = basename_counts.get(key, 0) + 1

    mapping: dict[str, str] = {}
    for source in sorted(sources):
        if source == "LICENSE":
            destination = "LICENSE"
        elif source == f"skills/{skill_name}/SKILL.md":
            destination = "SKILL.md"
        elif source.startswith(skill_prefix):
            destination = source[len(skill_prefix) :]
        elif source.startswith("scripts/"):
            destination = source
        else:
            name = PurePosixPath(source).name
            if basename_counts[name.casefold()] > 1:
                path = PurePosixPath(name)
                suffix = hashlib.sha256(source.encode("utf-8")).hexdigest()[:8]
                name = f"{path.stem}-{suffix}{path.suffix}"
            destination = f"references/{name}"
        mapping[source] = destination

    destinations = list(mapping.values())
    if len(destinations) != len(set(destinations)):
        raise ValueError("bundle destination collision")
    if len(destinations) != len({value.casefold() for value in destinations}):
        raise ValueError("case-colliding bundle destinations")
    return mapping


def create_bundle_plan(root: Path, skill_name: str) -> BundlePlan:
    root = root.resolve()
    entries = {entry.name: entry for entry in load_registry(root)}
    entry = entries.get(skill_name)
    if entry is None:
        raise ValueError(f"skill is not present in standalone registry: {skill_name}")
    if entry.classification == "full-plugin-only":
        raise ValueError(f"{skill_name} is full-plugin-only: {entry.rationale}")

    initial_sources = {
        *_skill_runtime_sources(root, skill_name),
        "LICENSE",
        *entry.resources,
        *entry.runtime_helpers,
    }
    pending = deque(sorted(initial_sources))
    sources: set[str] = set()
    source_casefolds: dict[str, str] = {}
    edges: set[DependencyEdge] = set()
    while pending:
        source_relative = pending.popleft()
        if source_relative in sources:
            continue
        source_path = safe_source_path(root, source_relative)
        folded = source_relative.casefold()
        previous = source_casefolds.get(folded)
        if previous is not None and previous != source_relative:
            raise ValueError(f"case-colliding source paths: {previous!r}, {source_relative!r}")
        source_casefolds[folded] = source_relative
        sources.add(source_relative)

        if source_path.suffix.lower() in TEXT_SUFFIXES:
            text = source_path.read_text(encoding="utf-8")
            for raw_reference in extract_local_references(text):
                target = _resolve_reference(root, source_relative, raw_reference)
                edges.add(DependencyEdge(source_relative, raw_reference, target))
                if target not in sources:
                    pending.append(target)
        if source_path.suffix.lower() == ".py":
            for target in _local_python_imports(root, source_relative):
                edges.add(DependencyEdge(source_relative, f"import:{PurePosixPath(target).stem}", target))
                if target not in sources:
                    pending.append(target)

    return BundlePlan(
        skill_name=skill_name,
        classification=entry.classification,
        rationale=entry.rationale,
        source_to_bundle=_destination_mapping(skill_name, sources),
        dependency_edges=tuple(sorted(edges)),
    )


def _stable_json_bytes(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")


def plugin_version(root: Path) -> str:
    manifest_path = root.resolve() / ".codex-plugin" / "plugin.json"
    payload = _load_json_with_unique_keys(manifest_path)
    version = payload.get("version") if isinstance(payload, dict) else None
    if not isinstance(version, str) or not version.strip():
        raise ValueError(".codex-plugin/plugin.json: version must be a non-empty string")
    return version.strip()


def source_commit(root: Path) -> str:
    resolved_root = root.resolve()
    try:
        repository_result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=resolved_root,
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return "unavailable"
    if repository_result.returncode != 0:
        return "unavailable"

    repository_root = Path(repository_result.stdout.strip()).resolve()
    try:
        plugin_prefix = resolved_root.relative_to(repository_root)
    except ValueError:
        return "unavailable"

    manifest_path = plugin_prefix / ".codex-plugin" / "plugin.json"
    tracked_manifest = subprocess.run(
        [
            "git",
            "-C",
            str(repository_root),
            "ls-files",
            "--error-unmatch",
            "--",
            manifest_path.as_posix(),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if tracked_manifest.returncode != 0:
        return "unavailable"

    package_pathspecs = [
        (plugin_prefix / relative_path).as_posix()
        for relative_path in sorted(
            ALLOWED_PACKAGE_DIRECTORIES | ALLOWED_PACKAGE_ROOT_FILES
        )
    ]
    package_status = subprocess.run(
        [
            "git",
            "-C",
            str(repository_root),
            "status",
            "--porcelain=v1",
            "--untracked-files=all",
            "--",
            *package_pathspecs,
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if package_status.returncode != 0 or package_status.stdout.strip():
        return "unavailable"

    commit_result = subprocess.run(
        ["git", "-C", str(repository_root), "rev-parse", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    commit = commit_result.stdout.strip()
    if commit_result.returncode != 0 or not re.fullmatch(r"[0-9a-fA-F]{40}", commit):
        return "unavailable"
    return commit.lower()


def _relative_bundle_reference(source_destination: str, target_destination: str) -> str:
    source_parent = PurePosixPath(source_destination).parent.as_posix()
    return posixpath.relpath(target_destination, source_parent)


def _rewrite_text_source(
    text: str,
    source_relative: str,
    plan: BundlePlan,
) -> str:
    source_destination = plan.source_to_bundle[source_relative]
    source_edges = sorted(
        (
            edge
            for edge in plan.dependency_edges
            if edge.source == source_relative and not edge.raw_reference.startswith("import:")
        ),
        key=lambda edge: (-len(edge.raw_reference), edge.raw_reference, edge.target),
    )
    for edge in source_edges:
        target_destination = plan.source_to_bundle.get(edge.target)
        if target_destination is None:
            raise ValueError(
                f"{source_relative}: dependency target is absent from bundle plan: {edge.target}"
            )
        replacement = _relative_bundle_reference(source_destination, target_destination)
        text = text.replace(edge.raw_reference, replacement)
    if plan.classification == "route-only" and source_destination == "SKILL.md":
        text = text.rstrip() + (
            "\n\n## Standalone bundle boundary\n\n"
            "This generated bundle is route-only. It can recommend an appropriate specialist, "
            "but it must not claim that an absent specialist skill was run. Install the selected "
            "skill or the full plugin before executing that specialist workflow.\n"
        )
    return text


def _render_bundle_files(root: Path, plan: BundlePlan) -> dict[str, bytes]:
    rendered: dict[str, bytes] = {}
    for source_relative, destination in sorted(plan.source_to_bundle.items()):
        source_path = safe_source_path(root, source_relative)
        source_bytes = source_path.read_bytes()
        if source_path.suffix.lower() in TEXT_SUFFIXES:
            try:
                source_text = source_bytes.decode("utf-8")
            except UnicodeDecodeError as error:
                raise ValueError(f"{source_relative}: text source must be UTF-8") from error
            source_bytes = _rewrite_text_source(source_text, source_relative, plan).encode("utf-8")
        rendered[destination] = source_bytes
    return rendered


def _bundle_manifest(root: Path, plan: BundlePlan, rendered: dict[str, bytes]) -> dict[str, Any]:
    return {
        "schema_version": BUNDLE_SCHEMA_VERSION,
        "skill_name": plan.skill_name,
        "classification": plan.classification,
        "rationale": plan.rationale,
        "plugin_version": plugin_version(root),
        "source_commit": source_commit(root),
        "source_to_bundle": dict(sorted(plan.source_to_bundle.items())),
        "sha256": {
            destination: hashlib.sha256(content).hexdigest()
            for destination, content in sorted(rendered.items())
        },
    }


def _enforce_bundle_limits(
    rendered: dict[str, bytes],
    manifest_bytes: bytes,
    max_file_count: int,
    max_total_bytes: int,
) -> None:
    file_count = len(rendered) + 1
    total_bytes = sum(len(content) for content in rendered.values()) + len(manifest_bytes)
    if max_file_count < 1 or file_count > max_file_count:
        raise ValueError(f"bundle file count {file_count} exceeds limit {max_file_count}")
    if max_total_bytes < 1 or total_bytes > max_total_bytes:
        raise ValueError(f"bundle uncompressed size {total_bytes} exceeds limit {max_total_bytes}")


def _remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink(missing_ok=True)
    elif path.is_dir():
        shutil.rmtree(path)


def stage_standalone_bundle(
    root: Path,
    skill_name: str,
    bundle_directory: Path,
    *,
    max_file_count: int = DEFAULT_MAX_FILE_COUNT,
    max_total_bytes: int = DEFAULT_MAX_TOTAL_BYTES,
) -> dict[str, Any]:
    root = root.resolve()
    plan = create_bundle_plan(root, skill_name)
    rendered = _render_bundle_files(root, plan)
    manifest = _bundle_manifest(root, plan, rendered)
    manifest_bytes = _stable_json_bytes(manifest)
    _enforce_bundle_limits(rendered, manifest_bytes, max_file_count, max_total_bytes)

    if bundle_directory.exists() or bundle_directory.is_symlink():
        raise ValueError(f"staged bundle destination already exists: {bundle_directory}")
    try:
        bundle_directory.mkdir(parents=True)
        for destination, content in sorted(rendered.items()):
            output_path = bundle_directory / destination
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(content)
            output_path.chmod(0o644)
        manifest_path = bundle_directory / "standalone-bundle.json"
        manifest_path.write_bytes(manifest_bytes)
        manifest_path.chmod(0o644)
    except Exception:
        _remove_path(bundle_directory)
        raise
    return manifest


def write_deterministic_zip(bundle_directory: Path, archive_path: Path) -> None:
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_archive = archive_path.with_suffix(archive_path.suffix + ".tmp")
    _remove_path(temporary_archive)
    try:
        with zipfile.ZipFile(
            temporary_archive,
            "w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=9,
        ) as archive:
            for path in sorted(bundle_directory.rglob("*")):
                if not path.is_file() or path.is_symlink():
                    continue
                relative_path = path.relative_to(bundle_directory).as_posix()
                archive_name = f"{bundle_directory.name}/{relative_path}"
                info = zipfile.ZipInfo(archive_name, FIXED_ZIP_TIMESTAMP)
                info.create_system = 3
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = (stat.S_IFREG | 0o644) << 16
                info.flag_bits = 0
                archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        temporary_archive.replace(archive_path)
    except Exception:
        _remove_path(temporary_archive)
        raise


def _manifest_from_directory(bundle_directory: Path) -> dict[str, Any]:
    manifest_path = bundle_directory / "standalone-bundle.json"
    payload = _load_json_with_unique_keys(manifest_path)
    if not isinstance(payload, dict):
        raise ValueError(f"{manifest_path}: manifest must be a JSON object")
    return payload


def verify_staged_pair(bundle_directory: Path, bundle_zip: Path) -> None:
    manifest = _manifest_from_directory(bundle_directory)
    hashes = manifest.get("sha256")
    if not isinstance(hashes, dict):
        raise ValueError("standalone bundle manifest sha256 must be an object")
    directory_files = {
        path.relative_to(bundle_directory).as_posix(): path.read_bytes()
        for path in sorted(bundle_directory.rglob("*"))
        if path.is_file() and not path.is_symlink()
    }
    if set(hashes) != set(directory_files) - {"standalone-bundle.json"}:
        raise ValueError("staged bundle manifest inventory does not match directory")
    for relative_path, expected_hash in hashes.items():
        if not isinstance(expected_hash, str):
            raise ValueError(f"invalid staged hash for {relative_path}")
        actual_hash = hashlib.sha256(directory_files[relative_path]).hexdigest()
        if actual_hash != expected_hash:
            raise ValueError(f"staged bundle hash mismatch: {relative_path}")
    with zipfile.ZipFile(bundle_zip) as archive:
        zip_files = {
            name[len(bundle_directory.name) + 1 :]: archive.read(name)
            for name in archive.namelist()
            if not name.endswith("/") and name.startswith(f"{bundle_directory.name}/")
        }
        expected_names = {
            f"{bundle_directory.name}/{relative_path}" for relative_path in directory_files
        }
        if set(archive.namelist()) != expected_names:
            raise ValueError("staged archive inventory does not match directory")
    if zip_files != directory_files:
        raise ValueError("staged archive content does not match directory")


def stage_bundle_pair(root: Path, skill_name: str, catalog_root: Path) -> tuple[Path, Path]:
    bundle_directory = catalog_root / skill_name
    bundle_zip = catalog_root / f"{skill_name}.zip"
    stage_standalone_bundle(root, skill_name, bundle_directory)
    write_deterministic_zip(bundle_directory, bundle_zip)
    verify_staged_pair(bundle_directory, bundle_zip)
    validate_bundle_pair(bundle_directory, bundle_zip)
    return bundle_directory, bundle_zip


def _replace_path(source: Path, target: Path) -> None:
    source.replace(target)


def _validated_output_root(root: Path, output_root: Path) -> Path:
    root = root.resolve()
    output_root = Path(output_root)
    if output_root.is_symlink():
        raise ValueError(f"standalone output root must not be a symlink: {output_root}")
    resolved_output = output_root.resolve(strict=False)
    try:
        root.relative_to(resolved_output)
    except ValueError:
        pass
    else:
        raise ValueError(
            f"standalone output must not contain or replace the canonical source: {resolved_output}"
        )

    try:
        resolved_output.relative_to(root)
    except ValueError:
        return resolved_output

    generated_root = (root / "dist").resolve()
    try:
        resolved_output.relative_to(generated_root)
    except ValueError as error:
        raise ValueError(
            "standalone output inside the plugin must stay under the generated output "
            f"directory {generated_root}: {resolved_output}"
        ) from error
    return resolved_output


def _validate_pair_publication_target(output_root: Path, skill_name: str) -> None:
    if output_root.exists() and not output_root.is_dir():
        raise ValueError(f"standalone output root must be a directory: {output_root}")
    target_directory = output_root / skill_name
    target_zip = output_root / f"{skill_name}.zip"
    has_directory = target_directory.exists() or target_directory.is_symlink()
    has_zip = target_zip.exists() or target_zip.is_symlink()
    if has_directory:
        try:
            validate_bundle_directory(target_directory, expected_name=skill_name)
        except (OSError, ValueError) as error:
            raise ValueError(
                "refusing to replace an existing target that is not a valid generated bundle: "
                f"{target_directory}"
            ) from error
    if has_zip:
        try:
            validate_bundle_zip(target_zip, expected_name=skill_name)
        except (OSError, ValueError) as error:
            raise ValueError(
                "refusing to replace an existing target that is not a valid generated bundle: "
                f"{target_zip}"
            ) from error
    if has_directory and has_zip:
        try:
            validate_bundle_pair(target_directory, target_zip)
        except (OSError, ValueError) as error:
            raise ValueError(
                f"refusing to replace a mismatched generated bundle pair: {skill_name}"
            ) from error


def _validate_catalog_publication_target(output_root: Path) -> None:
    if not output_root.exists():
        return
    if not output_root.is_dir() or output_root.is_symlink():
        raise ValueError(f"standalone catalog output must be a real directory: {output_root}")
    entries = sorted(output_root.iterdir())
    if not entries:
        return

    directories = {
        path.name
        for path in entries
        if path.is_dir() and not path.is_symlink()
    }
    archives = {
        path.stem
        for path in entries
        if path.is_file() and not path.is_symlink() and path.suffix == ".zip"
    }
    expected_entry_names = directories | {f"{name}.zip" for name in archives}
    if {path.name for path in entries} != expected_entry_names or directories != archives:
        raise ValueError(
            "refusing to replace a nonempty directory that is not a generated standalone catalog: "
            f"{output_root}"
        )
    for skill_name in sorted(directories):
        try:
            validate_bundle_pair(
                output_root / skill_name,
                output_root / f"{skill_name}.zip",
            )
        except (OSError, ValueError) as error:
            raise ValueError(
                "refusing to replace a nonempty directory that is not a valid generated "
                f"standalone catalog: {output_root}"
            ) from error


def _rollback_publication(
    *,
    removal_paths: tuple[Path, ...],
    restoration_pairs: tuple[tuple[Path, Path], ...],
    replace_function: Callable[[Path, Path], None],
    backup_root: Path,
    publication_error: Exception,
) -> None:
    rollback_errors: list[str] = []
    for path in removal_paths:
        try:
            _remove_path(path)
        except OSError as error:
            rollback_errors.append(f"remove {path}: {error}")
    for backup, target in restoration_pairs:
        if not backup.exists() and not backup.is_symlink():
            continue
        try:
            replace_function(backup, target)
        except OSError as error:
            rollback_errors.append(f"restore {target}: {error}")
    if rollback_errors:
        details = "; ".join(rollback_errors)
        raise RuntimeError(
            f"publication failed and rollback was incomplete; backups retained at "
            f"{backup_root}: {details}"
        ) from publication_error


def publish_bundle_pair(
    staged_directory: Path,
    staged_zip: Path,
    output_root: Path,
    skill_name: str,
    *,
    replace_function: Callable[[Path, Path], None] | None = None,
) -> tuple[Path, Path]:
    replace = replace_function or _replace_path
    output_root.mkdir(parents=True, exist_ok=True)
    target_directory = output_root / skill_name
    target_zip = output_root / f"{skill_name}.zip"
    backup_root = Path(
        tempfile.mkdtemp(prefix=f".{skill_name}.backup-", dir=output_root.parent)
    )
    backup_directory = backup_root / skill_name
    backup_zip = backup_root / f"{skill_name}.zip"
    had_directory = target_directory.exists() or target_directory.is_symlink()
    had_zip = target_zip.exists() or target_zip.is_symlink()
    published_directory = False
    published_zip = False
    retain_backup = False
    try:
        if had_directory:
            replace(target_directory, backup_directory)
        if had_zip:
            replace(target_zip, backup_zip)
        replace(staged_directory, target_directory)
        published_directory = True
        replace(staged_zip, target_zip)
        published_zip = True
    except Exception as publication_error:
        try:
            _rollback_publication(
                removal_paths=tuple(
                    path
                    for path, published in (
                        (target_zip, published_zip),
                        (target_directory, published_directory),
                    )
                    if published
                ),
                restoration_pairs=tuple(
                    pair
                    for pair, had_target in (
                        ((backup_directory, target_directory), had_directory),
                        ((backup_zip, target_zip), had_zip),
                    )
                    if had_target
                ),
                replace_function=replace,
                backup_root=backup_root,
                publication_error=publication_error,
            )
        except RuntimeError:
            retain_backup = True
            raise
        raise
    finally:
        if not retain_backup:
            _remove_path(backup_root)
    return target_directory, target_zip


def build_standalone_skill(
    root: Path,
    skill_name: str,
    output_root: Path,
) -> tuple[Path, Path]:
    root = root.resolve()
    create_bundle_plan(root, skill_name)
    output_root = _validated_output_root(root, output_root)
    _validate_pair_publication_target(output_root, skill_name)
    output_root.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=f".{skill_name}.staging-",
        dir=output_root.parent,
    ) as temporary_directory:
        staged_root = Path(temporary_directory)
        staged_directory, staged_zip = stage_bundle_pair(root, skill_name, staged_root)
        return publish_bundle_pair(
            staged_directory,
            staged_zip,
            output_root,
            skill_name,
        )


def _publish_catalog(
    staged_catalog: Path,
    output_root: Path,
    *,
    replace_function: Callable[[Path, Path], None] | None = None,
) -> None:
    replace = replace_function or _replace_path
    output_root.parent.mkdir(parents=True, exist_ok=True)
    backup_root = Path(
        tempfile.mkdtemp(prefix=f".{output_root.name}.backup-", dir=output_root.parent)
    )
    backup_catalog = backup_root / output_root.name
    had_catalog = output_root.exists() or output_root.is_symlink()
    published = False
    retain_backup = False
    try:
        if had_catalog:
            replace(output_root, backup_catalog)
        replace(staged_catalog, output_root)
        published = True
    except Exception as publication_error:
        try:
            _rollback_publication(
                removal_paths=(output_root,) if published else (),
                restoration_pairs=((backup_catalog, output_root),) if had_catalog else (),
                replace_function=replace,
                backup_root=backup_root,
                publication_error=publication_error,
            )
        except RuntimeError:
            retain_backup = True
            raise
        raise
    finally:
        if not retain_backup:
            _remove_path(backup_root)


def build_all_standalone_skills(root: Path, output_root: Path) -> list[tuple[Path, Path]]:
    root = root.resolve()
    eligible_names = [
        entry.name
        for entry in load_registry(root)
        if entry.classification != "full-plugin-only"
    ]
    output_root = _validated_output_root(root, output_root)
    _validate_catalog_publication_target(output_root)
    output_root.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=f".{output_root.name}.staging-",
        dir=output_root.parent,
    ) as temporary_directory:
        staged_catalog = Path(temporary_directory) / output_root.name
        staged_catalog.mkdir()
        for skill_name in eligible_names:
            stage_bundle_pair(root, skill_name, staged_catalog)
        _publish_catalog(staged_catalog, output_root)
    return [
        (output_root / skill_name, output_root / f"{skill_name}.zip")
        for skill_name in eligible_names
    ]


BUNDLE_ROOT_DIRECTORIES = {"agents", "assets", "references", "scripts"}
BUNDLE_ROOT_FILES = {"LICENSE", "SKILL.md", "standalone-bundle.json"}
GENERIC_INLINE_FILE_LABELS = {"README.md", "SKILL.md", "standalone-bundle.json"}
BUNDLE_REFERENCE_SUFFIXES = TEXT_SUFFIXES | {
    ".gif",
    ".jpeg",
    ".jpg",
    ".pdf",
    ".png",
    ".svg",
    ".webp",
}
def _safe_bundle_relative_path(relative_value: str) -> PurePosixPath:
    if "\\" in relative_value or "\x00" in relative_value:
        raise ValueError(f"unsafe bundle path: {relative_value!r}")
    path = PurePosixPath(relative_value)
    if not relative_value or path.is_absolute() or ".." in path.parts or "." in path.parts:
        raise ValueError(f"unsafe bundle path: {relative_value!r}")
    if path.name in FORBIDDEN_SOURCE_NAMES or path.suffix in FORBIDDEN_SOURCE_SUFFIXES:
        raise ValueError(f"forbidden bundle file: {relative_value}")
    if FORBIDDEN_SOURCE_DIRECTORIES.intersection(path.parts):
        raise ValueError(f"forbidden bundle directory: {relative_value}")
    if path.parts[0] not in BUNDLE_ROOT_DIRECTORIES and relative_value not in BUNDLE_ROOT_FILES:
        raise ValueError(f"unexpected bundle root entry: {path.parts[0]}")
    return path


def _directory_inventory(
    bundle_directory: Path,
    *,
    max_file_count: int,
    max_total_bytes: int,
) -> dict[str, bytes]:
    if bundle_directory.is_symlink():
        raise ValueError(f"bundle directory must not be a symlink: {bundle_directory}")
    if not bundle_directory.is_dir():
        raise ValueError(f"bundle directory is missing: {bundle_directory}")
    inventory: list[tuple[Path, str, int]] = []
    folded_paths: dict[str, str] = {}
    declared_total_bytes = 0
    for path in sorted(bundle_directory.rglob("*")):
        relative_path = path.relative_to(bundle_directory).as_posix()
        if path.is_symlink():
            raise ValueError(f"bundle symlink is not allowed: {relative_path}")
        _safe_bundle_relative_path(relative_path)
        folded = relative_path.casefold()
        previous = folded_paths.get(folded)
        if previous is not None and previous != relative_path:
            raise ValueError(f"case-colliding bundle paths: {previous!r}, {relative_path!r}")
        folded_paths[folded] = relative_path
        file_status = path.stat()
        if stat.S_ISDIR(file_status.st_mode):
            continue
        if not stat.S_ISREG(file_status.st_mode):
            raise ValueError(f"bundle special file is not allowed: {relative_path}")
        inventory.append((path, relative_path, file_status.st_size))
        if len(inventory) > max_file_count:
            raise ValueError(
                f"bundle file count {len(inventory)} exceeds limit {max_file_count}"
            )
        declared_total_bytes += file_status.st_size
        if declared_total_bytes > max_total_bytes:
            raise ValueError(
                f"bundle uncompressed size {declared_total_bytes} exceeds limit "
                f"{max_total_bytes}"
            )

    files: dict[str, bytes] = {}
    total_bytes = 0
    for path, relative_path, expected_size in inventory:
        remaining_bytes = max_total_bytes - total_bytes
        with path.open("rb") as source:
            content = source.read(remaining_bytes + 1)
        if len(content) > remaining_bytes:
            raise ValueError(
                f"bundle uncompressed size {total_bytes + len(content)} exceeds limit "
                f"{max_total_bytes}"
            )
        if len(content) != expected_size:
            raise ValueError(f"bundle file changed during validation: {relative_path}")
        files[relative_path] = content
        total_bytes += len(content)
    return files


def _validated_manifest(
    manifest_bytes: bytes,
    files: dict[str, bytes],
    expected_name: str,
) -> dict[str, Any]:
    try:
        manifest = json.loads(
            manifest_bytes.decode("utf-8"),
            object_pairs_hook=lambda pairs: _unique_pairs(pairs, "standalone-bundle.json"),
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise ValueError(f"invalid standalone-bundle.json: {error}") from error
    if not isinstance(manifest, dict):
        raise ValueError("standalone-bundle.json must contain a JSON object")
    required_fields = {
        "schema_version",
        "skill_name",
        "classification",
        "rationale",
        "plugin_version",
        "source_commit",
        "source_to_bundle",
        "sha256",
    }
    if set(manifest) != required_fields:
        raise ValueError(
            "standalone bundle manifest fields do not match the required schema "
            f"(missing={sorted(required_fields - set(manifest))!r}, "
            f"extra={sorted(set(manifest) - required_fields)!r})"
        )
    if manifest["schema_version"] != BUNDLE_SCHEMA_VERSION:
        raise ValueError(f"unsupported bundle manifest schema: {manifest['schema_version']!r}")
    if manifest["skill_name"] != expected_name:
        raise ValueError(
            f"bundle name {expected_name!r} does not match manifest skill_name "
            f"{manifest['skill_name']!r}"
        )
    if manifest["classification"] not in {"self-sufficient", "route-only"}:
        raise ValueError(f"invalid standalone classification: {manifest['classification']!r}")
    for field in ("rationale", "plugin_version", "source_commit"):
        if not isinstance(manifest[field], str) or not manifest[field].strip():
            raise ValueError(f"standalone bundle manifest {field} must be a non-empty string")
    if manifest["source_commit"] != "unavailable" and not re.fullmatch(
        r"[0-9a-f]{40}", manifest["source_commit"]
    ):
        raise ValueError("standalone bundle source_commit must be a lowercase commit or unavailable")

    source_to_bundle = manifest["source_to_bundle"]
    hashes = manifest["sha256"]
    if not isinstance(source_to_bundle, dict) or not all(
        isinstance(source, str) and isinstance(destination, str)
        for source, destination in source_to_bundle.items()
    ):
        raise ValueError("standalone bundle source_to_bundle must map strings to strings")
    if not isinstance(hashes, dict) or not all(
        isinstance(path, str) and re.fullmatch(r"[0-9a-f]{64}", digest or "")
        for path, digest in hashes.items()
    ):
        raise ValueError("standalone bundle sha256 must map paths to lowercase SHA-256 values")

    destinations = list(source_to_bundle.values())
    for source in source_to_bundle:
        source_path = PurePosixPath(source)
        if source_path.is_absolute() or ".." in source_path.parts or "\\" in source:
            raise ValueError(f"unsafe manifest source path: {source}")
    for destination in destinations:
        _safe_bundle_relative_path(destination)
    if len(destinations) != len(set(destinations)) or len(destinations) != len(
        {destination.casefold() for destination in destinations}
    ):
        raise ValueError("manifest source_to_bundle destinations collide")
    expected_files = set(files) - {"standalone-bundle.json"}
    if set(destinations) != expected_files:
        raise ValueError("manifest source_to_bundle inventory does not match bundle files")
    if set(hashes) != expected_files:
        raise ValueError("manifest hash inventory does not match bundle files")
    for relative_path, expected_hash in hashes.items():
        actual_hash = hashlib.sha256(files[relative_path]).hexdigest()
        if actual_hash != expected_hash:
            raise ValueError(f"bundle hash mismatch: {relative_path}")
    if _stable_json_bytes(manifest) != manifest_bytes:
        raise ValueError("standalone-bundle.json must use stable sorted JSON with a final newline")
    return manifest


def _unique_pairs(pairs: list[tuple[str, Any]], label: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"{label}: duplicate JSON key {key!r}")
        result[key] = value
    return result


def _frontmatter_field(text: str, field: str) -> str:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("SKILL.md frontmatter is not closed")
    frontmatter = text[4:end]
    match = re.search(rf"(?m)^{re.escape(field)}:\s*(.+?)\s*$", frontmatter)
    if not match:
        raise ValueError(f"SKILL.md frontmatter {field} is missing")
    return match.group(1).strip().strip('"\'')


def _validate_skill_and_agent(files: dict[str, bytes], expected_name: str) -> None:
    required = {"SKILL.md", "agents/openai.yaml", "LICENSE", "standalone-bundle.json"}
    missing = sorted(required - set(files))
    if missing:
        raise ValueError(f"bundle is missing required files: {missing!r}")
    try:
        skill_text = files["SKILL.md"].decode("utf-8")
        agent_text = files["agents/openai.yaml"].decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("SKILL.md and agents/openai.yaml must be UTF-8") from error
    frontmatter_name = _frontmatter_field(skill_text, "name")
    if frontmatter_name != expected_name:
        raise ValueError(
            f"SKILL.md frontmatter name {frontmatter_name!r} does not match {expected_name!r}"
        )
    if not _frontmatter_field(skill_text, "description"):
        raise ValueError("SKILL.md frontmatter description must be non-empty")
    metadata = parse_simple_yaml_mapping(agent_text)
    interface = nested_mapping(metadata, "interface")
    policy = nested_mapping(metadata, "policy")
    for field_name in ("display_name", "short_description", "default_prompt"):
        value = interface.get(field_name)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"agents/openai.yaml interface.{field_name} must be non-empty")
    if not isinstance(policy.get("allow_implicit_invocation"), bool):
        raise ValueError(
            "agents/openai.yaml policy.allow_implicit_invocation must be boolean"
        )
    for field_name, expected_value in agent_policy_fields(expected_name).items():
        actual_value = policy.get(field_name)
        if actual_value != expected_value:
            raise ValueError(
                f"agents/openai.yaml policy.{field_name} must be {expected_value!r}, "
                f"got {actual_value!r}"
            )


def _extract_bundle_references(text: str) -> tuple[str, ...]:
    markdown_values = MARKDOWN_LINK_RE.findall(text)
    inline_values = BACKTICK_REFERENCE_RE.findall(text)
    candidates = [
        *markdown_values,
        *(
            value
            for value in inline_values
            if value.startswith(("./", "../", *LOCAL_REFERENCE_PREFIXES))
            or (
                "/" not in value
                and PurePosixPath(value).suffix.lower() in BUNDLE_REFERENCE_SUFFIXES
                and value not in GENERIC_INLINE_FILE_LABELS
            )
        ),
        *INLINE_PATH_TOKEN_RE.findall(text),
    ]
    references: set[str] = set()
    for candidate in candidates:
        cleaned = _clean_reference(candidate)
        if not cleaned or any(token in cleaned for token in (" ", "*", "<", ">", "|")):
            continue
        if cleaned.startswith(("/", "~", "#")) or EXTERNAL_SCHEME_RE.match(cleaned):
            continue
        if cleaned.endswith("/") or not PurePosixPath(cleaned).suffix:
            if cleaned not in LOCAL_REFERENCE_ROOT_FILES:
                continue
        references.add(cleaned)
    return tuple(sorted(references))


def _resolve_bundle_reference(
    source_relative: str,
    raw_reference: str,
    inventory: set[str],
) -> str:
    source_parent = PurePosixPath(source_relative).parent
    target = source_parent.joinpath(raw_reference)
    normalized = PurePosixPath(posixpath.normpath(target.as_posix()))
    if normalized.is_absolute() or ".." in normalized.parts:
        raise ValueError(
            f"{source_relative}: local reference escapes the bundle: {raw_reference}"
        )
    target_value = normalized.as_posix()
    if target_value not in inventory:
        raise ValueError(f"{source_relative}: missing local reference: {raw_reference}")
    return target_value


def _validate_bundle_references(files: dict[str, bytes]) -> None:
    inventory = set(files)
    for source_relative, content in sorted(files.items()):
        if source_relative == "standalone-bundle.json":
            continue
        if PurePosixPath(source_relative).suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError as error:
            raise ValueError(f"{source_relative}: text bundle file must be UTF-8") from error
        for raw_reference in _extract_bundle_references(text):
            _resolve_bundle_reference(source_relative, raw_reference, inventory)


def _require_bundled_python_module(
    source_path: PurePosixPath,
    module_name: str,
    level: int,
    inventory: set[str],
    *,
    required: bool = True,
) -> None:
    if not module_name:
        return
    module_parts = tuple(part for part in module_name.split(".") if part)
    top_level = module_parts[0]
    if level == 0 and top_level in STANDARD_LIBRARY_MODULES:
        return
    if level > 0:
        base = source_path.parent
        for _ in range(level - 1):
            base = base.parent
        search_roots = [base]
    else:
        search_roots = [source_path.parent, PurePosixPath("scripts")]

    candidates: set[str] = set()
    for search_root in search_roots:
        module_path = search_root.joinpath(*module_parts)
        candidates.update(
            {
                module_path.with_suffix(".py").as_posix(),
                (module_path / "__init__.py").as_posix(),
            }
        )
    matches = candidates & inventory
    if not matches and required:
        raise ValueError(
            f"{source_path.as_posix()}: unresolved bundled Python import {module_name!r}"
        )
    if len(matches) > 1:
        raise ValueError(
            f"{source_path.as_posix()}: ambiguous bundled Python import {module_name!r}"
        )


def _bundle_python_dependencies(source_relative: str, content: bytes, inventory: set[str]) -> None:
    try:
        tree = ast.parse(content.decode("utf-8"), filename=source_relative)
    except (SyntaxError, UnicodeDecodeError) as error:
        raise ValueError(f"{source_relative}: invalid bundled Python source: {error}") from error
    source_path = PurePosixPath(source_relative)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                _require_bundled_python_module(
                    source_path,
                    alias.name,
                    0,
                    inventory,
                )
            continue
        if not isinstance(node, ast.ImportFrom):
            continue
        module_name = node.module or ""
        if module_name:
            _require_bundled_python_module(
                source_path,
                module_name,
                node.level,
                inventory,
            )
            for alias in node.names:
                if alias.name == "*":
                    continue
                _require_bundled_python_module(
                    source_path,
                    f"{module_name}.{alias.name}",
                    node.level,
                    inventory,
                    required=False,
                )
        elif node.level:
            for alias in node.names:
                if alias.name == "*":
                    continue
                _require_bundled_python_module(
                    source_path,
                    alias.name,
                    node.level,
                    inventory,
                )


def _validate_bundle_python(files: dict[str, bytes]) -> None:
    inventory = set(files)
    for source_relative, content in sorted(files.items()):
        if source_relative.endswith(".py"):
            _bundle_python_dependencies(source_relative, content, inventory)


def validate_bundle_directory(
    bundle_directory: Path,
    *,
    expected_name: str | None = None,
    max_file_count: int = DEFAULT_MAX_FILE_COUNT,
    max_total_bytes: int = DEFAULT_MAX_TOTAL_BYTES,
) -> dict[str, Any]:
    bundle_directory = Path(bundle_directory)
    name = expected_name or bundle_directory.name
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        raise ValueError(f"invalid standalone skill name: {name!r}")
    files = _directory_inventory(
        bundle_directory,
        max_file_count=max_file_count,
        max_total_bytes=max_total_bytes,
    )
    manifest = _validated_manifest(files["standalone-bundle.json"], files, name)
    _validate_skill_and_agent(files, name)
    _validate_bundle_references(files)
    _validate_bundle_python(files)
    return manifest


def _inspect_archive_members(
    archive: zipfile.ZipFile,
    expected_name: str,
    *,
    max_file_count: int,
    max_total_bytes: int,
) -> list[zipfile.ZipInfo]:
    members = archive.infolist()
    seen: set[str] = set()
    seen_folded: dict[str, str] = {}
    file_paths: set[str] = set()
    total_bytes = 0
    regular_members: list[zipfile.ZipInfo] = []
    for info in members:
        name = info.filename
        if "\\" in name or "\x00" in name:
            raise ValueError(f"unsafe archive member name: {name!r}")
        path = PurePosixPath(name)
        if path.is_absolute():
            raise ValueError(f"absolute archive member is not allowed: {name}")
        if ".." in path.parts:
            raise ValueError(f"parent traversal archive member is not allowed: {name}")
        canonical_name = path.as_posix()
        comparable_name = name[:-1] if info.is_dir() and name.endswith("/") else name
        if canonical_name != comparable_name:
            raise ValueError(f"non-canonical archive member is not allowed: {name}")
        if name in seen:
            raise ValueError(f"duplicate archive member: {name}")
        seen.add(name)
        folded = name.casefold()
        previous = seen_folded.get(folded)
        if previous is not None and previous != name:
            raise ValueError(f"case-colliding archive members: {previous!r}, {name!r}")
        seen_folded[folded] = name
        if not path.parts or path.parts[0] != expected_name:
            raise ValueError(
                f"archive member must be rooted at {expected_name!r}: {name}"
            )
        relative_parts = path.parts[1:]
        if not relative_parts:
            if not info.is_dir():
                raise ValueError(f"archive root must be a directory entry: {name}")
            continue
        relative_value = PurePosixPath(*relative_parts).as_posix()
        mode = (info.external_attr >> 16) & 0xFFFF
        if mode and stat.S_ISLNK(mode):
            raise ValueError(f"archive symlink is not allowed: {name}")
        file_type = stat.S_IFMT(mode)
        if file_type and not (stat.S_ISREG(mode) or stat.S_ISDIR(mode)):
            raise ValueError(f"archive special file is not allowed: {name}")
        _safe_bundle_relative_path(relative_value)
        if info.flag_bits & 0x1:
            raise ValueError(f"encrypted archive member is not allowed: {name}")
        if info.is_dir():
            continue
        file_paths.add(relative_value)
        regular_members.append(info)
        total_bytes += info.file_size
    for file_path in file_paths:
        parts = PurePosixPath(file_path).parts
        for index in range(1, len(parts)):
            prefix = PurePosixPath(*parts[:index]).as_posix()
            if prefix in file_paths:
                raise ValueError(f"archive directory/file prefix conflict: {prefix}")
    if len(regular_members) > max_file_count:
        raise ValueError(
            f"archive file count {len(regular_members)} exceeds limit {max_file_count}"
        )
    if total_bytes > max_total_bytes:
        raise ValueError(f"archive uncompressed size {total_bytes} exceeds limit {max_total_bytes}")
    return regular_members


def validate_bundle_zip(
    bundle_zip: Path,
    *,
    expected_name: str | None = None,
    max_file_count: int = DEFAULT_MAX_FILE_COUNT,
    max_total_bytes: int = DEFAULT_MAX_TOTAL_BYTES,
) -> dict[str, Any]:
    bundle_zip = Path(bundle_zip)
    name = expected_name or bundle_zip.stem
    if not bundle_zip.is_file() or bundle_zip.is_symlink():
        raise ValueError(f"standalone bundle archive is missing or unsafe: {bundle_zip}")
    try:
        with zipfile.ZipFile(bundle_zip) as archive:
            members = _inspect_archive_members(
                archive,
                name,
                max_file_count=max_file_count,
                max_total_bytes=max_total_bytes,
            )
            with tempfile.TemporaryDirectory(prefix=f".{name}.validate-") as temporary_directory:
                extracted_root = Path(temporary_directory) / name
                extracted_root.mkdir()
                for info in members:
                    relative_path = PurePosixPath(*PurePosixPath(info.filename).parts[1:])
                    target = extracted_root.joinpath(*relative_path.parts)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    with archive.open(info) as source:
                        content = source.read(max_total_bytes + 1)
                    if len(content) != info.file_size:
                        raise ValueError(f"archive member size mismatch: {info.filename}")
                    target.write_bytes(content)
                return validate_bundle_directory(
                    extracted_root,
                    expected_name=name,
                    max_file_count=max_file_count,
                    max_total_bytes=max_total_bytes,
                )
    except zipfile.BadZipFile as error:
        raise ValueError(f"invalid standalone bundle archive: {error}") from error


def validate_bundle_pair(bundle_directory: Path, bundle_zip: Path) -> dict[str, Any]:
    name = Path(bundle_directory).name
    directory_manifest = validate_bundle_directory(bundle_directory, expected_name=name)
    archive_manifest = validate_bundle_zip(bundle_zip, expected_name=name)
    if directory_manifest != archive_manifest:
        raise ValueError(f"directory/archive manifest equivalence failed for {name}")
    return directory_manifest


def _catalog_registry_entries(registry_path: Path) -> list[RegistryEntry]:
    try:
        payload = _load_json_with_unique_keys(Path(registry_path))
    except (OSError, ValueError, json.JSONDecodeError) as error:
        raise ValueError(f"invalid catalog registry: {error}") from error
    if not isinstance(payload, dict) or payload.get("schema_version") != REGISTRY_SCHEMA_VERSION:
        raise ValueError("catalog registry has an unsupported schema")
    raw_entries = payload.get("skills")
    if not isinstance(raw_entries, list):
        raise ValueError("catalog registry skills must be a list")
    entries: list[RegistryEntry] = []
    seen: set[str] = set()
    for raw_entry in raw_entries:
        if not isinstance(raw_entry, dict):
            raise ValueError("catalog registry skill entries must be objects")
        name = raw_entry.get("name")
        classification = raw_entry.get("classification")
        rationale = raw_entry.get("rationale")
        if not isinstance(name, str) or name in seen:
            raise ValueError(f"duplicate or invalid catalog registry skill: {name!r}")
        if classification not in SUPPORTED_CLASSIFICATIONS:
            raise ValueError(f"invalid catalog classification for {name}: {classification!r}")
        if not isinstance(rationale, str) or not rationale.strip():
            raise ValueError(f"catalog registry rationale is missing for {name}")
        seen.add(name)
        entries.append(
            RegistryEntry(
                name,
                classification,
                rationale,
                tuple(raw_entry.get("resources", ())),
                tuple(raw_entry.get("runtime_helpers", ())),
            )
        )
    return entries


def validate_catalog(
    catalog_root: Path,
    registry_path: Path,
    *,
    require_complete: bool = True,
) -> list[dict[str, Any]]:
    catalog_root = Path(catalog_root)
    if not catalog_root.is_dir() or catalog_root.is_symlink():
        raise ValueError(f"standalone catalog directory is missing or unsafe: {catalog_root}")
    entries = _catalog_registry_entries(Path(registry_path))
    eligible = {
        entry.name: entry for entry in entries if entry.classification != "full-plugin-only"
    }
    full_plugin_names = {
        entry.name for entry in entries if entry.classification == "full-plugin-only"
    }
    actual_directories = {
        path.name for path in catalog_root.iterdir() if path.is_dir() and not path.is_symlink()
    }
    actual_archives = {
        path.stem for path in catalog_root.iterdir() if path.is_file() and path.suffix == ".zip"
    }
    unexpected_entries = sorted(
        path.name
        for path in catalog_root.iterdir()
        if not (path.is_dir() and path.name in eligible)
        and not (path.is_file() and path.suffix == ".zip" and path.stem in eligible)
    )
    if unexpected_entries:
        raise ValueError(f"unexpected catalog entries: {unexpected_entries!r}")
    forbidden_full = sorted((actual_directories | actual_archives) & full_plugin_names)
    if forbidden_full:
        raise ValueError(f"full-plugin-only bundles are forbidden in catalog: {forbidden_full!r}")
    present_names = actual_directories | actual_archives
    missing_pairs = sorted(
        name
        for name in present_names
        if name not in actual_directories or name not in actual_archives
    )
    if missing_pairs:
        raise ValueError(f"missing catalog bundle pair: {missing_pairs!r}")
    if require_complete:
        missing = sorted(set(eligible) - actual_directories)
        if missing:
            raise ValueError(f"missing catalog bundle: {missing!r}")
    manifests: list[dict[str, Any]] = []
    for name in sorted(actual_directories):
        manifest = validate_bundle_pair(
            catalog_root / name,
            catalog_root / f"{name}.zip",
        )
        entry = eligible[name]
        if manifest["classification"] != entry.classification:
            raise ValueError(f"catalog classification mismatch for {name}")
        if manifest["rationale"] != entry.rationale:
            raise ValueError(f"catalog rationale mismatch for {name}")
        manifests.append(manifest)
    return manifests


def validate_standalone_path(
    target: Path,
    *,
    registry_path: Path | None = None,
    require_catalog_complete: bool = False,
) -> Any:
    target = Path(target)
    if target.is_file() and target.suffix == ".zip":
        return validate_bundle_zip(target)
    if target.is_dir() and (target / "standalone-bundle.json").is_file():
        return validate_bundle_directory(target)
    if target.is_dir() and (target / "SKILL.md").is_file():
        raise ValueError(
            "raw source skill folder is not a standalone bundle; build it before validation"
        )
    if target.is_dir():
        if registry_path is None:
            raise ValueError("catalog validation requires --registry")
        return validate_catalog(
            target,
            registry_path,
            require_complete=require_catalog_complete,
        )
    raise ValueError(f"standalone bundle or catalog does not exist: {target}")
