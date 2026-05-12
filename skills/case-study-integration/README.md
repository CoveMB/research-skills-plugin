# case-study-integration

## What it does

Use this skill to select and use cases responsibly in a research book. It classifies the job a case is meant to do, checks whether cases are comparable, adds counter-cases where needed, and prevents examples from being treated as proof of claims they cannot support.

Cases can illustrate, test, complicate, generate theory, or challenge a claim. This skill keeps those uses separate so the author does not overgeneralize from a striking story.

## When to use it

Use it when planning a case chapter, choosing examples, comparing cases, building narrative dossiers, or checking whether a case supports a claim. It works well after argument architecture and before chapter architecture for case-heavy chapters.

Use it again when a draft leans too much on one favorable example or ignores failure cases and counterexamples.

## Good inputs

- The claim the case is supposed to support.
- Candidate cases or examples.
- Available source base for each case.
- Scope, geography, time period, actors, and context.
- Concerns about comparability or overclaiming.

## Example requests

```text
Choose which cases should appear in this chapter and explain what each case can support.
```

```text
Evaluate whether these two cases are comparable enough for my argument.
```

```text
Add counter-cases and safer wording so this chapter does not overgeneralize.
```

## Typical output

Expect a case integration plan with claim needing a case, candidate cases, case function, support and challenge columns, source base, limits, recommended case set, counter-cases, dossier template, safer wording, and next skill.

## Procedure

1. State the source basis and source access level.
2. Follow the skill's `SKILL.md` procedure instead of working from memory.
3. Produce the stated output format and keep verified facts, interpretation, speculation, and recommendation separate.
4. End with verification gaps. Add a risk-gated follow-up only when it is useful.

## Quality checks

- Evidence strength must match claim strength.
- Missing source access must be marked clearly.
- Uncertainty, limits, and user verification needs must be visible.
- Output should preserve scholarly caution without becoming vague.

## Failure modes

- Fabricated citations, quotes, page numbers, source metadata, datasets, market facts, or field consensus.
- Confident synthesis from partial sources.
- Generic prose or structure that hides weak evidence or weak reasoning.
- Overstated claims, missing counterarguments, or unclear source basis.

## Files/folders it may read

- This skill's `SKILL.md`, `README.md`, `assets/`, `references/`, and `agents/openai.yaml` when present and relevant.
- User-provided drafts, notes, sources, artifacts, or project files explicitly named in the request.
- Shared project documentation when it is needed for workflow, quality, or artifact compatibility.

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

After this skill, use `chapter-architecture` to place cases inside a chapter sequence. Use `claim-evidence-ledger` when case-based claims need support checks.
