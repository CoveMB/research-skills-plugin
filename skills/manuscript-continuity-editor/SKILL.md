---
name: manuscript-continuity-editor
description: Review multiple chapters or a whole manuscript when thesis coherence, repetition, contradictions, concept tracking, tone consistency, chapter order, argument drift, or revision priorities need diagnosis.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# Manuscript continuity editor

## Purpose

Evaluate coherence across a long research nonfiction manuscript: argument progression, conceptual continuity, repetition, contradictions, tone, structure, and chapter dependencies.

## When to use

Use when the user provides multiple chapters, a table of contents, chapter summaries, manuscript outline, proposal, or revision plan.

## Automatic selection guidance

- High-signal triggers: whole manuscript, multiple chapters, contradictions, repetition, concept drift, thesis drift, chapter order, tone consistency, or continuity review.
- Light-route behavior: map continuity risks and route evidence problems to claim or citation audit only when needed.
- Deep-work gate: cross-file review requires the user to provide chapter files, excerpts, or summaries.
- Noise and slowdown guard: do not perform line edits across a manuscript when structural continuity is the requested task.

## Do not use this skill when

- The user has only one chapter; use `chapter-architecture`.
- The user asks for claim support status; use `claim-evidence-ledger`.
- The user asks for sentence-level prose revision; use `scholarly-prose-editor`.

## Inputs expected

- Multiple chapters, table of contents, chapter summaries, manuscript outline, proposal, or revision plan.
- Central thesis, intended audience, chapter order, and known continuity concerns.
- Existing concept list, claim ledger, citation audit, or style sheet when available.
- File list or chapter boundaries if reviewing separate manuscript files.

## Source basis and AI limits

Follow `docs/SOURCE_LIMITS.md`: state the source access level, separate source basis from interpretation, include What I can verify, What remains uncertain, and User verification needed. Do not invent citations or source support.

## Machine-readable artifacts

When the user explicitly asks for JSON or a contract artifact, use `shared/contracts/book/book_artifact.schema.json` with `artifact_type: continuity_review`. If the output is normal Markdown, do not force the JSON contract.

## Files/folders it may read

- This skill's `SKILL.md`, `README.md`, `assets/continuity-map-template.md`, and `agents/openai.yaml`.
- `docs/SOURCE_LIMITS.md` for shared source-access and verification rules.
- `docs/AUTO_SELECTION_GUARDRAILS.md` for shared automatic-trigger guardrails.
- User-provided chapters, outlines, proposals, chapter summaries, style sheets, claim ledgers, and citation audits explicitly named in the request.
- Adjacent manuscript files only when the user asks for cross-chapter review.

## Files/folders it may write

- None by default.
- May create or update user-requested continuity maps, revision memos, or manuscript tracking notes in the current project.
- Must not rewrite chapters or restructure files unless explicitly asked.

## What it must not do

- Do not treat repetition as evidence.
- Do not focus only on prose when structure, concept drift, or claim drift is the problem.
- Do not invent chapter content for chapters not provided.

## Procedure

### 1. Identify global thesis

Extract the manuscript's central claim and determine whether each chapter serves it.

### 2. Map chapter functions

Classify each chapter's role. Identify chapters that repeat, drift, or do not advance the argument.

### 3. Track recurring concepts

For each key concept, check:

- where it is introduced
- whether it is defined
- whether its meaning shifts
- whether it is overused
- whether it needs a glossary or earlier explanation

Also track claim drift: whether a claim becomes stronger, weaker, broader, or contradictory across chapters.

### 4. Detect repetition and redundancy

Separate productive repetition from accidental repetition.

Track repeated unsupported claims so stylistic repetition does not hide evidence gaps.

### 5. Detect contradictions and tensions

Flag contradictions, unresolved tensions, or changes in scope/audience.

### 6. Evaluate chapter order

Suggest reordering when the argument would become clearer.

### 7. Create revision priorities

Rank fixes by impact.

## Output format

```markdown
# Manuscript continuity review

## Source basis

## What I can verify

## What remains uncertain

## User verification needed

## Global thesis as currently expressed

## Chapter function map
| Chapter | Current function | Contribution to thesis | Issues | Recommendation |

## Repetition map

## Concept tracking
| Concept | First introduced | Defined? | Later use | Continuity issue |

## Claim drift

## Repeated unsupported claims

## Contradictions or unresolved tensions

## Tone and audience consistency

## Suggested restructuring

## Priority revision list

## Limits / failure risks

## Suggested next step

```

Use the optional Suggested next step policy in `docs/AUTO_SELECTION_GUARDRAILS.md`. The section may be omitted. If included, it must identify the named scholarly risk it reduces and use one skill only.

## Quality checks

- Do not focus only on sentence-level prose.
- Identify structural issues even if the writing is polished.
- Preserve useful recurring motifs while cutting accidental repetition.
- Flag missing transitions between major argument stages.
- Do not treat a repeated claim as stronger merely because it appears in many chapters.
- Suggested next step must reduce a named scholarly risk, not promote a skill because it exists.

## Failure modes

- Review misses cross-chapter claim drift.
- Concept tracking ignores shifts in definition or scope.
- Repetition map treats motif and redundancy as the same problem.
- Continuity recommendations require chapters or evidence not supplied.
- Premature citation audit before citations, quotes, page numbers, bibliography entries, or cited claims exist.
