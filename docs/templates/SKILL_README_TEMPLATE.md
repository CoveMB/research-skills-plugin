# Skill README template

Use this structure when adding or refreshing a skill README. Put skill-specific guidance near the top. Keep shared safety language short and link to shared docs.

## What it does

Explain the skill's job in plain language.

## When to use it

Name the manuscript stage, useful inputs, and strongest trigger cases.

If the skill should defer rough notes, dictation, spelling ambiguity, prose repair, or reading-load triage to a specific accessibility skill or to `dyslexia-research-companion`, say so here.

## Good inputs

- User-provided drafts, notes, source lists, citations, artifacts, or constraints.
- Any source access limits that matter for verification.

## Example requests

```text
Use skill-name to [specific task].
```

## Typical output

Describe the main output. Note that follow-up suggestions are optional, risk-gated.
For low-load or accessibility-facing skills, say whether the output should prefer tables, short chunks, or ambiguity flags.
If compact output is supported, describe it as an output shape, not a route mode. Require a visible `How to use this result` line with a short status and a full-sentence reliance limit, and say when to escalate from compact output to full review.
If the skill can produce durable artifacts for downstream reuse, remind users to add `handoff_artifact: true` and a `process_passport` following `docs/policy/PROCESS_PASSPORT.md` when the artifact is saved, handed to another skill, sent to a reviewer, or used in a release/submission workflow.

## Operational boundaries

Follow `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`.

## Best next steps

Name only follow-ups that reduce a concrete scholarly risk.
