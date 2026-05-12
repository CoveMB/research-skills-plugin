# citation-integrity-auditor

## What it does

Use this skill to protect a research draft from citation problems. It checks whether claims have support, whether citations match the claim they are meant to support, whether quotes need exact verification, whether page numbers are missing, and whether bibliography details look incomplete.

It does not pretend to verify sources it cannot see. If source text is unavailable, it marks verification as unavailable and states what would be needed.

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

Expect a citation integrity audit with summary verdict, claim-level audit, quotation audit, bibliography issues, high-priority repairs, claims safe as interpretation or argument, severity labels, and a risk-gated follow-up when it is useful.

## Procedure

1. State the source basis and source access level.
2. Follow the skill's `SKILL.md` procedure instead of working from memory.
3. Produce the stated output format and keep verified facts, interpretation, speculation, and recommendation separate.
4. End with verification gaps. Add a risk-gated follow-up only when it is useful.

## Quality checks

- Evidence strength must match claim strength.
- Missing source access must be marked clearly.
- Uncertainty, limits, and user verification needs must be visible.
- Output should preserve scholarly caution without becoming vague.

## Failure modes

- Fabricated citations, quotes, page numbers, source metadata, datasets, market facts, or field consensus.
- Confident synthesis from partial sources.
- Generic prose or structure that hides weak evidence or weak reasoning.
- Overstated claims, missing counterarguments, or unclear source basis.

## Files/folders it may read

- This skill's `SKILL.md`, `README.md`, `assets/`, `references/`, and `agents/openai.yaml` when present and relevant.
- User-provided drafts, notes, sources, artifacts, or project files explicitly named in the request.
- Shared project documentation when it is needed for workflow, quality, or artifact compatibility.

## Files/folders it may write

- None by default.
- May create or update user-requested research artifacts, notes, drafts, or review files in the current project.
- Must not overwrite source material, bibliography databases, manuscript files, or plugin files without explicit user request.

## What it must not do

- Invent missing scholarly facts or verification.
- Treat unavailable evidence as confirmed.
- Use style polish to mask weak argument, weak sources, or unsupported claims.
- Claim external searches, source checks, or database access that did not happen.

## Best next steps

After this skill, repair citations and source wording. Then use `scholarly-prose-editor` for prose cleanup or `manuscript-continuity-editor` for a whole-manuscript pass.
