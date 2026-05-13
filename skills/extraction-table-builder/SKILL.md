---
name: extraction-table-builder
description: Turn source notes, annotations, excerpts, or reading notes into structured extraction tables, source matrices, and comparison grids before synthesis, literature mapping, or claim drafting.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# Extraction table builder

## Purpose

Turn source notes and annotations into structured extraction tables and source matrices so evidence can be compared before synthesis.

## When to use

Use when the user needs comparable evidence across sources before literature mapping, synthesis, chapter drafting, or claim building.

## Automatic selection guidance

- High-signal triggers: extraction table, source matrix, compare sources, coding table, comparable evidence, source rows, or structured extraction.
- Light-route behavior: build tables only from supplied notes, annotations, excerpts, or metadata and mark uneven extraction.
- Deep-work gate: source lookup happens only when the user asks, source existence is central, or router deep mode routes here with lookup available.
- Noise and slowdown guard: do not synthesize the literature or draft claims from thin extraction.

## Do not use this skill when

- The user needs a search strategy; use `systematic-source-discovery`.
- The user needs full source annotations; use `annotated-bibliography-builder`.
- The user needs schools of thought or debates mapped; use `literature-review-mapper`.

## Inputs expected

- Source notes, annotations, excerpts, PDFs, bibliographies, or source lists.
- Research question, chapter question, variables, codes, or comparison dimensions when available.
- Source metadata, citekeys, source types, methods, and locators when available.
- Desired table format, such as Markdown, CSV-like table, or matrix.

## Source basis and AI limits

Follow `docs/SOURCE_LIMITS.md`: state the source access level, separate source basis from interpretation, include What I can verify, What remains uncertain, and User verification needed. Do not invent citations or source support.

## Machine-readable artifacts

When the user explicitly asks for JSON or a contract artifact, use `shared/contracts/book/book_artifact.schema.json` with `artifact_type: extraction_table`. If the output is normal Markdown, do not force the JSON contract.

## Files/folders it may read

- Bundled skill instructions, metadata, and assets if available (including, but not limited to, `SKILL.md`, `README.md`, `assets/`, `references/`, and `agents/openai.yaml` in this project or equivalent files in another project).
- Shared policy docs, especially `docs/SOURCE_LIMITS.md` and `docs/AUTO_SELECTION_GUARDRAILS.md`.
- User-provided source notes, annotations, bibliographies, excerpts, PDFs, and project files explicitly named in the request.

## Files/folders it may write

- None by default.
- May create or update user-requested extraction tables, source matrices, or coding notes in the user-designated project or workspace.
- Must not rewrite original source notes, bibliography databases, or manuscript files unless explicitly asked.

## What it must not do

- Do not synthesize beyond the extracted material.
- Do not fill empty cells from memory or plausible guesses.
- Do not treat uneven extraction as cross-source evidence.

## Procedure

### 1. Choose extraction level

Use source-level rows when the user compares whole sources. Use passage-level rows when the question depends on locators or close reading.

### 2. Define fields

Include source, citekey, locator, evidence type, method or source type, extracted point, claim relevance, limitations, coding decision, follow-up question, and extraction status.

### 3. Populate from available material

Fill only what the provided notes, excerpts, or metadata support. Mark missing, unclear, not provided, or not applicable.

### 4. Build comparison view

Create a cross-source matrix when there are enough comparable fields. Mark uneven extraction instead of forcing symmetry.

### 5. Identify next extraction work

List sources that need full text, better locators, method details, coding clarification, or closer reading.

## Output format

```markdown
# Extraction table

## Source basis

## What I can verify

## What remains uncertain

## User verification needed

## Extraction fields

## Source-level extraction
| Source | Citekey | Source type / method | Extracted point | Evidence type | Claim relevance | Limitations | Coding decision | Follow-up question | Status |

## Passage-level extraction
| Source | Locator | Passage basis | Extracted point | Evidence type | Claim relevance | Limitations | Coding decision | Follow-up question | Status |

## Cross-source comparison matrix

## Uneven or insufficient extraction

## Limits / failure risks

## Suggested next step
```

Use the optional Suggested next step policy in `docs/AUTO_SELECTION_GUARDRAILS.md`; it may be omitted unless one skill reduces a named scholarly risk.

## Quality checks

- Every filled cell has a visible basis in supplied material.
- Empty or uncertain cells are marked instead of guessed.
- Passage-level claims keep locator needs visible.
- Comparison does not become synthesis unless the user asks and the evidence supports it.

## Failure modes

- Source tables imply all sources were read equally.
- Thin excerpts are treated as full-source evidence.
- Coding decisions are hidden.
- The output drafts claims before extraction is adequate.
- Premature citation audit before citations, quotes, page numbers, bibliography entries, or cited claims exist.
