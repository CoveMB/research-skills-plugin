# reading-load-reducer

## What it does

Use this skill to reduce reading burden by turning dense material, source lists, abstracts, search results, or long notes into read/skim/park/skip triage.

It helps decide where close reading is worth the effort, what to extract from each item, and how to spend any stated reading budget.

## When to use it

Use it before literature synthesis, source annotation, or citation audit when the immediate problem is too much text.

Use `literature-review-mapper` after a corpus is ready for synthesis. Use `annotated-bibliography-builder` when individual source annotations are needed. Use `dyslexia-research-companion` when reading load is part of a broader accessibility bottleneck.

## Good inputs

- Source excerpts, abstracts, titles, search results, bibliography entries, notes, chapter drafts, or reading list.
- Project question, chapter, thesis, or reason for reading.
- Available source access level and optional time budget.

## Example requests

```text
Use reading-load-reducer. Tell me which of these sources to read closely, skim, park, or skip for chapter 2.
```

```text
Use reading-load-reducer. This article is dense; give me close-reading targets and what to extract.
```

```text
Use reading-load-reducer. Reduce this source list to a reading plan without pretending title-only records are verified.
```

## Typical output

Typical output is a triage table, reading plan, verification gaps, and one optional risk-gated next step. Close-reading targets, skim targets, and park/skip lists should appear only when they add value beyond the triage table.

Ask for compact output when you want one source-basis line, one triage table, uncertainty only when needed, and one next action. Compact output should include `How to use this result: TRIAGE ONLY - Use this only to prioritize reading; do not treat it as literature synthesis, source verification, expert-review, or publication clearance.` It changes output shape, not route selection or evidence requirements.

## Operational boundaries

Follow `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`.

Keep access-level limits, provisional triage, and expert-review or user-verification limits visible for high-stakes or publication-facing decisions.

Call out title-only overreach, unsupported synthesis, or output that adds reading load.

## Best next steps

After this skill, use `annotation-to-source-note` for close-read excerpts, `extraction-table-builder` for source comparison, or `literature-review-mapper` after enough sources are ready for synthesis.
