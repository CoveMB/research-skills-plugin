# Additive Live Pilot v2

This directory records the second additive live-capture pilot. It must stay additive: deterministic reference outputs, manifests, and scores under `tests/skill_evals/scholar_grade/outputs`, `manifests`, and `scores` remain the default package gate. The original `live_pilot` directory must not be overwritten by this run.

The pilot fixture subset is listed in `fixture-ids.json`. It focuses on high-risk failures: overclaiming, private-text boundaries, quote locator fabrication, compact-output blocker loss, meaning-changing prose repair, missing AI workflow verification, hallucinated results, fabricated methodology details, evidence-chain failures, discovery dedupe, figure/table provenance, consensus overstatement, mixed-evidence annotation, extraction gaps, and stale comparable-title claims.

Generate operator prompt packets for just this subset:

```bash
python3 tests/skill_evals/scholar_grade/live_capture_protocol.py --fixtures tests/skill_evals/scholar_grade/fixtures.json --root . --out-dir /tmp/scholar-live-pilot-v2-protocol --fixture-id unsupported-causal-claim --fixture-id private-manuscript-search-consent --fixture-id quote-without-locator --fixture-id compact-output-hides-blocker --fixture-id prose-edit-changes-meaning --fixture-id ai-workflow-missing-verification-record --fixture-id hallucinated-result-without-run-log --fixture-id methodology-fabrication-run-config --fixture-id claim-traceability-nearby-citation --fixture-id discovery-dedupe-fuzzy-export --fixture-id chart-without-data-provenance --fixture-id literature-map-overstates-consensus --fixture-id annotation-source-note-mixed-evidence --fixture-id extraction-table-uneven-source-notes --fixture-id book-comps-stale-mismatch
```

Record each completed live capture under this directory with `run_live_capture.py --out-root tests/skill_evals/scholar_grade/live_pilot_v2`. Review scores must be completed under `live_pilot_v2/scores` before validation.

Validate only this v2 pilot subset:

```bash
python3 tests/skill_evals/scholar_grade/live_pilot_calibration.py --pilot-plan tests/skill_evals/scholar_grade/live_pilot_v2/fixture-ids.json --live-root tests/skill_evals/scholar_grade/live_pilot_v2 --format markdown --strict
```

The calibration report compares recorded v2 review scores to deterministic baseline scores and emits actions for missing captures, validation failures, or score regressions.

After skill instructions change, do not overwrite these blind captures. Record the next pilot run in a new additive root with a fresh operator or session that has not read the hidden answer keys.
