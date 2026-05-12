---
name: counterargument-peer-review
description: Simulate rigorous research peer review by generating strong objections, rival explanations, missing literatures, positional blind spots, and thesis revisions.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# Counterargument Peer Review

## Purpose

Stress-test a research argument. The goal is not negativity; it is to make the book harder to dismiss.

## When to use

Use when the user has a thesis, chapter draft, outline, proposal, or argument and wants serious critique.

## Inputs expected

- Thesis, draft section, chapter outline, proposal, or argument summary.
- Intended audience, discipline, evidence base, and known counterarguments.
- Source basis for major claims when available.
- User's revision goal: strengthen thesis, narrow scope, identify risks, or prepare for review.

## Review stance

Be charitable first, then rigorous. Steelman the argument before attacking it. Do not flatter. Do not dismiss. Improve.

## Source basis and AI limits

Before reviewing, state the source access level as one of:

- user-provided full text
- excerpt only
- citation only
- model knowledge only
- live/current search needed

Every output must separate source basis, what can be verified from available material, what remains uncertain, and what the user must verify. Do not invent citations, page numbers, quotations, DOIs, datasets, market facts, field consensus, source metadata, or claims of having searched a database. Separate verified facts, interpretation, speculation, and recommendation.

## Files/folders it may read

- This skill's `SKILL.md`, `README.md`, and `agents/openai.yaml`.
- User-provided drafts, proposals, outlines, notes, claim ledgers, literature maps, and source excerpts explicitly named in the request.
- Related argument or chapter artifacts when critique depends on manuscript structure.

## Files/folders it may write

- None by default.
- May create or update user-requested peer-review critiques or revision memos in the current project.
- Must not rewrite manuscript files unless explicitly asked.

## What it must not do

- Do not protect the user's preferred thesis from strong objections.
- Do not invent specific missing citations or expert positions.
- Do not replace critique with generic warnings.

## Procedure

### 1. Charitable restatement

Restate the user's thesis in its strongest plausible form.

### 2. Identify strongest objections

Generate objections from:

- evidence base
- rival theory
- methodology
- context and background
- ethics
- practice and application
- feasibility
- causal inference
- scale/generalizability
- unintended consequences

### 3. Identify missing literatures

Name literatures or fields that would likely object or add nuance. Do not invent specific citations unless verified or provided; name the area instead.

Name missing specialist review needs when a claim requires field expertise, methods expertise, legal/medical/technical review, or current source verification.

### 4. Identify hidden assumptions and biases

Look for:

- confirmation bias
- selection bias
- survivorship bias
- single-cause determinism
- reductionism
- presentism
- cultural or status bias
- overgeneralization from exceptional cases
- conflation of possibility and probability

### 5. Provide revision strategy

For each objection, suggest ways to:

- add evidence
- narrow scope
- reword claim
- add counterargument section
- change chapter order
- concede a point without losing the thesis

For high-severity objections, state what evidence would falsify or materially weaken the thesis.

## Output format

```markdown
# Peer-Review Style Critique

## Source basis

## What I can verify

## What remains uncertain

## User verification needed

## Charitable restatement

## Strongest objections
| Objection | Source of challenge | Severity | Why it matters | Falsifying evidence | Revision strategy |

## Rival explanations

## Missing literatures or perspectives

## Specialist review needed

## Hidden assumptions / bias risks

## Claims to narrow

## Revised stronger thesis

## Limits / failure risks

## Next best skill
```

## Severity scale

- Critical: could collapse the thesis.
- Major: must be addressed explicitly.
- Moderate: should be qualified or supported.
- Minor: clarity or framing issue.

## Quality checks

- Include objections that would come from experts as well as casual readers.
- Do not protect the user's favorite thesis.
- Do not replace critique with generic warnings.
- Always offer constructive fixes.
- Do not name specific missing sources unless they are provided or verified.

## Failure modes

- Critique becomes performative negativity without revision strategy.
- Rival explanations are weaker than real expert objections would be.
- Missing literatures are fabricated instead of named as fields to check.
- Thesis revisions preserve confidence by hiding uncertainty.
