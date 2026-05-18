# Live Capture Prompt: implementation-bug-without-clean-run

Skill: `scholarly-integrity-gate`
Source access level: `controlled-packet`
Visible source packet: `tests/skill_evals/scholar_grade/corpora/implementation-bug-without-clean-run/source-packet.md`

## Operator Rules

- Use only the visible source packet below.
- Do not use hidden answer keys or fixture expectation fields during the skill run.
- Save the live skill response as Markdown before scoring.

## Prompt

Use scholarly-integrity-gate. This computed table supports a chapter claim, but the only run record shows warnings and a nonzero exit.

## Visible Source Packet

# Synthetic Source Packet: Implementation Bug Without Clean Run

This packet is synthetic and exists only for evaluation. It is not a real experiment record.

## Available material

- Draft claim: Table 2 shows the parser improved extraction accuracy.
- Run record: `exit_code=1`.
- Warning: `division by zero encountered in metric aggregation`.
- Table status: copied from the failed run output directory.

## Missing material

- No clean rerun.
- No saved script hash.
- No independent recomputation.
