---
name: annotated-bibliography-builder
description: Create scholarly annotated bibliographies that summarize argument, method, evidence, relevance, limitations, key terms, and chapter placement for research book sources.
license: MIT
metadata:
  version: "1.0.0"
  category: scholarly-book-writing
---
# Annotated Bibliography Builder

## Purpose

Produce high-quality scholarly annotations that help a book author remember what each source argues, how it argues, why it matters, and how it can be used.

## When to use

Use when the user provides sources, citations, excerpts, abstracts, notes, PDFs, or a bibliography and needs structured annotations.

## Workflow

### 1. Normalize bibliographic details

Record available metadata: author, title, year, publisher/journal, DOI/URL if provided, edition, pages. If details are missing, mark them missing; do not invent them.

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

## Source 1: [Full citation or available metadata]

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

[Repeat]
```

## Short table option

```markdown
| Source | Type | Main argument | Method | Best use | Limits | Chapter |
```

## Quality checks

- Do not cite a source as read if only an abstract or excerpt was provided.
- Mark all missing citation details.
- Distinguish source argument from user's interpretation.
- Include how the source might challenge the book, not only how it helps.
