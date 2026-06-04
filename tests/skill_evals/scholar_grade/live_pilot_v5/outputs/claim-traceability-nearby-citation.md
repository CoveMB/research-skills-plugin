# Claim traceability graph

## Source basis

Source access level: `controlled-packet`.

Only the visible packet was used:
- Draft sentence: “Dashboard adoption reduced congestion in all pilot cities. [Source A]”
- Source note A: “The city launched a public dashboard in 2021.”
- Packet-stated missing material: congestion reduction evidence, all-pilot-cities evidence, and direct trace from Source A to the stronger claim.

## What I can verify

The draft makes a strong causal and universal claim: dashboard adoption reduced congestion in all pilot cities.

Source note A only supports a narrower factual claim: a city launched a public dashboard in 2021.

The nearby citation `[Source A]` does not, by itself, prove support for reduced congestion, adoption effects, causality, or all pilot cities.

## What remains uncertain

It remains unknown whether congestion actually declined, whether any decline was caused by dashboard adoption, whether the pattern held in all pilot cities, and whether Source A contains fuller evidence outside the provided source note.

Verification is unavailable from the supplied material; this is not the same as verification failed against the underlying source.

## User verification needed

Provide or check a source note, citation, and locator that directly supports:
- congestion reduction,
- the full set of pilot cities,
- the causal link between dashboard adoption and congestion reduction,
- any passage-specific or quantitative evidence behind the claim.

## Traceability table

| Claim ID | Claim text | Type | Ledger / source note pointer | Citation / citekey | Locator need | Verification status | Missing link | Repair action |
|---|---|---|---|---|---|---|---|---|
| TEMP-001 | Dashboard adoption reduced congestion in all pilot cities. | Causal outcome claim; universal scope claim | Source note A: “The city launched a public dashboard in 2021.” | `[Source A]` | Required; missing | Unsupported in provided material; nearby citation only supports dashboard launch, not the stronger claim | Missing congestion evidence, all-cities evidence, causal trace, and locator | Add a source note and locator that directly support the stronger claim, or revise to the supported narrower claim: “The city launched a public dashboard in 2021.” |

## Orphan claims

- `TEMP-001` is an evidentiary orphan in the supplied packet. It has a nearby citation, but the provided source note does not support the stronger claim.

## Claims with nearby citations but no proven support

- `TEMP-001`: `[Source A]` appears near the claim, but Source note A only establishes dashboard launch in 2021. It does not establish reduced congestion, causality, or all pilot cities.

## Optional graph notation

```text
TEMP-001 --nearby citation--> Source A
Source A --supports in packet--> dashboard launched in 2021
Source A --does not support in packet--> reduced congestion in all pilot cities
```

## Repair priorities

1. Add a direct source note and locator for congestion reduction.
2. Add evidence that the reduction occurred in all pilot cities.
3. Add evidence for causality, not just dashboard launch.
4. If those links are unavailable, narrow or remove the claim.

## Limits / failure risks

This audit is limited to the controlled packet. The underlying Source A may contain more information, but that cannot be verified here. The main traceability risk is treating citation proximity as proof of support.