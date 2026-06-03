---
name: literature-review-mapper
description: Map a research literature when a topic, source list, bibliography, annotations, or notes need schools of thought, debates, consensus, intellectual genealogy, methods, gaps, and thesis implications.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# Literature review mapper

## Purpose

Create an intellectual map of a research field. The goal is not to summarize sources one by one but to show structure: schools, debates, methods, genealogy, consensus, gaps, and relevance to the book.

## When to use

Use when the user has a topic, source list, annotations, or scattered notes and needs a literature review structure for a research book or scholarly nonfiction project.

## Automatic selection guidance

- High-signal triggers: literature review, schools of thought, debates, gaps, consensus, controversy, intellectual genealogy, methods, or thesis implications.
- Light-route behavior: map the supplied corpus or clearly mark the map as provisional when the corpus is partial.
- Deep-work gate: do not synthesize field consensus or missing literatures without a representative source set, explicit lookup, or router deep mode lookup.
- Noise and slowdown guard: do not summarize sources one by one when the user needs field structure.

## Do not use this skill when

- The user needs source search queries; use `systematic-source-discovery`.
- The user needs extraction tables or source matrices before synthesis; use `extraction-table-builder`.
- The user needs annotations for individual sources; use `annotated-bibliography-builder`.
- The user needs source credibility or method quality; use `methodology-source-auditor`.

## Inputs expected

- Source list, annotations, bibliography, research notes, or topic map.
- Project thesis, research question, field, audience, and scope boundaries when available.
- Known schools, debates, authors, methods, or gaps the user already suspects.
- Clear indication of whether the supplied corpus is representative or partial.

## Source basis and AI limits

Use `docs/SOURCE_LIMITS.md` for source-access rules. Keep source access level, What I can verify, What remains uncertain, and User verification needed visible. Do not invent citations or source support.

## Machine-readable artifacts

When the user explicitly asks for JSON or a contract artifact, use `shared/contracts/book/book_artifact.schema.json` with `artifact_type: literature_map`. If the output is normal Markdown, do not force the JSON contract.

## Files/folders it may read

- Shared operational boundary doc: `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.
- Shared policy docs, especially `docs/SOURCE_LIMITS.md` and `docs/AUTO_SELECTION_GUARDRAILS.md`.
- User-provided bibliographies, annotations, source notes, literature maps, and project files explicitly named in the request.
- Related research agenda or source discovery artifacts when available.

## Files/folders it may write

- None by default.
- May create or update user-requested literature maps or synthesis notes in the user-designated project or workspace.
- Must not alter original sources, bibliographies, or repository files unless explicitly asked.

## What it must not do

- Do not claim field consensus from a small or one-sided corpus.
- Do not invent representative authors, canonical works, or current debates.
- Do not confuse a gap in the user's sources with a gap in the field.
- Do not call a stale bibliography current unless live/current lookup or an up-to-date corpus supports that claim.
- Do not hide corpus skew that could change the map, including English-only, famous-author, database, open-access, Global North, or discipline-boundary skew.

## Procedure

### 1. Identify disciplines and subfields

List every discipline involved. For interdisciplinary work, explain how each field frames the problem differently.

State corpus limits: what source set was supplied, what fields may be missing, and whether the map reflects the provided corpus or a broader field that needs live/current verification.

Flag corpus bias that could change the conclusion: languages searched, database coverage, open-access availability, famous-author anchoring, geography, publication type, and disciplines excluded by the search terms.

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

Use `current consensus` or `recent debate` only when the source basis is current enough for the field or lookup was performed. Otherwise label the map as stale, partial, or currentness-unverified.

### 5. Trace intellectual genealogy

Where useful, map how ideas developed over time: canonical works, turning points, methodological shifts, and recent challenges.

### 6. Identify gaps and book opportunities

Gaps can be empirical, theoretical, contextual, methodological, geographic, conceptual, or translational. Do not overclaim novelty; phrase contribution carefully.

## Output format

```markdown
# Literature review map

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

```

Use the optional Suggested next step policy in `docs/AUTO_SELECTION_GUARDRAILS.md`; it may be omitted unless a follow-on skill reduces a named scholarly risk.

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
- Premature citation audit before citations, quotes, page numbers, bibliography entries, or cited claims exist.
