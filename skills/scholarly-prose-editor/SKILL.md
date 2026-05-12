---
name: scholarly-prose-editor
description: Edit research nonfiction prose for clarity, precision, structure, rhythm, readability, and authorial voice while preserving nuance and avoiding generic AI style.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# Research Prose Editor

## Purpose

Improve serious nonfiction prose without flattening the author's voice or over-polishing into generic language.

## When to use

Use when the user provides a paragraph, section, chapter excerpt, proposal, abstract, or introduction that needs clearer research prose.

## Inputs expected

- Passage, chapter excerpt, proposal section, abstract, introduction, or style sample.
- Desired edit mode, audience, length target, and terms or claims that must be preserved.
- Source basis for factual claims if evidence issues should be flagged.
- Any style constraints from press, journal, advisor, or authorial voice.

## Editing priorities

1. Preserve meaning and intellectual nuance.
2. Improve clarity and sentence flow.
3. Reduce repetition and throat-clearing.
4. Strengthen transitions.
5. Replace inflated language with precise language.
6. Keep uncertainty where uncertainty is intellectually honest.
7. Avoid adding new factual claims.

## Source basis and AI limits

Before editing, state the source access level as one of:

- user-provided full text
- excerpt only
- citation only
- model knowledge only
- live/current search needed

Every output must separate source basis, what can be verified from available material, what remains uncertain, and what the user must verify. Do not invent citations, page numbers, quotations, DOIs, datasets, market facts, field consensus, source metadata, or claims of having searched a database. Separate verified facts, interpretation, speculation, and recommendation.

## Files/folders it may read

- This skill's `SKILL.md`, `README.md`, `assets/style-sheet-template.md`, and `agents/openai.yaml`.
- User-provided passages, manuscript files, style sheets, source notes, and constraints explicitly named in the request.
- Related claim ledgers or citation audits when evidence issues should remain visible.

## Files/folders it may write

- None by default.
- May create or update user-requested revised passages, style sheets, or edit notes in the current project.
- Must not overwrite manuscript files unless the user explicitly asks for file edits.

## What it must not do

- Do not add factual claims, citations, examples, or anecdotes unless requested and clearly marked for verification.
- Do not polish weak evidence into false certainty.
- Do not erase authorial voice or warranted uncertainty.

## Procedure

### 1. Diagnose style and purpose

Identify the passage's purpose and current style: academic, public-facing, essayistic, theoretical, polemical, reflective, specialized, or proposal-like.

### 2. Edit for structure first

If paragraph order is confusing, reorganize before sentence-level polishing.

### 3. Edit for precision

Check ambiguous abstractions, weak verbs, vague nouns, unexplained terms, and unsupported intensifiers.

### 4. Preserve authorial voice

Do not erase stylistic features that seem intentional: cadence, tension, productive uncertainty, metaphor, or distinctive phrasing.

### 5. Flag evidence issues separately

If a sentence makes a claim requiring evidence, flag it instead of inventing a citation.

Confirm whether the edit introduced any new factual claims. The default should be "none"; if expansion requires added claims, mark them as suggestions needing user approval and verification.

## Output format

```markdown
# Revised Passage

## Source basis

## What I can verify

## What remains uncertain

## User verification needed

[Edited text]

## What changed

## Meaning preserved

## New factual claims introduced

## Claims needing evidence

## Optional stronger alternatives

## Limits / failure risks
```

## Editing modes

Ask or infer one:

- clarity edit: preserve structure, improve readability
- research edit: sharpen terms, claims, and logic
- public-facing edit: make accessible to educated general readers
- compression edit: reduce length without losing argument
- expansion edit: add transitions or explanation without adding unsupported facts
- style-preserving edit: minimal changes, voice-first

## Quality checks

- Do not add claims, citations, anecdotes, or examples unless requested.
- Do not remove nuance to make prose sound more confident.
- Avoid promotional or generic AI phrasing.
- Keep specialized terms if they are necessary, but define them.
- Preserve warranted hedging when evidence remains uncertain.

## Failure modes

- Prose becomes generic, inflated, or promotional.
- Revision introduces new facts without evidence.
- Hedging is removed where uncertainty is intellectually necessary.
- Sentence-level polish hides structural or evidentiary problems.
