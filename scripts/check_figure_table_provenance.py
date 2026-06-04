#!/usr/bin/env python3
"""Check local figure/table provenance records without verifying data truth."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable, NamedTuple

from plugin_utils import (
    read_csv_records as read_csv_record_objects,
    read_json_or_csv_records,
    read_json_records as read_json_record_objects,
    validate_record_objects,
)


JSON_RECORD_ERROR = "JSON input must be a list or an object with a records, figures, tables, or objects list"
EMPTY_RECORD_ERROR = "input must contain at least one figure/table provenance record"
UNKNOWN_RIGHTS_VALUES = {"", "unknown", "unclear", "not specified", "not_specified", "pending", "tbd"}
ACCEPTED_ORIGINS = {"original", "adapted", "reproduced", "generated"}
FIGURE_TYPES_REQUIRING_AXES = {"chart", "graph", "plot", "map"}
QUANTITATIVE_MARKERS = (
    "%",
    "average",
    "confidence",
    "correlation",
    "estimate",
    "interval",
    "mean",
    "median",
    "percentage",
    "proportion",
    "rate",
    "ratio",
    "regression",
    "sample",
    "uncertainty",
)
DENOMINATOR_MARKERS = ("%", "percentage", "proportion", "rate", "ratio", "per ")
SAMPLE_SIZE_MARKERS = ("sample", "respondent", "participant", "survey", "cohort", "n=")
CAPTION_MISMATCH_MARKERS = ("mismatch", "inconsistent", "misleading", "contradict")
CAPTION_UNKNOWN_VALUES = {"", "unknown", "unchecked", "not checked", "not_checked", "unclear"}
NO_GAP_VALUES = {"", "none", "no", "n/a", "na", "resolved"}
TRUE_VALUES = {"true", "yes", "y", "1", "provided", "reproducible"}
FALSE_VALUES = {"false", "no", "n", "0", "not required", "not needed", "waived"}
TRUTH_LIMITS = [
    "This checker validates local provenance structure only.",
    "It does not verify data values, source truth, calculations, rights clearance, or source-claim support.",
    "Data values require supplied source data and reproducible calculation records before truth can be checked.",
]


class Issue(NamedTuple):
    code: str
    severity: str
    message: str


def read_json_records(path: Path) -> list[dict[str, Any]]:
    return read_json_record_objects(
        path,
        container_keys=("records", "figures", "tables", "objects", "figure_table_checks"),
        json_error_message=JSON_RECORD_ERROR,
        empty_error_message=EMPTY_RECORD_ERROR,
    )


def read_csv_records(path: Path) -> list[dict[str, Any]]:
    return read_csv_record_objects(path, empty_error_message=EMPTY_RECORD_ERROR)


def validate_provenance_records(records: list[Any]) -> list[dict[str, Any]]:
    return validate_record_objects(records, empty_error_message=EMPTY_RECORD_ERROR)


def read_records(path: Path) -> list[dict[str, Any]]:
    return read_json_or_csv_records(
        path,
        json_container_keys=("records", "figures", "tables", "objects", "figure_table_checks"),
        json_error_message=JSON_RECORD_ERROR,
        empty_error_message=EMPTY_RECORD_ERROR,
    )


def text_value(record: dict[str, Any], keys: Iterable[str]) -> str:
    for key in keys:
        value = record.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
        if isinstance(value, int):
            return str(value)
        if isinstance(value, float):
            return str(value)
        if isinstance(value, list):
            strings = [str(item).strip() for item in value if str(item).strip()]
            if strings:
                return "; ".join(strings)
    return ""


def normalized(value: Any) -> str:
    return " ".join(str(value).strip().casefold().replace("-", " ").replace("_", " ").split())


def boolish_true(value: Any) -> bool:
    return normalized(value) in TRUE_VALUES


def record_identifier(record: dict[str, Any], index: int = 0) -> str:
    value = text_value(record, ["object_id", "figure_id", "table_id", "id", "record_id"])
    return value or f"object-{index + 1}"


def object_type(record: dict[str, Any]) -> str:
    return normalized(text_value(record, ["object_type", "type", "kind", "visual_type"]))


def combined_claim_text(record: dict[str, Any]) -> str:
    values = (
        text_value(record, keys)
        for keys in (
            ["caption"],
            ["claim_supported", "claim", "manuscript_claim"],
            ["title"],
            ["measure", "metric"],
            ["y_axis_label"],
            ["units"],
        )
    )
    return " ".join(value for value in values if value)


def has_any_marker(value: str, markers: Iterable[str]) -> bool:
    folded = value.casefold()
    return any(marker in folded for marker in markers)


def is_quantitative_record(record: dict[str, Any]) -> bool:
    if object_type(record) in {"chart", "figure", "graph", "plot", "table"}:
        return has_any_marker(combined_claim_text(record), QUANTITATIVE_MARKERS)
    return False


def requires_axis_labels(record: dict[str, Any]) -> bool:
    record_type = object_type(record)
    return record_type in FIGURE_TYPES_REQUIRING_AXES or (
        record_type == "figure" and is_quantitative_record(record)
    )


def denominator_is_relevant(record: dict[str, Any]) -> bool:
    return boolish_true(record.get("requires_denominator")) or has_any_marker(
        combined_claim_text(record),
        DENOMINATOR_MARKERS,
    )


def sample_size_is_relevant(record: dict[str, Any]) -> bool:
    return boolish_true(record.get("requires_sample_size")) or has_any_marker(
        combined_claim_text(record),
        SAMPLE_SIZE_MARKERS,
    )


def uncertainty_is_relevant(record: dict[str, Any]) -> bool:
    return boolish_true(record.get("requires_uncertainty")) or has_any_marker(
        combined_claim_text(record),
        ("confidence", "interval", "uncertainty", "estimate", "mean", "average", "regression"),
    )


def source_data_provided(record: dict[str, Any]) -> bool:
    return boolish_true(record.get("source_data_provided")) or boolish_true(record.get("data_file_provided"))


def calculation_reproducible(record: dict[str, Any]) -> bool:
    return boolish_true(record.get("calculation_reproducible")) or boolish_true(record.get("run_log_provided"))


def data_value_verification_status(record: dict[str, Any]) -> str:
    if source_data_provided(record) and calculation_reproducible(record):
        return "reproducibility_inputs_available"
    if source_data_provided(record):
        return "source_data_available_calculation_not_reproducible"
    return "not_checked"


def has_text(record: dict[str, Any], keys: Iterable[str]) -> bool:
    return bool(text_value(record, keys))


def missing_human_review_requirement(record: dict[str, Any]) -> bool:
    return "human_review_required" not in record and "human_review" not in record


def human_review_value_is_valid(value: Any) -> bool:
    return isinstance(value, bool) or normalized(value) in TRUE_VALUES | FALSE_VALUES


def invalid_human_review_requirement(record: dict[str, Any]) -> bool:
    return any(
        key in record and not human_review_value_is_valid(record.get(key))
        for key in ("human_review_required", "human_review")
    )


def declared_human_review_required(record: dict[str, Any]) -> bool:
    return boolish_true(record.get("human_review_required")) or boolish_true(record.get("human_review"))


def unresolved_gap_values(record: dict[str, Any]) -> list[str]:
    value = record.get("unresolved_provenance_gaps", record.get("provenance_gaps", ""))
    if isinstance(value, list):
        return [str(item).strip() for item in value if normalized(item) not in NO_GAP_VALUES]
    return [str(value).strip()] if normalized(value) not in NO_GAP_VALUES else []


def caption_consistency_issue(record: dict[str, Any]) -> Issue | None:
    status = text_value(record, ["caption_source_consistency", "caption_axis_status", "caption_status"])
    if has_any_marker(status, CAPTION_MISMATCH_MARKERS):
        return Issue(
            "caption_source_mismatch",
            "high",
            "Caption/source consistency is reported as mismatch",
        )
    if normalized(status) in CAPTION_UNKNOWN_VALUES:
        return Issue(
            "caption_source_consistency_unchecked",
            "medium",
            "Caption/source consistency is missing or unchecked",
        )
    return None


def origin_issue(record: dict[str, Any]) -> Issue | None:
    origin = normalized(text_value(record, ["origin", "figure_origin", "table_origin", "reuse_status"]))
    if not origin:
        return Issue("missing_origin", "medium", "Figure/table origin is missing")
    if origin not in ACCEPTED_ORIGINS:
        return Issue("unknown_origin", "medium", "Figure/table origin must be original, adapted, reproduced, or generated")
    return None


def rights_issue(record: dict[str, Any]) -> Issue | None:
    status = normalized(text_value(record, ["rights_status", "license", "licensing_status", "permission_status"]))
    if status in UNKNOWN_RIGHTS_VALUES:
        return Issue("unknown_rights_or_license", "medium", "Rights or licensing status is unknown")
    return None


def generated_without_provenance(record: dict[str, Any]) -> bool:
    origin = normalized(text_value(record, ["origin", "figure_origin", "table_origin", "reuse_status"]))
    if origin != "generated":
        return False
    return not has_text(record, ["data_source", "source", "dataset", "source_pointer"]) or not has_text(
        record,
        ["transformation_notes", "calculation_notes", "method_notes", "processing_notes"],
    )


def base_provenance_issues(record: dict[str, Any], index: int) -> list[Issue]:
    issues: list[Issue] = []
    if record_identifier(record, index).startswith("object-"):
        issues.append(Issue("missing_object_id", "high", "Figure/table ID is missing"))
    if not has_text(record, ["data_source", "source", "dataset", "source_pointer"]):
        issues.append(Issue("missing_data_source", "high", "Data source is missing"))
    if not has_text(record, ["source_access_level", "source_access", "access_level"]):
        issues.append(Issue("missing_source_access_level", "medium", "Source access level is missing"))
    if has_text(record, ["data_source", "source", "dataset", "source_pointer"]) and not has_text(
        record,
        ["date_accessed", "accessed_at", "dataset_version", "data_version", "source_version"],
    ):
        issues.append(Issue("missing_date_accessed_or_dataset_version", "medium", "Date accessed or dataset version is missing"))
    if not has_text(record, ["transformation_notes", "calculation_notes", "method_notes", "processing_notes"]):
        issues.append(Issue("missing_transformation_notes", "medium", "Transformation or calculation notes are missing"))
    if not has_text(record, ["aggregation_level", "aggregation", "level"]):
        issues.append(Issue("missing_aggregation_level", "medium", "Aggregation level is missing"))
    if requires_axis_labels(record):
        if not has_text(record, ["x_axis_label", "axis_x", "x_label"]):
            issues.append(Issue("missing_x_axis_label", "medium", "X-axis label is missing"))
        if not has_text(record, ["y_axis_label", "axis_y", "y_label"]):
            issues.append(Issue("missing_y_axis_label", "medium", "Y-axis label is missing"))
    if is_quantitative_record(record) and not has_text(record, ["units", "unit", "measurement_unit"]):
        issues.append(Issue("missing_units", "medium", "Units are missing for a quantitative figure/table"))
    if denominator_is_relevant(record) and not has_text(record, ["denominator", "base"]):
        issues.append(Issue("missing_denominator_or_sample_size", "medium", "Denominator or rate base is missing"))
    if sample_size_is_relevant(record) and not has_text(record, ["sample_size", "sample", "n"]):
        issues.append(Issue("missing_denominator_or_sample_size", "medium", "Sample size is missing"))
    if uncertainty_is_relevant(record) and not has_text(record, ["uncertainty_notes", "confidence_interval_notes", "ci_notes"]):
        issues.append(Issue("missing_uncertainty_notes", "medium", "Uncertainty or confidence interval notes are missing"))
    if missing_human_review_requirement(record):
        issues.append(Issue("missing_human_review_requirement", "medium", "Human-review requirement is missing"))
    elif invalid_human_review_requirement(record):
        issues.append(
            Issue(
                "invalid_human_review_requirement",
                "medium",
                "Human-review requirement must be a boolean or recognized yes/no value",
            )
        )
    return issues


def provenance_issues(record: dict[str, Any], index: int) -> list[Issue]:
    issues = base_provenance_issues(record, index)
    for optional_issue in (caption_consistency_issue(record), rights_issue(record), origin_issue(record)):
        if optional_issue is not None:
            issues.append(optional_issue)
    if generated_without_provenance(record):
        issues.append(Issue("generated_without_provenance", "high", "Generated figure/table lacks data source or transformation provenance"))
    for gap in unresolved_gap_values(record):
        issues.append(Issue("unresolved_provenance_gap", "medium", f"Unresolved provenance gap: {gap}"))
    return issues


def risk_for_issues(issues: list[Issue]) -> str:
    if any(issue.severity == "high" for issue in issues):
        return "high"
    if any(issue.severity == "medium" for issue in issues):
        return "medium"
    return "low"


def evaluated_record(record: dict[str, Any], index: int) -> dict[str, Any]:
    issues = provenance_issues(record, index)
    review_required = declared_human_review_required(record) or bool(issues)
    return {
        "object_id": record_identifier(record, index),
        "object_type": object_type(record) or "unknown",
        "provenance_status": "provenance_complete" if not issues else "provenance_gaps",
        "risk": risk_for_issues(issues),
        "human_review_required": review_required,
        "data_value_verification_status": data_value_verification_status(record),
        "issues": [
            {"code": issue.code, "severity": issue.severity, "message": issue.message}
            for issue in issues
        ],
        "notes": [issue.message for issue in issues],
    }


def build_report_from_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    evaluated_records = [evaluated_record(record, index) for index, record in enumerate(records)]
    return {
        "schema_version": "figure-table-provenance-check-v1",
        "execution_mode": "deterministic-local",
        "records": evaluated_records,
        "limits": TRUTH_LIMITS,
        "errors": [],
    }


def build_provenance_report(path: Path) -> dict[str, Any]:
    records = read_records(path)
    return build_report_from_records(records)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Local JSON or CSV figure/table provenance export.")
    parser.add_argument("--quiet", action="store_true", help="Suppress JSON output unless validation fails.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        report = build_provenance_report(args.input)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"errors": [str(error)]}, indent=2))
        return 1

    has_gaps = any(record["risk"] in {"medium", "high"} for record in report["records"])
    if not args.quiet or has_gaps:
        print(json.dumps(report, indent=2))
    return 1 if has_gaps else 0


if __name__ == "__main__":
    raise SystemExit(main())
