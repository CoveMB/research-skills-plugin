---
name: literature-review-mapper
description: Map a research literature into schools of thought, debates, consensus, intellectual genealogy, methods, gaps, and how each cluster supports or challenges a book thesis.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# Literature Review Mapper

## Purpose

Create an intellectual map of a research field. The goal is not to summarize sources one by one but to show structure: schools, debates, methods, genealogy, consensus, gaps, and relevance to the book.

## When to use

Use when the user has a topic, source list, annotations, or scattered notes and needs a literature review structure for a research book or serious nonfiction project.

## Inputs expected

- Source list, annotations, bibliography, research notes, or topic map.
- Project thesis, research question, field, audience, and scope boundaries when available.
- Known schools, debates, authors, methods, or gaps the user already suspects.
- Clear indication of whether the supplied corpus is representative or partial.

## Source basis and AI limits

Before mapping the literature, state the source access level as one of:

- user-provided full text
- excerpt only
- citation only
- model knowledge only
- live/current search needed

Every output must separate source basis, what can be verified from available material, what remains uncertain, and what the user must verify. Do not invent citations, page numbers, quotations, DOIs, datasets, market facts, field consensus, source metadata, or claims of having searched a database. Separate verified facts, interpretation, speculation, and recommendation.

## Files/folders it may read

- This skill's `SKILL.md`, `README.md`, `assets/lit-map-template.md`, and `agents/openai.yaml`.
- User-provided bibliographies, annotations, source notes, literature maps, and project files explicitly named in the request.
- Related research agenda or source discovery artifacts when available.

## Files/folders it may write

- None by default.
- May create or update user-requested literature maps or synthesis notes in the current project.
- Must not alter original sources, bibliographies, or repository files unless explicitly asked.

## What it must not do

- Do not claim field consensus from a small or one-sided corpus.
- Do not invent representative authors, canonical works, or current debates.
- Do not confuse a gap in the user's sources with a gap in the field.

## Procedure

### 1. Identify disciplines and subfields

List every discipline involved. For interdisciplinary work, explain how each field frames the problem differently.

State corpus limits: what source set was supplied, what fields may be missing, and whether the map reflects the provided corpus or a broader field that needs live/current verification.

### 2. Cluster sources into schools of thought

Group sources by shared assumptions, methods, theories, or conclusions. Do not group only by topic.

### 3. Map major debates

For each debate:

- what is the disagreement?
- who are the representative authors?
- what evidence is used?
- what assumptions differ?
- what would count as stronger evidence?

### 4. Separate consensus from controversy

Classify claims as:

- broad consensus
- dominant but contested position
- active controversy
- marginal or speculative position
- open empirical question

### 5. Trace intellectual genealogy

Where useful, map how ideas developed over time: canonical works, turning points, methodological shifts, and recent challenges.

### 6. Identify gaps and book opportunities

Gaps can be empirical, theoretical, contextual, methodological, geographic, conceptual, or translational. Do not overclaim novelty; phrase contribution carefully.

## Output format

```markdown
# Literature Review Map

## Source basis

## What I can verify

## What remains uncertain

## User verification needed

## Corpus limits

## Field overview

## Disciplines and subfields

## Schools of thought
| School | Core claim | Representative sources | Methods/evidence | Strengths | Limits |

## Major debates
| Debate | Side A | Side B | Stakes | Evidence needed |

## Consensus / controversy map

## Intellectual genealogy

## Gaps in the literature

## How this literature shapes the book thesis

## Sources still needed

## Limits / failure risks

## Next best skill
```

## Quality checks

- Do not flatten disagreement into a single consensus.
- Identify methods as well as conclusions.
- Include canonical and recent works where available.
- Distinguish a gap in the user's reading from a gap in the field.
- Flag areas that require a specialist review.
- Do not infer field consensus from a small or one-sided source list.

## Failure modes

- Literature map becomes annotated bibliography instead of field structure.
- Missing opposing literature makes the thesis look stronger than it is.
- Interdisciplinary sources are forced into one field's categories.
- Speculative gaps are stated as proven scholarly absences.
