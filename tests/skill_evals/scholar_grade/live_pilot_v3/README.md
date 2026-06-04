# Additive Live Pilot v3

This directory is the current completed additive live-capture root after skill instruction changes made the corresponding `live_pilot_v2` manifests stale.

The v3 subset in `fixture-ids.json` contains only the v2 fixtures whose recorded `skill_file_sha256` no longer matches the current skill file. The unchanged v2 fixtures remain historical live-capture evidence and do not need to be copied into this root.

Completed manual-live-capture artifacts are checked in under `prompts/`, `outputs/`, `manifests/`, `score-templates/`, and `scores/`. Generated operator packets and manifest, score, and trace templates remain checked in under `capture_protocol/` as setup artifacts for future recapture.

Generate operator prompt packets for just this subset into a temporary directory:

```bash
python3 tests/skill_evals/scholar_grade/live_capture_protocol.py --fixtures tests/skill_evals/scholar_grade/fixtures.json --root . --out-dir /tmp/scholar-live-pilot-v3-protocol --fixture-id unsupported-causal-claim --fixture-id private-manuscript-search-consent --fixture-id quote-without-locator --fixture-id chart-without-data-provenance --fixture-id prose-edit-changes-meaning --fixture-id literature-map-overstates-consensus --fixture-id hallucinated-result-without-run-log --fixture-id methodology-fabrication-run-config --fixture-id ai-workflow-missing-verification-record --fixture-id extraction-table-uneven-source-notes
```

Record replacement live captures under this directory with `run_live_capture.py --out-root tests/skill_evals/scholar_grade/live_pilot_v3`. Use a fresh operator or session that has not read hidden answer keys. Review scores must be completed under `live_pilot_v3/scores` before strict validation.

Inspect the planned capture paths before recording:

```bash
python3 tests/skill_evals/scholar_grade/run_live_capture.py --fixtures tests/skill_evals/scholar_grade/fixtures.json --out-root tests/skill_evals/scholar_grade/live_pilot_v3 --fixture-id unsupported-causal-claim --fixture-id private-manuscript-search-consent --fixture-id quote-without-locator --fixture-id chart-without-data-provenance --fixture-id prose-edit-changes-meaning --fixture-id literature-map-overstates-consensus --fixture-id hallucinated-result-without-run-log --fixture-id methodology-fabrication-run-config --fixture-id ai-workflow-missing-verification-record --fixture-id extraction-table-uneven-source-notes --dry-run
```

Validate v3 readiness:

```bash
python3 tests/skill_evals/scholar_grade/live_pilot_calibration.py --pilot-plan tests/skill_evals/scholar_grade/live_pilot_v3/fixture-ids.json --live-root tests/skill_evals/scholar_grade/live_pilot_v3 --format markdown --strict
```

The expected strict status is `Ready: true` with no actions or regressions.
