# Workflow Playbook

## 0. Start with the orchestrator

Prompt:

```text
Use scholarly-book-orchestrator. I am writing a scholarly nonfiction book about [topic]. Build a staged research and writing workflow with quality gates.
```

## 1. Agenda sprint

Use `scholarly-research-agenda` to define:

- central research question
- subquestions
- contribution claim
- scope boundaries
- evidence plan

Output artifact: `research-agenda.md`.

## 2. Source discovery sprint

Use `systematic-source-discovery` to create:

- search families
- Boolean queries
- search venues
- inclusion/exclusion rules
- search log

Output artifact: `search-log.md`.

## 3. Literature mapping sprint

Use `literature-review-mapper` to create:

- schools of thought
- debates
- consensus/controversy map
- gaps
- chapter implications

Output artifact: `literature-map.md`.

## 4. Argument design sprint

Use `argument-architecture` and `counterargument-peer-review` together.

Output artifacts:

- `thesis-tree.md`
- `peer-review-critique.md`

## 5. Chapter build sprint

Use `chapter-architecture` for each chapter.

Output artifact per chapter: `chapter-brief.md`.

## 6. Drafting and prose sprint

Use `scholarly-prose-editor` after the chapter's logic is stable. Do not use prose polish to hide evidence problems.

## 7. Evidence audit sprint

Use `claim-evidence-ledger` before `citation-integrity-auditor`.

Output artifacts:

- `claim-evidence-ledger.csv`
- `citation-integrity-audit.md`

## 8. Whole manuscript sprint

Use `manuscript-continuity-editor` after several chapters exist.

Output artifact: `continuity-review.md`.

## 9. Proposal sprint

Use `book-proposal-scholarship` once the thesis, audience, source base, and chapter structure are stable.
