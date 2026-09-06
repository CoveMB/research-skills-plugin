# figure-table-integrity-auditor

## What it does

Use this skill to audit figures, tables, charts, screenshots, images, maps, and visual evidence before they support scholarly claims.

It checks data provenance, captions, axes, duplicate visual risk, source licensing, and claim-support limits.

## When to use it

Use it before publication, external sharing, release review, or citation audit when a figure or table carries factual, empirical, comparative, or quantitative claims.

## Good inputs

- Figure/table IDs, captions, charts, screenshots, images, or table values.
- Data files, extraction tables, scripts, notebooks, run logs, or source pointers.
- The manuscript claim each object is meant to support.

## Example requests

```text
Audit these charts for data provenance, axis accuracy, and caption support.
```

```text
Check whether these tables and screenshots are safe to use as evidence.
```

## Typical output

Expect a figure/table audit table, provenance gaps, caption and axis issues, duplicate visual risks, rights/release risks, verdicts, repair actions, and a risk-gated next step when useful. Ask for compact output when you want only the visual/table blockers that change manuscript, citation, or release action. Compact output should include `How to use this result: BLOCKER SUMMARY - This lists visible figure/table blockers only; do not treat it as full data, rights, or claim clearance.` It changes output shape, not route selection or evidence requirements.

## Operational boundaries

Follow `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`.

When a figure/table provenance export exists, run or recommend `python3 scripts/check_figure_table_provenance.py --input path/to/figure-table-provenance.json` before assigning readiness. Treat a clean helper result as structural provenance only, not data-value, rights, or claim-support clearance.

## Best next steps

After this skill, use `rights-privacy-release-auditor` for external-sharing blockers or `citation-integrity-auditor` when the visual/table claim also needs citation-source fit checked.
