# Discovery runner dedupe report

## Source basis

Controlled synthetic packet only. The packet states that this is not a real search export.

## What I can verify

- Row 1 and Row 2 share the same DOI.
- Row 3 has a similar title but no DOI.
- Database A is listed as completed.
- Database B is listed as planned, not run.

## What remains uncertain

- Exact titles, authors, years, venues, DOI value, URLs, abstracts, and query details are not provided.
- Whether Row 3 is the same work as Row 1 / Row 2 cannot be determined from the visible packet alone.
- No metadata correction authority file is available.

## User verification needed

- Confirm which of Row 1 or Row 2 should be the preferred retained record.
- Human-review Row 3 against Row 1 / Row 2 using full title, authors, year, venue, DOI, abstract, and source metadata.
- Do not mark Database B as completed unless it is actually searched and logged.

## Search status

| Venue | Query | Date | Filters | Candidate count | Status | Basis |
|---|---|---:|---|---:|---|---|
| Database A | Unknown | Unknown | Unknown | 3 visible rows | Completed export | Packet states Database A is completed and provides Rows 1-3 |
| Database B | Unknown | Unknown | Unknown | Unknown | Planned, not completed | Packet states Database B is planned |

## Corpus representativeness label

Limited candidate export only. This packet does not justify claims of representative corpus coverage, literature balance, consensus, or absence of evidence.

## Candidate matrix

| Candidate ID | Title | Authors | Year | Venue | DOI / identifier | Source export | Metadata confidence | Screening decision | Reason |
|---|---|---|---:|---|---|---|---|---|---|
| Row 1 | Not provided | Not provided | Unknown | Not provided | Shared DOI with Row 2; value not provided | Database A | Low | Duplicate group member | Exact DOI match with Row 2 |
| Row 2 | Not provided | Not provided | Unknown | Not provided | Shared DOI with Row 1; value not provided | Database A | Low | Duplicate group member | Exact DOI match with Row 1 |
| Row 3 | Similar to Row 1 / Row 2; exact title not provided | Not provided | Unknown | Not provided | No DOI provided | Database A | Low | Needs review | Similar title but insufficient metadata to merge |

## Duplicate clusters

| Cluster ID | Candidate IDs | Match basis | Confidence | Preferred record | Review needed |
|---|---|---|---|---|---|
| D1 | Row 1, Row 2 | Same DOI | High for duplicate relationship; low for preferred-record choice | Undetermined from visible packet | Yes, choose the most complete / accurate row |
| D2 | Row 3 with Row 1 / Row 2 | Similar title; Row 3 lacks DOI | Low to moderate | None; preserve Row 3 separately | Yes, human review required |

## Keep / reject log

| Candidate ID | Decision | Reason | Criterion | Reviewer note |
|---|---|---|---|---|
| Row 1 | Maybe keep as preferred duplicate record | Exact DOI duplicate with Row 2, but completeness unknown | Duplicate handling | Compare Row 1 and Row 2 metadata before retaining one |
| Row 2 | Maybe reject as duplicate after preferred record chosen | Exact DOI duplicate with Row 1 | Duplicate handling | Do not discard until preferred row is selected |
| Row 3 | Needs review | Similar title but no DOI and no supporting metadata | Insufficient metadata / fuzzy duplicate | Preserve until title-author-year-venue comparison is available |

## Search-log update draft

Database A was completed and produced three visible candidate rows in this packet. Rows 1 and 2 are exact DOI duplicates. Row 3 is a possible fuzzy duplicate because it has a similar title but lacks DOI metadata. Database B remains a planned search and should not be counted as completed or included in completed-search totals.

## Follow-up searches or metadata checks

- Retrieve or inspect full metadata for Rows 1-3.
- Compare Row 3 against the DOI-matched record using title, authors, year, venue, abstract, and stable identifiers.
- Run Database B only if it remains part of the discovery plan, then log query, date, filters, hit count, and export basis.

## Process passport, if saved or handed downstream

- Source access level: controlled-packet.
- Input basis: synthetic visible packet only.
- Completed search basis: Database A listed as completed.
- Planned search basis: Database B listed as planned, not run.
- Corpus coverage label: limited candidate export only.
- Unresolved risks: missing authority file, missing full metadata, unresolved fuzzy duplicate decision.
- Handoff limit: candidate records are not verified bibliography entries.

## Limits / failure risks

- Row 3 could be the same work, a related work, a different edition/version, or a distinct source with a similar title.
- Choosing a preferred record between Row 1 and Row 2 is not possible from the visible packet.
- Treating Database B as completed would create search-log drift.