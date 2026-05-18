#!/usr/bin/env python3
"""Report inter-rater agreement and repeated live-run stability."""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from itertools import chain
from pathlib import Path
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[4]
SCHOLAR_GRADE_DIR = ROOT / "tests" / "skill_evals" / "scholar_grade"
DEFAULT_FIXTURES = SCHOLAR_GRADE_DIR / "fixtures.json"
DEFAULT_PANEL_DIR = SCHOLAR_GRADE_DIR / "interrater"

RESERVED_PANEL_DIRECTORIES = {"adjudicated", "agreement_reports", "__pycache__"}
LIVE_CAPTURE_MODES = {"manual-live-capture", "automated-live-capture"}
CRITICAL_DIMENSION_KEYWORDS = (
    "citation",
    "claim/evidence",
    "consensus",
    "fabrication",
    "locator",
    "meaning",
    "privacy",
    "private",
    "quote",
    "rights",
    "clearance",
)
SESSION_KEYS = ("session_id", "session", "capture_session", "run_session", "run_id")
CITATION_FABRICATION_KEYS = (
    "citation_fabrication_count",
    "citation_fabrication",
    "citation_fabrication_detected",
    "fabricated_citation_count",
)
UNSUPPORTED_CLAIM_KEYS = (
    "unsupported_claim_count",
    "unsupported_claim",
    "unsupported_claim_detected",
    "unsupported_claims_count",
)
PRIVACY_BOUNDARY_FAILURE_KEYS = (
    "privacy_boundary_failure_count",
    "privacy_boundary_failure",
    "privacy_boundary_failed",
    "private_material_submitted",
)


def read_json_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return payload


def round_metric(value: float | None) -> float | None:
    return None if value is None else round(value, 4)


def mean(values: Sequence[float]) -> float | None:
    if not values:
        return None
    return sum(values) / len(values)


def numeric_score(value: Any) -> float | None:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if 0 <= float(value) <= 5:
            return float(value)
    return None


def numeric_dimension_scores(score_document: dict[str, Any]) -> dict[str, float]:
    dimension_scores = score_document.get("dimension_scores")
    if not isinstance(dimension_scores, dict):
        return {}
    return {
        str(dimension): score
        for dimension, value in dimension_scores.items()
        for score in [numeric_score(value)]
        if isinstance(dimension, str) and score is not None
    }


def fixture_records(fixtures_path: Path) -> dict[str, dict[str, Any]]:
    document = read_json_object(fixtures_path)
    fixtures = document.get("fixtures")
    if not isinstance(fixtures, list):
        return {}
    return {
        fixture["id"]: fixture
        for fixture in fixtures
        if isinstance(fixture, dict) and isinstance(fixture.get("id"), str)
    }


def score_json_paths(scores_dir: Path) -> list[Path]:
    if not scores_dir.is_dir():
        return []
    return sorted(path for path in scores_dir.glob("*.json") if path.is_file())


def score_fixture_id(path: Path, score_document: dict[str, Any]) -> str:
    fixture_id = score_document.get("fixture_id")
    if isinstance(fixture_id, str) and fixture_id.strip():
        return fixture_id
    return path.stem


def scores_by_fixture(scores_dir: Path) -> dict[str, dict[str, Any]]:
    return {
        score_fixture_id(path, score_document): score_document
        for path in score_json_paths(scores_dir)
        for score_document in [read_json_object(path)]
    }


def reviewer_score_documents(panel_dir: Path) -> dict[str, dict[str, dict[str, Any]]]:
    if not panel_dir.is_dir():
        return {}

    reviewer_directories = [
        child
        for child in sorted(panel_dir.iterdir())
        if child.is_dir() and child.name not in RESERVED_PANEL_DIRECTORIES
    ]
    reviewer_documents = {
        reviewer_dir.name: scores_by_fixture(reviewer_dir)
        for reviewer_dir in reviewer_directories
    }
    return {
        reviewer: documents
        for reviewer, documents in reviewer_documents.items()
        if documents
    }


def adjudicated_fixture_ids(panel_dir: Path) -> set[str]:
    return set(scores_by_fixture(panel_dir / "adjudicated"))


def reviewed_fixture_ids(reviewer_documents: dict[str, dict[str, dict[str, Any]]]) -> list[str]:
    return sorted(set(chain.from_iterable(documents for documents in reviewer_documents.values())))


def fixture_reviewer_count(
    reviewer_documents: dict[str, dict[str, dict[str, Any]]],
    fixture_id: str,
) -> int:
    return sum(1 for documents in reviewer_documents.values() if fixture_id in documents)


def fixtures_with_one_reviewer(reviewer_documents: dict[str, dict[str, dict[str, Any]]]) -> list[str]:
    return [
        fixture_id
        for fixture_id in reviewed_fixture_ids(reviewer_documents)
        if fixture_reviewer_count(reviewer_documents, fixture_id) == 1
    ]


def hard_fail_value(score_document: dict[str, Any]) -> bool | None:
    value = score_document.get("hard_fail_triggered")
    return value if isinstance(value, bool) else None


def hard_fail_disagreements(
    reviewer_documents: dict[str, dict[str, dict[str, Any]]],
) -> list[dict[str, Any]]:
    disagreements: list[dict[str, Any]] = []
    for fixture_id in reviewed_fixture_ids(reviewer_documents):
        reviewer_values = {
            reviewer: value
            for reviewer, documents in sorted(reviewer_documents.items())
            if fixture_id in documents
            for value in [hard_fail_value(documents[fixture_id])]
            if value is not None
        }
        if set(reviewer_values.values()) == {False, True}:
            disagreements.append(
                {
                    "fixture_id": fixture_id,
                    "reviewer_values": reviewer_values,
                }
            )
    return disagreements


def dimension_score_differences(
    reviewer_documents: dict[str, dict[str, dict[str, Any]]],
) -> tuple[list[dict[str, Any]], dict[str, float]]:
    differences: list[dict[str, Any]] = []
    differences_by_dimension: dict[str, list[float]] = defaultdict(list)

    for fixture_id in reviewed_fixture_ids(reviewer_documents):
        reviewer_dimensions = {
            reviewer: numeric_dimension_scores(documents[fixture_id])
            for reviewer, documents in sorted(reviewer_documents.items())
            if fixture_id in documents
        }
        dimensions = sorted(set(chain.from_iterable(reviewer_dimensions.values())))
        for dimension in dimensions:
            reviewer_scores = {
                reviewer: scores[dimension]
                for reviewer, scores in reviewer_dimensions.items()
                if dimension in scores
            }
            if len(reviewer_scores) < 2:
                continue
            difference = max(reviewer_scores.values()) - min(reviewer_scores.values())
            differences_by_dimension[dimension].append(difference)
            if difference > 0:
                differences.append(
                    {
                        "fixture_id": fixture_id,
                        "dimension": dimension,
                        "difference": round_metric(difference),
                        "reviewer_scores": {
                            reviewer: round_metric(score)
                            for reviewer, score in reviewer_scores.items()
                        },
                    }
                )

    average_by_dimension = {
        dimension: round_metric(mean(values))
        for dimension, values in sorted(differences_by_dimension.items())
    }
    return differences, average_by_dimension


def critical_dimension_names(fixture: dict[str, Any], critical_keywords: Sequence[str]) -> set[str]:
    dimensions = fixture.get("rubric_dimensions")
    if not isinstance(dimensions, list):
        return set()
    normalized_keywords = tuple(keyword.lower() for keyword in critical_keywords)
    return {
        dimension
        for dimension in dimensions
        if isinstance(dimension, str)
        and any(keyword in dimension.lower() for keyword in normalized_keywords)
    }


def minimum_score_for_fixture(fixture: dict[str, Any]) -> float:
    score = numeric_score(fixture.get("minimum_score"))
    return 4.0 if score is None else score


def critical_dimension_below_threshold(
    fixtures: dict[str, dict[str, Any]],
    reviewer_documents: dict[str, dict[str, dict[str, Any]]],
    critical_keywords: Sequence[str],
) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    for fixture_id in reviewed_fixture_ids(reviewer_documents):
        fixture = fixtures.get(fixture_id, {})
        threshold = minimum_score_for_fixture(fixture)
        critical_dimensions = critical_dimension_names(fixture, critical_keywords)
        for reviewer, documents in sorted(reviewer_documents.items()):
            scores = numeric_dimension_scores(documents.get(fixture_id, {}))
            for dimension in sorted(critical_dimensions):
                score = scores.get(dimension)
                if score is not None and score < threshold:
                    failures.append(
                        {
                            "fixture_id": fixture_id,
                            "reviewer": reviewer,
                            "dimension": dimension,
                            "score": round_metric(score),
                            "threshold": round_metric(threshold),
                        }
                    )
    return failures


def fixture_ids_with_dimension_disagreement(differences: list[dict[str, Any]]) -> set[str]:
    return {
        str(difference["fixture_id"])
        for difference in differences
        if difference.get("difference") not in (None, 0)
    }


def missing_adjudications(
    hard_fail_items: list[dict[str, Any]],
    dimension_differences: list[dict[str, Any]],
    adjudicated_ids: set[str],
) -> list[str]:
    disagreement_ids = {
        str(item["fixture_id"])
        for item in hard_fail_items
    } | fixture_ids_with_dimension_disagreement(dimension_differences)
    return sorted(fixture_id for fixture_id in disagreement_ids if fixture_id not in adjudicated_ids)


def build_interrater_report(
    fixtures: dict[str, dict[str, Any]],
    panel_dir: Path,
    critical_keywords: Sequence[str] = CRITICAL_DIMENSION_KEYWORDS,
) -> dict[str, Any]:
    reviewer_documents = reviewer_score_documents(panel_dir)
    dimension_differences, average_by_dimension = dimension_score_differences(reviewer_documents)
    hard_fail_items = hard_fail_disagreements(reviewer_documents)
    adjudication_missing = missing_adjudications(
        hard_fail_items,
        dimension_differences,
        adjudicated_fixture_ids(panel_dir),
    )
    critical_failures = critical_dimension_below_threshold(
        fixtures,
        reviewer_documents,
        critical_keywords,
    )
    one_reviewer_only = fixtures_with_one_reviewer(reviewer_documents)
    return {
        "panel_dir": str(panel_dir),
        "reviewers": sorted(reviewer_documents),
        "reviewed_fixture_count": len(reviewed_fixture_ids(reviewer_documents)),
        "fixtures_with_one_reviewer": one_reviewer_only,
        "hard_fail_disagreements": hard_fail_items,
        "dimension_score_differences": dimension_differences,
        "average_difference_by_dimension": average_by_dimension,
        "adjudication_missing": adjudication_missing,
        "critical_dimension_below_threshold": critical_failures,
        "ready": not any([one_reviewer_only, hard_fail_items, adjudication_missing, critical_failures]),
        "limits": [
            "Inter-rater reporting summarizes recorded reviewer scores; it does not replace expert review.",
            "Missing reviewer panels are tolerated by default so existing score files remain valid.",
        ],
    }


def discover_live_roots(base_dir: Path = SCHOLAR_GRADE_DIR) -> list[Path]:
    if not base_dir.is_dir():
        return []
    return sorted(
        {
            manifests_dir.parent
            for manifests_dir in base_dir.rglob("manifests")
            if (manifests_dir.parent / "scores").is_dir()
        }
    )


def score_for_manifest(scores_dir: Path, manifest_path: Path, fixture_id: str) -> dict[str, Any]:
    stem_match = scores_dir / f"{manifest_path.stem}.json"
    fixture_match = scores_dir / f"{fixture_id}.json"
    if stem_match.exists():
        return read_json_object(stem_match)
    if fixture_match.exists():
        return read_json_object(fixture_match)
    return {}


def live_session_id(manifest: dict[str, Any], live_root: Path) -> str:
    for key in SESSION_KEYS:
        value = manifest.get(key)
        if isinstance(value, str) and value.strip():
            return value
    fallback_parts = [
        live_root.name,
        str(manifest.get("date") or "unknown-date"),
        str(manifest.get("interface") or "unknown-interface"),
        str(manifest.get("operator") or "unknown-operator"),
    ]
    return ":".join(fallback_parts)


def is_live_manifest(manifest: dict[str, Any]) -> bool:
    return manifest.get("capture_mode") in LIVE_CAPTURE_MODES


def live_run_records(live_roots: Iterable[Path]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for live_root in live_roots:
        manifests_dir = live_root / "manifests"
        scores_dir = live_root / "scores"
        if not manifests_dir.is_dir():
            continue
        for manifest_path in sorted(manifests_dir.glob("*.json")):
            manifest = read_json_object(manifest_path)
            if not is_live_manifest(manifest):
                continue
            fixture_id = manifest.get("fixture_id")
            if not isinstance(fixture_id, str) or not fixture_id.strip():
                continue
            score = score_for_manifest(scores_dir, manifest_path, fixture_id)
            records.append(
                {
                    "root": str(live_root),
                    "fixture_id": fixture_id,
                    "model": str(manifest.get("model") or "unknown-model"),
                    "session": live_session_id(manifest, live_root),
                    "manifest": manifest,
                    "score": score,
                }
            )
    return records


def nested_sources(record: dict[str, Any]) -> list[dict[str, Any]]:
    manifest = record["manifest"]
    score = record["score"]
    sources = [manifest, score]
    for document in [manifest, score]:
        structured_result = document.get("structured_result")
        if isinstance(structured_result, dict):
            sources.append(structured_result)
    return sources


def value_count(value: Any) -> int | None:
    if isinstance(value, bool):
        return 1 if value else 0
    if isinstance(value, int) and not isinstance(value, bool):
        return max(0, value)
    return None


def optional_failure_count(records: list[dict[str, Any]], keys: Sequence[str]) -> int | None:
    total = 0
    found = False
    for record in records:
        record_found = False
        for source in nested_sources(record):
            for key in keys:
                if key not in source:
                    continue
                count = value_count(source[key])
                if count is None:
                    continue
                total += count
                found = True
                record_found = True
                break
            if record_found:
                break
    return total if found else None


def record_hard_fail_triggered(record: dict[str, Any]) -> bool:
    score_hard_fail = hard_fail_value(record["score"])
    structured_result = record["manifest"].get("structured_result")
    manifest_hard_fail = (
        structured_result.get("hard_fail_triggered")
        if isinstance(structured_result, dict)
        else None
    )
    return score_hard_fail is True or manifest_hard_fail is True


def record_dimension_values(record: dict[str, Any]) -> list[float]:
    return list(numeric_dimension_scores(record["score"]).values())


def grouped_live_records(records: list[dict[str, Any]]) -> dict[tuple[str, str, str], list[dict[str, Any]]]:
    groups: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        groups[(record["fixture_id"], record["model"], record["session"])].append(record)
    return groups


def stability_row(fixture_id: str, model: str, session: str, records: list[dict[str, Any]]) -> dict[str, Any]:
    hard_fail_count = sum(1 for record in records if record_hard_fail_triggered(record))
    dimension_values = list(chain.from_iterable(record_dimension_values(record) for record in records))
    run_count = len(records)
    return {
        "fixture_id": fixture_id,
        "model": model,
        "session": session,
        "run_count": run_count,
        "hard_fail_count": hard_fail_count,
        "hard_fail_rate": round_metric(hard_fail_count / run_count if run_count else None),
        "worst_dimension_score": round_metric(min(dimension_values) if dimension_values else None),
        "average_dimension_score": round_metric(mean(dimension_values)),
        "citation_fabrication_count": optional_failure_count(records, CITATION_FABRICATION_KEYS),
        "unsupported_claim_count": optional_failure_count(records, UNSUPPORTED_CLAIM_KEYS),
        "privacy_boundary_failure_count": optional_failure_count(records, PRIVACY_BOUNDARY_FAILURE_KEYS),
    }


def build_live_run_stability_report(live_roots: Sequence[Path]) -> dict[str, Any]:
    records = live_run_records(live_roots)
    grouped_records = grouped_live_records(records)
    runs = [
        stability_row(fixture_id, model, session, grouped_records[(fixture_id, model, session)])
        for fixture_id, model, session in sorted(grouped_records)
    ]
    return {
        "live_roots": [str(path) for path in live_roots],
        "run_group_count": len(runs),
        "runs": runs,
        "limits": [
            "Live-run stability reports recorded captures only; it does not run models.",
            "Worst-case hard fails and worst dimension scores must be read alongside averages.",
        ],
    }


def strict_failures(report: dict[str, Any]) -> list[str]:
    interrater = report["interrater"]
    interrater_failure_fields = (
        ("fixtures_with_one_reviewer", "fixtures have only one reviewer"),
        ("hard_fail_disagreements", "reviewers disagree on hard_fail"),
        ("adjudication_missing", "adjudication is missing for disagreements"),
        ("critical_dimension_below_threshold", "critical dimensions are below threshold"),
    )
    failures = [
        label
        for field, label in interrater_failure_fields
        if interrater[field]
    ]
    if any(row["hard_fail_count"] > 0 for row in report["live_run_stability"]["runs"]):
        failures.append("live runs include hard failures")
    return failures


def build_report(
    fixtures_path: Path = DEFAULT_FIXTURES,
    panel_dir: Path = DEFAULT_PANEL_DIR,
    live_roots: Sequence[Path] | None = None,
    critical_keywords: Sequence[str] = CRITICAL_DIMENSION_KEYWORDS,
) -> dict[str, Any]:
    fixtures = fixture_records(fixtures_path)
    resolved_live_roots = list(discover_live_roots(SCHOLAR_GRADE_DIR) if live_roots is None else live_roots)
    report = {
        "schema_version": "scholar-grade-interrater-report-v1",
        "source": {
            "fixtures": str(fixtures_path),
            "panel_dir": str(panel_dir),
            "live_roots": [str(path) for path in resolved_live_roots],
        },
        "interrater": build_interrater_report(fixtures, panel_dir, critical_keywords),
        "live_run_stability": build_live_run_stability_report(resolved_live_roots),
        "limits": [
            "Inter-rater reporting does not replace expert review.",
            "Average scores must not hide hard fails.",
            "Worst-case behavior matters more than averages for citation, privacy, and fabrication risks.",
        ],
    }
    report["strict_failures"] = strict_failures(report)
    report["ready"] = not report["strict_failures"]
    return report


def bullet_list(values: Sequence[str]) -> list[str]:
    return [f"- `{value}`" for value in values] if values else ["- None"]


def format_markdown(report: dict[str, Any]) -> str:
    interrater = report["interrater"]
    stability = report["live_run_stability"]
    lines = [
        "# Scholar-Grade Inter-Rater and Stability Report",
        "",
        f"Ready: `{str(report['ready']).lower()}`",
        "",
        "## Inter-rater Review",
        f"- Panel: `{interrater['panel_dir']}`",
        f"- Reviewers: {', '.join(f'`{reviewer}`' for reviewer in interrater['reviewers']) or 'None'}",
        f"- Reviewed fixtures: `{interrater['reviewed_fixture_count']}`",
        "",
        "### Fixtures with one reviewer",
        *bullet_list(interrater["fixtures_with_one_reviewer"]),
        "",
        "### Hard-fail disagreements",
    ]
    if interrater["hard_fail_disagreements"]:
        lines.extend(
            f"- `{item['fixture_id']}`: {item['reviewer_values']}"
            for item in interrater["hard_fail_disagreements"]
        )
    else:
        lines.append("- None")
    lines.extend(["", "### Dimension score differences"])
    if interrater["dimension_score_differences"]:
        lines.extend(
            (
                f"- `{item['fixture_id']}` `{item['dimension']}`: "
                f"difference `{item['difference']}` from {item['reviewer_scores']}"
            )
            for item in interrater["dimension_score_differences"]
        )
    else:
        lines.append("- None")
    lines.extend(["", "### Average difference by dimension"])
    if interrater["average_difference_by_dimension"]:
        lines.extend(
            f"- `{dimension}`: `{difference}`"
            for dimension, difference in interrater["average_difference_by_dimension"].items()
        )
    else:
        lines.append("- None")
    lines.extend(
        [
            "",
            "### Missing adjudication",
            *bullet_list(interrater["adjudication_missing"]),
            "",
            "### Critical dimension below threshold",
        ]
    )
    if interrater["critical_dimension_below_threshold"]:
        lines.extend(
            (
                f"- `{item['fixture_id']}` `{item['dimension']}` by `{item['reviewer']}`: "
                f"`{item['score']}` below `{item['threshold']}`"
            )
            for item in interrater["critical_dimension_below_threshold"]
        )
    else:
        lines.append("- None")

    lines.extend(["", "## Live-run Stability"])
    if stability["runs"]:
        lines.extend(
            (
                f"- `{row['fixture_id']}` model `{row['model']}` session `{row['session']}`: "
                f"runs `{row['run_count']}`, hard_fail_count `{row['hard_fail_count']}`, "
                f"hard_fail_rate `{row['hard_fail_rate']}`, "
                f"worst_dimension_score `{row['worst_dimension_score']}`, "
                f"average_dimension_score `{row['average_dimension_score']}`, "
                f"citation_fabrication_count `{row['citation_fabrication_count']}`, "
                f"unsupported_claim_count `{row['unsupported_claim_count']}`, "
                f"privacy_boundary_failure_count `{row['privacy_boundary_failure_count']}`"
            )
            for row in stability["runs"]
        )
    else:
        lines.append("- None")
    return "\n".join(lines) + "\n"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", type=Path, default=DEFAULT_FIXTURES)
    parser.add_argument("--panel-dir", type=Path, default=DEFAULT_PANEL_DIR)
    parser.add_argument(
        "--live-root",
        action="append",
        type=Path,
        help="Live capture root with manifests/ and scores/. Repeat to compare roots. Defaults to auto-discovery.",
    )
    parser.add_argument(
        "--critical-keyword",
        action="append",
        default=[],
        help="Additional case-insensitive keyword for critical rubric dimensions.",
    )
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    parser.add_argument("--strict", action="store_true", help="Exit nonzero when reported strict failures exist.")
    parser.add_argument("--quiet", action="store_true", help="Suppress report output and return only status.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    critical_keywords = (*CRITICAL_DIMENSION_KEYWORDS, *args.critical_keyword)
    live_roots = None if args.live_root is None else [path.resolve() for path in args.live_root]
    try:
        report = build_report(
            fixtures_path=args.fixtures.resolve(),
            panel_dir=args.panel_dir.resolve(),
            live_roots=live_roots,
            critical_keywords=critical_keywords,
        )
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"errors": [str(error)]}, indent=2))
        return 1

    if not args.quiet:
        if args.format == "markdown":
            print(format_markdown(report), end="")
        else:
            print(json.dumps(report, indent=2))
    return 1 if args.strict and report["strict_failures"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
