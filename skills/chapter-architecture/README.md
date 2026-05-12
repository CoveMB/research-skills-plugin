# chapter-architecture

## What it does

Use this skill to design a chapter that has a job, a question, a claim, a sequence, and evidence. It turns notes or a chapter idea into a structured plan with section functions, evidence placement, counterarguments, transitions, opening options, ending strategy, and revision risks.

This is different from a topic outline. A chapter architecture explains what each section does for the argument. It helps prevent chapters that summarize literature, collect examples, or drift away from the book thesis.

## When to use it in the book writing process

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

After this skill, draft or revise the chapter. Then use `claim-evidence-ledger` to check support and `scholarly-prose-editor` to improve the prose.
