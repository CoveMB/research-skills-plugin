# annotated-bibliography-builder

## What it does

Use this skill to create useful annotations for sources in a research book project. A good annotation records more than a summary. It explains the source's argument, method, evidence, limits, relevance, terms, and possible chapter placement.

This skill helps an author avoid rereading the same source months later because the original notes were too thin. It also keeps source use honest by separating what the source says from what the author wants it to prove.

## When to use it in the book writing process

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

1. Establish source basis and source access level.
2. Use the skill's `SKILL.md` procedure, not memory-only shortcuts.
3. Produce the stated output format and separate verified facts, interpretation, speculation, and recommendation.
4. End with verification gaps and the next best skill or repair step.

## Quality checks

- Evidence strength must match claim strength.
- Missing source access must be marked, not hidden.
- Uncertainty, limits, and user verification needs must be visible.
- Output should preserve scholarly caution without becoming vague.

## Failure modes

- Fabricated citations, quotes, page numbers, source metadata, datasets, market facts, or field consensus.
- Confident synthesis from partial sources.
- Generic prose or structure that hides weak evidence.
- Overstated claims, missing counterarguments, or unclear source basis.

## Files/folders it may read

- This skill's `SKILL.md`, `README.md`, `assets/`, `references/`, and `agents/openai.yaml` when present and relevant.
- User-provided drafts, notes, sources, artifacts, or project files explicitly named in the request.
- Shared project documentation only when needed for workflow, quality, or artifact compatibility.

## Files/folders it may write

- None by default.
- May create or update user-requested research artifacts, notes, drafts, or review files in the current project.
- Must not overwrite source material, bibliography databases, manuscript files, or plugin files without explicit user request.

## What it must not do

- Invent missing scholarly facts or verification.
- Treat unavailable evidence as confirmed.
- Use style polish to mask weak argument, weak sources, or unsupported claims.
- Claim external searches, source checks, or database access that did not happen.

## Best next steps

After this skill, use `literature-review-mapper` to organize the annotated sources into debates and schools. Use `methodology-source-auditor` for sources that may be weak, old, partisan, methodologically unclear, or too narrow for the claims they are being asked to support.
