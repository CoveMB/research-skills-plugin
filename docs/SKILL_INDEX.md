# Skill index

Use this file when you already have a sense of the work needed and want the right skill. Use `MODE_REGISTRY.md` for route names and artifact outputs. Use `docs/ROUTING_MATRIX.md` for canonical automatic routing.

| Skill folder | Display name | When to use |
|---|---|---|
| `dyslexia-research-companion` | Dyslexia Research Companion | Route mixed or unclear accessibility bottlenecks for dyslexic, dysorthographic, dictation-heavy, or reading-fatigued scholarly authors when no smaller accessibility skill clearly owns the task. |
| `dictation-to-research-notes` | Dictation to Research Notes | Turn dictated research thoughts, voice transcripts, speech-to-text output, meeting notes, or rambling spoken fragments into structured scholarly notes, claims, questions, evidence needs, ambiguities, and next actions without changing meaning. |
| `reading-load-reducer` | Reading Load Reducer | Reduce reading burden by turning dense articles, source excerpts, search results, bibliographies, chapter drafts, or long notes into skim-read-skip triage, close-reading targets, extraction priorities, evidence needs, and next actions. |
| `dyslexia-friendly-prose-editor` | Dyslexia-Friendly Prose Editor | Repair spelling, grammar, sentence boundaries, punctuation, and readability in scholarly prose while preserving meaning, authorial voice, uncertainty, evidence limits, and a compact change summary. |
| `research-intent-router` | Research Intent Router | Auto-detect scholarly research intent, choose the smallest useful research-book skill, and gate deep source lookup so it only runs when it materially improves evidence quality. |
| `research-book-orchestrator` | Research Book Orchestrator | Coordinate a full research nonfiction or research book workflow. Use for project planning, routing tasks across research agenda, source discovery, literature review, argument design, chapter work, evidence ledgers, citation audits, and manuscript revision. |
| `scholarly-research-agenda` | Research Agenda | Turn a broad research book idea into precise research questions, scope boundaries, contribution claims, key terms, evidence needs, and an initial research agenda. Use before source gathering or outlining. |
| `systematic-source-discovery` | Systematic Source Discovery | Design source-discovery strategies, keyword sets, database searches, citation-chaining plans, primary-source targets, and search logs for research books and literature reviews. |
| `discovery-runner-deduper` | Discovery Runner Deduper | Process academic index exports, library catalogue exports, bibliography exports, tabular files, or pasted candidate source records into deduped screening records, duplicate clusters, keep/reject logs, and search-log updates. |
| `annotation-to-source-note` | Annotation to Source Note | Convert reference-manager notes, document highlights, manual annotations, excerpts, or reading notes into source-bound notes with quote, paraphrase, metadata, and locator gaps preserved. |
| `extraction-table-builder` | Extraction Table Builder | Turn source notes, annotations, excerpts, or reading notes into extraction tables, source matrices, and comparison grids before synthesis or claim drafting. |
| `literature-review-mapper` | Literature Review Mapper | Map a research literature into schools of thought, debates, consensus, intellectual genealogy, methods, gaps, and how each cluster supports or challenges a book thesis. |
| `annotated-bibliography-builder` | Annotated Bibliography Builder | Create structured annotated bibliographies that summarize argument, method, evidence, relevance, limitations, key terms, and chapter placement for research book sources. |
| `methodology-source-auditor` | Methodology Source Auditor | Evaluate source credibility, methodology, evidence quality, bias, generalizability, and what each source can or cannot support in a research manuscript. |
| `claim-evidence-ledger` | Claim Evidence Ledger | Extract major claims from a research draft and classify claim type, evidence status, citation need, confidence, overclaiming risk, and safer wording. |
| `claim-traceability-graph` | Claim Traceability Graph | Map claims to claim IDs, source notes, citekeys, locators, evidence status, missing evidence-chain links, and repair actions. |
| `argument-architecture` | Argument Architecture | Build a research book-level thesis tree with claims, warrants, evidence, assumptions, counterarguments, chapter sequence, and argumentative dependencies. |
| `counterargument-peer-review` | Counterargument Peer Review | Run a research peer-review style critique with objections, rival explanations, missing literatures, positional blind spots, and thesis revisions. |
| `chapter-architecture` | Chapter Architecture | Design research nonfiction chapters with purpose, central question, main claim, concept definitions, evidence placement, counterarguments, transitions, and revision priorities. |
| `scholarly-prose-editor` | Research Prose Editor | Edit research nonfiction prose for clarity, precision, structure, rhythm, readability, and authorial voice while preserving nuance and avoiding formulaic style. |
| `citation-integrity-auditor` | Citation Integrity Auditor | Audit research drafts for citation accuracy, unsupported claims, quote integrity, page-number needs, fabricated-reference risk, source-claim mismatch, and bibliography problems. |
| `rights-privacy-release-auditor` | Rights Privacy Release Auditor | Audit notes, research artifacts, manuscript exports, proposal materials, and shared files for privacy, copyright, quotation, license, secret, credential, local metadata, and release risks before external sharing. |
| `manuscript-continuity-editor` | Manuscript Continuity Editor | Review multiple chapters or a whole manuscript for thesis coherence, repetition, contradictions, concept tracking, tone consistency, chapter order, and revision priorities. |
| `case-study-integration` | Case Study Integration | Select, compare, and integrate case studies into research arguments while avoiding cherry-picking, weak analogy, anecdotal overreach, and unsupported generalization. |
| `book-proposal-scholarship` | Book Proposal Scholarship | Develop a research nonfiction book proposal with thesis, contribution, audience, market/field positioning, chapter summaries, comparable titles, and sample-material plan. |
| `book-comps-verifier` | Book Comps Verifier | Verify comparable titles and positioning claims for research nonfiction proposals, press pitches, grants, audience claims, market claims, timeliness claims, and publication positioning. |

## Accessibility entry points

Use one of these before the core research workflow only when text friction blocks the next scholarly action:

1. `dictation-to-research-notes` when voice transcripts are the first bottleneck
2. `reading-load-reducer` when dense material or source volume is the first bottleneck
3. `dyslexia-friendly-prose-editor` when existing prose needs meaning-preserving repair
4. `dyslexia-research-companion` when the accessibility bottleneck is mixed or unclear

## Core research workflow

For a research book with scholarly standards, start with:

1. `research-intent-router`
2. `scholarly-research-agenda`
3. `systematic-source-discovery`
4. `annotation-to-source-note`
5. `extraction-table-builder`
6. `literature-review-mapper`
7. `argument-architecture`
8. `claim-evidence-ledger`
9. `claim-traceability-graph`
10. `counterargument-peer-review`
11. `citation-integrity-auditor`

These catch the common failures: vague scope, weak sources, missing literature context, unsupported claims, one-sided argument, and citation errors.

## Automatic selection policy

Use the smallest accessibility skill before routing when text friction blocks the user's intended claim or next action: `dictation-to-research-notes` for spoken input, `reading-load-reducer` for dense material triage, and `dyslexia-friendly-prose-editor` for existing prose repair. Use `dyslexia-research-companion` when the accessibility bottleneck is mixed or unclear.

Use `research-intent-router` as the light first pass when a prompt could match several research skills. It should classify intent, artifact stage, source access, and risk level, then choose the smallest useful skill or short skill sequence. It should not run live or deep source lookup unless the user asks to find or check sources, source existence or metadata is central, quote/page/citation verification is requested, a claim depends on current facts, or a high-risk claim would otherwise be unsupported.

Router modes: `research-route-normal` and `research-route-deep`. See `MODE_REGISTRY.md` for mode behavior.

Suggested next steps are optional and risk-gated. They should appear only when one follow-on skill reduces a named scholarly risk; the shared policy lives in `docs/AUTO_SELECTION_GUARDRAILS.md`, with route gates in `docs/ROUTING_MATRIX.md`.

## Later-stage manuscript set

Use these once chapters exist. Start with one accessibility entry point only if text friction blocks revision:

1. `dictation-to-research-notes`, `reading-load-reducer`, `dyslexia-friendly-prose-editor`, or `dyslexia-research-companion`
2. `chapter-architecture`
3. `scholarly-prose-editor`
4. `manuscript-continuity-editor`
5. `rights-privacy-release-auditor`
6. `book-proposal-scholarship`
7. `book-comps-verifier`

## Case and evidence set

Use these when examples and source quality matter:

1. `case-study-integration`
2. `methodology-source-auditor`
3. `annotated-bibliography-builder`
4. `annotation-to-source-note`
5. `extraction-table-builder`
6. `discovery-runner-deduper`
