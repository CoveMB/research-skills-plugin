# Live Capture Prompt: claim-traceability-nearby-citation

Skill: `claim-traceability-graph`
Source access level: `controlled-packet`
Visible source packet: `tests/skill_evals/scholar_grade/corpora/claim-traceability-nearby-citation/source-packet.md`

## Operator Rules

- Use only the visible source packet below.
- Do not use hidden answer keys or fixture expectation fields during the skill run.
- Save the live skill response as Markdown before scoring.

## Prompt

Use claim-traceability-graph. Check whether a nearby citation actually supports a stronger claim in the draft.

## Visible Source Packet

# Synthetic Source Packet: Claim Traceability Nearby Citation

This packet is synthetic and exists only for evaluation. It is not a real claim graph.

## Available material

- Draft sentence: "Dashboard adoption reduced congestion in all pilot cities. [Source A]"
- Source note A: "The city launched a public dashboard in 2021."

## Missing material

- Evidence of congestion reduction.
- Evidence for all pilot cities.
- Direct trace from source note to the stronger claim.
