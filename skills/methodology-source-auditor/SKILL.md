---
name: methodology-source-auditor
description: Evaluate source credibility, methodology, evidence quality, bias, generalizability, and what each source can or cannot support in a research manuscript.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# Methodology Source Auditor

## Purpose

Assess whether sources are credible enough for a research book and identify what claims each source can legitimately support.

## When to use

Use when the user has articles, books, reports, source data, case studies, working papers, journalism, or web sources and needs source quality evaluated.

## Inputs expected

- Source text, excerpt, citation, abstract, dataset description, or report details.
- Claim or manuscript section each source is expected to support.
- Field, method context, publication venue, author information, and date when available.
- Known concerns about bias, generalizability, recency, or source type.

## Evaluation dimensions

Assess each source by:

- source type
- author expertise
- publication venue
- method
- evidence quality
- transparency and reproducibility
- context and recency
- positional or financial incentives
- sample size or case selection where relevant
- generalizability
- relation to opposing evidence

## Source basis and AI limits

Before auditing, state the source access level as one of:

- user-provided full text
- excerpt only
- citation only
- model knowledge only
- live/current search needed

Every output must separate source basis, what can be verified from available material, what remains uncertain, and what the user must verify. Do not invent citations, page numbers, quotations, DOIs, datasets, market facts, field consensus, source metadata, or claims of having searched a database. Separate verified facts, interpretation, speculation, and recommendation.

## Files/folders it may read

- This skill's `SKILL.md`, `README.md`, `assets/source-audit-rubric.md`, and `agents/openai.yaml`.
- User-provided sources, excerpts, data descriptions, bibliographies, and manuscript files explicitly named in the request.
- Related claim ledgers or chapter notes when source-use fit depends on them.

## Files/folders it may write

- None by default.
- May create or update user-requested source audit tables or notes in the current project.
- Must not edit original sources, datasets, citation databases, or external files unless explicitly asked.

## What it must not do

- Do not equate prestige, citation count, or confident prose with truth.
- Do not rate method quality as high when the method and evidence are unavailable.
- Do not treat persuasive material as neutral proof.

## Procedure

### 1. Classify source type

Use categories:

- peer-reviewed empirical article
- peer-reviewed theoretical article
- academic monograph
- edited volume chapter
- review article
- primary or source document
- documentation or reference material
- dataset or source data
- institutional or organizational report
- persuasive publication
- journalism
- opinion/essay

### 2. Identify method and evidence

For each source, identify its design, evidence base, interpretive framework, and limitations. Use field-specific method names only if they are provided or verifiable.

### 3. Determine supportable claims

For each source, list what it can support, what it cannot support, and what it can only contextualize. Mark this as the source-use verdict.

### 4. Assign credibility level

Use:

- High: strong venue, transparent method, appropriate evidence, limited overreach.
- Medium: useful but limited by method, age, scope, or contested interpretation.
- Low: persuasive, weak method, unclear evidence, or primarily rhetorical.
- Contextual: valuable as a primary source or object of analysis, not as neutral evidence.

### 5. Recommend usage

Decide whether to use as core evidence, contextual support, counterpoint, object of critique, or not use.

## Output format

```markdown
# Source Methodology Audit

## Source basis

## What I can verify

## What remains uncertain

## User verification needed

| Source | Type | Method/evidence | Credibility | Bias risk | Can support | Cannot support | Only contextual | Use recommendation |

## High-risk sources

## Missing stronger evidence

## Recommended upgrades

## Limits / failure risks

## Next best skill
```

## Quality checks

- Do not equate prestige with correctness.
- Do not equate citation count with truth.
- Do not use persuasive sources as neutral proof.
- Do not generalize from a single case without warning.
- Treat old sources carefully: they may be canonical but not current.
- Do not claim methodological quality is high unless method and evidence are visible enough to assess.

## Failure modes

- Source verdict ignores what claim the source is meant to support.
- Audit overgeneralizes from source type without reading visible evidence.
- Contextual sources are treated as direct evidence.
- Missing method details are converted into false confidence.
