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

## Operational boundaries

Follow `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`.

Template: `assets/case-study-dossier-template.md`.

## Best next steps

After this skill, use `chapter-architecture` to place cases inside a chapter sequence. Use `claim-evidence-ledger` when case-based claims need support checks.
