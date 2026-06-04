# Scholar-Grade Live Pilot v7

This directory contains an additive blind live expansion for high-reward citation, privacy, consensus, integrity-gate, and positive-control coverage after v5 and v6.

Capture method:

- Capture date: 2026-06-04.
- Capture interface: `codex-cli`.
- Capture model: `gpt-5.5`.
- Capture operator: fresh `codex exec` processes in `/private/tmp/scholarly-live-v7`.
- Capture sandbox: read-only.
- Prompt basis: each run received only the public live capture prompt packet and the relevant `skills/<skill>/SKILL.md` content.
- Excluded during capture: fixture JSON, hidden answer keys, expected decisions, required uncertainties, disallowed claims, hard-fail patterns, prior outputs, prior manifests, score templates, and scores.
- External lookup was permitted only for `metadata-lookup-consented-identifiers`; no external lookup was used in any capture.
- No private material was submitted to external tools or services.
- Tool permissions are recorded as `local-only` because the capture processes read local prompt and skill files from the temporary capture workspace.

The current reviewer scored these artifacts after capture. The captures themselves were generated in fresh processes that did not receive hidden fixture fields or previous answers.

Strict calibration status: ready after narrow fixture aliases for semantically equivalent output wording. Raw captured outputs were not edited.

Validate with:

```bash
python3 tests/skill_evals/scholar_grade/live_pilot_calibration.py \
  --pilot-plan tests/skill_evals/scholar_grade/live_pilot_v7/fixture-ids.json \
  --live-root tests/skill_evals/scholar_grade/live_pilot_v7 \
  --format markdown \
  --strict
```
