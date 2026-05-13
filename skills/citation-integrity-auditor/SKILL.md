---
name: citation-integrity-auditor
description: Audit citation accuracy when drafts, footnotes, bibliographies, quotes, paraphrases, page numbers, source-claim fit, fabricated-reference risk, or unsupported cited claims need verification.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# Citation integrity auditor

## Purpose

Protect a manuscript from citation errors, fabricated references, unsupported claims, quotation problems, and source-claim mismatches.

## When to use

Use when the user has a draft with citations, footnotes, bibliography, quoted material, paraphrases, or claims that need verification.

## Automatic selection guidance

- High-signal triggers: citation accuracy, unsupported claims, quotes, page numbers, bibliography mismatch, source-claim fit, fabricated-reference risk, or citation audit.
- Light-route behavior: classify verification availability and mark unverified items without guessing.
- Deep-work gate: exact quote, page, DOI, or source-claim verification requires source text, images, PDFs, database access, explicit lookup, or router deep mode with available lookup tools.
- Noise and slowdown guard: a nearby citation is not proof; do not resolve missing locators from memory.

## Do not use this skill when

- The draft has claims but few or no citations; use `claim-evidence-ledger` first.
- The claim-to-source-note chain is unclear before citation verification; use `claim-traceability-graph`.
- The user asks to find sources rather than check existing citations; use `systematic-source-discovery`.
- The user only wants style editing with no evidentiary check.

## Inputs expected

- Draft text with citations, footnotes, bibliography entries, paraphrases, or quotes.
- Source text, excerpts, page images, PDFs, links, or notes needed to verify claims.
- Citation style and locator requirements when formatting matters.
- Known high-risk claims, quotes, or sources the user wants prioritized.

## Hard rules

- Never invent bibliographic details, page numbers, DOIs, quotations, or citations.
- If the source text is not available, mark verification as unavailable.
- A citation nearby does not automatically support the claim.
- Distinguish citation formatting issues from evidentiary issues.
- Treat direct quotes as requiring exact source text and page/locator verification.

## Source basis and AI limits

Follow `docs/SOURCE_LIMITS.md`: state the source access level, separate source basis from interpretation, include What I can verify, What remains uncertain, and User verification needed. Do not invent citations or source support.

## Machine-readable artifacts

When the user explicitly asks for JSON or a contract artifact, use `shared/contracts/book/book_artifact.schema.json` with `artifact_type: citation_integrity_audit`. If the output is normal Markdown, do not force the JSON contract.

## Audit categories

Label each issue as:

- unsupported claim
- citation needed
- citation-source mismatch
- overstatement relative to source
- quotation needs verification
- paraphrase too close to source language
- page number / locator needed
- bibliography detail missing
- source type too weak for claim
- outdated source risk
- contradictory evidence not addressed

Use distinct verification statuses:

- verification unavailable: source text or metadata was not provided
- verification failed: available source does not support the claim or quote
- verification partial: source is relevant but locator, context, or exact wording is missing
- verification passed: source content and locator support the claim

## Metadata verification ladder

Use this metadata verification ladder before calling a reference real or bibliographically sound:

1. DOI or stable identifier match from a source such as Crossref, publisher page, OpenAlex, Semantic Scholar, library catalogue, or repository record.
2. normalized title match with author-year and venue agreement.
3. fuzzy title match only when differences are explainable, such as punctuation, subtitle, transliteration, or edition variation.
4. Bibliography-only match remains unverified unless an authoritative record or full text is available.

Flag identifier hijack risk when the DOI, URL, title, author, year, or venue points to a different work than the manuscript claims. Do not repair metadata from memory.

## Files/folders it may read

- Bundled skill instructions, metadata, and assets if available (including, but not limited to, `SKILL.md`, `README.md`, `assets/`, `references/`, and `agents/openai.yaml` in this project or equivalent files in another project).
- Shared policy docs, especially `docs/SOURCE_LIMITS.md` and `docs/AUTO_SELECTION_GUARDRAILS.md`.
- User-provided drafts, citation lists, bibliography files, source excerpts, page images, PDFs, and notes explicitly named in the request.
- Related claim ledgers when citation audit depends on claim classification.

## Files/folders it may write

- None by default.
- May create or update user-requested citation audits, checklists, or repair notes in the user-designated project or workspace.
- Must not modify bibliography databases, citation keys, source files, or manuscript files unless explicitly asked.

## What it must not do

- Do not mark verification as passed without source content and locator support.
- Do not call unavailable verification a failed citation.
- Do not assume a nearby citation supports the specific claim.

## Procedure

### 1. Extract claims requiring support

Prioritize factual, causal, quantitative, field-specific, and controversial claims.

### 2. Check citation linkage

For each claim, identify the citation meant to support it. If no citation is present, flag it.

Flag the citation-proximity fallacy: a nearby citation does not prove the specific claim unless the source content actually supports it.

### 2.1. Verify citation metadata when needed

Apply the metadata verification ladder when fabricated-reference risk, DOI risk, bibliography mismatch, or source identity is central to the request.

### 3. Assess source strength

If source details are available, assess whether the source type can support the claim.

### 4. Audit quotations

For quotes:

- check exactness only if source text is provided
- require page/locator
- flag ellipsis/bracket issues if visible
- ensure quote is not taken out of context where context is available

### 5. Recommend fixes

Offer safer wording, stronger source types, or citation placement changes.

## Output format

```markdown
# Citation integrity audit

## Source basis

## What I can verify

## What remains uncertain

## User verification needed

## Summary verdict

## Claim-level audit
| Claim | Current citation | Verification status | Issue type | Severity | What is needed | Suggested fix |

## Quotation audit

## Bibliography issues

## Metadata verification ladder results
| Reference | DOI / identifier | Title match | Author-year match | Venue match | Status | Repair task |

## High-priority repairs

## Claims safe as interpretation or argument

## Limits / failure risks

## Suggested next step

```

Use the optional Suggested next step policy in `docs/AUTO_SELECTION_GUARDRAILS.md`; it may be omitted unless one skill reduces a named scholarly risk.

## Severity scale

- Critical: possible fabricated source, false claim, or serious source mismatch.
- Major: claim likely needs citation or stronger support.
- Moderate: citation placement, page, or wording issue.
- Minor: formatting or style issue.

## Quality checks

- Do not claim a citation is correct unless source content was available.
- Do not turn every interpretive claim into a citation demand.
- Flag weak support, especially when a weak source supports a strong causal claim.
- Prefer precise statements over citation padding.
- Do not mark verification as failed when the source is unavailable; mark it unavailable.

## Failure modes

- Citation proximity is mistaken for source-claim fit.
- Missing source text leads to invented verification.
- Formatting issues distract from evidentiary problems.
- Direct quotes are checked without exact source text and locator.
- Premature follow-on skill suggestion when the citation audit resolves the only concrete scholarly risk.
