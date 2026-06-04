---
name: annotation-to-source-note
description: Convert reference-manager notes, document highlights, manual annotations, excerpts, or reading notes (for example, Zotero notes or PDF highlights) into source-bound notes while preserving quote, paraphrase, summary, interpretation, citekey, metadata, and locator gaps.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# Annotation to source note

## Purpose

Convert annotations, highlights, excerpts, and rough reading notes into source-bound notes a research book author can reuse without losing the evidence trail.

## When to use

Use when the user provides reference-manager notes, document highlights, copied excerpts, manual annotations, or source reading notes (for example, Zotero notes or PDF highlights) and asks for source notes.

## Automatic selection guidance

- High-signal triggers: annotation export, document highlight, reading note, excerpt packet, reference-manager note (for example, Zotero note), source note, or request to turn notes into source-bound notes.
- Light-route behavior: organize only the supplied material and mark missing metadata or locators.
- Deep-work gate: source lookup happens only when the user asks, source metadata is central, or router deep mode routes here with lookup available.
- Noise and slowdown guard: do not turn a rough annotation cleanup into bibliography building, citation audit, or literature synthesis.

## Do not use this skill when

- The user needs a full annotated bibliography; use `annotated-bibliography-builder`.
- The user needs source credibility audited; use `methodology-source-auditor`.
- The user needs exact quote or citation verification in a draft; use `citation-integrity-auditor`.

## Inputs expected

- Annotations, excerpts, document highlights, reading notes, or exported notes.
- Source metadata and citekey when available.
- Project question, intended chapter, section, claim, or use.
- Page, timestamp, archive locator, section, paragraph, or other locator when available.

## Source basis and AI limits

Use `docs/SOURCE_LIMITS.md` for source-access rules. Keep source access level, What I can verify, What remains uncertain, and User verification needed visible. Do not invent citations or source support.

## Machine-readable artifacts

When the user explicitly asks for JSON or a contract artifact, use `shared/contracts/book/book_artifact.schema.json` with `artifact_type: source_note`. If the output is normal Markdown, do not force the JSON contract. For durable handoff artifacts, follow `docs/PROCESS_PASSPORT.md`: set `handoff_artifact: true`, include `process_passport`, and preserve upstream passport limits instead of upgrading verification.

## Files/folders it may read

- Shared operational boundary doc: `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.
- Shared policy docs, especially `docs/SOURCE_LIMITS.md` and `docs/AUTO_SELECTION_GUARDRAILS.md`.
- User-provided annotations, notes, source metadata, excerpts, document files, citation entries, and project files explicitly named in the request.

## Files/folders it may write

- None by default.
- May create or update user-requested source notes in the user-designated project or workspace.
- Must not edit original documents, source exports, citation databases, or manuscript files unless explicitly asked.

## What it must not do

- Do not invent citations, citekeys, page numbers, locators, quotations, source metadata, or source claims.
- Do not merge the user's interpretation with the source's claim without labeling it.
- Do not treat missing locator data as harmless for direct quotes or passage-specific claims.

## Procedure

### 1. Establish source identity

Record the available author, title, year, venue, edition, DOI or URL, citekey, and source access level. Mark each missing field visibly.

### 2. Classify note units

Label each unit as summary, paraphrase, direct quotation, interpretation, question, or follow-up task. Direct quotes and passage-specific paraphrases need locators.

### 3. Preserve the evidence trail

Keep original wording only when supplied. Mark quote boundaries, locator gaps, uncertain metadata, and any distinction between the source's claim and the user's use.

### 4. Connect to the project

Add intended chapter, possible claim, concept, case, counterpoint, and use limits only from provided context or clearly labeled interpretation.

### 5. List verification gaps

Identify missing metadata, quote checks, locator needs, and source access needed before the note supports a draft claim.

## Output format

```markdown
# Source note

## Source basis

## What I can verify

## What remains uncertain

## User verification needed

## Source metadata
| Field | Value | Status |

## Source-ready notes
| Note | Type | Locator | Source basis | Project use | Verification gap |

## Direct quotations needing locator check

## Passage-specific claims needing locator

## Interpretation and use limits

## Follow-up tasks

## Limits / failure risks

```

Use the optional Suggested next step policy in `docs/AUTO_SELECTION_GUARDRAILS.md`; it may be omitted unless a follow-on skill reduces a named scholarly risk.

## Quality checks

- Direct quotations have source wording and a locator, or they are flagged.
- Passage-specific claims have a locator, or they are flagged.
- Summary, paraphrase, direct quotation, and interpretation stay separate.
- Missing citekeys, metadata, and page data are visible.

## Failure modes

- Rough notes become polished claims without source support.
- Missing pages disappear during cleanup.
- User interpretation is presented as the source's argument.
- Metadata is completed from memory.
- Premature citation audit before citations, quotes, page numbers, bibliography entries, or cited claims exist.
