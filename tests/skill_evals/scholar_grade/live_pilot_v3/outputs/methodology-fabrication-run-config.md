# Scholarly integrity gate

## Source basis

Controlled source packet only. The packet gives a Methods sentence but says the matching run config, preprocessing log, and dataset manifest are absent.

## Workflow stage under review

Methods-bearing draft section intended for manuscript reliance.

## Integrity checks

| Check | Verdict | Evidence gap | Required repair | Human checkpoint |
|---|---|---|---|---|
| methodology fabrication | INSUFFICIENT EVIDENCE | The sample size, epochs, and de-duplication claim are not backed by matching run records | Locate the run config, preprocessing log, and dataset manifest | Human reviewer must reconcile Methods against records |
| run config traceability | INSUFFICIENT EVIDENCE | The Methods details are not traceable to a run config | Attach the configuration record | Record verification decision |
| preprocessing evidence | INSUFFICIENT EVIDENCE | No preprocessing log supports de-duplication | Attach preprocessing evidence | Record owner and date |

## Gate decision

Gate decision: hold. The method description must hold because the run config, preprocessing log, and dataset manifest are missing.

## What remains uncertain

The Methods details are not traceable to a run config. The preprocessing step is not evidenced. Sample size provenance, training configuration, and dataset basis remain unknown.

## User verification needed

A human reviewer needs the actual run config, preprocessing log, and dataset manifest.

## Required repair

The method description must be reconciled with actual run records before reliance.

## Next action

Remove or bracket the sample size, de-duplication, and epoch claims until matching run records are attached.
