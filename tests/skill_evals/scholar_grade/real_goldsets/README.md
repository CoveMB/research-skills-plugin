# Real-Source Gold Sets

This directory holds real-source scholar-grade gold sets. It is intentionally
separate from the controlled fixture suite.

Controlled fixtures test epistemic discipline against small local packets: whether
a skill preserves uncertainty, refuses unsupported claims, avoids hidden answer
keys, and hard-fails on fabricated verification. They do not certify real-world
source truth.

Real-source gold sets test source selection and synthesis after human reviewers
populate the cases with a reviewed source basis. They are for questions such as
whether a skill identifies core sources, avoids decoys, distinguishes primary
sources from reviews or commentary, preserves live field uncertainty, avoids
cherry-picking, and synthesizes accurately. Active MVP cases remain bounded to
their reviewed packet and waiver notes; they do not certify source discovery
completeness or independent scholarly truth beyond the recorded human review.

## Files

- `goldset.schema.json` documents the JSON shape for each gold-set case.
- `validate_goldsets.py` validates all gold-set JSON files in this directory.
- `live_test_goldsets.py` validates active real-source cases for local
  live-test readiness and checks reviewed candidate output scorecards.
- `templates/` contains fillable Markdown intake, source-appraisal, and reviewer
  checklist templates.
- `new_goldset_intake.py` scaffolds an inactive Markdown intake packet from the
  templates.
- `retrieval-template.inactive.json` is an inactive retrieval-focused template.
- `synthesis-template.inactive.json` is an inactive synthesis-focused template.

The inactive templates contain placeholders. They are examples of structure, not
scholarly claims.

See `docs/GOLDSET_INTAKE_WORKFLOW.md` for the human-guided workflow from source
discovery through fixture activation.

## Activation Rules

Do not mark a gold set `active` until human review has provided:

- real source metadata for every gold, acceptable, decoy, and disallowed source
- access notes or locators sufficient for another reviewer to inspect the basis
- the role of each source, such as primary source, review, commentary, weak
  source, decoy, or disallowed source
- decoy reasons explaining why a source should not satisfy the task
- evidence bases for every `must_support`, `must_reject`, and
  `must_remain_uncertain` item
- required source-type distinctions that the skill must preserve
- citation-audit expectations when the task includes citation checking
- a field-state note that distinguishes reviewed facts from unresolved expert
  uncertainty
- `last_reviewed_date` in `YYYY-MM-DD` form
- reviewer notes describing what was checked and what remains outside scope

The agent must not fabricate any of those values. Use placeholders while a case
is inactive. If documentation and source evidence drift, resolve the drift with
human review rather than treating the documentation as source truth.

## Data Limits

Gold-set JSON stores metadata, review notes, and short evidence descriptions
only. Do not store full copyrighted passages, real source excerpts, private
unpublished manuscript text, confidential notes, or material that requires
separate access permission.

Use source identifiers and access notes instead of copying source text. When a
claim requires source truth, store the human-reviewed evidence basis, not the
source passage.

## Validation

Run:

```bash
python3 tests/skill_evals/scholar_grade/real_goldsets/validate_goldsets.py
```

The validator checks required fields, source-entry metadata, decoy reasons,
expectation evidence bases, active-case placeholder removal, human-review
requirements, and obvious attempts to store copyrighted excerpts or private
manuscript text. When a draft records `candidate_output_scorecards`, the
validator also checks that every scorecard covers every listed
`minimum_failure_checks` entry and does not score unknown checks. If an active
MVP fixture uses a search-log scope waiver, the waiver must include explicit
approval, waived requirement, scope limit, residual risk, and approval date.

Validate active real-source live-test readiness:

```bash
python3 tests/skill_evals/scholar_grade/real_goldsets/live_test_goldsets.py
python3 scripts/run_package_checks.py --scope real-goldsets
```

The live-test readiness check renders the visible prompt packet, verifies that
the packet does not expose grader-only fields, and checks that active cases
include reviewed passing and failing candidate outputs for every
`minimum_failure_checks` entry. It does not run a model or replace human review.
