# Workflow Passport Live Pilot v1 Results

Date: 2026-06-04

This v1 root adds blind live captures for four workflow-passport preservation routes:

- `extraction-to-literature-map-preserves-passport`
- `claim-ledger-to-citation-audit-preserves-passport`
- `book-proposal-to-comps-preserves-passport`
- `workflow-log-to-release-audit-preserves-passport`

## Capture Summary

- Raw captures completed: 4 / 4.
- Capture interface: `codex-cli`.
- Capture model: `gpt-5.5`.
- Capture mode recorded in manifests: `manual-live-capture`.
- Capture operator recorded in manifests: `fresh codex exec blind process`.
- Capture prompt basis: live prompt packet, embedded input artifact JSON, `docs/policy/PROCESS_PASSPORT.md`, and the target downstream skill instructions.
- Fixture JSON, expected output artifacts, forbidden behavior lists, checker code, previous outputs, and answer-key material were excluded from capture prompts.
- External lookup, browsing, upload, and network access were not permitted or used.
- No private material was submitted to external tools or services.
- Raw captured outputs were not edited.
- Codex runtime startup warnings and generic hook material were visible during capture but were not fixture, checker, expected-output, previous-output, or answer-key material.

## Artifact Summary

- Outputs present: 4 / 4.
- Manifests present: 4 / 4.
- Actual-output validation errors: none.

## Validation Result

Command:

```bash
python3 scripts/check_workflow_passport_fixtures.py \
  --fixtures tests/skill_evals/workflow_passports/fixtures.json \
  --actual-output-root tests/skill_evals/workflow_passports/live_pilot_v1/outputs
```

Current result: `OK: workflow passport fixtures are valid.`

## Coverage Added

Newly live-tested behavior:

- Downstream skills preserve inherited `unresolved_risks` and `handoff_limits`.
- Downstream skills do not upgrade citation-only, abstract-only, no-full-text, partial, or unverified source access to verified status.
- Downstream skills keep human verification needed before downstream reliance.
- Rights, privacy, citation, market, and literature-map outputs keep release, locator, source-support, and corpus limits visible.

## Deferred Fixtures

The following deterministic workflow-passport fixtures remain outside this first live root:

- `source-discovery-to-extraction-preserves-passport`
- `literature-map-to-argument-preserves-passport`
- `argument-to-claim-ledger-preserves-passport`
- `chapter-brief-to-integrity-gate-preserves-passport`

## Remaining Risks

- Live captures validate passport preservation behavior for synthetic fixtures, not real-world source truth.
- The captures used a local Codex runtime that emitted plugin startup warnings and generic hook content; manifests record this as runtime context.
