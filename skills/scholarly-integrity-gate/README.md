# scholarly-integrity-gate

## What it does

Use this skill to audit research workflows and generated artifacts for integrity failure modes before they become manuscript claims or shareable outputs.

It produces a verdict table with CLEAR, SUSPECTED, INSUFFICIENT EVIDENCE, or OVERRIDDEN decisions.

## When to use it

Use it before relying on AI-assisted analyses, generated literature syntheses, source pipelines, claim ledgers, tables, figures, or high-stakes manuscript sections.

## Good inputs

- Workflow summary, generated artifact, claim ledger, source log, analysis output, or draft section.
- Source access, data/code availability, and tool-use history.
- Human checkpoints or override decisions, if any.

## Example requests

```text
Run a scholarly integrity gate on this source-discovery and synthesis workflow.
```

```text
Check whether this generated analysis has hallucinated evidence, methodology fabrication, shortcut reliance, or frame-lock risk.
```

## Typical output

Expect source basis, visible verification, integrity checks, verdicts, gate decision, override table, repair priorities, and a risk-gated next step when useful. Ask for compact output when you want the gate decision, blockers, required repair, human checkpoint, and one next action. Compact output should include `How to use this result: LIMITED GATE DECISION - Use this as a proceed/hold/repair decision based only on visible evidence, provenance, and named human checkpoints.` It changes output shape, not route selection or evidence requirements.

## Procedure

Follow the shared procedure in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.

## Quality checks

Apply the shared quality checks in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`; keep any skill-specific caveats visible in the output.

## Failure modes

Use the shared failure modes in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`; call out the skill-specific failure most relevant to the request.

## Files/folders it may read

Follow the shared read boundary in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.

## Files/folders it may write

Follow the shared write boundary in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.

## What it must not do

Follow the shared prohibitions in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.

## Best next steps

After this skill, use the single repair skill named by the gate. Use `ai-human-workflow-log` when a checkpoint, override, or disclosure record needs to be preserved.
