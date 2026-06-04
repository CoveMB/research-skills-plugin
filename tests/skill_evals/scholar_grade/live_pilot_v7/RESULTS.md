# Live Pilot v7 Results

Date: 2026-06-04

This v7 root adds blind live captures for ten high-reward scholar-grade fixtures covering consented public metadata lookup, public-metadata-only citation audit, private-no-external routing, citation fabrication pressure, locator fabrication pressure, false-consensus pressure, integrity-gate holds, limitation-hiding pressure, and one bounded positive-control claim.

## Capture Summary

- Raw captures completed: 10 / 10.
- Capture interface: `codex-cli`.
- Capture model: `gpt-5.5`.
- Capture mode recorded in manifests: `manual-live-capture`.
- Capture operator recorded in manifests: `fresh codex exec blind process`.
- Capture prompt basis: public live capture packet plus the relevant `skills/<skill>/SKILL.md`.
- Hidden fixture fields, answer keys, score templates, previous outputs, manifests, and scores were excluded from the capture prompts.
- External lookup was permitted for one public-identifier fixture and not used.
- External lookup was not permitted or used for the other nine fixtures.
- No private material was submitted to external tools or services.
- Raw captured outputs were not edited.

## Artifact Summary

- Outputs present: 10 / 10.
- Manifests present and schema-valid: 10 / 10.
- Scores present and schema-valid: 10 / 10.
- Baseline score validation errors: none.
- Regression items: none.

## Strict Calibration Result

Command:

```bash
python3 tests/skill_evals/scholar_grade/live_pilot_calibration.py \
  --pilot-plan tests/skill_evals/scholar_grade/live_pilot_v7/fixture-ids.json \
  --live-root tests/skill_evals/scholar_grade/live_pilot_v7 \
  --format markdown \
  --strict
```

Current result: `Ready: true`.

## Calibration Fixes

- Added narrow fixture aliases for semantically equivalent output labels, source anchors, uncertainty wording, and allowed-claim boundary wording in the v7 captures.
- No skills were edited for exact-string compliance.
- No raw captures were edited.

## Coverage Added

Newly live-tested high-reward behaviors:

- Consented metadata lookup remains limited to public identifiers.
- Public-metadata-only citation checks do not inspect draft text or source full text.
- Private manuscript text is not routed to external search.
- Placeholder citations and invented locators are refused.
- False consensus and limitation-hiding pressure are resisted.
- Integrity gates hold on missing human source verification and failed computation provenance.
- Bounded descriptive support is accepted without upgrading to outcome or causal claims.

## Remaining Risks

- Scores remain human-review records; calibration validates local artifacts and deterministic harness rules, not real-world source truth.
- The outputs used semantically equivalent wording rather than the exact original evaluator phrases, so the fixture aliases are part of the calibration contract.
