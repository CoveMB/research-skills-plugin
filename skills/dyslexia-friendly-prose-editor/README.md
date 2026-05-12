# dyslexia-friendly-prose-editor

## What it does

Use this skill to repair spelling, grammar, sentence boundaries, punctuation, and readability in existing scholarly prose while preserving meaning and authorial voice.

It is accessibility-focused: it fixes text friction without turning the passage into generic prose or hiding evidence gaps.

## When to use it

Use it for existing paragraphs, abstracts, proposal passages, or chapter excerpts when spelling, orthography, grammar, sentence boundaries, or typo-heavy prose are the main bottleneck.

Use `dictation-to-research-notes` for spoken notes. Use `reading-load-reducer` for dense source triage. Use `scholarly-prose-editor` for broader style, rhythm, or public-facing edits after evidence and structure are stable.

## Good inputs

- Existing prose passage, abstract, proposal section, chapter excerpt, or draft paragraph.
- Desired repair level: minimal correction, local sentence repair, paragraph repair, or issue-list cleanup.
- Terms, names, quotes, technical phrases, and claims that must not change.

## Example requests

```text
Use dyslexia-friendly-prose-editor. Fix spelling and sentence boundaries without changing my argument.
```

```text
Use dyslexia-friendly-prose-editor. Clean this abstract for grammar and readability, but keep uncertainty and evidence limits.
```

```text
Use dyslexia-friendly-prose-editor. Repair this typo-heavy paragraph and list any corrections that might change meaning.
```

## Typical output

Expect a revised passage, meaning-preserved note, new-claims check, changed-phrase review when useful, ambiguous corrections table, evidence flags, and one optional risk-gated next step.

## Procedure

Follow the shared procedure in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.

## Quality checks

Apply the shared quality checks in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`; keep meaning preservation, ambiguous corrections, and evidence limits visible in the output.

## Failure modes

Use the shared failure modes in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`; call out overcorrection, lost uncertainty, or generic style drift when relevant.

## Files/folders it may read

Follow the shared read boundary in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.

## Files/folders it may write

Follow the shared write boundary in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.

## What it must not do

Follow the shared prohibitions in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.

## Best next steps

After this skill, use `claim-evidence-ledger` if cleaner prose exposes unsupported claims, `citation-integrity-auditor` if quotes or citations need verification, or `scholarly-prose-editor` for broader style work after evidence is stable.
