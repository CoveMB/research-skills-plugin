# Live Pilot v5 Results

Date: 2026-06-04

This v5 root adds blind live captures for 17 high-risk fixtures that were missing from the current strict blind root.

## Capture Summary

- Raw captures completed: 17 / 17.
- Capture interface: `codex-cli`.
- Capture model: `gpt-5.5`.
- Capture mode recorded in manifests: `manual-live-capture`.
- Capture operator recorded in manifests: `fresh codex exec blind process`.
- Capture prompt basis: public live capture packet plus the relevant `skills/<skill>/SKILL.md`.
- Hidden fixture fields, answer keys, score templates, previous outputs, manifests, and scores were excluded from the capture prompts.
- External lookup was not permitted or used.
- Private material was not submitted.
- Raw captured outputs were not edited.

## Artifact Summary

- Outputs present: 17 / 17.
- Manifests present and schema-valid: 17 / 17.
- Scores present and schema-valid: 17 / 17.
- Baseline score validation errors: none.
- Regression items: none.

## Strict Calibration Result

Command:

```bash
python3 tests/skill_evals/scholar_grade/live_pilot_calibration.py \
  --pilot-plan tests/skill_evals/scholar_grade/live_pilot_v5/fixture-ids.json \
  --live-root tests/skill_evals/scholar_grade/live_pilot_v5 \
  --format markdown \
  --strict
```

Current result: `Ready: true`.

## Calibration Fixes

- Added one evaluator rejection-context fix so `cannot verify ... field consensus` is treated as rejected unsafe wording rather than an asserted hard fail.
- Added narrow fixture aliases for semantically equivalent section labels, source anchors, uncertainty wording, and allowed-claim boundary wording in the v5 captures.
- No skills were edited for exact-string compliance.
- No raw captures were edited.

## Coverage Added

Newly live-tested skills:

- `systematic-source-discovery`
- `book-proposal-scholarship`
- `claim-evidence-ledger`
- `scholarly-prose-editor`
- `annotated-bibliography-builder`
- `case-study-integration`
- `argument-architecture`
- `counterargument-peer-review`
- `chapter-architecture`
- `manuscript-continuity-editor`
- `research-book-orchestrator`
- `scholarly-research-agenda`

Older-only skills recaptured into the current strict expansion:

- `rights-privacy-release-auditor`
- `book-comps-verifier`
- `claim-traceability-graph`
- `annotation-to-source-note`
- `discovery-runner-deduper`

## Remaining Risks

- Scores remain human-review records; calibration validates local artifacts and deterministic harness rules, not real-world source truth.
- The outputs used semantically equivalent wording rather than the exact original evaluator phrases, so the fixture aliases are part of the calibration contract.
- Lower-risk wrapper skills remain for v6 until `dictation-to-research-notes`, `dyslexia-research-companion`, and `reading-load-reducer` are captured.
