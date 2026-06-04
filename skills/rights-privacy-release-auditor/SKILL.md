---
name: rights-privacy-release-auditor
description: Audit notes, research artifacts, manuscript exports, proposal materials, and shared files for privacy, copyright, quotation, license, secret, credential, local metadata, and release risks before external sharing.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# Rights privacy release auditor

## Purpose

Audit research materials before external sharing for privacy, copyright, quotation, license, credential, and local metadata risks.

## When to use

Use before sending notes, artifacts, manuscript exports, proposal materials, source packets, or project files to readers, collaborators, editors, agents, presses, reviewers, or public venues.

## Automatic selection guidance

- High-signal triggers: release audit, share externally, privacy risk, copyright risk, quote risk, license mismatch, secrets, credentials, publisher text, or proposal packet review.
- Light-route behavior: produce an issue table and release verdict without rewriting content.
- Deep-work gate: external license or publication lookup requires explicit user permission, available tools, and a concrete release risk.
- Noise and slowdown guard: do not run for private drafting unless sharing, export, publication, or handoff is at issue.

## Do not use this skill when

- The user needs citation-source fit checked; use `citation-integrity-auditor`.
- The user needs prose edited; use `scholarly-prose-editor`.
- The user asks for legal advice rather than a writing and release risk audit.
- The user only needs AI-use disclosure or human checkpoint records; use `ai-human-workflow-log`.

## Inputs expected

- Notes, research artifacts, manuscript exports, proposal materials, source packets, bibliography files, or file lists.
- Intended recipient, sharing venue, publication status, and whether the artifact will be public.
- Known permissions, licenses, source ownership, quote policies, and sensitive-data constraints.
- Whether the user wants audit only or repair suggestions.

## Source basis and AI limits

Use `docs/policy/SOURCE_LIMITS.md` for source-access rules. Keep source access level, What I can verify, What remains uncertain, and User verification needed visible. Do not invent citations or source support.

## Compact output

Use compact output when the user asks for low reading load, release blockers, or a quick send/hold decision. Compact output should minimize sensitive repetition, keep source basis and legal uncertainty visible, list critical and major release blockers first, and end with one next action.

## Machine-readable artifacts

When the user explicitly asks for JSON or a contract artifact, use `shared/contracts/book/book_artifact.schema.json` with `artifact_type: rights_privacy_release_audit`. If the output is normal Markdown, do not force the JSON contract. For durable handoff artifacts, follow `docs/policy/PROCESS_PASSPORT.md`: set `handoff_artifact: true`, include `process_passport`, and preserve upstream passport limits instead of upgrading verification.

## Files/folders it may read

- Shared operational boundary doc: `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`.
- Shared policy docs, especially `docs/policy/SOURCE_LIMITS.md` and `docs/policy/AUTO_SELECTION_GUARDRAILS.md`.
- User-provided notes, artifacts, drafts, exports, metadata, source packets, and project files explicitly named in the request.

## Files/folders it may write

- None by default.
- May create or update user-requested release audit reports or issue logs in the user-designated project or workspace.
- Must not delete, redact, rewrite, publish, send, or move content unless explicitly asked.

## What it must not do

- Do not delete or rewrite content unless explicitly asked.
- Do not provide legal advice or claim legal clearance.
- Do not invent permissions, licenses, consent, copyright status, or release approval.
- Do not expose secrets, private notes, or sensitive data in the output more than needed to identify the issue.

## Procedure

### 1. Identify release context

Record intended audience, destination, public or private status, file types, and source access level.

### 2. Scan for risk categories

Check for secrets, tokens, credentials, private personal notes, sensitive data, excessive copied source text, direct quotes without locators, publisher text in public artifacts, AI-generated claims presented as evidence, license mismatch risk, and local bibliography or source metadata that should stay private.

For AI-assisted materials, check whether an AI-use disclosure record exists. Route missing tool use, affected sections, human verification, or venue-specific disclosure notes to `ai-human-workflow-log` before external release when disclosure is likely required.

### 3. Classify severity

Use critical, major, moderate, or minor. Critical means do not release until fixed.

### 4. Specify required fixes

State the smallest fix: remove, redact, verify permission, add locator, replace copied text with paraphrase, cite source, mark as AI-generated, separate private metadata, or get legal review.

### 5. Give release verdict

Use ready to share, share after listed fixes, hold until reviewed, or do not release in current form.

## Output format

```markdown
# Rights privacy release audit

## Source basis

## What I can verify

## What remains uncertain

## User verification needed

## Release context

## Issue table
| Severity | File / artifact pointer | Risk | Evidence visible | Required fix | Release impact |

## Secrets and sensitive-data check

## Copyright and quotation check

## License and vendored-material check

## AI-evidence and source-metadata check

## AI-use disclosure check

## Release verdict

## Limits / failure risks

```

## Failure-mode output boundaries

When handling release-blocker cases, use stable labels that keep rights and privacy limits visible: Source basis, How to use this result, Release verdict, Legal/permission uncertainty, Required fix, and Next action. If rights, copied text, comments, metadata, consent, or permissions are unresolved, state Hold release. Keep uncertainties explicit, including Private notes may be present, and include: The packet should be held until copied text and private notes are reviewed.

Compact output:

```markdown
# Release blockers

Source basis: [one line]
How to use this result: BLOCKER SUMMARY - This lists visible release blockers only; do not treat it as legal clearance or permission to publish.
Release verdict: [ready / share after fixes / hold / do not release]
Legal/permission uncertainty: [none visible / unresolved rights, consent, license, or legal-review need]

| Severity | Artifact pointer | Risk | Required fix | Release impact |

Next action: [one action]
```

Use the optional Suggested next step policy in `docs/policy/AUTO_SELECTION_GUARDRAILS.md`; it may be omitted unless a follow-on skill reduces a named scholarly risk.

## Quality checks

- Critical release blockers are clear.
- Sensitive data is identified with minimal exposure.
- Direct quotes without locators are flagged.
- Legal uncertainty is labeled as uncertainty, not resolved by the audit.

## Failure modes

- Audit becomes legal advice.
- Sensitive content is repeated unnecessarily.
- Copyright or license status is invented.
- Release verdict ignores private metadata or copied source text.
- Premature citation audit before citations, quotes, page numbers, bibliography entries, or cited claims exist.
