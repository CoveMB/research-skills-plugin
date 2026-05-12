# Skill README template

Use this structure when adding or refreshing a skill README. Put skill-specific guidance near the top. Keep shared safety language short and link to shared docs when possible.

## What it does

Explain the skill's job in plain language.

## When to use it

Name the manuscript stage, useful inputs, and strongest trigger cases.

## Good inputs

- User-provided drafts, notes, source lists, citations, artifacts, or constraints.
- Any source access limits that matter for verification.

## Example requests

```text
Use skill-name to [specific task].
```

## Typical output

Describe the main output. Note that follow-up suggestions are optional and risk-gated.

## Procedure

1. State the source basis and source access level using `docs/SOURCE_LIMITS.md`.
2. Follow the procedure in the skill's `SKILL.md`.
3. Produce the stated output format and keep verified facts, interpretation, speculation, and recommendation separate.
4. End with verification gaps. Add a risk-gated follow-up only when it is useful.

## Quality checks

- Evidence strength must match claim strength.
- Missing source access must be marked clearly.
- Uncertainty, limits, and user verification needs must be visible.

## Failure modes

- Fabricated scholarly facts or verification.
- Confident synthesis from partial sources.
- Generic prose or structure that hides weak evidence or weak reasoning.

## Files/folders it may read

- This skill's `SKILL.md`, `README.md`, relevant `assets/`, `references/`, and `agents/openai.yaml`.
- User-provided project material explicitly named in the request.

## Files/folders it may write

- None by default.
- User-requested artifacts or notes in the current project.

## What it must not do

- Invent missing scholarly facts or verification.
- Treat unavailable evidence as confirmed.
- Claim external searches, source checks, or database access that did not happen.

## Best next steps

Name only follow-ups that reduce a concrete scholarly risk.
