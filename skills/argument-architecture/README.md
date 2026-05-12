# argument-architecture

## What it does

Use this skill to design the book's argument rather than only its topic order. It builds a thesis tree with supporting claims, warrants, evidence needs, assumptions, counterarguments, dependencies, and chapter placement.

An outline says what the book covers. Argument architecture says what the book must prove, in what order, and what happens if a supporting claim fails. That distinction matters in research nonfiction because chapters should advance an argument, not simply collect related material.

## When to use it in the book writing process

Use it after the research agenda and literature map are strong enough to support a thesis. It belongs before chapter architecture and drafting.

Use it again when the thesis changes, when a draft feels like a sequence of topics, or when a reviewer says the book has interesting material but no clear argument.

## Good inputs

- A provisional thesis.
- Research agenda, literature map, annotations, or chapter notes.
- Known counterarguments or rival explanations.
- Draft chapter list or table of contents.
- Evidence already gathered and evidence still missing.

## Example requests

```text
Build a thesis tree for this research book and show which claims are essential.
```

```text
Turn this topic outline into an argument architecture with warrants and evidence needs.
```

```text
Give me bold, moderate, conservative, academic, and public-facing versions of the thesis.
```

## Typical output

The output usually includes the main thesis, thesis variants, a thesis tree, hidden assumptions, chapter-level argument sequence, weak links, a stronger formulation, and next best skill.

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

After this skill, use `counterargument-peer-review` to stress-test the argument. Then use `chapter-architecture` to turn the argument sequence into chapter plans.
