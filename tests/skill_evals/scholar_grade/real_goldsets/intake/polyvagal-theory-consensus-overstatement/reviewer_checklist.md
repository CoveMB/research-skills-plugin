# Reviewer Checklist

Gold-set ID: polyvagal-theory-consensus-overstatement
Gold-set title: Polyvagal Theory Consensus Overstatement
Reviewer: TODO
Review date: TODO

This checklist gates fixture activation. Do not approve activation unless the
human-reviewed source truth is complete for the narrow evaluation question.

Checked items below are non-appraisal structural facts already present in the
intake packet. They are not reviewer approval and do not activate the fixture.

## Current Intake State

- Intake status: `intake-draft, not active`
- Narrow question: can the skill avoid overstating consensus around Polyvagal
  Theory in clinical psychology, trauma therapy, and affective neuroscience?
- Primary failure mode: field uncertainty collapsed into overstated consensus.
- Inverse failure mode: critique overreach, where criticism of specific PVT
  mechanisms is inflated into a claim that the whole theory is useless, fully
  disproven, or clinically irrelevant.
- Current appraisal worksheet: `appraisal_matrix.md`
- Elicit export status: contaminated discovery artifact only; never source
  truth.
- Recovered candidate metadata: Neuhuber/Berthoud, Taylor/lungfish, SSP/FNI,
  and selected clinical/acoustic intervention candidates have candidate records,
  but remain not appraised.
- Activation state: needs metadata verification and source appraisal.

## Source Discovery

- [x] Gold-set title is clear.
- [x] Narrow research or evaluation question is clear.
- [x] Scholarly failure mode being tested is explicit.
- [x] Target skill or skill group is identified.
- [x] Expected output type is identified.
- [x] Search domains or databases are listed.
- [x] Inclusion criteria are listed.
- [x] Exclusion criteria are listed.
- [ ] Discovery notes identify search dates, access limits, and unresolved gaps.

Discovery note: literature-map or synthesis skill group is identified, but the
exact target skill still needs confirmation before fixture authoring.
Access-limit policy and unresolved gaps are recorded. Exact executed search
dates are still missing.

## Source Appraisal

- [x] Candidate source records with recovered metadata have title, authors or
  authoring body, year if known, locator/access note, and provisional role.
- [x] Metadata-recovery TODO records identify missing metadata and are barred
  from evidence use until verified.
- [x] Decoy candidate records have title, authoring body, year if known,
  locator/access note, URL/access date when supplied, role, and decoy reason.
- [x] True disallowed sources are recorded as none identified yet; quarantine is
  kept separate from disallow.
- [ ] Each source judgment states what the source supports.
- [ ] Each source judgment states what the source does not support.
- [x] Peer-reviewed status was not treated as automatic gold-set truth.
- [x] Field uncertainty and source limits are preserved.

## Gold-Set Authoring

- [x] Provisional claims the output is expected to support are listed.
- [x] Provisional claims the output is expected to reject are listed.
- [x] Provisional uncertainties the output should preserve are listed.
- [x] Required distinctions are listed.
- [x] Citation-audit expectations are listed or explicitly marked not applicable.
- [ ] Every support/reject/uncertain/distinction/citation item has an evidence
  basis.
- [ ] Field-state note distinguishes reviewed facts from unresolved uncertainty.
- [ ] Source access notes are sufficient for another reviewer.
- [x] No copyrighted excerpts, full source text, private manuscript text, or
  confidential notes are stored in the current intake packet.

## Reviewer Approval

- [x] Reviewer status is recorded.
- [x] Reviewer uncertainty is recorded.
- [x] Remaining gaps are either resolved or explicitly outside scope.
- [x] Documentation and source logic do not drift based on current intake
  wording.
- [ ] A second reviewer is identified when the domain or risk warrants it.

## Fixture Activation

- [x] Activation decision is explicit.
- [ ] No placeholders remain in fields intended for the active JSON fixture.
- [ ] `human_review_required` remains `true`, unless an explicit waiver rationale
  has been reviewed.
- [ ] `last_reviewed_date` is a real `YYYY-MM-DD` date.
- [x] The JSON gold set remains inactive until all activation criteria are met.
- [x] `python3 tests/skill_evals/scholar_grade/real_goldsets/validate_goldsets.py`
  passes for the current inactive JSON fixtures.

Activation decision:

- needs metadata verification and source appraisal

Activation rationale:

- The intake packet has structure, search strategy, candidate source records,
  decoy policy, exact decoy URLs/access dates from human intake, quarantine
  policy, and an appraisal matrix. It still lacks executed search logs,
  source-access records for selected sources, human-reviewed source appraisals,
  evidence bases, and reviewer approval.
