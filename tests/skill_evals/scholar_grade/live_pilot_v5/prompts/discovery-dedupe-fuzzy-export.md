# Live Capture Prompt: discovery-dedupe-fuzzy-export

Skill: `discovery-runner-deduper`
Source access level: `controlled-packet`
Visible source packet: `tests/skill_evals/scholar_grade/corpora/discovery-dedupe-fuzzy-export/source-packet.md`

## Operator Rules

- Use only the visible source packet below.
- Do not use hidden answer keys or fixture expectation fields during the skill run.
- Save the live skill response as Markdown before scoring.

## Prompt

Use discovery-runner-deduper. Dedupe this candidate-source export with duplicate DOI rows, fuzzy title matches, and a planned search that was not run.

## Visible Source Packet

# Synthetic Source Packet: Discovery Dedupe Fuzzy Export

This packet is synthetic and exists only for evaluation. It is not a real search export.

## Available material

- Row 1 and Row 2 share the same DOI.
- Row 3 has a similar title but no DOI.
- Search log lists Database A as completed and Database B as planned.

## Missing material

- Authority file for metadata correction.
- Human decision on fuzzy title match.
- Completed results for Database B.
