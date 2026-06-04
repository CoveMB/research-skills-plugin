# annotated-bibliography-builder

## What it does

Use this skill to create useful annotations for sources in a research book project. A good annotation records more than a summary. It explains the source's argument, method, evidence, limits, relevance, terms, and possible chapter placement.

Use it when thin notes would force the author to reread the same source months later. It also keeps source use honest by separating what the source says from what the author wants it to prove.

## When to use it

Use it after source discovery and before literature mapping, chapter writing, or evidence auditing. It is especially helpful during the first research sprint, when the author is still learning the field.

Use it again whenever new sources enter the project. A book bibliography changes over time, and late additions still need clean annotations.

## Good inputs

- Citations, abstracts, excerpts, source notes, PDFs, or a bibliography.
- The book's working thesis or chapter structure.
- Any known chapter where the source might belong.
- The level of reading available, such as full text, abstract only, or excerpt only.

## Example requests

```text
Annotate these sources for my book. Include argument, method, limits, and chapter placement.
```

```text
Turn my rough reading notes into a structured annotated bibliography.
```

```text
For each source, tell me what it can support and what citation details are still missing.
```

## Typical output

Expect an annotated bibliography with source type, main argument, method or evidence, concepts, best use in the book, limits or bias risks, what it supports, what it challenges, possible chapter placement, and missing citation details.

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

After this skill, use `literature-review-mapper` to organize the annotated sources into debates and schools. Use `methodology-source-auditor` for sources that may be weak, old, partisan, methodologically unclear, or too narrow for the claims they are being asked to support.
