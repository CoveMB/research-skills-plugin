---
name: counterargument-peer-review
description: Run a research peer-review style critique when a thesis, chapter, outline, proposal, or argument needs objections, rival explanations, missing literatures, positional blind spots, and revision paths.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# Counterargument peer review

## Purpose

Stress-test a research argument. The goal is not negativity; it is to make the book harder to dismiss.

## When to use

Use when the user has a thesis, chapter draft, outline, proposal, or argument and wants direct critique.

## Automatic selection guidance

- High-signal triggers: challenge this, peer review, strong objections, rival explanations, missing literatures, one-sided argument, brittle thesis, or review preparation.
- Light-route behavior: steelman the argument, then identify objections and revision options tied to known source limits.
- Deep-work gate: only claim that a literature is missing or settled when a corpus, source list, live search, or router deep mode lookup supports it.
- Noise and slowdown guard: do not generate generic objections detached from the user's thesis, audience, and evidence base.

## Do not use this skill when

- The user needs a thesis tree before critique; use `argument-architecture`.
- The user needs citation verification; use `citation-integrity-auditor`.
- The user asks for line editing rather than intellectual stress-testing.

## Inputs expected

- Thesis, draft section, chapter outline, proposal, or argument summary.
- Intended audience, discipline, evidence base, and known counterarguments.
- Source basis for major claims when available.
- User's revision goal: strengthen thesis, narrow scope, identify risks, or prepare for review.

## Review stance

Be charitable first, then direct. Steelman the argument before attacking it, and avoid flattery or dismissal.

## Source basis and AI limits

Use `docs/SOURCE_LIMITS.md` for source-access rules. Keep source access level, What I can verify, What remains uncertain, and User verification needed visible. Do not invent citations or source support.

## Machine-readable artifacts

When the user explicitly asks for JSON or a contract artifact, use `shared/contracts/book/book_artifact.schema.json` with `artifact_type: peer_review_report`. If the output is normal Markdown, do not force the JSON contract.

## Files/folders it may read

- Shared operational boundary doc: `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.
- Shared policy docs, especially `docs/SOURCE_LIMITS.md` and `docs/AUTO_SELECTION_GUARDRAILS.md`.
- User-provided drafts, proposals, outlines, notes, claim ledgers, literature maps, and source excerpts explicitly named in the request.
- Related argument or chapter artifacts when critique depends on manuscript structure.

## Files/folders it may write

- None by default.
- May create or update user-requested peer-review critiques or revision memos in the user-designated project or workspace.
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
# Peer-review style critique

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

```

Use the optional Suggested next step policy in `docs/AUTO_SELECTION_GUARDRAILS.md`; it may be omitted unless a follow-on skill reduces a named scholarly risk.

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
- Premature citation audit before citations, quotes, page numbers, bibliography entries, or cited claims exist.
