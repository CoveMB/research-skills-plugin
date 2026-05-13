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

## Source basis and AI limits

Follow `docs/SOURCE_LIMITS.md`: state the source access level, separate source basis from interpretation, include What I can verify, What remains uncertain, and User verification needed. Do not invent citations or source support.

## Machine-readable artifacts

When the user explicitly asks for JSON or a contract artifact, use `shared/contracts/book/book_artifact.schema.json` with `artifact_type: source_discovery_log`. If the output is normal Markdown, do not force the JSON contract.

## Systematic review mode

Use systematic review mode only when the user requests a systematic review, scoping review, evidence review, PRISMA-style search record, reproducible database search, or protocol-grade literature discovery. Do not impose it on ordinary book research.

When active, add:

- protocol snapshot: review question, scope, databases, dates, filters, inclusion/exclusion rules, and reviewer assumptions
- exact search strings by venue, with date searched and filter settings
- screening counts: records found, records deduped, records screened, included, excluded, and full-text unavailable
- exclusion reasons tied to criteria, not vague judgment
- PRISMA flow fields where the user needs reporting-grade documentation

For compact guidance and query design reminders, read `references/search-strategy-guide.md`.

## Files/folders it may read

- Bundled skill instructions, metadata, and assets if available (including, but not limited to, `SKILL.md`, `README.md`, `assets/`, `references/`, and `agents/openai.yaml` in this project or equivalent files in another project).
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

## Procedure

### 0. Declare search status

State whether the output is a search plan, a completed search log, or a mixed plan-plus-log. Never imply that a database, catalogue, website, or repository has been searched unless the search was actually performed and logged.

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

### 2. Create Boolean search strings

For each search family, generate combinations using AND, OR, quotes, and exclusions. Include both broad and narrow searches.

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

### 5. Plan citation chaining

For foundational sources:

- backward chaining: inspect references cited by the source
- forward chaining: inspect works citing the source
- lateral chaining: inspect authors, coauthors, conferences, journals, and debates

### 6. Create a search log

Record every search query, venue, date, filters, number of useful hits, and notes.

### 7. Add protocol-grade fields when requested

If systematic review mode is active, include the protocol snapshot, screening counts, and exclusion reasons. Keep planned searches separate from completed searches.

## Output format

```markdown
# Source discovery plan

## Search status

## Source basis

## What I can verify

## What remains uncertain

## User verification needed

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

## Protocol snapshot

## Screening counts
| Stage | Count | Basis |

## Exclusion reasons
| Record or cluster | Exclusion criterion | Reason | Reviewer note |

## Limits / failure risks

## Suggested next step

```

Use the optional Suggested next step policy in `docs/AUTO_SELECTION_GUARDRAILS.md`; it may be omitted unless one skill reduces a named scholarly risk.

## Quality checks

- Include opposing terms as well as terms that support the user's thesis.
- Include primary-source targets where appropriate.
- Distinguish places to search from sources already verified.
- Avoid overreliance on search-engine snippets.
- Mark any live-search requirement clearly when current information is needed.
- Mark unsearched venues as planned venues, not evidence.

## Failure modes

- Query bank mirrors only the user's preferred thesis.
- Search log mixes completed searches with planned searches.
- Source list overweights convenient web results.
- Inclusion criteria are too vague to prevent cherry-picking.
- Premature citation audit before citations, quotes, page numbers, bibliography entries, or cited claims exist.
