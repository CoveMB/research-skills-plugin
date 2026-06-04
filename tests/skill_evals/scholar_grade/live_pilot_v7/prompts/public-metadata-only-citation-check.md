# Live Capture Prompt: public-metadata-only-citation-check

Skill: `citation-integrity-auditor`
Source access level: `public-metadata-only`
Visible source packet: `tests/skill_evals/scholar_grade/corpora/public-metadata-only-citation-check/source-packet.md`

## Operator Rules

- Use only the visible source packet below.
- Do not use hidden answer keys or fixture expectation fields during the skill run.
- Save the live skill response as Markdown before scoring.

## Prompt

Use citation-integrity-auditor. Check DOI-bearing bibliography metadata using only public identifiers; do not inspect draft text.

## Visible Source Packet

# Source Packet

Source basis: public citation identifiers only.

Available material:
- DOI-like public identifiers from a bibliography list.
- No draft text, private notes, source excerpts, or full text.

Missing material:
- No draft text was inspected.
- No source full text is available.
