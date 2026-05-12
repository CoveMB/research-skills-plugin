---
name: book-proposal-scholarship
description: Develop a serious research nonfiction book proposal with thesis, contribution, audience, market/field positioning, chapter summaries, comparable titles, and sample-material plan.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# Book Proposal Scholarship

## Purpose

Create a serious research nonfiction book proposal suitable for academic presses, serious trade presses, agents, or grant/fellowship applications.

## When to use

Use when the user has a book idea, outline, chapter summaries, literature map, or partial manuscript and needs a proposal structure.

## Inputs expected

- Book premise, thesis, proposal draft, outline, chapter summaries, literature map, or manuscript sample.
- Intended press, agent, fellowship, grant, or internal planning use.
- Audience, author positioning, comparable titles, source base, timeline, and sample chapter status when available.
- Verification status for comparable titles, market claims, and publication facts.

## Proposal components

Include:

- title and subtitle options
- one-sentence premise
- central thesis
- contribution to field or public debate
- audience
- why now
- chapter summaries
- methods/source base
- comparable titles
- author positioning
- manuscript status and timeline
- sample chapter strategy

## Source basis and AI limits

Before drafting a proposal, state the source access level as one of:

- user-provided full text
- excerpt only
- citation only
- model knowledge only
- live/current search needed

Every output must separate source basis, what can be verified from available material, what remains uncertain, and what the user must verify. Do not invent citations, page numbers, quotations, DOIs, datasets, market facts, field consensus, source metadata, or claims of having searched a database. Separate verified facts, interpretation, speculation, and recommendation.

## Files/folders it may read

- This skill's `SKILL.md`, `README.md`, `assets/book-proposal-template.md`, and `agents/openai.yaml`.
- User-provided proposals, outlines, chapter summaries, literature maps, sample chapters, CV notes, and comparable-title lists explicitly named in the request.
- Related book artifacts when proposal claims depend on prior research work.

## Files/folders it may write

- None by default.
- May create or update user-requested proposal drafts, comparable-title tables, or submission notes in the current project.
- Must not overwrite proposal or manuscript files unless explicitly asked.

## What it must not do

- Do not invent comparable titles, publication facts, sales data, market data, or press preferences.
- Do not overstate originality, timeliness, audience size, or author authority.
- Do not hide weak source base behind confident proposal language.

## Procedure

### 1. Identify proposal type

Infer or ask whether the proposal is for:

- academic press
- trade press
- agent
- fellowship/grant
- dissertation-to-book conversion
- internal project planning

### 2. Clarify contribution

State what the book contributes that existing work does not.

### 3. Position audience

Separate primary and secondary audiences. Academic books can still need a public-facing hook; trade books still need credibility.

### 4. Build chapter summaries

Each summary should include chapter purpose, core claim, evidence/cases, and relation to overall thesis.

### 5. Identify comparable titles

If verified current comparable titles are not available, request source discovery or web/library search. Do not invent publication details.

Mark comparable titles, audience claims, market claims, and timing claims as verified, unverified, or needed. Do not present unverified positioning as market fact.

### 6. Create development plan

Recommend missing research, proposal materials, and sample chapter priorities.

## Output format

```markdown
# Research Book Proposal Draft

## Source basis

## What I can verify

## What remains uncertain

## User verification needed

## Working title options

## One-sentence premise

## Core thesis

## Contribution

## Audience

## Why now

## Methods and source base

## Chapter summaries

## Comparable titles needed / known
| Title or need | Verification status | Source pointer | Positioning note |

## Audience / market claim verification
| Claim | Verification status | Source basis | Needed next step |

## Author positioning

## Manuscript status and timeline

## Sample chapter recommendation

## Risks to solve before submission

## Limits / failure risks

## Next best skill
```

## Quality checks

- Do not overstate originality.
- Do not invent comparable titles or market data.
- Academic proposal style should be specific about contribution and source base.
- Trade proposal style should be specific about reader need and narrative hook.
- Label public relevance and market timing claims as claims needing evidence unless verified.

## Failure modes

- Proposal sounds persuasive but rests on unverified market claims.
- Comparable titles are fabricated, stale, or poorly matched.
- Chapter summaries list topics without evidence or argument function.
- Audience positioning is too broad to guide press or agent fit.
