---
name: scholarly-prose-editor
description: Edit research nonfiction prose when passages, chapter excerpts, proposals, abstracts, or introductions need clarity, precision, structure, rhythm, compression, readability, or voice while preserving nuance and evidence limits.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# Research prose editor

## Purpose

Improve research nonfiction prose without flattening the author's voice or over-polishing into generic language.

## When to use

Use when the user provides a paragraph, section, chapter excerpt, proposal, abstract, or introduction that needs clearer research prose.

## Automatic selection guidance

- High-signal triggers: edit prose, clarity, precision, structure, rhythm, compression, readability, authorial voice, abstract, introduction, or proposal language.
- Light-route behavior: revise only the supplied prose and flag unsupported claims without adding new factual content.
- Deep-work gate: route to `claim-evidence-ledger` when prose problems hide evidence gaps or overclaiming.
- Noise and slowdown guard: do not transform a prose edit into a research audit unless claim risk is visible.

## Do not use this skill when

- The user needs chapter structure; use `chapter-architecture`.
- The user needs citation verification; use `citation-integrity-auditor`.
- The user needs privacy, copyright, quote, license, or release risk checked before sharing; use `rights-privacy-release-auditor`.
- The user asks for new source-backed claims rather than prose revision.
- The user needs rough notes, dictation, spelling ambiguity, reading load, or meaning-preserving surface repair before broader style work; use the smallest accessibility entry point in `docs/ROUTING_MATRIX.md`.

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

Use `docs/SOURCE_LIMITS.md` for source-access rules. Keep source access level, What I can verify, What remains uncertain, and User verification needed visible. Do not invent citations or source support.

## Machine-readable artifacts

When the user explicitly asks for JSON or a contract artifact, use `shared/contracts/book/book_artifact.schema.json` with `artifact_type: style_sheet`. If the output is normal Markdown, do not force the JSON contract. For durable handoff artifacts, follow `docs/PROCESS_PASSPORT.md`: set `handoff_artifact: true`, include `process_passport`, and preserve upstream passport limits instead of upgrading verification.

## Files/folders it may read

- Shared operational boundary doc: `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.
- Shared policy docs, especially `docs/SOURCE_LIMITS.md` and `docs/AUTO_SELECTION_GUARDRAILS.md`.
- User-provided passages, manuscript files, style sheets, source notes, and constraints explicitly named in the request.
- Related claim ledgers or citation audits when evidence issues should remain visible.

## Files/folders it may write

- None by default.
- May create or update user-requested revised passages, style sheets, or edit notes in the user-designated project or workspace.
- Must not overwrite manuscript files unless the user explicitly asks for file edits.

## What it must not do

- Do not add factual claims, citations, examples, or anecdotes unless requested and clearly marked for verification.
- Do not polish weak evidence into false certainty.
- Do not erase authorial voice or warranted uncertainty.
- Do not compress away decision-critical caveats, disputed terms, source limits, or responsibility language.
- Do not agree with a false premise in the user's requested wording; flag the premise and offer the strongest supportable revision.

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
# Revised passage

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

Use the optional Suggested next step policy in `docs/AUTO_SELECTION_GUARDRAILS.md`; it may be omitted unless a follow-on skill reduces a named scholarly risk.

## Editing modes

Ask or infer one:

- clarity edit: preserve structure, improve readability
- research edit: sharpen terms, claims, and logic
- public-facing edit: make accessible to educated general readers
- compression edit: reduce length without losing argument
- caveat-preserving compression edit: reduce length while keeping uncertainty, source limits, method limits, and responsibility language intact
- expansion edit: add transitions or explanation without adding unsupported facts
- style-preserving edit: minimal changes, voice-first

## Quality checks

- Do not add claims, citations, anecdotes, or examples unless requested.
- Do not remove nuance to make prose sound more confident.
- Avoid promotional or formulaic phrasing.
- Keep specialized terms if they are necessary, but define them.
- Preserve warranted hedging when evidence remains uncertain.
- Preserve caveats that change claim strength, authorship responsibility, source status, method limits, or release/disclosure decisions.

## Failure modes

- Prose becomes generic, inflated, or promotional.
- Revision introduces new facts without evidence.
- Hedging is removed where uncertainty is intellectually necessary.
- Sentence-level polish hides structural or evidentiary problems.
- Compression makes an unverified, stale, causal, statistical, or source-support claim sound settled.
- Premature citation audit before citations, quotes, page numbers, bibliography entries, or cited claims exist.
