"""Tests for research behavior fixture output checks."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_research_behavior_fixtures import (
    validate_fixture_document,
    validate_fixture_outputs,
)


def fixture_document(*fixtures: dict) -> dict:
    return {
        "schema_version": "research-skill-behavior-fixtures-v1",
        "purpose": "Fixture document for behavior checker tests.",
        "fixtures": list(fixtures),
    }


def fixture(
    fixture_id: str = "compact-routing",
    *,
    required_markers: list[str] | None = None,
    forbidden_claims: list[str] | None = None,
    risk_covered: str = "compact routing",
) -> dict:
    return {
        "id": fixture_id,
        "prompt": "Fixture prompt.",
        "expected_route": "research-intent-router",
        "risk_covered": risk_covered,
        "required_output_markers": required_markers
        or ["Source basis", "How to use this result", "Next action"],
        "forbidden_claims": forbidden_claims or ["source verified"],
    }


def write_fixture_file(root: Path, document: dict) -> Path:
    fixture_path = root / "fixtures.json"
    fixture_path.write_text(json.dumps(document), encoding="utf-8")
    return fixture_path


class TestResearchBehaviorFixtures(unittest.TestCase):
    def test_valid_output_passes(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_file(root, fixture_document(fixture()))
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (outputs_dir / "compact-routing.md").write_text(
                "\n".join([
                    "Source basis: user prompt only.",
                    "How to use this result: TRIAGE ONLY - Pick the next step.",
                    "Next action: Use the smallest route.",
                ]),
                encoding="utf-8",
            )

            self.assertEqual(validate_fixture_document(fixture_path), [])
            self.assertEqual(validate_fixture_outputs(fixture_path, outputs_dir), [])

    def test_missing_required_marker_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_file(root, fixture_document(fixture()))
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (outputs_dir / "compact-routing.md").write_text(
                "Source basis: user prompt only.\nNext action: Use the smallest route.",
                encoding="utf-8",
            )

            errors = validate_fixture_outputs(fixture_path, outputs_dir)

            self.assertIn("compact-routing: missing required marker 'How to use this result'", errors)

    def test_forbidden_claim_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_file(root, fixture_document(fixture()))
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (outputs_dir / "compact-routing.md").write_text(
                "\n".join([
                    "Source basis: user prompt only.",
                    "How to use this result: TRIAGE ONLY - Pick the next step.",
                    "Next action: Use the smallest route.",
                    "Source verified.",
                ]),
                encoding="utf-8",
            )

            errors = validate_fixture_outputs(fixture_path, outputs_dir)

            self.assertIn("compact-routing: contains forbidden claim 'source verified'", errors)

    def test_duplicate_fixture_ids_fail(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_file(root, fixture_document(fixture(), fixture()))

            errors = validate_fixture_document(fixture_path)

            self.assertIn("duplicate fixture id 'compact-routing'", errors)

    def test_missing_output_file_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_file(root, fixture_document(fixture()))
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()

            errors = validate_fixture_outputs(fixture_path, outputs_dir)

            self.assertIn("compact-routing: missing output file compact-routing.md", errors)

    def test_compact_output_requires_one_result_use_and_next_action(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_file(root, fixture_document(fixture()))
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (outputs_dir / "compact-routing.md").write_text(
                "\n".join([
                    "Source basis: user prompt only.",
                    "How to use this result: TRIAGE ONLY - Pick the next step.",
                    "How to use this result: TRIAGE ONLY - Repeat.",
                    "Next action: Use the smallest route.",
                    "Next action: Repeat.",
                ]),
                encoding="utf-8",
            )

            errors = validate_fixture_outputs(fixture_path, outputs_dir)

            self.assertIn("compact-routing: expected exactly 1 'How to use this result', found 2", errors)
            self.assertIn("compact-routing: expected exactly 1 'Next action', found 2", errors)


if __name__ == "__main__":
    unittest.main()
