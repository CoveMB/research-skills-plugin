# Polyvagal Theory Appraisal Matrix

Gold-set ID: polyvagal-theory-consensus-overstatement
Gold-set title: Polyvagal Theory Consensus Overstatement
Status: appraisal worksheet, not active

This worksheet is for human source appraisal. It is not source truth by itself.
Do not mark a source, claim, distinction, or citation expectation as ready until
a reviewer has checked what the source does and does not support.

Related triage worksheets: `first_pass_appraisal_triage.md`,
`second_pass_appraisal_review.md`, and `third_pass_appraisal_review.md`. Their
scores, proof notes, and short quotes are pre-appraisal confidence aids only;
they are not evidence bases, source appraisals, or reviewer approval. Use the
third-pass worksheet for the strictest current score wording.

## Parse Conventions

- Keep source IDs stable.
- Use `TODO` for fields that still need human review.
- Use `not_appraised` until a reviewer has inspected the source record and, when
  needed, accessible full text.
- Do not treat the Elicit export as source truth. It is a contaminated discovery
  artifact only.
- Do not use decoys as evidence of scientific support or consensus.
- Do not infer field consensus from source count, citation count, popularity, or
  clinical uptake.
- `doi`, `review_link`, `exact_url`, and `additional_locator` fields are review
  convenience locators only. They do not appraise source content or establish
  evidence strength.

Allowed source decisions:

- `gold`
- `acceptable`
- `decoy`
- `disallowed`
- `exclude`
- `undecided`

Allowed evidence-strength labels:

- `strong`
- `moderate`
- `mixed`
- `weak`
- `speculative`
- `not_applicable`
- `undecided`

## Reviewer Run

reviewer_name: Cove
review_date: 05/20/2026
metadata_reconciliation_date: 2026-05-20
locator_update_date: 2026-05-26
databases_checked: TODO
search_dates: 05/18/2026
full_text_access_notes: TODO
remaining_access_gaps: TODO

## Metadata Reconciliation Ledger

- `candidate-neuhuber-berthoud-2023-corrigendum`: DOI reconciled as
  `10.1016/j.biopsycho.2023.108554`; Biological Psychology, 179, Article
  108554. Keep as `not_appraised`.
- `candidate-rogowski-et-al-2024-ajot-ssp-young-children`: promoted from
  unresolved metadata recovery to candidate source record; DOI reconciled as
  `10.5014/ajot.2024.78S2-PO332`. Treat as abstract/poster candidate, not full
  article evidence.
- `candidate-heilman-et-al-2023-ssp-autism-single-arm`: Zenodo record DOI
  reconciled as `10.5281/zenodo.8018744`; public OADD PDF is linked from that
  record. DOI `10.5281/zenodo.8018743` resolves as the Zenodo parent/concept
  DOI. No separate journal-assigned DOI has been recovered.
- `retired-kishimoto-et-al-2023-ssp-children-autism`: retired from the
  candidate source queue. The only recovered record is Longdom-hosted; the
  publisher/PDF-stated DOI `10.35248/2161-0487.23.13.455` did not resolve via
  `doi.org` in this review pass; venue/source quality remains unresolved. DOI
  `10.3390/ijerph20064862` belongs to
  `candidate-kawai-et-al-2023-ssp-adult-autism`, not this source.
- `unresolved-ajot-ssp-young-children`: retired after candidate source record
  was added.

## Source Appraisal Queue

Each source starts as `not_appraised`. Fill only after checking reliable metadata
and source content.

### candidate-porges-2025-current-status

group: author_side_theory_position
metadata_status: candidate_metadata_recorded
provisional_role: author-side review/defense candidate, not independent validation
intake_metadata_ref: goldset_intake.md source_id candidate-porges-2025-current-status
doi: 10.36131/cnfioritieditore20250301
review_link: https://doi.org/10.36131/cnfioritieditore20250301
Former local PDF: Clinical25-3_correzione articolo Porges.pdf
appraisal_status: human_reviewed
reviewer_source_decision: acceptable
access_status: open-access full text reviewed during MVP intake; repository no longer stores the local PDF copy; DOI publisher page also available; the reviewed 2026 response record is separate and was not used for this 2025 record
full_text_reviewed: yes for machine-assisted draft extraction; future human verification should use the DOI/publisher page or a separately obtained full text
can_support: Porges's current author-side articulation of Polyvagal Theory as an evolutionarily informed, systems-level framework; Porges's framing of hierarchical autonomic state regulation, the ventral vagal complex/social engagement system, neuroception, co-regulation, dorsal-vagal defensive states, and dissolution; Porges's author-side claims about RSA, vagal efficiency, and weighted coherence as autonomic metrics; Porges's clinical and translational framing across trauma, chronic pain or functional disorders, autism or neurodevelopmental conditions, mood disorders, development or attachment, education, public health, and systems design; Porges's responses to critiques about popularization, falsifiability, anatomical specificity, and RSA/respiration interpretation
cannot_support: independent validation, field consensus, or proof that contested PVT mechanisms are settled; proof that clinical applications are empirically established or PVT-specific; proof that RSA, vagal efficiency, or weighted coherence are accepted direct biomarkers by independent physiology literature; proof that critiques by Grossman, Taylor, Neuhuber, Berthoud, Doody, or others are refuted; proof that clinical uptake validates the theory's physiological mechanisms
must_remain_uncertain: whether Porges's clarifications resolve independent critiques; whether independent neuroanatomy, comparative physiology, RSA methodology, or clinical-intervention sources support the specific mechanisms claimed; whether clinical usefulness establishes PVT-specific mechanisms; whether the field broadly accepts the theory; exact page range because the reviewed PDF copy and citation metadata conflict
source_limits: author-side invited paper and narrative/theory review; not independent adjudication, systematic review, meta-analysis, formal consensus statement, or clinical-practice guideline; reviewed PDF header lists Clinical Neuropsychiatry 22(3), 169-184 while the citation block lists 22(3), 175-191, so cite by DOI until reconciled; use to represent Porges's position and programmatic claims, not as stand-alone evidence that those claims are correct
reviewer_notes: Machine-assisted draft from a matched 2025 PDF for human review. Useful as an author-position source for comparing Porges's current claims against critiques. The 2026 response is a separate record and was not used for this 2025 entry. Pair with Grossman et al. 2026, Porges 2026 response, and independent anatomy/RSA/comparative-physiology/clinical sources before using in the claim matrix.

### candidate-porges-2025-journey

group: author_side_theory_position
metadata_status: candidate_metadata_recorded
provisional_role: author-side theory-articulation or clinical-insight candidate
intake_metadata_ref: goldset_intake.md source_id candidate-porges-2025-journey
doi: 10.3389/fnbeh.2025.1659083
review_link: https://doi.org/10.3389/fnbeh.2025.1659083
Former local PDF: fnbeh-19-1659083.pdf
appraisal_status: human_reviewed
reviewer_source_decision: acceptable
access_status: open-access full text reviewed during MVP intake; repository no longer stores the local PDF copy; DOI publisher page also available
full_text_reviewed: yes for machine-assisted draft extraction; future human verification should use the DOI/publisher page or a separately obtained full text
can_support: Porges's author-side 2025 Frontiers articulation of PVT as an integrative autonomic-regulation model; Porges's current framing of PVT's historical development from HRV/RSA observations to neural innervation, hierarchical autonomic state regulation, neuroception, social engagement, and clinical translation; Porges's claims that RSA is a functional output of myelinated ventral vagal/nucleus ambiguus pathways rather than a mere respiratory artifact; Porges's claims about the Porges-Bohrer RSA method, vagal efficiency, weighted coherence, transcriptomic/neuropeptidergic extensions, and clinical/translational applications including SSP, Rest and Restore, VNS, and polyvagal-informed therapies; Porges's author-side responses to critiques by Grossman, Taylor, and collaborators, including claims that critiques misrepresent PVT's assertions about mammalian RSA, cardiorespiratory coupling, sympathetic involvement, and empirical support
cannot_support: independent adjudication of contested claims; field consensus; proof that PVT's mechanistic, evolutionary, RSA, transcriptomic, or clinical claims are settled; proof that Grossman, Taylor, Neuhuber, Berthoud, Doody, or other critiques are refuted; clinical efficacy or mechanism validation for SSP, Rest and Restore, VNS, or polyvagal-informed therapies; neutral evidence synthesis, systematic review, meta-analysis, or guideline-level support
must_remain_uncertain: whether independent RSA methodology, neuroanatomy, comparative physiology, transcriptomics, and clinical-intervention sources support Porges's claims; whether non-mammalian cardiorespiratory coupling is best treated as merely analogous rather than homologous to mammalian RSA; whether Porges's critique responses accurately represent opposing sources; whether PVT's clinical applications exceed the available evidence; whether broad uptake in clinical settings indicates usefulness, mechanistic validity, both, or neither
source_limits: single-author Hypothesis and Theory article by the theory originator; peer-reviewed and open access, but author-side and programmatic rather than independent validation; use to represent Porges's current Frontiers framing, terminology, claimed empirical foundation, and response to critiques, not as stand-alone proof that those claims are correct
reviewer_notes: Machine-assisted draft from full PDF extraction for human review. Useful for ensuring the gold set tests whether an answer fairly includes Porges's current author-side clarifications without treating them as independent validation. Pair with Porges 2025 Clinical Neuropsychiatry current-status paper, Porges 2026 response, Grossman 2023/2026 critiques, Taylor et al. 2022, and independent RSA/neuroanatomy/clinical sources before using in the claim matrix.

### candidate-porges-2026-response

group: author_side_theory_position
metadata_status: candidate_metadata_recorded
provisional_role: author response/rebuttal candidate
intake_metadata_ref: goldset_intake.md source_id candidate-porges-2026-response
doi: 10.36131/cnfioritieditore20260111
review_link: https://doi.org/10.36131/cnfioritieditore20260111
Former local PDF: 11_Porges_Clinical26-1.pdf
appraisal_status: human_reviewed
reviewer_source_decision: acceptable
access_status: open-access full text reviewed during MVP intake; repository no longer stores the local PDF copy; publisher page also available through DOI
full_text_reviewed: yes for machine-assisted draft extraction; future human verification should use the DOI/publisher page or a separately obtained full text
can_support: Porges's author-side rebuttal to Grossman et al. 2026; Porges's current framing that PVT is a systems-level, pathway-specific framework with proposed falsifiability conditions; Porges's claim that critiques mischaracterize PVT by treating it as anatomical exclusivity, global vagal tone, or recapitulationist evolution; Porges's argument that disagreement over RSA metrics, comparative anatomy, or evolutionary framing does not by itself falsify PVT unless it engages the theory's specified mechanisms
cannot_support: independent validation of the theory
must_remain_uncertain: whether Porges's clarifications resolve independent critiques; whether the broader field accepts Porges's framing; whether PVT-specific mechanisms are empirically established; whether clinical or translational usefulness claims are supported independently of author-side interpretation
source_limits: author response/rebuttal; not independent adjudication; use to represent Porges's position and clarifications, not field consensus or mechanism validation; page range 113-128 in the reviewed PDF copy; competing-interest statement points to Porges 2025 Clinical Neuropsychiatry paper
reviewer_notes: Machine-assisted draft from full PDF extraction for human review. Useful for testing whether an answer acknowledges author-side responses without treating them as independent validation. Pair with Grossman et al. 2026 and independent anatomy/RSA/comparative-physiology sources before using in claim matrix.

### candidate-austin-riniolo-porges-2007-bpd

group: supportive_theory_adjacent_empirical
metadata_status: candidate_metadata_recorded
provisional_role: empirical supportive/suggestive candidate, not whole-theory validation
intake_metadata_ref: goldset_intake.md source_id candidate-austin-riniolo-porges-2007-bpd
doi: 10.1016/j.bandc.2006.05.007
review_link: https://doi.org/10.1016/j.bandc.2006.05.007
appraisal_status: not_appraised
reviewer_source_decision: TODO
access_status: TODO
full_text_reviewed: TODO
can_support: TODO
cannot_support: validation of Polyvagal Theory as a whole
must_remain_uncertain: TODO
source_limits: TODO
reviewer_notes: TODO

### candidate-porges-riniolo-mcbride-campbell-2003-reptiles

group: supportive_theory_adjacent_empirical
metadata_status: candidate_metadata_recorded
provisional_role: author-side comparative empirical support candidate
intake_metadata_ref: goldset_intake.md source_id candidate-porges-riniolo-mcbride-campbell-2003-reptiles
doi: 10.1016/S0278-2626(03)00012-5
review_link: https://doi.org/10.1016/S0278-2626(03)00012-5
appraisal_status: not_appraised
reviewer_source_decision: TODO
access_status: TODO
full_text_reviewed: TODO
can_support: TODO
cannot_support: independent adjudication of PVT
must_remain_uncertain: TODO
source_limits: author-side comparative/autonomic evidence
reviewer_notes: TODO

### candidate-obrien-2021-act-rsa

group: adjacent_supportive_pending_appraisal
metadata_status: candidate_metadata_recorded
provisional_role: empirical clinical association / adjacent autonomic evidence candidate
intake_metadata_ref: goldset_intake.md source_id candidate-obrien-2021-act-rsa
doi: 10.1521/BUMC.2021.85.1.9
review_link: https://doi.org/10.1521/BUMC.2021.85.1.9
appraisal_status: not_appraised
reviewer_source_decision: TODO
access_status: TODO
full_text_reviewed: TODO
can_support: TODO
cannot_support: Polyvagal-specific mechanistic validation
must_remain_uncertain: TODO
source_limits: TODO
reviewer_notes: TODO

### candidate-poli-2021-contemplative-review

group: adjacent_supportive_pending_appraisal
metadata_status: candidate_metadata_recorded
provisional_role: systematic review / preliminary clinical-adjacent evidence candidate
intake_metadata_ref: goldset_intake.md source_id candidate-poli-2021-contemplative-review
doi: 10.3390/ijerph182211778
review_link: https://doi.org/10.3390/ijerph182211778
Former local PDF: A Systematic Review of a Polyvagal Perspective on Embodied Contemplative Practices.pdf
appraisal_status: human_reviewed
reviewer_source_decision: acceptable
access_status: open-access full text reviewed during MVP intake; repository no longer stores the local PDF copy; DOI publisher page also available
full_text_reviewed: yes for machine-assisted draft extraction; future human verification should use the DOI/publisher page or a separately obtained full text
can_support: systematic-review source showing that some clinical-adjacent contemplative-practice literature is explicitly framed through a Polyvagal perspective; evidence that Poli et al. searched PubMed and Scopus using PRISMA 2020 procedures and AMSTAR-2 appraisal; evidence that only six articles met inclusion criteria, with mixed designs including cross-sectional, pre-post, cohort, RCT, and RCT-protocol material; support for the limited claim that some included PTSD/OCD mindfulness-related studies reported parasympathetic activity, increased vagal-tone or HRV-related measures, symptom improvements, or neural findings compatible with a PVT interpretation; support for using this source as an example that PVT-framed clinical-adjacent evidence is preliminary, heterogeneous, and methodologically limited
cannot_support: strong validation of PVT; proof that mindfulness, compassion meditation, or contemplative practices activate the ventral vagal complex as a demonstrated mechanism; proof that RSA/HRV directly measures VVC activation or safety; strong treatment-efficacy claims for PTSD or OCD; general trauma-therapy validation; SSP or acoustic-intervention claims; field consensus; direct adjudication of PVT's anatomical, evolutionary, dorsal-vagal, or RSA-measurement controversies
must_remain_uncertain: whether the included studies' physiological outcomes actually support PVT-specific mechanisms rather than broader autonomic or clinical effects; how much weight to give findings from small, uncontrolled, underpowered, or protocol-only studies; whether medication, respiration, expectancy, intervention heterogeneity, or other confounds explain observed HRV/RSA or symptom changes; whether later reviews or trials confirm, weaken, or supersede this 2021 evidence base; whether this source should be cited as acceptable background or kept only as a decoy-resistance example of preliminary clinical translation
source_limits: systematic review limited to PubMed and Scopus searches through July 2021; only six included articles; review population restricted to adult PTSD and OCD patients and mindfulness- or compassion-related interventions with physiological measures; several included clinical studies had small sample sizes, lacked power analysis, lacked randomization, or were not outcome trials; one included RCT record is described as a protocol; source is useful for clinical-adjacent preliminary evidence and methodological caution, not for mechanistic validation of PVT
reviewer_notes: Machine-assisted draft from full PDF extraction for human review. Useful for testing whether the skill distinguishes preliminary PVT-framed clinical-adjacent findings from proof of the full theory. Short extracted anchors for reviewer verification: "Six articles met the inclusion criteria"; "very limited research"; "underpowered and poorly designed RCTs may be overrated". Pair with direct clinical/intervention studies and independent RSA-methodology sources before using in the claim matrix.

### candidate-tonhajzerova-2011-cardiac-vagal-control

group: adjacent_supportive_pending_appraisal
metadata_status: candidate_metadata_recorded_with_page_gap
provisional_role: background autonomic/clinical review candidate
intake_metadata_ref: goldset_intake.md source_id candidate-tonhajzerova-2011-cardiac-vagal-control
doi: 10.2478/v10201-011-0011-y
review_link: https://doi.org/10.2478/v10201-011-0011-y
appraisal_status: not_appraised
reviewer_source_decision: TODO
access_status: TODO
full_text_reviewed: TODO
can_support: TODO
cannot_support: central PVT evidence
must_remain_uncertain: TODO
source_limits: page range unresolved; cite by DOI unless resolved
reviewer_notes: TODO

### candidate-hanazawa-2022-clinical-overview

group: adjacent_supportive_pending_appraisal
metadata_status: candidate_metadata_recorded
provisional_role: clinical overview / supportive-conceptual candidate
intake_metadata_ref: goldset_intake.md source_id candidate-hanazawa-2022-clinical-overview
doi: 10.11477/mf.1416202169
review_link: https://doi.org/10.11477/mf.1416202169
appraisal_status: not_appraised
reviewer_source_decision: TODO
access_status: TODO
full_text_reviewed: TODO
can_support: TODO
cannot_support: central mechanistic evidence or independent validation
must_remain_uncertain: TODO
source_limits: Japanese clinical/background context unless reliable metadata or English abstract supports classification
reviewer_notes: TODO

### candidate-grossman-taylor-2007-rsa

group: critique_methodology
metadata_status: candidate_metadata_recorded
provisional_role: methodological critique / RSA measurement caveats candidate
intake_metadata_ref: goldset_intake.md source_id candidate-grossman-taylor-2007-rsa
doi: 10.1016/j.biopsycho.2005.11.014
review_link: https://doi.org/10.1016/j.biopsycho.2005.11.014
appraisal_status: abstract_metadata_reviewed_full_text_unavailable
reviewer_source_decision: undecided
access_status: paywalled full text not accessible to reviewer; ScienceDirect abstract/preview, PubMed metadata, DOI metadata, and University of Birmingham record reviewed
full_text_reviewed: no
can_support: metadata-level identification of this source as Grossman and Taylor's 2007 Biological Psychology article on RSA, cardiac vagal tone, evolution, and biobehavioral functions; abstract-level support that RSA is often used as an index of cardiac vagal tone but has major interpretation caveats; abstract-level support that respiratory parameters, within-person versus between-person differences, momentary physical activity, beta-adrenergic tone, and RSA/cardiac-vagal-tone dissociation can complicate RSA interpretation; abstract-level support that the article critiques PVT evolution-based claims about RSA, vagal tone, behavior, and the evolution of vagal control of heart-rate variability; abstract-level support that RSA may still be a reasonable reflection of cardiac vagal tone when these complexities are considered
cannot_support: fine-grained claim-level adjudication without full text; direct quotation or page-specific evidence beyond public metadata/abstract/preview; blanket refutation of all autonomic-regulation findings; claim that RSA is useless or meaningless; formal field consensus; clinical efficacy or trauma-therapy claims; use as a gold evidence source before full-text appraisal
must_remain_uncertain: exact full-text argument structure and evidence basis; how the article handles specific PVT claims beyond the public abstract/preview; whether all relevant caveats are equally emphasized in the full text; which details later Grossman/Taylor/Grossman et al. sources modify, sharpen, or supersede; whether this source should become gold or acceptable after full-text review
source_limits: abstract/metadata/public-preview review only; full text is paywalled for the current reviewer; use as a candidate RSA-methodology critique locator and source-priority signal, not as appraised gold evidence; do not use for fine-grained evidence bases until a reviewer with full-text access checks the article
reviewer_notes: Machine-assisted access-limited draft for human review. Public records verify title, authors, journal, volume, issue, pages 263-285, DOI, and abstract-level RSA caveats. Because full text is not accessible, keep this source out of fine-grained evidence bases and rely on full-text-reviewed sources such as Grossman 2023/2026 and Taylor et al. 2022 for central claims already appraised in this worksheet.

### candidate-grossman-2023-five-premises

group: critique_core_premises
metadata_status: candidate_metadata_recorded
provisional_role: major critique / actively contested candidate
intake_metadata_ref: goldset_intake.md source_id candidate-grossman-2023-five-premises
doi: 10.1016/j.biopsycho.2023.108589
review_link: https://doi.org/10.1016/j.biopsycho.2023.108589
Former local PDF: Fundamental challenges and likely refutations of the five basic premises of the polyvagal theory.pdf
appraisal_status: human_reviewed
reviewer_source_decision: gold
access_status: open-access full text reviewed during MVP intake; repository no longer stores the local PDF copy; DOI publisher page also available
full_text_reviewed: yes for machine-assisted draft extraction; future human verification should use the DOI/publisher page or a separately obtained full text
can_support: major single-author review critique of five stated basic premises of PVT; critique that PVT depends heavily on RSA as the main noninvasive index of vagal processes; critique that RSA is an imperfect, indirect, and condition-dependent marker of cardiac vagal tone rather than general vagal tone; critique that dorsal motor nucleus mediation of massive bradycardia, vasovagal syncope, emotional freezing, or trauma-related dissociation is unsupported; critique that nA-mediated cardiac vagal control, myelinated cardiac vagal fibers, and RSA-like cardiorespiratory interactions are not uniquely mammalian; critique that broad claims about mammalian autonomic repurposing for sociality are not supported by comparative biology; critique that emotion, facial expression, vocalization, bronchomotor tone, RSA, and cardiac vagal tone cannot be reduced to a single nucleus ambiguus or vagal mechanism; evidence that Grossman frames the five physiological premises as falsified or highly implausible, while relying on cited physiology/comparative-biology literature rather than new empirical data
cannot_support: formal field-wide consensus process; dismissal of all clinical metaphors; proof that every body-based or autonomic clinical practice is invalid; proof that broad autonomic regulation or cardiac vagal physiology is irrelevant to emotion or behavior; direct evidence about therapy efficacy, trauma treatment, SSP, or clinical outcomes; independent adjudication of Porges's later 2025 and 2026 clarifications without reading those paired sources; proof that critiques of physiological premises automatically refute all weaker clinical or metaphorical uses of PVT
must_remain_uncertain: whether Grossman's five-premise framing fully captures current PVT formulations; whether later Porges clarifications change the appraisal of specific claims; whether critiques of core physiological premises invalidate weaker clinical or metaphorical uses; whether the article's statements about expert consensus should be treated as a critic's synthesis rather than a formal consensus process; which component findings about autonomic regulation remain supported outside PVT-specific mechanisms; how to weight this 2023 single-author critique against Grossman et al. 2026, Porges 2025/2026, and independent neuroanatomy/RSA/comparative-physiology sources
source_limits: single-author review/critique, not a systematic review, meta-analysis, Delphi panel, professional-society statement, clinical-practice guideline, or original empirical study; use as central critique evidence for core physiological and evolutionary premises, not as a stand-alone final verdict on all PVT uses; article is Biological Psychology 180, Article 108589, DOI 10.1016/j.biopsycho.2023.108589
reviewer_notes: Machine-assisted draft from full-text extraction for human review. Central critique source for testing whether the skill avoids treating PVT-specific RSA, dorsal/ventral vagal, evolutionary, and sociality claims as settled. Short extracted anchors for reviewer verification: "category mistake"; "no credible evidence"; "not a direct measure". Pair with Grossman et al. 2026, Porges 2025 current-status, Porges 2026 response, and independent neuroanatomy/RSA/comparative-physiology sources before using in the claim matrix.

### candidate-grossman-2024-rsa

group: critique_methodology
metadata_status: candidate_metadata_recorded
provisional_role: RSA methodology / measurement caveats candidate
intake_metadata_ref: goldset_intake.md source_id candidate-grossman-2024-rsa
doi: 10.1016/j.biopsycho.2023.108739
review_link: https://doi.org/10.1016/j.biopsycho.2023.108739
Former local PDF: Respiratory sinus arrhythmia (RSA), vagal tone and biobehavioral integration- Beyond parasympathetic function.pdf
appraisal_status: human_reviewed
reviewer_source_decision: gold
access_status: open-access full text reviewed during MVP intake; repository no longer stores the local PDF copy; DOI publisher page also available
full_text_reviewed: yes for machine-assisted draft extraction; future human verification should use the DOI/publisher page or a separately obtained full text
can_support: major RSA-methodology review and conceptual critique; support that RSA is not equivalent to, nor a direct or invariably reliable measure of, cardiac vagal tone or central vagal outflow; support that RSA is at best an imperfect indirect proxy of cardiac vagal effects on heart rate, not whole-body vagal tone; support caveats including respiration rate and volume, cardiac aliasing, abrupt bradycardia, hypercapnia, beta-adrenergic sympathetic effects, central-vagal-output versus final cardiac-effect ambiguity, local cardiac influences, mechanical effects, ageing, and weak between-person validity; support that respiratory-circulatory and behavioral integration are central to RSA's adaptive meaning; support interpreting RSA as an evolutionarily entrenched cardiorespiratory and biobehavioral coordination phenomenon rather than merely a parasympathetic index
cannot_support: direct adjudication of all PVT clinical claims; proof that RSA is useless or meaningless; proof that all broad autonomic-regulation findings are invalid; proof that clinical interventions validate or fail to validate PVT; formal field consensus; clinical efficacy, trauma-therapy, or SSP claims; page-specific claims about sources cited by this review without checking those sources directly
must_remain_uncertain: how much of RSA's clinical usefulness survives each caveat in a given study design; whether specific PVT claims about ventral vagal pathways, social engagement, or clinical interventions are supported by independent evidence; whether individual empirical studies adequately controlled respiration, sympathetic tone, and context; how to weight this RSA-focused critique against Porges's RSA-specific rebuttals and newer direct-measurement work
source_limits: single-author theoretical/review article focused on RSA measurement, vagal tone, and biobehavioral integration; not a clinical trial, systematic review, meta-analysis, professional-society statement, or direct therapy-efficacy source; use as central measurement-caveat evidence and conceptual RSA critique, not as a stand-alone verdict on all PVT mechanisms or clinical applications
reviewer_notes: Machine-assisted draft from full PDF extraction for human review. This replaces the earlier access-limited draft. Central source for testing whether the skill avoids treating RSA/HRV as a direct biomarker of vagal tone, safety, or PVT-specific ventral vagal activation. Short extracted anchors for reviewer verification: "neither an invariably reliable index of cardiac vagal tone"; "At best, it is an imprecise proxy." Pair with Grossman & Taylor 2007, Grossman 2023/2026, Porges 2025/2026, Taylor et al. 2022, and direct empirical/clinical studies before using in the claim matrix.

### candidate-grossman-2026-untenable

group: critique_core_premises
metadata_status: candidate_metadata_recorded
provisional_role: multi-author expert critique/commentary candidate
intake_metadata_ref: goldset_intake.md source_id candidate-grossman-2026-untenable
doi: 10.36131/cnfioritieditore20260110
review_link: https://doi.org/10.36131/cnfioritieditore20260110
Former local PDF: 10_Grossmanetal_Clinical26-1.pdf
appraisal_status: human_reviewed
reviewer_source_decision: gold
access_status: open-access full text reviewed during MVP intake; repository no longer stores the local PDF copy; publisher page also available through DOI
full_text_reviewed: yes for machine-assisted draft extraction; future human verification should use the DOI/publisher page or a separately obtained full text
can_support: major multi-author expert critique of PVT's core physiological and evolutionary premises; critique that RSA/respiratory heart-rate variability should not be treated as a direct or consistently reliable measure of central vagal outflow, cardiac vagal tone, or general vagal activity; critique of PVT dorsal/ventral vagal pathway mapping, sequential autonomic ladder, and dorsal vagal shutdown claims in humans; critique of mammalian-uniqueness and sociality/evolution claims, including claims about myelinated vagal fibers and cardiorespiratory coupling; distinction that psychological and clinical concepts associated with PVT may predate PVT and may have value apart from PVT's proposed physiological framework
cannot_support: formal field-wide consensus process; proof that every clinical or metaphorical use of PVT is useless; proof that broad autonomic regulation, HRV/RSA, trauma physiology, or body-based clinical work are invalid; independent adjudication of Porges's rebuttal without reading the paired response
must_remain_uncertain: whether the article's expert critique should be treated as formal field consensus; whether weaker clinical or metaphorical versions of PVT retain usefulness; which specific PVT claims survive when separated from strong mechanistic and evolutionary claims; how Porges's 2026 response addresses or reframes these objections
source_limits: critique/commentary and expert evaluation; page range 100-112 for Grossman et al. 2026; 169-184 refers to the Porges 2025 article named in the title; author group is expert and multi-author but not a Delphi panel, professional-society statement, systematic review, or meta-analysis; use as central critique evidence, not as a stand-alone final consensus verdict
reviewer_notes: Machine-assisted draft from full PDF extraction for human review. Central source for the benchmark's overstatement-risk test because it directly contests PVT's RSA measurement, dorsal/ventral vagal mapping, autonomic hierarchy, dorsal vagal shutdown, mammalian-uniqueness, and sociality/evolution claims. Pair with Porges 2026 response and independent RSA, neuroanatomy, and comparative-physiology sources before using in the claim matrix.

### candidate-doody-burghardt-dinets-2023-sociality

group: critique_evolution_sociality
metadata_status: candidate_metadata_recorded
provisional_role: evolutionary/sociality critique candidate
intake_metadata_ref: goldset_intake.md source_id candidate-doody-burghardt-dinets-2023-sociality
doi: 10.1016/j.biopsycho.2023.108569
review_link: https://doi.org/10.1016/j.biopsycho.2023.108569
appraisal_status: not_appraised
reviewer_source_decision: TODO
access_status: TODO
full_text_reviewed: TODO
can_support: TODO
cannot_support: sole refutation of all PVT claims
must_remain_uncertain: TODO
source_limits: TODO
reviewer_notes: TODO

### candidate-walz-grossman-2024-facts

group: critique_clinical_facing
metadata_status: candidate_metadata_recorded_with_language_caveat
provisional_role: critique / clinical-facing commentary candidate, not primary empirical evidence
intake_metadata_ref: goldset_intake.md source_id candidate-walz-grossman-2024-facts
doi: 10.30820/2364-1517-2024-2-163
review_link: https://doi.org/10.30820/2364-1517-2024-2-163
appraisal_status: not_appraised
reviewer_source_decision: TODO
access_status: TODO
full_text_reviewed: TODO
can_support: TODO
cannot_support: primary empirical evidence
must_remain_uncertain: TODO
source_limits: German source; classification must not depend on unsupported machine translation
reviewer_notes: TODO

### candidate-neuhuber-berthoud-2022-vagus-anatomy

group: critique_neuroanatomy
metadata_status: candidate_metadata_recorded
provisional_role: neuroanatomical critique candidate
intake_metadata_ref: goldset_intake.md source_id candidate-neuhuber-berthoud-2022-vagus-anatomy
doi: 10.1016/j.biopsycho.2022.108425
review_link: https://doi.org/10.1016/j.biopsycho.2022.108425
appraisal_status: abstract_metadata_reviewed_full_text_unavailable
reviewer_source_decision: undecided
access_status: paywalled full text not accessible to reviewer; PubMed, FAU CRIS, DOI metadata, and limited ScienceDirect public snippets reviewed
full_text_reviewed: no
can_support: metadata-level identification of this source as a 2022 Biological Psychology review article by Neuhuber and Berthoud on functional anatomy of the vagus system and PVT compliance; abstract-level support that the article reviews basic vagal anatomy in light of HRV use and PVT; abstract-level support that relevant anatomy includes dorsal motor nucleus, nucleus ambiguus, nucleus tractus solitarii, spinal trigeminal and paratrigeminal nuclei, and NTS integration of visceral and somatic afferents; public ScienceDirect snippet-level support that the authors caution against reducing the complexity of a social engagement system to a new ventral vagus
cannot_support: fine-grained claim-level adjudication without full text; direct quotation or page-specific evidence beyond public metadata/snippets; blanket proof that all clinical or metaphorical uses of PVT are invalid; formal field consensus; use as a gold evidence source before full-text appraisal; appraisal of corrected details without checking the 2023 corrigendum
must_remain_uncertain: exact claim scope and evidentiary basis inside the full article; whether the full text supports specific claims about dorsal/ventral vagal mapping, emotional freezing, dorsal vagal complex usage, or phylogenetic tenets; how the 2023 corrigendum changes or qualifies any anatomical wording; whether this source should become gold or acceptable after full-text review
source_limits: abstract/metadata/public-snippet review only; full text is paywalled for the current reviewer; use as a candidate neuroanatomy critique locator and source-priority signal, not as appraised gold evidence; pair with candidate-neuhuber-berthoud-2023-corrigendum before any full-text-based claim matrix use
reviewer_notes: Machine-assisted access-limited draft for human review. The public records verify title, authors, year, journal, volume, article number, DOI, review-article status, and abstract-level topic. Because the full text is not accessible, keep this source out of fine-grained evidence bases until a reviewer with full-text access can inspect the article and corrigendum.

### candidate-neuhuber-berthoud-2023-corrigendum

group: correction_corrigendum
metadata_status: candidate_metadata_recorded
provisional_role: correction/corrigendum record candidate
intake_metadata_ref: goldset_intake.md source_id candidate-neuhuber-berthoud-2023-corrigendum
doi: 10.1016/j.biopsycho.2023.108554
review_link: https://doi.org/10.1016/j.biopsycho.2023.108554
appraisal_status: not_appraised
reviewer_source_decision: TODO
access_status: published erratum/corrigendum record recoverable via PubMed and ScienceDirect
full_text_reviewed: TODO
can_support: corrected details for the 2022 neuroanatomy critique if verified
cannot_support: independent evidence beyond corrected details
must_remain_uncertain: TODO
source_limits: Biological Psychology, 179, Article 108554, DOI 10.1016/j.biopsycho.2023.108554; corrected article DOI is 10.1016/j.biopsycho.2022.108425
reviewer_notes: TODO

### candidate-taylor-wang-leite-2022-cardiorespiratory-phylogeny

group: critique_comparative_physiology
metadata_status: candidate_metadata_recorded
provisional_role: comparative physiology / evolutionary-mechanism critique candidate
intake_metadata_ref: goldset_intake.md source_id candidate-taylor-wang-leite-2022-cardiorespiratory-phylogeny
doi: 10.1016/j.biopsycho.2022.108382
review_link: https://doi.org/10.1016/j.biopsycho.2022.108382
Former local PDF: An overview of the phylogeny of cardiorespiratory control in vertebrates with some reflections on the ‘Polyvagal Theory’ .pdf
appraisal_status: human_reviewed
reviewer_source_decision: gold
access_status: open-access full text reviewed during MVP intake; repository no longer stores the local PDF copy; DOI publisher page also available
full_text_reviewed: yes for machine-assisted draft extraction; future human verification should use the DOI/publisher page or a separately obtained full text
can_support: comparative-physiology review evidence that vagal control of heart rate, heart-rate variability, and cardiorespiratory interactions are distributed across vertebrate phylogeny rather than uniquely mammalian; critique of strong PVT mammalian-uniqueness claims about RSA-like cardiorespiratory interactions, myelinated cardiac vagal efferent fibres, and a uniquely mammalian ventral vagal/nucleus ambiguus pathway; evidence synthesis that representatives of all vertebrate groups show inhibitory vagal tonus and respiration-related phasic vagal modulation of heart rate; evidence synthesis that CRI similar to RSA has been identified in air-breathing vertebrates including birds, snakes, lizards, toads, and lungfish; evidence synthesis that myelinated fast-conducting cardiac vagal fibres have been described in shark, bony fish, lungfish, birds, and mammals; distinction that mammalian RSA may be phylogenetically rooted in earlier cardiorespiratory interaction systems rather than a wholly novel mammalian social-engagement mechanism
cannot_support: full refutation of every PVT claim or clinical application; direct adjudication of whether the vagus nerve supports social engagement, calming, or socializing in humans; clinical usefulness or therapeutic efficacy claims; trauma-therapy claims; formal field-wide consensus; proof that all broad autonomic regulation findings are invalid; proof that all PVT reformulations fail after accounting for comparative physiology limits
must_remain_uncertain: whether PVT's social-engagement or clinical claims survive when separated from strong mammalian-uniqueness claims; whether later Porges formulations can accommodate the comparative physiology evidence; which exact neural generators produce RSA-like cardiorespiratory interactions in every non-mammalian group where mechanisms remain partly putative; whether RSA-like CRI in other vertebrates has the same behavioral meaning as mammalian RSA; how this review should be weighted against Porges's current author-side responses
source_limits: comparative physiology review focused on cardiorespiratory control, vagal heart-rate modulation, RSA-like CRI, and vertebrate phylogeny; not a psychotherapy, trauma, clinical-outcome, social-behavior, systematic-review, meta-analysis, or formal-consensus source; authors explicitly limit their engagement to comparative physiology and state that they did not address evidence for a vagus-nerve role in social engagement; use as central evidence against strong mammalian-uniqueness and evolutionary-mechanism claims, not as a stand-alone verdict on the whole theory
reviewer_notes: Machine-assisted draft from full-text extraction for human review. Central source for testing whether the skill distinguishes broad comparative autonomic evidence from PVT-specific evolutionary and mammalian-uniqueness claims. Short extracted anchors for reviewer verification: "mammals are not set apart"; "have not addressed the evidence". Pair with Monteiro et al. 2018 lungfish evidence, Grossman 2023/2026 critiques, Porges 2025/2026 author-side sources, and any independent sociality/clinical sources before using in the claim matrix.

### candidate-monteiro-taylor-sartori-cruz-rantin-leite-2018-lungfish

group: comparative_physiology_lungfish
metadata_status: candidate_metadata_recorded
provisional_role: comparative physiology / lungfish evidence candidate
intake_metadata_ref: goldset_intake.md source_id candidate-monteiro-taylor-sartori-cruz-rantin-leite-2018-lungfish
doi: 10.1126/sciadv.aaq0800
review_link: https://doi.org/10.1126/sciadv.aaq0800
appraisal_status: not_appraised
reviewer_source_decision: TODO
access_status: open-access article available through PMC or Science Advances according to human intake
full_text_reviewed: TODO
can_support: TODO
cannot_support: standalone appraisal of PVT as a whole
must_remain_uncertain: TODO
source_limits: not appraised; use only for exact comparative physiology claims after review
reviewer_notes: TODO

### candidate-porges-et-al-2014-listening-project-protocol

group: clinical_acoustic_intervention
metadata_status: candidate_metadata_recorded
provisional_role: precursor acoustic/listening intervention study candidate
intake_metadata_ref: goldset_intake.md source_id candidate-porges-et-al-2014-listening-project-protocol
doi: 10.3389/fped.2014.00080
review_link: https://doi.org/10.3389/fped.2014.00080
appraisal_status: not_appraised
reviewer_source_decision: TODO
access_status: open access
full_text_reviewed: TODO
can_support: TODO
cannot_support: strong validation of SSP, PVT mechanisms, or broad clinical efficacy
must_remain_uncertain: TODO
source_limits: preliminary intervention evidence; not appraised
reviewer_notes: TODO

### candidate-kawai-et-al-2023-ssp-adult-autism

group: clinical_acoustic_intervention
metadata_status: candidate_metadata_recorded
provisional_role: SSP exploratory pilot study candidate
intake_metadata_ref: goldset_intake.md source_id candidate-kawai-et-al-2023-ssp-adult-autism
doi: 10.3390/ijerph20064862
review_link: https://doi.org/10.3390/ijerph20064862
appraisal_status: not_appraised
reviewer_source_decision: TODO
access_status: open access
full_text_reviewed: TODO
can_support: TODO
cannot_support: strong efficacy evidence or PVT-specific mechanistic validation
must_remain_uncertain: TODO
source_limits: exploratory pilot; not appraised
reviewer_notes: TODO

### candidate-heilman-et-al-2023-ssp-autism-single-arm

group: clinical_acoustic_intervention
metadata_status: candidate_metadata_recorded
provisional_role: SSP prospective single-arm study candidate
intake_metadata_ref: goldset_intake.md source_id candidate-heilman-et-al-2023-ssp-autism-single-arm
doi: 10.5281/zenodo.8018744
review_link: https://doi.org/10.5281/zenodo.8018744
additional_locator: parent/concept DOI 10.5281/zenodo.8018743; https://doi.org/10.5281/zenodo.8018743
appraisal_status: not_appraised
reviewer_source_decision: TODO
access_status: public OADD PDF and Zenodo metadata record available; Zenodo record DOI 10.5281/zenodo.8018744; parent/concept DOI 10.5281/zenodo.8018743
full_text_reviewed: TODO
can_support: TODO
cannot_support: randomized evidence, strong causal evidence, or PVT-specific mechanistic validation
must_remain_uncertain: TODO
source_limits: single-arm; Zenodo record and parent/concept DOIs are available, but no separate journal-assigned DOI has been recovered; not appraised
reviewer_notes: TODO

### candidate-porges-et-al-2019-fni-autonomic-regulation

group: clinical_coregulation_intervention
metadata_status: candidate_metadata_recorded
provisional_role: FNI autonomic-regulation RCT evidence candidate
intake_metadata_ref: goldset_intake.md source_id candidate-porges-et-al-2019-fni-autonomic-regulation
doi: 10.1002/dev.21841
review_link: https://doi.org/10.1002/dev.21841
appraisal_status: not_appraised
reviewer_source_decision: TODO
access_status: publisher/metadata recoverable; full text may depend on access
full_text_reviewed: TODO
can_support: TODO
cannot_support: direct validation of the full Polyvagal Theory or of PVT-specific mechanisms
must_remain_uncertain: TODO
source_limits: intervention includes multiple components; not appraised
reviewer_notes: TODO

### candidate-welch-et-al-2020-fni-follow-up

group: clinical_coregulation_intervention
metadata_status: candidate_metadata_recorded
provisional_role: FNI follow-up autonomic-regulation evidence candidate
intake_metadata_ref: goldset_intake.md source_id candidate-welch-et-al-2020-fni-follow-up
doi: 10.1371/journal.pone.0236930
review_link: https://doi.org/10.1371/journal.pone.0236930
appraisal_status: not_appraised
reviewer_source_decision: TODO
access_status: open access
full_text_reviewed: TODO
can_support: TODO
cannot_support: direct proof of PVT-specific mechanisms or broad trauma-therapy validation
must_remain_uncertain: TODO
source_limits: follow-up subset/attrition caveat from human intake; not appraised
reviewer_notes: TODO

### candidate-rajabalee-et-al-2022-computer-altered-music-fnd

group: clinical_acoustic_intervention
metadata_status: candidate_metadata_recorded
provisional_role: case report / acoustic neuromodulation candidate
intake_metadata_ref: goldset_intake.md source_id candidate-rajabalee-et-al-2022-computer-altered-music-fnd
doi: 10.1097/HRP.0000000000000341
review_link: https://doi.org/10.1097/HRP.0000000000000341
appraisal_status: not_appraised
reviewer_source_decision: TODO
access_status: metadata recoverable; full text may depend on access
full_text_reviewed: TODO
can_support: TODO
cannot_support: generalizable evidence of SSP efficacy or PVT-specific mechanism
must_remain_uncertain: TODO
source_limits: case report; low-level clinical evidence; not appraised
reviewer_notes: TODO

### candidate-rogowski-et-al-2024-ajot-ssp-young-children

group: clinical_acoustic_intervention
metadata_status: candidate_metadata_recorded
provisional_role: SSP young-children occupational-therapy abstract candidate
intake_metadata_ref: goldset_intake.md source_id candidate-rogowski-et-al-2024-ajot-ssp-young-children
doi: 10.5014/ajot.2024.78S2-PO332
review_link: https://doi.org/10.5014/ajot.2024.78S2-PO332
appraisal_status: not_appraised
reviewer_source_decision: TODO
access_status: Ovid/EBSCO metadata record recoverable; full abstract record may require database access
full_text_reviewed: TODO
can_support: TODO
cannot_support: full peer-reviewed trial evidence, strong efficacy evidence, or PVT-specific mechanistic validation
must_remain_uncertain: TODO
source_limits: American Journal of Occupational Therapy, 78(Suppl. 2), abstract/poster PO332, DOI 10.5014/ajot.2024.78S2-PO332; do not rely on page range without publisher reconciliation
reviewer_notes: TODO

## Decoy Appraisal Queue

Decoys may be cited only as examples of overstatement risk, never as evidence of
scientific support.

### candidate-decoy-polyvagal-institute-what-is

group: decoy_public_facing
metadata_status: decoy_metadata_recorded
intake_metadata_ref: goldset_intake.md source_id candidate-decoy-polyvagal-institute-what-is
appraisal_status: human_reviewed
reviewer_source_decision: decoy
exact_url: https://www.polyvagalinstitute.org/whatispolyvagaltheory
review_link: https://www.polyvagalinstitute.org/whatispolyvagaltheory
access_date: 2026-06-03
overstatement_risk_identified: public-facing institute page frames PVT as a scientific framework and presents its concepts, diagrams, videos, principles, applications, FAQ, trauma framing, and healthcare/classroom guidance in accessible educational language; useful decoy for testing whether the skill treats institute/public-facing explanation, clinical uptake, applications, diagrams, or authority-adjacent framing as evidence of scholarly consensus; page includes strong-sounding theory claims about hierarchy, neuroception, co-regulation, ventral vagal regulation, dorsal vagal shutdown, trauma, health, resilience, and recovery; nuance: the page also cautions that applied metaphors are interpretations and should be distinguished from foundational science, so the decoy should test both over-endorsement and failure to notice the page's own caveat
must_not_be_used_as: evidence of scientific support or consensus; peer-reviewed scholarly source; independent validation; source for claim-level physiology, neuroanatomy, evolutionary biology, trauma-treatment efficacy, or field-state judgments; evidence that criticism is resolved or based only on misunderstanding
reviewer_notes: Machine-assisted draft from public webpage review for human review. Decoy role only. Short extracted anchors for reviewer verification: "scientific framework"; "grounded in neuroscience"; "Trauma and the Nervous System". Use this source only to identify popularized/public-facing overstatement risks and communication framing; keep it separate from scholarly evidence tables.

### candidate-decoy-ifm-ptsd-polyvagal

group: decoy_clinical_marketing
metadata_status: decoy_metadata_recorded
intake_metadata_ref: goldset_intake.md source_id candidate-decoy-ifm-ptsd-polyvagal
appraisal_status: not_appraised
exact_url: https://www.ifm.org/articles/understanding-ptsd-from-a-polyvagal-perspective
review_link: https://www.ifm.org/articles/understanding-ptsd-from-a-polyvagal-perspective
access_date: 2026-05-18
overstatement_risk_identified: TODO
must_not_be_used_as: evidence of scientific support or consensus
reviewer_notes: TODO

### candidate-decoy-khiron-ladder

group: decoy_clinical_marketing
metadata_status: decoy_metadata_recorded
intake_metadata_ref: goldset_intake.md source_id candidate-decoy-khiron-ladder
appraisal_status: human_reviewed
reviewer_source_decision: decoy
exact_url: https://khironclinics.com/blog/polyvagal-theory-a-ladder-of-nervous-states/
review_link: https://khironclinics.com/blog/polyvagal-theory-a-ladder-of-nervous-states/
access_date: 2026-06-03
overstatement_risk_identified: clinical-marketing/public-facing trauma page presents PVT through a simplified ladder of nervous states; useful decoy for testing whether the skill treats sequential ladder language, clinic authority, trauma-treatment framing, expert-name marketing, or treatment calls to action as scholarly evidence; page states the ladder is predictable and sequential, links PTSD stress and immobilisation to movement through the ladder, frames safe/social as a high or peak state, and describes dorsal-vagal shutdown/collapse/dissociation language in strong clinical terms; useful for detecting answers that overstate hierarchy, dorsal-vagal shutdown, or clinical applicability without source-quality calibration
must_not_be_used_as: evidence of scientific support or consensus; peer-reviewed scholarly source; independent validation; source for claim-level neurophysiology, evolutionary biology, trauma-treatment efficacy, dorsal-vagal shutdown mechanisms, dissociation mechanisms, or field-state judgments; evidence that PVT-informed treatment is established
reviewer_notes: Machine-assisted draft from public webpage review for human review. Decoy role only. Short extracted anchors for reviewer verification: "states can only be moved through in sequence"; "important implications for clinical application"; "massive activation of the dorsal vagus". Use only to identify popularized ladder/clinical-marketing overstatement risks; keep separate from scholarly evidence tables.

### candidate-decoy-positivepsychology-exercises

group: decoy_public_facing
metadata_status: decoy_metadata_recorded
intake_metadata_ref: goldset_intake.md source_id candidate-decoy-positivepsychology-exercises
appraisal_status: not_appraised
exact_url: https://positivepsychology.com/polyvagal-theory/
review_link: https://positivepsychology.com/polyvagal-theory/
access_date: 2026-05-18
overstatement_risk_identified: TODO
must_not_be_used_as: evidence of scientific support or consensus
reviewer_notes: TODO

### candidate-decoy-rhythm-of-regulation-deb-dana

group: decoy_training_public_facing
metadata_status: decoy_metadata_recorded
intake_metadata_ref: goldset_intake.md source_id candidate-decoy-rhythm-of-regulation-deb-dana
appraisal_status: not_appraised
exact_url: https://www.rhythmofregulation.com/
review_link: https://www.rhythmofregulation.com/
access_date: 2026-05-18
overstatement_risk_identified: TODO
must_not_be_used_as: evidence of scientific support or consensus
reviewer_notes: TODO

### candidate-decoy-unyte-ssp-product

group: decoy_product_marketing
metadata_status: decoy_metadata_recorded
intake_metadata_ref: goldset_intake.md source_id candidate-decoy-unyte-ssp-product
appraisal_status: not_appraised
exact_url: https://integratedlistening.com/products/ssp-safe-sound-protocol/
review_link: https://integratedlistening.com/products/ssp-safe-sound-protocol/
access_date: 2026-05-18
overstatement_risk_identified: TODO
must_not_be_used_as: evidence of scientific support or consensus
reviewer_notes: TODO

## Metadata Recovery Queue

These follow-up records cannot be used as evidence until source content is
verified and reviewer appraisal is complete.

### followup-heilman-2023-journal-doi

group: metadata_followup
related_source_id: candidate-heilman-et-al-2023-ssp-autism-single-arm
metadata_status: zenodo_record_and_parent_doi_recovered
review_link: https://doi.org/10.5281/zenodo.8018744
additional_locator: parent/concept DOI 10.5281/zenodo.8018743; https://doi.org/10.5281/zenodo.8018743
needed_before_appraisal: confirm whether any separate journal-assigned DOI exists; otherwise use Zenodo record DOI 10.5281/zenodo.8018744 as the stable locator and note parent/concept DOI 10.5281/zenodo.8018743
appraisal_status: metadata_partially_recovered_not_appraised
reviewer_notes: TODO

### retired-kishimoto-et-al-2023-ssp-children-autism

group: retired_metadata_lead
related_source_id: none
metadata_status: retired_longdom_only_record
review_link: none; retired lead, do not review unless a stable non-Longdom scholarly record is recovered
needed_before_appraisal: do not use unless a stable non-Longdom scholarly record is recovered and venue/source-quality concerns are resolved
appraisal_status: retired_not_appraised
reviewer_notes: TODO

### unresolved-additional-ssp-rest-restore-voicepro

group: metadata_recovery
provisional_role: possible clinical/acoustic intervention sources
metadata_status: marketing_summary_only
review_link: none; no stable scholarly metadata recovered
needed_before_appraisal: do not add SSP, Rest & Restore, VoicePro, or similar studies mentioned only in marketing summaries until stable scholarly metadata is recovered
appraisal_status: metadata_missing_not_appraised
reviewer_notes: TODO

## Claim Appraisal Matrix

### support-influential-clinically-popular

expected_behavior: support_if_confirmed_by_appraisal
claim: Polyvagal theory is influential and clinically popular.
candidate_source_ids_to_check: TODO
reviewer_decision: TODO
evidence_strength: undecided
evidence_basis: TODO
source_limits: TODO

### support-adjacent-autonomic-social-safety

expected_behavior: support_if_confirmed_by_appraisal
claim: Some adjacent ideas about autonomic regulation and social safety may have broader support than the full theory.
candidate_source_ids_to_check: TODO
reviewer_decision: TODO
evidence_strength: undecided
evidence_basis: TODO
source_limits: TODO

### reject-settled-neuroscience

expected_behavior: reject_if_confirmed_by_appraisal
claim: Polyvagal theory is settled neuroscience.
candidate_source_ids_to_check: TODO
reviewer_decision: TODO
evidence_strength: undecided
evidence_basis: TODO
source_limits: TODO

### reject-general-autonomic-proves-full-theory

expected_behavior: reject_if_confirmed_by_appraisal
claim: General autonomic regulation evidence proves the full Polyvagal theory.
candidate_source_ids_to_check: TODO
reviewer_decision: TODO
evidence_strength: undecided
evidence_basis: TODO
source_limits: TODO

### reject-wholly-useless-or-fully-disproven

expected_behavior: reject_if_confirmed_by_appraisal
claim: Polyvagal theory is entirely useless, disproven, or irrelevant.
candidate_source_ids_to_check: TODO
reviewer_decision: TODO
evidence_strength: undecided
evidence_basis: TODO
source_limits: TODO

### preserve-uncertainty-mechanistic-evolutionary-claims

expected_behavior: preserve_uncertainty_if_confirmed_by_appraisal
uncertainty: Which specific mechanistic and evolutionary claims remain contested, weakly supported, or outside the reviewed source basis.
candidate_source_ids_to_check: TODO
reviewer_decision: TODO
evidence_strength: undecided
evidence_basis: TODO
source_limits: TODO

### preserve-uncertainty-clinical-usefulness

expected_behavior: preserve_uncertainty_if_confirmed_by_appraisal
uncertainty: Whether clinical usefulness claims are supported by direct evidence, indirect plausibility, clinician uptake, or popularized framing.
candidate_source_ids_to_check: TODO
reviewer_decision: TODO
evidence_strength: undecided
evidence_basis: TODO
source_limits: TODO

## Required Distinction Matrix

### distinction-general-ans-vs-specific-pvt

distinction: Well-supported general autonomic nervous system findings versus Porges's specific theoretical claims.
candidate_source_ids_to_check: TODO
reviewer_decision: TODO
evidence_basis: TODO

### distinction-clinical-usefulness-vs-mechanism

distinction: Clinical or therapeutic usefulness claims versus physiological mechanism claims.
candidate_source_ids_to_check: TODO
reviewer_decision: TODO
evidence_basis: TODO

### distinction-popularized-vs-research-claims

distinction: Popularized trauma-regulation claims versus source-supported research claims.
candidate_source_ids_to_check: TODO
reviewer_decision: TODO
evidence_basis: TODO

### distinction-adjacent-support-vs-full-theory-proof

distinction: Adjacent support for autonomic regulation or social safety versus proof of the full Polyvagal theory.
candidate_source_ids_to_check: TODO
reviewer_decision: TODO
evidence_basis: TODO

### distinction-counts-vs-reviewed-consensus

distinction: Source count or citation count versus reviewed consensus or evidence strength.
candidate_source_ids_to_check: TODO
reviewer_decision: TODO
evidence_basis: TODO

### distinction-broad-ans-vs-contested-pvt-claims

distinction: Broad autonomic-regulation findings versus Porges's specific contested physiological, mechanistic, and evolutionary claims.
candidate_source_ids_to_check: TODO
reviewer_decision: TODO
evidence_basis: TODO

## Activation Readiness

activation_mode: active MVP with search-log waiver
activation_readiness_record: mvp_source_access_record.md
active_json_fixture: ../../polyvagal-theory-consensus-overstatement.draft.json
all_core_metadata_verified_for_active_mvp: yes, limited to selected MVP sources
all_decoy_urls_and_access_dates_recorded_for_active_mvp: yes, limited to selected MVP decoys
all_claims_have_evidence_basis_for_active_mvp: yes, in active JSON fixture
all_uncertainties_have_evidence_basis_for_active_mvp: yes, in active JSON fixture
all_required_distinctions_have_evidence_basis_for_active_mvp: yes, in active JSON fixture
copyright_or_private_text_absent_from_repo_fixture: yes; local PDF cache removed from repository; retained access basis is metadata, DOI/publisher pages, and reviewer notes
second_review_complete: no
full_reproducible_search_benchmark_ready: no
activation_decision: active_mvp_with_search_log_waiver

This worksheet still contains draft and follow-up sections for a broader future
benchmark. Those unresolved sections do not expand the active fixture beyond the
MVP boundary recorded in `mvp_source_access_record.md`,
`reviewer_checklist.md`, and the active JSON fixture.
