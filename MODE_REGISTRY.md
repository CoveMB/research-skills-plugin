# Mode registry

Book workflow modes for this package.

Last updated: 2026-05-12

Use `docs/ROUTING_MATRIX.md` for canonical skill-routing choices.

## Core pipeline modes

| Mode | Primary skill | Output | Oversight | Triggers |
|---|---|---|---|---|
| `research-route` | `research-intent-router` | Research intent route; non-contract routing output | Medium | "start research", "what skill should I use", "route this research task", unclear research request |
| `research-route-normal` | `research-intent-router` | Plan-first research route; non-contract routing output | Medium | "research normal mode", "normal research mode", "plan first" |
| `research-route-deep` | `research-intent-router` | Deep research route with lookup attempt; non-contract routing output | High | "research deep mode", "deep research mode", "deep lookup by default" |
| `orchestrate` | `research-book-orchestrator` | Staged workflow plan | Very High | "full book workflow", "where should I start", "plan my research book" |
| `agenda` | `scholarly-research-agenda` | Book Research Agenda | Very High | "book idea", "research question", "scope", "contribution" |
| `source-discovery` | `systematic-source-discovery` | Source Discovery Log | High | "find sources", "search strategy", "source plan" |
| `literature-map` | `literature-review-mapper` | Literature Map | High | "map literature", "schools of thought", "debates", "gaps" |
| `argument-architecture` | `argument-architecture` | Thesis Tree | High | "thesis tree", "argument structure", "book-level argument" |
| `counterargument-review` | `counterargument-peer-review` | Peer-Review Style Critique | High | "challenge thesis", "strong objections", "peer review" |
| `chapter-architecture` | `chapter-architecture` | Chapter Brief | High | "chapter outline", "chapter structure", "chapter logic" |
| `claim-ledger` | `claim-evidence-ledger` | Claim-Evidence Ledger | High | "audit claims", "evidence status", "overclaiming" |
| `citation-audit` | `citation-integrity-auditor` | Citation Integrity Audit | High | "check citations", "unsupported claims", "quote verification" |
| `continuity-audit` | `manuscript-continuity-editor` | Continuity Review | High | "whole manuscript", "concept drift", "contradictions", "repetition" |
| `proposal` | `book-proposal-scholarship` | Research Book Proposal | High | "book proposal", "press proposal", "comparable titles" |

## Automatic selection rule

`research-route` is an alias for `research-route-normal`.

Start with `research-route` when a prompt involves scholarly research but the best specialist skill is unclear. The router should use light routing first, then allow deep source lookup only when it materially strengthens evidence quality: source finding or checking is requested, source existence or metadata is central, citation/page/quote verification is requested, current facts matter, or a high-risk claim would otherwise be unsupported.

Use `research-route-normal` for normal mode. Normal mode is the default and plans first.

Use `research-route-deep` for deep mode. Deep mode always attempts lookup after routing, but it still marks missing tools, missing full text, and unavailable sources as unverified.

## Support modes

| Mode | Primary skill | Output | Oversight | Triggers |
|---|---|---|---|---|
| `annotated-bibliography` | `annotated-bibliography-builder` | Annotated Bibliography | Medium | "annotate sources", "source notes", "bibliography" |
| `source-audit` | `methodology-source-auditor` | Source Methodology Audit | Medium | "evaluate source", "credibility", "method" |
| `case-study` | `case-study-integration` | Case Study Integration Plan | Medium | "case study", "counter-case", "example integration" |
| `prose-edit` | `scholarly-prose-editor` | Revised Passage | Medium | "edit prose", "clarity", "research style" |

## Artifact types

| Artifact type | Produced by |
|---|---|
| `book_research_agenda` | `agenda` |
| `source_discovery_log` | `source-discovery` |
| `literature_map` | `literature-map` |
| `thesis_tree` | `argument-architecture` |
| `chapter_brief` | `chapter-architecture` |
| `claim_evidence_ledger` | `claim-ledger` |
| `continuity_review` | `continuity-audit` |
| `book_proposal` | `proposal` |

## Oversight levels

| Level | Meaning |
|---|---|
| Very High | User must confirm the intellectual object, scope, and next stage |
| High | User confirms major argument, evidence, or manuscript structure decisions |
| Medium | Structured output with limited decision points |
| Low | Mechanical formatting or conversion only; currently no low-oversight mode |
