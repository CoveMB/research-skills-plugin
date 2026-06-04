# chapter-architecture

## What it does

Use this skill to design a chapter that has a job, a question, a claim, a sequence, and evidence. It turns notes or a chapter idea into a structured plan with section functions, evidence placement, counterarguments, transitions, opening options, ending strategy, and revision risks.

This is different from a topic outline. A chapter architecture explains what each section does for the argument. It helps prevent chapters that summarize literature, collect examples, or drift away from the book thesis.

## When to use it

Use it after the book-level argument is clear and before drafting a chapter. It also works well when revising a chapter that feels long, shapeless, too literature-heavy, or disconnected from the rest of the manuscript.

Use it for each major chapter, especially chapters that introduce theory, handle counterarguments, analyze evidence, or bridge from one part of the book to another.

## Good inputs

- Book thesis or argument architecture.
- Chapter idea, notes, or rough section list.
- Evidence, case material, literature notes, or known counterarguments.
- Desired chapter role, such as theory chapter, case chapter, literature chapter, or synthesis chapter.
- Problems with the current draft.

## Example requests

```text
Design a chapter architecture for Chapter 2, which needs to define the main concept and introduce the debate.
```

```text
This chapter draft feels like a list of topics. Rebuild it around a central question and claim.
```

```text
Create a section sequence with evidence placement, transitions, and revision risks.
```

## Typical output

The output usually includes chapter purpose, central question, chapter thesis, concepts to define, a section outline table, counterarguments, opening options, ending or bridge to the next chapter, research still needed, revision risks, and next skill.

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

After this skill, draft or revise the chapter. Then use `claim-evidence-ledger` to check support and `scholarly-prose-editor` to improve the prose.
