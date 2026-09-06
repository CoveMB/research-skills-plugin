"""Unit tests for the book artifact contract checker."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = Path(__file__).resolve().parent / "check_book_artifact_contract.py"
CANONICAL_SCHEMA = ROOT / "shared" / "contracts" / "book" / "book_artifact.schema.json"
CANONICAL_EXAMPLES_DIR = ROOT / "examples" / "book_artifacts"


def run_checker(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--path", str(root)],
        check=False,
        capture_output=True,
        text=True,
    )


def copy_contract(root: Path) -> tuple[Path, Path]:
    schema_path = root / "shared" / "contracts" / "book" / "book_artifact.schema.json"
    schema_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(CANONICAL_SCHEMA, schema_path)

    examples_dir = root / "examples" / "book_artifacts"
    examples_dir.mkdir(parents=True, exist_ok=True)
    for example_path in sorted(CANONICAL_EXAMPLES_DIR.glob("*.json")):
        shutil.copy2(example_path, examples_dir / example_path.name)
    return schema_path, examples_dir


def valid_claim_ledger_process_passport() -> dict:
    return {
        "artifact_id": "claim-ledger-fixture-2026-06-03",
        "source_basis": "Fixture chapter excerpt only; no source lookup.",
        "source_access_level": "excerpt only",
        "corpus_coverage": "No corpus coverage; claim audit is limited to the supplied excerpt.",
        "evidence_status": "partial_unverified",
        "tool_use": ["No external lookup; local fixture validation only."],
        "human_verification_status": "needed",
        "unresolved_risks": ["Source-claim fit remains unchecked."],
        "handoff_limits": ["Do not treat unverified claims as verified downstream."],
        "generated_or_updated_at": "2026-06-03T00:00:00-04:00",
        "producing_skill": "claim-evidence-ledger",
        "intended_next_skill_or_use": "claim-traceability-graph",
    }


class TestBookArtifactContract(unittest.TestCase):
    def test_valid_examples_pass(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            _schema_path, examples_dir = copy_contract(root)

            copied_example_names = sorted(path.name for path in examples_dir.glob("*.json"))
            canonical_example_names = sorted(
                path.name for path in CANONICAL_EXAMPLES_DIR.glob("*.json")
            )
            self.assertEqual(copied_example_names, canonical_example_names)

            result = run_checker(root)

            self.assertEqual(
                result.returncode,
                0,
                msg=f"stdout={result.stdout!r} stderr={result.stderr!r}",
            )

    def test_missing_schema_fails_loudly(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            schema_path, _examples_dir = copy_contract(root)
            schema_path.unlink()

            result = run_checker(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("book_artifact.schema.json", result.stdout)

    def test_missing_claim_evidence_status_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            _schema_path, examples_dir = copy_contract(root)
            payload_path = examples_dir / "claim-evidence-ledger.json"
            payload = json.loads(payload_path.read_text(encoding="utf-8"))
            del payload["claims"][0]["evidence_status"]
            payload_path.write_text(json.dumps(payload), encoding="utf-8")

            result = run_checker(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("evidence_status", result.stdout)

    def test_verified_comparable_title_requires_source_pointer(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            _schema_path, examples_dir = copy_contract(root)
            payload_path = examples_dir / "book-proposal.json"
            payload = json.loads(payload_path.read_text(encoding="utf-8"))
            payload["comparable_titles"][0]["verification_status"] = "verified"
            payload["comparable_titles"][0].pop("source_pointer", None)
            payload_path.write_text(json.dumps(payload), encoding="utf-8")

            result = run_checker(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("source_pointer", result.stdout)

    def test_unverified_comparable_title_does_not_require_source_pointer(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            _schema_path, examples_dir = copy_contract(root)
            payload_path = examples_dir / "book-proposal.json"
            payload = json.loads(payload_path.read_text(encoding="utf-8"))
            payload["comparable_titles"][0]["verification_status"] = "unverified"
            payload["comparable_titles"][0].pop("source_pointer", None)
            payload_path.write_text(json.dumps(payload), encoding="utf-8")

            result = run_checker(root)

            self.assertEqual(
                result.returncode,
                0,
                msg=f"stdout={result.stdout!r} stderr={result.stderr!r}",
            )

    def test_invalid_artifact_type_enum_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            _schema_path, examples_dir = copy_contract(root)
            canonical_path = examples_dir / "claim-evidence-ledger.json"
            payload = json.loads(canonical_path.read_text(encoding="utf-8"))
            payload["artifact_type"] = "invented_artifact"
            (examples_dir / "malformed-artifact-type.json").write_text(
                json.dumps(payload),
                encoding="utf-8",
            )

            result = run_checker(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("expected one of", result.stdout)

    def test_handoff_artifact_requires_process_passport(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            _schema_path, examples_dir = copy_contract(root)
            payload_path = examples_dir / "claim-evidence-ledger.json"
            payload = json.loads(payload_path.read_text(encoding="utf-8"))
            payload["handoff_artifact"] = True
            payload.pop("process_passport", None)
            payload_path.write_text(json.dumps(payload), encoding="utf-8")

            result = run_checker(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("process_passport", result.stdout)

    def test_handoff_artifact_accepts_valid_process_passport(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            _schema_path, examples_dir = copy_contract(root)
            payload_path = examples_dir / "claim-evidence-ledger.json"
            payload = json.loads(payload_path.read_text(encoding="utf-8"))
            payload["handoff_artifact"] = True
            payload["process_passport"] = valid_claim_ledger_process_passport()
            payload_path.write_text(json.dumps(payload), encoding="utf-8")

            result = run_checker(root)

            self.assertEqual(
                result.returncode,
                0,
                msg=f"stdout={result.stdout!r} stderr={result.stderr!r}",
            )

    def test_invalid_examples_are_checked_as_expected_failures(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            _schema_path, examples_dir = copy_contract(root)
            invalid_dir = examples_dir / "invalid"
            invalid_dir.mkdir(parents=True, exist_ok=True)
            canonical_path = examples_dir / "claim-evidence-ledger.json"
            payload = json.loads(canonical_path.read_text(encoding="utf-8"))
            payload["handoff_artifact"] = True
            payload.pop("process_passport", None)
            (invalid_dir / "handoff-missing-passport.json").write_text(
                json.dumps(payload),
                encoding="utf-8",
            )

            result = run_checker(root)

            self.assertEqual(
                result.returncode,
                0,
                msg=f"stdout={result.stdout!r} stderr={result.stderr!r}",
            )
            self.assertIn("invalid examples failed as expected", result.stdout)

    def test_unexpected_property_fails_with_property_name(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            _schema_path, examples_dir = copy_contract(root)
            payload_path = examples_dir / "claim-evidence-ledger.json"
            payload = json.loads(payload_path.read_text(encoding="utf-8"))
            payload["unexpected_field"] = "not allowed"
            payload_path.write_text(json.dumps(payload), encoding="utf-8")

            result = run_checker(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("unexpected_field", result.stdout)

    def test_missing_example_for_schema_artifact_type_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            _schema_path, examples_dir = copy_contract(root)
            for example_path in sorted(examples_dir.glob("*.json")):
                payload = json.loads(example_path.read_text(encoding="utf-8"))
                if payload.get("artifact_type") == "source_discovery_log":
                    example_path.unlink()

            result = run_checker(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("missing example for artifact_type", result.stdout)

    def test_unresolved_schema_reference_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            schema_path, _examples_dir = copy_contract(root)
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            schema["properties"]["project_title"] = {"$ref": "#/$defs/missing"}
            schema_path.write_text(json.dumps(schema), encoding="utf-8")

            result = run_checker(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("unresolved schema reference", result.stdout)

    def test_unsupported_schema_keyword_fails_loudly(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            schema_path, _examples_dir = copy_contract(root)
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            schema["properties"]["project_title"] = {"type": "string", "pattern": "^Fixture"}
            schema_path.write_text(json.dumps(schema), encoding="utf-8")

            result = run_checker(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("unsupported schema keyword", result.stdout)

    def test_unsupported_schema_type_fails_loudly(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            schema_path, _examples_dir = copy_contract(root)
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            schema["properties"]["project_title"] = {"type": "number"}
            schema_path.write_text(json.dumps(schema), encoding="utf-8")

            result = run_checker(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("unsupported schema type", result.stdout)

    def test_missing_artifact_type_does_not_trigger_artifact_specific_requirements(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            _schema_path, examples_dir = copy_contract(root)
            canonical_path = examples_dir / "claim-evidence-ledger.json"
            payload = json.loads(canonical_path.read_text(encoding="utf-8"))
            del payload["artifact_type"]
            (examples_dir / "malformed-missing-artifact-type.json").write_text(
                json.dumps(payload),
                encoding="utf-8",
            )

            result = run_checker(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("artifact_type", result.stdout)
            self.assertNotIn("section_outline", result.stdout)
            self.assertNotIn("comparable_titles", result.stdout)

    def test_number_below_minimum_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            _schema_path, examples_dir = copy_contract(root)
            payload_path = examples_dir / "source-discovery-log.json"
            payload = json.loads(payload_path.read_text(encoding="utf-8"))
            payload["search_log"][0]["useful_results"] = -1
            payload_path.write_text(json.dumps(payload), encoding="utf-8")

            result = run_checker(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("minimum", result.stdout)

    def test_whitespace_only_string_fails_minimum_length(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            _schema_path, examples_dir = copy_contract(root)
            payload_path = examples_dir / "chapter-brief.json"
            payload = json.loads(payload_path.read_text(encoding="utf-8"))
            payload["project_title"] = "   "
            payload_path.write_text(json.dumps(payload), encoding="utf-8")

            result = run_checker(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("blank string", result.stdout)

    def test_artifact_specific_field_from_other_artifact_type_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            _schema_path, examples_dir = copy_contract(root)
            payload_path = examples_dir / "book-proposal.json"
            payload = json.loads(payload_path.read_text(encoding="utf-8"))
            payload["claims"] = [
                {
                    "claim": "This unrelated field belongs to another artifact.",
                    "evidence_status": "needed",
                    "safer_wording": "Remove this field from the proposal artifact.",
                }
            ]
            payload_path.write_text(json.dumps(payload), encoding="utf-8")

            result = run_checker(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("not allowed for artifact_type 'book_proposal'", result.stdout)
            self.assertIn("claims", result.stdout)

    def test_artifact_boundaries_derive_optional_fields_from_schema_conditionals(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            schema_path, examples_dir = copy_contract(root)
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            optional_field_schema = {"type": "string", "minLength": 1}
            schema["properties"]["optional_protocol_note"] = optional_field_schema
            for branch in schema["allOf"]:
                artifact_type = branch["if"].get("properties", {}).get("artifact_type", {}).get("const")
                if artifact_type == "source_discovery_log":
                    branch["then"].setdefault("properties", {})[
                        "optional_protocol_note"
                    ] = optional_field_schema
            schema_path.write_text(json.dumps(schema), encoding="utf-8")
            payload_path = examples_dir / "source-discovery-log.json"
            payload = json.loads(payload_path.read_text(encoding="utf-8"))
            payload["optional_protocol_note"] = "Optional field declared by the schema branch."
            payload_path.write_text(json.dumps(payload), encoding="utf-8")

            result = run_checker(root)

            self.assertEqual(
                result.returncode,
                0,
                msg=f"stdout={result.stdout!r} stderr={result.stderr!r}",
            )


if __name__ == "__main__":
    unittest.main()
