---
name: book-comps-verifier
description: Verify comparable titles and positioning claims for research nonfiction proposals, press pitches, agent queries, grant applications, audience claims, market claims, timeliness claims, and publication positioning.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# Book comps verifier

## Purpose

Verify comparable titles and positioning claims for research nonfiction proposals, pitches, grants, fellowships, and publication planning.

## When to use

Use when the user is building or checking comparable titles, audience claims, market claims, timeliness claims, press positioning, or proposal positioning.

## Automatic selection guidance

- High-signal triggers: comparable titles, comps, comp verification, press positioning, agent pitch comps, audience claim, market claim, why now, publication positioning, or proposal comps.
- Light-route behavior: verify only supplied comps and mark speculative comp needs.
- Deep-work gate: live or current lookup is needed to verify publication details unless the user supplies authoritative source data.
- Noise and slowdown guard: do not draft a full proposal when the user only needs comps checked.

## Do not use this skill when

- The user needs a whole proposal drafted; use `book-proposal-scholarship`.
- The user needs sources for the book's argument; use `systematic-source-discovery`.
- The user asks for sales data or market facts without sources or lookup permission.

## Inputs expected

- Comparable title list, proposal section, press pitch, agent query, grant application, or positioning notes.
- Title, author, publisher, year, edition, format, and source pointers when available.
- The user's book premise, audience, method, form, and press category.
- Any claims about timeliness, readership, market fit, or press list.

## Source basis and AI limits

Use `docs/SOURCE_LIMITS.md` for source-access rules. Keep source access level, What I can verify, What remains uncertain, and User verification needed visible. Do not invent citations or source support.

Use `docs/CORPUS_REPRESENTATIVENESS_TAXONOMY.md` when the comp set is used to imply market coverage, press-category coverage, field positioning, timeliness, or absence of better comps. Verifying individual titles is not the same as verifying a representative comp corpus.

## Compact output

Use compact output when the user asks for low reading load, comp blockers, or a fast proposal-positioning check. Compact output should keep source basis and lookup needs visible, show only comps or claims whose status changes positioning, and end with one next action.

## Machine-readable artifacts

When the user explicitly asks for JSON or a contract artifact, use `shared/contracts/book/book_artifact.schema.json` with `artifact_type: comps_verification`. If the output is normal Markdown, do not force the JSON contract. For durable handoff artifacts, follow `docs/PROCESS_PASSPORT.md`: set `handoff_artifact: true`, include `process_passport`, and preserve upstream passport limits instead of upgrading verification.

## Files/folders it may read

- Shared operational boundary doc: `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.
- Shared policy docs, especially `docs/SOURCE_LIMITS.md` and `docs/AUTO_SELECTION_GUARDRAILS.md`.
- User-provided proposal drafts, comp lists, source pointers, press notes, bibliographies, and project files explicitly named in the request.

## Files/folders it may write

- None by default.
- May create or update user-requested comp verification tables, positioning notes, or proposal repair notes in the user-designated project or workspace.
- Must not rewrite proposals, query letters, or submission materials unless explicitly asked.

## What it must not do

- Do not invent comparable titles, publication facts, sales data, market data, press preferences, or audience facts.
- Do not call a title verified without a source basis.
- Do not treat a thematically related book as a good comp unless audience, method, form, or press category also fits.

## Procedure

### 1. Separate comp types

Classify each item as verified comparable title, unverified comparable title, speculative comparable need, or positioning claim.

Classify the comp set itself as supplied, partial, convenience-selected, stale, field-balanced, or unknown coverage before using it for market-level or field-positioning claims.

### 2. Verify available details

Check title, author, publisher, year, edition, format, and source pointer where possible. Mark each detail as verified, unverified, missing, or needs lookup.

### 3. Explain comparability

Assess topic, audience, method, form, press category, scale, and date fit. State why the comp helps and where it misleads.

### 4. Audit positioning claims

Flag stale, mismatched, fabricated, unsupported, or overbroad audience and market claims. Do not invent sales or market data.

### 5. Recommend repairs

Suggest replacement criteria, missing verification tasks, safer wording, or comp gaps to fill.

## Output format

```markdown
# Book comps verification

## Source basis

## What I can verify

## What remains uncertain

## User verification needed

## Comparable-title verification table
| Title / need | Author | Publisher | Year | Verification status | Why comparable | Mismatch risk | Source basis | Repair task |

## Positioning notes

## Audience / market / timeliness claims
| Claim | Status | Source basis | Risk | Repair action |

## Comp corpus coverage

## Stale, mismatched, fabricated, or unverified comps

## Missing verification tasks

## Limits / failure risks

```

Compact output:

```markdown
# Comps check

Source basis: [one line]
How to use this result: TRIAGE ONLY - Use this only for visible comp-fit triage; do not treat it as market or proposal clearance.

| Comp or claim | Status | Fit or mismatch | Verification needed |

Ambiguity: [only if it could change proposal positioning]
Next action: [one action]
```

Use the optional Suggested next step policy in `docs/AUTO_SELECTION_GUARDRAILS.md`; it may be omitted unless a follow-on skill reduces a named scholarly risk.

## Quality checks

- Each comp has a reason tied to topic, audience, method, form, or press category.
- Publication details are marked by verification status.
- Speculative comp needs are not presented as actual titles.
- Market and sales claims stay unverified unless sources support them.
- Supplied comps are distinguished from market-level evidence.

## Failure modes

- Famous books are chosen because they sound impressive rather than comparable.
- Publication details are filled from memory.
- Market claims are presented without evidence.
- A full proposal draft hides weak or stale comps.
- Premature citation audit before citations, quotes, page numbers, bibliography entries, or cited claims exist.
