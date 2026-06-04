# Scholarly integrity gate

## Source basis

Source access level: controlled packet only. Visible material: one draft result sentence claiming “The intervention improved accuracy by 12%.” The packet states that no raw metric table, run directory, notebook, log, CSV, raw numbers, formula, seed count, or run identifiers are attached.

## What I can verify

The artifact is result-bearing. I can verify only that the 12% improvement claim appears in the draft and that the packet provides no result provenance.

## What remains uncertain

The raw numbers, computation formula, run config, seed count, run identifiers, preprocessing, and saved run log are unavailable. I cannot verify whether the 12% value was computed correctly, copied from another run, estimated, fabricated, or generated without evidence.

## User verification needed

Provide the raw metric table, formula for the percentage, run log or notebook/CSV, seed count, and run identifiers before this result is used in manuscript claims.

## Workflow stage under review

Generated or drafted empirical result before reliance in a research output.

## Corpus coverage check

Not applicable. This is not a literature synthesis or corpus-coverage claim.

## Integrity checks

| Check | Verdict | Evidence visible | Risk | Required repair | Human checkpoint |
|---|---|---|---|---|---|
| Hallucinated experimental result | SUSPECTED | A precise 12% accuracy improvement is claimed, but no raw numbers or saved run log are present. | The result may be unsupported or fabricated. | Reconstruct the result from raw numbers and saved run records. | Human must verify the reconstructed calculation before use. |
| Implementation bug | INSUFFICIENT EVIDENCE | No formula, notebook, script, CSV, or run directory is attached. | Calculation, aggregation, parsing, or seed-handling errors cannot be ruled out. | Provide computation logic and rerunnable or inspectable run evidence. | Human review of the calculation is required. |
| Methodology provenance | INSUFFICIENT EVIDENCE | Seed count and run identifiers are missing. | The experiment design and run basis cannot be verified. | Attach run config, seed count, preprocessing details, and run identifiers. | Human must confirm the method matches actual run records. |
| Missing human checkpoint | INSUFFICIENT EVIDENCE | No approval, verification note, or unresolved-risk record is visible. | The claim may advance without documented review. | Record who verified the result, what evidence they checked, and any remaining risk. | Required before forward movement. |

## Gate decision

Hold. This is a result-bearing artifact with missing result provenance. The raw numbers, run log, formula, and run identifiers are absent, so the draft must hold before manuscript reliance. The percentage can only be treated as an unverified draft claim.

## OVERRIDDEN decisions, if any

| Decision | Override reason | Unresolved risk | Required follow-up |
|---|---|---|---|
| None visible | Not applicable | Not applicable | Not applicable |

## Repair priorities

1. Attach raw metric table and saved run log.
2. Provide the formula used to compute the 12% improvement.
3. Add seed count, run identifiers, and run config.
4. Recalculate the percentage and record a human verification checkpoint.

## Limits / failure risks

This gate does not evaluate whether the intervention works. It only finds that the visible packet cannot support the 12% claim. The main failure mode is a hallucinated or unreproducible experimental result being promoted into a manuscript claim without provenance.