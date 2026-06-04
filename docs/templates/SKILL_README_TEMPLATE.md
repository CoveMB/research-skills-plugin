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

## Procedure

Follow the shared procedure in `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`; add only skill-specific procedure caveats here.

## Quality checks

Apply the shared quality checks in `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`; add only skill-specific checks here.

## Failure modes

Use the shared failure modes in `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`; add only skill-specific failure modes here.

## Files/folders it may read

Follow the shared read boundary in `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`; add only skill-specific read boundaries here.

## Files/folders it may write

Follow the shared write boundary in `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`; add only skill-specific write boundaries here.

## What it must not do

Follow the shared prohibitions in `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`; add only skill-specific prohibitions here.

## Best next steps

Name only follow-ups that reduce a concrete scholarly risk.
