# Workflow playbook

For the staged architecture, see `docs/ARCHITECTURE.md`. For route names and outputs, see `MODE_REGISTRY.md`.

## 0. Start with the orchestrator

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

Use `argument-architecture` and `counterargument-peer-review` together.

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

Use `claim-evidence-ledger` before `citation-integrity-auditor`.

Output artifacts:

- `claim-evidence-ledger.csv`
- `citation-integrity-audit.md`

Contract artifact type: `claim_evidence_ledger`.

## 8. Whole manuscript sprint

Use `manuscript-continuity-editor` after several chapters exist.

Output artifact: `continuity-review.md`.

Contract artifact type: `continuity_review`.

## 9. Proposal sprint

Use `book-proposal-scholarship` once the thesis, audience, source base, and chapter structure are stable.

Contract artifact type: `book_proposal`.

## Validation

Run package validation after structural changes:

```bash
./validate.sh
```
