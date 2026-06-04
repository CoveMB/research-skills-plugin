# Citation integrity audit

## Source basis

Allowed material only: `public-metadata-only-citation-check` prompt and `citation-integrity-auditor` skill instructions.

Source access level: public metadata only. No browsing, external lookup, draft text, source full text, abstracts, notes, or private material inspected.

## What I can verify

The allowed source packet states that only DOI-like public identifiers from a bibliography list are in scope.

No actual DOI strings, bibliography rows, titles, authors, years, venues, or draft claims are visible in the allowed material.

Because no DOI-bearing records are present in the allowed material, individual bibliography metadata cannot be checked.

## What remains uncertain

All reference-level metadata remains unchecked:

- DOI existence
- DOI-to-title match
- author-year match
- venue match
- identifier hijack risk
- duplicate or reused citation keys
- retraction, correction, expression-of-concern, questionable-venue, predatory-venue, or paper-mill status

Source-claim support is also not checked because no draft text or source content was inspected.

## User verification needed

Provide the public bibliography metadata rows or DOI list if a metadata-only audit should be completed. For each reference, the minimum useful fields are DOI, title, authors, year, and venue.

External DOI lookup would require explicit permission and was not performed.

## Summary verdict

Verification unavailable for individual DOI-bearing bibliography entries. The audit cannot confirm or reject any specific reference because the allowed material does not include the identifiers or metadata rows to inspect.

## Claim-level audit

| Claim | Current citation | Verification status | Issue type | Severity | What is needed | Suggested fix |
|---|---|---|---|---|---|---|
| Not inspected | Not inspected | verification unavailable | unsupported claim status unchecked | N/A | Draft text and source content would be needed for claim-level support checks | Not applicable to this public-metadata-only run |

## Quotation audit

No draft text or source text was inspected. Quote exactness, page numbers, and locators are verification unavailable.

## Bibliography issues

No specific bibliography issues can be confirmed from the allowed material. The absence of visible DOI records is the blocking limitation.

## Metadata verification ladder results

| Reference | DOI / identifier | Title match | Author-year match | Venue match | Status | Repair task |
|---|---|---|---|---|---|---|
| No visible reference rows | No visible DOI strings | unchecked | unchecked | unchecked | verification unavailable | Provide public bibliography metadata or DOI list |

## High-priority repairs

Provide the DOI-bearing bibliography list before scoring metadata integrity.

Do not treat this run as citation clearance. No source existence or metadata correctness was established.

## Claims safe as interpretation or argument

Not assessed. No draft text was inspected.

## Limits / failure risks

A DOI-like string alone would not verify source-claim support, quotation accuracy, paraphrase faithfulness, or locator accuracy.

No external public metadata lookup was performed.

No reference should be marked as verified, clean, or bibliographically sound based on this run.