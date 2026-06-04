# Scholarly integrity gate

## Source basis

Controlled packet only: the author used AI-generated summaries to draft source claims; original sources have not been checked by a human; there is no source-note ledger, citation locator record, or override log.

## What I can verify

The workflow is attempting to move AI-summary-derived source claims into a chapter without visible human source checking.

## What remains uncertain

The truth of the claims, source-claim fit, citation metadata, quotation accuracy, page or section locators, and whether any claims were distorted by AI summary error are all unverified.

## User verification needed

A human must check the original sources before these claims are relied on in the chapter. Each retained claim needs a source-note record, locator, source-basis label, and unresolved-risk note if any uncertainty remains.

## Workflow stage under review

Draft source claims moving toward chapter reliance.

## Corpus coverage check

No source corpus, source list, search log, or coverage label is visible. Any consensus, novelty, balance, or absence-of-evidence claim must hold until corpus boundaries and source verification are recorded.

## Integrity checks

| Check | Verdict | Evidence visible | Risk | Required repair | Human checkpoint |
|---|---|---|---|---|---|
| Shortcut reliance | SUSPECTED | AI-generated summaries were used to draft source claims. | Summaries may replace required reading of original sources. | Recheck original sources directly and mark AI summaries as draft aids only. | Human source check required before chapter reliance. |
| Hallucinated evidence | INSUFFICIENT EVIDENCE | Original sources have not been checked. | Claims may cite nonexistent, misstated, or unsupported evidence. | Verify each claim against source text and locator. | Human must confirm source support. |
| Missing human checkpoint | SUSPECTED | Packet says no human has checked the sources. | Stage could advance without accountable verification. | Record verification decision, reviewer, date, and unresolved risks. | Required. |
| Broken claim lineage | INSUFFICIENT EVIDENCE | No source-note ledger or citation locator record exists. | Claims may drift from AI summary to manuscript without traceable support. | Create claim ledger with claim, source, locator, evidence status, and source-basis label. | Human must approve any claim status upgrade. |
| Methodology fabrication | Not applicable | No method, sample, or analysis design is being claimed in the visible packet. | None for this gate. | None. | None. |
| Implementation bug | Not applicable | No code, extraction script, table, or computed result is visible. | None for this gate. | None. | None. |
| Duplicate or recycled result | Not applicable | No figures, tables, or repeated results are visible. | None for this gate. | None. | None. |
| OVERRIDDEN decision | INSUFFICIENT EVIDENCE | No override log exists. | Proceeding despite known unverified sources would be an undocumented override. | Do not override unless decision, reason, owner, and follow-up are recorded. | Required if proceeding before full verification. |

## Gate decision

Hold. The blocker is reliance on AI-summary-derived source claims without human verification of the original sources.

## OVERRIDDEN decisions, if any

| Decision | Override reason | Unresolved risk | Required follow-up |
|---|---|---|---|
| None visible | None visible | Source claims remain unverified. | Do not rely on the claims until source checking is complete. |

## Repair priorities

1. Treat every AI-summary-derived claim as an unverified draft note.
2. Check each original source directly.
3. Create a source-note ledger with locators and evidence status.
4. Only move claims into the chapter after human verification.

## Limits / failure risks

This gate does not verify the actual sources or claims. It only evaluates the visible workflow evidence. The main failure risk is laundering unverified AI summary content into chapter prose as if it had been source-checked.