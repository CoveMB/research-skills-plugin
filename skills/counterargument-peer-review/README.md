# counterargument-peer-review

## What it does

Use this skill to stress-test a thesis, chapter, outline, or proposal. It restates the argument charitably, then raises strong objections, rival explanations, missing literatures, hidden assumptions, bias risks, and claims that should be narrowed.

Research books need to survive skeptical readers. The goal is not to tear down the project. The goal is to make the argument harder to dismiss.

## When to use it

Use it after argument architecture, before major drafting, after a chapter draft, and before proposal submission. It is also useful after peer feedback, when the author needs to understand which objections matter most.

Use it before prose editing. Stylish prose can hide weak argument for a while, but reviewers will still find the problem.

## Good inputs

- A thesis, chapter draft, proposal, or outline.
- The intended field and audience.
- Known rival views or objections.
- The author's strongest concern about the argument.
- Evidence already available.

## Example requests

```text
Review this thesis like a skeptical but fair academic reviewer.
```

```text
Find the strongest objections to this chapter and suggest revision strategies.
```

```text
Identify rival explanations, missing literatures, and hidden assumptions in this proposal.
```

## Typical output

Expect a peer-review style critique with a charitable restatement, strongest objections, rival explanations, missing literatures or perspectives, hidden assumptions, claims to narrow, revised stronger thesis, severity labels, and a risk-gated follow-up when it is useful.

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

After this skill, use `argument-architecture` again if the thesis needs restructuring. Use `claim-evidence-ledger` if the main issue is support. Use `chapter-architecture` if the argument is sound but the chapter sequence needs work.
