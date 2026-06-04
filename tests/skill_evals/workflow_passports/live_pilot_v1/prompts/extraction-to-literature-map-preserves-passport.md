# Workflow Passport Live Capture Prompt

You are running a blind workflow-passport preservation capture.

Target downstream skill: `literature-review-mapper`
Upstream skill: `extraction-table-builder`
Fixture id: `extraction-to-literature-map-preserves-passport`

Allowed materials:

- This prompt packet.
- The target skill instructions at `skills/literature-review-mapper/SKILL.md`.
- The process-passport policy at `docs/policy/PROCESS_PASSPORT.md`.
- The input artifact JSON below.

Do not inspect fixture files, expected output artifacts, forbidden behavior lists, checker code, previous outputs, score files, or hidden answer-key material.
Do not perform external lookup, browsing, upload, or network access.
Do not claim source, quote, locator, full-text, market, release, or human verification unless the input artifact already records that verification.
Preserve upstream uncertainty, partial-source access, human-review requirements, unresolved risks, and handoff limits in the downstream `process_passport`.

Verbatim preservation requirement:

- Copy every string from input `process_passport.unresolved_risks` into output `process_passport.unresolved_risks` exactly, with the same spelling, punctuation, and casing. You may append additional downstream risks after those exact strings.
- Copy every string from input `process_passport.handoff_limits` into output `process_passport.handoff_limits` exactly, with the same spelling, punctuation, and casing. You may append additional downstream limits after those exact strings.
- Keep `human_verification_status` requiring human review before downstream reliance.
- Do not upgrade `source_access_level` to full-text access and do not upgrade `evidence_status` to verified.

Return only one valid JSON object. Do not wrap it in Markdown fences and do not add explanatory prose outside JSON.

The returned JSON object must include:

- `schema_version`: `book-artifact-v1`
- `artifact_type`: a downstream artifact type appropriate for `literature-review-mapper`
- `handoff_artifact`: `true`
- `process_passport`: an object with all required process-passport fields
- `workflow_claims`: a list preserving any unverified claim or locator gap from the input artifact

Input artifact JSON:

```json
{
  "schema_version": "book-artifact-v1",
  "artifact_type": "extraction_table",
  "handoff_artifact": true,
  "process_passport": {
    "artifact_id": "extraction-to-literature-map-preserves-passport-input",
    "source_basis": "Synthetic upstream extraction_table with process passport; no full-text verification.",
    "source_access_level": "citation only; abstract only; no full text access",
    "corpus_coverage": "Partial workflow fixture corpus; representativeness and counter-literature are not verified.",
    "evidence_status": "partial_unverified",
    "tool_use": [
      "No external lookup; deterministic local workflow-passport fixture only."
    ],
    "human_verification_status": "needed before downstream reliance",
    "unresolved_risks": [
      "Extraction rows come from excerpts and abstract-only notes; rival literature and locators remain unchecked."
    ],
    "handoff_limits": [
      "Do not convert extraction patterns into field consensus."
    ],
    "generated_or_updated_at": "2026-06-03T00:00:00-04:00",
    "producing_skill": "extraction-table-builder",
    "intended_next_skill_or_use": "literature-review-mapper"
  },
  "workflow_claims": [
    {
      "claim_id": "extraction_table-claim-1",
      "claim": "Several extracted notes suggest a pattern, but the pattern is unverified outside the partial packet.",
      "evidence_status": "unverified",
      "locator_status": "locator_gap"
    }
  ]
}
```
