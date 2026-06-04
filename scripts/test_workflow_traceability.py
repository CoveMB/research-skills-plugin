"""Tests for deterministic end-to-end workflow traceability fixtures."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_workflow_traceability as checker


SCRIPT = Path(__file__).resolve().parent / "check_workflow_traceability.py"
ROOT = Path(__file__).resolve().parents[1]
SHIPPED_TRACE = ROOT / "tests" / "skill_evals" / "workflow_traces" / "claim-lineage-fixture" / "workflow-trace.json"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def passport(
    *,
    artifact_id: str,
    producing_skill: str,
    next_use: str,
    parent_ids: list[str] | None = None,
    parent_hashes: list[str] | None = None,
    source_access_level: str = "citation only; abstract only; no full text access",
    evidence_status: str = "partial_unverified",
    human_verification_status: str = "needed before downstream reliance",
    unresolved_risks: list[str] | None = None,
    handoff_limits: list[str] | None = None,
) -> dict:
    payload = {
        "artifact_id": artifact_id,
        "source_basis": "Synthetic workflow trace fixture; no external lookup.",
        "source_access_level": source_access_level,
        "corpus_coverage": "Partial synthetic corpus; counter-literature is not verified.",
        "evidence_status": evidence_status,
        "tool_use": ["No external lookup; deterministic local fixture only."],
        "human_verification_status": human_verification_status,
        "unresolved_risks": unresolved_risks
        or ["Central causal claim lacks full-text verification and a page locator."],
        "handoff_limits": handoff_limits
        or ["Do not mark the causal claim verified downstream."],
        "generated_or_updated_at": "2026-06-03T00:00:00-04:00",
        "producing_skill": producing_skill,
        "intended_next_skill_or_use": next_use,
    }
    if parent_ids is not None:
        payload["parent_artifact_ids"] = parent_ids
    if parent_hashes is not None:
        payload["input_artifact_hashes"] = parent_hashes
    return payload


def claim(
    *,
    claim_id: str = "claim-dashboard-causality",
    claim_text: str = "Mobility dashboards caused lower congestion.",
    claim_type: str = "causal",
    evidence_status: str = "unverified",
    locator_status: str = "locator_gap",
    human_verification_status: str = "needed",
    source_id: str = "source-dashboard-study",
    source_locator: str | None = "page locator missing",
    source_basis: str | None = "citation only; no full text",
    source_claim_fit_note: str | None = "Source is not yet checked for causal support.",
    version_note: str | None = None,
) -> dict:
    payload = {
        "claim_id": claim_id,
        "claim": claim_text,
        "claim_type": claim_type,
        "evidence_status": evidence_status,
        "locator_status": locator_status,
        "human_verification_status": human_verification_status,
        "source_id": source_id,
    }
    if source_locator is not None:
        payload["source_locator"] = source_locator
    if source_basis is not None:
        payload["source_basis"] = source_basis
    if source_claim_fit_note is not None:
        payload["source_claim_fit_note"] = source_claim_fit_note
    if version_note is not None:
        payload["version_note"] = version_note
    return payload


def traceability_link(claim_id: str = "claim-dashboard-causality") -> dict:
    return {
        "claim_id": claim_id,
        "claim": "Mobility dashboards caused lower congestion.",
        "source_pointer": "source-dashboard-study",
        "locator_status": "locator_gap",
        "verification_status": "unverified",
        "repair_action": "Verify full text and locator before relying on this causal claim.",
    }


def artifact(
    *,
    artifact_id: str,
    artifact_type: str,
    producing_skill: str,
    next_use: str,
    parent_ids: list[str] | None = None,
    parent_hashes: list[str] | None = None,
    claims: list[dict] | None = None,
    traceability_links: list[dict] | None = None,
    process_passport: dict | None = None,
) -> dict:
    payload = {
        "schema_version": checker.TRACE_ARTIFACT_SCHEMA_VERSION,
        "artifact_type": artifact_type,
        "handoff_artifact": True,
        "process_passport": process_passport
        or passport(
            artifact_id=artifact_id,
            producing_skill=producing_skill,
            next_use=next_use,
            parent_ids=parent_ids,
            parent_hashes=parent_hashes,
        ),
        "claims": claims or [claim()],
    }
    if traceability_links is not None:
        payload["traceability_links"] = traceability_links
    return payload


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_trace_fixture(
    root: Path,
    *,
    mutate_second_artifact: dict | None = None,
    stale_hash: bool = False,
    include_traceability_links: bool = False,
) -> Path:
    artifacts_dir = root / "artifacts"
    first_path = artifacts_dir / "01-source-discovery-log.json"
    first_artifact = artifact(
        artifact_id="source-discovery-log",
        artifact_type="source_discovery_log",
        producing_skill="systematic-source-discovery",
        next_use="extraction-table-builder",
    )
    write_json(first_path, first_artifact)
    first_hash = sha256_file(first_path)

    second_path = artifacts_dir / "02-extraction-table.json"
    second_artifact = artifact(
        artifact_id="extraction-table",
        artifact_type="extraction_table",
        producing_skill="extraction-table-builder",
        next_use="literature-review-mapper",
        parent_ids=["source-discovery-log"],
        parent_hashes=[first_hash],
        traceability_links=[traceability_link()] if include_traceability_links else None,
    )
    if mutate_second_artifact:
        second_artifact.update(mutate_second_artifact)
    write_json(second_path, second_artifact)
    second_hash = sha256_file(second_path)

    trace = {
        "schema_version": "workflow-trace-v1",
        "scenario_id": "claim-lineage-fixture",
        "tracked_claim_ids": ["claim-dashboard-causality"],
        "stages": [
            {
                "stage_id": "source-discovery",
                "skill": "systematic-source-discovery",
                "artifact_id": "source-discovery-log",
                "artifact_path": "artifacts/01-source-discovery-log.json",
                "artifact_sha256": "0" * 64 if stale_hash else first_hash,
            },
            {
                "stage_id": "extraction",
                "skill": "extraction-table-builder",
                "artifact_id": "extraction-table",
                "artifact_path": "artifacts/02-extraction-table.json",
                "artifact_sha256": second_hash,
                "parent_artifact_ids": ["source-discovery-log"],
                "parent_artifact_sha256": [first_hash],
            },
        ],
    }
    trace_path = root / "workflow-trace.json"
    write_json(trace_path, trace)
    return trace_path


def first_stage_hash(trace_path: Path) -> str:
    payload = json.loads(trace_path.read_text(encoding="utf-8"))
    return payload["stages"][0]["artifact_sha256"]


def verification_event() -> dict:
    return {
        "event_type": "source and claim verification",
        "verified_at": "2026-06-03T00:00:00-04:00",
        "verification_basis": "Synthetic fixture records full-text, locator, evidence, and human review.",
        "verified_by_or_tool": "human-review-fixture",
        "verified_fields": [
            "source_access_level",
            "evidence_status",
            "human_verification_status",
            "locator_status",
        ],
        "claim_ids": ["claim-dashboard-causality"],
    }


def run_checker(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--trace", str(path)],
        check=False,
        text=True,
        capture_output=True,
    )


class TestWorkflowTraceability(unittest.TestCase):
    def test_valid_trace_passes(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            trace_path = write_trace_fixture(Path(temporary_directory))

            self.assertEqual(checker.validate_trace_file(trace_path), [])

    def test_valid_traceability_graph_with_claim_links_passes(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            trace_path = write_trace_fixture(Path(temporary_directory), include_traceability_links=True)

            self.assertEqual(checker.validate_trace_file(trace_path), [])

    def test_non_object_stage_entry_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            trace_path = write_trace_fixture(Path(temporary_directory))
            payload = json.loads(trace_path.read_text(encoding="utf-8"))
            payload["stages"].append("not a stage object")
            write_json(trace_path, payload)

            errors = checker.validate_trace_file(trace_path)

            self.assertIn("trace: stages[2] must be an object", errors)

    def test_process_passport_mixed_string_list_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            first_hash = first_stage_hash(write_trace_fixture(root))
            second_passport = passport(
                artifact_id="extraction-table",
                producing_skill="extraction-table-builder",
                next_use="literature-review-mapper",
                parent_ids=["source-discovery-log"],
                parent_hashes=[first_hash],
            )
            second_passport["tool_use"] = ["No external lookup.", 123]
            trace_path = write_trace_fixture(
                root,
                mutate_second_artifact={"process_passport": second_passport},
            )

            errors = checker.validate_trace_file(trace_path)

            self.assertIn(
                "extraction: process_passport 'tool_use' must contain only non-empty strings",
                errors,
            )

    def test_process_passport_empty_required_scalar_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            first_hash = first_stage_hash(write_trace_fixture(root))
            second_passport = passport(
                artifact_id="extraction-table",
                producing_skill="extraction-table-builder",
                next_use="literature-review-mapper",
                parent_ids=["source-discovery-log"],
                parent_hashes=[first_hash],
            )
            second_passport["source_basis"] = ""
            trace_path = write_trace_fixture(
                root,
                mutate_second_artifact={"process_passport": second_passport},
            )

            errors = checker.validate_trace_file(trace_path)

            self.assertIn(
                "extraction: process_passport 'source_basis' must be a non-empty string",
                errors,
            )

    def test_book_artifact_schema_version_fails_for_trace_artifact(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            trace_path = write_trace_fixture(
                Path(temporary_directory),
                mutate_second_artifact={"schema_version": "book-artifact-v1"},
            )

            errors = checker.validate_trace_file(trace_path)

            self.assertIn(
                "extraction: artifact schema_version must be workflow-trace-artifact-v1",
                errors,
            )

    def test_stale_artifact_hash_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            trace_path = write_trace_fixture(Path(temporary_directory), stale_hash=True)

            errors = checker.validate_trace_file(trace_path)

            self.assertIn("source-discovery: artifact_sha256 does not match artifact file", errors)

    def test_missing_parent_hash_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            trace_path = write_trace_fixture(Path(temporary_directory))
            payload = json.loads(trace_path.read_text(encoding="utf-8"))
            payload["stages"][1]["parent_artifact_sha256"] = ["f" * 64]
            write_json(trace_path, payload)

            errors = checker.validate_trace_file(trace_path)

            self.assertIn("extraction: parent_artifact_sha256 does not match previous stage hash", errors)

    def test_symlink_artifact_path_outside_trace_directory_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            outside_path = root.parent / f"{root.name}-outside-artifact.json"
            outside_path.write_text("{}", encoding="utf-8")
            symlink_path = root / "artifact-link.json"
            try:
                symlink_path.symlink_to(outside_path)
            except OSError as error:
                outside_path.unlink(missing_ok=True)
                self.skipTest(f"symlink creation unavailable: {error}")

            try:
                trace_path = root / "workflow-trace.json"
                write_json(trace_path, {})

                self.assertIsNone(checker.safe_artifact_path(trace_path, "artifact-link.json"))
            finally:
                outside_path.unlink(missing_ok=True)

    def test_dropped_claim_id_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            trace_path = write_trace_fixture(
                Path(temporary_directory),
                mutate_second_artifact={"claims": [claim(claim_id="new-claim")]},
            )

            errors = checker.validate_trace_file(trace_path)

            self.assertIn("extraction: missing tracked claim_id 'claim-dashboard-causality'", errors)

    def test_traceability_link_to_undefined_claim_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            trace_path = write_trace_fixture(
                Path(temporary_directory),
                mutate_second_artifact={"traceability_links": [traceability_link("missing-claim")]},
            )

            errors = checker.validate_trace_file(trace_path)

            self.assertIn("extraction: referenced claim_id 'missing-claim' is not defined in claims", errors)

    def test_orphan_claim_definition_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            trace_path = write_trace_fixture(
                Path(temporary_directory),
                mutate_second_artifact={"claims": [claim(), claim(claim_id="claim-orphan")]},
            )

            errors = checker.validate_trace_file(trace_path)

            self.assertIn("extraction: defined claim_id 'claim-orphan' is never referenced", errors)

    def test_duplicate_claim_id_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            trace_path = write_trace_fixture(
                Path(temporary_directory),
                mutate_second_artifact={"claims": [claim(), claim(claim_text="Duplicate row with the same ID.")]},
            )

            errors = checker.validate_trace_file(trace_path)

            self.assertIn("extraction: duplicate claim_id 'claim-dashboard-causality'", errors)

    def test_silent_claim_text_change_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            trace_path = write_trace_fixture(
                Path(temporary_directory),
                mutate_second_artifact={
                    "claims": [
                        claim(claim_text="Mobility dashboards reliably reduced congestion across the city.")
                    ]
                },
            )

            errors = checker.validate_trace_file(trace_path)

            self.assertIn(
                "extraction: claim 'claim-dashboard-causality' text changed without version note",
                errors,
            )

    def test_source_locator_source_basis_and_claim_type_removals_fail(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            trace_path = write_trace_fixture(
                Path(temporary_directory),
                mutate_second_artifact={
                    "claims": [
                        claim(
                            claim_type="descriptive",
                            source_locator=None,
                            source_basis=None,
                        )
                    ],
                },
            )

            errors = checker.validate_trace_file(trace_path)

            self.assertIn("extraction: claim 'claim-dashboard-causality' removed source locator", errors)
            self.assertIn("extraction: claim 'claim-dashboard-causality' removed source-basis label", errors)
            self.assertIn("extraction: claim 'claim-dashboard-causality' type changed without explanation", errors)

    def test_same_source_for_different_claim_types_requires_fit_note(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            trace_path = write_trace_fixture(
                Path(temporary_directory),
                mutate_second_artifact={
                    "claims": [
                        claim(source_claim_fit_note=None),
                        claim(
                            claim_id="claim-dashboard-description",
                            claim_text="Mobility dashboards displayed street-level congestion data.",
                            claim_type="descriptive",
                            source_claim_fit_note=None,
                        ),
                    ],
                    "traceability_links": [
                        traceability_link("claim-dashboard-description"),
                    ],
                },
            )

            errors = checker.validate_trace_file(trace_path)

            self.assertIn(
                "extraction: source 'source-dashboard-study' supports multiple claim types without source-claim-fit note",
                errors,
            )

    def test_dropped_unresolved_risk_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            second_passport = passport(
                artifact_id="extraction-table",
                producing_skill="extraction-table-builder",
                next_use="literature-review-mapper",
                parent_ids=["source-discovery-log"],
                parent_hashes=["placeholder"],
                unresolved_risks=["A downstream-only risk remains."],
            )
            trace_path = write_trace_fixture(
                Path(temporary_directory),
                mutate_second_artifact={"process_passport": second_passport},
            )

            errors = checker.validate_trace_file(trace_path)

            self.assertIn(
                "extraction: missing unresolved risk from prior stage 'Central causal claim lacks full-text verification and a page locator.'",
                errors,
            )

    def test_bare_resolved_risks_does_not_allow_dropped_unresolved_risk(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            first_hash = first_stage_hash(write_trace_fixture(root))
            second_passport = passport(
                artifact_id="extraction-table",
                producing_skill="extraction-table-builder",
                next_use="literature-review-mapper",
                parent_ids=["source-discovery-log"],
                parent_hashes=[first_hash],
                unresolved_risks=["A downstream-only risk remains."],
            )
            trace_path = write_trace_fixture(
                root,
                mutate_second_artifact={
                    "process_passport": second_passport,
                    "resolved_risks": [
                        "Central causal claim lacks full-text verification and a page locator."
                    ],
                },
            )

            errors = checker.validate_trace_file(trace_path)

            self.assertIn(
                "extraction: missing unresolved risk from prior stage 'Central causal claim lacks full-text verification and a page locator.'",
                errors,
            )

    def test_unrelated_risk_resolution_note_does_not_allow_dropped_unresolved_risk(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            first_hash = first_stage_hash(write_trace_fixture(root))
            second_passport = passport(
                artifact_id="extraction-table",
                producing_skill="extraction-table-builder",
                next_use="literature-review-mapper",
                parent_ids=["source-discovery-log"],
                parent_hashes=[first_hash],
                unresolved_risks=["A downstream-only risk remains."],
            )
            trace_path = write_trace_fixture(
                root,
                mutate_second_artifact={
                    "process_passport": second_passport,
                    "risk_resolution_note": "A generic downstream note exists, but it does not resolve the upstream risk.",
                },
            )

            errors = checker.validate_trace_file(trace_path)

            self.assertIn(
                "extraction: missing unresolved risk from prior stage 'Central causal claim lacks full-text verification and a page locator.'",
                errors,
            )

    def test_source_evidence_locator_and_human_review_upgrades_fail(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            second_passport = passport(
                artifact_id="extraction-table",
                producing_skill="extraction-table-builder",
                next_use="literature-review-mapper",
                source_access_level="full text verified",
                evidence_status="verified",
                human_verification_status="completed",
                parent_ids=["source-discovery-log"],
                parent_hashes=["placeholder"],
            )
            trace_path = write_trace_fixture(
                Path(temporary_directory),
                mutate_second_artifact={
                    "process_passport": second_passport,
                    "claims": [
                        claim(
                            evidence_status="verified",
                            locator_status="verified_locator",
                            human_verification_status="completed",
                        )
                    ],
                },
            )

            errors = checker.validate_trace_file(trace_path)

            self.assertIn("extraction: must not upgrade partial source access to full-text verification", errors)
            self.assertIn("extraction: must not upgrade unverified passport evidence status to verified", errors)
            self.assertIn("extraction: must not mark human verification complete without verification event", errors)
            self.assertIn("extraction: claim 'claim-dashboard-causality' must not upgrade evidence status to verified", errors)
            self.assertIn("extraction: claim 'claim-dashboard-causality' must not upgrade locator gap to verified", errors)

    def test_placeholder_verification_event_does_not_allow_upgrades(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            first_hash = first_stage_hash(write_trace_fixture(root))
            second_passport = passport(
                artifact_id="extraction-table",
                producing_skill="extraction-table-builder",
                next_use="literature-review-mapper",
                source_access_level="full text verified",
                evidence_status="verified",
                human_verification_status="completed",
                parent_ids=["source-discovery-log"],
                parent_hashes=[first_hash],
            )
            trace_path = write_trace_fixture(
                root,
                mutate_second_artifact={
                    "process_passport": second_passport,
                    "verification_events": [{}],
                    "claims": [
                        claim(
                            evidence_status="verified",
                            locator_status="verified_locator",
                            human_verification_status="completed",
                        )
                    ],
                },
            )

            errors = checker.validate_trace_file(trace_path)

            self.assertIn("extraction: must not upgrade partial source access to full-text verification", errors)
            self.assertIn("extraction: must not upgrade unverified passport evidence status to verified", errors)
            self.assertIn("extraction: must not mark human verification complete without verification event", errors)
            self.assertIn("extraction: claim 'claim-dashboard-causality' must not upgrade evidence status to verified", errors)
            self.assertIn("extraction: claim 'claim-dashboard-causality' must not upgrade locator gap to verified", errors)

    def test_scoped_verification_event_allows_matching_upgrades(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            first_hash = first_stage_hash(write_trace_fixture(root))
            second_passport = passport(
                artifact_id="extraction-table",
                producing_skill="extraction-table-builder",
                next_use="literature-review-mapper",
                source_access_level="full text verified",
                evidence_status="verified",
                human_verification_status="completed",
                parent_ids=["source-discovery-log"],
                parent_hashes=[first_hash],
            )
            trace_path = write_trace_fixture(
                root,
                mutate_second_artifact={
                    "process_passport": second_passport,
                    "verification_events": [verification_event()],
                    "claims": [
                        claim(
                            evidence_status="verified",
                            locator_status="verified_locator",
                            human_verification_status="completed",
                        )
                    ],
                },
            )

            self.assertEqual(checker.validate_trace_file(trace_path), [])

    def test_script_reports_success_for_valid_trace(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            trace_path = write_trace_fixture(Path(temporary_directory))

            result = run_checker(trace_path)

            self.assertEqual(
                result.returncode,
                0,
                msg=f"stdout={result.stdout!r} stderr={result.stderr!r}",
            )
            self.assertIn("OK: workflow trace is valid.", result.stdout)

    def test_shipped_trace_fixture_is_valid(self) -> None:
        self.assertEqual(checker.validate_trace_file(SHIPPED_TRACE), [])


if __name__ == "__main__":
    unittest.main()
