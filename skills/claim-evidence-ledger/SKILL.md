---
name: claim-evidence-ledger
description: Extract and audit major claims from research drafts, outlines, notes, theses, or arguments by classifying claim type, evidence status, citation need, confidence, overclaiming risk, and safer wording.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# Claim evidence ledger

## Purpose

Turn a draft, outline, or argument into an auditable ledger of claims. This is one of the main safeguards against unsupported research writing.

## When to use

Use when the user provides prose, notes, outline, chapter draft, thesis, or argument and needs to know which claims are supported, unsupported, speculative, overstated, or citation-ready.

## Automatic selection guidance

- High-signal triggers: draft or outline contains factual, empirical, causal, comparative, conceptual, theoretical, normative, predictive, or field-specific claims.
- Light-route behavior: extract claims, classify risk, and recommend safer wording before citation polish.
- Deep-work gate: route to `citation-integrity-auditor` only for cited, quoted, or locator-dependent claims.
- Noise and slowdown guard: do not chase every minor statement; prioritize major claims that affect the thesis.

## Do not use this skill when

- The user asks only for citation formatting; use `citation-integrity-auditor`.
- The claims already exist and the user needs source-note, citekey, locator, or evidence-chain mapping; use `claim-traceability-graph`.
- The user needs source credibility rather than claim extraction; use `methodology-source-auditor`.
- The text is purely stylistic with no research claims.

## Inputs expected

- Draft text, notes, outline, thesis, chapter section, or claim list.
- Provided sources, excerpts, citations, bibliography, or source notes when available.
- User's tolerance for conservative wording and claims they want preserved.
- Citation style or locator expectations when relevant.

## Claim types

Classify claims as:

- empirical
- factual/documentary
- causal
- comparative
- conceptual
- theoretical
- normative
- field-specific
- predictive/speculative
- anecdotal/illustrative
- interpretive

## Evidence status labels

Use these labels:

- Directly supported by provided source
- Plausibly supported but citation needed
- Needs stronger evidence
- Overstated relative to evidence
- Speculative; label as such
- Unsupported in provided material
- Contradicted or contested
- Normative; needs argument rather than empirical citation
- Definition/conceptual; needs conceptual grounding

## Source basis and AI limits

Use `docs/policy/SOURCE_LIMITS.md` for source-access rules. Keep source access level, What I can verify, What remains uncertain, and User verification needed visible. Do not invent citations or source support.

## Compact output

Use compact output when the user asks for low reading load, blocker-first claim triage, or the riskiest claims only. Compact output should keep source basis and verification gaps visible, show only claims whose evidence status changes the next action, and end with one next action.

## Machine-readable artifacts

When the user explicitly asks for JSON or a contract artifact, use `shared/contracts/book/book_artifact.schema.json` with `artifact_type: claim_evidence_ledger`. If the output is normal Markdown, do not force the JSON contract. For durable handoff artifacts, follow `docs/policy/PROCESS_PASSPORT.md`: set `handoff_artifact: true`, include `process_passport`, and preserve upstream passport limits instead of upgrading verification.

For durable multi-stage claim workflows with a workflow trace JSON, use or recommend `python3 scripts/check_workflow_traceability.py --trace path/to/workflow-trace.json` after the ledger is linked downstream. Treat the helper as structural only: it checks claim IDs, link integrity, claim drift, source locator/source-basis preservation, evidence-status non-upgrades, and unresolved-risk preservation; it does not judge argument quality or source-claim fit.

## Files/folders it may read

- Shared operational boundary doc: `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`.
- Shared policy docs, especially `docs/policy/SOURCE_LIMITS.md` and `docs/policy/AUTO_SELECTION_GUARDRAILS.md`.
- User-provided drafts, notes, source excerpts, citations, bibliographies, and claim lists explicitly named in the request.
- Related chapter or argument artifacts when claim context matters.

## Files/folders it may write

- None by default.
- May create or update user-requested claim ledgers, CSVs, or audit notes in the user-designated project or workspace.
- Must not alter source files, citation databases, or manuscript drafts unless explicitly asked.

## What it must not do

- Do not treat unsupported-in-provided-material as false.
- Do not invent citations, page numbers, or source support.
- Do not strengthen claims beyond available evidence.

## Procedure

### 1. Extract claims

Extract only meaningful claims, not every sentence. Prioritize claims that carry the argument.

### 2. Classify each claim

Identify type and level of risk. Causal, predictive, and universal claims are high risk.

### 3. Match to evidence

If sources are provided, match each claim to source support. If no sources are provided, mark evidence needs without inventing citations.

For each claim, record source basis, confidence, and whether a page, timestamp, section, archive locator, dataset variable, or other locator is needed.

Preserve stable claim IDs across downstream artifacts. If claim text, claim type, evidence status, locator status, source basis, or unresolved risk changes, record a version note, verification event, or explicit explanation rather than silently rewriting the lineage.

For empirical, quantitative, computational, or table/figure-backed claims, record analysis provenance: dataset, transformation, script or notebook, run log, output table/figure pointer, and any missing reproducibility material.

### 4. Rewrite overclaims

Offer safer research wording that preserves the argument while reducing unsupported certainty.

### 5. Identify missing evidence

Recommend source types, not fake sources.

## Output format

```markdown
# Claim-evidence ledger

## Source basis

## What I can verify

## What remains uncertain

## User verification needed

| # | Claim | Type | Source basis | Evidence status | Current support | Evidence needed | Locator status | Confidence | Risk | Safer wording |

## Analysis provenance
| Claim | Dataset | Transformation | Script or notebook | Run log | Output pointer | Gap |

## High-risk claims needing attention

## Claims that can remain interpretive or normative

## Suggested source priorities

## Limits / failure risks

```

Compact output:

```markdown
# Claim risk triage

Source basis: [one line]
How to use this result: TRIAGE ONLY - Use this only to spot visible claim risks; do not treat it as final evidence clearance.

| Claim | Evidence status | Risk | Safer wording or evidence need |

Ambiguity: [only if wording or evidence status could change]
Next action: [one action]
```

Use the optional Suggested next step policy in `docs/policy/AUTO_SELECTION_GUARDRAILS.md`; it may be omitted unless a follow-on skill reduces a named scholarly risk.

## Quality checks

- Flag absolute words: always, never, inevitable, proves, revolutionizes, solves, destroys, guarantees.
- Treat causal claims as needing stronger evidence than correlation or analogy.
- Mark normative claims as arguments, not facts.
- Do not invent citations or page numbers.
- Preserve the user's thesis where possible, but make it defensible.
- Unsupported in the provided material does not mean false; it means not yet supported here.

## Failure modes

- Ledger extracts every sentence instead of argument-bearing claims.
- Safer wording weakens the thesis unnecessarily.
- Evidence status hides the difference between no source and weak source.
- Interpretive or normative claims are over-cited instead of argued.
- Premature citation audit before citations, quotes, page numbers, bibliography entries, or cited claims exist.
