"""Tests for real-source gold-set validation."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_goldsets import validate_goldset_document


def valid_source(role: str = "gold") -> dict[str, object]:
    return {
        "source_id": f"{role}-source",
        "title": "PLACEHOLDER: human-reviewed source title",
        "authors": ["PLACEHOLDER: author or authoring body"],
        "year": "PLACEHOLDER: publication year if known",
        "locator_or_access_note": "PLACEHOLDER: DOI, stable URL, archive note, or access note",
        "role": role,
    }


def expectation(identifier: str) -> dict[str, str]:
    return {
        "id": identifier,
        "expectation": "PLACEHOLDER: human-reviewed expectation",
        "evidence_basis": "PLACEHOLDER: source IDs and human reviewer basis",
    }


def valid_inactive_goldset() -> dict[str, object]:
    return {
        "schema_version": "real-source-goldset-v1",
        "status": "inactive-template",
        "goldset_id": "example-template",
        "domain": "PLACEHOLDER: scholarly domain",
        "task_type": "retrieval",
        "visible_prompt": "PLACEHOLDER: prompt shown to the skill",
        "allowed_tools": ["PLACEHOLDER: allowed tool"],
        "network_policy": "PLACEHOLDER: network policy",
        "gold_sources": [valid_source("gold")],
        "acceptable_sources": [valid_source("acceptable")],
        "decoy_sources": [{**valid_source("decoy"), "decoy_reason": "PLACEHOLDER: why this is a decoy"}],
        "disallowed_sources": [valid_source("disallowed")],
        "required_distinctions": [expectation("distinction-1")],
        "must_support": [expectation("support-1")],
        "must_reject": [expectation("reject-1")],
        "must_remain_uncertain": [expectation("uncertain-1")],
        "citation_audit_expectations": [expectation("citation-audit-1")],
        "field_state_note": "PLACEHOLDER: human-reviewed field-state note",
        "human_review_required": True,
        "reviewer_notes": "PLACEHOLDER: reviewer notes",
        "last_reviewed_date": "PLACEHOLDER: YYYY-MM-DD after human review",
        "source_access_notes": "PLACEHOLDER: access limits and review basis",
    }


class RealGoldsetValidationTests(unittest.TestCase):
    def test_inactive_templates_may_keep_placeholders(self) -> None:
        self.assertEqual(validate_goldset_document(valid_inactive_goldset()), [])

    def test_active_goldsets_reject_unreviewed_or_unsafe_content(self) -> None:
        active_goldset = {
            **valid_inactive_goldset(),
            "status": "active",
            "human_review_required": False,
            "must_support": [{"id": "support-1", "expectation": "PLACEHOLDER: claim"}],
            "decoy_sources": [valid_source("decoy")],
            "reviewer_notes": "This private unpublished manuscript text should not be stored here.",
        }

        errors = validate_goldset_document(active_goldset)

        self.assertTrue(any("active gold set contains placeholder" in error for error in errors))
        self.assertTrue(any("human_review_required must be true" in error for error in errors))
        self.assertTrue(any("decoy_reason" in error for error in errors))
        self.assertTrue(any("evidence_basis" in error for error in errors))
        self.assertTrue(any("private unpublished manuscript text" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
