# Mode registry

Book workflow modes across the plugin.

Last updated: 2026-05-12

## Core pipeline modes

| Mode | Primary skill | Output | Oversight | Triggers |
|---|---|---|---|---|
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
