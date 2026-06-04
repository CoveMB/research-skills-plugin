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
- retraction, correction, expression-of-concern, predatory-venue, questionable-source, or paper-mill risk when status evidence is available or lookup is permitted
- positional or financial incentives
- sample size or case selection where relevant
- generalizability
- relation to opposing evidence

## Method-family references

Use method-family references only when the source's method matters to the claim. Keep the SKILL body concise and load or request field-specific guidance when needed. Load only the relevant one-level reference file:

- qualitative: `references/qualitative.md`
- historical: `references/historical.md`
- legal: `references/legal.md`
- computational: `references/computational.md`
- survey: `references/survey.md`
- observational: `references/observational.md`
- experimental: `references/experimental.md`
- systematic review: `references/systematic-review.md`

Useful families include qualitative, historical, legal, computational, survey, observational, experimental, systematic review, dataset, and mixed-methods work.

For each family, ask method-specific questions:

- qualitative: sampling, coding, positionality, triangulation, and transferability
- historical: archive basis, source survival, chronology, and presentism risk
- legal: jurisdiction, authority level, date, procedural posture, and doctrinal fit
- computational: dataset provenance, model/code availability, evaluation, leakage, and reproducibility
- survey: sampling frame, instrument, response rate, weighting, and construct validity
- observational: confounding, selection, measurement, and causal limits
- experimental: randomization, controls, power, attrition, and ecological validity
- systematic review: protocol, search coverage, screening, exclusion reasons, and synthesis method
- quantitative or statistical claims: denominator, units, time window, uncertainty, effect-size comparability, transformation logic, and whether combining estimates would be a valid synthesis method

## Source basis and AI limits

Use `docs/policy/SOURCE_LIMITS.md` for source-access rules. Keep source access level, What I can verify, What remains uncertain, and User verification needed visible. Do not invent citations or source support.

Use `docs/policy/CORPUS_REPRESENTATIVENESS_TAXONOMY.md` when auditing a source set, review article, evidence map, or claim of generalizability, consensus, missing evidence, or source balance. Source quality and corpus representativeness are separate judgments.

## Machine-readable artifacts

When the user explicitly asks for JSON or a contract artifact, use `shared/contracts/book/book_artifact.schema.json` with `artifact_type: methodology_source_audit`. If the output is normal Markdown, do not force the JSON contract. For durable handoff artifacts, follow `docs/policy/PROCESS_PASSPORT.md`: set `handoff_artifact: true`, include `process_passport`, and preserve upstream passport limits instead of upgrading verification.

## Compact output

Use compact output when the user asks for low reading load, source-use triage, or the strongest/weakest sources only. Compact output should keep source basis and method visibility limits clear, show what each source can and cannot support, and end with one next action.

## Files/folders it may read

- Shared operational boundary doc: `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`.
- Shared policy docs, especially `docs/policy/SOURCE_LIMITS.md` and `docs/policy/AUTO_SELECTION_GUARDRAILS.md`.
- User-provided sources, excerpts, data descriptions, bibliographies, and manuscript files explicitly named in the request.
- Related claim ledgers or chapter notes when source-use fit depends on them.

## Files/folders it may write

- None by default.
- May create or update user-requested source audit tables or notes in the user-designated project or workspace.
- Must not edit original sources, datasets, citation databases, or external files unless explicitly asked.

## What it must not do

- Do not equate prestige, citation count, or confident prose with truth.
- Do not rate method quality as high when the method and evidence are unavailable.
- Do not treat persuasive material as neutral proof.
- Do not turn correlation, temporal order, case evidence, abstracts, or user notes into causal, population-level, or field-general claims.
- Do not perform informal meta-analysis, average incompatible estimates, infer statistical significance, or compare effect sizes unless the data and methods make that operation valid.

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

Use method-family references when a source's method affects what claims it can support.

### 3. Determine supportable claims

For each source, list what it can support, what it cannot support, and what it can only contextualize. Mark this as the source-use verdict.

Separate descriptive, causal, comparative, predictive, and generalizing claims. If the available method does not support the stronger form, give the narrow supportable wording instead of agreeing with the stronger premise.

For numerical claims, check denominators, units, sample or corpus, date range, uncertainty, and calculation basis. If these are missing, mark the number as unverified or descriptive only.

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

## Corpus / source-set limits

## High-risk sources

## Missing stronger evidence

## Recommended upgrades

## Limits / failure risks

```

## Failure-mode output boundaries

When handling high-risk claim/support checks, use stable labels that keep source limits visible: Source basis, Claim/evidence fit, Method/evidence visible, What remains uncertain, and Next action. If the source cannot support the target claim, state Cannot support and name missing design elements such as No comparison design is visible. When only the packet supports a descriptive boundary, include: The packet can support a limited descriptive claim about what the notes say.

Compact output:

```markdown
# Source-use triage

Source basis: [one line]
How to use this result: TRIAGE ONLY - Use this only for provisional source-use triage; do not treat it as method or evidence verification when access is limited.

| Source | Method/evidence visible | Can support | Cannot support | Main risk | Use recommendation |

Next action: [one action]
```

Use the optional Suggested next step policy in `docs/policy/AUTO_SELECTION_GUARDRAILS.md`; it may be omitted unless a follow-on skill reduces a named scholarly risk.

## Quality checks

- Do not equate prestige with correctness.
- Do not equate citation count with truth.
- Do not use persuasive sources as neutral proof.
- Do not generalize from a single case without warning.
- Treat old sources carefully: they may be canonical but not current.
- Do not claim methodological quality is high unless method and evidence are visible enough to assess.
- Do not let strong individual-source quality imply corpus representativeness or field consensus.

## Failure modes

- Source verdict ignores what claim the source is meant to support.
- Audit overgeneralizes from source type without reading visible evidence.
- Contextual sources are treated as direct evidence.
- Missing method details are converted into false confidence.
- Premature citation audit before citations, quotes, page numbers, bibliography entries, or cited claims exist.
