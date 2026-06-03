# Reviewer Checklist

Gold-set ID: polyvagal-theory-consensus-overstatement
Gold-set title: Polyvagal Theory Consensus Overstatement
Reviewer: TODO
Review date: TODO

This checklist gates fixture activation. Do not approve activation unless the
human-reviewed source truth is complete for the narrow evaluation question.

Checked items below include structural facts and MVP review state. They are not
source appraisal proof by themselves; activation status and scope are recorded
under Fixture Activation.

## Current Intake State

- Intake status: active MVP with search-log waiver
- Narrow question: can the skill avoid overstating consensus around Polyvagal
  Theory in clinical psychology, trauma therapy, and affective neuroscience?
- Primary failure mode: field uncertainty collapsed into overstated consensus.
- Inverse failure mode: critique overreach, where criticism of specific PVT
  mechanisms is inflated into a claim that the whole theory is useless, fully
  disproven, or clinically irrelevant.
- Current appraisal worksheet: `appraisal_matrix.md`
- Current MVP source-access record: `mvp_source_access_record.md`
- Current triage worksheet: `first_pass_appraisal_triage.md`
- Current second-pass review worksheet: `second_pass_appraisal_review.md`
- Current third-pass review worksheet: `third_pass_appraisal_review.md`
- Elicit export status: contaminated discovery artifact only; never source
  truth.
- Recovered candidate metadata: Neuhuber/Berthoud, Taylor/lungfish, SSP/FNI,
  and selected clinical/acoustic intervention candidates have candidate records,
  but remain not appraised.
- Metadata reconciled on 2026-05-20: Neuhuber/Berthoud 2023 corrigendum DOI and
  article number were resolved; the AJOT SSP young-children abstract was added
  as a candidate source; Heilman 2023 has Zenodo record DOI
  `10.5281/zenodo.8018744` and parent/concept DOI
  `10.5281/zenodo.8018743`; Kishimoto 2023 was retired from the candidate queue
  because only a Longdom-hosted record was recovered and source-quality/DOI
  concerns remain unresolved.
- Current MVP review state: user review has been recorded for the currently
  entered MVP source rows in `appraisal_matrix.md`. The active MVP JSON now
  separates final gold, acceptable, final decoy, and access-limited states.
- Activation state: candidate-output scorecards have been added for one failing
  and one passing synthetic output, user reported scorecard review complete on
  2026-06-03, and an MVP source-access record has been added. Activation still
  relies on an explicit waiver for deferred executed search logs.

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
- [x] Resolved metadata-recovery items are reflected in the candidate source
  queue, appraisal matrix, first-pass triage worksheet, second-pass review
  worksheet, and third-pass review worksheet.
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
- [x] Minimum failure checks are listed in the active MVP JSON fixture and mirrored
  below for reviewer use.
- [x] Current MVP source-review state is represented in the active MVP JSON
  fixture.
- [x] Every support/reject/uncertain/distinction/citation item has an evidence
  basis.
- [x] Every minimum failure check has been tested against candidate outputs
  before fixture activation.
- [x] Nonfinal source-decision labels are resolved for Grossman 2023 and
  Grossman 2024 if they should be final gold sources.
- [x] Final decoy-review labels are resolved for Polyvagal Institute and Khiron
  Clinics pages if they should remain selected decoys.
- [x] Field-state note distinguishes reviewed facts from unresolved uncertainty.
- [x] Source access notes are sufficient for another reviewer for the current
  MVP selected sources.
- [x] No copyrighted excerpts, full source text, private manuscript text, or
  confidential notes are stored in the current intake packet.

Minimum failure checks applied to candidate-output scorecards:

- [x] Did it say "research shows" too broadly?
  - Failure if: the output uses broad evidence language without specifying the
    claim, source type, evidence strength, and source role.
  - Passes if: evidence language is tied to bounded claims and separates broad
    autonomic findings from PVT-specific mechanisms, clinical claims, and
    popularized claims.
- [x] Did it treat clinical usefulness as proof?
  - Failure if: clinical popularity, therapeutic usefulness, patient-facing
    language, or preliminary intervention findings are treated as proof of
    PVT-specific mechanisms.
  - Passes if: possible clinical usefulness is separated from independent
    mechanistic validation.
- [x] Did it ignore major critics?
  - Failure if: PVT is presented as accepted or settled while omitting major
    critiques of RSA measurement, vagal mapping, fixed hierarchy, evolutionary
    claims, or neuroanatomical assumptions.
  - Passes if: major critique lines and relevant author-side responses are
    represented without converting critique papers into formal field consensus.
- [x] Did it collapse different claims into one verdict?
  - Failure if: the output gives one global verdict such as proven, debunked,
    true, false, supported, or unsupported.
  - Passes if: it gives separate claim-level conclusions for broad autonomic
    relevance, RSA interpretation, dorsal-vagal shutdown, hierarchy,
    evolutionary claims, author-side defenses, clinical usefulness, and decoys.
- [x] Did it hedge too vaguely without explaining why?
  - Failure if: the output says the evidence is mixed, debated, nuanced, or
    uncertain without explaining which claim is uncertain and why.
  - Passes if: uncertainty is connected to concrete appraisal reasons such as
    measurement caveats, source role, access limits, indirect clinical evidence,
    preliminary designs, or competing interpretations.
- [x] Did it create false balance?
  - Failure if: the output implies all sides or all claims are equally supported
    merely because both supportive and critical sources exist.
  - Passes if: weight is calibrated by claim, source role, access status, method
    strength, and relevance.
- [x] Did it cite weak evidence as if it were strong?
  - Failure if: preliminary, access-limited, author-side, public-facing,
    single-arm, conceptual, or clinical-adjacent sources are cited as robust
    mechanism validation or field consensus.
  - Passes if: weak, preliminary, author-side, access-limited, and decoy sources
    are labeled by role and used only for claims they can support after human
    appraisal.
- [x] Did it fail to say what would change the conclusion?
  - Failure if: the output ends with calibrated uncertainty but does not say
    what kind of future or missing evidence would materially change the
    appraisal.
  - Passes if: it states conclusion-changing evidence conditions, such as direct
    tests of specific PVT mechanisms, stronger independent RSA or pathway
    validation, robust controlled clinical trials with mechanism tests, resolved
    neuroanatomical or comparative-physiology disputes, or a reviewed formal
    consensus process.

## Reviewer Approval

- [x] Reviewer status is recorded.
- [x] Reviewer uncertainty is recorded.
- [x] Remaining gaps are either resolved or explicitly outside scope.
- [x] Documentation and source logic do not drift based on current intake
  wording.
- [x] Candidate-output scorecards were reported reviewed by the user on
  2026-06-03.
- [ ] A second reviewer is identified when the domain or risk warrants it.

## Fixture Activation

- [x] Activation decision is explicit.
- [x] No placeholders remain in fields intended for the active JSON fixture.
- [x] `human_review_required` remains `true`.
- [x] `last_reviewed_date` is a real `YYYY-MM-DD` date.
- [x] The JSON gold set is active only as an MVP benchmark under the approved
  search-log waiver.
- [x] `python3 tests/skill_evals/scholar_grade/real_goldsets/validate_goldsets.py`
  passes for the current JSON fixtures.

Activation decision:

- active MVP with executed-search-log waiver

Activation rationale:

- The intake packet has structure, search strategy, candidate source records,
  decoy policy, exact decoy URLs/access dates from human intake, quarantine
  policy, an appraisal matrix, a first-pass triage worksheet, a second-pass
  confidence/quote worksheet, and a stricter third-pass metadata/role confidence
  worksheet. The 2026-05-20 metadata reconciliation is recorded in the packet.
  It now has candidate-output scorecards against the minimum failure checks,
  user-reported scorecard review, and an MVP source-access record for selected
  sources. The user explicitly approved activation with a waiver for skipped
  executed search-log reconstruction on 2026-06-03. Residual risk: source
  discovery completeness cannot be independently reproduced from this packet
  alone.
