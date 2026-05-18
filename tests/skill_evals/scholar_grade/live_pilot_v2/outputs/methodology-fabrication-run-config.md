# Scholarly integrity gate

## Source basis

Visible synthetic methods packet only. The packet provides a draft methods sentence but no run config, preprocessing log, or dataset manifest.

## Gate decision: hold

Failure mode: methodology fabrication.

The methods-bearing claim must hold because the named sample size, preprocessing step, and training setting are not backed by matching run records.

The method description must be reconciled with actual run records before reliance.

## What remains uncertain

Sample size provenance, stratification, de-duplication evidence, dataset manifest, training configuration, and the claimed 20 epochs are all unverified.

## User verification needed

The user must provide the dataset manifest, preprocessing log, run config, and any training record that supports the sample size, de-duplication step, stratified sampling, and epoch count.

## Integrity checks

| Check | Verdict | Blocker or evidence gap | Required repair | Human checkpoint |
|---|---|---|---|---|
| Sample size provenance | INSUFFICIENT EVIDENCE | No dataset manifest or sample record supports 4,000 documents | Attach manifest or sampling record | Human verifies sample count and sampling method |
| Preprocessing evidence | INSUFFICIENT EVIDENCE | No preprocessing log supports de-duplication | Attach preprocessing log and de-duplication criteria | Human verifies preprocessing actually occurred |
| Training configuration | INSUFFICIENT EVIDENCE | No run config supports 20 epochs | Attach run config or training log | Human verifies method sentence against run record |
| Manuscript methods reliance | SUSPECTED | Draft presents precise methods without provenance | Hold or rewrite as unverified until records match | Human decides whether to remove, qualify, or repair the method claim |

## Required repair

Do not use the methods sentence as a settled methods description until the run config, preprocessing evidence, and dataset manifest are supplied and reconciled with the draft.

## Next action

Gather the actual run records and update the Methods section to match only documented configuration and preprocessing facts.
