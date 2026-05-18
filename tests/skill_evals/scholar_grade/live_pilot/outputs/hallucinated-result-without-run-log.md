# Scholarly integrity gate

## Source basis

Controlled packet only. The visible packet contains a draft result sentence claiming a 12% accuracy improvement, but no raw metric table, run directory, notebook, log, CSV, formula, seed count, or run identifiers are attached.

## What I can verify

- The draft contains the sentence: "The intervention improved accuracy by 12%."
- The packet provides no raw numbers or saved run log.
- The packet provides no formula for computing the percentage.

## What remains uncertain

- Whether the 12% value was computed correctly.
- Which runs, seeds, or datasets produced the result.
- Whether the intervention improved accuracy at all.
- Whether the metric was absolute or relative.

## User verification needed

Provide raw metrics, run logs, identifiers, computation formula, and notebook/CSV evidence before using the result in a manuscript claim.

## Workflow stage under review

Result-bearing artifact intended to support a draft manuscript claim.

## Integrity checks

| Check | Verdict | Evidence visible | Risk | Required repair | Human checkpoint |
|---|---|---|---|---|---|
| Result provenance | INSUFFICIENT EVIDENCE | Draft result sentence only | The 12% value could be hallucinated or copied from an untracked run | Attach raw metric table and run identifiers | Human must verify the source of the number |
| Computation logic | INSUFFICIENT EVIDENCE | No formula supplied | Absolute/relative improvement may be miscomputed | Record formula and recompute from raw numbers | Human must approve recomputation |
| Reproducibility | INSUFFICIENT EVIDENCE | No notebook, log, CSV, run directory, or seed count | Result cannot be reproduced or audited | Attach run log, notebook, CSV, and seed/run metadata | Human must confirm artifact chain |
| Manuscript readiness | SUSPECTED | The draft advances a precise quantitative result without support | Unsupported result may enter the manuscript | Remove or hold the 12% claim until provenance exists | Human checkpoint required before draft use |

## Gate decision

Hold. The 12% accuracy-improvement claim cannot be used as a manuscript result from the visible packet.

## OVERRIDDEN decisions, if any

None visible.

## Repair priorities

1. Recover the raw metric table and run log.
2. Record the formula and run identifiers.
3. Recompute the percentage.
4. Replace the draft sentence with a provenance-limited note until verified.

## Limits / failure risks

This gate does not verify any result. It only evaluates whether the visible workflow evidence is sufficient to support the draft claim.
