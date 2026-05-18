# Additive Live Pilot

This directory holds the original small live-capture pilot. It must stay additive: deterministic reference outputs, manifests, and scores under `tests/skill_evals/scholar_grade/outputs`, `manifests`, and `scores` remain intact, and newer pilot runs should use a fresh additive root.

The pilot fixture subset is listed in `fixture-ids.json`. It focuses on high-risk failures: overclaiming, private-text boundaries, quote locator fabrication, compact-output blocker loss, meaning-changing prose repair, missing AI workflow verification, hallucinated results, and fabricated methodology details.

Generate operator prompt packets for just this subset:

```bash
python3 tests/skill_evals/scholar_grade/live_capture_protocol.py --fixtures tests/skill_evals/scholar_grade/fixtures.json --root . --out-dir /tmp/scholar-live-pilot-protocol --fixture-id unsupported-causal-claim --fixture-id private-manuscript-search-consent --fixture-id quote-without-locator --fixture-id compact-output-hides-blocker --fixture-id prose-edit-changes-meaning --fixture-id ai-workflow-missing-verification-record --fixture-id hallucinated-result-without-run-log --fixture-id methodology-fabrication-run-config
```

Record each completed live capture under this directory with `run_live_capture.py --out-root tests/skill_evals/scholar_grade/live_pilot`. Review scores must be completed under `live_pilot/scores` before validation.

Report only the original pilot subset:

```bash
python3 scripts/run_package_checks.py --scope live-pilot
```

`--scope live-pilot` emits a calibration report and exits successfully even when the historical capture set is not ready. Use the report actions to decide whether a newer pilot run is needed.

Generate a calibration report at any point:

```bash
python3 tests/skill_evals/scholar_grade/live_pilot_calibration.py --format markdown
```

The calibration report compares recorded pilot review scores to deterministic baseline scores and emits actions for missing captures, validation failures, or score regressions. Use `--strict` after the pilot artifacts are complete.

After skill instructions change, do not overwrite the original blind captures. The manifest skill hash should identify the skill text used at capture time. Record the next pilot run in a new additive root with a fresh operator or session that has not read the hidden answer keys.
