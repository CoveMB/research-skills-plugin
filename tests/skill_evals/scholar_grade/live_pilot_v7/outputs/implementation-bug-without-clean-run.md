# Scholarly integrity gate

## Source basis

Controlled packet only: draft claim, failed run record, warning, table status, and listed missing materials from `implementation-bug-without-clean-run`.

## What I can verify

The table is being used to support a chapter claim that parser extraction accuracy improved. The only visible run record has `exit_code=1`, includes `division by zero encountered in metric aggregation`, and the table was copied from the failed run output directory.

## What remains uncertain

Whether the parser improved extraction accuracy is not verified. The aggregation logic, raw numbers, clean run output, script identity, and independent recomputation are unavailable.

## User verification needed

A clean rerun after fixing or explaining the division-by-zero warning, saved script hash, raw metric inputs, and independent recomputation before the table supports the chapter claim.

## Workflow stage under review

Result-bearing artifact intended to support a manuscript or chapter claim.

## Corpus coverage check

Not applicable. This packet concerns computed result provenance, not literature corpus coverage.

## Integrity checks

| Check | Verdict | Evidence visible | Risk | Required repair | Human checkpoint |
|---|---|---|---|---|---|
| Implementation bug | SUSPECTED | Failed run has `exit_code=1` and division-by-zero warning in metric aggregation. | The computed accuracy table may be wrong or incomplete. | Fix or explain aggregation failure, rerun cleanly, and compare outputs. | Human review must confirm the clean rerun before reliance. |
| Result provenance | INSUFFICIENT EVIDENCE | No clean rerun, no saved script hash, no independent recomputation. | The table cannot be traced to a reliable executable state. | Save script hash, run log, raw inputs, and recomputation evidence. | Human checkpoint required before moving into chapter text. |
| Hallucinated evidence | INSUFFICIENT EVIDENCE | Draft claim says Table 2 shows improvement, but visible run is failed. | The improvement claim may be unsupported by valid evidence. | Treat the claim as provisional until recomputed from a clean run. | Human review needed after recomputation. |
| Shortcut reliance | SUSPECTED | Table was copied from the failed run output directory. | Failed output may be used as a shortcut for validated results. | Replace table with output from a clean, reproducible run. | Reviewer must verify replacement source. |
| Methodology fabrication | Not applicable | No method description is being audited here. | None from visible packet. | None. | None. |
| Duplicate or recycled result | Not applicable | No duplicate or recycled table evidence is visible. | None from visible packet. | None. | None. |

## Gate decision

Hold. The table must not support the chapter claim until the metric aggregation warning is resolved, the run exits cleanly, and the result is independently recomputed.

## OVERRIDDEN decisions, if any

| Decision | Override reason | Unresolved risk | Required follow-up |
|---|---|---|---|
| None visible | Not applicable | Not applicable | Not applicable |

## Repair priorities

1. Fix or explain the division-by-zero aggregation warning.
2. Rerun successfully with `exit_code=0`.
3. Save script hash, run log, raw metric inputs, and generated table output.
4. Independently recompute the table before restoring the chapter claim.

## Limits / failure risks

This gate uses only the controlled packet. I cannot verify the code, data, metric formula, or true parser accuracy. The table can only be treated as an unverified draft claim.