---
name: annotated-bibliography-builder
description: Create research-grade annotated bibliographies that summarize argument, method, evidence, relevance, limitations, key terms, and chapter placement for research book sources.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# Annotated Bibliography Builder

## Purpose

Produce high-quality research annotations that help a book author remember what each source argues, how it argues, why it matters, and how it can be used.

## When to use

Use when the user provides sources, citations, excerpts, abstracts, notes, PDFs, or a bibliography and needs structured annotations.

## Inputs expected

- Source text, excerpt, abstract, citation, bibliography entry, notes, or PDF path.
- User's project question, thesis, chapter plan, or intended use for each source.
- Required citation style or metadata fields when relevant.
- Source access level for each item when different sources have different evidence bases.

## Source basis and AI limits

Before annotating, state the source access level as one of:

- user-provided full text
- excerpt only
- citation only
- model knowledge only
- live/current search needed

Every output must separate source basis, what can be verified from available material, what remains uncertain, and what the user must verify. Do not invent citations, page numbers, quotations, DOIs, datasets, market facts, field consensus, source metadata, or claims of having searched a database. Separate verified facts, interpretation, speculation, and recommendation.

## Files/folders it may read

- This skill's `SKILL.md`, `README.md`, `assets/annotation-template.md`, and `agents/openai.yaml`.
- User-provided sources, excerpts, PDFs, notes, bibliographies, and project files explicitly named in the request.
- Related project artifacts when chapter placement or source relevance depends on them.

## Files/folders it may write

- None by default.
- May create or update user-requested annotated bibliography files or notes in the current project.
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
# Annotated Bibliography

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
