"""Tests for research behavior fixture output checks."""
from __future__ import annotations

import json
import hashlib
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_research_behavior_fixtures import (
    OVERSTATEMENT_POLICY_REQUIRED_MARKERS,
    output_path_for_fixture,
    validate_fixture_document,
    validate_fixture_outputs,
    validate_fixture_traces,
)


SCRIPT = Path(__file__).resolve().parent / "check_research_behavior_fixtures.py"


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
    required_output_patterns: list[str] | None = None,
    forbidden_output_patterns: list[str] | None = None,
    risk_covered: str = "compact routing",
    should_trigger: bool = True,
    expected_route: str = "research-intent-router",
) -> dict:
    payload = {
        "id": fixture_id,
        "prompt": "Fixture prompt.",
        "expected_route": expected_route,
        "should_trigger": should_trigger,
        "risk_covered": risk_covered,
        "required_output_markers": required_markers
        or ["Source basis", "How to use this result", "Next action"],
        "forbidden_claims": forbidden_claims or ["source verified"],
    }
    if required_output_patterns is not None:
        payload["required_output_patterns"] = required_output_patterns
    if forbidden_output_patterns is not None:
        payload["forbidden_output_patterns"] = forbidden_output_patterns
    return payload


def high_risk_fixture(
    *,
    required_markers: list[str] | None = None,
    forbidden_claims: list[str] | None = None,
    risk_covered: str = "thin corpus field consensus overclaim",
) -> dict:
    return fixture(
        fixture_id="thin-corpus-consensus-overclaim",
        expected_route="literature-review-mapper",
        risk_covered=risk_covered,
        required_markers=required_markers or ["schools of thought"],
        forbidden_claims=forbidden_claims or ["field consensus is settled"],
    )


def write_fixture_file(root: Path, document: dict) -> Path:
    fixture_path = root / "fixtures.json"
    fixture_path.write_text(json.dumps(document), encoding="utf-8")
    return fixture_path


def write_trace_file(traces_dir: Path, fixture_id: str, payload: dict) -> None:
    traces_dir.mkdir()
    (traces_dir / f"{fixture_id}.json").write_text(json.dumps(payload), encoding="utf-8")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def route_trace(fixture_id: str = "compact-routing", selected_skill: str = "research-intent-router") -> dict:
    return {
        "schema_version": "research-behavior-route-trace-v2",
        "fixture_id": fixture_id,
        "selected_skill": selected_skill,
        "prompt_sha256": sha256_text("Fixture prompt."),
        "output_sha256": sha256_text(""),
        "skill_invoked": True,
        "prompt_supplied": True,
        "output_captured": True,
    }


def negative_route_trace(fixture_id: str = "adjacent-negative-control") -> dict:
    return {
        "schema_version": "research-behavior-route-trace-v2",
        "fixture_id": fixture_id,
        "selected_skill": "none",
        "prompt_sha256": sha256_text("Fixture prompt."),
        "output_sha256": sha256_text(""),
        "skill_invoked": False,
        "prompt_supplied": True,
        "output_captured": True,
    }


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
                    "Selected skill: research-intent-router.",
                    "How to use this result: TRIAGE ONLY - Pick the next step.",
                    "Next action: Use the smallest route.",
                ]),
                encoding="utf-8",
            )

            self.assertEqual(validate_fixture_document(fixture_path), [])
            self.assertEqual(validate_fixture_outputs(fixture_path, outputs_dir), [])

    def test_valid_route_trace_with_output_hash_passes(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_file(root, fixture_document(fixture()))
            outputs_dir = root / "outputs"
            traces_dir = root / "traces"
            output_text = "Selected skill: research-intent-router.\nSource basis: user prompt only.\n"
            outputs_dir.mkdir()
            (outputs_dir / "compact-routing.md").write_text(output_text, encoding="utf-8")
            write_trace_file(
                traces_dir,
                "compact-routing",
                {
                    **route_trace(),
                    "output_sha256": sha256_text(output_text),
                },
            )

            self.assertEqual(validate_fixture_traces(fixture_path, traces_dir, outputs_dir), [])

    def test_valid_route_trace_passes(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_file(root, fixture_document(fixture()))
            traces_dir = root / "traces"
            write_trace_file(traces_dir, "compact-routing", route_trace())

            self.assertEqual(validate_fixture_traces(fixture_path, traces_dir), [])

    def test_negative_control_route_trace_passes_when_skill_does_not_trigger(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            negative_fixture = fixture(
                fixture_id="adjacent-negative-control",
                expected_route="none",
                should_trigger=False,
                risk_covered="negative trigger control",
            )
            fixture_path = write_fixture_file(root, fixture_document(negative_fixture))
            traces_dir = root / "traces"
            write_trace_file(traces_dir, "adjacent-negative-control", negative_route_trace())

            self.assertEqual(validate_fixture_traces(fixture_path, traces_dir), [])

    def test_negative_control_route_trace_rejects_accidental_skill_invocation(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            negative_fixture = fixture(
                fixture_id="adjacent-negative-control",
                expected_route="none",
                should_trigger=False,
                risk_covered="negative trigger control",
            )
            fixture_path = write_fixture_file(root, fixture_document(negative_fixture))
            traces_dir = root / "traces"
            write_trace_file(
                traces_dir,
                "adjacent-negative-control",
                {**negative_route_trace(), "selected_skill": "citation-integrity-auditor", "skill_invoked": True},
            )

            errors = validate_fixture_traces(fixture_path, traces_dir)

            self.assertIn("adjacent-negative-control: trace skill_invoked must be false", errors)
            self.assertIn(
                "adjacent-negative-control: trace selected_skill must match expected_route 'none'",
                errors,
            )

    def test_route_trace_rejects_prompt_hash_mismatch(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_file(root, fixture_document(fixture()))
            traces_dir = root / "traces"
            write_trace_file(traces_dir, "compact-routing", {**route_trace(), "prompt_sha256": sha256_text("stale prompt")})

            errors = validate_fixture_traces(fixture_path, traces_dir)

            self.assertIn("compact-routing: trace prompt_sha256 does not match fixture prompt", errors)

    def test_route_trace_rejects_output_hash_mismatch_when_outputs_checked(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_file(root, fixture_document(fixture()))
            outputs_dir = root / "outputs"
            traces_dir = root / "traces"
            outputs_dir.mkdir()
            (outputs_dir / "compact-routing.md").write_text(
                "Selected skill: research-intent-router.\nSource basis: user prompt only.\n",
                encoding="utf-8",
            )
            write_trace_file(traces_dir, "compact-routing", route_trace())

            errors = validate_fixture_traces(fixture_path, traces_dir, outputs_dir)

            self.assertIn("compact-routing: trace output_sha256 does not match captured output", errors)

    def test_route_trace_rejects_wrong_selected_skill(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_file(root, fixture_document(fixture()))
            traces_dir = root / "traces"
            write_trace_file(traces_dir, "compact-routing", route_trace(selected_skill="citation-integrity-auditor"))

            errors = validate_fixture_traces(fixture_path, traces_dir)

            self.assertIn(
                "compact-routing: trace selected_skill must match expected_route 'research-intent-router'",
                errors,
            )

    def test_route_trace_requires_skill_invocation_and_capture_flags(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_file(root, fixture_document(fixture()))
            traces_dir = root / "traces"
            write_trace_file(
                traces_dir,
                "compact-routing",
                {
                    **route_trace(),
                    "skill_invoked": False,
                    "prompt_supplied": False,
                    "output_captured": False,
                },
            )

            errors = validate_fixture_traces(fixture_path, traces_dir)

            self.assertIn("compact-routing: trace skill_invoked must be true", errors)
            self.assertIn("compact-routing: trace prompt_supplied must be true", errors)
            self.assertIn("compact-routing: trace output_captured must be true", errors)

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

    def test_required_output_pattern_catches_marker_only_output(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_file(
                root,
                fixture_document(
                    fixture(
                        required_output_patterns=[
                            r"(?is)What I can verify.{0,120}(controlled packet|user prompt only)",
                        ]
                    )
                ),
            )
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (outputs_dir / "compact-routing.md").write_text(
                "\n".join([
                    "Selected skill: research-intent-router.",
                    "Source basis:",
                    "What I can verify:",
                    "What remains uncertain:",
                    "User verification needed:",
                    "How to use this result: TRIAGE ONLY - Pick the next step.",
                    "Next action: Use the smallest route.",
                ]),
                encoding="utf-8",
            )

            errors = validate_fixture_outputs(fixture_path, outputs_dir)

            self.assertIn(
                "compact-routing: missing required output pattern "
                "'(?is)What I can verify.{0,120}(controlled packet|user prompt only)'",
                errors,
            )

    def test_forbidden_output_pattern_catches_paraphrased_bad_behavior(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_file(
                root,
                fixture_document(
                    fixture(
                        forbidden_output_patterns=[
                            r"(?is)(external|web).{0,80}(used|searched).{0,80}(private|manuscript)",
                        ]
                    )
                ),
            )
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (outputs_dir / "compact-routing.md").write_text(
                "\n".join([
                    "Selected skill: research-intent-router.",
                    "Source basis: user prompt only.",
                    "What I can verify: the route.",
                    "What remains uncertain: source details.",
                    "User verification needed: provide sources.",
                    "How to use this result: TRIAGE ONLY - Pick the next step.",
                    "Next action: Use the smallest route.",
                    "The web was searched with the private manuscript wording.",
                ]),
                encoding="utf-8",
            )

            errors = validate_fixture_outputs(fixture_path, outputs_dir)

            self.assertIn(
                "compact-routing: matches forbidden output pattern "
                "'(?is)(external|web).{0,80}(used|searched).{0,80}(private|manuscript)'",
                errors,
            )

    def test_optional_output_patterns_must_be_compilable_string_lists(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_file(
                root,
                fixture_document(
                    {
                        **fixture(),
                        "required_output_patterns": ["("],
                        "forbidden_output_patterns": [42],
                    }
                ),
            )

            errors = validate_fixture_document(fixture_path)

            self.assertIn("compact-routing: forbidden_output_patterns must be a string list when present", errors)
            self.assertIn("compact-routing: invalid required_output_patterns regex '('", errors)

    def test_high_risk_fixture_requires_overstatement_policy_markers(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_file(root, fixture_document(high_risk_fixture()))

            errors = validate_fixture_document(fixture_path)

            for marker in OVERSTATEMENT_POLICY_REQUIRED_MARKERS:
                self.assertIn(
                    (
                        "thin-corpus-consensus-overclaim: high-risk overstatement policy "
                        f"requires required marker {marker!r}"
                    ),
                    errors,
                )

    def test_low_risk_fixture_does_not_require_overstatement_policy_markers(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            low_risk_fixture = fixture(
                fixture_id="low-risk-routing",
                expected_route="research-intent-router",
                risk_covered="low-risk route triage",
                required_markers=["Best route"],
                forbidden_claims=["source verified"],
            )
            fixture_path = write_fixture_file(root, fixture_document(low_risk_fixture))

            self.assertEqual(validate_fixture_document(fixture_path), [])

    def test_high_risk_output_reports_missing_uncertainty_marker(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_file(
                root,
                fixture_document(
                    high_risk_fixture(
                        required_markers=OVERSTATEMENT_POLICY_REQUIRED_MARKERS,
                        forbidden_claims=["field consensus is settled"],
                    )
                ),
            )
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (outputs_dir / "thin-corpus-consensus-overclaim.md").write_text(
                "\n".join([
                    "Selected skill: literature-review-mapper.",
                    "Source basis: two supplied abstracts.",
                    "User verification needed: run a broader search.",
                ]),
                encoding="utf-8",
            )

            errors = validate_fixture_outputs(fixture_path, outputs_dir)

            self.assertIn(
                "thin-corpus-consensus-overclaim: missing required marker 'What remains uncertain'",
                errors,
            )

    def test_high_risk_output_checks_reusable_policy_forbidden_claims(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_file(
                root,
                fixture_document(
                    high_risk_fixture(
                        required_markers=OVERSTATEMENT_POLICY_REQUIRED_MARKERS,
                        forbidden_claims=["field consensus is settled"],
                    )
                ),
            )
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (outputs_dir / "thin-corpus-consensus-overclaim.md").write_text(
                "\n".join([
                    "Selected skill: literature-review-mapper.",
                    "Source basis: abstract only.",
                    "What I can verify: the source topic.",
                    "What remains uncertain: method and evidence.",
                    "User verification needed: read the full source.",
                    "Abstract proves causation.",
                ]),
                encoding="utf-8",
            )

            errors = validate_fixture_outputs(fixture_path, outputs_dir)

            self.assertIn(
                "thin-corpus-consensus-overclaim: contains forbidden claim 'abstract proves causation'",
                errors,
            )

    def test_missing_selected_skill_route_evidence_fails(self) -> None:
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

            errors = validate_fixture_outputs(fixture_path, outputs_dir)

            self.assertIn(
                "compact-routing: missing selected skill route evidence 'research-intent-router'",
                errors,
            )

    def test_forbidden_claim_fails(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_file(root, fixture_document(fixture()))
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (outputs_dir / "compact-routing.md").write_text(
                "\n".join([
                    "Source basis: user prompt only.",
                    "Selected skill: research-intent-router.",
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

    def test_fixture_id_cannot_escape_outputs_dir(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_file(root, fixture_document(fixture("../secret")))
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (root / "secret.md").write_text(
                "\n".join([
                    "Source basis: user prompt only.",
                    "Selected skill: research-intent-router.",
                    "How to use this result: TRIAGE ONLY - Pick the next step.",
                    "Next action: Use the smallest route.",
                ]),
                encoding="utf-8",
            )

            document_errors = validate_fixture_document(fixture_path)
            output_errors = validate_fixture_outputs(fixture_path, outputs_dir)
            unsafe_output_path = output_path_for_fixture(outputs_dir, fixture("../secret")).resolve()

            self.assertIn("../secret: id must be lowercase kebab-case", document_errors)
            self.assertEqual(output_errors, document_errors)
            self.assertTrue(unsafe_output_path.is_relative_to(outputs_dir.resolve()))

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
                    "Selected skill: research-intent-router.",
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

    def test_cli_checks_outputs_dir_flag(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            fixture_path = write_fixture_file(root, fixture_document(fixture()))
            outputs_dir = root / "outputs"
            outputs_dir.mkdir()
            (outputs_dir / "compact-routing.md").write_text(
                "\n".join([
                    "Source basis: user prompt only.",
                    "Selected skill: research-intent-router.",
                    "How to use this result: TRIAGE ONLY - Pick the next step.",
                    "Next action: Use the smallest route.",
                ]),
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--fixtures", str(fixture_path), "--outputs-dir", str(outputs_dir)],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, msg=f"stdout={result.stdout} stderr={result.stderr}")
            self.assertIn("OK: research behavior fixtures are valid.", result.stdout)


if __name__ == "__main__":
    unittest.main()
