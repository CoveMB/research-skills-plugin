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

## Workflow

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

### 4. Detect repetition and redundancy

Separate productive repetition from accidental repetition.

### 5. Detect contradictions and tensions

Flag contradictions, unresolved tensions, or changes in scope/audience.

### 6. Evaluate chapter order

Suggest reordering when the argument would become clearer.

### 7. Create revision priorities

Rank fixes by impact.

## Output format

```markdown
# Manuscript Continuity Review

## Global thesis as currently expressed

## Chapter function map
| Chapter | Current function | Contribution to thesis | Issues | Recommendation |

## Repetition map

## Concept tracking
| Concept | First introduced | Defined? | Later use | Continuity issue |

## Contradictions or unresolved tensions

## Tone and audience consistency

## Suggested restructuring

## Priority revision list

## Next best skill
```

## Quality checks

- Do not focus only on sentence-level prose.
- Identify structural issues even if the writing is polished.
- Preserve useful recurring motifs while cutting accidental repetition.
- Flag missing transitions between major argument stages.
