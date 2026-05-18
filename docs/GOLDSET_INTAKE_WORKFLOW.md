# Gold-Set Intake Workflow

This workflow guides a human reviewer through creating a real-source gold set
for scholar-grade evaluation. It is a readiness process, not an automated truth
generator.

Codex may help format notes, copy templates, run validators, and identify missing
fields. Codex must not invent scholarly truth, source judgments, field consensus,
DOIs, page numbers, quotes, retraction status, or expert conclusions. When a
field requires source truth, a human reviewer supplies it.

**Warning:** A source being peer-reviewed does not automatically make it
gold-set truth. Gold-set truth means a human reviewer has checked what the
source does and does not support for the narrow evaluation question.

## Workflow Phases

### 1. Source Discovery

Purpose: build a candidate pool without judging it as gold truth yet.

The human supplies:

- gold-set title
- narrow research or evaluation question
- scholarly failure mode being tested
- target skill or skill group
- expected output type
- search domains or databases to use
- inclusion criteria
- exclusion criteria
- candidate gold sources
- candidate acceptable, decoy, and disallowed sources when already known

What matters:

- Keep the question narrow enough that a reviewer can inspect source support.
- Record where searches were run and which access limits apply.
- Separate candidate discovery from source appraisal. Do not mark a source as
  gold just because it appears central, recent, cited often, or peer-reviewed.
- Do not copy source excerpts into repository files. Use source identifiers,
  metadata, locators, and access notes.

### 2. Source Appraisal

Purpose: decide what each source can and cannot support.

The human supplies:

- source role: gold, acceptable, decoy, disallowed, or still undecided
- source type: primary source, review, commentary, method paper, dataset,
  replication, correction, weak source, or another explicit type
- locator or access note sufficient for reviewer inspection
- reason for inclusion or exclusion
- decoy reason for every decoy source
- reviewed support limits
- reviewer uncertainty

What matters:

- Peer review is not enough. Check whether the source addresses the specific
  population, period, method, corpus, claim type, and evidentiary standard.
- Decoys are useful only when their failure mode is explicit, such as wrong
  population, wrong endpoint, commentary only, outdated source, unsupported
  extrapolation, or weak evidence for the prompt.
- Disallowed sources should have a concrete reason, not a preference.
- If source metadata or field-state documentation drift, stop and resolve the
  drift with human review.

### 3. Gold-Set Authoring

Purpose: convert reviewed source judgments into a structured inactive gold set.

The human supplies:

- claims the output must support
- claims the output must reject
- claims that must remain uncertain
- required distinctions, such as primary versus review, empirical finding
  versus commentary, or metadata versus claim support
- citation-audit expectations
- field-state note
- source access notes

What matters:

- Each `must_support`, `must_reject`, and `must_remain_uncertain` item needs a
  human-reviewed evidence basis.
- The authoring step may still use placeholders for unresolved fields, but the
  fixture must stay inactive while placeholders remain.
- The field-state note should distinguish reviewed facts from unresolved
  disagreement or insufficient evidence.
- Store short reviewer notes and source IDs, not full copyrighted passages or
  private manuscript text.

### 4. Reviewer Approval

Purpose: confirm that the gold set represents reviewed source truth for the
bounded evaluation question.

The reviewer supplies:

- reviewer status
- reviewer uncertainty
- unresolved issues or exclusions
- activation decision
- review date

What matters:

- Approval means the reviewer has checked what each source does and does not
  support, not merely checked that metadata exists.
- The reviewer should reject activation when evidence bases are vague, decoy
  reasons are missing, field uncertainty is collapsed, or source-access notes
  are insufficient for another reviewer.
- If a waiver is used for `human_review_required`, it must include explicit
  rationale. Waivers should be rare and should not be used to bypass source
  appraisal.

### 5. Fixture Activation

Purpose: move from an intake packet to an active JSON gold set only when the
human-review gate is complete.

Activation requirements:

- no `PLACEHOLDER`, `TODO`, or `TBD` values remain
- `human_review_required` is `true`, unless explicitly waived with rationale
- `last_reviewed_date` is a real `YYYY-MM-DD` date
- every source has title, authors or authoring body, year if known,
  locator/access note, and role
- every decoy source has a decoy reason
- every support, reject, uncertain, distinction, and citation-audit expectation
  has an evidence basis
- no copyrighted excerpts, full source text, private manuscript text, or
  confidential notes are stored
- `validate_goldsets.py` passes

Codex may run the validator and report errors. Codex must not mark a fixture
active unless the human has explicitly provided activation readiness and the
reviewed fields needed by the validator.

## Intake Files

Use these templates:

- `tests/skill_evals/scholar_grade/real_goldsets/templates/goldset_intake.md`
- `tests/skill_evals/scholar_grade/real_goldsets/templates/source_appraisal.md`
- `tests/skill_evals/scholar_grade/real_goldsets/templates/reviewer_checklist.md`

Optional scaffold:

```bash
python3 tests/skill_evals/scholar_grade/real_goldsets/new_goldset_intake.py \
  --goldset-id my-goldset-id \
  --title "My Gold Set Title"
```

The helper creates Markdown intake files only. It does not create an active JSON
fixture and does not supply scholarly truth.
