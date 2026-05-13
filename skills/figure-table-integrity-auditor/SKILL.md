---
name: figure-table-integrity-auditor
description: Audit scholarly figures, tables, charts, captions, screenshots, extracted results, image panels, and visual evidence for data provenance, axis and caption accuracy, duplicate visual risk, source licensing, manipulation, and claim support limits.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# Figure table integrity auditor

## Purpose

Audit non-prose evidence objects before they support manuscript claims: figures, tables, charts, screenshots, images, maps, result tables, and visual panels.

This skill checks data provenance, caption accuracy, axis labels, duplicate visual risk, extraction or transformation basis, source licensing, and whether the figure or table can support the claim attached to it.

## When to use

Use when a research book, article, proposal, or release packet contains figures, tables, charts, images, screenshots, maps, extracted result tables, or visual evidence that may be cited as support.

Use before publication, external sharing, or citation audit when a visual or table carries factual, empirical, comparative, or quantitative claims.

## Automatic selection guidance

- High-signal triggers: figure audit, table audit, chart integrity, caption check, axis check, data provenance, duplicate visual, image manipulation, screenshot source, table claim support, or visual evidence.
- Light-route behavior: audit only visible figures/tables and mark unavailable data or source files as verification gaps.
- Deep-work gate: source file, dataset, image-source, license, or current lookup happens only when provided, explicitly requested, or routed from deep mode with available tools.
- Noise and slowdown guard: do not run on decorative images unless they carry scholarly claims, source rights, or release risk.

## Do not use this skill when

- The user needs text citation-source fit checked; use `citation-integrity-auditor`.
- The user needs broad release risk checked; use `rights-privacy-release-auditor`.
- The user needs source credibility rather than visual/table provenance; use `methodology-source-auditor`.

## Inputs expected

- Figures, tables, captions, chart data, image files, screenshots, source pointers, or manuscript passages that discuss the visual/table.
- Dataset, extraction table, script or notebook, run log, source citation, license, or source image when available.
- The claim each figure/table is meant to support.

## Source basis and AI limits

Follow `docs/SOURCE_LIMITS.md`: state the source access level, separate source basis from interpretation, include What I can verify, What remains uncertain, and User verification needed. Do not invent citations or source support.

## Compact output

Use compact output when the user asks for low reading load, visual/table blockers, or a quick evidence-object triage. Compact output should keep source basis and unavailable data/source files visible, focus on objects whose verdict changes manuscript, citation, or release action, and end with one next action.

## Machine-readable artifacts

When the user explicitly asks for JSON or a contract artifact, use `shared/contracts/book/book_artifact.schema.json` with `artifact_type: figure_table_integrity_audit`. If the output is normal Markdown, do not force the JSON contract.

## Files/folders it may read

- Bundled skill instructions, metadata, and assets if available (including, but not limited to, `SKILL.md`, `README.md`, `assets/`, `references/`, and `agents/openai.yaml` in this project or equivalent files in another project).
- Shared policy docs, especially `docs/SOURCE_LIMITS.md`, `docs/AUTO_SELECTION_GUARDRAILS.md`, and `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.
- User-provided figures, tables, captions, data files, extracted rows, notebooks, source images, licenses, manuscript sections, and project files explicitly named in the request.

## Files/folders it may write

- None by default.
- May create or update user-requested figure/table audit reports, repair lists, or release notes in the user-designated project or workspace.
- Must not alter figures, tables, datasets, images, manuscripts, or source files unless explicitly asked.

## What it must not do

- Do not infer data provenance from a polished chart or caption.
- Do not invent data, source images, licenses, transformations, or statistical results.
- Do not declare a figure/table safe for release when rights, source, or sensitive-data status is unavailable.

## Procedure

### 1. Identify evidence object and claim

For each object, record figure/table ID, caption, manuscript claim, source basis, and available data/source files.

### 2. Check data provenance

Record dataset, source note, extraction table, script or notebook, run log, manual transformation, and version where available. Mark missing provenance visibly.

### 3. Audit caption and axis claims

Check whether caption, axis labels, units, legends, date ranges, sample descriptions, and aggregation claims match the visible data or supplied source.

### 4. Check visual integrity risks

Flag duplicate visual risk, reused panel, unexplained cropping, missing scale, manipulated image, misleading axis, unmarked uncertainty, cherry-picked range, or table values without calculation basis.

### 5. Check rights and release constraints

Flag missing license, unclear permission, sensitive data, source-image reuse, screenshot risk, or copied publisher material. Route broad release blockers to `rights-privacy-release-auditor`.

### 6. Assign repair action

Use the smallest repair: add provenance, correct caption, relabel axis, add uncertainty, cite source, provide data file, verify license, replace visual, or remove unsupported claim.

## Output format

```markdown
# Figure table integrity audit

## Source basis

## What I can verify

## What remains uncertain

## User verification needed

## Figure/table audit
| Object | Claim supported | Data provenance | Caption/axis status | Duplicate visual risk | Rights/release risk | Verdict | Repair action |

## High-priority blockers

## Data or source files still needed

## Limits / failure risks

```

Compact output:

```markdown
# Figure/table blockers

Source basis: [one line]
How to use this result: BLOCKER SUMMARY - This lists visible figure/table blockers only; do not treat it as full data, rights, or claim clearance.

| Object | Verdict | Blocker or gap | Required repair |

Needed files: [only if data, source image, license, or run log is needed]
Next action: [one action]
```

Use the optional Suggested next step policy in `docs/AUTO_SELECTION_GUARDRAILS.md`; it may be omitted unless one skill reduces a named scholarly risk.

## Quality checks

- Every figure/table verdict distinguishes visible inspection from verified source data.
- Caption and axis claims must match available evidence or stay unverified.
- Duplicate visual and manipulated image risks are visible.
- Data provenance gaps block strong empirical claims.

## Failure modes

- Caption claims are accepted without source data.
- A duplicate visual or reused panel hides weak evidence.
- Missing axis units or date ranges create misleading claims.
- Rights and license risk is treated as citation formatting.
