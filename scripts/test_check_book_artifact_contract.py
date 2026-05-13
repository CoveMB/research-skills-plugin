"""Unit tests for the book artifact contract checker."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


SCRIPT = Path(__file__).resolve().parent / "check_book_artifact_contract.py"


def run_checker(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--path", str(root)],
        check=False,
        capture_output=True,
        text=True,
    )


def write_schema(root: Path) -> None:
    schema_dir = root / "shared" / "contracts" / "book"
    schema_dir.mkdir(parents=True, exist_ok=True)
    (schema_dir / "book_artifact.schema.json").write_text(
        json.dumps(
            {
                "type": "object",
                "additionalProperties": False,
                "required": ["schema_version", "artifact_type", "project_title"],
                "properties": {
                    "schema_version": {"const": "book-artifact-v1"},
                    "artifact_type": {
                        "enum": [
                            "claim_evidence_ledger",
                            "chapter_brief",
                            "book_proposal",
                            "source_discovery_log",
                            "methodology_source_audit",
                            "annotated_bibliography",
                            "case_study_dossier",
                            "peer_review_report",
                            "style_sheet",
                        ]
                    },
                    "project_title": {"type": "string", "minLength": 1},
                    "claims": {
                        "type": "array",
                        "minItems": 1,
                        "items": {
                            "type": "object",
                            "required": ["claim", "evidence_status", "safer_wording"],
                            "properties": {
                                "claim": {"type": "string", "minLength": 1},
                                "evidence_status": {"type": "string", "minLength": 1},
                                "safer_wording": {"type": "string", "minLength": 1},
                            },
                        },
                    },
                    "section_outline": {
                        "type": "array",
                        "minItems": 1,
                        "items": {
                            "type": "object",
                            "required": ["section", "function", "key_claim"],
                            "properties": {
                                "section": {"type": "string", "minLength": 1},
                                "function": {"type": "string", "minLength": 1},
                                "key_claim": {"type": "string", "minLength": 1},
                            },
                        },
                    },
                    "comparable_titles": {
                        "type": "array",
                        "minItems": 1,
                        "items": {
                            "type": "object",
                            "required": ["title", "verification_status"],
                            "properties": {
                                "title": {"type": "string", "minLength": 1},
                                "verification_status": {
                                    "enum": ["verified", "unverified", "needed"]
                                },
                                "source_pointer": {"type": "string", "minLength": 1},
                            },
                            "allOf": [
                                {
                                    "if": {
                                        "properties": {
                                            "verification_status": {"const": "verified"}
                                        }
                                    },
                                    "then": {"required": ["source_pointer"]},
                                }
                            ],
                        },
                    },
                    "search_log": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["useful_results"],
                            "properties": {
                                "useful_results": {"type": "integer", "minimum": 0},
                            },
                        },
                    },
                    "source_audit_rows": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["source", "source_type", "method_evidence", "credibility", "bias_risk", "can_support", "cannot_support", "use_recommendation"],
                            "properties": {
                                "source": {"type": "string", "minLength": 1},
                                "source_type": {"type": "string", "minLength": 1},
                                "method_evidence": {"type": "string", "minLength": 1},
                                "credibility": {"type": "string", "minLength": 1},
                                "bias_risk": {"enum": ["low", "medium", "high", "critical"]},
                                "can_support": {"type": "string", "minLength": 1},
                                "cannot_support": {"type": "string", "minLength": 1},
                                "use_recommendation": {"type": "string", "minLength": 1},
                            },
                        },
                    },
                    "bibliography_annotations": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["source", "annotation_basis", "source_type", "main_argument", "method_evidence", "best_use", "limitations", "chapter_placement", "citation_details_needed"],
                            "properties": {
                                "source": {"type": "string", "minLength": 1},
                                "annotation_basis": {"type": "string", "minLength": 1},
                                "source_type": {"type": "string", "minLength": 1},
                                "main_argument": {"type": "string", "minLength": 1},
                                "method_evidence": {"type": "string", "minLength": 1},
                                "best_use": {"type": "string", "minLength": 1},
                                "limitations": {"type": "string", "minLength": 1},
                                "chapter_placement": {"type": "string", "minLength": 1},
                                "citation_details_needed": {"type": "string", "minLength": 1},
                            },
                        },
                    },
                    "claim_needing_case": {"type": "string", "minLength": 1},
                    "case_selection_logic": {"type": "string", "minLength": 1},
                    "case_dossiers": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["case", "function", "supports", "challenges", "source_base", "selection_risk", "generalization_limit", "chapter_use"],
                            "properties": {
                                "case": {"type": "string", "minLength": 1},
                                "function": {"type": "string", "minLength": 1},
                                "supports": {"type": "string", "minLength": 1},
                                "challenges": {"type": "string", "minLength": 1},
                                "source_base": {"type": "string", "minLength": 1},
                                "selection_risk": {"type": "string", "minLength": 1},
                                "generalization_limit": {"type": "string", "minLength": 1},
                                "chapter_use": {"type": "string", "minLength": 1},
                            },
                        },
                    },
                    "counter_cases": {
                        "type": "array",
                        "items": {"type": "string", "minLength": 1},
                    },
                    "safer_case_claims": {
                        "type": "array",
                        "items": {"type": "string", "minLength": 1},
                    },
                    "charitable_restatement": {"type": "string", "minLength": 1},
                    "review_objections": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["objection", "source_of_challenge", "severity", "why_it_matters", "falsifying_evidence", "revision_strategy"],
                            "properties": {
                                "objection": {"type": "string", "minLength": 1},
                                "source_of_challenge": {"type": "string", "minLength": 1},
                                "severity": {"enum": ["low", "medium", "high", "critical"]},
                                "why_it_matters": {"type": "string", "minLength": 1},
                                "falsifying_evidence": {"type": "string", "minLength": 1},
                                "revision_strategy": {"type": "string", "minLength": 1},
                            },
                        },
                    },
                    "rival_explanations": {
                        "type": "array",
                        "items": {"type": "string", "minLength": 1},
                    },
                    "missing_literatures": {
                        "type": "array",
                        "items": {"type": "string", "minLength": 1},
                    },
                    "claims_to_narrow": {
                        "type": "array",
                        "items": {"type": "string", "minLength": 1},
                    },
                    "revision_priorities": {
                        "type": "array",
                        "items": {"type": "string", "minLength": 1},
                    },
                    "style_rules": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["rule", "reason", "example"],
                            "properties": {
                                "rule": {"type": "string", "minLength": 1},
                                "reason": {"type": "string", "minLength": 1},
                                "example": {"type": "string", "minLength": 1},
                            },
                        },
                    },
                    "voice_constraints": {
                        "type": "array",
                        "items": {"type": "string", "minLength": 1},
                    },
                    "terms_to_preserve": {
                        "type": "array",
                        "items": {"type": "string", "minLength": 1},
                    },
                    "claim_language_guidance": {
                        "type": "array",
                        "items": {"type": "string", "minLength": 1},
                    },
                    "new_factual_claims_policy": {"type": "string", "minLength": 1},
                },
                "allOf": [
                    {
                        "if": {"properties": {"artifact_type": {"const": "claim_evidence_ledger"}}},
                        "then": {"required": ["claims"]},
                    },
                    {
                        "if": {"properties": {"artifact_type": {"const": "chapter_brief"}}},
                        "then": {"required": ["section_outline"]},
                    },
                    {
                        "if": {"properties": {"artifact_type": {"const": "book_proposal"}}},
                        "then": {"required": ["comparable_titles"]},
                    },
                    {
                        "if": {"properties": {"artifact_type": {"const": "methodology_source_audit"}}},
                        "then": {"required": ["source_audit_rows"]},
                    },
                    {
                        "if": {"properties": {"artifact_type": {"const": "annotated_bibliography"}}},
                        "then": {"required": ["bibliography_annotations"]},
                    },
                    {
                        "if": {"properties": {"artifact_type": {"const": "case_study_dossier"}}},
                        "then": {"required": ["claim_needing_case", "case_selection_logic", "case_dossiers", "counter_cases", "safer_case_claims"]},
                    },
                    {
                        "if": {"properties": {"artifact_type": {"const": "peer_review_report"}}},
                        "then": {"required": ["charitable_restatement", "review_objections", "rival_explanations", "missing_literatures", "claims_to_narrow", "revision_priorities"]},
                    },
                    {
                        "if": {"properties": {"artifact_type": {"const": "style_sheet"}}},
                        "then": {"required": ["style_rules", "voice_constraints", "terms_to_preserve", "claim_language_guidance", "new_factual_claims_policy"]},
                    },
                ],
            }
        ),
        encoding="utf-8",
    )


def write_example(root: Path, name: str, payload: dict) -> None:
    examples_dir = root / "examples" / "book_artifacts"
    examples_dir.mkdir(parents=True, exist_ok=True)
    (examples_dir / name).write_text(json.dumps(payload), encoding="utf-8")


def valid_claim_ledger() -> dict:
    return {
        "schema_version": "book-artifact-v1",
        "artifact_type": "claim_evidence_ledger",
        "project_title": "Fixture Book",
        "claims": [
            {
                "claim": "The draft makes a causal claim.",
                "evidence_status": "needs_stronger_evidence",
                "safer_wording": "The draft can frame this as a plausible causal pathway.",
            }
        ],
    }


def valid_chapter_brief() -> dict:
    return {
        "schema_version": "book-artifact-v1",
        "artifact_type": "chapter_brief",
        "project_title": "Fixture Book",
        "section_outline": [
            {
                "section": "Introduction",
                "function": "Frame the chapter problem.",
                "key_claim": "The chapter needs a clear opening claim.",
            }
        ],
    }


def valid_book_proposal() -> dict:
    return {
        "schema_version": "book-artifact-v1",
        "artifact_type": "book_proposal",
        "project_title": "Fixture Book",
        "comparable_titles": [
            {
                "title": "Unverified Comparable",
                "verification_status": "unverified",
            }
        ],
    }


def valid_source_discovery_log() -> dict:
    return {
        "schema_version": "book-artifact-v1",
        "artifact_type": "source_discovery_log",
        "project_title": "Fixture Book",
        "search_log": [
            {
                "useful_results": 0,
            }
        ],
    }


def valid_methodology_source_audit() -> dict:
    return {
        "schema_version": "book-artifact-v1",
        "artifact_type": "methodology_source_audit",
        "project_title": "Fixture Book",
        "source_audit_rows": [
            {
                "source": "Fixture source",
                "source_type": "peer-reviewed empirical article",
                "method_evidence": "Abstract only; methods unavailable.",
                "credibility": "contextual",
                "bias_risk": "medium",
                "can_support": "Topic relevance only.",
                "cannot_support": "Strong causal or generalizable claim.",
                "use_recommendation": "Request method details before relying on it.",
            }
        ],
    }


def valid_annotated_bibliography() -> dict:
    return {
        "schema_version": "book-artifact-v1",
        "artifact_type": "annotated_bibliography",
        "project_title": "Fixture Book",
        "bibliography_annotations": [
            {
                "source": "Fixture source",
                "annotation_basis": "Citation and abstract only.",
                "source_type": "article",
                "main_argument": "Fixture-level argument summary.",
                "method_evidence": "Method not visible in this fixture.",
                "best_use": "Background orientation.",
                "limitations": "Cannot infer full argument from the fixture.",
                "chapter_placement": "Chapter 1",
                "citation_details_needed": "Verify metadata before citing.",
            }
        ],
    }


def valid_case_study_dossier() -> dict:
    return {
        "schema_version": "book-artifact-v1",
        "artifact_type": "case_study_dossier",
        "project_title": "Fixture Book",
        "claim_needing_case": "The chapter needs a bounded illustrative case.",
        "case_selection_logic": "Fixture case selected to test schema shape only.",
        "case_dossiers": [
            {
                "case": "Fixture case",
                "function": "illustrative example",
                "supports": "Shows how a claim might be introduced.",
                "challenges": "Does not establish generality.",
                "source_base": "Fixture notes only.",
                "selection_risk": "Cherry-picking risk unresolved.",
                "generalization_limit": "Do not generalize beyond fixture scope.",
                "chapter_use": "Use as placeholder only.",
            }
        ],
        "counter_cases": ["Add a real counter-case before handoff."],
        "safer_case_claims": ["This case can illustrate, not prove, the claim."],
    }


def valid_peer_review_report() -> dict:
    return {
        "schema_version": "book-artifact-v1",
        "artifact_type": "peer_review_report",
        "project_title": "Fixture Book",
        "charitable_restatement": "The fixture thesis is strongest when narrowly framed.",
        "review_objections": [
            {
                "objection": "The evidence base is too thin.",
                "source_of_challenge": "Methodological scope",
                "severity": "high",
                "why_it_matters": "The claim may overreach the visible evidence.",
                "falsifying_evidence": "A stronger source base could undermine the objection.",
                "revision_strategy": "Narrow the claim and add evidence.",
            }
        ],
        "rival_explanations": ["Alternative mechanism not yet ruled out."],
        "missing_literatures": ["Relevant specialist literature not checked."],
        "claims_to_narrow": ["Narrow broad causal phrasing."],
        "revision_priorities": ["Resolve high-severity objection first."],
    }


def valid_style_sheet() -> dict:
    return {
        "schema_version": "book-artifact-v1",
        "artifact_type": "style_sheet",
        "project_title": "Fixture Book",
        "style_rules": [
            {
                "rule": "Preserve uncertainty where evidence is incomplete.",
                "reason": "The style sheet must not polish weak evidence into certainty.",
                "example": "Use 'suggests' rather than 'proves' for fixture claims.",
            }
        ],
        "voice_constraints": ["Keep authorial voice concise and precise."],
        "terms_to_preserve": ["fixture term"],
        "claim_language_guidance": ["Mark new factual claims for verification."],
        "new_factual_claims_policy": "No new factual claims without user approval and verification.",
    }


def write_valid_coverage_examples(root: Path, *, skip: set[str] | None = None) -> None:
    skipped = skip or set()
    examples = {
        "claim_evidence_ledger": ("claim-ledger.json", valid_claim_ledger()),
        "chapter_brief": ("chapter-brief.json", valid_chapter_brief()),
        "book_proposal": ("book-proposal.json", valid_book_proposal()),
        "source_discovery_log": ("source-discovery-log.json", valid_source_discovery_log()),
        "methodology_source_audit": ("methodology-source-audit.json", valid_methodology_source_audit()),
        "annotated_bibliography": ("annotated-bibliography.json", valid_annotated_bibliography()),
        "case_study_dossier": ("case-study-dossier.json", valid_case_study_dossier()),
        "peer_review_report": ("peer-review-report.json", valid_peer_review_report()),
        "style_sheet": ("style-sheet.json", valid_style_sheet()),
    }
    for artifact_type, (name, payload) in examples.items():
        if artifact_type not in skipped:
            write_example(root, name, payload)


class TestBookArtifactContract(unittest.TestCase):
    def test_valid_examples_pass(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_schema(root)
            write_valid_coverage_examples(root)

            result = run_checker(root)

            self.assertEqual(
                result.returncode,
                0,
                msg=f"stdout={result.stdout!r} stderr={result.stderr!r}",
            )

    def test_missing_schema_fails_loudly(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_example(root, "claim-ledger.json", valid_claim_ledger())

            result = run_checker(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("book_artifact.schema.json", result.stdout)

    def test_missing_claim_evidence_status_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_schema(root)
            payload = valid_claim_ledger()
            del payload["claims"][0]["evidence_status"]
            write_example(root, "claim-ledger.json", payload)

            result = run_checker(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("evidence_status", result.stdout)

    def test_verified_comparable_title_requires_source_pointer(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_schema(root)
            write_example(
                root,
                "book-proposal.json",
                {
                    "schema_version": "book-artifact-v1",
                    "artifact_type": "book_proposal",
                    "project_title": "Fixture Book",
                    "comparable_titles": [
                        {
                            "title": "Known Comparable",
                            "verification_status": "verified",
                        }
                    ],
                },
            )

            result = run_checker(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("source_pointer", result.stdout)

    def test_unverified_comparable_title_does_not_require_source_pointer(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_schema(root)
            write_valid_coverage_examples(root, skip={"book_proposal"})
            write_example(
                root,
                "book-proposal.json",
                {
                    "schema_version": "book-artifact-v1",
                    "artifact_type": "book_proposal",
                    "project_title": "Fixture Book",
                    "comparable_titles": [
                        {
                            "title": "Unverified Comparable",
                            "verification_status": "unverified",
                        }
                    ],
                },
            )

            result = run_checker(root)

            self.assertEqual(
                result.returncode,
                0,
                msg=f"stdout={result.stdout!r} stderr={result.stderr!r}",
            )

    def test_invalid_artifact_type_enum_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_schema(root)
            payload = valid_claim_ledger()
            payload["artifact_type"] = "invented_artifact"
            write_example(root, "claim-ledger.json", payload)

            result = run_checker(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("expected one of", result.stdout)

    def test_unexpected_property_fails_with_property_name(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_schema(root)
            payload = valid_claim_ledger()
            payload["unexpected_field"] = "not allowed"
            write_example(root, "claim-ledger.json", payload)

            result = run_checker(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("unexpected_field", result.stdout)

    def test_missing_example_for_schema_artifact_type_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_schema(root)
            write_example(root, "claim-ledger.json", valid_claim_ledger())

            result = run_checker(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("missing example for artifact_type", result.stdout)

    def test_unresolved_schema_reference_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_schema(root)
            schema_path = root / "shared" / "contracts" / "book" / "book_artifact.schema.json"
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            schema["properties"]["project_title"] = {"$ref": "#/$defs/missing"}
            schema_path.write_text(json.dumps(schema), encoding="utf-8")
            write_example(root, "claim-ledger.json", valid_claim_ledger())

            result = run_checker(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("unresolved schema reference", result.stdout)

    def test_unsupported_schema_keyword_fails_loudly(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_schema(root)
            schema_path = root / "shared" / "contracts" / "book" / "book_artifact.schema.json"
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            schema["properties"]["project_title"] = {"type": "string", "pattern": "^Fixture"}
            schema_path.write_text(json.dumps(schema), encoding="utf-8")
            write_example(root, "claim-ledger.json", valid_claim_ledger())

            result = run_checker(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("unsupported schema keyword", result.stdout)

    def test_missing_artifact_type_does_not_trigger_artifact_specific_requirements(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_schema(root)
            payload = valid_claim_ledger()
            del payload["artifact_type"]
            write_example(root, "claim-ledger.json", payload)

            result = run_checker(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("artifact_type", result.stdout)
            self.assertNotIn("section_outline", result.stdout)
            self.assertNotIn("comparable_titles", result.stdout)

    def test_number_below_minimum_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_schema(root)
            write_example(
                root,
                "source-log.json",
                {
                    "schema_version": "book-artifact-v1",
                    "artifact_type": "source_discovery_log",
                    "project_title": "Fixture Book",
                    "search_log": [
                        {
                            "useful_results": -1,
                        }
                    ],
                },
            )

            result = run_checker(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("minimum", result.stdout)

    def test_whitespace_only_string_fails_minimum_length(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_schema(root)
            write_valid_coverage_examples(root, skip={"chapter_brief"})
            payload = valid_chapter_brief()
            payload["project_title"] = "   "
            write_example(root, "chapter-brief.json", payload)

            result = run_checker(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("blank string", result.stdout)

    def test_artifact_specific_field_from_other_artifact_type_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_schema(root)
            write_valid_coverage_examples(root, skip={"book_proposal"})
            payload = valid_book_proposal()
            payload["claims"] = [
                {
                    "claim": "This unrelated field belongs to another artifact.",
                    "evidence_status": "needed",
                    "safer_wording": "Remove this field from the proposal artifact.",
                }
            ]
            write_example(root, "book-proposal.json", payload)

            result = run_checker(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("not allowed for artifact_type 'book_proposal'", result.stdout)
            self.assertIn("claims", result.stdout)

    def test_artifact_boundaries_derive_optional_fields_from_schema_conditionals(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_schema(root)
            schema_path = root / "shared" / "contracts" / "book" / "book_artifact.schema.json"
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            schema["properties"]["optional_protocol_note"] = {"type": "string", "minLength": 1}
            for branch in schema["allOf"]:
                artifact_type = branch["if"]["properties"]["artifact_type"]["const"]
                if artifact_type == "source_discovery_log":
                    branch["then"]["properties"] = {
                        "optional_protocol_note": {"type": "string", "minLength": 1}
                    }
            schema_path.write_text(json.dumps(schema), encoding="utf-8")
            write_valid_coverage_examples(root, skip={"source_discovery_log"})
            payload = valid_source_discovery_log()
            payload["optional_protocol_note"] = "Optional field declared by the schema branch."
            write_example(root, "source-discovery-log.json", payload)

            result = run_checker(root)

            self.assertEqual(
                result.returncode,
                0,
                msg=f"stdout={result.stdout!r} stderr={result.stderr!r}",
            )


if __name__ == "__main__":
    unittest.main()
