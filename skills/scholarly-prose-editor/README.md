# scholarly-prose-editor

## What it does

Use this skill to improve research nonfiction prose without flattening the author's voice. It edits for clarity, precision, structure, rhythm, readability, and tone while preserving nuance and avoiding generic language.

Use it for prose that already has an argument to serve. It can clean up unclear sentences, reduce repetition, sharpen terms, improve transitions, and make difficult ideas easier to follow. It should not make weak evidence sound stronger than it is.

## When to use it

Use it after the chapter logic and evidence are reasonably stable. It is useful for paragraphs, chapter sections, introductions, abstracts, proposals, and sample chapters.

Use it earlier only for targeted clarity work. If the draft has unsupported claims or structural problems, use `claim-evidence-ledger` or `chapter-architecture` first.

If the input is rough notes, dictation, typo-heavy fragments, dense material, or accessibility-focused surface repair before prose editing, use the smallest accessibility entry point in `docs/policy/ROUTING_MATRIX.md` first.

## Good inputs

- A paragraph, section, chapter excerpt, introduction, abstract, or proposal passage.
- Desired editing mode, such as clarity, research, public-facing, compression, expansion, or style-preserving.
- Notes on audience and tone.
- Any claims the author wants preserved carefully.

## Example requests

```text
Edit this passage for clarity and rhythm without changing the argument.
```

```text
Make this chapter introduction more readable for educated general readers while keeping the research nuance.
```

```text
Compress this section by 25 percent and flag any claims that still need evidence.
```

## Typical output

Expect a revised passage, notes on what changed, confirmation of meaning preserved, claims needing evidence, and optional stronger alternatives.

## Procedure

Follow the shared procedure in `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`.

## Quality checks

Apply the shared quality checks in `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`; keep any skill-specific caveats visible in the output.

## Failure modes

Use the shared failure modes in `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`; call out the skill-specific failure most relevant to the request.

## Files/folders it may read

Follow the shared read boundary in `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`.
Template: `assets/style-sheet-template.md`.

## Files/folders it may write

Follow the shared write boundary in `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`.

## What it must not do

Follow the shared prohibitions in `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`.

## Best next steps

After this skill, use `citation-integrity-auditor` if the edited passage contains citations or quotations. Use `manuscript-continuity-editor` when several edited chapters need a whole-manuscript review.
