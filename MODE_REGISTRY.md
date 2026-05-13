# Mode registry

Book workflow modes for this package.

Last updated: 2026-05-12

Use `docs/ROUTING_MATRIX.md` for canonical skill-routing choices.

## Core pipeline modes

| Mode | Primary skill | Output | Oversight | Triggers |
|---|---|---|---|---|
| `accessibility-companion` | `dyslexia-research-companion` | Low-load route, cleaned structure, ambiguity table, or next action for mixed cases | Medium | "mixed accessibility bottleneck", "unclear accessibility route", "dictation plus reading load", "spelling ambiguity plus rough notes" |
| `dictation-notes` | `dictation-to-research-notes` | Cleaned research notes with claims, questions, evidence needs, ambiguities, and next actions | Medium | "dictated notes", "voice memo", "speech-to-text", "transcript", "spoken fragments" |
| `reading-load` | `reading-load-reducer` | Read/skim/park/skip triage and close-reading targets | Medium | "reading fatigue", "too much to read", "skim", "read closely", "source triage" |
| `accessible-prose-repair` | `dyslexia-friendly-prose-editor` | Meaning-preserving prose repair with ambiguity and evidence flags | Medium | "spelling repair", "grammar cleanup", "sentence boundaries", "dysorthographic", "typo-heavy prose" |
| `research-route` | `research-intent-router` | Research intent route; non-contract routing output | Medium | "start research", "what skill should I use", "route this research task", unclear research request |
| `research-route-normal` | `research-intent-router` | Plan-first research route; non-contract routing output | Medium | "research normal mode", "normal research mode", "plan first" |
| `research-route-deep` | `research-intent-router` | Deep research route with lookup attempt; non-contract routing output | High | "research deep mode", "deep research mode", "deep lookup by default" |
| `orchestrate` | `research-book-orchestrator` | Staged workflow plan | Very High | "full book workflow", "where should I start", "plan my research book" |
| `agenda` | `scholarly-research-agenda` | Book Research Agenda | Very High | "book idea", "research question", "scope", "contribution" |
| `source-discovery` | `systematic-source-discovery` | Source Discovery Log | High | "find sources", "search strategy", "source plan" |
| `discovery-dedupe` | `discovery-runner-deduper` | Candidate Matrix and Search-Log Update | High | "dedupe candidates", "screen search results", "CSV", "BIB", "RIS" |
| `source-note` | `annotation-to-source-note` | Source Note | High | "annotations", "PDF highlights", "Zotero notes", "source notes" |
| `extraction-table` | `extraction-table-builder` | Extraction Table or Source Matrix | High | "extraction table", "source matrix", "compare sources" |
| `literature-map` | `literature-review-mapper` | Literature Map | High | "map literature", "schools of thought", "debates", "gaps" |
| `argument-architecture` | `argument-architecture` | Thesis Tree | High | "thesis tree", "argument structure", "book-level argument" |
| `counterargument-review` | `counterargument-peer-review` | Peer-Review Style Critique | High | "challenge thesis", "strong objections", "peer review" |
| `chapter-architecture` | `chapter-architecture` | Chapter Brief | High | "chapter outline", "chapter structure", "chapter logic" |
| `claim-ledger` | `claim-evidence-ledger` | Claim-Evidence Ledger | High | "audit claims", "evidence status", "overclaiming" |
| `claim-traceability` | `claim-traceability-graph` | Claim Traceability Graph | High | "trace claims", "evidence chain", "orphan claims", "locators" |
| `citation-audit` | `citation-integrity-auditor` | Citation Integrity Audit | High | "check citations", "unsupported claims", "quote verification" |
| `figure-table-audit` | `figure-table-integrity-auditor` | Figure Table Integrity Audit | High | "figure audit", "table audit", "caption", "axis", "data provenance", "duplicate visual" |
| `integrity-gate` | `scholarly-integrity-gate` | Scholarly Integrity Audit | Very High | "integrity gate", "AI research failure", "methodology fabrication", "implementation bug", "frame-lock" |
| `ai-human-log` | `ai-human-workflow-log` | AI Human Workflow Log | High | "AI-use disclosure", "human checkpoint", "tool use", "override reason" |
| `release-audit` | `rights-privacy-release-auditor` | Rights Privacy Release Audit | High | "release audit", "share externally", "privacy", "copyright", "license" |
| `continuity-audit` | `manuscript-continuity-editor` | Continuity Review | High | "whole manuscript", "concept drift", "contradictions", "repetition" |
| `proposal` | `book-proposal-scholarship` | Research Book Proposal | High | "book proposal", "press proposal", "comparable titles" |
| `comps-verification` | `book-comps-verifier` | Comparable Title Verification | High | "comps", "comparable titles", "press positioning", "audience claims" |

## Automatic selection rule

`research-route` is an alias for `research-route-normal`.

Use the specific accessibility mode when ownership is clear: `dictation-notes` for spoken input, `reading-load` for dense material triage, and `accessible-prose-repair` for existing prose repair.

Start with `accessibility-companion` only when text friction blocks the user's next scholarly action and the smaller accessibility skill is unclear or several bottlenecks overlap.

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
