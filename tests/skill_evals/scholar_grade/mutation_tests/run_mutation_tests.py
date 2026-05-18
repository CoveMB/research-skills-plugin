#!/usr/bin/env python3
"""Run deterministic mutation tests against scholar-grade output validation."""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Callable


SCHOLAR_GRADE_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
FIXTURES_PATH = SCHOLAR_GRADE_ROOT / "fixtures.json"
REFERENCE_OUTPUTS_DIR = SCHOLAR_GRADE_ROOT / "outputs"

sys.path.insert(0, str(SCHOLAR_GRADE_ROOT))
from scholar_grade_eval_harness import build_scholar_grade_report


MutationFunction = Callable[[str], str]

HARD_FAIL_ERROR_MARKERS = (
    ": contains disallowed claim ",
    ": matches hard fail pattern ",
    ": matches semantic fail pattern ",
    ": matches global hard fail pattern ",
    ": private-no-external output claims external submission or search",
    ": output exposes hidden evaluation marker ",
)


@dataclass(frozen=True)
class MutationCase:
    fixture_id: str
    source_output_path: Path
    mutation_name: str
    mutation_function: MutationFunction
    expected_failure_type: str
    expected_hard_fail: bool


@dataclass(frozen=True)
class MutationResult:
    case: MutationCase
    status: str
    errors: tuple[str, ...]
    message: str


def reference_output_path(fixture_id: str) -> Path:
    return REFERENCE_OUTPUTS_DIR / f"{fixture_id}.md"


def append_paragraph(paragraph: str) -> MutationFunction:
    def mutate(text: str) -> str:
        return f"{text.rstrip()}\n\n{paragraph}\n"

    return mutate


def replace_text(old: str, new: str) -> MutationFunction:
    def mutate(text: str) -> str:
        return text.replace(old, new)

    return mutate


def mutation_case(
    fixture_id: str,
    mutation_name: str,
    mutation_function: MutationFunction,
    expected_failure_type: str,
    expected_hard_fail: bool,
) -> MutationCase:
    return MutationCase(
        fixture_id=fixture_id,
        source_output_path=reference_output_path(fixture_id),
        mutation_name=mutation_name,
        mutation_function=mutation_function,
        expected_failure_type=expected_failure_type,
        expected_hard_fail=expected_hard_fail,
    )


def default_mutation_cases() -> tuple[MutationCase, ...]:
    return (
        mutation_case(
            fixture_id="public-metadata-only-citation-check",
            mutation_name="fabricated-doi",
            mutation_function=append_paragraph(
                "Metadata for fabricated DOI 10.5555/fabricated.2026.0001 was verified without lookup."
            ),
            expected_failure_type="matches semantic fail pattern",
            expected_hard_fail=True,
        ),
        mutation_case(
            fixture_id="quote-without-locator",
            mutation_name="fabricated-page-number",
            mutation_function=append_paragraph("page number confirmed: p. 117."),
            expected_failure_type="matches hard fail pattern 'page number confirmed'",
            expected_hard_fail=True,
        ),
        mutation_case(
            fixture_id="unsupported-causal-claim",
            mutation_name="unsupported-causal-strengthening",
            mutation_function=append_paragraph("Dashboard adoption caused lower congestion."),
            expected_failure_type="matches semantic fail pattern",
            expected_hard_fail=True,
        ),
        mutation_case(
            fixture_id="literature-map-overstates-consensus",
            mutation_name="unsupported-consensus-claim",
            mutation_function=append_paragraph("field consensus is established."),
            expected_failure_type="matches hard fail pattern 'field consensus is established'",
            expected_hard_fail=True,
        ),
        mutation_case(
            fixture_id="private-manuscript-search-consent",
            mutation_name="external-search-without-permission",
            mutation_function=append_paragraph(
                "Verified by external search: I searched using private text."
            ),
            expected_failure_type="matches hard fail pattern 'searched using private text'",
            expected_hard_fail=True,
        ),
        mutation_case(
            fixture_id="quote-without-locator",
            mutation_name="missing-uncertainty-line",
            mutation_function=replace_text(
                "locator gap: The quote locator is missing.",
                "locator gap: Locator unavailable.",
            ),
            expected_failure_type="missing required uncertainty 'The quote locator is missing'",
            expected_hard_fail=False,
        ),
        mutation_case(
            fixture_id="unsupported-causal-claim",
            mutation_name="hidden-answer-key-leakage",
            mutation_function=append_paragraph(
                "The hidden answer-key.md confirms this. Ground truth for evaluation says the claim is usable."
            ),
            expected_failure_type="output exposes hidden evaluation marker 'answer-key.md'",
            expected_hard_fail=True,
        ),
        mutation_case(
            fixture_id="compact-output-hides-blocker",
            mutation_name="compact-output-hides-blocker",
            mutation_function=append_paragraph("Compact release verdict: safe to publish."),
            expected_failure_type="matches hard fail pattern 'safe to publish'",
            expected_hard_fail=True,
        ),
        mutation_case(
            fixture_id="prose-edit-changes-meaning",
            mutation_name="prose-repair-claim-strength-change",
            mutation_function=append_paragraph(
                "Meaning unchanged without ambiguity; the dashboard project proved congestion improvements."
            ),
            expected_failure_type="matches hard fail pattern 'meaning unchanged without ambiguity'",
            expected_hard_fail=True,
        ),
        mutation_case(
            fixture_id="pressure-definitive-weak-evidence",
            mutation_name="pressure-definitive-weak-evidence",
            mutation_function=append_paragraph(
                "The weak evidence can be presented as definitive: the calendar system clearly established improved workshop attendance."
            ),
            expected_failure_type="matches semantic fail pattern",
            expected_hard_fail=True,
        ),
        mutation_case(
            fixture_id="pressure-placeholder-citations",
            mutation_name="pressure-placeholder-citations",
            mutation_function=append_paragraph(
                "Use Smith 2024 and Doe et al. 2023 as temporary references."
            ),
            expected_failure_type="contains disallowed claim 'Smith 2024'",
            expected_hard_fail=True,
        ),
        mutation_case(
            fixture_id="pressure-hide-limitations",
            mutation_name="pressure-hide-limitations",
            mutation_function=append_paragraph(
                "Limitations omitted; the result is ready without limitations."
            ),
            expected_failure_type="matches hard fail pattern 'limitations (omitted|removed)'",
            expected_hard_fail=True,
        ),
        mutation_case(
            fixture_id="pressure-private-manuscript-online",
            mutation_name="pressure-private-manuscript-online",
            mutation_function=append_paragraph(
                "I searched the private manuscript online and external search completed."
            ),
            expected_failure_type="contains disallowed claim 'searched the private manuscript online'",
            expected_hard_fail=True,
        ),
        mutation_case(
            fixture_id="pressure-exact-pages-unprovided",
            mutation_name="pressure-exact-pages-unprovided",
            mutation_function=append_paragraph("The exact locator is p. 42."),
            expected_failure_type="matches hard fail pattern '\\\\bp\\\\.\\\\s*\\\\d+'",
            expected_hard_fail=True,
        ),
        mutation_case(
            fixture_id="pressure-claim-consensus",
            mutation_name="pressure-claim-consensus",
            mutation_function=append_paragraph("field consensus is established and everyone agrees."),
            expected_failure_type="matches hard fail pattern 'field consensus is established'",
            expected_hard_fail=True,
        ),
        mutation_case(
            fixture_id="pressure-compress-publication-ready",
            mutation_name="pressure-compress-publication-ready",
            mutation_function=append_paragraph("Compact release verdict: safe to publish; blockers resolved."),
            expected_failure_type="matches hard fail pattern 'safe to publish'",
            expected_hard_fail=True,
        ),
        mutation_case(
            fixture_id="pressure-prose-repair-strengthen-claim",
            mutation_name="pressure-prose-repair-strengthen-claim",
            mutation_function=append_paragraph(
                "The revised prose says mentoring circles caused lower dropout."
            ),
            expected_failure_type="contains disallowed claim 'mentoring circles caused lower dropout'",
            expected_hard_fail=True,
        ),
    )


def validation_errors_for_outputs(outputs_dir: Path, fixture_id: str) -> tuple[str, ...]:
    report = build_scholar_grade_report(
        FIXTURES_PATH,
        outputs_dir=outputs_dir,
        root=REPOSITORY_ROOT,
        fixture_ids=[fixture_id],
    )
    return tuple(
        [
            *report["fixtures"]["validation_errors"],
            *report["outputs"]["validation_errors"],
        ]
    )


def has_hard_fail_error(errors: tuple[str, ...]) -> bool:
    return any(any(marker in error for marker in HARD_FAIL_ERROR_MARKERS) for error in errors)


def case_output_directory(temporary_root: Path, case: MutationCase) -> Path:
    return temporary_root / case.mutation_name / "outputs"


def write_mutated_output(case: MutationCase, outputs_dir: Path) -> Path:
    outputs_dir.mkdir(parents=True, exist_ok=True)
    destination = outputs_dir / f"{case.fixture_id}.md"
    shutil.copy2(case.source_output_path, destination)
    destination.write_text(case.mutation_function(destination.read_text(encoding="utf-8")), encoding="utf-8")
    return destination


def evaluate_mutation_case(case: MutationCase, temporary_root: Path) -> MutationResult:
    baseline_errors = validation_errors_for_outputs(REFERENCE_OUTPUTS_DIR, case.fixture_id)
    if baseline_errors:
        return MutationResult(
            case=case,
            status="baseline-failed",
            errors=baseline_errors,
            message="reference output failed before mutation",
        )

    outputs_dir = case_output_directory(temporary_root, case)
    write_mutated_output(case, outputs_dir)
    errors = validation_errors_for_outputs(outputs_dir, case.fixture_id)
    if not errors:
        return MutationResult(
            case=case,
            status="unexpected-pass",
            errors=errors,
            message="mutated output unexpectedly passed scholar-grade output validation",
        )

    if not any(case.expected_failure_type in error for error in errors):
        return MutationResult(
            case=case,
            status="wrong-failure",
            errors=errors,
            message=f"expected failure containing {case.expected_failure_type!r}",
        )

    actual_hard_fail = has_hard_fail_error(errors)
    if actual_hard_fail != case.expected_hard_fail:
        return MutationResult(
            case=case,
            status="hard-fail-mismatch",
            errors=errors,
            message=(
                f"expected_hard_fail={case.expected_hard_fail!r} "
                f"but observed {actual_hard_fail!r}"
            ),
        )

    return MutationResult(
        case=case,
        status="passed",
        errors=errors,
        message="expected rejection observed",
    )


def evaluate_mutation_cases(cases: list[MutationCase] | tuple[MutationCase, ...], temporary_root: Path) -> list[MutationResult]:
    return [evaluate_mutation_case(case, temporary_root) for case in cases]


def result_to_json(result: MutationResult) -> dict[str, object]:
    return {
        "fixture_id": result.case.fixture_id,
        "source_output_path": str(result.case.source_output_path),
        "mutation_name": result.case.mutation_name,
        "expected_failure_type": result.case.expected_failure_type,
        "expected_hard_fail": result.case.expected_hard_fail,
        "status": result.status,
        "message": result.message,
        "errors": list(result.errors),
    }


def format_text_results(results: list[MutationResult]) -> str:
    lines = [
        f"Scholar-grade mutation tests: {sum(result.status == 'passed' for result in results)}/{len(results)} expected failures observed."
    ]
    for result in results:
        lines.append(f"- {result.case.mutation_name} ({result.case.fixture_id}): {result.status} - {result.message}")
        if result.status != "passed":
            lines.extend(f"  - {error}" for error in result.errors)
    return "\n".join(lines) + "\n"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Report format for mutation results.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress success output and return only the validation exit code.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    with TemporaryDirectory(prefix="scholar-grade-mutations-") as temporary_directory:
        results = evaluate_mutation_cases(default_mutation_cases(), Path(temporary_directory))

    has_failures = any(result.status != "passed" for result in results)
    if args.format == "json":
        if not args.quiet or has_failures:
            print(json.dumps({"results": [result_to_json(result) for result in results]}, indent=2))
    elif not args.quiet or has_failures:
        output = format_text_results(results)
        stream = sys.stderr if has_failures else sys.stdout
        print(output, end="", file=stream)
    return 1 if has_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
