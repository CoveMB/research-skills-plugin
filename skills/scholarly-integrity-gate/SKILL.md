---
name: scholarly-integrity-gate
description: Audit scholar-grade research workflows, AI-assisted papers, draft analyses, source pipelines, or book artifacts for integrity failure modes such as hallucinated evidence, methodology fabrication, implementation bugs, shortcut reliance, frame-lock, weak human checkpoints, and override decisions.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# Scholarly integrity gate

## Purpose

Run a narrow integrity gate before research outputs become draft claims, manuscript sections, proposals, or shareable artifacts. This skill checks whether the workflow itself is reliable, not whether the prose sounds persuasive.

Use it to catch AI research failure modes that ordinary citation review can miss: implementation bug, hallucinated evidence, methodology fabrication, shortcut reliance, duplicate or recycled results, frame-lock, missing adversarial review, and weak human checkpoint records.

## When to use

Use when a research project, AI-assisted analysis, literature synthesis, evidence ledger, paper draft, book chapter, or generated artifact needs a pass/fail/hold integrity decision before the next stage.

Use this before relying on generated research claims, generated reviews, automated source discovery, computed results, extracted tables, or high-stakes synthesis.

## Automatic selection guidance

- High-signal triggers: integrity gate, failure mode audit, AI research failure, hallucinated result, methodology fabrication, implementation bug, shortcut reliance, frame-lock, human checkpoint, override decision, or before moving from generated analysis to manuscript claims.
- Light-route behavior: classify the visible workflow and name the smallest integrity checks needed before forward movement.
- Deep-work gate: only audit source content, code, data, figures, or citations when those materials are provided or lookup/tool access is explicitly available.
- Noise and slowdown guard: do not run a broad integrity audit when the user needs a narrow citation, source, prose, or accessibility task.

## Do not use this skill when

- The user only needs citation-source fit checked; use `citation-integrity-auditor`.
- The user only needs source credibility assessed; use `methodology-source-auditor`.
- The user only needs a human/AI decision record or disclosure log; use `ai-human-workflow-log`.
- The user only needs figure or table provenance checked; use `figure-table-integrity-auditor`.

## Inputs expected

- Research workflow summary, artifact, draft section, claim ledger, source log, analysis notes, code output, table, figure, or review report.
- Source access level, data/code availability, tool-use history, and known human checkpoints.
- Intended next stage: synthesis, drafting, proposal, publication, peer review, public release, or internal decision.
- Any override decisions the user wants recorded or evaluated.

## Source basis and AI limits

Follow `docs/SOURCE_LIMITS.md`: state the source access level, separate source basis from interpretation, include What I can verify, What remains uncertain, and User verification needed. Do not invent citations or source support.

## Machine-readable artifacts

When the user explicitly asks for JSON or a contract artifact, use `shared/contracts/book/book_artifact.schema.json` with `artifact_type: scholarly_integrity_audit`. If the output is normal Markdown, do not force the JSON contract.

## Files/folders it may read

- Bundled skill instructions, metadata, and assets if available (including, but not limited to, `SKILL.md`, `README.md`, `assets/`, `references/`, and `agents/openai.yaml` in this project or equivalent files in another project).
- Shared policy docs, especially `docs/SOURCE_LIMITS.md` and `docs/AUTO_SELECTION_GUARDRAILS.md`.
- User-provided drafts, ledgers, source logs, analysis notes, code outputs, figures, tables, audit reports, and project files explicitly named in the request.
- Related claim, citation, methodology, figure/table, or workflow logs when the integrity decision depends on them.

## Files/folders it may write

- None by default.
- May create or update user-requested integrity audit reports, checkpoint logs, or repair lists in the user-designated project or workspace.
- Must not alter data, source files, manuscripts, bibliography databases, or generated outputs unless explicitly asked.

## What it must not do

- Do not treat a clean-looking output as valid without visible evidence, provenance, or verification.
- Do not invent citations, source support, data provenance, code behavior, human approval, or override rationale.
- Do not clear a stage when key evidence is unavailable; use INSUFFICIENT EVIDENCE.

## Procedure

### 1. Declare source and workflow basis

State what is visible: sources, claims, data, code, search logs, extraction tables, citations, figures, tool history, and human checkpoints.

### 2. Classify integrity checks

Check only relevant failure classes:

- implementation bug: code, formula, extraction, parsing, or automation error can change result
- hallucinated evidence: source, quote, metadata, fact, or support is not verified
- methodology fabrication: method, sample, instrument, search process, or analysis design is claimed without evidence
- shortcut reliance: generated summaries, abstracts, snippets, or convenience sources replace needed reading
- frame-lock: the workflow only tests the user's preferred thesis or search vocabulary
- duplicate or recycled result: table, figure, case, or source appears reused without provenance
- missing human checkpoint: stage advanced without user decision, rationale, or unresolved-risk record

### 3. Assign verdicts

Use one verdict per check:

- CLEAR: visible evidence supports moving forward
- SUSPECTED: there is a concrete warning sign requiring repair
- INSUFFICIENT EVIDENCE: material needed for the check is unavailable
- OVERRIDDEN: a human checkpoint chose to proceed despite a named unresolved risk

### 4. Name the gate decision

Use pass, pass with conditions, hold, or escalate. A hold should name the blocker and the smallest repair task.

### 5. Route repair work

Recommend one repair owner only when useful: citation audit, methodology audit, claim ledger, figure/table audit, source discovery, or AI-human workflow log.

## Output format

```markdown
# Scholarly integrity gate

## Source basis

## What I can verify

## What remains uncertain

## User verification needed

## Workflow stage under review

## Integrity checks
| Check | Verdict | Evidence visible | Risk | Required repair | Human checkpoint |

## Gate decision

## OVERRIDDEN decisions, if any
| Decision | Override reason | Unresolved risk | Required follow-up |

## Repair priorities

## Limits / failure risks

## Suggested next step
```

Use the optional Suggested next step policy in `docs/AUTO_SELECTION_GUARDRAILS.md`; it may be omitted unless one skill reduces a named scholarly risk.

## Quality checks

- Every CLEAR verdict must cite visible evidence or provenance.
- SUSPECTED and INSUFFICIENT EVIDENCE must not be softened into pass language.
- OVERRIDDEN requires a human decision, override reason, unresolved risk, and follow-up.
- Integrity checks should be specific to the workflow stage, not a generic warning list.

## Failure modes

- Passing generated analysis because it is plausible.
- Treating absent provenance as low risk.
- Letting shortcut reliance, frame-lock, or methodology fabrication hide behind fluent prose.
- Recording an override without the human checkpoint that authorized it.
