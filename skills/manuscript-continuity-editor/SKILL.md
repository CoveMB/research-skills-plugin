---
name: manuscript-continuity-editor
description: Review multiple chapters or a whole manuscript for thesis coherence, repetition, contradictions, concept tracking, tone consistency, chapter order, and revision priorities.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# Manuscript Continuity Editor

## Purpose

Evaluate coherence across a long research nonfiction manuscript: argument progression, conceptual continuity, repetition, contradictions, tone, structure, and chapter dependencies.

## When to use

Use when the user provides multiple chapters, a table of contents, chapter summaries, manuscript outline, proposal, or revision plan.

## Inputs expected

- Multiple chapters, table of contents, chapter summaries, manuscript outline, proposal, or revision plan.
- Central thesis, intended audience, chapter order, and known continuity concerns.
- Existing concept list, claim ledger, citation audit, or style sheet when available.
- File list or chapter boundaries if reviewing separate manuscript files.

## Source basis and AI limits

Before reviewing continuity, state the source access level as one of:

- user-provided full text
- excerpt only
- citation only
- model knowledge only
- live/current search needed

Every output must separate source basis, what can be verified from available material, what remains uncertain, and what the user must verify. Do not invent citations, page numbers, quotations, DOIs, datasets, market facts, field consensus, source metadata, or claims of having searched a database. Separate verified facts, interpretation, speculation, and recommendation.

## Files/folders it may read

- This skill's `SKILL.md`, `README.md`, `assets/continuity-map-template.md`, and `agents/openai.yaml`.
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
# Manuscript Continuity Review

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

## Next best skill
```

## Quality checks

- Do not focus only on sentence-level prose.
- Identify structural issues even if the writing is polished.
- Preserve useful recurring motifs while cutting accidental repetition.
- Flag missing transitions between major argument stages.
- Do not treat a repeated claim as stronger merely because it appears in many chapters.

## Failure modes

- Review misses cross-chapter claim drift.
- Concept tracking ignores shifts in definition or scope.
- Repetition map treats motif and redundancy as the same problem.
- Continuity recommendations require chapters or evidence not supplied.
