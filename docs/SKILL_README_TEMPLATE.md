# Skill README template

Use this structure when adding or refreshing a skill README. Put skill-specific guidance near the top. Keep shared safety language short and link to shared docs when possible.

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

Describe the main output. Note that follow-up suggestions are optional and risk-gated.
For low-load or accessibility-facing skills, say whether the output should prefer tables, short chunks, or ambiguity flags.

## Procedure

1. State the source basis and source access level using the available source-access policy (including, but not limited to, `docs/SOURCE_LIMITS.md` in this project or an equivalent policy in another project).
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

- Bundled skill instructions, metadata, and assets if available (including, but not limited to, `SKILL.md`, `README.md`, `assets/`, `references/`, and `agents/openai.yaml` in this project or equivalent files in another project).
- User-provided project material explicitly named in the request.

## Files/folders it may write

- None by default.
- User-requested artifacts or notes in the user-designated project or workspace.

## What it must not do

- Invent missing scholarly facts or verification.
- Treat unavailable evidence as confirmed.
- Claim external searches, source checks, or database access that did not happen.

## Best next steps

Name only follow-ups that reduce a concrete scholarly risk.
