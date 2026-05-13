---
name: annotated-bibliography-builder
description: Create structured annotated bibliographies when sources, citations, excerpts, abstracts, notes, PDFs, or bibliographies need notes on argument, method, evidence, relevance, limits, and chapter placement.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# Annotated bibliography builder

## Purpose

Produce research annotations that help a book author remember what each source argues, how it argues, why it matters, and how it can be used.

## When to use

Use when the user provides sources, citations, excerpts, abstracts, notes, PDFs, or a bibliography and needs structured annotations.

## Automatic selection guidance

- High-signal triggers: provided sources, citations, abstracts, PDFs, notes, bibliographies, or requests for source annotations.
- Light-route behavior: classify available source access and produce an annotation plan or focused annotations from the supplied material.
- Deep-work gate: only infer method, argument, or relevance from full text, abstracts, excerpts, notes, explicit source lookup, or router deep mode results.
- Noise and slowdown guard: do not browse for missing metadata or summarize unseen sources unless the user asks for source lookup.

## Do not use this skill when

- The user only needs a search strategy; use `systematic-source-discovery`.
- The user needs annotations or highlights converted into source-bound notes with quote and locator gaps; use `annotation-to-source-note`.
- The user asks whether sources are credible enough for a claim; use `methodology-source-auditor`.
- The user provides no source material and only wants a general topic plan.

## Inputs expected

- Source text, excerpt, abstract, citation, bibliography entry, notes, or PDF path.
- User's project question, thesis, chapter plan, or intended use for each source.
- Required citation style or metadata fields when relevant.
- Source access level for each item when different sources have different evidence bases.

## Source basis and AI limits

Follow `docs/SOURCE_LIMITS.md`: state the source access level, separate source basis from interpretation, include What I can verify, What remains uncertain, and User verification needed. Do not invent citations or source support.

## Files/folders it may read

- Bundled skill instructions, metadata, and assets if available (including, but not limited to, `SKILL.md`, `README.md`, `assets/`, `references/`, and `agents/openai.yaml` in this project or equivalent files in another project).
- Shared policy docs, especially `docs/SOURCE_LIMITS.md` and `docs/AUTO_SELECTION_GUARDRAILS.md`.
- User-provided sources, excerpts, PDFs, notes, bibliographies, and project files explicitly named in the request.
- Related project artifacts when chapter placement or source relevance depends on them.

## Files/folders it may write

- None by default.
- May create or update user-requested annotated bibliography files or notes in the user-designated project or workspace.
- Must not alter original source files, bibliography databases, or citation keys unless explicitly asked.

## What it must not do

- Do not cite a source as read when only an abstract, excerpt, or citation was provided.
- Do not complete missing metadata from memory.
- Do not infer full argument, method, or evidence from a title alone.

## Procedure

### 1. Normalize bibliographic details

Record available metadata: author, title, year, publisher/journal, DOI/URL if provided, edition, pages. If details are missing, mark them missing; do not invent them.

For each source, record annotation basis: full text, abstract, excerpt, notes, citation only, or live/current search needed.

### 2. Summarize the source's argument

State the central argument in 2–4 sentences. Avoid vague phrases such as "the source discusses." Explain the claim.

### 3. Identify method and evidence

Name the method or evidence approach in the source's own terms. If the method is unclear, say so rather than forcing a label.

### 4. Evaluate relevance

Explain how the source supports, complicates, or challenges the user's project.

### 5. Identify limitations

Include limits such as scope, date, sample, perspective, method, outdated data, or weak generalizability.

### 6. Suggest placement

Recommend book chapter or section placement.

## Output format

```markdown
# Annotated bibliography

## Source basis

## What I can verify

## What remains uncertain

## User verification needed

## Source 1: [Full citation or available metadata]

**Annotation basis:**
**Type:**
**Main argument:**
**Method/evidence:**
**Key concepts:**
**Best use in book:**
**Limitations / bias risk:**
**Supports:**
**Challenges:**
**Possible chapter placement:**
**Citation details still needed:**
**Limits / failure risks:**

[Repeat]

## Limits / failure risks

```

Use the optional Suggested next step policy in `docs/AUTO_SELECTION_GUARDRAILS.md`; it may be omitted unless one skill reduces a named scholarly risk.

## Short table option

```markdown
| Source | Type | Main argument | Method | Best use | Limits | Chapter |
```

## Quality checks

- Do not cite a source as read if only an abstract or excerpt was provided.
- Mark all missing citation details.
- Distinguish source argument from user's interpretation.
- Include how the source might challenge the book as well as how it helps.
- Do not infer a source's full argument from a title, citation, or abstract alone.

## Failure modes

- Annotation overstates what was visible in the provided material.
- Summary collapses method, evidence, and argument into one vague note.
- Relevance to the book is asserted without explaining the claim it can support.
- Missing citation details are silently filled in.
- Premature citation audit before citations, quotes, page numbers, bibliography entries, or cited claims exist.
