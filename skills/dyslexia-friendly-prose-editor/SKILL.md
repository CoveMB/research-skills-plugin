---
name: dyslexia-friendly-prose-editor
description: Repair spelling, grammar, sentence boundaries, punctuation, paragraph breaks, and local readability in existing scholarly prose for dyslexic or dysorthographic authors while preserving meaning, authorial voice, uncertainty, evidence limits, and a brief change summary.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# Dyslexia-friendly prose editor

## Purpose

Make existing scholarly prose easier to read, review, and use without changing the author's argument.

This skill focuses on meaning-preserving repair: spelling, grammar, sentence boundaries, punctuation, paragraph breaks, and readability. It keeps uncertainty and evidence gaps visible.

## When to use

Use when the user provides an existing paragraph, section, abstract, proposal passage, or chapter excerpt and asks for spelling repair, grammar cleanup, sentence repair, dyslexia-friendly editing, dysorthographic cleanup, or a meaning-preserving edit.

Use this instead of `scholarly-prose-editor` when accessibility, spelling, or orthography is the main bottleneck. Use `dictation-to-research-notes` when the input is spoken notes rather than prose.

## Automatic selection guidance

- High-signal triggers: spelling repair, grammar cleanup, dyslexia-friendly edit, dysorthographic edit, sentence boundaries, punctuation repair, typo-heavy prose, meaning-preserving edit, or correction log.
- Light-route behavior: revise only the supplied prose, preserve meaning, and provide a brief change summary.
- Deep-work gate: route to claim audit, citation audit, release audit, or expert/user verification only when the edit exposes evidence gaps, overclaiming, citations, quotes, locators, privacy concerns, consent language, legal/medical/financial claims, commitments, obligations, or publication-facing wording needing verification.
- Noise and slowdown guard: do not turn a surface repair into a style rewrite, chapter restructure, source search, or literature synthesis.

## Do not use this skill when

- The user provides voice notes or fragments that are not yet prose; use `dictation-to-research-notes`.
- The user needs dense source triage; use `reading-load-reducer`.
- The user needs argument or chapter structure; use `argument-architecture` or `chapter-architecture`.
- The user wants a broader style, rhythm, or public-facing prose edit after evidence is stable; use `scholarly-prose-editor`.
- The user needs citation, quote, page, or bibliography verification; use `citation-integrity-auditor`.

## Inputs expected

- Existing prose passage, abstract, proposal section, chapter excerpt, or draft paragraph.
- Desired repair level: minimal correction, local sentence repair, paragraph breaks, or issue-list cleanup.
- Terms, names, quotes, technical phrases, numbers, dates, diagnoses, policy phrases, commitments, obligations, consent language, and claims that must not change.
- Optional source basis if claims or citations should be flagged.

## Source basis and AI limits

Use `docs/SOURCE_LIMITS.md` for source-access rules. Keep source access level, What I can verify, What remains uncertain, and User verification needed visible. Do not invent citations or source support.

Treat spelling and grammar cleanup as surface repair. If a correction could change a claim, responsibility, consent, obligation, commitment, deadline, diagnosis, or evidence status, keep the original wording visible and mark the ambiguity.

## Compact output

Use compact output when the user asks for low reading load, minimal correction, or fast prose repair. Compact output should use short chunks, stable table labels when a table is needed, the revised passage, one source-basis line, changed phrases only when review is needed, and one evidence or ambiguity note only when relevant.

## Files/folders it may read

- Shared operational boundary doc: `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.
- Shared policy docs, especially `docs/SOURCE_LIMITS.md`, `docs/AUTO_SELECTION_GUARDRAILS.md`, `docs/ROUTING_MATRIX.md`, and `docs/SKILL_INDEX.md`.
- User-provided passages, drafts, source excerpts, style constraints, citation notes, or artifacts explicitly named in the request.

## Files/folders it may write

- None by default.
- May create or update user-requested revised passages, correction notes, or edit logs in the user-designated project or workspace.
- Must not overwrite original manuscripts, source files, notes, or bibliography databases unless the user explicitly asks.

## What it must not do

- Do not change the author's argument to make the prose smoother.
- Do not erase warranted uncertainty, qualifiers, commitments, consent language, obligations, or evidence limits.
- Do not silently "fix" names, terms, citations, quotes, numbers, dates, diagnoses, policy language, or technical language when uncertain.
- Do not add facts, examples, citations, promises, obligations, or source claims.
- Do not shame or foreground the user's spelling difficulty.

## Procedure

### 1. Select repair level

Default to minimal correction unless the user asks for a stronger pass or the requested output clearly requires one:

- minimal correction: spelling, punctuation, grammar, and sentence boundaries only
- local sentence repair: minimal correction plus light reordering inside sentences
- paragraph repair: add paragraph breaks and transitions without new claims
- issue-list cleanup: repair prose and include a concise issue list without broader style polish

### 2. Protect meaning

Identify terms, claims, quotes, citations, names, numbers, dates, diagnoses, commitments, obligations, consent language, policy phrases, and qualifiers that must remain stable.

If a correction may change meaning, keep it in the ambiguity table rather than silently editing.

### 3. Repair the prose

Fix spelling, grammar, punctuation, sentence boundaries, and readability. Keep authorial voice where possible.

Do not add new factual claims, promises, or obligations. If a repair requires adding explanation, label it as optional.

### 4. Summarize changes compactly

Report:

- meaning preserved
- new factual claims introduced
- ambiguous corrections
- changed phrases that deserve quick user review, when present
- claims or commitments needing verification

### 5. Route only when needed

If the repaired prose reveals a concrete scholarly risk, suggest one next skill:

- unsupported or overstated claims: `claim-evidence-ledger`
- citation or quote verification: `citation-integrity-auditor`
- privacy, consent, or external-sharing risk: `rights-privacy-release-auditor`
- broader rhythm or public-facing style after evidence is stable: `scholarly-prose-editor`
- rough idea structure still unclear: `dictation-to-research-notes` or `dyslexia-research-companion`

For legal, medical, financial, workplace, or publication verification, state the need for appropriate source access, user confirmation, or expert review instead of treating the edit as clearance.

## Output format

```markdown
# Prose edit

## Source basis

## Repair level

## Revised passage

## Meaning preserved

## New factual claims introduced

## Changed phrases to review
| Original | Revised | Why changed | User check needed |

## Ambiguous corrections
| Original | Possible correction | Why it matters | User check |

## Claims or commitments needing verification

## What I can verify

## What remains uncertain

## User verification needed

```

## Failure-mode output boundaries

When handling evidence-sensitive prose repair, use stable labels that keep meaning and claim strength visible: Source basis, Revised passage, Meaning-preserving changes, Ambiguity, What remains uncertain, and Next action. If rough wording strengthens a claim beyond the evidence, state Repair wording without changing claim strength. Make the causal-strength risk visible with The causal verb changes the claim strength and keep the safe boundary The revised passage may soften unsupported causal wording.

Compact output:

```markdown
# Prose repair

Source basis: [one line]
How to use this result: TRIAGE ONLY - Use this only as meaning-preserving prose repair; do not treat it as evidence, citation, or release clearance.

[Revised passage]

Ambiguity: [only if meaning could change]

Review: [meaning-preserving notes or "No meaning-changing edits"]

Next action: [one action]
```

Use the optional Suggested next step policy in `docs/AUTO_SELECTION_GUARDRAILS.md`; it may be omitted unless a follow-on skill reduces a named scholarly risk.

## Quality checks

- Meaning, argument, and uncertainty are preserved.
- Spelling and grammar repairs do not create new claims, promises, or obligations.
- Ambiguous corrections are visible.
- Output includes a brief change summary.
- No citations, page numbers, source claims, or field consensus are invented.
- Consent language, commitments, obligations, dates, diagnoses, and policy phrases remain stable or are flagged for user review.

## Failure modes

- Prose becomes smoother but less accurate.
- Qualifiers or warranted uncertainty are removed.
- Technical terms, names, or citations are silently miscorrected.
- The edit becomes generic style polish instead of accessibility-focused repair.
- Evidence gaps are hidden by cleaner sentences.
- Smoother prose silently changes commitments, consent, obligations, deadlines, diagnoses, responsibility, or claim strength.
