# manuscript-continuity-editor

## What it does

Use this skill to review coherence across several chapters or a full manuscript. It checks whether the thesis holds across the book, whether chapters have clear functions, whether concepts stay consistent, whether repetition is useful or accidental, and whether contradictions or tone shifts need revision.

This skill is not a sentence-level copyedit. It is a structural continuity pass for long-form research nonfiction.

## When to use it in the book writing process

Use it after several chapters exist, after a full draft, before a major revision, or before proposal/sample submission when chapter summaries must line up with the manuscript.

Use it when the author suspects the book repeats itself, loses its thesis, changes audience halfway through, defines terms inconsistently, or has chapters in the wrong order.

## Good inputs

- Multiple chapters, chapter summaries, table of contents, proposal, or revision plan.
- The intended thesis and audience.
- Notes about known problem chapters.
- Any required structure, such as parts, sections, or press guidelines.

## Example requests

```text
Review these chapter summaries for thesis continuity, repetition, and chapter order.
```

```text
Track how my core concepts change across the manuscript and flag contradictions.
```

```text
Build a priority revision list for this full draft based on argument coherence.
```

## Typical output

The output usually includes the global thesis as currently expressed, chapter function map, repetition map, concept tracking table, contradictions or unresolved tensions, tone and audience consistency notes, suggested restructuring, priority revision list, and next best skill.

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

After this skill, use `chapter-architecture` for chapters that need rebuilding. Use `scholarly-prose-editor` once structure and continuity problems are resolved.
