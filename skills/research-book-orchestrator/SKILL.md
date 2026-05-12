---
name: research-book-orchestrator
description: Coordinate a full research nonfiction or research book workflow. Use for project planning, routing tasks across research agenda, source discovery, literature review, argument design, chapter work, evidence ledgers, citation audits, and manuscript revision.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# Research Book Orchestrator

## Purpose

Coordinate a serious research-book workflow from idea to manuscript. This skill does not replace the specialized skills. It decides which skill should be used next, sequences the work, and keeps the project grounded in scholarly standards.

Use `docs/ARCHITECTURE.md` as the stage map and `MODE_REGISTRY.md` as the route registry when the user asks for a full workflow, mode choice, or package-level orchestration.

## Use this skill when

- The user has a broad book idea and needs a complete workflow.
- The user is unsure whether to start with sources, outline, argument, chapters, or citation audit.
- The task spans multiple phases of a research nonfiction manuscript.
- The project involves academic standards, evidence management, citations, literature review, or peer-review style critique.

## Do not use this skill when

- The user asks for a narrow one-step task that clearly belongs to another skill.
- The user only wants a stylistic edit, citation audit, literature map, or chapter outline.
- The project is pure fiction or casual writing without research standards.

## Core routing map

Use these routes:

| User need | Route to skill |
|---|---|
| Broad idea, scope, research questions | `scholarly-research-agenda` |
| Search terms, databases, source plan | `systematic-source-discovery` |
| Schools of thought, debates, gaps | `literature-review-mapper` |
| Source summaries and annotations | `annotated-bibliography-builder` |
| Credibility, method, bias, evidence quality | `methodology-source-auditor` |
| Claims needing evidence or safer wording | `claim-evidence-ledger` |
| Thesis tree, warrants, argument sequence | `argument-architecture` |
| Strong objections and rival explanations | `counterargument-peer-review` |
| Chapter design and section flow | `chapter-architecture` |
| Style, clarity, research readability | `scholarly-prose-editor` |
| Citation verification and quote/page audit | `citation-integrity-auditor` |
| Whole-manuscript coherence | `manuscript-continuity-editor` |
| Case studies and real-world examples | `case-study-integration` |
| Book proposal and positioning | `book-proposal-scholarship` |

## Operating principles

1. Start from the book's intellectual contribution, not from prose.
2. Separate discovery, interpretation, argument, drafting, and verification.
3. Track evidence before producing confident prose.
4. Never invent citations, page numbers, quotations, studies, or bibliographic details.
5. Flag uncertainty instead of smoothing it over.
6. Include opposing literatures and rival explanations early.
7. Keep a claim-evidence ledger for all major factual and causal claims.
8. Treat theory, empirical evidence, source records, case studies, and normative argument as different kinds of support.

## Workflow

### 1. Diagnose project phase

Classify the project into one or more phases:

- Phase A: concept and scope
- Phase B: source discovery
- Phase C: literature mapping
- Phase D: argument architecture
- Phase E: chapter architecture
- Phase F: drafting and style
- Phase G: evidence and citation audit
- Phase H: whole-manuscript continuity
- Phase I: proposal and external positioning

### 2. Identify missing inputs

List only high-impact missing inputs. Do not stall if the user has provided enough to proceed. Infer a reasonable workflow and mark assumptions.

### 3. Choose next skill sequence

Recommend a sequence of 3–6 skills. For each, explain:

- purpose
- expected output
- dependency on prior work
- risk it reduces

### 4. Produce a concrete work plan

Create a plan with deliverables. Prefer concrete artifacts: research agenda, search log, literature map, thesis tree, chapter brief, claim ledger, citation audit, continuity memo.

When the user requests machine-readable artifacts, use `shared/contracts/book/book_artifact.schema.json`. The supported artifact types are:

- `book_research_agenda`
- `source_discovery_log`
- `literature_map`
- `thesis_tree`
- `chapter_brief`
- `claim_evidence_ledger`
- `continuity_review`
- `book_proposal`

### 5. Enforce scholarly quality gates

At each transition, check:

- Are the central terms defined?
- Are major claims classified by type?
- Are primary and secondary sources separated?
- Are influential opposing viewpoints represented?
- Are causal claims supported by stronger evidence than analogy?
- Are speculative claims labeled as speculative?

## Output format

```markdown
# Research Book Workflow Plan

## Project diagnosis

## Assumptions I am making

## Recommended skill sequence
| Step | Skill | Why now | Output | Risk reduced |

## Immediate next deliverable

## Quality gates

## Longer-term manuscript roadmap
```

## Common failure modes

- Starting with a chapter draft before the thesis and evidence are stable.
- Treating all sources as equal.
- Using case studies as proof when they are only illustrations.
- Ignoring literatures that would challenge the user's preferred thesis.
- Producing a confident synthesis without source verification.
