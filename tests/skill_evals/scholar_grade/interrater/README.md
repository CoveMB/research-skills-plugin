# Inter-rater and live-run stability reports

This directory is an additive reviewer-panel layer for scholar-grade evaluations. It does not replace expert review, source-truth review, or the existing deterministic fixture harness.

Use the existing score-file shape for reviewer panels:

- `reviewer_A/<fixture-id>.json`: first independent reviewer score.
- `reviewer_B/<fixture-id>.json`: second independent reviewer score.
- `adjudicated/<fixture-id>.json`: adjudicated decision when reviewers disagree.
- `agreement_reports/`: optional saved JSON or Markdown reports generated from `report_interrater.py`.

Do not invent reviewer scores. Add files here only when a human reviewer has actually reviewed the captured output bound by `reviewed_output_sha256`.

Run the diagnostic report:

```bash
python3 tests/skill_evals/scholar_grade/interrater/report_interrater.py --format markdown
```

The report lists fixtures with only one reviewer, hard-fail disagreement, per-dimension score differences, average difference by dimension, missing adjudication where disagreement exists, and critical dimensions below threshold for any reviewer.

The same command also summarizes live-run stability from live capture roots with `manifests/` and `scores/`. It reports run count, hard-fail count, hard-fail rate, worst dimension score, average dimension score, and optional fabrication/unsupported-claim/privacy counts when those fields are present.

Average scores must not hide hard fails. For citation, privacy, fabrication, locator, rights, and meaning-preservation risks, worst-case behavior matters more than the average score.

`--strict` is available for completed panels, but it is intentionally not required for existing fixtures. Missing reviewer panels should not block normal full validation.
