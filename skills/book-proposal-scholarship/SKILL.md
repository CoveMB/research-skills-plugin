---
name: book-proposal-scholarship
description: Develop a research nonfiction book proposal when a project needs thesis, contribution, audience, market or field positioning, chapter summaries, comparable titles, and sample-material planning.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# Book proposal scholarship

## Purpose

Create a research nonfiction book proposal suitable for academic presses, trade presses, agents, or grant or fellowship applications.

## When to use

Use when the user has a book idea, outline, chapter summaries, literature map, or partial manuscript and needs a proposal structure.

## Automatic selection guidance

- High-signal triggers: book proposal, press proposal, pitch, contribution, audience, comparable titles, positioning, chapter summaries, or sample-material plan.
- Light-route behavior: draft proposal architecture and mark market, comparable-title, and positioning claims by verification status.
- Deep-work gate: only validate comparable titles, press lists, market facts, or publication facts when the user asks for lookup, provides sources, or arrives through router deep mode.
- Noise and slowdown guard: do not invent market facts, comparable titles, sales claims, or field consensus.

## Do not use this skill when

- The thesis, audience, or chapter structure is not stable enough for proposal work.
- The user only needs comparable titles or positioning claims verified; use `book-comps-verifier`.
- The user only needs prose polishing; use `scholarly-prose-editor`.
- The user asks for citation or source verification; use `citation-integrity-auditor`.

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

Use `docs/SOURCE_LIMITS.md` for source-access rules. Keep source access level, What I can verify, What remains uncertain, and User verification needed visible. Do not invent citations or source support.

Use `docs/CORPUS_REPRESENTATIVENESS_TAXONOMY.md` for contribution-to-field, originality, timeliness, field-positioning, comparable-title set, or market-coverage claims. Supplied comps are supplied evidence, not market-level coverage, unless a representative or protocol-bounded comp search is visible.

## Machine-readable artifacts

When the user explicitly asks for JSON or a contract artifact, use `shared/contracts/book/book_artifact.schema.json` with `artifact_type: book_proposal`. If the output is normal Markdown, do not force the JSON contract. For durable handoff artifacts, follow `docs/PROCESS_PASSPORT.md`: set `handoff_artifact: true`, include `process_passport`, and preserve upstream passport limits instead of upgrading verification.

## Files/folders it may read

- Shared operational boundary doc: `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.
- Shared policy docs, especially `docs/SOURCE_LIMITS.md` and `docs/AUTO_SELECTION_GUARDRAILS.md`.
- User-provided proposals, outlines, chapter summaries, literature maps, sample chapters, CV notes, and comparable-title lists explicitly named in the request.
- Related book artifacts when proposal claims depend on prior research work.

## Files/folders it may write

- None by default.
- May create or update user-requested proposal drafts, comparable-title tables, or submission notes in the user-designated project or workspace.
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

Distinguish supplied comps from market-level evidence. Label a small, stale, or user-selected comp list as `partial_corpus`, `convenience_corpus`, `stale_corpus`, or `unknown_coverage` before using it for positioning strength.

### 6. Create development plan

Recommend missing research, proposal materials, and sample chapter priorities.

## Output format

```markdown
# Research book proposal draft

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

## Scholarship / market coverage limits

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

```

Use the optional Suggested next step policy in `docs/AUTO_SELECTION_GUARDRAILS.md`; it may be omitted unless a follow-on skill reduces a named scholarly risk.

## Quality checks

- Do not overstate originality.
- Do not invent comparable titles or market data.
- Academic proposal style should be specific about contribution and source base.
- Trade proposal style should be specific about reader need and narrative hook.
- Label public relevance and market timing claims as claims needing evidence unless verified.
- Supplied comps must not be treated as market-level evidence without a corpus coverage label and verification path.

## Failure modes

- Proposal sounds persuasive but rests on unverified market claims.
- Comparable titles are fabricated, stale, or poorly matched.
- Chapter summaries list topics without evidence or argument function.
- Audience positioning is too broad to guide press or agent fit.
- Premature citation audit before citations, quotes, page numbers, bibliography entries, or cited claims exist.
