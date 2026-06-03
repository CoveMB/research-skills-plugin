# Citation integrity audit
Selected skill: citation-integrity-auditor.

## Source basis

The bibliography entries contain DOI-bearing public citation metadata. No source text, draft prose, notes, abstracts, or manuscript excerpts are available or needed for this metadata-only check.

## What I can verify

The local checker can compare supplied public fields for DOI, title, author-year, and venue. Default mode remains no-network.

## What remains uncertain

Source identity, source-claim fit, quotation accuracy, page locators, and manuscript support remain unchecked unless source text or authoritative metadata is provided.

## User verification needed

Use public metadata lookup only with explicit consent:

```bash
python3 scripts/check_citation_metadata.py --input path/to/public-metadata.json --lookup-provider crossref --allow-network
```

This path submits DOI identifiers only. Keep private fields such as `full_text`, `excerpt`, `abstract`, `notes`, `private_notes`, `source_text`, and manuscript excerpts out of the input file.

## Metadata verification ladder results

| Reference | DOI / identifier | Title match | Author-year match | Venue match | Status | Repair task |
| --- | --- | --- | --- | --- | --- | --- |
| DOI-bearing entries | unchecked until the consent-gated public metadata lookup or user-provided authoritative metadata is available | unchecked | unchecked | unchecked | verification unavailable | Run the local no-network comparison, or run the consent-gated public metadata lookup if approved. |

## Limits / failure risks

Public metadata lookup checks bibliographic identity only. It does not verify quotation accuracy, source-claim fit, page locators, or whether the cited source supports the manuscript claim.
