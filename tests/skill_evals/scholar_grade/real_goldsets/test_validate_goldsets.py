"""Tests for real-source gold-set validation."""
from __future__ import annotations

import json
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


def minimum_failure_check(identifier: str) -> dict[str, str]:
    return {
        "id": identifier,
        "question": f"PLACEHOLDER: reviewer question for {identifier}",
        "failure_if": f"PLACEHOLDER: failure condition for {identifier}",
        "passes_if": f"PLACEHOLDER: pass condition for {identifier}",
        "evidence_basis": f"PLACEHOLDER: MVP source basis for {identifier}",
    }


def check_result(identifier: str, outcome: str = "pass") -> dict[str, str]:
    return {
        "check_id": identifier,
        "outcome": outcome,
        "rationale": f"PLACEHOLDER: scoring rationale for {identifier}",
        "evidence_basis": f"PLACEHOLDER: reviewed source basis for {identifier}",
    }


def candidate_output_scorecard(*check_identifiers: str) -> dict[str, object]:
    return {
        "output_id": "candidate-output",
        "output_label": "PLACEHOLDER: candidate output label",
        "output_text": "PLACEHOLDER: candidate skill output for the visible prompt",
        "score_basis": "PLACEHOLDER: bounded source basis used for scoring",
        "check_results": [check_result(identifier) for identifier in check_identifiers],
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


def remove_placeholder_text(value: object) -> object:
    if isinstance(value, str):
        return value.replace("PLACEHOLDER: ", "Reviewed ")
    if isinstance(value, list):
        return [remove_placeholder_text(item) for item in value]
    if isinstance(value, dict):
        return {key: remove_placeholder_text(child) for key, child in value.items()}
    return value


def valid_active_goldset() -> dict[str, object]:
    return {
        **remove_placeholder_text(valid_inactive_goldset()),
        "status": "active",
        "last_reviewed_date": "2026-06-03",
    }


class RealGoldsetValidationTests(unittest.TestCase):
    def test_schema_matches_author_and_waiver_validator_boundaries(self) -> None:
        schema_path = Path(__file__).resolve().parent / "goldset.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        source_definition = schema["$defs"]["source"]

        self.assertEqual(source_definition["properties"]["authors"]["minItems"], 1)
        self.assertIn("search_log_scope_waiver", schema["properties"])
        self.assertIn("searchLogScopeWaiver", schema["$defs"])

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

    def test_candidate_output_scorecards_must_cover_minimum_failure_checks(self) -> None:
        goldset = {
            **valid_inactive_goldset(),
            "minimum_failure_checks": [
                minimum_failure_check("broad-overclaim"),
                minimum_failure_check("clinical-proof"),
            ],
            "candidate_output_scorecards": [
                candidate_output_scorecard("broad-overclaim"),
            ],
        }

        errors = validate_goldset_document(goldset)

        self.assertIn(
            "candidate_output_scorecards[0] is missing check results for "
            "minimum_failure_checks: clinical-proof",
            errors,
        )

    def test_candidate_output_scorecards_accept_full_minimum_check_coverage(self) -> None:
        goldset = {
            **valid_inactive_goldset(),
            "minimum_failure_checks": [
                minimum_failure_check("broad-overclaim"),
                minimum_failure_check("clinical-proof"),
            ],
            "candidate_output_scorecards": [
                candidate_output_scorecard("broad-overclaim", "clinical-proof"),
            ],
        }

        self.assertEqual(validate_goldset_document(goldset), [])

    def test_active_search_log_scope_waiver_must_be_explicit(self) -> None:
        goldset = {
            **valid_active_goldset(),
            "search_log_scope_waiver": {
                "waiver_status": "draft",
                "approved_by": "Reviewer",
                "approval_date": "2026-06-03",
                "waived_requirement": "Executed search-log reconstruction is deferred.",
                "scope_limit": "Active fixture is limited to the reviewed MVP packet.",
                "residual_risk": "Search completeness is not independently reproducible.",
            },
        }

        errors = validate_goldset_document(goldset)

        self.assertIn(
            "active gold set search_log_scope_waiver.waiver_status must be 'approved'",
            errors,
        )

    def test_active_search_log_scope_waiver_accepts_approved_boundary(self) -> None:
        goldset = {
            **valid_active_goldset(),
            "search_log_scope_waiver": {
                "waiver_status": "approved",
                "approved_by": "Reviewer",
                "approval_date": "2026-06-03",
                "waived_requirement": "Executed search-log reconstruction is deferred.",
                "scope_limit": "Active fixture is limited to the reviewed MVP packet.",
                "residual_risk": "Search completeness is not independently reproducible.",
            },
        }

        self.assertEqual(validate_goldset_document(goldset), [])

    def test_polyvagal_draft_scores_every_minimum_failure_check(self) -> None:
        fixture_path = (
            Path(__file__).resolve().parent
            / "polyvagal-theory-consensus-overstatement.draft.json"
        )
        document = json.loads(fixture_path.read_text(encoding="utf-8"))

        errors = validate_goldset_document(document)
        scorecards = document.get("candidate_output_scorecards")

        self.assertEqual(errors, [])
        self.assertIsInstance(scorecards, list)
        self.assertGreaterEqual(len(scorecards), 2)


if __name__ == "__main__":
    unittest.main()
