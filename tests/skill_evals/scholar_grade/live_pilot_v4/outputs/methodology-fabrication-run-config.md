# Scholarly integrity gate

## Source basis

Controlled packet only. Visible material includes one Draft Methods sentence and explicit absence of attached run config, preprocessing log, and dataset manifest.

## What I can verify

The Methods sentence claims three methods facts: 20 training epochs, a stratified sample of 4,000 documents, and de-duplication before training. The packet states that the run config, preprocessing log, and dataset manifest are absent.

## What remains uncertain

The actual training configuration, sample construction, stratification process, de-duplication step, and dataset size provenance are all unverified.

## User verification needed

Provide the run config, preprocessing log, and dataset manifest, or revise the Methods sentence so it only states what is actually supported.

## Workflow stage under review

Methods-bearing draft claim before reliance in manuscript methods.

## Corpus coverage check

Not applicable. The packet is not making literature consensus, novelty, market coverage, or absence-of-evidence claims.

## Integrity checks

| Check | Verdict | Evidence visible | Risk | Required repair | Human checkpoint |
|---|---|---|---|---|---|
| Methodology fabrication | INSUFFICIENT EVIDENCE | Methods sentence names epochs, sample size, stratification, and de-duplication; matching records are absent. | The Methods section may describe a run that cannot be shown to have occurred as written. | Reconcile the method description with actual run records before reliance. | Human must confirm whether records exist or approve revision/removal. |
| Implementation / configuration provenance | INSUFFICIENT EVIDENCE | Run config is absent. | The 20-epoch setting cannot be verified. | Provide run config or remove the setting. | Human verification required. |
| Preprocessing provenance | INSUFFICIENT EVIDENCE | Preprocessing log is absent. | De-duplication may be fabricated, incomplete, or different from the draft claim. | Provide preprocessing log or revise the claim. | Human verification required. |
| Sample size provenance | INSUFFICIENT EVIDENCE | Dataset manifest is absent. | The 4,000-document stratified sample cannot be verified. | Provide dataset manifest and sampling record. | Human verification required. |
| Missing human checkpoint | INSUFFICIENT EVIDENCE | No approval, rationale, or unresolved-risk record is visible. | The claim could advance despite missing provenance. | Record a checkpoint decision after records are reviewed. | Required before forward movement. |

## Gate decision

Hold. This is a methods provenance gap and possible methodology fabrication. The method description must be reconciled with actual run records before reliance.

## OVERRIDDEN decisions, if any

| Decision | Override reason | Unresolved risk | Required follow-up |
|---|---|---|---|
| None visible | Not applicable | Not applicable | Not applicable |

## Repair priorities

1. Provide the run config for the 20-epoch training claim.
2. Provide the preprocessing log supporting de-duplication.
3. Provide the dataset manifest and sampling record supporting the stratified 4,000-document sample.
4. If records cannot be produced, revise or remove the Methods sentence.

## Limits / failure risks

This gate only evaluates the visible packet. It cannot determine whether the run actually happened, only that the current packet does not support the Methods claim.