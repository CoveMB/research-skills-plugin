# Live Pilot v6 Results

Date: 2026-06-04

This v6 root adds blind live captures for the three lower-risk fixtures that remained outside the current strict blind root after v5.

## Capture Summary

- Raw captures completed: 3 / 3.
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

- Outputs present: 3 / 3.
- Manifests present and schema-valid: 3 / 3.
- Scores present and schema-valid: 3 / 3.
- Baseline score validation errors: none.
- Regression items: none.

## Strict Calibration Result

Command:

```bash
python3 tests/skill_evals/scholar_grade/live_pilot_calibration.py \
  --pilot-plan tests/skill_evals/scholar_grade/live_pilot_v6/fixture-ids.json \
  --live-root tests/skill_evals/scholar_grade/live_pilot_v6 \
  --format markdown \
  --strict
```

Current result: `Ready: true`.

## Calibration Fixes

- Added narrow fixture aliases for semantically equivalent output labels, source anchors, uncertainty wording, and allowed-claim boundary wording in the v6 captures.
- No skills were edited for exact-string compliance.
- No raw captures were edited.

## Coverage Added

Newly live-tested lower-risk skills:

- `dictation-to-research-notes`
- `dyslexia-research-companion`
- `reading-load-reducer`

## Remaining Risks

- Scores remain human-review records; calibration validates local artifacts and deterministic harness rules, not real-world source truth.
- The outputs used semantically equivalent wording rather than the exact original evaluator phrases, so the fixture aliases are part of the calibration contract.
- With v5 and v6 present, all skills listed as current strict-root gaps in the expansion plan have now been blind live-captured.
