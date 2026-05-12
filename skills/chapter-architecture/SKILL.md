---
name: chapter-architecture
description: Design research nonfiction chapters with purpose, central question, main claim, concept definitions, evidence placement, counterarguments, transitions, and revision priorities.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# Chapter Architecture

## Purpose

Turn research, notes, or a chapter idea into a coherent chapter architecture. A chapter should have a job in the book, a question, a claim, a sequence, and evidence.

## When to use

Use when the user is planning, restructuring, or diagnosing a chapter in a research nonfiction manuscript.

## Inputs expected

- Chapter idea, draft, notes, outline, chapter summary, or book-level thesis.
- Intended chapter function, target audience, known evidence, and missing evidence when available.
- Prior and next chapter context if transition or continuity matters.
- Any cases, concepts, sources, or counterarguments that must appear.

## Source basis and AI limits

Before designing the chapter, state the source access level as one of:

- user-provided full text
- excerpt only
- citation only
- model knowledge only
- live/current search needed

Every output must separate source basis, what can be verified from available material, what remains uncertain, and what the user must verify. Do not invent citations, page numbers, quotations, DOIs, datasets, market facts, field consensus, source metadata, or claims of having searched a database. Separate verified facts, interpretation, speculation, and recommendation.

## Files/folders it may read

- This skill's `SKILL.md`, `README.md`, `assets/chapter-brief-template.md`, and `agents/openai.yaml`.
- User-provided chapter drafts, outlines, notes, source excerpts, thesis trees, and continuity artifacts explicitly named in the request.
- Adjacent chapter files when the user asks for transitions or whole-book fit.

## Files/folders it may write

- None by default.
- May create or update user-requested chapter briefs, outlines, or planning notes in the current project.
- Must not rewrite manuscript chapters unless the user explicitly asks for drafting or restructuring edits.

## What it must not do

- Do not produce a topic list without section claims and evidence anchors.
- Do not add unsupported facts, examples, or citations.
- Do not make transitions solve gaps in argument or evidence.

## Procedure

### 1. Define chapter function

Choose one or more:

- introduces the problem
- defines key concepts
- reviews a literature
- develops theory
- presents a case study
- analyzes evidence
- handles counterarguments
- synthesizes prior chapters
- proposes an intervention
- transitions to next part

### 2. State central question and claim

Every chapter needs a central question and a chapter-level thesis.

### 3. Build section sequence

Use this pattern unless another pattern fits better:

1. opening problem or puzzle
2. stakes
3. concept definitions
4. literature or context
5. core argument
6. evidence/case analysis
7. counterargument or complication
8. synthesis
9. bridge to next chapter

### 4. Place evidence deliberately

Assign evidence to claims rather than sections alone. Mark where citations, examples, figures, or primary-source excerpts are needed.

Each section must have an evidence anchor: provided source, planned source type, case dossier, conceptual authority, or verification needed. Warn when a section is only a topic and does not carry an argument.

### 5. Add reader guidance

Write transitions that explain why the reader is moving from one section to the next.

### 6. Identify draft risks

Common risks:

- too much literature summary
- no chapter-level claim
- unclear connection to book thesis
- example-heavy but argument-light
- concept introduced too late
- unsupported causal claims
- weak ending

## Output format

```markdown
# Chapter Architecture

## Source basis

## What I can verify

## What remains uncertain

## User verification needed

## Chapter purpose

## Central question

## Chapter thesis

## Key concepts to define

## Proposed section outline
| Section | Function | Key claim | Evidence anchor | Evidence needed | Transition purpose |

## Counterarguments to include

## Opening options

## Ending / bridge to next chapter

## Research still needed

## Revision risks

## Limits / failure risks

## Next best skill
```

## Quality checks

- A chapter outline must not be only a list of topics.
- Every section must have a function and claim.
- Include counterargument or complication where appropriate.
- Endings should synthesize, not merely stop.
- Do not turn a topic list into a chapter plan without claims and evidence anchors.

## Failure modes

- Chapter sequence summarizes literature without advancing the thesis.
- Evidence placement is vague or detached from claims.
- Case study sections become anecdotal proof.
- Opening and ending are stylistic but not argumentative.
