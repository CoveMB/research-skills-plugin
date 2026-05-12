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

## Workflow

### 1. Extract claims

Extract only meaningful claims, not every sentence. Prioritize claims that carry the argument.

### 2. Classify each claim

Identify type and level of risk. Causal, predictive, and universal claims are high risk.

### 3. Match to evidence

If sources are provided, match each claim to source support. If no sources are provided, mark evidence needs without inventing citations.

### 4. Rewrite overclaims

Offer safer research wording that preserves the argument while reducing unsupported certainty.

### 5. Identify missing evidence

Recommend source types, not fake sources.

## Output format

```markdown
# Claim-Evidence Ledger

| # | Claim | Type | Evidence status | Current support | Evidence needed | Risk | Safer wording |

## High-risk claims needing attention

## Claims that can remain interpretive or normative

## Suggested source priorities

## Next best skill
```

## Quality checks

- Flag absolute words: always, never, inevitable, proves, revolutionizes, solves, destroys, guarantees.
- Treat causal claims as needing stronger evidence than correlation or analogy.
- Mark normative claims as arguments, not facts.
- Do not invent citations or page numbers.
- Preserve the user's thesis where possible, but make it defensible.
