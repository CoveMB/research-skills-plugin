---
name: claim-evidence-ledger
description: Extract major claims from a research draft and classify claim type, evidence status, citation need, confidence, overclaiming risk, and safer wording.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# Claim Evidence Ledger

## Purpose

Turn a draft, outline, or argument into an auditable ledger of claims. This is one of the main safeguards against unsupported research writing.

## When to use

Use when the user provides prose, notes, outline, chapter draft, thesis, or argument and needs to know which claims are supported, unsupported, speculative, overstated, or citation-ready.

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

Before building the ledger, state the source access level as one of:

- user-provided full text
- excerpt only
- citation only
- model knowledge only
- live/current search needed

Every output must separate source basis, what can be verified from available material, what remains uncertain, and what the user must verify. Do not invent citations, page numbers, quotations, DOIs, datasets, market facts, field consensus, source metadata, or claims of having searched a database. Separate verified facts, interpretation, speculation, and recommendation.

## Files/folders it may read

- This skill's `SKILL.md`, `README.md`, `assets/claim-ledger-template.csv`, and `agents/openai.yaml`.
- User-provided drafts, notes, source excerpts, citations, bibliographies, and claim lists explicitly named in the request.
- Related chapter or argument artifacts when claim context matters.

## Files/folders it may write

- None by default.
- May create or update user-requested claim ledgers, CSVs, or audit notes in the current project.
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

### 4. Rewrite overclaims

Offer safer research wording that preserves the argument while reducing unsupported certainty.

### 5. Identify missing evidence

Recommend source types, not fake sources.

## Output format

```markdown
# Claim-Evidence Ledger

## Source basis

## What I can verify

## What remains uncertain

## User verification needed

| # | Claim | Type | Source basis | Evidence status | Current support | Evidence needed | Locator needed | Confidence | Risk | Safer wording |

## High-risk claims needing attention

## Claims that can remain interpretive or normative

## Suggested source priorities

## Limits / failure risks

## Next best skill
```

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
