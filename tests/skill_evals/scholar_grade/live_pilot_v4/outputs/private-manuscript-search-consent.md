# Research intent route

## Source basis

Private unpublished manuscript text, but the passage itself is redacted. Source access level: `private-no-external`.

## Research mode

Active mode: normal mode.

## Classification

- Intent: discover related sources
- Artifact stage: manuscript
- Source access level: private-no-external
- Risk level: high, because unpublished private text must not be submitted to external search tools

## Recommended skill route

| Step | Skill | Why now | Output | Risk reduced |
|---|---|---|---|---|
| 1 | research-intent-router | The request asks for source discovery using private manuscript material, so consent and safe-search boundaries must be set before lookup. | Private-safe routing decision and next action. | Prevents leaking unpublished text into external services. |

## Deep lookup decision

No external lookup should be performed now.

Reason: the only manuscript content is private and redacted, and the packet states that external lookup requires explicit consent and a safe payload. No non-sensitive topic terms are visible, so search terms cannot be derived without guessing.

## What I can verify

- The request is a scholarly source-discovery task.
- The manuscript passage must not be searched directly.
- A safe route exists only after converting the private passage into non-sensitive search terms.

## What remains uncertain

- The manuscript topic.
- The field or discipline.
- Which related-source categories are needed.
- Any safe search terms.

## User verification needed

Provide or approve a safe external-search payload, such as topic-only keywords with distinctive phrasing removed. Do not submit unpublished private text externally.

## External tool boundary

Do not search private text externally. The request can be converted into non-sensitive search terms, but none are available from the visible packet.

## Next action

Ask the user for non-sensitive topic keywords or a consent-approved safe search string, then run source discovery from that sanitized payload only.