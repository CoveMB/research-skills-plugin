# Skill index

Use this file when you already have a sense of the work needed and want the right skill. Use `MODE_REGISTRY.md` for route names and artifact outputs. Use `docs/ROUTING_MATRIX.md` for canonical automatic routing.

| Skill folder | Display name | When to use |
|---|---|---|
| `research-intent-router` | Research Intent Router | Auto-detect scholarly research intent, choose the smallest useful research-book skill, and gate deep source lookup so it only runs when it materially improves evidence quality. |
| `research-book-orchestrator` | Research Book Orchestrator | Coordinate a full research nonfiction or research book workflow. Use for project planning, routing tasks across research agenda, source discovery, literature review, argument design, chapter work, evidence ledgers, citation audits, and manuscript revision. |
| `scholarly-research-agenda` | Research Agenda | Turn a broad research book idea into precise research questions, scope boundaries, contribution claims, key terms, evidence needs, and an initial research agenda. Use before source gathering or outlining. |
| `systematic-source-discovery` | Systematic Source Discovery | Design rigorous research source-discovery strategies, keyword sets, database searches, citation-chaining plans, primary-source targets, and search logs for research books and literature reviews. |
| `literature-review-mapper` | Literature Review Mapper | Map a research literature into schools of thought, debates, consensus, intellectual genealogy, methods, gaps, and how each cluster supports or challenges a book thesis. |
| `annotated-bibliography-builder` | Annotated Bibliography Builder | Create research-grade annotated bibliographies that summarize argument, method, evidence, relevance, limitations, key terms, and chapter placement for research book sources. |
| `methodology-source-auditor` | Methodology Source Auditor | Evaluate source credibility, methodology, evidence quality, bias, generalizability, and what each source can or cannot support in a research manuscript. |
| `claim-evidence-ledger` | Claim Evidence Ledger | Extract major claims from a research draft and classify claim type, evidence status, citation need, confidence, overclaiming risk, and safer wording. |
| `argument-architecture` | Argument Architecture | Build a research book-level thesis tree with claims, warrants, evidence, assumptions, counterarguments, chapter sequence, and argumentative dependencies. |
| `counterargument-peer-review` | Counterargument Peer Review | Simulate rigorous research peer review by generating strong objections, rival explanations, missing literatures, positional blind spots, and thesis revisions. |
| `chapter-architecture` | Chapter Architecture | Design research nonfiction chapters with purpose, central question, main claim, concept definitions, evidence placement, counterarguments, transitions, and revision priorities. |
| `scholarly-prose-editor` | Research Prose Editor | Edit research nonfiction prose for clarity, precision, structure, rhythm, readability, and authorial voice while preserving nuance and avoiding formulaic style. |
| `citation-integrity-auditor` | Citation Integrity Auditor | Audit research drafts for citation accuracy, unsupported claims, quote integrity, page-number needs, fabricated-reference risk, source-claim mismatch, and bibliography problems. |
| `manuscript-continuity-editor` | Manuscript Continuity Editor | Review multiple chapters or a whole manuscript for thesis coherence, repetition, contradictions, concept tracking, tone consistency, chapter order, and revision priorities. |
| `case-study-integration` | Case Study Integration | Select, compare, and integrate case studies into research arguments while avoiding cherry-picking, weak analogy, anecdotal overreach, and unsupported generalization. |
| `book-proposal-scholarship` | Book Proposal Scholarship | Develop a serious research nonfiction book proposal with thesis, contribution, audience, market/field positioning, chapter summaries, comparable titles, and sample-material plan. |

## Core set

For a serious research book, start with:

1. `research-intent-router`
2. `scholarly-research-agenda`
3. `systematic-source-discovery`
4. `literature-review-mapper`
5. `argument-architecture`
6. `claim-evidence-ledger`
7. `counterargument-peer-review`
8. `citation-integrity-auditor`

These catch the common failures: vague scope, weak sources, missing literature context, unsupported claims, one-sided argument, and citation errors.

## Automatic selection policy

Use `research-intent-router` as the light first pass when a prompt could match several research skills. It should classify intent, artifact stage, source access, and risk level, then choose the smallest useful skill or short skill sequence. It should not run live or deep source lookup unless the user asks to find or check sources, source existence or metadata is central, quote/page/citation verification is requested, a claim depends on current facts, or a high-risk claim would otherwise be unsupported.

Router modes: `research-route-normal` and `research-route-deep`. See `MODE_REGISTRY.md` for mode behavior.

Suggested next steps are optional and risk-gated. They should appear only when one follow-on skill reduces a named scholarly risk; the shared policy lives in `docs/AUTO_SELECTION_GUARDRAILS.md`, with route gates in `docs/ROUTING_MATRIX.md`.

## Later-stage manuscript set

Use these once chapters exist:

1. `chapter-architecture`
2. `scholarly-prose-editor`
3. `manuscript-continuity-editor`
4. `book-proposal-scholarship`

## Case and evidence set

Use these when examples and source quality matter:

1. `case-study-integration`
2. `methodology-source-auditor`
3. `annotated-bibliography-builder`
