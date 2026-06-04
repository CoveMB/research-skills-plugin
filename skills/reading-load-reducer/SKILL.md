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
- Deep-work gate: source lookup happens only when the user asks, source metadata is central, current facts matter, a factual or high-stakes claim would otherwise be unsupported, or router deep mode routes here with lookup available.
- Noise and slowdown guard: do not synthesize a field, audit citations, make legal/medical/financial/workplace/publication decisions, or produce an annotated bibliography when the user needs reading triage first.

## Do not use this skill when

- The user needs source search strategy; use `systematic-source-discovery`.
- The user needs field synthesis from a stable corpus; use `literature-review-mapper`.
- The user needs annotations for individual sources; use `annotated-bibliography-builder`.
- The user needs source credibility or method quality audited; use `methodology-source-auditor`.
- The user needs rough dictation or fragment cleanup; use `dictation-to-research-notes`.
- The user asks for legal, medical, financial, workplace, or publication advice from dense material; reduce reading load and state source, expert-review, or user-verification limits.

## Inputs expected

- Source excerpts, abstracts, titles, search results, bibliography entries, notes, chapter drafts, or reading list.
- Project question, chapter, thesis, or reason for reading.
- Available source access level: full text, excerpt, citation only, or no source material.
- Optional time budget, priority threshold, or output length limit.

## Source basis and AI limits

Use `docs/policy/SOURCE_LIMITS.md` for source-access rules. Keep source access level, What I can verify, What remains uncertain, and User verification needed visible. Do not invent citations or source support.

Use `docs/policy/CORPUS_REPRESENTATIVENESS_TAXONOMY.md` only when triage could imply corpus coverage, field balance, missing counterarguments, or literature synthesis. Keep the label compact in source-basis or uncertainty text; do not add a full taxonomy section to low-load output unless the user asks.

If only titles, abstracts, or snippets are available, mark triage and skip risk as provisional.

## Compact output

Use compact output when the user asks for low reading load, time-boxed triage, or a fast skim/read/skip decision. Compact output should use short chunks, stable table labels, one source-basis line, one triage table, one ambiguity or uncertainty note only when needed, and the first reading action.

Compression must not remove decision-critical caveats. Keep access level, provisional status, counterargument risk, currentness limits, and source-support gaps visible when they affect read/skim/park/skip decisions.

## Files/folders it may read

- Shared operational boundary doc: `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`.
- Shared policy docs, especially `docs/policy/SOURCE_LIMITS.md`, `docs/policy/AUTO_SELECTION_GUARDRAILS.md`, `docs/policy/ROUTING_MATRIX.md`, and `docs/user/SKILL_INDEX.md`.
- User-provided source excerpts, abstracts, search results, bibliographies, drafts, notes, artifacts, or constraints explicitly named in the request.

## Files/folders it may write

- None by default.
- May create or update user-requested reading triage tables, reading plans, source-priority notes, or follow-up task lists in the user-designated project or workspace.
- Must not overwrite source files, notes, bibliography databases, or manuscript files unless the user explicitly asks.

## What it must not do

- Do not infer source support from title or abstract alone.
- Do not turn provisional reading triage into literature synthesis.
- Do not claim a source is irrelevant when source access is too thin; mark it as park or needs metadata instead.
- Do not convert `not yet assessed`, title-only, citation-only, or unknown-access items into `irrelevant`.
- Do not produce long summaries when the goal is reducing reading load.
- Do not make legal, medical, financial, workplace, or publication decisions for the user.

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

Before assigning `skip`, apply the access rule: title-only, citation-only, snippet-only, or unclear-access items default to `park` unless the supplied metadata makes them clearly off-scope for the current project. State the uncertainty rather than treating unread material as irrelevant.

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

```

Compact output:

```markdown
# Reading triage

Source basis: [one line]
How to use this result: TRIAGE ONLY - Use this only to prioritize reading; do not treat it as literature synthesis or source verification.

| Item | Access level | Decision | Why | First extraction target | Skip/park risk |

Uncertainty: [only if access is thin or meaning is unclear]

Next action: [first reading action]
```

Use the optional Suggested next step policy in `docs/policy/AUTO_SELECTION_GUARDRAILS.md`; it may be omitted unless a follow-on skill reduces a named scholarly risk.

Use `Close-reading targets`, `Skim targets`, and `Park or skip` only when those sections add value beyond the triage table and reading plan. Omit them in compact output unless the user asks.

## Quality checks

- Triage decisions match the user's current project goal.
- Thin source access stays labeled as provisional.
- Time-budgeted requests receive a reading sequence that fits the stated budget.
- Read closely, skim, park, and skip are distinct.
- Output reduces reading load rather than adding a new essay.
- No citations, page numbers, source claims, or field consensus are invented.
- Corpus coverage labels are used only when a triage decision could be mistaken for synthesis or field balance.
- Expert-review, source-access, and user-verification limits remain visible for high-stakes or publication-facing decisions.
- Compact output preserves the caveat that would change the next reading decision.

## Failure modes

- Title-only records are treated as if the source was read.
- A skim decision hides a source that could be a major counterargument.
- Triage becomes unsupported literature synthesis.
- The output is too long to reduce reading load.
- The output is short but hides access limits, uncertainty, or counterargument risk.
- Current project goal is ignored.
- Triage wording implies legal, medical, financial, workplace, or publication clearance from unread or partial material.
