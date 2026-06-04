---
name: systematic-source-discovery
description: Design source-discovery strategies when research books or literature reviews need source plans, keyword banks, database searches, inclusion rules, citation chaining, primary-source targets, candidate sources, or search logs.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# Systematic source discovery

## Purpose

Create a repeatable source-discovery strategy for research nonfiction: search terms, databases, primary-source targets, citation chaining, inclusion/exclusion rules, and a search log.

## When to use

Use when the user needs to find credible sources, build a literature base, avoid cherry-picking, or document how sources were discovered.

## Automatic selection guidance

- High-signal triggers: find sources, search strategy, source plan, keyword bank, database search, inclusion criteria, citation chaining, primary-source targets, or search log.
- Light-route behavior: create search families, query banks, venues, and inclusion/exclusion rules before collecting candidates.
- Deep-work gate: browse or collect candidate sources only when the user asks for actual sources, source existence matters now, or router deep mode routes here.
- Noise and slowdown guard: do not launch broad live search for a vague topic before agenda and scope are stable.

## Do not use this skill when

- The user needs the topic made researchable first; use `scholarly-research-agenda`.
- The user already has exported or queried candidate results that need dedupe or screening; use `discovery-runner-deduper`.
- The user already has sources and needs field structure; use `literature-review-mapper`.
- The user asks whether a specific source is credible; use `methodology-source-auditor`.

## Inputs expected

- Book topic, research question, thesis, scope boundaries, field, and audience when available.
- Known seed sources, authors, cases, search terms, databases, or excluded areas.
- Time period, geography, source languages, and source types that matter.
- Whether live/current searching is available or the task is only to design a search plan.

## Source hierarchy

Prefer a balanced mix of:

1. Primary or source materials: original documents, records, reports, data, interviews, field notes, or working papers when they are objects of study.
2. Peer-reviewed journal articles and academic books.
3. Review articles and handbooks.
4. Books from reputable academic or trade presses.
5. Institutional or organizational reports.
6. Reputable journalism for recent events or narrative context.
7. Persuasive or organizational material only with explicit perspective/context labeling.

Do not let the hierarchy become a corpus-bias shortcut. Track languages, databases, open-access constraints, geography, discipline boundaries, famous-author anchoring, grey literature, and opposing-view search families when they could change discovery results.

## Source basis and AI limits

Use `docs/SOURCE_LIMITS.md` for source-access rules. Keep source access level, What I can verify, What remains uncertain, and User verification needed visible. Do not invent citations or source support.

Use `docs/CORPUS_REPRESENTATIVENESS_TAXONOMY.md` when the output could imply coverage, balance, consensus, novelty, missing literature, or absence of counter-literature.

## Machine-readable artifacts

When the user explicitly asks for JSON or a contract artifact, use `shared/contracts/book/book_artifact.schema.json` with `artifact_type: source_discovery_log`. If the output is normal Markdown, do not force the JSON contract. For durable handoff artifacts, follow `docs/PROCESS_PASSPORT.md`: set `handoff_artifact: true`, include `process_passport`, and preserve upstream passport limits instead of upgrading verification.

## Systematic review mode

Use systematic review mode only when the user requests a systematic review, scoping review, evidence review, PRISMA-style search record, reproducible database search, or protocol-grade literature discovery. Do not impose it on ordinary book research.

Apply a review-type prefilter before adding reporting-grade structure:

- systematic review: requires a narrow question, reproducible search, reviewer process, screening, appraisal plan, risk of bias or quality appraisal, synthesis method, and certainty or confidence limits where the field expects them
- scoping review: requires transparent search, charting fields, screening process, and map-of-evidence limits; do not claim effect estimates or settled certainty
- rapid review: requires abbreviated-search limits, reviewer process, omitted steps, and time-boxed caveats
- narrative review: may use transparent source selection and coverage limits, but must not present itself as systematic or PRISMA-complete
- critical review: may prioritize argument and theoretical synthesis, but must label selection rationale and field-coverage limits

When active, add:

- review type and reason for using that review type
- protocol snapshot: review question, scope, databases, dates, filters, inclusion/exclusion rules, and reviewer assumptions
- reviewer process: number of reviewers, screening stages, conflict resolution, and any single-reviewer limitations
- appraisal plan: method or quality appraisal approach, risk of bias fields where relevant, and when appraisal is not applicable
- synthesis method: narrative synthesis, thematic synthesis, vote counting, meta-analysis, evidence map, or other method with limits
- certainty or confidence assessment: GRADE, CERQual, field-specific confidence language, or explicit note that certainty assessment is not being performed
- exact search strings by venue, with date searched and filter settings
- screening counts: records found, records deduped, records screened, included, excluded, and full-text unavailable
- exclusion reasons tied to criteria, not vague judgment
- PRISMA flow fields where the user needs reporting-grade documentation

For concise guidance and query design reminders, read `references/search-strategy-guide.md`.

## Files/folders it may read

- Shared operational boundary doc: `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.
- Shared policy docs, especially `docs/SOURCE_LIMITS.md` and `docs/AUTO_SELECTION_GUARDRAILS.md`.
- User-provided research agendas, source lists, bibliographies, notes, and search logs explicitly named in the request.
- Project workflow docs when aligning source discovery with book artifacts.

## Files/folders it may write

- None by default.
- May create or update a user-requested search plan, query bank, or search log in the user-designated project or workspace.
- Must not alter source databases, bibliography managers, or repository files without explicit permission.

## What it must not do

- Do not claim a venue was searched unless it was actually searched and logged.
- Do not treat planned sources as verified sources.
- Do not invent search results, hit counts, bibliographic metadata, or source availability.
- Do not present a one-database, English-only, open-access, famous-author, or Global North search as representative unless that limit is intentional and labeled.
- Do not treat retraction, correction, predatory, or questionable-source status as checked unless the check was actually performed or supplied.

## Procedure

### 0. Declare search status

State whether the output is `planned_search`, `partial_search`, `completed_search_log`, `completed_protocol`, or a mixed plan-plus-log. Never imply that a database, catalogue, website, or repository has been searched unless the search was actually performed and logged.

Assign a corpus-representativeness label from `docs/CORPUS_REPRESENTATIVENESS_TAXONOMY.md` when the output includes completed or proposed corpus claims. Use `unknown_coverage` for `planned_search`, `partial_corpus` or a narrower skew label for `partial_search`, and `systematic_protocol` or `scoping_protocol` only for an executed protocol with visible search, screening, appraisal or charting, and limits. A planned search is not evidence of field coverage.

### 1. Translate the topic into search families

Create search families:

- core concept terms
- synonyms and adjacent terms
- context terms
- field terms
- methods terms
- opposing-view terms
- case-study terms
- author/theorist names
- contrary or disconfirming terms that could surface rival explanations, failed replications, corrections, retractions, or critiques

### 2. Create Boolean search strings

For each search family, generate combinations using AND, OR, quotes, and exclusions. Include both broad and narrow searches.

For currentness-sensitive topics, add date-window rules and a current lookup checkpoint. For historical or archival topics, explain why currentness is less central and which source-status checks still matter.

### 3. Identify search venues

Suggest venues such as:

- library catalogues
- Google Scholar
- Semantic Scholar
- JSTOR
- Project MUSE
- subject databases selected for the project
- preprint or working-paper indexes where relevant
- institutional repositories
- reference lists in canonical books

Do not claim that a database has been searched unless it actually has.

### 4. Build inclusion/exclusion rules

Define what counts as relevant and what will be excluded. Include quality and date rules.

Include source-status rules when relevant: how to handle retracted, corrected, predatory, questionable, duplicate, low-credibility, or non-scholarly sources without erasing them as possible objects of analysis.

### 5. Plan citation chaining

For foundational sources:

- backward chaining: inspect references cited by the source
- forward chaining: inspect works citing the source
- lateral chaining: inspect authors, coauthors, conferences, journals, and debates

### 6. Create a search log

Record every search query, venue, date, filters, number of useful hits, and notes.

### 7. Add protocol-grade fields when requested

If systematic review mode is active, include the review type, protocol snapshot, reviewer process, appraisal plan, synthesis method, certainty assessment, screening counts, and exclusion reasons. Keep planned searches separate from completed searches.

## Output format

```markdown
# Source discovery plan

## Search status

## Source basis

## What I can verify

## What remains uncertain

## User verification needed

## Corpus representativeness label

## Claim limit

## Counter-literature check

## Search families

## Boolean query bank
| Purpose | Query | Venue | Notes |

## Priority venues

## Inclusion criteria

## Exclusion criteria

## Citation-chaining plan

## Primary-source targets

## Opposing-literature targets

## Search log template
| Date | Venue | Query | Filters | Useful results | Notes |

## Systematic review mode fields, if requested

## Review type

## Protocol snapshot

## Reviewer process

## Appraisal plan

## Synthesis method

## Certainty / confidence assessment

## Screening counts
| Stage | Count | Basis |

## Exclusion reasons
| Record or cluster | Exclusion criterion | Reason | Reviewer note |

## Limits / failure risks

```

Use the optional Suggested next step policy in `docs/AUTO_SELECTION_GUARDRAILS.md`; it may be omitted unless a follow-on skill reduces a named scholarly risk.

## Quality checks

- Include opposing terms as well as terms that support the user's thesis.
- Include primary-source targets where appropriate.
- Distinguish places to search from sources already verified.
- Avoid overreliance on search-engine snippets.
- Mark any live-search requirement clearly when current information is needed.
- Mark unsearched venues as planned venues, not evidence.
- Do not use PRISMA-style labels to imply completed screening, appraisal, risk of bias review, synthesis, or certainty assessment.
- Do not label a search `field_balanced_corpus`, `systematic_protocol`, or `scoping_protocol` unless the visible search status and protocol details justify that label.

## Failure modes

- Query bank mirrors only the user's preferred thesis.
- Search log mixes completed searches with planned searches.
- Source list overweights convenient web results.
- Inclusion criteria are too vague to prevent cherry-picking.
- Systematic, scoping, narrative, rapid, and critical review types are collapsed into one template.
- Appraisal plan, reviewer process, synthesis method, risk of bias, or certainty limits are missing while the output appears reporting-grade.
- Premature citation audit before citations, quotes, page numbers, bibliography entries, or cited claims exist.
