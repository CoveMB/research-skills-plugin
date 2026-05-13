# Skill operational boundaries

This file is the shared operating policy for skill READMEs. Individual READMEs should keep skill-specific purpose, inputs, examples, output expectations, and best next steps.

## Procedure

1. State the source basis and source access level.
2. Follow the skill's `SKILL.md` procedure instead of working from memory.
3. Produce the stated output format and keep verified facts, interpretation, speculation, and recommendation separate.
4. End with verification gaps. Add a risk-gated follow-up only when it is useful and does not add avoidable reading load.
5. For accessibility work, follow `docs/ROUTING_MATRIX.md`: use the smallest clear accessibility skill first, and use `dyslexia-research-companion` only for mixed or unclear bottlenecks.
6. For compact output in accessibility work, use one source-basis line, one table or revised passage, ambiguity only when it could change meaning, and one next action. Compact output is an output shape, not a route mode.
7. For compact output in routing, audit, gate, or verifier work, keep the source basis, main route or verdict, decision-changing gaps, and one next action visible.
8. For compact output, include `How to use this result: [status] - [full sentence]` with `TRIAGE ONLY`, `BLOCKER SUMMARY`, or `LIMITED GATE DECISION`.
9. Escalate from compact output to full review before the result supports manuscript claims, external release, legal/privacy decisions, citation verification, method credibility, or final submission.

## Quality checks

- Evidence strength must match claim strength.
- Missing source access must be marked clearly.
- Uncertainty, limits, and user verification needs must be visible.
- Output should preserve scholarly caution without becoming vague.
- If the request involves rough notes, dictation, spelling ambiguity, or reading fatigue, preserve meaning and keep the output easy to scan.
- Compact output must reduce reading load without hiding uncertainty, verification gaps, blocker status, or meaning-changing ambiguity.
- Compact output must make reliance limits explicit enough that the user knows whether it is triage, blocker summary, or limited gate decision.
- Compact output status explanations must be full sentences, not shorthand labels alone.

## Failure modes

- Fabricated citations, quotes, page numbers, source metadata, datasets, market facts, or field consensus.
- Confident synthesis from partial sources.
- Generic prose or structure that hides weak evidence or weak reasoning.
- Overstated claims, missing counterarguments, or unclear source basis.
- Overcorrected text that changes the author's intended claim.
- AI-assisted workflow steps used without a human checkpoint, disclosure basis, or integrity gate when they support manuscript claims.
- Figures, tables, or charts treated as evidence without data provenance, caption/axis checks, or duplicate visual review.

## Files/folders it may read

- Bundled skill instructions, metadata, and assets if available, including `SKILL.md`, `README.md`, `assets/`, `references/`, and `agents/openai.yaml`.
- User-provided drafts, notes, sources, artifacts, or project files explicitly named in the request.
- Shared project documentation when it is needed for workflow, quality, or artifact compatibility.

## Files/folders it may write

- None by default.
- May create or update user-requested research artifacts, notes, drafts, or review files in the user-designated project or workspace.
- Must not overwrite source material, bibliography databases, manuscript files, or plugin files without explicit user request.

## What it must not do

- Invent missing scholarly facts or verification.
- Treat unavailable evidence as confirmed.
- Use style polish to mask weak argument, weak sources, or unsupported claims.
- Claim external searches, source checks, or database access that did not happen.
