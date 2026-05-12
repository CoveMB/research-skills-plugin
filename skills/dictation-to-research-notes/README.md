# dictation-to-research-notes

## What it does

Use this skill to turn dictated research thoughts, voice transcripts, speech-to-text output, meeting notes, or rambling spoken fragments into structured scholarly notes.

It preserves meaning, separates claims from questions, flags transcript ambiguity, and produces evidence needs and next actions.

## When to use it

Use it when the input is spoken material rather than finished prose.

Use `reading-load-reducer` for dense source triage. Use `dyslexia-friendly-prose-editor` for existing prose. Use `dyslexia-research-companion` when dictation is only one part of a broader accessibility bottleneck.

## Good inputs

- Dictated text, transcript, voice-note dump, meeting note, or spoken fragment list.
- Intended use: idea capture, chapter planning, claim drafting, source planning, or next-step triage.
- Speaker labels, meeting context, interview/privacy constraints, terms that must stay unchanged, and any relevant chapter or project context.

## Example requests

```text
Use dictation-to-research-notes. Turn this voice transcript into claims, questions, evidence needs, and next actions.
```

```text
Use dictation-to-research-notes. Clean this dictated chapter idea into research notes without changing my meaning.
```

```text
Use dictation-to-research-notes. Segment these rambling notes into idea units and flag ambiguous transcript errors.
```

## Typical output

Expect a cleaned note table with speaker/source or original-fragment anchors when useful, ambiguity table, source basis, verification gaps, and one optional risk-gated next step.

## Procedure

Follow the shared procedure in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.

## Quality checks

Apply the shared quality checks in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`; keep transcript ambiguity and meaning-preservation checks visible in the output.

## Failure modes

Use the shared failure modes in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`; call out transcript overcorrection, false confidence, or hidden evidence gaps when relevant.

## Files/folders it may read

Follow the shared read boundary in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.

## Files/folders it may write

Follow the shared write boundary in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.

## What it must not do

Follow the shared prohibitions in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.

## Best next steps

After this skill, use `scholarly-research-agenda` for unstable questions, `argument-architecture` for claim structure, `chapter-architecture` for chapter planning, `claim-evidence-ledger` for evidence risk, `rights-privacy-release-auditor` before sharing identifiable interview or meeting material, or `dyslexia-friendly-prose-editor` once the idea structure is stable.
