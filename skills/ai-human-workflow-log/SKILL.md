---
name: ai-human-workflow-log
description: Record AI/human research workflow decisions, human checkpoints, tool use, override reasons, unresolved risks, verification responsibilities, and AI-use disclosure notes for scholarly manuscripts, book projects, proposals, or release packets.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# AI human workflow log

## Purpose

Create a concise audit trail for AI-assisted scholarship: what the AI helped with, what a human decided, what remains unverified, and what disclosure may be needed for a venue, press, committee, or collaborator.

This skill does not judge the scholarship by itself. It records human decision points, tool use, override reason, affected sections, human verification, and venue-specific disclosure needs so later audits can see who decided what and why.

## When to use

Use when a project has AI-assisted research, drafting, summarization, extraction, search planning, citation checking, data analysis, or revision and the user needs a workflow record or AI-use disclosure basis.

Use it after a `scholarly-integrity-gate` reports OVERRIDDEN or when a project is heading toward external sharing, submission, proposal review, or publication.

## Automatic selection guidance

- High-signal triggers: AI-use disclosure, AI workflow log, human checkpoint, human decision, override reason, tool use, affected sections, human verification, venue-specific disclosure, or external sharing after AI-assisted work.
- Light-route behavior: record the visible workflow decisions and mark missing decisions instead of reconstructing history from memory.
- Deep-work gate: review manuscript, source, citation, or release facts only when provided or routed from a specialist audit.
- Noise and slowdown guard: do not require a workflow log for private low-risk brainstorming unless the user asks or external sharing is likely.

## Do not use this skill when

- The user needs a scholarly integrity pass/fail decision; use `scholarly-integrity-gate`.
- The user needs privacy/copyright/release blockers audited; use `rights-privacy-release-auditor`.
- The user needs source or citation verification; use `citation-integrity-auditor`.

## Inputs expected

- Tool names or AI-assisted steps used in the project.
- Human decisions, approvals, overrides, or unresolved risks.
- Draft sections, artifacts, sources, analyses, or proposal elements affected by AI assistance.
- Target venue, press, committee, collaborator, or disclosure policy when known.

## Source basis and AI limits

Use `docs/policy/SOURCE_LIMITS.md` for source-access rules. Keep source access level, What I can verify, What remains uncertain, and User verification needed visible. Do not invent citations or source support.

## Machine-readable artifacts

When the user explicitly asks for JSON or a contract artifact, use `shared/contracts/book/book_artifact.schema.json` with `artifact_type: ai_human_workflow_log`. If the output is normal Markdown, do not force the JSON contract. For durable handoff artifacts, follow `docs/policy/PROCESS_PASSPORT.md`: set `handoff_artifact: true`, include `process_passport`, and preserve upstream passport limits instead of upgrading verification.

## Files/folders it may read

- Shared operational boundary doc: `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`.
- Shared policy docs, especially `docs/policy/SOURCE_LIMITS.md` and `docs/policy/AUTO_SELECTION_GUARDRAILS.md`.
- User-provided drafts, audit reports, tool-use notes, workflow notes, source logs, release packets, proposal files, and project files explicitly named in the request.

## Files/folders it may write

- None by default.
- May create or update user-requested workflow logs, disclosure notes, checkpoint tables, or override records in the user-designated project or workspace.
- Must not edit manuscript, bibliography, source, or submission files unless explicitly asked.

## What it must not do

- Do not invent AI tool use, human approval, source verification, disclosure requirements, or override rationale.
- Do not imply that disclosure language satisfies a venue policy unless the policy text was provided or verified.
- Do not hide unresolved risks behind a vague statement that a human reviewed the work.
- Do not conceal AI involvement or rewrite the record to make AI-assisted work appear fully human-authored.
- Do not transfer responsibility to the tool; authors, researchers, or project owners remain responsible for claims, sources, rights, privacy, and submission decisions.

## Procedure

### 1. Establish workflow basis

List what is known from supplied material: AI tool use, human decisions, review checkpoints, artifacts affected, and policies or venue requirements.

### 2. Record human checkpoints

For each human decision, capture:

- checkpoint name
- human decision
- rationale
- unresolved risks
- override reason, if any
- next stage allowed or blocked

### 3. Record AI assistance

For each AI-assisted step, record:

- tool or system used, if known
- task performed
- affected sections or artifacts
- human verification completed
- remaining verification needed

### 4. Draft disclosure basis

When a venue or press requires disclosure, create conservative disclosure notes that identify tool use, scope, affected sections, and human responsibility. Mark venue-specific disclosure as draft language unless policy text was supplied.

If venue policy is missing or possibly currentness-sensitive, mark policy status as unverified or lookup needed instead of claiming compliance.

### 5. Route unresolved risk

Recommend one repair owner only when a concrete unresolved risk remains.

## Output format

```markdown
# AI human workflow log

## Source basis

## What I can verify

## What remains uncertain

## User verification needed

## Human checkpoints
| Checkpoint | Human decision | Rationale | Unresolved risk | Override reason | Next stage |

## AI assistance record
| Tool use | Task | Affected sections | Human verification | Remaining verification |

## Disclosure notes

## Venue-specific disclosure draft

## Risks requiring follow-up

## Limits / failure risks

```

## Failure-mode output boundaries

When handling missing AI-use provenance, use stable labels that keep the audit actionable: Source basis, affected sections, human verification gap, override reason, disclosure note, and Next action. If verification records are missing, state Record verification gaps before release. Keep uncertainty explicit with No human verification record is visible, and include: The log can identify missing verification and disclosure records.

Use the optional Suggested next step policy in `docs/policy/AUTO_SELECTION_GUARDRAILS.md`; it may be omitted unless a follow-on skill reduces a named scholarly risk.

## Quality checks

- Every override has a reason and unresolved risk.
- Every AI-assisted step has an affected artifact or section.
- Human verification is specific, not a generic approval claim.
- Disclosure language is labeled as draft unless the venue policy was available.

## Failure modes

- Treating tool use as harmless because it happened early in the workflow.
- Recording human review without saying what was reviewed.
- Omitting affected sections, making later disclosure unusable.
- Inventing policy-specific disclosure language without the policy text.
