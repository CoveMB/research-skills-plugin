# Workflow Passport Live Pilot v1

This directory contains blind live captures for workflow-passport preservation across four high-value handoff routes.

Capture method:

- Capture date: 2026-06-04.
- Capture interface: `codex-cli`.
- Capture model: `gpt-5.5`.
- Capture operator: fresh `codex exec` processes in `/private/tmp/workflow-passport-live-v1`.
- Capture sandbox: read-only.
- Prompt basis: each run received the live capture prompt packet, the input artifact JSON embedded in that prompt, `docs/policy/PROCESS_PASSPORT.md`, and the relevant downstream `skills/<skill>/SKILL.md`.
- Excluded during capture: workflow-passport fixture JSON, expected output artifacts, forbidden behavior lists, checker code, previous outputs, and answer-key material.
- External lookup, browsing, upload, and network access were not permitted or used.
- No private material was submitted to external tools or services.
- Raw captured outputs were not edited.
- Tool permissions are recorded as `local-only` because the capture processes read local prompt, policy, and skill files from the temporary capture workspace.
- The Codex runtime emitted plugin loader warnings and exposed generic Superpowers hook material during capture. That runtime material was not fixture, checker, expected-output, previous-output, or answer-key material.

The actual-output validator checks only the fixture ids listed in `fixture-ids.json` when run against this live root.

Validate with:

```bash
python3 scripts/check_workflow_passport_fixtures.py \
  --fixtures tests/skill_evals/workflow_passports/fixtures.json \
  --actual-output-root tests/skill_evals/workflow_passports/live_pilot_v1/outputs
```
