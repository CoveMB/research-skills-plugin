# Scholarly integrity gate

## Source basis

Controlled packet only. The visible packet includes a draft Methods sentence claiming 20 training epochs, a stratified sample of 4,000 documents, and de-duplication, but the run config, preprocessing log, and dataset manifest are absent.

## What I can verify

- The draft Methods sentence makes specific claims about sample size, preprocessing, and model setting.
- No run config is attached.
- No preprocessing log is attached.
- No dataset manifest is attached.

## What remains uncertain

- Whether the sample size was actually 4,000 documents.
- Whether the sample was stratified.
- Whether de-duplication occurred.
- Whether training ran for 20 epochs.
- Which dataset and configuration produced the stated method details.

## User verification needed

Provide the dataset manifest, preprocessing log, and run configuration before keeping these method details.

## Workflow stage under review

Result-bearing methods section with specific computational or data-processing claims.

## Integrity checks

| Check | Verdict | Evidence visible | Risk | Required repair | Human checkpoint |
|---|---|---|---|---|---|
| Sample size provenance | INSUFFICIENT EVIDENCE | Draft says 4,000 documents; no dataset manifest | Sample size may be fabricated or stale | Attach dataset manifest or sampling record | Human must verify sample provenance |
| Stratification claim | INSUFFICIENT EVIDENCE | Draft says stratified sample; no sampling log | Stratification may not have occurred | Provide sampling procedure and strata record | Human must approve method wording |
| De-duplication claim | INSUFFICIENT EVIDENCE | Draft says after de-duplication; no preprocessing log | Preprocessing may be invented or undocumented | Attach preprocessing log | Human must verify de-duplication evidence |
| Training configuration | INSUFFICIENT EVIDENCE | Draft says 20 epochs; no run config | Model setting may be fabricated or from a different run | Attach run config | Human must verify configuration |

## Gate decision

Hold. The Methods sentence should not be used in its current form because the packet lacks run config, preprocessing evidence, and dataset provenance.

## OVERRIDDEN decisions, if any

None visible.

## Repair priorities

1. Recover or recreate the dataset manifest.
2. Attach the preprocessing log.
3. Attach the training run configuration.
4. Revise the Methods sentence to match only verified records.

## Limits / failure risks

This gate does not validate the method. It identifies missing provenance needed before the method claims can be treated as scholar-grade.
