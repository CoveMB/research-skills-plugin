# Live Capture Prompt: metadata-lookup-consented-identifiers

Skill: `citation-integrity-auditor`
Source access level: `external-lookup-consented`
Visible source packet: `tests/skill_evals/scholar_grade/corpora/metadata-lookup-consented-identifiers/source-packet.md`

## Operator Rules

- Use only the visible source packet below.
- Do not use hidden answer keys or fixture expectation fields during the skill run.
- Save the live skill response as Markdown before scoring.

## Prompt

Use citation-integrity-auditor. I consent to external metadata lookup for these public DOI identifiers only; do not send notes or draft text.

## Visible Source Packet

# Source Packet

Source basis: public DOI identifiers plus explicit lookup consent.

Available material:
- User consent for external metadata lookup of public identifiers only.
- DOI-like public identifiers from a bibliography list.

Missing material:
- No private notes or draft text may be submitted.
- Lookup results must be recorded before metadata can be treated as verified.
