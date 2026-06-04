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

After this skill, use `argument-architecture` again if the thesis needs restructuring. Use `claim-evidence-ledger` if the main issue is support. Use `chapter-architecture` if the argument is sound but the chapter sequence needs work.
