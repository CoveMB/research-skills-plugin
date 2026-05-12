---
name: systematic-source-discovery
description: Design rigorous research source-discovery strategies, keyword sets, database searches, citation-chaining plans, primary-source targets, and search logs for research books and literature reviews.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# Systematic Source Discovery

## Purpose

Create a repeatable source-discovery strategy for research nonfiction: search terms, databases, primary-source targets, citation chaining, inclusion/exclusion rules, and a search log.

## When to use

Use when the user needs to find high-quality sources, build a literature base, avoid cherry-picking, or document how sources were discovered.

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
4. Books from reputable academic or serious trade presses.
5. Institutional or organizational reports.
6. Reputable journalism for recent events or narrative context.
7. Persuasive or organizational material only with explicit perspective/context labeling.

## Source basis and AI limits

Before creating a search plan, state the source access level as one of:

- user-provided full text
- excerpt only
- citation only
- model knowledge only
- live/current search needed

Every output must separate source basis, what can be verified from available material, what remains uncertain, and what the user must verify. Do not invent citations, page numbers, quotations, DOIs, datasets, market facts, field consensus, source metadata, or claims of having searched a database. Separate verified facts, interpretation, speculation, and recommendation.

## Files/folders it may read

- This skill's `SKILL.md`, `README.md`, `assets/search-log-template.md`, `references/search-strategy-guide.md`, and `agents/openai.yaml`.
- User-provided research agendas, source lists, bibliographies, notes, and search logs explicitly named in the request.
- Project workflow docs when aligning source discovery with book artifacts.

## Files/folders it may write

- None by default.
- May create or update a user-requested search plan, query bank, or search log in the current project.
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

## Output format

```markdown
# Source Discovery Plan

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

## Limits / failure risks

## Next best skill
```

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
