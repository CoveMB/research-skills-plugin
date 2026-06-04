---
name: research-book-orchestrator
description: Coordinate a full research nonfiction or research book workflow when a project spans multiple stages, has an unclear next step, or mixes accessibility triage, agenda, sources, literature review, argument, chapters, evidence ledgers, citation audits, and manuscript revision.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# Research book orchestrator

## Purpose

Coordinate a research-book workflow with scholarly standards from idea to manuscript and external sharing. This skill does not replace the specialized skills. It decides which skill should be used next, sequences the work, and keeps the project grounded in scholarly standards.

Use `docs/reference/ARCHITECTURE.md` as the stage map and `MODE_REGISTRY.md` as the route registry when the user asks for a full workflow, mode choice, or package-level orchestration.

## When to use

- The user has a broad book idea and needs a complete workflow.
- The user is unsure whether to start with accessibility triage, sources, outline, argument, chapters, or citation audit.
- The task spans multiple phases of a research nonfiction manuscript, source trail, proposal, or release packet.
- The project involves academic standards, evidence management, citations, figures/tables, AI-assisted workflow integrity, literature review, or peer-review style critique.

## Inputs expected

- Book premise, working thesis, table of contents, chapter draft, proposal, or source list.
- User's intended audience, discipline, manuscript stage, deadline, and known constraints when available.
- Current materials available for verification: sources, excerpts, notes, bibliography, case notes, or prior artifacts.
- The user's main uncertainty about what to do next.

## Do not use this skill when

- The user asks for a narrow one-step task that clearly belongs to another skill.
- The user only wants a stylistic edit, citation audit, literature map, or chapter outline.
- The project is pure fiction or casual writing without research standards.

## Automatic selection guidance

- High-signal triggers: broad multi-stage research book task, unclear next step, or mixed request spanning accessibility triage, sources, notes, extraction, argument, chapters, evidence, citations, proposal, release, and revision.
- Light-route behavior: produce a workflow diagnosis and route sequence without performing source validation itself.
- Deep-work gate: send source lookup, citation verification, and claim audits to specialized skills only when the route requires them.
- Noise and slowdown guard: do not replace narrow specialist skills when the user's request has one clear owner.

## Core routing map

Use `docs/policy/ROUTING_MATRIX.md` as the canonical route table. This skill should summarize only the route sequence needed for the user-designated project or workspace, not duplicate the full route matrix.

## Operating principles

1. Start from the book's intellectual contribution, not from prose.
2. Separate discovery, interpretation, argument, drafting, and verification.
3. Track evidence before producing confident prose.
4. Never invent citations, page numbers, quotations, studies, or bibliographic details.
5. Flag uncertainty instead of smoothing it over.
6. Include opposing literatures and rival explanations early.
7. Keep a claim-evidence ledger for all major factual and causal claims.
8. Treat theory, empirical evidence, source records, case studies, and normative argument as different kinds of support.
9. Use the smallest accessibility skill before workflow routing when text friction hides the author's intended claim or next action.

## Source basis and AI limits

Use `docs/policy/SOURCE_LIMITS.md` for source-access rules. Keep source access level, What I can verify, What remains uncertain, and User verification needed visible. Do not invent citations or source support.

Use `docs/policy/PROCESS_PASSPORT.md` when a workflow plan, artifact sequence, or generated project artifact is saved as durable project state or handed to another skill. Preserve upstream source-access, evidence-status, corpus-coverage, unresolved-risk, and handoff-limit labels; do not turn routing confidence into scholarly verification.

## Files/folders it may read

- Shared operational boundary doc: `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`.
- Shared policy docs, especially `docs/policy/SOURCE_LIMITS.md`, `docs/policy/PROCESS_PASSPORT.md`, and `docs/policy/AUTO_SELECTION_GUARDRAILS.md`.
- `docs/reference/ARCHITECTURE.md`, `MODE_REGISTRY.md`, `docs/policy/QUALITY_STANDARD.md`, and `shared/contracts/book/book_artifact.schema.json` when routing, artifacts, or quality gates matter.
- User-provided files, drafts, notes, bibliographies, and artifacts explicitly named in the request.

## Files/folders it may write

- None by default.
- May create or update user-requested workflow plans or book artifacts in the user-designated project or workspace when explicitly asked.
- Must not rewrite skill files, source files, external libraries, or citation databases unless the user explicitly requests that maintenance work.

## What it must not do

- Do not skip source, literature, argument, evidence, or citation gates to produce confident prose faster.
- Do not treat routing recommendations as proof that the underlying scholarship is sound.
- Do not fabricate missing sources, market facts, field consensus, or manuscript status.

## Procedure

### 1. Diagnose project phase

Classify the project into one or more phases:

- Phase A: concept and scope
- Phase A0: accessibility triage for rough notes, dictation, spelling ambiguity, dense material, reading fatigue, or prose repair
- Phase B: source discovery
- Phase C: source notes, extraction, and candidate screening
- Phase D: literature mapping
- Phase E: argument architecture
- Phase F: chapter architecture
- Phase G: drafting and style
- Phase H: evidence, traceability, and citation audit
- Phase H1: figure/table integrity and scholarly integrity gate
- Phase I: whole-manuscript continuity
- Phase J: proposal, comparable titles, AI/human workflow log, and release review

### 2. Identify missing inputs

List only high-impact missing inputs. Do not stall if the user has provided enough to proceed. Infer a reasonable workflow and mark assumptions.

### 3. Apply phase gates

Do not route directly to drafting or prose polish when the agenda, source plan, or claim-evidence status is weak. If a gate is not met, name the blocked phase, explain the risk, and route to the skill that resolves it.

Block or qualify forward movement when:

- rough input or reading load hides the intended claim or next action
- central question, audience, or scope is undefined
- source plan is missing or only anecdotal
- literature map is one-sided or based on a narrow corpus
- thesis claims lack evidence status
- citation or quotation verification is unavailable
- figures, tables, generated syntheses, or automated analyses lack provenance or human checkpoint status
- existing prose needs meaning-preserving surface repair before broader revision

### 4. Choose next skill sequence

Recommend a sequence of 3–6 skills. For each, explain:

- purpose
- expected output
- dependency on prior work
- risk it reduces

### 5. Produce a concrete work plan

Create a plan with deliverables. Prefer concrete artifacts: research agenda, search log, literature map, thesis tree, chapter brief, claim ledger, citation audit, continuity memo.

When the user requests machine-readable artifacts, use `shared/contracts/book/book_artifact.schema.json`. Durable handoff artifacts must set `handoff_artifact: true`, include `process_passport`, and preserve upstream passport limits. The supported artifact types are:

- `book_research_agenda`
- `source_discovery_log`
- `literature_map`
- `thesis_tree`
- `chapter_brief`
- `claim_evidence_ledger`
- `source_note`
- `extraction_table`
- `annotated_bibliography`
- `methodology_source_audit`
- `claim_traceability_graph`
- `peer_review_report`
- `citation_integrity_audit`
- `figure_table_integrity_audit`
- `case_study_dossier`
- `scholarly_integrity_audit`
- `ai_human_workflow_log`
- `rights_privacy_release_audit`
- `comps_verification`
- `continuity_review`
- `style_sheet`
- `book_proposal`

### 6. Enforce scholarly quality gates

At each transition, check:

- Are the central terms defined?
- Are major claims classified by type?
- Are primary and secondary sources separated?
- Are influential opposing viewpoints represented?
- Are causal claims supported by stronger evidence than analogy?
- Are speculative claims labeled as speculative?
- Do figures/tables have data provenance, caption/axis checks, and rights status where needed?
- Do AI-assisted workflow steps have human checkpoints, override reasons, and disclosure notes where needed?

## Output format

```markdown
# Research book workflow plan

## Source basis

## What I can verify

## What remains uncertain

## User verification needed

## Project diagnosis

## Assumptions I am making

## Recommended skill sequence
| Step | Skill | Why now | Output | Risk reduced |

## Immediate next deliverable

## Quality gates

## Limits / failure risks

## Longer-term manuscript roadmap

## Process passport, if saved or handed downstream
```

## Failure modes

- Starting with a chapter draft before the thesis and evidence are stable.
- Treating all sources as equal.
- Using case studies as proof when they are only illustrations.
- Ignoring literatures that would challenge the user's preferred thesis.
- Producing a confident synthesis without source verification.
- Letting generated analysis, figures, or tables support manuscript claims without provenance and integrity checks.

## Quality checks

- The recommended sequence must name the risk each step reduces.
- Block drafting when phase gates are not met.
- Make assumptions and verification gaps visible.
- Prefer concrete artifacts over vague next steps.
- Saved workflow plans or downstream artifact handoffs include a process passport without upgrading verification status.
