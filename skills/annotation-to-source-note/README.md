# annotation-to-source-note

## What it does

Use this skill to turn annotations, document highlights, reference-manager notes, excerpts, or rough reading notes (for example, PDF highlights or Zotero notes) into source-bound notes. It keeps the evidence trail visible, especially the line between summary, paraphrase, quote, and interpretation.

It is useful when notes are good enough to keep but too messy to trust in a chapter draft.

## When to use it

Use it after reading or annotation export and before claim drafting, extraction tables, or citation audit.

Use it when missing pages, missing citekeys, or unclear quote boundaries would make later writing risky.

## Good inputs

- Reference-manager notes, document highlights, excerpts, manual annotations, or reading notes (for example, Zotero notes or PDF highlights).
- Source metadata and citekey if available.
- Project question, intended chapter, or intended claim use.
- Page, timestamp, archive locator, section, or paragraph data when available.

## Example requests

```text
Turn these document highlights into source notes with quote, paraphrase, and locator gaps marked.
```

```text
Convert my reference-manager notes into source-bound notes for chapter 2.
```

```text
Clean these reading notes, but flag every missing page number and uncertain quotation.
```

## Typical output

Expect a source note with metadata status, source basis, classified note units, quote and locator gaps, project use, interpretation limits, and follow-up tasks.

## Procedure

Follow the shared procedure in `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`.

## Quality checks

Apply the shared quality checks in `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`; keep any skill-specific caveats visible in the output.

## Failure modes

Use the shared failure modes in `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`; call out the skill-specific failure most relevant to the request.

## Files/folders it may read

Follow the shared read boundary in `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`.
Template: `assets/source-note-template.md`.

## Files/folders it may write

Follow the shared write boundary in `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`.

## What it must not do

Follow the shared prohibitions in `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`.

## Best next steps

After this skill, use `extraction-table-builder` when several source notes need comparison. Use `claim-evidence-ledger` when the draft claims are ready to audit.
