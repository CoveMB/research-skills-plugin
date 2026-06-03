# Research book quality standard

Use this standard whenever a skill plans, searches, audits, drafts, or revises scholarly nonfiction.

## Claim discipline

Every major claim should be classified by evidentiary need: factual, empirical, causal, comparative, conceptual, theoretical, normative, predictive, anecdotal, interpretive, or field-specific.

## Calibrated certainty discipline

The goal is calibrated certainty, not maximum hedging. A strong claim can stay strong when the source basis, method visibility, corpus coverage, locator support, and verification record justify that strength. When those supports are thin, partial, stale, citation-only, abstract-only, one-sided, or method-incomplete, keep the limit visible and push the user toward the smallest needed verification step.

High-risk research outputs should keep source basis, what can be verified, what remains uncertain, and user verification needed visible. They must not turn thin corpora into field-consensus claims, abstracts or summaries into causal certainty, citation-only access into source-support claims, blocker gaps into clearance language, or downstream handoffs into upgraded certainty without an intervening verification step. Novelty and absence-of-evidence claims need a systematic or representative search basis.

## Evidence discipline

Match source type to claim type:

- Empirical claims need empirical studies, data, or credible reports.
- Factual claims need verifiable primary or secondary support.
- Causal claims need stronger evidence than analogy.
- Field-specific claims need sources accepted by the relevant field, not generic support.
- Normative claims need argument rather than citation alone.

## Source-note discipline

Keep summary, paraphrase, direct quotation, and interpretation separate. Direct quotes and passage-specific claims need locators, or the gap must stay visible.

## Accessibility discipline

When spelling, dictation, rough fragments, dense material, or reading fatigue shape the task, reduce text load before adding scholarly complexity. Preserve the author's meaning, mark only ambiguities that affect claims or evidence, and prefer short tables with one next action. Use specific accessibility skills for clear bottlenecks: spoken input, reading triage, or prose repair.

Compact output is an output shape, not a route mode. When requested, use one source-basis line, one table or revised passage, ambiguity only when it could change meaning, and one next action. In routing, audit, gate, or verifier work, compact output must keep the main route or verdict, decision-changing gaps, and one next action visible.

Every compact result must include `How to use this result: [status] - [full sentence]`. Use `TRIAGE ONLY` when the result only helps choose the next step, `BLOCKER SUMMARY` when it lists visible blockers without clearing the work, and `LIMITED GATE DECISION` when it gives a constrained proceed/hold/repair decision from visible evidence and stated limits. These statuses are compact-output-only; full reports should keep the fuller source-basis, verification, uncertainty, and user-check sections. Escalate from compact output to full review before the result supports manuscript claims, external release, legal/privacy decisions, citation verification, method credibility, or final submission.

## Extraction discipline

Do not synthesize before extraction is even enough to compare sources. Empty fields are better than guessed fields.

## Citation discipline

Never invent citations, page numbers, quotes, DOIs, or bibliographic metadata. If a citation cannot be verified from available material, mark it as unverified.

## Traceability discipline

A claim should trace to a source note, citekey, locator, or repair task. A nearby citation is not proof that the source supports the claim.

## Figure and table discipline

Figures, tables, charts, screenshots, and image panels need data provenance, caption/axis checks, duplicate visual review, and rights status before they support factual, empirical, comparative, or quantitative claims.

## AI/human workflow discipline

AI-assisted research, generated synthesis, automated extraction, or computed results need an integrity gate before manuscript reliance. Human checkpoints should record decisions, override reasons, unresolved risks, affected sections, and disclosure notes when external sharing or submission is likely.

Use a `process_passport` in machine-readable artifacts when a result will be handed to another skill, reviewer, or submission workflow. The schema keeps this field structurally optional so drafts and partial fixtures can validate before they become handoff artifacts. When present, it should name the stage, inputs, tool use, gate status, human checkpoints, and handoff limits without turning fixture or partial work into verified scholarship.

## Evaluation discipline

High-risk routing behavior should have prompt fixtures that state the expected route, required output markers, and forbidden claims. Store reusable fixtures under `tests/skill_evals/` so future skill changes can be checked against real failure modes instead of only structural tests.

The research behavior fixture checker detects structural and behavioral risk markers around overstatement and uncertainty handling. It does not verify source truth, field consensus, citation accuracy, method validity, or scholarly correctness.

## Counterargument discipline

Every major thesis should survive at least one peer-review style critique that includes rival explanations and missing literatures.

## Prose discipline

Readable prose is not a substitute for evidence. Strong style should clarify the argument, not hide weak support.

## Proposal and release discipline

Comparable titles, market claims, and press positioning need a source basis. Before sharing materials outside the project, check private notes, copied source text, quote locators, license risk, credentials, and local metadata.
