---
name: reading-load-reducer
description: Reduce reading burden for scholarly work by turning dense articles, source excerpts, search results, bibliographies, chapter drafts, or long notes into skim-read-skip triage, close-reading targets, extraction priorities, evidence needs, and next actions without inventing source support.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# Reading load reducer

## Purpose

Help a researcher decide what to read closely, skim, park, or ignore when text volume is the bottleneck.

This skill reduces reading load before synthesis. It does not claim field consensus or source support unless the available material permits it.

## When to use

Use when the user provides dense source material, article excerpts, abstracts, search results, bibliographies, long notes, chapter drafts, or reading lists and asks what matters, what to read first, or how to reduce reading burden.

Use this instead of `literature-review-mapper` when the user needs triage before synthesis. Use `dyslexia-research-companion` when reading load is mixed with dictation, spelling ambiguity, or broader accessibility routing.

## Automatic selection guidance

- High-signal triggers: reading fatigue, too much to read, dense article, skim/read/skip, source triage, reading priority, reading load, close reading target, or long notes.
- Light-route behavior: classify material into read closely, skim, park, or skip, with short reasons and evidence-use limits.
- Deep-work gate: source lookup happens only when the user asks, source metadata is central, current facts matter, or router deep mode routes here with lookup available.
- Noise and slowdown guard: do not synthesize a field, audit citations, or produce an annotated bibliography when the user needs reading triage first.

## Do not use this skill when

- The user needs source search strategy; use `systematic-source-discovery`.
- The user needs field synthesis from a stable corpus; use `literature-review-mapper`.
- The user needs annotations for individual sources; use `annotated-bibliography-builder`.
- The user needs source credibility or method quality audited; use `methodology-source-auditor`.
- The user needs rough dictation or fragment cleanup; use `dictation-to-research-notes`.

## Inputs expected

- Source excerpts, abstracts, titles, search results, bibliography entries, notes, chapter drafts, or reading list.
- Project question, chapter, thesis, or reason for reading.
- Available source access level: full text, excerpt, citation only, or no source material.
- Optional time budget, priority threshold, or output length limit.

## Source basis and AI limits

Follow `docs/SOURCE_LIMITS.md`: state the source access level, separate source basis from interpretation, include What I can verify, What remains uncertain, and User verification needed. Do not invent citations, page numbers, quotes, source support, or field consensus.

If only titles, abstracts, or snippets are available, mark triage and skip risk as provisional.

## Files/folders it may read

- Bundled skill instructions, metadata, and assets if available (including, but not limited to, `SKILL.md`, `README.md`, `assets/`, `references/`, and `agents/openai.yaml` in this project or equivalent files in another project).
- Shared policy docs, especially `docs/SOURCE_LIMITS.md`, `docs/AUTO_SELECTION_GUARDRAILS.md`, `docs/ROUTING_MATRIX.md`, and `docs/SKILL_INDEX.md`.
- User-provided source excerpts, abstracts, search results, bibliographies, drafts, notes, artifacts, or constraints explicitly named in the request.

## Files/folders it may write

- None by default.
- May create or update user-requested reading triage tables, reading plans, source-priority notes, or follow-up task lists in the user-designated project or workspace.
- Must not overwrite source files, notes, bibliography databases, or manuscript files unless the user explicitly asks.

## What it must not do

- Do not infer source support from title or abstract alone.
- Do not turn provisional reading triage into literature synthesis.
- Do not claim a source is irrelevant when source access is too thin; mark it as park or needs metadata instead.
- Do not produce long summaries when the goal is reducing reading load.

## Procedure

### 1. State the reading goal

Identify the user's project question, chapter, claim, or task. If absent, use the visible task and mark the goal as inferred.

### 2. Classify source access

For each item or excerpt, mark access level:

- full text
- excerpt only
- abstract only
- citation only
- unclear

### 3. Triage the material

Classify each item:

- read closely: likely central to the current claim, method, debate, case, or chapter
- skim: useful context, background, or secondary support
- park: potentially relevant but needs metadata, source access, or later phase
- skip: off-scope for the current task based on available material

### 4. Name the reason

Give short reasons tied to the user's project:

- claim support
- method or evidence
- counterargument
- case material
- key concept
- field context
- low relevance
- insufficient access

### 5. Build a reading plan

Suggest a short sequence that starts with the highest-return reading and names what to extract from each source. If the user supplies a time budget, spend it explicitly across read closely, skim, and park decisions.

## Output format

```markdown
# Reading load reducer

## Source basis

## Reading goal

## Triage table
| Item | Access level | Decision | Why | What to extract | Risk or uncertainty if skipped |

## Reading plan

## Close-reading targets

## Skim targets

## Park or skip

## What I can verify

## What remains uncertain

## User verification needed

## Suggested next step
```

Use the optional Suggested next step policy in `docs/AUTO_SELECTION_GUARDRAILS.md`; it may be omitted unless one specialist skill reduces a named scholarly risk.

## Quality checks

- Triage decisions match the user's current project goal.
- Thin source access stays labeled as provisional.
- Time-budgeted requests receive a reading sequence that fits the stated budget.
- Read closely, skim, park, and skip are distinct.
- Output reduces reading load rather than adding a new essay.
- No citations, page numbers, source claims, or field consensus are invented.

## Failure modes

- Title-only records are treated as if the source was read.
- A skim decision hides a source that could be a major counterargument.
- Triage becomes unsupported literature synthesis.
- The output is too long to reduce reading load.
- Current project goal is ignored.
