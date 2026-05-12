# Workflow playbook

Use this playbook when you know the project stage and need the next concrete artifact. For the staged architecture, see `docs/ARCHITECTURE.md`. For route names and outputs, see `MODE_REGISTRY.md`.

## 0. Choose the smallest accessibility entry point

Prompt:

```text
Use dictation-to-research-notes. Turn this voice transcript into claims, questions, evidence needs, ambiguities, and next actions.
```

Use the smallest accessibility skill before routing when text friction makes the next scholarly action hard to see:

- `dictation-to-research-notes` for voice transcripts or speech-to-text output
- `reading-load-reducer` for dense material or source-volume triage
- `dyslexia-friendly-prose-editor` for existing prose needing meaning-preserving repair
- `dyslexia-research-companion` when the bottleneck is mixed, unclear, or explicitly requested as a wrapper

For mixed cases:

```text
Use dyslexia-research-companion. I have rough notes, dictation fragments, and dense sources. Choose the smallest low-load first step and keep ambiguities visible.
```

## 0.1. Start with the research intent router

Prompt:

```text
Use research-intent-router. I want to start research on [topic]. Classify the request, choose the smallest useful skill route, and say whether deep source lookup is needed.
```

Use `research-intent-router` to classify:

- intent: plan, discover, map, audit, draft, revise, verify, or propose
- artifact stage: idea, source list, notes, draft, chapter, manuscript, or proposal
- source access level
- scholarly risk level

Default: light routing first. Do not run live or deep source lookup unless the user asks to find or check sources, source existence or metadata is central, citation/page/quote verification is requested, current facts matter, or a high-risk claim would otherwise be unsupported.

Router modes: `research-route-normal` and `research-route-deep`. See `MODE_REGISTRY.md` for mode behavior.

## 0.2. Use the orchestrator for multi-stage work

Prompt:

```text
Use research-book-orchestrator. I am writing a research nonfiction book about [topic]. Build a staged research and writing workflow with quality gates.
```

## 1. Agenda sprint

Use `scholarly-research-agenda` to define:

- central research question
- subquestions
- contribution claim
- scope boundaries
- evidence plan

Output artifact: `research-agenda.md`.

Contract artifact type: `book_research_agenda`.

## 2. Source discovery sprint

Use `systematic-source-discovery` to create:

- search families
- Boolean queries
- search venues
- inclusion/exclusion rules
- search log

Output artifact: `search-log.md`.

Contract artifact type: `source_discovery_log`.

When a search has produced exported candidates, use `discovery-runner-deduper` before treating the results as a usable corpus. It should create candidate matrices, duplicate clusters, keep/reject logs, and search-log updates. It must keep planned searches separate from completed searches.

## 2.1. Source-note and extraction sprint

Use `annotation-to-source-note` when document highlights, reference-manager notes, excerpts, or manual reading notes need source-bound notes with quote, paraphrase, summary, interpretation, metadata, and locator gaps kept visible.

Use `extraction-table-builder` when source notes need comparable fields before synthesis. It should create source-level rows, passage-level rows, coding decisions, limitations, follow-up questions, and a cross-source matrix only where the material supports comparison.

## 3. Literature mapping sprint

Use `literature-review-mapper` to create:

- schools of thought
- debates
- consensus/controversy map
- gaps
- chapter implications

Output artifact: `literature-map.md`.

Contract artifact type: `literature_map`.

## 4. Argument design sprint

Use `argument-architecture` first, then use `counterargument-peer-review` to test the result.

Output artifacts:

- `thesis-tree.md`
- `peer-review-critique.md`

Contract artifact type: `thesis_tree`.

## 5. Chapter build sprint

Use `chapter-architecture` for each chapter.

Output artifact per chapter: `chapter-brief.md`.

Contract artifact type: `chapter_brief`.

## 6. Drafting and prose sprint

Use `scholarly-prose-editor` after the chapter's logic is stable. Do not use prose polish to hide evidence problems.

## 7. Evidence audit sprint

Use `claim-evidence-ledger` before `claim-traceability-graph`, so the claims and evidence status are clear before chain audit.

Use `claim-traceability-graph` before `citation-integrity-auditor` when claims need to be connected to source notes, citekeys, locators, and repair actions. It should not treat nearby citations as proof.

Output artifacts:

- `claim-evidence-ledger.csv`
- `claim-traceability-graph.md`
- `citation-integrity-audit.md`

Contract artifact type: `claim_evidence_ledger`.

## 8. Whole manuscript sprint

Use `manuscript-continuity-editor` after several chapters exist.

Output artifact: `continuity-review.md`.

Contract artifact type: `continuity_review`.

## 9. Proposal sprint

Use `book-proposal-scholarship` once the thesis, audience, source base, and chapter structure are stable.

Use `book-comps-verifier` for comparable titles, audience claims, market claims, timeliness claims, and press positioning before sending the proposal.

Contract artifact type: `book_proposal`.

## 10. Release sprint

Use `rights-privacy-release-auditor` before sharing notes, source packets, proposal materials, manuscript exports, or research artifacts outside the project. It should report release blockers and required fixes. It should not delete, redact, rewrite, publish, or send files unless the user asks.

## Validation

Run package validation after structural changes:

```bash
./validate.sh
```
