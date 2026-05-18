# Reviewer Checklist

Gold-set ID: {{goldset_id}}
Gold-set title: {{goldset_title}}
Reviewer:
Review date:

This checklist gates fixture activation. Do not approve activation unless the
human-reviewed source truth is complete for the narrow evaluation question.

## Source Discovery

- [ ] Gold-set title is clear.
- [ ] Narrow research or evaluation question is clear.
- [ ] Scholarly failure mode being tested is explicit.
- [ ] Target skill or skill group is identified.
- [ ] Expected output type is identified.
- [ ] Search domains or databases are listed.
- [ ] Inclusion criteria are listed.
- [ ] Exclusion criteria are listed.
- [ ] Discovery notes identify search dates, access limits, and unresolved gaps.

## Source Appraisal

- [ ] Candidate gold sources have title, authors or authoring body, year if
  known, locator/access note, and role.
- [ ] Acceptable sources have title, authors or authoring body, year if known,
  locator/access note, and role.
- [ ] Decoy sources have title, authors or authoring body, year if known,
  locator/access note, role, and decoy reason.
- [ ] Disallowed sources have title, authors or authoring body, year if known,
  locator/access note, role, and disallow reason.
- [ ] Each source judgment states what the source supports.
- [ ] Each source judgment states what the source does not support.
- [ ] Peer-reviewed status was not treated as automatic gold-set truth.
- [ ] Field uncertainty and source limits are preserved.

## Gold-Set Authoring

- [ ] Claims the output must support are listed.
- [ ] Claims the output must reject are listed.
- [ ] Claims that must remain uncertain are listed.
- [ ] Required distinctions are listed.
- [ ] Citation-audit expectations are listed or explicitly marked not applicable.
- [ ] Every support/reject/uncertain/distinction/citation item has an evidence
  basis.
- [ ] Field-state note distinguishes reviewed facts from unresolved uncertainty.
- [ ] Source access notes are sufficient for another reviewer.
- [ ] No copyrighted excerpts, full source text, private manuscript text, or
  confidential notes are stored.

## Reviewer Approval

- [ ] Reviewer status is recorded.
- [ ] Reviewer uncertainty is recorded.
- [ ] Remaining gaps are either resolved or explicitly outside scope.
- [ ] Documentation and source logic do not drift.
- [ ] A second reviewer is identified when the domain or risk warrants it.

## Fixture Activation

- [ ] Activation decision is explicit.
- [ ] No placeholders remain in fields intended for the active JSON fixture.
- [ ] `human_review_required` remains `true`, unless an explicit waiver rationale
  has been reviewed.
- [ ] `last_reviewed_date` is a real `YYYY-MM-DD` date.
- [ ] The JSON gold set remains inactive until all activation criteria are met.
- [ ] `python3 tests/skill_evals/scholar_grade/real_goldsets/validate_goldsets.py`
  passes for the authored JSON fixture.

Activation decision:

- [inactive | needs more source discovery | needs source appraisal | needs
  reviewer approval | ready for JSON authoring | ready for activation]

Activation rationale:

- [fill in]
