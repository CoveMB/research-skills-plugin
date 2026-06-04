# Scholar-Grade Live Pilot v4

This directory contains an additive blind recapture of the same ten fixtures used in `live_pilot_v3`.

Capture method:

- Capture date: 2026-06-04.
- Capture interface: `codex-cli`.
- Capture model: `gpt-5.5`.
- Capture operator: fresh `codex exec` processes in `/private/tmp/scholarly-blind-recapture-v4`.
- Capture sandbox: read-only.
- Prompt basis: each run received only the public live capture prompt packet and the relevant `skills/<skill>/SKILL.md` content.
- Excluded during capture: fixture JSON, hidden answer keys, expected decisions, required uncertainties, disallowed claims, hard-fail patterns, prior v3 outputs, prior manifests, score templates, and scores.

The current reviewer can score these artifacts after capture, but the captures themselves were generated in a fresh process that did not receive hidden fixture fields or previous answers.

Strict calibration status: ready after harness rejection-context handling and fixture alias metadata were updated to accept semantically equivalent scholarly output wording. See `RESULTS.md` for details.

Validate with:

```bash
python3 tests/skill_evals/scholar_grade/live_pilot_calibration.py \
  --pilot-plan tests/skill_evals/scholar_grade/live_pilot_v4/fixture-ids.json \
  --live-root tests/skill_evals/scholar_grade/live_pilot_v4 \
  --format markdown \
  --strict
```
