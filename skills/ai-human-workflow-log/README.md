# ai-human-workflow-log

## What it does

Use this skill to record AI-assisted research decisions, human checkpoints, override reasons, affected sections, verification responsibilities, and disclosure notes.

## When to use it

Use it when AI-assisted work is headed toward external sharing, submission, publication, proposal review, or a high-stakes manuscript stage.

Use it after an integrity gate reports OVERRIDDEN or when the user asks for AI-use disclosure.

## Good inputs

- AI tool use or workflow notes.
- Human decisions, approvals, overrides, or unresolved risks.
- Sections, artifacts, or files affected by AI assistance.
- Venue, press, committee, or collaborator disclosure expectations.

## Example requests

```text
Create an AI/human workflow log for this research project.
```

```text
Record the human checkpoints and disclosure notes for this AI-assisted chapter draft.
```

## Typical output

Expect checkpoint tables, AI assistance records, affected sections, verification responsibilities, disclosure notes, unresolved risks, and a risk-gated next step when useful.

## Operational boundaries

Follow `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`.

## Best next steps

After this skill, use `rights-privacy-release-auditor` before external sharing or `scholarly-integrity-gate` if unresolved risks need a pass/hold decision.
