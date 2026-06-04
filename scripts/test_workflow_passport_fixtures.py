"""Tests for multi-skill workflow process-passport preservation fixtures."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_workflow_passport_fixtures as checker


SCRIPT = Path(__file__).resolve().parent / "check_workflow_passport_fixtures.py"
ROOT = Path(__file__).resolve().parents[1]
SHIPPED_FIXTURES = ROOT / "tests" / "skill_evals" / "workflow_passports" / "fixtures.json"


def passport(
    *,
    source_access_level: str = "citation only; abstract only; no full text",
    evidence_status: str = "partial_unverified",
    human_verification_status: str = "needed before downstream reliance",
    unresolved_risks: list[str] | None = None,
) -> dict:
    return {
        "artifact_id": "fixture-artifact",
        "source_basis": "Synthetic fixture packet and upstream process passport only.",
        "source_access_level": source_access_level,
        "corpus_coverage": "Partial corpus; no representative field coverage.",
        "evidence_status": evidence_status,
        "tool_use": ["No external lookup; local fixture only."],
        "human_verification_status": human_verification_status,
        "unresolved_risks": unresolved_risks
        or ["Locator gap for the central claim remains unresolved."],
        "handoff_limits": ["Do not treat upstream claims as verified."],
        "generated_or_updated_at": "2026-06-03T00:00:00-04:00",
        "producing_skill": "systematic-source-discovery",
        "intended_next_skill_or_use": "extraction-table-builder",
    }


def artifact(*, process_passport: dict | None = None, claims: list[dict] | None = None) -> dict:
    return {
        "schema_version": "book-artifact-v1",
        "artifact_type": "source_discovery_log",
        "handoff_artifact": True,
        "process_passport": process_passport or passport(),
        "claims": claims
        or [
            {
                "claim": "Candidate source may support the chapter claim.",
                "evidence_status": "unverified",
                "locator_status": "locator_gap",
            }
        ],
    }


def workflow_fixture(
    *,
    output_artifact: dict | None = None,
    fixture_id: str = "source-discovery-to-extraction-preserves-passport",
) -> dict:
    return {
        "id": fixture_id,
        "from_skill": "systematic-source-discovery",
        "to_skill": "extraction-table-builder",
        "handoff": "source discovery -> extraction table",
        "input_artifact": artifact(),
        "expected_output_artifact": output_artifact or artifact(),
        "forbidden_behavior": [
            "Removing unresolved risks without a verification note.",
            "Treating citation-only or abstract-only access as full-text verification.",
            "Dropping human-review requirements.",
        ],
    }


def fixture_document(*fixtures: dict) -> dict:
    return {
        "schema_version": "workflow-passport-fixtures-v1",
        "purpose": "Fixture document for workflow passport checker tests.",
        "fixtures": list(fixtures),
    }


def write_fixture_document(root: Path, document: dict) -> Path:
    path = root / "fixtures.json"
    path.write_text(json.dumps(document), encoding="utf-8")
    return path


def run_checker(path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--fixtures", str(path), *args],
        check=False,
        text=True,
        capture_output=True,
    )


def write_actual_output(root: Path, fixture_id: str, output_artifact: dict) -> Path:
    output_root = root / "actual-outputs"
    output_root.mkdir()
    (output_root / f"{fixture_id}.json").write_text(json.dumps(output_artifact), encoding="utf-8")
    return output_root


class TestWorkflowPassportFixtures(unittest.TestCase):
    def test_valid_fixture_preserves_passport_limits(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            fixture_path = write_fixture_document(
                Path(temporary_directory),
                fixture_document(workflow_fixture()),
            )

            self.assertEqual(checker.validate_fixture_document(fixture_path), [])

    def test_non_object_fixture_entry_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            document = fixture_document(workflow_fixture())
            document["fixtures"].append("not a fixture object")
            fixture_path = write_fixture_document(Path(temporary_directory), document)

            errors = checker.validate_fixture_document(fixture_path)

            self.assertIn("fixtures[1] must be an object", errors)

    def test_process_passport_mixed_string_list_fails(self) -> None:
        output = artifact()
        output["process_passport"]["tool_use"] = ["No external lookup.", 123]
        with TemporaryDirectory() as temporary_directory:
            fixture_path = write_fixture_document(
                Path(temporary_directory),
                fixture_document(workflow_fixture(output_artifact=output)),
            )

            errors = checker.validate_fixture_document(fixture_path)

            self.assertIn(
                "source-discovery-to-extraction-preserves-passport: expected_output_artifact process_passport 'tool_use' must contain only non-empty strings",
                errors,
            )

    def test_process_passport_empty_required_scalar_fails(self) -> None:
        output = artifact()
        output["process_passport"]["source_basis"] = ""
        with TemporaryDirectory() as temporary_directory:
            fixture_path = write_fixture_document(
                Path(temporary_directory),
                fixture_document(workflow_fixture(output_artifact=output)),
            )

            errors = checker.validate_fixture_document(fixture_path)

            self.assertIn(
                "source-discovery-to-extraction-preserves-passport: expected_output_artifact process_passport 'source_basis' must be a non-empty string",
                errors,
            )

    def test_output_missing_unresolved_risk_fails(self) -> None:
        output = artifact(
            process_passport=passport(unresolved_risks=["A new downstream risk remains."])
        )
        with TemporaryDirectory() as temporary_directory:
            fixture_path = write_fixture_document(
                Path(temporary_directory),
                fixture_document(workflow_fixture(output_artifact=output)),
            )

            errors = checker.validate_fixture_document(fixture_path)

            self.assertIn(
                "source-discovery-to-extraction-preserves-passport: expected output missing unresolved risk 'Locator gap for the central claim remains unresolved.'",
                errors,
            )

    def test_output_must_not_treat_partial_source_access_as_full_text_verified(self) -> None:
        output = artifact(
            process_passport=passport(
                source_access_level="full text verified",
                evidence_status="verified",
            )
        )
        with TemporaryDirectory() as temporary_directory:
            fixture_path = write_fixture_document(
                Path(temporary_directory),
                fixture_document(workflow_fixture(output_artifact=output)),
            )

            errors = checker.validate_fixture_document(fixture_path)

            self.assertIn(
                "source-discovery-to-extraction-preserves-passport: expected output must not upgrade partial source access to full-text verification",
                errors,
            )
            self.assertIn(
                "source-discovery-to-extraction-preserves-passport: expected output must not upgrade unverified evidence status to verified",
                errors,
            )

    def test_output_must_not_drop_human_review_requirement(self) -> None:
        output = artifact(
            process_passport=passport(human_verification_status="completed")
        )
        with TemporaryDirectory() as temporary_directory:
            fixture_path = write_fixture_document(
                Path(temporary_directory),
                fixture_document(workflow_fixture(output_artifact=output)),
            )

            errors = checker.validate_fixture_document(fixture_path)

            self.assertIn(
                "source-discovery-to-extraction-preserves-passport: expected output must preserve human-review requirement",
                errors,
            )

    def test_valid_actual_live_output_passes(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture = workflow_fixture()
            fixture_path = write_fixture_document(root, fixture_document(fixture))
            output_root = write_actual_output(root, fixture["id"], artifact())

            self.assertEqual(checker.validate_fixture_document(fixture_path, output_root), [])

    def test_actual_live_output_missing_process_passport_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture = workflow_fixture()
            fixture_path = write_fixture_document(root, fixture_document(fixture))
            output_root = write_actual_output(root, fixture["id"], {"handoff_artifact": True})

            errors = checker.validate_fixture_document(fixture_path, output_root)

            self.assertIn(
                "source-discovery-to-extraction-preserves-passport: actual output artifact must include process_passport object",
                errors,
            )

    def test_actual_live_output_upgrading_partial_access_to_full_text_verified_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture = workflow_fixture()
            fixture_path = write_fixture_document(root, fixture_document(fixture))
            output_root = write_actual_output(
                root,
                fixture["id"],
                artifact(
                    process_passport=passport(
                        source_access_level="full text verified",
                        evidence_status="verified",
                    )
                ),
            )

            errors = checker.validate_fixture_document(fixture_path, output_root)

            self.assertIn(
                "source-discovery-to-extraction-preserves-passport: actual output must not upgrade partial source access to full-text verification",
                errors,
            )
            self.assertIn(
                "source-discovery-to-extraction-preserves-passport: actual output must not upgrade unverified evidence status to verified",
                errors,
            )

    def test_actual_live_output_dropping_human_review_requirement_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture = workflow_fixture()
            fixture_path = write_fixture_document(root, fixture_document(fixture))
            output_root = write_actual_output(
                root,
                fixture["id"],
                artifact(process_passport=passport(human_verification_status="completed")),
            )

            errors = checker.validate_fixture_document(fixture_path, output_root)

            self.assertIn(
                "source-discovery-to-extraction-preserves-passport: actual output must preserve human-review requirement",
                errors,
            )

    def test_actual_live_output_dropping_inherited_unresolved_risk_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture = workflow_fixture()
            fixture_path = write_fixture_document(root, fixture_document(fixture))
            output_root = write_actual_output(
                root,
                fixture["id"],
                artifact(process_passport=passport(unresolved_risks=["New downstream-only risk."])),
            )

            errors = checker.validate_fixture_document(fixture_path, output_root)

            self.assertIn(
                "source-discovery-to-extraction-preserves-passport: actual output missing unresolved risk 'Locator gap for the central claim remains unresolved.'",
                errors,
            )

    def test_script_reports_success_for_valid_actual_live_output(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture = workflow_fixture()
            fixture_path = write_fixture_document(root, fixture_document(fixture))
            output_root = write_actual_output(root, fixture["id"], artifact())

            result = run_checker(fixture_path, "--actual-output-root", str(output_root))

            self.assertEqual(
                result.returncode,
                0,
                msg=f"stdout={result.stdout!r} stderr={result.stderr!r}",
            )
            self.assertIn("OK: workflow passport fixtures are valid.", result.stdout)

    def test_actual_output_root_uses_live_fixture_manifest_when_present(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            selected_fixture = workflow_fixture()
            deferred_fixture = workflow_fixture(fixture_id="deferred-handoff-preserves-passport")
            fixture_path = write_fixture_document(
                root,
                fixture_document(selected_fixture, deferred_fixture),
            )
            live_root = root / "live_pilot_v1"
            output_root = live_root / "outputs"
            output_root.mkdir(parents=True)
            (live_root / "fixture-ids.json").write_text(
                json.dumps(
                    {
                        "schema_version": "workflow-passport-live-pilot-v1",
                        "fixture_ids": [selected_fixture["id"]],
                    }
                ),
                encoding="utf-8",
            )
            (output_root / f"{selected_fixture['id']}.json").write_text(
                json.dumps(artifact()),
                encoding="utf-8",
            )

            self.assertEqual(checker.validate_fixture_document(fixture_path, output_root), [])

    def test_input_must_have_unverified_claim_or_locator_gap(self) -> None:
        fixture = workflow_fixture()
        fixture["input_artifact"] = artifact(
            process_passport=passport(
                evidence_status="partial",
                unresolved_risks=["Generic evidence limitation remains."],
            ),
            claims=[{"claim": "No status labels."}],
        )
        with TemporaryDirectory() as temporary_directory:
            fixture_path = write_fixture_document(
                Path(temporary_directory),
                fixture_document(fixture),
            )

            errors = checker.validate_fixture_document(fixture_path)

            self.assertIn(
                "source-discovery-to-extraction-preserves-passport: input artifact must include an unverified claim or locator gap",
                errors,
            )

    def test_script_reports_success_for_valid_fixture(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            fixture_path = write_fixture_document(
                Path(temporary_directory),
                fixture_document(workflow_fixture()),
            )

            result = run_checker(fixture_path)

            self.assertEqual(
                result.returncode,
                0,
                msg=f"stdout={result.stdout!r} stderr={result.stderr!r}",
            )
            self.assertIn("OK: workflow passport fixtures are valid.", result.stdout)

    def test_shipped_fixtures_cover_required_workflow_handoffs(self) -> None:
        document = checker.read_json_object(SHIPPED_FIXTURES)
        handoffs = {
            (fixture.get("from_skill"), fixture.get("to_skill"))
            for fixture in checker.fixture_list(document)
        }

        self.assertEqual(
            handoffs,
            {
                ("systematic-source-discovery", "extraction-table-builder"),
                ("extraction-table-builder", "literature-review-mapper"),
                ("literature-review-mapper", "argument-architecture"),
                ("argument-architecture", "claim-evidence-ledger"),
                ("claim-evidence-ledger", "citation-integrity-auditor"),
                ("chapter-architecture", "scholarly-integrity-gate"),
                ("book-proposal-scholarship", "book-comps-verifier"),
                ("ai-human-workflow-log", "rights-privacy-release-auditor"),
            },
        )
        self.assertEqual(checker.validate_fixture_document(SHIPPED_FIXTURES), [])


if __name__ == "__main__":
    unittest.main()
