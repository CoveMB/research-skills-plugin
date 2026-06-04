# Process Passport Contract

Use a process passport when a durable research artifact is handed from one skill, reviewer, workflow gate, or release/submission step to another.

The passport is not proof that the artifact is correct. It records what produced the artifact, what source basis was visible, what remains unresolved, and what the next user or skill must not assume.

## When Required

Set `handoff_artifact: true` and include `process_passport` when an artifact is durable project state or cross-skill input, including:

- JSON book artifacts that another skill will consume.
- saved search logs, source notes, extraction tables, literature maps, claim ledgers, traceability graphs, citation audits, integrity audits, AI/human workflow logs, release audits, proposal artifacts, or comparable-title checks.
- generated or edited style sheets, chapter briefs, case dossiers, or workflow plans that will guide later work.
- compact outputs only when saved as project state or explicitly reused downstream.

## When Not Required

Do not require a passport for:

- casual answers or one-off advice.
- raw user drafts, source packets, or private notes before they become generated research artifacts.
- normal Markdown replies that are not saved or handed to another stage.
- research-intent routing outputs unless the route is saved as a durable workflow artifact.
- accessibility cleanup that is private, local, and not reused as research input.

These outputs should still keep source basis, source access level, uncertainty, privacy, and verification limits visible when relevant.

## Required Fields

Every `process_passport` must include:

- `artifact_id`: stable local identifier for this artifact.
- `source_basis`: what material was visible when the artifact was produced.
- `source_access_level`: access status such as full text, excerpt only, citation only, prompt only, private-no-external, fixture only, or lookup-consented metadata.
- `corpus_coverage`: corpus scope and representativeness limits, or an explicit statement that corpus coverage was not verified.
- `evidence_status`: concise status such as `verified`, `partial_unverified`, `fixture_unverified`, `verification_needed`, or `hold_for_verification`.
- `tool_use`: list of tools, lookups, scripts, commands, or explicit statement that no external lookup/tool use occurred.
- `human_verification_status`: completed, partial, needed, unavailable, overridden with rationale, or not applicable.
- `unresolved_risks`: list of evidence, source, privacy, method, citation, corpus, or release risks still open.
- `handoff_limits`: list of claims the next skill or reviewer must not make from this artifact.
- `generated_or_updated_at`: date or timestamp.
- `producing_skill`: skill that produced or last materially updated the artifact.
- `intended_next_skill_or_use`: next skill, review gate, release step, or intended use.

## Optional Fields

Use optional fields only when they add traceability without inventing verification:

- `parent_artifact_ids`
- `input_artifact_hashes`
- `output_artifact_hash`
- `verification_tasks`
- `privacy_flags`

When an artifact is part of a deterministic workflow trace, `parent_artifact_ids` and `input_artifact_hashes` are required for every non-initial stage so validators can bind the handoff to the exact upstream artifact bytes. Hashes prove continuity of local artifacts only; they do not prove source truth, full-text access, or human verification.

## Preservation Rules

A downstream skill consuming a passport must:

- read the passport when present.
- preserve unresolved risks and handoff limits unless a visible verification step resolves them.
- carry prior uncertainty into the new artifact's source basis, evidence status, unresolved risks, or handoff limits.
- refuse requests to turn `unverified`, `partial`, `citation only`, `unknown coverage`, or `fixture only` into verified status without a verification step.
- avoid claiming human verification, external lookup, full-text access, source support, field consensus, legal clearance, or release readiness unless the passport and visible evidence support it.

## Acceptable Example

```json
{
  "handoff_artifact": true,
  "process_passport": {
    "artifact_id": "literature-map-chapter-2-2026-06-03",
    "source_basis": "User-provided source notes and extraction table; no new lookup.",
    "source_access_level": "excerpt only",
    "corpus_coverage": "Partial corpus with unknown representativeness; counter-literature not checked.",
    "evidence_status": "partial_unverified",
    "tool_use": ["No external lookup; source notes reviewed locally."],
    "human_verification_status": "needed before manuscript reliance",
    "unresolved_risks": ["Consensus claims not permitted from this corpus.", "Source-claim fit not checked."],
    "handoff_limits": ["Use as a provisional map only.", "Do not convert local patterns into field consensus."],
    "generated_or_updated_at": "2026-06-03T00:00:00-04:00",
    "producing_skill": "literature-review-mapper",
    "intended_next_skill_or_use": "argument-architecture"
  }
}
```

## Unacceptable Example

```json
{
  "handoff_artifact": true,
  "process_passport": {
    "artifact_id": "lit-map-1",
    "source_basis": "Model knowledge",
    "source_access_level": "full text verified",
    "corpus_coverage": "Complete field coverage",
    "evidence_status": "verified",
    "tool_use": ["Searched databases"],
    "human_verification_status": "complete",
    "unresolved_risks": ["None"],
    "handoff_limits": ["None"],
    "generated_or_updated_at": "2026-06-03",
    "producing_skill": "literature-review-mapper",
    "intended_next_skill_or_use": "chapter-architecture"
  }
}
```

This is unacceptable unless actual full-text access, database searches, field coverage, and human verification records are visible. The passport must not fabricate verification.
