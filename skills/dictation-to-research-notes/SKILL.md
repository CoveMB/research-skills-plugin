---
name: dictation-to-research-notes
description: Turn dictated research thoughts, voice transcripts, speech-to-text output, meeting notes, or rambling spoken fragments into structured scholarly notes, claims, questions, evidence needs, ambiguities, and next actions without changing the author's meaning.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# Dictation to research notes

## Purpose

Convert spoken or speech-to-text research material into usable scholarly notes while preserving the author's intended ideas and making uncertainty visible.

This skill is for capture, not polish. It helps a researcher speak freely first, then receive structured notes that can feed agenda, argument, chapter, evidence, or prose work.

## When to use

Use when the user provides dictated notes, voice transcripts, speech-to-text output, rambling fragments, meeting notes, interview self-memos, or spoken thoughts that need structure.

Use this instead of `scholarly-prose-editor` when the input is not yet prose. Use `dyslexia-research-companion` when the task mixes dictation with broader reading-load or accessibility routing.

## Automatic selection guidance

- High-signal triggers: dictated notes, voice memo, speech-to-text, transcript, rambling notes, spoken fragments, "I talked this out", or meeting notes.
- Light-route behavior: segment the dictation into idea units, clean only obvious transcription noise, and produce a claim/question/evidence/action table.
- Deep-work gate: route to claim audit, source lookup, or citation audit only when the structured notes expose a concrete scholarly risk and source material or lookup permission exists.
- Noise and slowdown guard: do not turn dictation cleanup into a full literature review, citation audit, or polished chapter draft.

## Do not use this skill when

- The user needs dense source triage; use `reading-load-reducer`.
- The user needs sentence-level prose repair for an existing passage; use `dyslexia-friendly-prose-editor` or `scholarly-prose-editor`.
- The user needs exact citation, quote, page, or bibliography verification; use `citation-integrity-auditor`.
- The user needs broad accessibility routing across several bottlenecks; use `dyslexia-research-companion`.

## Inputs expected

- Dictated text, transcript, voice-note dump, meeting note, or spoken fragment list.
- Intended use: idea capture, chapter planning, claim drafting, source planning, or next-step triage.
- Optional constraints: speaker labels, source or meeting context, terms that must stay unchanged, target chapter, audience, source context, and whether to show a correction log.

## Source basis and AI limits

Follow `docs/SOURCE_LIMITS.md`: state the source access level, separate source basis from interpretation, include What I can verify, What remains uncertain, and User verification needed. Do not invent citations, page numbers, quotes, source support, or field consensus.

Treat transcription cleanup as surface repair. If a transcript error can change the claim, mark it as an ambiguity instead of guessing.

## Files/folders it may read

- Bundled skill instructions, metadata, and assets if available (including, but not limited to, `SKILL.md`, `README.md`, `assets/`, `references/`, and `agents/openai.yaml` in this project or equivalent files in another project).
- Shared policy docs, especially `docs/SOURCE_LIMITS.md`, `docs/AUTO_SELECTION_GUARDRAILS.md`, `docs/ROUTING_MATRIX.md`, and `docs/SKILL_INDEX.md`.
- User-provided transcripts, dictated notes, drafts, outlines, source excerpts, artifacts, or style constraints explicitly named in the request.

## Files/folders it may write

- None by default.
- May create or update user-requested cleaned notes, capture tables, claim lists, or next-action notes in the user-designated project or workspace.
- Must not overwrite original transcripts, notes, drafts, source files, or bibliography databases unless the user explicitly asks.

## What it must not do

- Do not turn unclear speech into confident scholarly claims.
- Do not erase repetitions that show emphasis unless the cleaned note preserves the emphasis.
- Do not add sources, citations, examples, or facts not present in the input.
- Do not output long prose when a table or short chunks would reduce reading load.
- Do not expose private participant, meeting, or interview details in shareable output without flagging release risk.

## Procedure

### 1. Identify capture context

State whether the input appears to be a voice memo, transcript, meeting note, or rough spoken idea. State the intended output use if provided.

If multiple speakers, interview participants, meeting attendees, or identifiable third parties appear, preserve speaker/source labels where useful and flag privacy review before external sharing.

### 2. Segment into idea units

Break the dictation into discrete units:

- claim
- question
- concept or term
- example or case
- evidence need
- writing task
- uncertainty or ambiguity

Ignore filler words unless they change emphasis, uncertainty, or argument logic.

### 3. Clean only what is safe

Repair obvious speech-to-text noise, punctuation, and sentence boundaries. Preserve terms, names, and technical language unless the correction is certain.

If a phrase has several plausible meanings, keep the original fragment and mark the ambiguity.

### 4. Build research notes

Create a compact table with:

- speaker or source, when present
- original fragment or transcript anchor, when it helps verify meaning
- cleaned note
- type
- argument role
- evidence needed
- ambiguity
- next action

### 5. Route only one next action

If the cleaned notes reveal a clear next step, suggest one specialist skill:

- unstable question: `scholarly-research-agenda`
- source search needed: `systematic-source-discovery`
- argument structure needed: `argument-architecture`
- chapter structure needed: `chapter-architecture`
- evidence risk: `claim-evidence-ledger`
- prose after structure is stable: `dyslexia-friendly-prose-editor`
- identifiable participant, interview, meeting, or third-party details before sharing: `rights-privacy-release-auditor`

## Output format

```markdown
# Dictation to research notes

## Source basis

## Capture context

## Cleaned note table
| # | Speaker/source | Original fragment | Cleaned note | Type | Argument role | Evidence needed | Ambiguity | Next action |

## Ambiguities that matter
| Fragment | Possible meanings | Why it matters | Question |

## What I can verify

## What remains uncertain

## User verification needed

## Suggested next step
```

Use the optional Suggested next step policy in `docs/AUTO_SELECTION_GUARDRAILS.md`; it may be omitted unless one specialist skill reduces a named scholarly risk.

## Quality checks

- Dictated meaning is preserved or ambiguity is explicitly flagged.
- Speaker/source context and original fragments are retained when needed to verify meaning.
- Filler is removed without losing uncertainty, emphasis, or sequence.
- Claims, questions, examples, and evidence needs are separated.
- Output is shorter and easier to scan than the transcript.
- No citations, page numbers, source claims, or field consensus are invented.

## Failure modes

- Transcription cleanup changes the argument.
- Spoken uncertainty becomes false confidence.
- The output becomes polished prose before the idea structure is clear.
- Every sentence is overprocessed instead of grouped into useful idea units.
- Missing evidence becomes hidden because the note is cleaner.
- Private meeting, interview, or participant material is prepared for sharing without release review.
