# scholarly-prose-editor

## What it does

Use this skill to improve research nonfiction prose without flattening the author's voice. It edits for clarity, precision, structure, rhythm, readability, and tone while preserving nuance and avoiding generic language.

This skill is for prose that already has an argument to serve. It can clean up unclear sentences, reduce repetition, sharpen terms, improve transitions, and make difficult ideas easier to follow. It should not be used to make weak evidence sound stronger than it is.

## When to use it in the book writing process

Use it after the chapter logic and evidence are reasonably stable. It is useful for paragraphs, chapter sections, introductions, abstracts, proposals, and sample chapters.

Use it earlier only for targeted clarity work. If the draft has unsupported claims or structural problems, use `claim-evidence-ledger` or `chapter-architecture` first.

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

1. Establish source basis and source access level.
2. Use the skill's `SKILL.md` procedure, not memory-only shortcuts.
3. Produce the stated output format and separate verified facts, interpretation, speculation, and recommendation.
4. End with verification gaps and the next best skill or repair step.

## Quality checks

- Evidence strength must match claim strength.
- Missing source access must be marked, not hidden.
- Uncertainty, limits, and user verification needs must be visible.
- Output should preserve scholarly caution without becoming vague.

## Failure modes

- Fabricated citations, quotes, page numbers, source metadata, datasets, market facts, or field consensus.
- Confident synthesis from partial sources.
- Generic prose or structure that hides weak evidence.
- Overstated claims, missing counterarguments, or unclear source basis.

## Files/folders it may read

- This skill's `SKILL.md`, `README.md`, `assets/`, `references/`, and `agents/openai.yaml` when present and relevant.
- User-provided drafts, notes, sources, artifacts, or project files explicitly named in the request.
- Shared project documentation only when needed for workflow, quality, or artifact compatibility.

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

After this skill, use `citation-integrity-auditor` if the edited passage contains citations or quotations. Use `manuscript-continuity-editor` when several edited chapters need a whole-manuscript review.
