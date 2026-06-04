# manuscript-continuity-editor

## What it does

Use this skill to review coherence across several chapters or a full manuscript. It checks whether the thesis holds across the book, whether chapters have clear functions, whether concepts stay consistent, whether repetition is useful or accidental, and whether contradictions or tone shifts need revision.

This skill is not a sentence-level copyedit. It is a structural continuity pass for long-form research nonfiction.

## When to use it

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

The output usually includes the global thesis as currently expressed, chapter function map, repetition map, concept tracking table, contradictions or unresolved tensions, tone and audience consistency notes, suggested restructuring, priority revision list, and a risk-gated follow-up when it is useful.

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

After this skill, use `chapter-architecture` for chapters that need rebuilding. Use `scholarly-prose-editor` once structure and continuity problems are resolved.
