# literature-review-mapper

## What it does

Use this skill to turn a pile of sources into a map of a field. It does not simply summarize each source. It groups the literature into schools of thought, debates, methods, areas of agreement, controversies, intellectual lineages, and gaps that matter for the book.

Use it when the author needs to know where the book sits. It helps separate a real gap in the literature from a gap in the author's current reading.

## When to use it

Use it after the first substantial round of source discovery and annotation. It belongs before argument architecture because the field should shape the book's thesis alongside the author's starting intuition.

Use it again when a chapter enters a new debate or when reviewers say the project is missing a field, tradition, or method.

## Good inputs

- A bibliography, source list, or annotated bibliography.
- Research notes organized by topic, author, field, or claim.
- A working thesis that needs to be tested against existing literature.
- Known debates, schools, or terms.
- Questions about what the field agrees on and where it remains divided.

## Example requests

```text
Map these sources into schools of thought, debates, consensus, and gaps for my research book.
```

```text
I have notes from several fields. Show how each field frames the problem differently.
```

```text
Use this bibliography to identify the debates my thesis must answer.
```

## Typical output

The output usually includes a field overview, disciplines and subfields, schools of thought, major debates, consensus and controversy map, intellectual genealogy, gaps, implications for the book thesis, missing sources, and an optional risk-gated suggested step.

## Procedure

Follow the shared procedure in `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`.

## Quality checks

Apply the shared quality checks in `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`; keep any skill-specific caveats visible in the output.

## Failure modes

Use the shared failure modes in `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`; call out the skill-specific failure most relevant to the request.

## Files/folders it may read

Follow the shared read boundary in `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`.

## Files/folders it may write

Follow the shared write boundary in `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`.

## What it must not do

Follow the shared prohibitions in `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`.

## Best next steps

After this skill, use `argument-architecture` to build a thesis tree. If the map exposes weak or questionable sources, use `methodology-source-auditor` first.
