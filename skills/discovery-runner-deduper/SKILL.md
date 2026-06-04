---
name: discovery-runner-deduper
description: Process academic index exports, library catalogue exports, bibliography exports, tabular files, or pasted candidate source records (for example, OpenAlex, Semantic Scholar, Elicit, scite, library catalogues, CSV, BIB, or RIS) into deduped screening records, duplicate clusters, and search-log updates.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# Discovery runner deduper

## Purpose

Operationalize a source discovery plan by processing exported or queried candidate results into deduped, screenable, search-log-ready records.

## When to use

Use when the user has a search plan or candidate source export from an academic index, library catalogue, bibliography manager, tabular file, or pasted record set (for example, OpenAlex, Semantic Scholar, Elicit, scite, library catalogues, CSV, BIB, or RIS) and needs deduping, screening, or search log updates.

## Automatic selection guidance

- High-signal triggers: dedupe source candidates, screen search results, process an academic index export, process a library catalogue export, process bibliography or tabular candidates (for example, OpenAlex, Semantic Scholar, Elicit, scite, CSV, BIB, or RIS), duplicate clusters, or update search log from completed searches.
- Light-route behavior: work from provided exports or pasted records first and distinguish planned searches from completed searches.
- Deep-work gate: network or API lookup requires explicit user permission, available tools, and a concrete metadata gap.
- Noise and slowdown guard: do not claim a database was searched unless the input proves it or the search was run and logged.

## Do not use this skill when

- The user needs a search plan but no candidate results; use `systematic-source-discovery`.
- The user needs source credibility audited; use `methodology-source-auditor`.
- The user needs annotations or source notes; use `annotated-bibliography-builder` or `annotation-to-source-note`.

## Inputs expected

- Search plan, completed query log, exported candidate list, bibliography export, tabular file, or pasted records (for example, CSV, BIB, or RIS).
- Venue, query, date, filters, candidate count, and source of each export when available.
- Inclusion and exclusion criteria.
- Screening fields or decisions already made.
- Permission status for network or API lookup if lookup is requested.

## Source basis and AI limits

Use `docs/policy/SOURCE_LIMITS.md` for source-access rules. Keep source access level, What I can verify, What remains uncertain, and User verification needed visible. Do not invent citations or source support.

Use `docs/policy/CORPUS_REPRESENTATIVENESS_TAXONOMY.md` when candidate exports, screening logs, or search-log updates could imply corpus coverage, balance, consensus, missing literature, or absence of evidence. Candidate records are not a representative corpus unless the logged venue, query, date, filter, and protocol basis justify that label.

For durable candidate matrices, duplicate clusters, screening logs, or search-log update drafts that are saved or handed to another skill, include a human-readable process passport following `docs/policy/PROCESS_PASSPORT.md`. Preserve upstream source-access, corpus-coverage, unresolved-risk, and handoff-limit labels; do not mark planned searches as completed.

## Files/folders it may read

- Shared operational boundary doc: `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`.
- Shared policy docs, especially `docs/policy/SOURCE_LIMITS.md`, `docs/policy/PROCESS_PASSPORT.md`, and `docs/policy/AUTO_SELECTION_GUARDRAILS.md`.
- User-provided search plans, search logs, candidate exports, bibliography exports, tabular files, source lists, and project files explicitly named in the request.

## Files/folders it may write

- None by default.
- May create or update user-requested candidate matrices, duplicate cluster tables, screening logs, or search-log drafts in the user-designated project or workspace.
- Must not add candidates to bibliography files, citation managers, or source databases as verified citations unless explicitly asked.

## What it must not do

- Do not claim planned searches were completed.
- Do not claim a venue was searched unless the input or actual logged search proves it.
- Do not add candidates to a bibliography as verified citations automatically.
- Do not invent DOI, title, author, year, abstract, hit count, or source metadata.

## Procedure

### 1. Declare search status

Separate planned searches, completed searches, candidate exports, and unknown-status records. Record venue, query, date, filters, candidate count, and export basis when available.

### 2. Normalize candidate fields

Extract title, authors, year, venue, DOI, URL, stable identifiers, abstract, source venue, query, and metadata confidence. Mark missing and uncertain fields.

### 3. Deduplicate records

Cluster by DOI or stable identifier first, then normalized title, then author-year-title similarity. Keep uncertainty visible for fuzzy matches.

When local JSON or CSV candidate exports are available, the optional deterministic helper can produce the first-pass duplicate screen:

```bash
python3 scripts/check_source_candidates.py --input path/to/source-candidates.json
```

Use the helper output as screening evidence only. It labels `exact_duplicate`, `probable_duplicate`, `possible_duplicate`, `related_but_distinct`, `insufficient_metadata`, and `human_review_required` cases, but it does not merge records, verify source truth, run searches, or add records to a bibliography. Preserve both records when the helper reports title-only similarity, author-year-title similarity, conflicting metadata, edition/version distinction, preprint/published distinction, translated or alternate-title caution, or missing metadata.

### 4. Screen candidates

Apply the supplied inclusion and exclusion criteria. Mark keep, reject, maybe, duplicate, or needs review. Never invent a reason if the record lacks enough data.

### 5. Draft search-log updates

Produce a search-log update that distinguishes completed search facts from candidate screening decisions and follow-up searches.

## Output format

```markdown
# Discovery runner dedupe report

## Source basis

## What I can verify

## What remains uncertain

## User verification needed

## Search status
| Venue | Query | Date | Filters | Candidate count | Status | Basis |

## Corpus representativeness label

## Candidate matrix
| Candidate ID | Title | Authors | Year | Venue | DOI / identifier | Source export | Metadata confidence | Screening decision | Reason |

## Duplicate clusters
| Cluster ID | Candidate IDs | Match basis | Confidence | Preferred record | Review needed |

## Keep / reject log
| Candidate ID | Decision | Reason | Criterion | Reviewer note |

## Search-log update draft

## Follow-up searches or metadata checks

## Process passport, if saved or handed downstream

## Limits / failure risks

```

Use the optional Suggested next step policy in `docs/policy/AUTO_SELECTION_GUARDRAILS.md`; it may be omitted unless a follow-on skill reduces a named scholarly risk.

## Quality checks

- Planned and completed searches are separate.
- Duplicate clusters show the match basis.
- Duplicate clusters preserve uncertain records and label human review needs.
- Metadata confidence is visible.
- Candidate records are not treated as verified bibliography entries.
- Corpus coverage labels reflect the logged search/export basis, not the number of candidates.
- Saved or downstream handoff outputs include a process passport and retain prior uncertainty labels.

## Failure modes

- Search plan language is mistaken for completed searches.
- Fuzzy duplicate matching hides uncertainty.
- Candidate metadata is silently completed from memory.
- Rejected sources lack a documented criterion.
- Premature citation audit before citations, quotes, page numbers, bibliography entries, or cited claims exist.
- A downstream search log loses source-access, corpus-coverage, unresolved-risk, or handoff-limit labels from earlier work.
