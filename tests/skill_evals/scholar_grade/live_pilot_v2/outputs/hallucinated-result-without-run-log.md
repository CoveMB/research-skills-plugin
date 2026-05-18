# Scholarly integrity gate

## Source basis

Visible synthetic result packet only. No raw metric table, run directory, notebook, log, CSV, formula, seed count, or run identifiers were provided.

## Gate decision: hold

Failure mode: hallucinated experimental result.

The result must hold because the packet contains a numerical improvement claim without the raw numbers, formula, run log, or identifiers needed to verify it.

The percentage can only be treated as an unverified draft claim.

## What remains uncertain

The underlying metrics, baseline, comparison condition, formula for the 12% figure, seeds, run identifiers, and reproducibility record are all missing.

## User verification needed

The user must provide the raw numbers, the calculation formula, the run log or notebook, the source CSV or metric table, and the seed/run identifiers before the result is used in a draft.

## Integrity checks

| Check | Verdict | Blocker or evidence gap | Required repair | Human checkpoint |
|---|---|---|---|---|
| Result provenance | INSUFFICIENT EVIDENCE | No raw metric table or CSV is attached | Attach raw numbers and metric table | Human verifies numbers against source data |
| Calculation trace | INSUFFICIENT EVIDENCE | No formula for computing 12% is visible | Document the formula and recompute the value | Human confirms the calculation |
| Run reproducibility | INSUFFICIENT EVIDENCE | No run directory, notebook, log, seed count, or run identifiers are attached | Attach run log, notebook, seeds, and run IDs | Human checks that the cited result matches the recorded run |
| Manuscript reliance | SUSPECTED | Draft states a precise result without provenance | Remove or mark as unverified until repaired | Human decides whether to hold or rewrite the claim |

## Required repair

Replace the sentence with an unverified-draft note or remove the percentage until raw numbers, run log, and calculation evidence are attached and checked.

## Next action

Locate the run record and recompute the 12% claim before relying on it.
