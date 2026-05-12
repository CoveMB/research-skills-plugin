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

Expect a triage table, reading plan, close-reading targets, skim targets, park/skip list, verification gaps, and one optional risk-gated next step.

## Procedure

Follow the shared procedure in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.

## Quality checks

Apply the shared quality checks in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`; keep access-level limits and provisional triage visible in the output.

## Failure modes

Use the shared failure modes in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`; call out title-only overreach, unsupported synthesis, or output that adds reading load.

## Files/folders it may read

Follow the shared read boundary in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.

## Files/folders it may write

Follow the shared write boundary in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.

## What it must not do

Follow the shared prohibitions in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.

## Best next steps

After this skill, use `annotation-to-source-note` for close-read excerpts, `extraction-table-builder` for source comparison, or `literature-review-mapper` after enough sources are ready for synthesis.
