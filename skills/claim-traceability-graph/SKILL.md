---
name: claim-traceability-graph
description: Map manuscript or note claims to claim IDs, source notes, citekeys, locators, and evidence status when traceability, unsupported claims, orphan claims, or incomplete evidence chains need review.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# Claim traceability graph

## Purpose

Map claims to their evidence chain: claim ID, source note, citation, locator, verification status, missing link, and repair action.

## When to use

Use when the user asks whether claims are traceable, whether the evidence chain is complete, or where unsupported or orphan claims exist.

## Automatic selection guidance

- High-signal triggers: claim traceability, evidence chain, orphan claim, unsupported claim with source notes, claim ID, locator chain, graph of support, or trace audit.
- Light-route behavior: map supplied claims to supplied evidence pointers and mark gaps.
- Deep-work gate: source lookup or quote verification happens only when requested, when source existence is central, or when router deep mode routes here with lookup available.
- Noise and slowdown guard: do not rebuild a claim ledger when the user only needs chain completeness.

## Do not use this skill when

- The user needs claims extracted and classified first; use `claim-evidence-ledger`.
- The user needs citation formatting or quote verification; use `citation-integrity-auditor`.
- The user needs source credibility assessed; use `methodology-source-auditor`.

## Inputs expected

- Manuscript passage, outline, claim list, or note set.
- Existing claim IDs, source notes, claim ledger, citations, citekeys, and locators when available.
- The chapter, section, or artifact where the claim appears.
- Any known evidence status labels or verification rules.

## Source basis and AI limits

Use `docs/policy/SOURCE_LIMITS.md` for source-access rules. Keep source access level, What I can verify, What remains uncertain, and User verification needed visible. Do not invent citations or source support.

## Machine-readable artifacts

When the user explicitly asks for JSON or a contract artifact, use `shared/contracts/book/book_artifact.schema.json` with `artifact_type: claim_traceability_graph`. If the output is normal Markdown, do not force the JSON contract. For durable handoff artifacts, follow `docs/policy/PROCESS_PASSPORT.md`: set `handoff_artifact: true`, include `process_passport`, and preserve upstream passport limits instead of upgrading verification.

For durable workflow traces, use or recommend `python3 scripts/check_workflow_traceability.py --trace path/to/workflow-trace.json`. The helper checks structural claim traceability only: referenced but undefined claim IDs, orphan definitions, duplicate claim IDs, silent claim-text or claim-type drift, unsupported evidence upgrades, removed source locators, removed source-basis labels, unresolved-risk removal, and same-source/multiple-claim-type links lacking a source-claim-fit note. It does not decide whether a claim is persuasive or whether a source actually supports it.

## Files/folders it may read

- Shared operational boundary doc: `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`.
- Shared policy docs, especially `docs/policy/SOURCE_LIMITS.md` and `docs/policy/AUTO_SELECTION_GUARDRAILS.md`.
- User-provided drafts, source notes, claim ledgers, citations, bibliographies, and project files explicitly named in the request.

## Files/folders it may write

- None by default.
- May create or update user-requested traceability tables, graph notes, or repair logs in the user-designated project or workspace.
- Must not rewrite manuscript, source notes, claim ledgers, or bibliography files unless explicitly asked.

## What it must not do

- Do not treat nearby citations as proof.
- Do not invent missing source notes, citekeys, locators, or page support.
- Do not collapse partial support, missing support, and failed verification into one label.

## Procedure

### 1. Identify claims and pointers

Use existing claim IDs when supplied. If no IDs exist, assign temporary IDs and label them as generated for this audit.

### 2. Trace each chain

For each claim, record manuscript location, claim type, source note pointer, citation or citekey, locator, evidence status, and verification basis.

When the same source pointer is used for different claim types, add a source-claim-fit note explaining the limited structural basis for that link. Do not treat this note as proof of support; it only records why the link needs review or how it should be checked.

### 3. Test the links

Check whether each link is present. A citation near a sentence is not proof that the source supports that claim.

### 4. Mark missing or weak links

Separate missing source note, missing citation, missing locator, weak source fit, unavailable verification, and unsupported in provided material.

### 5. Recommend repairs

Give the smallest repair action: add locator, connect source note, revise claim, find stronger source, mark interpretation, or remove unsupported claim.

## Output format

```markdown
# Claim traceability graph

## Source basis

## What I can verify

## What remains uncertain

## User verification needed

## Traceability table
| Claim ID | Claim text | Type | Ledger / source note pointer | Citation / citekey | Locator need | Verification status | Missing link | Repair action |

## Orphan claims

## Claims with nearby citations but no proven support

## Optional graph notation

## Repair priorities

## Limits / failure risks

```

Use the optional Suggested next step policy in `docs/policy/AUTO_SELECTION_GUARDRAILS.md`; it may be omitted unless a follow-on skill reduces a named scholarly risk.

## Quality checks

- Each claim has a visible chain status.
- Nearby citation is never treated as proof by proximity.
- Direct quotes and passage-specific claims require locators.
- Verification unavailable is not the same as verification failed.

## Failure modes

- Claim extraction expands beyond traceability needs.
- Nearby citation is counted as source support.
- Missing locator gaps are hidden by a confident status.
- Repair actions ask for broad research when a locator or source-note link would solve the gap.
- Premature citation audit before citations, quotes, page numbers, bibliography entries, or cited claims exist.
