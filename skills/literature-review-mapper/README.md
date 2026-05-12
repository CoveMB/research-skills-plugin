# literature-review-mapper

## What it does

Use this skill to turn a pile of sources into a map of a field. It does not simply summarize each source. It groups the literature into schools of thought, debates, methods, areas of agreement, controversies, intellectual lineages, and gaps that matter for the book.

This is the skill to use when the author needs to know where the book sits. It helps separate a real gap in the literature from a gap in the author's current reading.

## When to use it in the book writing process

Use it after the first serious round of source discovery and annotation. It belongs before argument architecture because the book's thesis should be shaped by the field, not only by the author's starting intuition.

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

The output usually includes a field overview, disciplines and subfields, schools of thought, major debates, consensus and controversy map, intellectual genealogy, gaps, implications for the book thesis, missing sources, and recommended next skill.

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

After this skill, use `argument-architecture` to build a thesis tree. If the map exposes weak or questionable sources, use `methodology-source-auditor` first.
