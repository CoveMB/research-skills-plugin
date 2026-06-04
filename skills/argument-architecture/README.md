# argument-architecture

## What it does

Use this skill to design the book's argument rather than only its topic order. It builds a thesis tree with supporting claims, warrants, evidence needs, assumptions, counterarguments, dependencies, and chapter placement.

An outline says what the book covers. Argument architecture says what the book must prove, in what order, and what happens if a supporting claim fails. That distinction matters in research nonfiction because chapters should advance an argument, not simply collect related material.

## When to use it

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

The output usually includes the main thesis, thesis variants, a thesis tree, hidden assumptions, chapter-level argument sequence, weak links, a stronger formulation, and a risk-gated follow-up when it is useful.

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

After this skill, use `counterargument-peer-review` to stress-test the argument. Then use `chapter-architecture` to turn the argument sequence into chapter plans.
