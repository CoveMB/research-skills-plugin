# citation-integrity-auditor

## What it does

Use this skill to protect a research draft from citation problems. It checks whether claims have support, whether citations match the claim they are meant to support, whether quotes need exact verification, whether page numbers are missing, and whether bibliography details look incomplete.

It does not pretend to verify sources it cannot see. If source text is unavailable, it marks verification as unavailable and states what would be needed.

For public metadata exports, the optional local helper `python3 scripts/check_citation_metadata.py --input path/to/public-metadata.json` can check identifier format, normalized metadata consistency, missing source-access labels, page-range warnings, locator-support gaps, duplicate citation keys, DOI/title conflicts, and title/metadata conflicts without network lookup. Do not pass manuscript text, excerpts, abstracts, or private notes to that helper.

The helper validates internal metadata consistency only. It does not prove that a source exists, that a DOI is real, or that a source supports a claim unless an allowed lookup or source-content verification path has been completed and recorded.

## When to use it

Use it after a draft has citations, footnotes, bibliography entries, paraphrases, or quoted material. It is most useful after the claim-evidence ledger, because the ledger identifies what needs support and the citation audit checks whether the support is actually there.

Use it before submitting a proposal, chapter, article, sample chapter, or full manuscript.

## Good inputs

- Draft text with citations, footnotes, or bibliography.
- Source excerpts, PDFs, page images, or notes when available.
- Bibliography entries.
- A list of claims the author is worried about.
- Style requirements, if citation formatting also needs review.

## Example requests

```text
Audit this chapter for unsupported claims, citation-source mismatch, and missing page numbers.
```

```text
Check whether these quotes have enough locator information and whether the surrounding claims overstate the source.
```

```text
Review this bibliography and flag missing details, possible fabricated references, and weak source types.
```

## Typical output

Expect a citation integrity audit with summary verdict, claim-level audit, quotation audit, bibliography issues, high-priority repairs, claims safe as interpretation or argument, severity labels, and a risk-gated follow-up when it is useful. Ask for compact output when you want critical and major citation blockers first, with source access limits still visible. Compact output should include `How to use this result: BLOCKER SUMMARY - This lists visible citation blockers only; no blocker listed does not mean citation clearance.` It changes output shape, not route selection or evidence requirements.

## Procedure

Follow the shared procedure in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.

## Quality checks

Apply the shared quality checks in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`; keep any skill-specific caveats visible in the output.

## Failure modes

Use the shared failure modes in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`; call out the skill-specific failure most relevant to the request.

## Files/folders it may read

Follow the shared read boundary in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.

## Files/folders it may write

Follow the shared write boundary in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.

## What it must not do

Follow the shared prohibitions in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.

## Best next steps

After this skill, repair citations and source wording. Then use `scholarly-prose-editor` for prose cleanup or `manuscript-continuity-editor` for a whole-manuscript pass.
