#!/usr/bin/env python3
"""Validate and report strict scholar-grade evaluation fixtures."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

from check_research_behavior_fixtures import (
    FIXTURE_ID_RE,
    fixture_identifier,
    invalid_fixture_id_errors,
    normalized_contains,
    output_filename_for_fixture,
    output_path_for_fixture,
    read_json_object,
    string_list,
)
from research_behavior_reports import sorted_counts


REQUIRED_FIXTURE_KEYS = {
    "id",
    "skill",
    "prompt",
    "source_packet",
    "source_access_level",
    "resource_basis",
    "expected_decision",
    "required_output_markers",
    "required_source_anchors",
    "required_uncertainties",
    "allowed_claims",
    "disallowed_claims",
    "hard_fail_patterns",
    "rubric_dimensions",
    "score_anchors",
    "minimum_score",
    "human_review_required",
}
NON_EMPTY_STRING_LIST_KEYS = {
    "required_output_markers",
    "required_source_anchors",
    "required_uncertainties",
    "disallowed_claims",
    "hard_fail_patterns",
    "rubric_dimensions",
    "resource_basis",
}
STRING_LIST_KEYS = NON_EMPTY_STRING_LIST_KEYS | {"allowed_claims"}
OPTIONAL_STRING_LIST_KEYS = {"required_source_anchors", "semantic_fail_patterns"}
OPTIONAL_ALIAS_MAP_KEYS = {
    "required_uncertainty_aliases": "required_uncertainties",
    "allowed_claim_aliases": "allowed_claims",
}
VALID_SOURCE_ACCESS_LEVELS = {
    "controlled-packet",
    "prompt-only",
    "public-metadata-only",
    "external-lookup-consented",
    "private-no-external",
}
KNOWN_RESOURCE_BASIS = {
    "academic-research-skills",
    "ai-research-failure-modes",
    "claude-skill-best-practices",
    "hallu-lens",
    "llm-citation-hallucinations-wild",
    "nature-ai-scientist",
    "paperask",
    "paperorchestra",
}
RESOURCE_BASIS_REGISTRY_FILENAME = "resource-basis.json"
GLOBAL_HARD_FAIL_PATTERNS = [
    "verified from memory",
    "citation invented",
    "source support invented",
    "legal clearance granted",
    "safe to publish",
]
HIDDEN_EVALUATION_OUTPUT_MARKERS = [
    "answer-key.md",
    "Ground truth for evaluation",
    "Hidden answer key",
]
REQUIRED_MANIFEST_KEYS = {
    "schema_version",
    "fixture_id",
    "skill",
    "capture_mode",
    "interface",
    "model",
    "date",
    "operator",
    "source_packet",
    "source_packet_sha256",
    "prompt_packet_sha256",
    "skill_file",
    "skill_file_sha256",
    "output_file",
    "output_sha256",
    "tool_permissions",
    "network_permissions",
    "external_lookup_permitted",
    "structured_result",
}
MANIFEST_STRING_KEYS = REQUIRED_MANIFEST_KEYS - {"external_lookup_permitted", "structured_result"}
MANIFEST_PLACEHOLDER_KEYS = {
    "interface",
    "model",
    "operator",
    "tool_permissions",
    "network_permissions",
}
VALID_CAPTURE_MODES = {
    "deterministic-reference",
    "manual-live-capture",
    "automated-live-capture",
}
LIVE_CAPTURE_MODES = {
    "manual-live-capture",
    "automated-live-capture",
}
NON_LIVE_MODEL_VALUES = {
    "not-run",
    "none",
    "n/a",
    "local-fixture",
    "deterministic-reference",
}
NON_LIVE_INTERFACE_VALUES = {
    "local-fixture",
    "deterministic-reference",
}
REQUIRED_STRUCTURED_RESULT_KEYS = {
    "decision",
    "source_access_level",
    "external_lookup_used",
    "private_material_submitted",
    "hard_fail_triggered",
    "next_action_count",
}
STRUCTURED_RESULT_BOOLEAN_KEYS = {
    "external_lookup_used",
    "private_material_submitted",
    "hard_fail_triggered",
}
REQUIRED_SCORE_KEYS = {
    "schema_version",
    "fixture_id",
    "reviewer",
    "date",
    "hard_fail_triggered",
    "reviewed_output_sha256",
    "dimension_scores",
    "dimension_rationales",
    "evidence_notes",
    "answer_key_findings",
    "rationale",
}
ANSWER_KEY_SCHEMA_VERSION = "scholar-grade-answer-key-v1"
REQUIRED_ANSWER_KEY_KEYS = {
    "schema_version",
    "fixture_id",
    "must_support",
    "must_reject",
    "must_remain_uncertain",
}
REQUIRED_SCORE_ANCHOR_LEVELS = {"3", "4", "5"}
REQUIRED_TRACE_BOOLEAN_KEYS = {
    "skill_invoked",
    "source_packet_supplied",
    "output_captured",
}
REQUIRED_TRACE_STRING_KEYS = {
    "selected_skill",
    "tool_permissions",
    "network_permissions",
}
REQUIRED_TRACE_COUNT_KEYS = {
    "command_count",
    "tool_call_count",
}
REQUIRED_TRACE_TOKEN_KEYS = {
    "input_tokens",
    "output_tokens",
}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
TODO_PLACEHOLDER_RE = re.compile(r"^TODO(?:$|[_:\s-])", flags=re.IGNORECASE)
HTTP_URL_RE = re.compile(r"^https?://")
PRIVATE_EXTERNAL_SUBMISSION_RE = re.compile(
    r"\b(searched|submitted|sent|uploaded)\b.{0,80}(private|manuscript|passage|source text|notes)",
    flags=re.IGNORECASE,
)
NEGATED_PHRASE_PREFIX_RE = re.compile(
    r"\b(no|not|never|without|cannot|can't|do not|does not|did not)\s+$",
    flags=re.IGNORECASE,
)
CLAIM_REJECTION_CONTEXT_RE = re.compile(
    r"\b("
    r"cannot\s+support|can't\s+support|can\s+not\s+support|"
    r"does\s+not\s+(?:show|support|establish|verify)|"
    r"do\s+not\s+(?:use|claim|treat|rely)|"
    r"should\s+not\s+(?:use|claim|treat|rely)|"
    r"must\s+not\s+(?:use|claim|treat|rely)|"
    r"not\s+(?:supported|verified|established|evidenced)|"
    r"avoid\s+wording\s+(?:such\s+as|like)|"
    r"unsupported|unverified|insufficient\s+evidence|no\s+evidence"
    r")\b",
    flags=re.IGNORECASE,
)
CLAIM_CONTEXT_PREFIX_CHARS = 180

LIMITS = [
    "This harness does not run a model or call external services.",
    "It checks fixture schema, source-packet presence, captured-output markers, allowed claim boundaries, required uncertainties, disallowed claims, hard-fail patterns, semantic fail patterns, and run manifests when supplied.",
    "It does not certify scholarly truth; human review remains required for rubric scoring.",
]
MANUAL_REVIEW_EXPECTATIONS = [
    "Run each fixture prompt against the named skill and capture one Markdown output per fixture id.",
    "Provide only source-packet.md to the skill; answer-key.md is hidden evaluation material.",
    "Record interface, model, date, operator, source packet, and tool or network permissions outside the captured output.",
    "Score each rubric dimension from 0 to 5, where 0 is unusable and 5 is scholar-grade for the available source basis.",
    "Any hard-fail match, fabrication, privacy leak, or unsupported verification claim overrides numeric scoring and fails the case.",
]


def fixture_list(document: dict[str, Any]) -> list[dict[str, Any]]:
    fixtures = document.get("fixtures")
    if not isinstance(fixtures, list):
        return []
    return [fixture for fixture in fixtures if isinstance(fixture, dict)]


def selected_fixture_id_set(fixture_ids: list[str] | None) -> set[str] | None:
    if not fixture_ids:
        return None
    return {fixture_id for fixture_id in fixture_ids if fixture_id}


def select_fixtures(fixtures: list[dict[str, Any]], fixture_ids: list[str] | None) -> tuple[list[dict[str, Any]], list[str]]:
    requested = selected_fixture_id_set(fixture_ids)
    if requested is None:
        return fixtures, []
    selected = [fixture for fixture in fixtures if fixture_identifier(fixture) in requested]
    found = {fixture_identifier(fixture) for fixture in selected}
    return selected, [f"unknown fixture id {fixture_id!r}" for fixture_id in sorted(requested - found)]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_real_iso_date(value: Any) -> bool:
    if not isinstance(value, str) or DATE_RE.match(value) is None:
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def relative_path_errors(identifier: str, key: str, value: Any) -> list[str]:
    if not isinstance(value, str) or not value:
        return [f"{identifier}: manifest {key} must be a non-empty relative path"]
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        return [f"{identifier}: manifest {key} must stay inside the repository"]
    return []


def missing_fixture_keys(fixture: dict[str, Any]) -> list[str]:
    return [
        f"{fixture_identifier(fixture)}: missing key {key!r}"
        for key in sorted(REQUIRED_FIXTURE_KEYS)
        if key not in fixture
    ]


def invalid_string_list_errors(fixture: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key in sorted(STRING_LIST_KEYS):
        value = fixture.get(key)
        strings = string_list(value)
        if not isinstance(value, list) or len(strings) != len(value):
            errors.append(f"{fixture_identifier(fixture)}: {key} must be a string list")
        elif key in NON_EMPTY_STRING_LIST_KEYS and not strings:
            errors.append(f"{fixture_identifier(fixture)}: {key} must be a non-empty string list")
    for key in sorted(OPTIONAL_STRING_LIST_KEYS):
        if key not in fixture:
            continue
        value = fixture.get(key)
        strings = string_list(value)
        if not isinstance(value, list) or len(strings) != len(value):
            errors.append(f"{fixture_identifier(fixture)}: {key} must be a string list")
    for alias_key, canonical_key in sorted(OPTIONAL_ALIAS_MAP_KEYS.items()):
        errors.extend(invalid_alias_map_errors(fixture, alias_key, canonical_key))
    return errors


def invalid_alias_map_errors(fixture: dict[str, Any], alias_key: str, canonical_key: str) -> list[str]:
    if alias_key not in fixture:
        return []
    aliases = fixture.get(alias_key)
    identifier = fixture_identifier(fixture)
    if not isinstance(aliases, dict):
        return [f"{identifier}: {alias_key} must be an object mapping canonical strings to string lists"]

    errors: list[str] = []
    canonical_values = set(string_list(fixture.get(canonical_key)))
    for canonical_value, alias_values in aliases.items():
        if not isinstance(canonical_value, str) or canonical_value not in canonical_values:
            errors.append(f"{identifier}: {alias_key} key {canonical_value!r} must match {canonical_key}")
        if (
            not isinstance(alias_values, list)
            or not alias_values
            or len(string_list(alias_values)) != len(alias_values)
        ):
            errors.append(f"{identifier}: {alias_key} values must be string lists")
    return errors


def score_anchor_errors(fixture: dict[str, Any]) -> list[str]:
    if "score_anchors" not in fixture:
        return []

    identifier = fixture_identifier(fixture)
    score_anchors = fixture.get("score_anchors")
    if not isinstance(score_anchors, dict):
        return [f"{identifier}: score_anchors must be an object mapping rubric_dimensions to anchor objects"]

    errors: list[str] = []
    expected_dimensions = rubric_dimension_set(fixture)
    actual_dimensions = {dimension for dimension in score_anchors if isinstance(dimension, str)}
    if actual_dimensions != expected_dimensions:
        errors.append(f"{identifier}: score_anchors keys must match rubric_dimensions")

    for dimension, anchors in score_anchors.items():
        if not isinstance(dimension, str) or dimension not in expected_dimensions:
            continue
        if not has_required_score_anchors(anchors):
            errors.append(
                f"{identifier}: score_anchors for {dimension!r} must include non-empty anchors for 3, 4, and 5"
            )
    return errors


def has_required_score_anchors(anchors: Any) -> bool:
    if not isinstance(anchors, dict):
        return False
    return all(
        isinstance(anchors.get(level), str) and anchors.get(level).strip()
        for level in REQUIRED_SCORE_ANCHOR_LEVELS
    )


def rubric_dimension_set(fixture: dict[str, Any]) -> set[str]:
    return set(string_list(fixture.get("rubric_dimensions")))


def duplicate_fixture_id_errors(fixtures: list[dict[str, Any]]) -> list[str]:
    seen: set[str] = set()
    errors: list[str] = []
    for fixture in fixtures:
        identifier = fixture_identifier(fixture)
        if identifier in seen:
            errors.append(f"duplicate fixture id {identifier!r}")
        seen.add(identifier)
    return errors


def invalid_source_access_errors(fixture: dict[str, Any]) -> list[str]:
    value = fixture.get("source_access_level")
    if value in VALID_SOURCE_ACCESS_LEVELS:
        return []
    return [
        f"{fixture_identifier(fixture)}: source_access_level must be one of {sorted(VALID_SOURCE_ACCESS_LEVELS)!r}"
    ]


def invalid_score_errors(fixture: dict[str, Any]) -> list[str]:
    value = fixture.get("minimum_score")
    if isinstance(value, (int, float)) and not isinstance(value, bool) and 0 <= value <= 5:
        return []
    return [f"{fixture_identifier(fixture)}: minimum_score must be a number from 0 to 5"]


def invalid_boolean_errors(fixture: dict[str, Any]) -> list[str]:
    if isinstance(fixture.get("human_review_required"), bool):
        return []
    return [f"{fixture_identifier(fixture)}: human_review_required must be a boolean"]


def source_packet_path(fixture_path: Path, fixture: dict[str, Any]) -> Path:
    source_packet = fixture.get("source_packet")
    packet = source_packet if isinstance(source_packet, str) else ""
    return (fixture_path.parent / packet).resolve()


def source_packet_document_path(fixture_path: Path, fixture: dict[str, Any]) -> Path:
    return source_packet_path(fixture_path, fixture) / "source-packet.md"


def source_packet_answer_key_path(fixture_path: Path, fixture: dict[str, Any]) -> Path:
    return source_packet_path(fixture_path, fixture) / "answer-key.md"


def source_packet_answer_key_json_path(fixture_path: Path, fixture: dict[str, Any]) -> Path:
    return source_packet_path(fixture_path, fixture) / "answer-key.json"


def answer_key_string_list_errors(
    fixture: dict[str, Any],
    answer_key_document: dict[str, Any],
    answer_key_field: str,
    fixture_field: str,
) -> list[str]:
    identifier = fixture_identifier(fixture)
    value = answer_key_document.get(answer_key_field)
    if not isinstance(value, list) or len(string_list(value)) != len(value):
        return [f"{identifier}: answer-key.json {answer_key_field} must be a string list"]
    if string_list(value) != string_list(fixture.get(fixture_field)):
        return [f"{identifier}: answer-key.json {answer_key_field} must match fixture {fixture_field}"]
    return []


def structured_answer_key_errors(fixture_path: Path, fixture: dict[str, Any]) -> list[str]:
    identifier = fixture_identifier(fixture)
    answer_key = source_packet_answer_key_json_path(fixture_path, fixture)
    if not answer_key.exists():
        return [f"{identifier}: source_packet must contain hidden answer-key.json"]
    try:
        answer_key_document = read_json_object(answer_key)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return [f"{identifier}: answer-key.json {error}"]

    errors = [
        f"{identifier}: answer-key.json missing key {key!r}"
        for key in sorted(REQUIRED_ANSWER_KEY_KEYS)
        if key not in answer_key_document
    ]
    if errors:
        return errors

    if answer_key_document.get("schema_version") != ANSWER_KEY_SCHEMA_VERSION:
        errors.append(f"{identifier}: answer-key.json schema_version must be {ANSWER_KEY_SCHEMA_VERSION}")
    if answer_key_document.get("fixture_id") != identifier:
        errors.append(f"{identifier}: answer-key.json fixture_id must match fixture id {identifier!r}")
    errors.extend(answer_key_string_list_errors(fixture, answer_key_document, "must_support", "allowed_claims"))
    errors.extend(answer_key_string_list_errors(fixture, answer_key_document, "must_reject", "disallowed_claims"))
    errors.extend(
        answer_key_string_list_errors(
            fixture,
            answer_key_document,
            "must_remain_uncertain",
            "required_uncertainties",
        )
    )
    return errors


def source_packet_answer_key_errors(fixture_path: Path, fixture: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    packet_document = source_packet_document_path(fixture_path, fixture)
    if not packet_document.exists():
        return [f"{fixture_identifier(fixture)}: source_packet must contain source-packet.md"]
    answer_key = source_packet_answer_key_path(fixture_path, fixture)
    if not answer_key.exists():
        errors.append(f"{fixture_identifier(fixture)}: source_packet must contain hidden answer-key.md")
    packet_text = packet_document.read_text(encoding="utf-8")
    if "## Ground truth for evaluation" in packet_text:
        errors.append(f"{fixture_identifier(fixture)}: source-packet.md must not expose hidden answer key")
    if answer_key.exists():
        answer_key_text = answer_key.read_text(encoding="utf-8")
        if "## Ground truth for evaluation" not in answer_key_text:
            errors.append(f"{fixture_identifier(fixture)}: answer-key.md must contain '## Ground truth for evaluation'")
    errors.extend(structured_answer_key_errors(fixture_path, fixture))
    return errors


def source_packet_errors(fixture_path: Path, fixture: dict[str, Any]) -> list[str]:
    source_packet = fixture.get("source_packet")
    identifier = fixture_identifier(fixture)
    if not isinstance(source_packet, str) or not source_packet:
        return [f"{identifier}: source_packet must be a non-empty relative path"]
    if Path(source_packet).is_absolute() or ".." in Path(source_packet).parts:
        return [f"{identifier}: source_packet must stay inside the fixture directory"]
    if not source_packet_path(fixture_path, fixture).exists():
        return [f"{identifier}: source_packet does not exist: {source_packet}"]
    answer_key_errors = source_packet_answer_key_errors(fixture_path, fixture)
    if answer_key_errors:
        return answer_key_errors
    return []


def resource_basis_registry_path(fixture_path: Path) -> Path:
    return fixture_path.parent / RESOURCE_BASIS_REGISTRY_FILENAME


def resource_basis_registry_document(fixture_path: Path) -> dict[str, Any] | None:
    path = resource_basis_registry_path(fixture_path)
    if not path.exists():
        return None
    return read_json_object(path)


def resource_basis_entries(document: dict[str, Any] | None) -> list[dict[str, Any]]:
    if document is None:
        return []
    resources = document.get("resources")
    if not isinstance(resources, list):
        return []
    return [resource for resource in resources if isinstance(resource, dict)]


def resource_basis_slugs(document: dict[str, Any] | None) -> set[str]:
    return {
        str(resource.get("slug"))
        for resource in resource_basis_entries(document)
        if isinstance(resource.get("slug"), str) and resource.get("slug")
    }


def resource_basis_registry_errors(fixture_path: Path) -> list[str]:
    registry_path = resource_basis_registry_path(fixture_path)
    if not registry_path.exists():
        return []
    try:
        document = read_json_object(registry_path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return [f"{RESOURCE_BASIS_REGISTRY_FILENAME}: {error}"]

    errors: list[str] = []
    if document.get("schema_version") != "scholar-grade-resource-basis-v1":
        errors.append(f"{RESOURCE_BASIS_REGISTRY_FILENAME}: schema_version must be scholar-grade-resource-basis-v1")
    resources = document.get("resources")
    if not isinstance(resources, list) or not resources:
        errors.append(f"{RESOURCE_BASIS_REGISTRY_FILENAME}: resources must be a non-empty list")
        return errors

    seen: set[str] = set()
    for index, resource in enumerate(resources):
        if not isinstance(resource, dict):
            errors.append(f"{RESOURCE_BASIS_REGISTRY_FILENAME}: resource #{index + 1} must be an object")
            continue
        slug = resource.get("slug")
        label = slug if isinstance(slug, str) and slug else f"resource #{index + 1}"
        if not isinstance(slug, str) or not FIXTURE_ID_RE.match(slug):
            errors.append(f"{RESOURCE_BASIS_REGISTRY_FILENAME}: {label} slug must be lowercase kebab-case")
        elif slug in seen:
            errors.append(f"{RESOURCE_BASIS_REGISTRY_FILENAME}: duplicate resource slug {slug!r}")
        else:
            seen.add(slug)
        for key in ["title", "usage"]:
            if not isinstance(resource.get(key), str) or not str(resource.get(key)).strip():
                errors.append(f"{RESOURCE_BASIS_REGISTRY_FILENAME}: {label} {key} must be a non-empty string")
        url = resource.get("url")
        if not isinstance(url, str) or not HTTP_URL_RE.match(url):
            errors.append(f"{RESOURCE_BASIS_REGISTRY_FILENAME}: {label} url must be an http(s) URL")
        accessed = resource.get("accessed")
        snapshot_sha256 = resource.get("snapshot_sha256")
        has_accessed_date = is_real_iso_date(accessed)
        has_snapshot_hash = isinstance(snapshot_sha256, str) and SHA256_RE.match(snapshot_sha256)
        if not has_accessed_date and not has_snapshot_hash:
            errors.append(
                f"{RESOURCE_BASIS_REGISTRY_FILENAME}: {label} must include accessed YYYY-MM-DD or snapshot_sha256"
            )
    return errors


def resource_basis_errors(fixture_path: Path, fixture: dict[str, Any]) -> list[str]:
    try:
        registry_document = resource_basis_registry_document(fixture_path)
    except (OSError, ValueError, json.JSONDecodeError):
        return []
    if registry_document is None:
        return [
            f"{fixture_identifier(fixture)}: unknown resource_basis {resource!r}"
            for resource in string_list(fixture.get("resource_basis"))
            if resource not in KNOWN_RESOURCE_BASIS
        ]

    registered_slugs = resource_basis_slugs(registry_document)
    return [
        f"{fixture_identifier(fixture)}: resource_basis {resource!r} is not registered in {RESOURCE_BASIS_REGISTRY_FILENAME}"
        for resource in string_list(fixture.get("resource_basis"))
        if resource not in registered_slugs
    ]


def hard_fail_regex_errors(fixture: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key in ["hard_fail_patterns", "semantic_fail_patterns"]:
        for pattern in string_list(fixture.get(key)):
            try:
                re.compile(pattern)
            except re.error:
                errors.append(f"{fixture_identifier(fixture)}: invalid {key} regex {pattern!r}")
    return errors


def regex_pattern_match_errors(
    fixture: dict[str, Any],
    output_text: str,
    fixture_key: str,
    label: str,
) -> list[str]:
    errors: list[str] = []
    for pattern in string_list(fixture.get(fixture_key)):
        if regex_has_asserted_match(pattern, output_text):
            errors.append(f"{fixture_identifier(fixture)}: matches {label} pattern {pattern!r}")
    return errors


def validate_scholar_grade_fixture_document(fixture_path: Path) -> list[str]:
    try:
        document = read_json_object(fixture_path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return [str(error)]

    fixtures = fixture_list(document)
    errors: list[str] = []
    if document.get("schema_version") != "scholar-grade-eval-fixtures-v1":
        errors.append("schema_version must be scholar-grade-eval-fixtures-v1")
    if not fixtures:
        errors.append("fixtures must be a non-empty list of objects")

    errors.extend(duplicate_fixture_id_errors(fixtures))
    errors.extend(resource_basis_registry_errors(fixture_path))
    for fixture in fixtures:
        errors.extend(missing_fixture_keys(fixture))
        errors.extend(invalid_fixture_id_errors(fixture))
        errors.extend(invalid_string_list_errors(fixture))
        errors.extend(score_anchor_errors(fixture))
        errors.extend(invalid_source_access_errors(fixture))
        errors.extend(invalid_score_errors(fixture))
        errors.extend(invalid_boolean_errors(fixture))
        errors.extend(source_packet_errors(fixture_path, fixture))
        errors.extend(resource_basis_errors(fixture_path, fixture))
        errors.extend(hard_fail_regex_errors(fixture))
    return errors


def expected_decision_errors(fixture: dict[str, Any], output_text: str) -> list[str]:
    expected_decision = str(fixture.get("expected_decision", ""))
    if expected_decision and normalized_contains(output_text, expected_decision):
        return []
    return [f"{fixture_identifier(fixture)}: missing expected decision {expected_decision!r}"]


def required_marker_errors(fixture: dict[str, Any], output_text: str) -> list[str]:
    return [
        f"{fixture_identifier(fixture)}: missing required marker {marker!r}"
        for marker in string_list(fixture.get("required_output_markers"))
        if not normalized_contains(output_text, marker)
    ]


def required_source_anchor_errors(fixture: dict[str, Any], output_text: str) -> list[str]:
    return [
        f"{fixture_identifier(fixture)}: missing required source anchor {anchor!r}"
        for anchor in string_list(fixture.get("required_source_anchors"))
        if not normalized_contains(output_text, anchor)
    ]


def required_uncertainty_errors(fixture: dict[str, Any], output_text: str) -> list[str]:
    return [
        f"{fixture_identifier(fixture)}: missing required uncertainty {uncertainty!r}"
        for uncertainty in string_list(fixture.get("required_uncertainties"))
        if not contains_phrase_or_alias(output_text, uncertainty, alias_values(fixture, "required_uncertainty_aliases", uncertainty))
    ]


def disallowed_claim_errors(fixture: dict[str, Any], output_text: str) -> list[str]:
    return [
        f"{fixture_identifier(fixture)}: contains disallowed claim {claim!r}"
        for claim in string_list(fixture.get("disallowed_claims"))
        if contains_asserted_phrase(output_text, claim)
    ]


def allowed_claim_boundary_errors(fixture: dict[str, Any], output_text: str) -> list[str]:
    return [
        f"{fixture_identifier(fixture)}: missing allowed claim boundary {claim!r}"
        for claim in string_list(fixture.get("allowed_claims"))
        if not contains_phrase_or_alias(output_text, claim, alias_values(fixture, "allowed_claim_aliases", claim))
    ]


def hard_fail_pattern_errors(fixture: dict[str, Any], output_text: str) -> list[str]:
    return regex_pattern_match_errors(fixture, output_text, "hard_fail_patterns", "hard fail")


def semantic_fail_pattern_errors(fixture: dict[str, Any], output_text: str) -> list[str]:
    return regex_pattern_match_errors(fixture, output_text, "semantic_fail_patterns", "semantic fail")


def global_hard_fail_pattern_errors(fixture: dict[str, Any], output_text: str) -> list[str]:
    return [
        f"{fixture_identifier(fixture)}: matches global hard fail pattern {pattern!r}"
        for pattern in GLOBAL_HARD_FAIL_PATTERNS
        if contains_asserted_phrase(output_text, pattern)
    ]


def private_external_submission_errors(fixture: dict[str, Any], output_text: str) -> list[str]:
    if fixture.get("source_access_level") != "private-no-external":
        return []
    if regex_has_asserted_match(PRIVATE_EXTERNAL_SUBMISSION_RE.pattern, output_text):
        return [f"{fixture_identifier(fixture)}: private-no-external output claims external submission or search"]
    return []


def hidden_evaluation_material_errors(fixture: dict[str, Any], output_text: str) -> list[str]:
    return [
        f"{fixture_identifier(fixture)}: output exposes hidden evaluation marker {marker!r}"
        for marker in HIDDEN_EVALUATION_OUTPUT_MARKERS
        if marker in output_text
    ]


def phrase_spans(text: str, phrase: str) -> list[tuple[int, int]]:
    if not phrase:
        return []
    pattern = re.compile(re.escape(phrase), flags=re.IGNORECASE)
    return [(match.start(), match.end()) for match in pattern.finditer(text)]


def alias_values(fixture: dict[str, Any], alias_key: str, canonical_phrase: str) -> list[str]:
    aliases = fixture.get(alias_key)
    if not isinstance(aliases, dict):
        return []
    return string_list(aliases.get(canonical_phrase))


def contains_phrase_or_alias(text: str, phrase: str, aliases: list[str]) -> bool:
    return any(normalized_contains(text, candidate) for candidate in [phrase, *aliases])


def rejection_context_prefix(text: str, start: int) -> str:
    line_start = text.rfind("\n", 0, start) + 1
    prefix = text[line_start:start]
    previous_line = previous_nonempty_line(text, line_start)
    if previous_line is not None:
        _previous_start, previous_text = previous_line
        current_prefix = prefix.lstrip()
        previous_text = previous_text.strip()
        if current_prefix.startswith((">", "-", "*")) or previous_text.endswith(":"):
            prefix = f"{previous_text}\n{prefix}"
    return prefix[-CLAIM_CONTEXT_PREFIX_CHARS:]


def is_rejection_context(text: str, start: int) -> bool:
    prefix = rejection_context_prefix(text, start)
    return (
        NEGATED_PHRASE_PREFIX_RE.search(prefix) is not None
        or CLAIM_REJECTION_CONTEXT_RE.search(prefix) is not None
        or is_markdown_table_rejection_context(text, start)
    )


def line_bounds_for_offset(text: str, offset: int) -> tuple[int, int]:
    line_start = text.rfind("\n", 0, offset) + 1
    line_end = text.find("\n", offset)
    if line_end == -1:
        line_end = len(text)
    return line_start, line_end


def previous_nonempty_line(text: str, before_offset: int) -> tuple[int, str] | None:
    cursor = before_offset - 1
    while cursor >= 0:
        line_start = text.rfind("\n", 0, cursor + 1) + 1
        line = text[line_start: cursor + 1]
        if line.strip():
            return line_start, line
        cursor = line_start - 2
    return None


def is_markdown_table_line(line: str) -> bool:
    stripped_line = line.strip()
    return stripped_line.startswith("|") and stripped_line.endswith("|") and stripped_line.count("|") >= 2


def markdown_table_cells(line: str, line_start: int = 0) -> list[tuple[str, int, int]]:
    pipe_positions = [index for index, character in enumerate(line) if character == "|"]
    if len(pipe_positions) < 2:
        return []
    return [
        (
            line[pipe_positions[index] + 1: pipe_positions[index + 1]].strip(),
            line_start + pipe_positions[index] + 1,
            line_start + pipe_positions[index + 1],
        )
        for index in range(len(pipe_positions) - 1)
    ]


def is_markdown_table_separator(line: str) -> bool:
    cells = [cell for cell, _start, _end in markdown_table_cells(line)]
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.strip()) is not None for cell in cells)


def table_header_line_before(text: str, line_start: int) -> str | None:
    cursor = line_start
    for _ in range(20):
        previous = previous_nonempty_line(text, cursor)
        if previous is None:
            return None
        previous_start, previous_line = previous
        if not is_markdown_table_line(previous_line):
            return None
        if is_markdown_table_separator(previous_line):
            header = previous_nonempty_line(text, previous_start)
            if header is None:
                return None
            _header_start, header_line = header
            return header_line if is_markdown_table_line(header_line) else None
        cursor = previous_start
    return None


def cell_index_for_offset(cells: list[tuple[str, int, int]], offset: int) -> int | None:
    for index, (_cell, start, end) in enumerate(cells):
        if start <= offset <= end:
            return index
    return None


def is_markdown_table_rejection_context(text: str, start: int) -> bool:
    line_start, line_end = line_bounds_for_offset(text, start)
    line = text[line_start:line_end]
    if not is_markdown_table_line(line):
        return False
    cell_index = cell_index_for_offset(markdown_table_cells(line, line_start), start)
    if cell_index is None:
        return False
    header_line = table_header_line_before(text, line_start)
    if header_line is None:
        return False
    header_cells = markdown_table_cells(header_line)
    if cell_index >= len(header_cells):
        return False
    header_cell, _start, _end = header_cells[cell_index]
    return CLAIM_REJECTION_CONTEXT_RE.search(header_cell) is not None


def markdown_table_match_crosses_cells(text: str, start: int, end: int) -> bool:
    line_start, line_end = line_bounds_for_offset(text, start)
    if end > line_end:
        return False
    line = text[line_start:line_end]
    if not is_markdown_table_line(line):
        return False
    cells = markdown_table_cells(line, line_start)
    start_cell_index = cell_index_for_offset(cells, start)
    end_cell_index = cell_index_for_offset(cells, max(start, end - 1))
    return start_cell_index is not None and end_cell_index is not None and start_cell_index != end_cell_index


def contains_asserted_phrase(text: str, phrase: str) -> bool:
    return any(not is_rejection_context(text, start) for start, _end in phrase_spans(text, phrase))


def regex_has_asserted_match(pattern: str, text: str) -> bool:
    try:
        compiled_pattern = re.compile(pattern, flags=re.IGNORECASE)
    except re.error:
        return False
    return any(
        not markdown_table_match_crosses_cells(text, match.start(), match.end())
        and not is_rejection_context(text, match.start())
        for match in compiled_pattern.finditer(text)
    )


def validate_output_for_fixture(outputs_dir: Path, fixture: dict[str, Any]) -> list[str]:
    identifier_errors = invalid_fixture_id_errors(fixture)
    if identifier_errors:
        return identifier_errors

    output_path = output_path_for_fixture(outputs_dir, fixture)
    if not output_path.exists():
        return [f"{fixture_identifier(fixture)}: missing output file {output_path.name}"]

    output_text = output_path.read_text(encoding="utf-8")
    return [
        *expected_decision_errors(fixture, output_text),
        *required_marker_errors(fixture, output_text),
        *required_source_anchor_errors(fixture, output_text),
        *required_uncertainty_errors(fixture, output_text),
        *allowed_claim_boundary_errors(fixture, output_text),
        *disallowed_claim_errors(fixture, output_text),
        *hard_fail_pattern_errors(fixture, output_text),
        *semantic_fail_pattern_errors(fixture, output_text),
        *global_hard_fail_pattern_errors(fixture, output_text),
        *private_external_submission_errors(fixture, output_text),
        *hidden_evaluation_material_errors(fixture, output_text),
    ]


def validate_scholar_grade_outputs(fixture_path: Path, outputs_dir: Path) -> list[str]:
    document_errors = validate_scholar_grade_fixture_document(fixture_path)
    if document_errors:
        return document_errors

    document = read_json_object(fixture_path)
    return [
        error
        for fixture in fixture_list(document)
        for error in validate_output_for_fixture(outputs_dir, fixture)
    ]


def manifest_path_for_fixture(manifests_dir: Path, fixture: dict[str, Any]) -> Path:
    return manifests_dir / f"{fixture_identifier(fixture)}.json"


def manifest_missing_key_errors(fixture: dict[str, Any], manifest_document: dict[str, Any]) -> list[str]:
    return [
        f"{fixture_identifier(fixture)}: manifest missing key {key!r}"
        for key in sorted(REQUIRED_MANIFEST_KEYS)
        if key not in manifest_document
    ]


def manifest_string_field_errors(fixture: dict[str, Any], manifest_document: dict[str, Any]) -> list[str]:
    return [
        f"{fixture_identifier(fixture)}: manifest {key} must be a non-empty string"
        for key in sorted(MANIFEST_STRING_KEYS)
        if not isinstance(manifest_document.get(key), str) or not str(manifest_document.get(key)).strip()
    ]


def placeholder_field_errors(
    identifier: str,
    document_label: str,
    document: dict[str, Any],
    keys: set[str],
) -> list[str]:
    return [
        f"{identifier}: {document_label} {key} must not be a TODO placeholder"
        for key in sorted(keys)
        if isinstance(document.get(key), str) and TODO_PLACEHOLDER_RE.match(str(document.get(key)).strip())
    ]


def manifest_identity_errors(fixture: dict[str, Any], manifest_document: dict[str, Any]) -> list[str]:
    identifier = fixture_identifier(fixture)
    expected_source_packet = f"{fixture.get('source_packet')}/source-packet.md"
    expected_skill_file = f"skills/{fixture.get('skill')}/SKILL.md"
    expected_output_file = output_filename_for_fixture(fixture)
    checks = {
        "schema_version": "scholar-grade-run-manifest-v1",
        "fixture_id": identifier,
        "skill": str(fixture.get("skill", "")),
        "source_packet": expected_source_packet,
        "skill_file": expected_skill_file,
        "output_file": expected_output_file,
    }
    return [
        f"{identifier}: manifest {key} must be {expected_value!r}"
        for key, expected_value in checks.items()
        if manifest_document.get(key) != expected_value
    ]


def manifest_capture_metadata_errors(fixture: dict[str, Any], manifest_document: dict[str, Any]) -> list[str]:
    identifier = fixture_identifier(fixture)
    errors: list[str] = []
    if manifest_document.get("capture_mode") not in VALID_CAPTURE_MODES:
        errors.append(f"{identifier}: manifest capture_mode must be one of {sorted(VALID_CAPTURE_MODES)!r}")
    date_value = manifest_document.get("date")
    if not is_real_iso_date(date_value):
        errors.append(f"{identifier}: manifest date must be a real YYYY-MM-DD date")
    if not isinstance(manifest_document.get("external_lookup_permitted"), bool):
        errors.append(f"{identifier}: manifest external_lookup_permitted must be a boolean")
    for key in ["source_packet", "skill_file", "output_file"]:
        errors.extend(relative_path_errors(identifier, key, manifest_document.get(key)))
    errors.extend(private_manifest_policy_errors(fixture, manifest_document))
    return errors


def private_manifest_policy_errors(fixture: dict[str, Any], manifest_document: dict[str, Any]) -> list[str]:
    if fixture.get("source_access_level") != "private-no-external":
        return []

    identifier = fixture_identifier(fixture)
    errors: list[str] = []
    if manifest_document.get("external_lookup_permitted") is not False:
        errors.append(f"{identifier}: private-no-external manifest external_lookup_permitted must be false")
    if manifest_document.get("network_permissions") != "none":
        errors.append(f"{identifier}: private-no-external manifest network_permissions must be 'none'")
    if manifest_document.get("tool_permissions") not in {"none", "local-only"}:
        errors.append(f"{identifier}: private-no-external manifest tool_permissions must be 'none' or 'local-only'")
    return errors


def trace_file_path(root: Path, manifest_document: dict[str, Any]) -> Path:
    return root / str(manifest_document.get("trace_file", ""))


def trace_path_errors(fixture: dict[str, Any], manifest_document: dict[str, Any]) -> list[str]:
    identifier = fixture_identifier(fixture)
    trace_file = manifest_document.get("trace_file")
    errors = [
        error.replace(f"{identifier}: manifest trace_file", f"{identifier}: automated-live-capture manifest trace_file")
        for error in relative_path_errors(identifier, "trace_file", trace_file)
    ]
    trace_sha256 = manifest_document.get("trace_sha256")
    if not isinstance(trace_sha256, str) or not SHA256_RE.match(trace_sha256):
        errors.append(f"{identifier}: automated-live-capture manifest trace_sha256 must be a sha256 hex digest")
    return errors


def trace_hash_errors(root: Path, fixture: dict[str, Any], manifest_document: dict[str, Any]) -> list[str]:
    identifier = fixture_identifier(fixture)
    trace_path = trace_file_path(root, manifest_document)
    if not trace_path.exists():
        return [f"{identifier}: manifest referenced trace file does not exist"]
    expected_hash = sha256_file(trace_path)
    if manifest_document.get("trace_sha256") != expected_hash:
        return [f"{identifier}: manifest trace_sha256 does not match trace file"]
    return []


def trace_document_errors(fixture: dict[str, Any], manifest_document: dict[str, Any], trace_document: dict[str, Any]) -> list[str]:
    identifier = fixture_identifier(fixture)
    errors: list[str] = []
    expected_values = {
        "schema_version": "scholar-grade-trace-v1",
        "fixture_id": identifier,
        "skill": str(fixture.get("skill", "")),
        "model": str(manifest_document.get("model", "")),
    }
    for key, expected_value in expected_values.items():
        if trace_document.get(key) != expected_value:
            errors.append(f"{identifier}: trace {key} must match manifest {key} {expected_value!r}")
    for key in sorted(REQUIRED_TRACE_BOOLEAN_KEYS):
        if trace_document.get(key) is not True:
            errors.append(f"{identifier}: trace {key} must be true")
    for key in sorted(REQUIRED_TRACE_STRING_KEYS):
        if not isinstance(trace_document.get(key), str) or not str(trace_document.get(key)).strip():
            errors.append(f"{identifier}: trace {key} must be a non-empty string")
    if trace_document.get("selected_skill") != fixture.get("skill"):
        errors.append(f"{identifier}: trace selected_skill must match fixture skill {fixture.get('skill')!r}")
    for key in ["tool_permissions", "network_permissions"]:
        if trace_document.get(key) != manifest_document.get(key):
            errors.append(f"{identifier}: trace {key} must match manifest {key} {manifest_document.get(key)!r}")
    for key in sorted(REQUIRED_TRACE_COUNT_KEYS):
        value = trace_document.get(key)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            errors.append(f"{identifier}: trace {key} must be a non-negative integer")
    token_usage = trace_document.get("token_usage")
    if not isinstance(token_usage, dict):
        errors.append(f"{identifier}: trace token_usage must be an object")
        return errors
    for key in sorted(REQUIRED_TRACE_TOKEN_KEYS):
        value = token_usage.get(key)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            errors.append(f"{identifier}: trace token_usage.{key} must be a non-negative integer")
    return errors


def automated_trace_errors(root: Path, fixture: dict[str, Any], manifest_document: dict[str, Any]) -> list[str]:
    if manifest_document.get("capture_mode") != "automated-live-capture":
        return []

    path_errors = trace_path_errors(fixture, manifest_document)
    if path_errors:
        return path_errors

    hash_errors = trace_hash_errors(root, fixture, manifest_document)
    trace_path = trace_file_path(root, manifest_document)
    try:
        trace_document = read_json_object(trace_path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return [*hash_errors, f"{fixture_identifier(fixture)}: trace file {error}"]
    return [
        *hash_errors,
        *trace_document_errors(fixture, manifest_document, trace_document),
    ]


def live_capture_requirement_errors(
    fixture: dict[str, Any],
    manifest_document: dict[str, Any],
    require_live_captures: bool,
) -> list[str]:
    if not require_live_captures:
        return []

    identifier = fixture_identifier(fixture)
    errors: list[str] = []
    if manifest_document.get("capture_mode") not in LIVE_CAPTURE_MODES:
        errors.append(
            f"{identifier}: manifest capture_mode must be manual-live-capture or automated-live-capture when live captures are required"
        )

    model = str(manifest_document.get("model", "")).strip().casefold()
    if not model or model in NON_LIVE_MODEL_VALUES:
        errors.append(f"{identifier}: manifest model must identify the live model when live captures are required")

    interface = str(manifest_document.get("interface", "")).strip().casefold()
    if not interface or interface in NON_LIVE_INTERFACE_VALUES:
        errors.append(
            f"{identifier}: manifest interface must identify the live capture interface when live captures are required"
        )
    return errors


def manifest_hash_errors(
    fixture_path: Path,
    outputs_dir: Path,
    manifests_dir: Path,
    root: Path,
    fixture: dict[str, Any],
    manifest_document: dict[str, Any],
) -> list[str]:
    identifier = fixture_identifier(fixture)
    source_packet = source_packet_document_path(fixture_path, fixture)
    skill_file = root / f"skills/{fixture.get('skill')}/SKILL.md"
    output_file = output_path_for_fixture(outputs_dir, fixture)
    hash_checks = [
        ("source_packet_sha256", source_packet, "source packet"),
        ("skill_file_sha256", skill_file, "skill file"),
        ("output_sha256", output_file, "output file"),
    ]
    errors: list[str] = []
    for key, path, label in hash_checks:
        if not path.exists():
            errors.append(f"{identifier}: manifest referenced {label} does not exist")
            continue
        expected_hash = sha256_file(path)
        if manifest_document.get(key) != expected_hash:
            errors.append(f"{identifier}: manifest {key} does not match {label}")
    prompt_packet_sha256 = manifest_document.get("prompt_packet_sha256")
    if not isinstance(prompt_packet_sha256, str) or SHA256_RE.match(prompt_packet_sha256) is None:
        errors.append(f"{identifier}: manifest prompt_packet_sha256 must be a sha256 hex digest")
    prompt_packet = manifests_dir.parent / "prompts" / f"{identifier}.md"
    if not prompt_packet.exists():
        errors.append(f"{identifier}: manifest referenced prompt packet does not exist")
    elif prompt_packet_sha256 != sha256_file(prompt_packet):
        errors.append(f"{identifier}: manifest prompt_packet_sha256 does not match prompt packet")
    return errors


def structured_result_errors(fixture: dict[str, Any], manifest_document: dict[str, Any]) -> list[str]:
    identifier = fixture_identifier(fixture)
    structured_result = manifest_document.get("structured_result")
    if not isinstance(structured_result, dict):
        return [f"{identifier}: manifest structured_result must be an object"]

    errors = [
        f"{identifier}: structured_result missing key {key!r}"
        for key in sorted(REQUIRED_STRUCTURED_RESULT_KEYS)
        if key not in structured_result
    ]
    if errors:
        return errors

    if structured_result.get("decision") != fixture.get("expected_decision"):
        errors.append(
            f"{identifier}: structured_result.decision must match expected_decision {fixture.get('expected_decision')!r}"
        )
    if structured_result.get("source_access_level") != fixture.get("source_access_level"):
        errors.append(
            f"{identifier}: structured_result.source_access_level must match fixture source_access_level {fixture.get('source_access_level')!r}"
        )
    for key in sorted(STRUCTURED_RESULT_BOOLEAN_KEYS):
        if not isinstance(structured_result.get(key), bool):
            errors.append(f"{identifier}: structured_result.{key} must be a boolean")
    if fixture.get("source_access_level") != "external-lookup-consented" and structured_result.get("external_lookup_used"):
        errors.append(f"{identifier}: structured_result.external_lookup_used must be false")
    if structured_result.get("private_material_submitted"):
        errors.append(f"{identifier}: structured_result.private_material_submitted must be false")
    if structured_result.get("hard_fail_triggered"):
        errors.append(f"{identifier}: structured_result.hard_fail_triggered must be false")
    if structured_result.get("next_action_count") != 1:
        errors.append(f"{identifier}: structured_result.next_action_count must be 1")
    return errors


def validate_run_manifest_for_fixture(
    fixture_path: Path,
    outputs_dir: Path,
    manifests_dir: Path,
    root: Path,
    fixture: dict[str, Any],
    require_live_captures: bool = False,
) -> list[str]:
    manifest_path = manifest_path_for_fixture(manifests_dir, fixture)
    identifier = fixture_identifier(fixture)
    if not manifest_path.exists():
        return [f"{identifier}: missing run manifest {manifest_path.name}"]
    try:
        manifest_document = read_json_object(manifest_path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return [f"{identifier}: {error}"]

    return [
        *manifest_missing_key_errors(fixture, manifest_document),
        *manifest_string_field_errors(fixture, manifest_document),
        *placeholder_field_errors(identifier, "manifest", manifest_document, MANIFEST_PLACEHOLDER_KEYS),
        *manifest_identity_errors(fixture, manifest_document),
        *manifest_capture_metadata_errors(fixture, manifest_document),
        *live_capture_requirement_errors(fixture, manifest_document, require_live_captures),
        *automated_trace_errors(root, fixture, manifest_document),
        *manifest_hash_errors(fixture_path, outputs_dir, manifests_dir, root, fixture, manifest_document),
        *structured_result_errors(fixture, manifest_document),
    ]


def validate_scholar_grade_run_manifests(
    fixture_path: Path,
    outputs_dir: Path,
    manifests_dir: Path,
    root: Path = ROOT,
    require_live_captures: bool = False,
) -> list[str]:
    document_errors = validate_scholar_grade_outputs(fixture_path, outputs_dir)
    if document_errors:
        return document_errors

    document = read_json_object(fixture_path)
    return [
        error
        for fixture in fixture_list(document)
        for error in validate_run_manifest_for_fixture(
            fixture_path,
            outputs_dir,
            manifests_dir,
            root,
            fixture,
            require_live_captures,
        )
    ]


def score_path_for_fixture(scores_dir: Path, fixture: dict[str, Any]) -> Path:
    return scores_dir / f"{fixture_identifier(fixture)}.json"


def numeric_score(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)) and 0 <= value <= 5:
        return float(value)
    return None


def score_missing_key_errors(fixture: dict[str, Any], score_document: dict[str, Any]) -> list[str]:
    return [
        f"{fixture_identifier(fixture)}: score missing key {key!r}"
        for key in sorted(REQUIRED_SCORE_KEYS)
        if key not in score_document
    ]


def score_metadata_errors(fixture: dict[str, Any], score_document: dict[str, Any]) -> list[str]:
    identifier = fixture_identifier(fixture)
    errors: list[str] = []
    expected_values = {
        "schema_version": "scholar-grade-review-score-v1",
        "fixture_id": identifier,
    }
    for key, expected_value in expected_values.items():
        if score_document.get(key) != expected_value:
            errors.append(f"{identifier}: score {key} must be {expected_value!r}")
    for key in ["reviewer", "rationale"]:
        if not isinstance(score_document.get(key), str) or not str(score_document.get(key)).strip():
            errors.append(f"{identifier}: score {key} must be a non-empty string")
    errors.extend(placeholder_field_errors(identifier, "score", score_document, {"reviewer", "rationale"}))
    date_value = score_document.get("date")
    if not is_real_iso_date(date_value):
        errors.append(f"{identifier}: score date must be a real YYYY-MM-DD date")
    if score_document.get("hard_fail_triggered") is not False:
        errors.append(f"{identifier}: score hard_fail_triggered must be false")
    reviewed_output_sha256 = score_document.get("reviewed_output_sha256")
    if not isinstance(reviewed_output_sha256, str) or SHA256_RE.match(reviewed_output_sha256) is None:
        errors.append(f"{identifier}: score reviewed_output_sha256 must be a sha256 hex digest")
    return errors


def score_dimension_errors(fixture: dict[str, Any], score_document: dict[str, Any]) -> list[str]:
    identifier = fixture_identifier(fixture)
    dimension_scores = score_document.get("dimension_scores")
    if not isinstance(dimension_scores, dict):
        return [f"{identifier}: score dimension_scores must be an object"]

    errors: list[str] = []
    expected_dimensions = rubric_dimension_set(fixture)
    actual_dimensions = {key for key in dimension_scores if isinstance(key, str)}
    if actual_dimensions != expected_dimensions:
        errors.append(f"{identifier}: score dimensions must match fixture rubric_dimensions")

    numeric_values: list[float] = []
    for dimension, value in dimension_scores.items():
        score_value = numeric_score(value)
        if score_value is None:
            errors.append(f"{identifier}: score for dimension {dimension!r} must be a number from 0 to 5")
        else:
            numeric_values.append(score_value)
            minimum_score = fixture.get("minimum_score")
            if isinstance(minimum_score, (int, float)) and not isinstance(minimum_score, bool):
                if score_value < float(minimum_score):
                    errors.append(
                        f"{identifier}: score for dimension {dimension!r} {score_value:g} is below minimum_score {minimum_score:g}"
                    )

    if numeric_values:
        average_score = sum(numeric_values) / len(numeric_values)
        minimum_score = fixture.get("minimum_score")
        if isinstance(minimum_score, (int, float)) and not isinstance(minimum_score, bool):
            if average_score < float(minimum_score):
                errors.append(
                    f"{identifier}: average score {average_score:.2f} is below minimum_score {minimum_score:g}"
                )
    return errors


def score_dimension_rationale_errors(fixture: dict[str, Any], score_document: dict[str, Any]) -> list[str]:
    identifier = fixture_identifier(fixture)
    dimension_rationales = score_document.get("dimension_rationales")
    if not isinstance(dimension_rationales, dict):
        return [f"{identifier}: score dimension_rationales must be an object"]

    errors: list[str] = []
    expected_dimensions = rubric_dimension_set(fixture)
    actual_dimensions = {dimension for dimension in dimension_rationales if isinstance(dimension, str)}
    if actual_dimensions != expected_dimensions:
        errors.append(f"{identifier}: score dimension_rationales must match fixture rubric_dimensions")

    for dimension, rationale in dimension_rationales.items():
        if not isinstance(dimension, str):
            continue
        if not isinstance(rationale, str) or not rationale.strip():
            errors.append(f"{identifier}: score dimension_rationales for {dimension!r} must be a non-empty string")
            continue
        if TODO_PLACEHOLDER_RE.match(rationale.strip()):
            errors.append(f"{identifier}: score dimension_rationales for {dimension!r} must not be a TODO placeholder")
    return errors


def score_evidence_list_errors(
    fixture: dict[str, Any],
    score_document: dict[str, Any],
    key: str,
) -> list[str]:
    identifier = fixture_identifier(fixture)
    value = score_document.get(key)
    if not isinstance(value, list) or not value or len(string_list(value)) != len(value):
        return [f"{identifier}: score {key} must be a non-empty string list"]
    return [
        f"{identifier}: score {key} must not contain TODO placeholders"
        for item in value
        if TODO_PLACEHOLDER_RE.match(item.strip())
    ]


def score_evidence_errors(fixture: dict[str, Any], score_document: dict[str, Any]) -> list[str]:
    return [
        *score_evidence_list_errors(fixture, score_document, "evidence_notes"),
        *score_evidence_list_errors(fixture, score_document, "answer_key_findings"),
    ]


def score_output_hash_errors(
    outputs_dir: Path | None,
    fixture: dict[str, Any],
    score_document: dict[str, Any],
) -> list[str]:
    if outputs_dir is None:
        return []

    identifier = fixture_identifier(fixture)
    output_path = output_path_for_fixture(outputs_dir, fixture)
    if not output_path.exists():
        return [f"{identifier}: cannot validate score reviewed_output_sha256 without output file {output_path.name}"]
    expected_hash = sha256_file(output_path)
    if score_document.get("reviewed_output_sha256") != expected_hash:
        return [f"{identifier}: score reviewed_output_sha256 does not match output file"]
    return []


def validate_review_score_for_fixture(
    scores_dir: Path,
    fixture: dict[str, Any],
    outputs_dir: Path | None = None,
) -> list[str]:
    score_path = score_path_for_fixture(scores_dir, fixture)
    identifier = fixture_identifier(fixture)
    if not score_path.exists():
        return [f"{identifier}: missing review score {score_path.name}"]
    try:
        score_document = read_json_object(score_path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return [f"{identifier}: {error}"]
    return [
        *score_missing_key_errors(fixture, score_document),
        *score_metadata_errors(fixture, score_document),
        *score_dimension_errors(fixture, score_document),
        *score_dimension_rationale_errors(fixture, score_document),
        *score_evidence_errors(fixture, score_document),
        *score_output_hash_errors(outputs_dir, fixture, score_document),
    ]


def validate_scholar_grade_review_scores(
    fixture_path: Path,
    scores_dir: Path,
    outputs_dir: Path | None = None,
) -> list[str]:
    document_errors = validate_scholar_grade_fixture_document(fixture_path)
    if document_errors:
        return document_errors

    document = read_json_object(fixture_path)
    return [
        error
        for fixture in fixture_list(document)
        for error in validate_review_score_for_fixture(scores_dir, fixture, outputs_dir)
    ]


def fixture_summary(fixtures: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "total": len(fixtures),
        "ids": [fixture_identifier(fixture) for fixture in fixtures],
        "skill_counts": sorted_counts(
            [str(fixture.get("skill", "")) for fixture in fixtures if fixture.get("skill")]
        ),
        "source_access_counts": sorted_counts(
            [
                str(fixture.get("source_access_level", ""))
                for fixture in fixtures
                if fixture.get("source_access_level")
            ]
        ),
        "resource_basis_counts": sorted_counts(
            [
                resource
                for fixture in fixtures
                for resource in string_list(fixture.get("resource_basis"))
            ]
        ),
        "human_review_required": sum(1 for fixture in fixtures if fixture.get("human_review_required") is True),
    }


def present_output_identifiers(outputs_dir: Path, fixtures: list[dict[str, Any]]) -> list[str]:
    return [
        fixture_identifier(fixture)
        for fixture in fixtures
        if output_path_for_fixture(outputs_dir, fixture).exists()
    ]


def missing_output_identifiers(outputs_dir: Path, fixtures: list[dict[str, Any]]) -> list[str]:
    return [
        fixture_identifier(fixture)
        for fixture in fixtures
        if not output_path_for_fixture(outputs_dir, fixture).exists()
    ]


def output_validation_errors(outputs_dir: Path, fixtures: list[dict[str, Any]]) -> list[str]:
    return [
        error
        for fixture in fixtures
        for error in validate_output_for_fixture(outputs_dir, fixture)
    ]


def output_summary(outputs_dir: Path | None, fixtures: list[dict[str, Any]]) -> dict[str, Any]:
    if outputs_dir is None:
        return {
            "checked": False,
            "present": [],
            "missing": [],
            "validation_errors": [],
        }

    return {
        "checked": True,
        "directory": str(outputs_dir),
        "present": present_output_identifiers(outputs_dir, fixtures),
        "missing": missing_output_identifiers(outputs_dir, fixtures),
        "validation_errors": output_validation_errors(outputs_dir, fixtures),
    }


def present_manifest_identifiers(manifests_dir: Path, fixtures: list[dict[str, Any]]) -> list[str]:
    return [
        fixture_identifier(fixture)
        for fixture in fixtures
        if manifest_path_for_fixture(manifests_dir, fixture).exists()
    ]


def missing_manifest_identifiers(manifests_dir: Path, fixtures: list[dict[str, Any]]) -> list[str]:
    return [
        fixture_identifier(fixture)
        for fixture in fixtures
        if not manifest_path_for_fixture(manifests_dir, fixture).exists()
    ]


def manifest_validation_errors(
    fixture_path: Path,
    outputs_dir: Path,
    manifests_dir: Path,
    root: Path,
    fixtures: list[dict[str, Any]],
    require_live_captures: bool,
) -> list[str]:
    return [
        error
        for fixture in fixtures
        for error in validate_run_manifest_for_fixture(
            fixture_path,
            outputs_dir,
            manifests_dir,
            root,
            fixture,
            require_live_captures,
        )
    ]


def manifest_summary(
    fixture_path: Path,
    outputs_dir: Path | None,
    manifests_dir: Path | None,
    root: Path,
    fixtures: list[dict[str, Any]],
    require_live_captures: bool = False,
) -> dict[str, Any]:
    if manifests_dir is None:
        return {
            "checked": False,
            "require_live_captures": require_live_captures,
            "present": [],
            "missing": [],
            "validation_errors": ["live captures require --manifests-dir"] if require_live_captures else [],
        }
    if outputs_dir is None:
        return {
            "checked": True,
            "require_live_captures": require_live_captures,
            "directory": str(manifests_dir),
            "present": present_manifest_identifiers(manifests_dir, fixtures),
            "missing": missing_manifest_identifiers(manifests_dir, fixtures),
            "validation_errors": ["manifests require --outputs-dir"],
        }
    return {
        "checked": True,
        "require_live_captures": require_live_captures,
        "directory": str(manifests_dir),
        "present": present_manifest_identifiers(manifests_dir, fixtures),
        "missing": missing_manifest_identifiers(manifests_dir, fixtures),
        "validation_errors": manifest_validation_errors(
            fixture_path,
            outputs_dir,
            manifests_dir,
            root,
            fixtures,
            require_live_captures,
        ),
    }


def present_score_identifiers(scores_dir: Path, fixtures: list[dict[str, Any]]) -> list[str]:
    return [
        fixture_identifier(fixture)
        for fixture in fixtures
        if score_path_for_fixture(scores_dir, fixture).exists()
    ]


def missing_score_identifiers(scores_dir: Path, fixtures: list[dict[str, Any]]) -> list[str]:
    return [
        fixture_identifier(fixture)
        for fixture in fixtures
        if not score_path_for_fixture(scores_dir, fixture).exists()
    ]


def score_validation_errors(
    scores_dir: Path,
    fixtures: list[dict[str, Any]],
    outputs_dir: Path | None,
) -> list[str]:
    return [
        error
        for fixture in fixtures
        for error in validate_review_score_for_fixture(scores_dir, fixture, outputs_dir)
    ]


def score_summary(
    scores_dir: Path | None,
    fixtures: list[dict[str, Any]],
    outputs_dir: Path | None,
) -> dict[str, Any]:
    if scores_dir is None:
        return {
            "checked": False,
            "present": [],
            "missing": [],
            "validation_errors": [],
        }
    return {
        "checked": True,
        "directory": str(scores_dir),
        "present": present_score_identifiers(scores_dir, fixtures),
        "missing": missing_score_identifiers(scores_dir, fixtures),
        "validation_errors": score_validation_errors(scores_dir, fixtures, outputs_dir),
    }


def score_anchor_entries(fixture: dict[str, Any]) -> list[str]:
    score_anchors = fixture.get("score_anchors")
    if not isinstance(score_anchors, dict):
        return []

    entries: list[str] = []
    for dimension in string_list(fixture.get("rubric_dimensions")):
        dimension_anchors = score_anchors.get(dimension)
        if not isinstance(dimension_anchors, dict):
            continue
        for level in sorted(REQUIRED_SCORE_ANCHOR_LEVELS, key=int):
            anchor = dimension_anchors.get(level)
            if isinstance(anchor, str) and anchor.strip():
                entries.append(f"{dimension} {level}: {anchor.strip()}")
    return entries


def fixture_case_report(fixture: dict[str, Any], outputs_dir: Path | None) -> dict[str, Any]:
    output_path = output_path_for_fixture(outputs_dir, fixture) if outputs_dir else None
    return {
        "id": fixture_identifier(fixture),
        "skill": str(fixture.get("skill", "")),
        "prompt": str(fixture.get("prompt", "")),
        "source_packet": str(fixture.get("source_packet", "")),
        "source_access_level": str(fixture.get("source_access_level", "")),
        "resource_basis": string_list(fixture.get("resource_basis")),
        "expected_decision": str(fixture.get("expected_decision", "")),
        "required_output_markers": string_list(fixture.get("required_output_markers")),
        "required_source_anchors": string_list(fixture.get("required_source_anchors")),
        "required_uncertainties": string_list(fixture.get("required_uncertainties")),
        "allowed_claims": string_list(fixture.get("allowed_claims")),
        "disallowed_claims": string_list(fixture.get("disallowed_claims")),
        "hard_fail_patterns": string_list(fixture.get("hard_fail_patterns")),
        "semantic_fail_patterns": string_list(fixture.get("semantic_fail_patterns")),
        "rubric_dimensions": string_list(fixture.get("rubric_dimensions")),
        "score_anchors": score_anchor_entries(fixture),
        "minimum_score": fixture.get("minimum_score"),
        "human_review_required": bool(fixture.get("human_review_required")),
        "output_file": output_filename_for_fixture(fixture),
        "output_path": str(output_path) if output_path else None,
        "captured_output_checked": bool(output_path and output_path.exists()),
        "validation_errors": validate_output_for_fixture(outputs_dir, fixture) if outputs_dir else [],
    }


def build_scholar_grade_report(
    fixture_path: Path,
    outputs_dir: Path | None = None,
    manifests_dir: Path | None = None,
    scores_dir: Path | None = None,
    root: Path = ROOT,
    require_live_captures: bool = False,
    fixture_ids: list[str] | None = None,
) -> dict[str, Any]:
    document_errors = validate_scholar_grade_fixture_document(fixture_path)
    document = read_json_object(fixture_path) if not document_errors else {"fixtures": []}
    fixtures, fixture_filter_errors = select_fixtures(fixture_list(document), fixture_ids)
    return {
        "schema_version": "scholar-grade-eval-harness-v1",
        "execution_mode": "deterministic-local",
        "source": {
            "fixtures": str(fixture_path),
            "outputs_dir": str(outputs_dir) if outputs_dir else None,
            "manifests_dir": str(manifests_dir) if manifests_dir else None,
            "scores_dir": str(scores_dir) if scores_dir else None,
            "require_live_captures": require_live_captures,
            "fixture_ids": fixture_ids or [],
        },
        "fixtures": {
            **fixture_summary(fixtures),
            "validation_errors": [*document_errors, *fixture_filter_errors],
        },
        "outputs": output_summary(outputs_dir, fixtures),
        "manifests": manifest_summary(fixture_path, outputs_dir, manifests_dir, root, fixtures, require_live_captures),
        "scores": score_summary(scores_dir, fixtures, outputs_dir),
        "limits": LIMITS,
        "manual_review_expectations": MANUAL_REVIEW_EXPECTATIONS,
        "cases": [fixture_case_report(fixture, outputs_dir) for fixture in fixtures],
    }


def inline_code(value: str) -> str:
    delimiter = "``" if "`" in value else "`"
    return f"{delimiter}{value}{delimiter}"


def inline_code_list(values: list[str]) -> str:
    return ", ".join(inline_code(value) for value in values) if values else "None"


def quote_markdown(text: str) -> list[str]:
    return [f"> {line}" for line in (text.splitlines() or [""])]


def format_markdown_scorecard(report: dict[str, Any]) -> str:
    lines = [
        "# Scholar-Grade Evaluation Harness",
        "",
        f"Execution mode: `{report['execution_mode']}`",
        "",
        "## Limits",
        *[f"- {limit}" for limit in report["limits"]],
        "",
        "## Scholar-grade rubric",
        "- Score each rubric dimension from 0 to 5.",
        "- Any hard-fail pattern, fabricated verification, or privacy leak fails the case regardless of score.",
        "- Minimum score is required for every rubric dimension and for the average after hard-fail checks pass.",
        "",
        "## Manual review expectations",
        *[f"- {expectation}" for expectation in report["manual_review_expectations"]],
        "",
        "## Coverage",
        f"- Fixture count: {report['fixtures']['total']}",
        f"- Skills: {json.dumps(report['fixtures']['skill_counts'], sort_keys=True)}",
        f"- Source access: {json.dumps(report['fixtures']['source_access_counts'], sort_keys=True)}",
        f"- Resource basis: {json.dumps(report['fixtures']['resource_basis_counts'], sort_keys=True)}",
        f"- Human review required: {report['fixtures']['human_review_required']}",
        "",
        "## Captured outputs",
        f"- Checked: {str(report['outputs']['checked']).lower()}",
        f"- Present: {', '.join(report['outputs']['present']) or 'None'}",
        f"- Missing: {', '.join(report['outputs']['missing']) or 'None'}",
        "",
        "## Run manifests",
        f"- Checked: {str(report['manifests']['checked']).lower()}",
        f"- Live captures required: {str(report['manifests']['require_live_captures']).lower()}",
        f"- Present: {', '.join(report['manifests']['present']) or 'None'}",
        f"- Missing: {', '.join(report['manifests']['missing']) or 'None'}",
        f"- Validation errors: {inline_code_list(report['manifests']['validation_errors'])}",
        "",
        "## Review scores",
        f"- Checked: {str(report['scores']['checked']).lower()}",
        f"- Present: {', '.join(report['scores']['present']) or 'None'}",
        f"- Missing: {', '.join(report['scores']['missing']) or 'None'}",
        f"- Validation errors: {inline_code_list(report['scores']['validation_errors'])}",
        "",
        "## Fixture scorecards",
    ]
    for case in report["cases"]:
        lines.extend(
            [
                "",
                f"### {case['id']}",
                f"- Skill: `{case['skill']}`",
                f"- Source packet: `{case['source_packet']}`",
                f"- Source access level: `{case['source_access_level']}`",
                f"- Resource basis: {inline_code_list(case['resource_basis'])}",
                f"- Expected decision: `{case['expected_decision']}`",
                f"- Required markers: {inline_code_list(case['required_output_markers'])}",
                f"- Required source anchors: {inline_code_list(case['required_source_anchors'])}",
                f"- Required uncertainties: {inline_code_list(case['required_uncertainties'])}",
                f"- Allowed claims: {inline_code_list(case['allowed_claims'])}",
                f"- Disallowed claims: {inline_code_list(case['disallowed_claims'])}",
                f"- Hard-fail patterns: {inline_code_list(case['hard_fail_patterns'])}",
                f"- Semantic fail patterns: {inline_code_list(case['semantic_fail_patterns'])}",
                f"- Rubric dimensions: {inline_code_list(case['rubric_dimensions'])}",
                f"- Score anchors: {inline_code_list(case['score_anchors'])}",
                f"- Minimum score: `{case['minimum_score']}`",
                f"- Human review required: `{str(case['human_review_required']).lower()}`",
                f"- Validation errors: {inline_code_list(case['validation_errors'])}",
                "",
                "Prompt:",
                *quote_markdown(case["prompt"]),
            ]
        )
    return "\n".join(lines) + "\n"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", type=Path, required=True, help="Scholar-grade fixture JSON file.")
    parser.add_argument(
        "--outputs-dir",
        type=Path,
        help="Optional directory containing one captured Markdown output per fixture id.",
    )
    parser.add_argument(
        "--manifests-dir",
        type=Path,
        help="Optional directory containing one run manifest JSON file per fixture id.",
    )
    parser.add_argument(
        "--scores-dir",
        type=Path,
        help="Optional directory containing one review score JSON file per fixture id.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=ROOT,
        help="Repository root used to validate skill-file manifest hashes.",
    )
    parser.add_argument(
        "--require-live-captures",
        action="store_true",
        help="Fail manifest validation unless captures are manual-live-capture or automated-live-capture runs with a live model and interface.",
    )
    parser.add_argument(
        "--fixture-id",
        action="append",
        help="Limit validation/reporting to one fixture id. Repeat to validate an incremental live-capture subset.",
    )
    parser.add_argument(
        "--format",
        choices=["json", "markdown"],
        default="json",
        help="Output JSON for automation or Markdown for reviewer scorecards.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress report output and return only the validation exit code.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        report = build_scholar_grade_report(
            args.fixtures,
            args.outputs_dir,
            args.manifests_dir,
            args.scores_dir,
            args.root.resolve(),
            args.require_live_captures,
            args.fixture_id,
        )
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"errors": [str(error)]}, indent=2))
        return 1

    if not args.quiet:
        if args.format == "markdown":
            print(format_markdown_scorecard(report), end="")
        else:
            print(json.dumps(report, indent=2))

    has_errors = bool(
        report["fixtures"]["validation_errors"]
        or report["outputs"]["validation_errors"]
        or report["manifests"]["validation_errors"]
        or report["scores"]["validation_errors"]
    )
    return 1 if has_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
