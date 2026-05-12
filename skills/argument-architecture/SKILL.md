---
name: argument-architecture
description: Build a research book-level thesis tree with claims, warrants, evidence, assumptions, counterarguments, chapter sequence, and argumentative dependencies.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# Argument Architecture

## Purpose

Design the book's argument as a structure rather than a plain outline. This skill builds thesis trees, warrants, assumptions, evidence paths, and chapter dependencies.

## When to use

Use when the user has a thesis, notes, research agenda, literature map, or draft and needs a coherent book-level argument.

## Inputs expected

- Provisional thesis, research agenda, literature map, outline, notes, or draft.
- Known evidence, missing evidence, counterarguments, and target audience.
- Proposed chapter sequence or table of contents when available.
- Source access level for evidence claims that shape the argument.

## Key distinction

An outline orders topics. An argument architecture orders claims and evidence. Prefer argument architecture before chapter drafting.

## Source basis and AI limits

Before designing the argument, state the source access level as one of:

- user-provided full text
- excerpt only
- citation only
- model knowledge only
- live/current search needed

Every output must separate source basis, what can be verified from available material, what remains uncertain, and what the user must verify. Do not invent citations, page numbers, quotations, DOIs, datasets, market facts, field consensus, source metadata, or claims of having searched a database. Separate verified facts, interpretation, speculation, and recommendation.

## Files/folders it may read

- This skill's `SKILL.md`, `README.md`, `assets/thesis-tree-template.md`, and `agents/openai.yaml`.
- User-provided agendas, literature maps, notes, outlines, drafts, and source summaries explicitly named in the request.
- Related claim ledgers or chapter briefs when argument dependency depends on them.

## Files/folders it may write

- None by default.
- May create or update user-requested thesis trees or argument architecture artifacts in the current project.
- Must not rewrite manuscript files or source materials unless explicitly asked.

## What it must not do

- Do not make a thesis sound proven when evidence is only planned.
- Do not hide weak dependencies behind elegant wording.
- Do not omit serious counterarguments because they threaten the user's preferred thesis.

## Procedure

### 1. State the strongest defensible thesis

Write a thesis that is bold but supportable. Avoid claims that require evidence the user does not have.

### 2. Build a thesis tree

Create:

- main thesis
- supporting claims
- warrants explaining why each claim supports the thesis
- evidence needed
- counterarguments
- chapter placement

### 3. Identify assumptions

Separate:

- empirical assumptions
- conceptual assumptions
- normative assumptions
- positional assumptions
- methodological assumptions

### 4. Test argumentative dependency

Ask: if this claim fails, does the whole thesis fail? Mark claims as:

- essential
- important but replaceable
- contextual
- illustrative

Add failure impact for each claim. Mark claims that could collapse the thesis without stronger evidence.

### 5. Build chapter logic

Each chapter should advance the argument, not simply cover a topic. Assign a function:

- define the problem
- establish context or background
- review literature
- introduce theory
- present evidence
- handle counterargument
- synthesize
- propose intervention

### 6. Generate stronger and weaker thesis variants

Offer versions:

- bold thesis
- moderate thesis
- conservative thesis
- public-facing thesis
- academic thesis

## Output format

```markdown
# Argument Architecture

## Source basis

## What I can verify

## What remains uncertain

## User verification needed

## Main thesis

## Thesis variants

## Thesis tree
| Claim | Warrant | Evidence needed | Counterargument | Dependency | Failure impact | Chapter |

## Hidden assumptions

## Chapter-level argument sequence

## Weak links

## Stronger formulation

## Limits / failure risks

## Next best skill
```

## Quality checks

- Do not confuse topic order with argument order.
- Every chapter must have a function in the thesis.
- Make assumptions explicit.
- Include the strongest counterargument at the architecture stage, not after drafting.
- Avoid single-factor determinism or reductionism unless strongly evidenced.
- Do not make a thesis sound proven when the evidence path is only proposed.

## Failure modes

- Output is a topic outline rather than a claim dependency map.
- Essential claims lack evidence or failure-impact labels.
- Thesis variants become rhetorical polish instead of different defensibility levels.
- Argument sequence ignores what available sources can actually support.
