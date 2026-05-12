---
name: citation-integrity-auditor
description: Audit research drafts for citation accuracy, unsupported claims, quote integrity, page-number needs, fabricated-reference risk, source-claim mismatch, and bibliography problems.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# Citation Integrity Auditor

## Purpose

Protect a manuscript from citation errors, fabricated references, unsupported claims, quotation problems, and source-claim mismatches.

## When to use

Use when the user has a draft with citations, footnotes, bibliography, quoted material, paraphrases, or claims that need verification.

## Hard rules

- Never invent bibliographic details, page numbers, DOIs, quotations, or citations.
- If the source text is not available, mark verification as unavailable.
- A citation nearby does not automatically support the claim.
- Distinguish citation formatting issues from evidentiary issues.
- Treat direct quotes as requiring exact source text and page/locator verification.

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

## Workflow

### 1. Extract claims requiring support

Prioritize factual, causal, quantitative, field-specific, and controversial claims.

### 2. Check citation linkage

For each claim, identify the citation meant to support it. If no citation is present, flag it.

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
# Citation Integrity Audit

## Summary verdict

## Claim-level audit
| Claim | Current citation | Issue type | Severity | What is needed | Suggested fix |

## Quotation audit

## Bibliography issues

## High-priority repairs

## Claims safe as interpretation or argument

## Next best skill
```

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
