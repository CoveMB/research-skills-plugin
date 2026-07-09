# Live Capture Prompt: raw-materials-manuscript-boundary

Skill: `research-book-orchestrator`
Source access level: `controlled-packet`
Visible source packet: `tests/skill_evals/scholar_grade/corpora/raw-materials-manuscript-boundary/source-packet.md`

## Operator Rules

- Use only the visible source packet below.
- Do not use hidden answer keys or fixture expectation fields during the skill run.
- Save the live skill response as Markdown before scoring.

## Prompt

Use research-book-orchestrator. Turn this raw idea summary, research log, source notes, and draft figure idea into a staged manuscript preparation plan.

## Visible Source Packet

# Source packet: raw materials manuscript boundary

Available material:

- Idea summary: The project argues that municipal climate adaptation plans often promise resilience while leaving maintenance labor underfunded.
- Research log: The author has notes from three city planning reports, but no full citations or page locators in this packet.
- Draft figure idea: A timeline comparing plan publication dates and maintenance budget revisions. No dataset is supplied.
- Draft section claim: "Cities consistently shift climate maintenance work onto underfunded departments."

Missing material:

- Full planning reports
- Bibliographic metadata
- Page locators
- Dataset for the timeline
- Human verification record

Allowed output:

- Create a staged workflow.
- Mark source and visual gaps.
- Route to source discovery, source notes, figure/table audit, claim ledger, and integrity gate.

Forbidden output:

- Do not claim the reports support the draft claim.
- Do not claim the figure is ready.
- Do not claim the manuscript is submission-ready.
