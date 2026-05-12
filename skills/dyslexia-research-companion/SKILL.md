---
name: dyslexia-research-companion
description: Route mixed or unclear accessibility bottlenecks for dyslexic, dysorthographic, dictation-heavy, or reading-fatigued scholarly authors when rough notes, spelling ambiguity, voice material, dense sources, or prose repair needs overlap and no smaller accessibility skill clearly owns the task.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# Dyslexia research companion

## Purpose

Reduce reading and writing load for scholarly authors when several text-friction problems overlap and the next smallest accessibility skill is not obvious.

This skill is an accessibility router and wrapper for mixed cases. It preserves the author's ideas, separates cleanup from interpretation, and routes to narrower accessibility or research skills when one clear owner emerges.

## When to use

Use when the user explicitly asks for this companion, asks for broad accessibility help, or describes overlapping bottlenecks such as dyslexia plus dictation plus reading fatigue, spelling ambiguity plus rough notes, or dense material plus unclear next scholarly action.

Also use when the request is accessibility-related but it is unclear whether `dictation-to-research-notes`, `reading-load-reducer`, or `dyslexia-friendly-prose-editor` should own the first pass.

## Automatic selection guidance

- High-signal triggers: mixed accessibility bottleneck, unclear accessibility route, "I have dyslexia and this has dictation plus reading load", "rough notes plus spelling ambiguity", or "help me choose the smallest low-load next step".
- Light-route behavior: choose or recommend the smallest accessibility skill first; normalize input only when no smaller skill clearly owns the request.
- Deep-work gate: route to source lookup, claim audit, citation audit, or literature mapping only when the normalized material exposes a concrete scholarly risk and the needed source material exists or lookup is explicitly requested.
- Noise and slowdown guard: do not produce long prose, broad skill menus, or comprehensive audits when the user needs low-load triage first.

## Do not use this skill when

- The user asks for a standard prose edit with no accessibility, transcription, spelling, or reading-load issue; use `scholarly-prose-editor`.
- The user asks for exact citation, quote, page, or bibliography verification; use `citation-integrity-auditor`.
- The user asks for a full workflow plan across a book project; use `research-book-orchestrator`.
- The user asks only for source discovery, literature mapping, claim audit, or chapter architecture and provides clean inputs for that specialist skill.
- The user asks only for dictated notes; use `dictation-to-research-notes`.
- The user asks only for reading triage; use `reading-load-reducer`.
- The user asks only for meaning-preserving prose repair; use `dyslexia-friendly-prose-editor`.

## Inputs expected

- Rough thought, typo-heavy note, voice transcript, fragment list, source excerpt, draft section, outline, or user-described bottleneck.
- Target use: think through idea, clean note, plan reading, draft claim, prepare chapter, revise paragraph, or decide next step.
- Optional constraints: desired output length, preferred table format, terms that must stay unchanged, and whether spelling should be corrected silently or shown.

## Source basis and AI limits

Follow `docs/SOURCE_LIMITS.md`: state the source access level, separate source basis from interpretation, include What I can verify, What remains uncertain, and User verification needed. Do not invent citations, page numbers, quotes, source support, or field consensus.

Treat spelling and grammar cleanup as surface repair. If a typo can change the claim, mark it as an ambiguity instead of guessing.

## Files/folders it may read

- Bundled skill instructions, metadata, and assets if available (including, but not limited to, `SKILL.md`, `README.md`, `assets/`, `references/`, and `agents/openai.yaml` in this project or equivalent files in another project).
- Shared policy docs, especially `docs/SOURCE_LIMITS.md`, `docs/AUTO_SELECTION_GUARDRAILS.md`, `docs/ROUTING_MATRIX.md`, and `docs/SKILL_INDEX.md`.
- User-provided rough notes, transcripts, drafts, source excerpts, outlines, bibliographies, artifacts, or style constraints explicitly named in the request.

## Files/folders it may write

- None by default.
- May create or update user-requested cleaned notes, low-load structures, action tables, reading plans, or research artifacts in the user-designated project or workspace.
- Must not overwrite original notes, transcripts, drafts, source files, or bibliography databases unless the user explicitly asks.

## What it must not do

- Do not treat spelling cleanup as permission to change the user's meaning.
- Do not hide uncertainty, missing evidence, or locator gaps to make text feel smoother.
- Do not overwhelm the user with long paragraphs when a table, numbered list, or short chunks would work.
- Do not frame dyslexia or dysorthographia as an intellectual weakness.
- Do not route to many skills when one small next action is enough.

## Procedure

### 1. State the work mode

Choose one mode and keep the output shaped for low reading load:

- routing mode: choose the smallest specialist skill for the next step
- mixed capture mode: rough ideas plus other accessibility bottlenecks into structured notes, or route to `dictation-to-research-notes`
- mixed reading triage mode: dense material plus other accessibility bottlenecks into skim/read/skip decisions, or route to `reading-load-reducer`
- claim mode: messy thought into claims, assumptions, and evidence needs
- mixed prose bridge mode: rough wording plus other accessibility bottlenecks into clean wording without new claims, or route to `dyslexia-friendly-prose-editor`

### 2. Normalize without erasing ambiguity

Correct spelling, punctuation, transcription noise, and sentence boundaries only where meaning is clear.

If several readings are plausible, list the ambiguity in a short table:

| Text fragment | Possible meaning | Why it matters | Question |

Ask only questions that change the argument, evidence need, or next action.

### 3. Preserve the author's idea

Separate:

- raw input meaning
- cleaned wording
- interpretation added by the assistant
- evidence need
- uncertainty or ambiguity

Do not turn a rough idea into a confident scholarly claim unless evidence status is clear.

### 4. Convert text into low-load structure

Prefer tables and short blocks:

- claim / why it matters / evidence needed / next action
- term / working definition / ambiguity / source needed
- source / read closely / skim / skip / reason
- paragraph role / current problem / small fix

Keep each cell concise. Use stable labels so the user can scan quickly.

### 5. Route only when useful

If one specialist skill clearly reduces a concrete risk, recommend or use it according to the user's request:

- dictated notes or voice transcript: `dictation-to-research-notes`
- reading fatigue or dense source triage: `reading-load-reducer`
- spelling, grammar, or sentence repair in existing prose: `dyslexia-friendly-prose-editor`
- unclear research question or scope: `scholarly-research-agenda`
- source search burden: `systematic-source-discovery`
- messy highlights or source notes: `annotation-to-source-note`
- source comparison load: `extraction-table-builder`
- field structure overload: `literature-review-mapper`
- argument structure: `argument-architecture`
- chapter structure: `chapter-architecture`
- unsupported claims: `claim-evidence-ledger`
- citation or quote verification: `citation-integrity-auditor`
- sentence clarity after evidence is stable: `scholarly-prose-editor`

## Output format

Use the shortest format that satisfies the request. Default:

```markdown
# Dyslexia research companion

## Source basis

## Work mode

## Cleaned core idea

## Low-load structure
| Item | Meaning | Evidence need | Next action |

## Ambiguities that matter
| Fragment | Possible meanings | Why it matters | Question |

## What I can verify

## What remains uncertain

## User verification needed

## Suggested next step
```

Use the optional Suggested next step policy in `docs/AUTO_SELECTION_GUARDRAILS.md`; it may be omitted unless one specialist skill reduces a named scholarly risk.

## Output rules

- Keep paragraphs short.
- Prefer one table over several paragraphs.
- Use direct wording and stable labels.
- Surface only meaningful spelling or transcription ambiguities.
- Do not show every minor correction unless the user asks for a correction log.
- When rewriting user text, include "meaning preserved" and "new factual claims introduced"; default new factual claims should be none.

## Quality checks

- The user's intellectual claim is preserved or ambiguity is explicitly flagged.
- Cleanup, interpretation, and evidence need are separated.
- Output is shorter and easier to scan than the input.
- Only one next action is recommended unless the user asks for a workflow.
- No citations, page numbers, source claims, or field consensus are invented.

## Failure modes

- Overcorrecting spelling into a different argument.
- Producing polished prose when the user needed idea capture or reading triage.
- Long explanatory output increases reading burden.
- Routing to several specialist skills instead of reducing load.
- Treating unsupported material as verified because it is now written clearly.
