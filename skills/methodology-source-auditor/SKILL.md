---
name: methodology-source-auditor
description: Evaluate source credibility when articles, books, reports, datasets, case studies, journalism, or web sources need method, evidence quality, bias, generalizability, and source-claim support limits audited.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# Methodology source auditor

## Purpose

Assess whether sources are credible enough for a research book and identify what claims each source can legitimately support.

## When to use

Use when the user has articles, books, reports, source data, case studies, working papers, journalism, or web sources and needs source quality evaluated.

## Automatic selection guidance

- High-signal triggers: source credibility, methodology, evidence quality, bias, generalizability, source strength, or whether a source can support a specific claim.
- Light-route behavior: audit only the provided or named sources against the claims they are meant to support.
- Deep-work gate: broad literature search happens only when needed to compare source quality, when the user asks, or when router deep mode routes here with lookup available.
- Noise and slowdown guard: do not turn a targeted source audit into a full literature review.

## Do not use this skill when

- The user needs source discovery; use `systematic-source-discovery`.
- The user needs structured source notes; use `annotated-bibliography-builder`.
- The user needs quote/page verification; use `citation-integrity-auditor`.

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

Follow `docs/SOURCE_LIMITS.md`: state the source access level, separate source basis from interpretation, include What I can verify, What remains uncertain, and User verification needed. Do not invent citations or source support.

## Files/folders it may read

- This skill's `SKILL.md`, `README.md`, `assets/source-audit-rubric.md`, and `agents/openai.yaml`.
- `docs/SOURCE_LIMITS.md` for shared source-access and verification rules.
- `docs/AUTO_SELECTION_GUARDRAILS.md` for shared automatic-trigger guardrails.
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
# Source methodology audit

## Source basis

## What I can verify

## What remains uncertain

## User verification needed

| Source | Type | Method/evidence | Credibility | Bias risk | Can support | Cannot support | Only contextual | Use recommendation |

## High-risk sources

## Missing stronger evidence

## Recommended upgrades

## Limits / failure risks

## Suggested next step

```

Use the optional Suggested next step policy in `docs/AUTO_SELECTION_GUARDRAILS.md`. The section may be omitted. If included, it must identify the named scholarly risk it reduces and use one skill only.

## Quality checks

- Do not equate prestige with correctness.
- Do not equate citation count with truth.
- Do not use persuasive sources as neutral proof.
- Do not generalize from a single case without warning.
- Treat old sources carefully: they may be canonical but not current.
- Do not claim methodological quality is high unless method and evidence are visible enough to assess.
- Suggested next step must reduce a named scholarly risk, not promote a skill because it exists.

## Failure modes

- Source verdict ignores what claim the source is meant to support.
- Audit overgeneralizes from source type without reading visible evidence.
- Contextual sources are treated as direct evidence.
- Missing method details are converted into false confidence.
- Premature citation audit before citations, quotes, page numbers, bibliography entries, or cited claims exist.
