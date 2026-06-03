# Gold-Set Intake

Gold-set ID: polyvagal-theory-consensus-overstatement
Gold-set title: Polyvagal Theory Consensus Overstatement
Status: active MVP intake with search-log waiver

Do not use this file as source truth by itself. A human reviewer must check what
each source does and does not support before any fixture can become active.

## 1. Evaluation Frame

Narrow research or evaluation question:

- Can the skill avoid overstating consensus around Polyvagal theory in clinical
  psychology, trauma therapy, and affective neuroscience?
- Focus areas: autonomic nervous system regulation, vagal tone, social
  engagement, trauma responses, and therapeutic applications.
- Human narrowing still required: executed search record, actual source corpus,
  source-access records for each selected source, and reviewer appraisal before
  fixture authoring.

Scholarly failure mode being tested:

- Field uncertainty collapsed into an overstated consensus claim.
- Related risks: cherry-picking, source-type confusion, decoy source accepted,
  and inaccurate synthesis.
- Related inverse failure mode: critique overreach, where serious criticism of
  specific Polyvagal Theory mechanisms is inflated into the claim that the whole
  theory is useless, fully disproven, or clinically irrelevant.
- The output must avoid both presenting Polyvagal theory as settled neuroscience
  and dismissing the whole theory as useless or disproven.

Target skill or skill group:

- Literature-map or synthesis skill group, especially `literature-review-mapper`
  style behavior. Confirm the exact skill before fixture authoring.

Expected output type:

- Bounded literature-map or synthesis output that explicitly separates reviewed
  support, disagreement, weak evidence, unresolved uncertainty, and popularized
  claims from source-supported claims.
- Expected calibration supplied by human intake, pending source appraisal:
  Polyvagal theory is influential and clinically popular, but several stronger
  mechanistic and evolutionary claims are contested; adjacent ideas about
  autonomic regulation and social safety may have broader support, but they
  should not be treated as proof of the full theory.

## 2. Source Discovery Plan

Search domains or databases to use:

- Broad academic discovery strategy, not general web search.
- PubMed / MEDLINE for biomedical, neuroscience, autonomic physiology,
  psychophysiology, and trauma-related literature.
- APA PsycInfo for psychology, clinical psychology, trauma therapy, affective
  science, attachment, and behavioral-science literature.
- Scopus and/or Web of Science for multidisciplinary citation tracing, review
  articles, and forward/backward citation discovery.
- Semantic Scholar as a practical discovery layer for related papers and
  citation networks.
- PubMed Central only for full-text access when available, not as the only
  discovery database.
- Google Scholar only as a supplementary citation-chasing tool, not as the
  primary evidence source.

Search boundaries:

- Main date range: 1995 through May 2026, because the human intake identifies
  the foundational Polyvagal Theory paper as published in 1995.
- Include foundational Porges papers and books even if older than the main date
  range.
- Prioritize 2010-2026 for current clinical, neuroscience, trauma, and critique
  literature.
- Prioritize 2020-2026 for the most recent state of debate, especially
  critiques, responses, reviews, and empirical tests.
- Do not exclude older physiology or anatomy papers when directly relevant to
  evaluating the theory's mechanisms.
- Language scope: primary inclusion language is English. Include non-English
  sources only when directly relevant, metadata is recoverable, and
  classification does not depend on unsupported machine translation. German
  critique sources may be included. Japanese overview sources may be included
  only as clinical or background context if reliable metadata or an English
  abstract is available.
- Discipline or venue scope: clinical psychology, trauma therapy, affective
  neuroscience, autonomic physiology, psychophysiology, attachment, and
  behavioral science.
- Access limits: paywalled scholarly sources may be included if title,
  authorship, journal, year, DOI, and abstract or record metadata are
  recoverable from reliable scholarly records. Use full-text claims only when
  full text is accessible. If only metadata or abstract is available, classify
  conservatively and do not extract fine-grained claims from unavailable full
  text. Exclude or quarantine sources whose DOI, authorship, title, year, or
  claim summary cannot be reconciled.

First-pass discovery queries:

PubMed / MEDLINE query 1:

```text
("polyvagal theory"[Title/Abstract] OR polyvagal[Title/Abstract] OR "social engagement system"[Title/Abstract] OR "ventral vagal"[Title/Abstract] OR "dorsal vagal"[Title/Abstract] OR "Porges SW"[Author])
AND
(critique*[Title/Abstract] OR critic*[Title/Abstract] OR evidence[Title/Abstract] OR empirical[Title/Abstract] OR validation[Title/Abstract] OR mechanism*[Title/Abstract] OR neuroanatom*[Title/Abstract] OR evolution*[Title/Abstract] OR "respiratory sinus arrhythmia"[Title/Abstract] OR "vagal tone"[Title/Abstract] OR trauma[Title/Abstract] OR therapy[Title/Abstract])
```

PubMed / MEDLINE query 2:

```text
("polyvagal theory"[Title/Abstract] OR polyvagal[Title/Abstract])
AND
("Autonomic Nervous System"[MeSH Terms] OR "Vagus Nerve"[MeSH Terms] OR "Heart Rate"[MeSH Terms] OR "Stress Disorders, Post-Traumatic"[MeSH Terms] OR "Psychophysiology"[Title/Abstract] OR "respiratory sinus arrhythmia"[Title/Abstract] OR "heart rate variability"[Title/Abstract])
```

PubMed / MEDLINE query 3:

```text
("polyvagal theory"[Title/Abstract] OR polyvagal[Title/Abstract])
AND
(review[Publication Type] OR systematic review[Title/Abstract] OR meta-analysis[Publication Type] OR critique[Title/Abstract] OR commentary[Title/Abstract])
```

APA PsycInfo portable logic:

```text
("polyvagal theory" OR polyvagal OR "social engagement system" OR "ventral vagal" OR "dorsal vagal" OR "Stephen Porges")
AND
(critique OR criticism OR evidence OR empirical OR validation OR mechanism OR neuroanatomy OR evolution OR "respiratory sinus arrhythmia" OR "vagal tone" OR "heart rate variability" OR trauma OR therapy OR psychotherapy)
```

APA PsycInfo Ovid-style query:

```text
("polyvagal theory" OR polyvagal OR "social engagement system" OR "ventral vagal" OR "dorsal vagal" OR "Stephen Porges").ti,ab,id.
AND
(critique* OR critic* OR evidence OR empirical OR validat* OR mechanism* OR neuroanatom* OR evolution* OR "respiratory sinus arrhythmia" OR "vagal tone" OR "heart rate variability" OR trauma OR therap* OR psychotherapy).ti,ab,id.
```

APA PsycInfo clinical query:

```text
("polyvagal theory" OR polyvagal).ti,ab,id.
AND
(trauma OR "posttraumatic stress" OR PTSD OR attachment OR emotion regulation OR psychotherapy OR "somatic therapy" OR "body-oriented therapy" OR "trauma-informed").ti,ab,id.
```

Scopus broad query:

```text
TITLE-ABS-KEY(
  "polyvagal theory" OR polyvagal OR "social engagement system" OR "ventral vagal" OR "dorsal vagal" OR "Stephen Porges"
)
AND
TITLE-ABS-KEY(
  critique* OR critic* OR evidence OR empirical OR validat* OR mechanism* OR neuroanatom* OR evolution* OR "respiratory sinus arrhythmia" OR "vagal tone" OR "heart rate variability" OR trauma OR therap*
)
AND PUBYEAR > 1994 AND PUBYEAR < 2027
```

Scopus targeted proximity query:

```text
TITLE-ABS-KEY(
  polyvagal W/5 (theory OR evidence OR critique OR criticism OR empirical OR validation OR neuroanatomy OR evolution OR trauma OR therapy)
)
AND PUBYEAR > 1994 AND PUBYEAR < 2027
```

Scopus clinical-overstatement query:

```text
TITLE-ABS-KEY(
  ("polyvagal theory" OR polyvagal)
  AND
  (trauma OR PTSD OR psychotherapy OR "emotion regulation" OR "somatic therapy" OR "trauma-informed care")
)
AND PUBYEAR > 1994 AND PUBYEAR < 2027
```

Web of Science broad query:

```text
TS=(
  "polyvagal theory" OR polyvagal OR "social engagement system" OR "ventral vagal" OR "dorsal vagal" OR "Stephen Porges"
)
AND
TS=(
  critique* OR critic* OR evidence OR empirical OR validat* OR mechanism* OR neuroanatom* OR evolution* OR "respiratory sinus arrhythmia" OR "vagal tone" OR "heart rate variability" OR trauma OR therap*
)
Timespan: 1995-2026
```

Web of Science targeted proximity query:

```text
TS=(
  polyvagal NEAR/5 (theory OR evidence OR critique OR criticism OR empirical OR validation OR neuroanatomy OR evolution OR trauma OR therapy)
)
Timespan: 1995-2026
```

Web of Science adjacent-evidence distinction query:

```text
TS=(
  ("respiratory sinus arrhythmia" OR "heart rate variability" OR "vagal tone" OR "autonomic regulation")
  AND
  (polyvagal OR "polyvagal theory" OR Porges)
)
Timespan: 1995-2026
```

Semantic Scholar natural-language searches:

```text
Polyvagal Theory evidence critique
Polyvagal Theory empirical validation respiratory sinus arrhythmia vagal tone
Polyvagal Theory neuroanatomy evolutionary critique
Polyvagal Theory trauma therapy clinical applications evidence
Stephen Porges Polyvagal Theory Grossman critique
Polyvagal Theory social engagement system evidence
```

Citation-chasing targets:

- Start from foundational Porges Polyvagal Theory papers, especially the
  human-identified 1995 foundational paper.
- Citation-chain forward to empirical tests, reviews, clinical applications,
  major critiques, author responses, and papers distinguishing RSA/vagal tone
  findings from Polyvagal Theory's stronger claims.
- Platform syntax note supplied by human intake: PubMed supports field tags such
  as `[Title/Abstract]` and MeSH searching; Scopus commonly uses
  `TITLE-ABS-KEY` and proximity operators such as `W/n`; Web of Science uses
  field tags such as `TS=` and proximity operators like `NEAR`; PsycInfo syntax
  depends on the platform, with Ovid PsycInfo supporting fielded title,
  abstract, and key-concept searches.

Preferred source domains:

- `ncbi.nlm.nih.gov`, `pubmed.ncbi.nlm.nih.gov`, and `pmc.ncbi.nlm.nih.gov`.
- `apa.org` and `psycnet.apa.org`.
- Publisher platforms for peer-reviewed journals, including Wiley,
  Elsevier/ScienceDirect, Springer, Taylor & Francis, Sage, Oxford Academic,
  Cambridge, Frontiers, and MDPI, while still evaluating article quality
  individually.
- University-hosted pages only when they point to primary publications or author
  bibliographies.

Do not use as evidence:

- Therapy training pages.
- Institute marketing pages.
- Coaching blogs.
- Popular trauma or self-help articles.
- Podcasts.
- YouTube.
- Social media.
- Unsourced summaries.
- Exception: these may be used only to identify popularized claims that may
  overstate the theory, not as evidence for the theory.

Inclusion criteria:

- Sources directly addressing Polyvagal theory or its specific physiological,
  evolutionary, clinical, or therapeutic claims.
- Sources addressing adjacent autonomic nervous system regulation, vagal tone,
  social engagement, trauma response, or social-safety claims, with source role
  clearly distinguished from support for the full theory.
- Sources useful for identifying whether consensus, disagreement, uncertainty,
  or weak support exists around the specific claim being evaluated.
- Foundational or supportive sources.
- Empirical tests of specific claims.
- Systematic or narrative reviews.
- Conceptual and methodological critiques.
- Author responses to critiques.
- Adjacent autonomic nervous system research that is often confused with support
  for the full theory.

Exclusion criteria:

- Sources that only popularize trauma-regulation language without reviewable
  support for the claim being tested, unless used as decoys.
- Sources that support general autonomic regulation but are being used as proof
  of the full Polyvagal theory without a reviewed bridge.
- Sources outside clinical psychology, trauma therapy, affective neuroscience,
  autonomic physiology, or another human-approved adjacent domain.
- Source count or citation count used as a substitute for consensus appraisal.
- General web results used as primary evidence.

Discovery notes:

- Search plan and first-pass exact queries supplied by human intake. Actual
  executed search logs, reviewer identity, final source-selection rationale, and
  unresolved access gaps still need to be recorded. Selected MVP source-access
  state is summarized in `mvp_source_access_record.md`.
- Discovery material supplied so far:
  - ChatGPT Deep Research synthesis pasted by human reviewer. Treat as an
    unverified synthesis aid only; temporary citation handles in that output are
    not recoverable source metadata.
  - Elicit CSV at
    `/Users/CoveMB/Downloads/Elicit - Polyvagal Theory evidence and critiques.csv`,
    inspected as a 13-row contaminated discovery export. It must never be
    treated as source truth. Treat raw Elicit titles, authors, years, DOIs,
    classifications, and claim summaries as untrusted discovery hints until a
    human reviewer verifies the source record and source content.
- The search goal is not to collect only supportive or only critical papers. The
  gold set must include foundational/supportive sources, serious critiques,
  empirical tests, reviews, clinical-application papers, and adjacent autonomic
  nervous system literature that is often confused with proof of the full
  theory.
- Do not treat broad evidence for autonomic regulation, HRV, vagal tone, stress
  physiology, or social safety as direct confirmation of Polyvagal Theory unless
  the paper directly supports the specific claim being evaluated.
- Metadata corrections supplied by human intake before appraisal:
  - Replace the contaminated Grossman/Taylor row carrying DOI
    `10.36131/cnfioritieditore20250301` with the 2007 Biological Psychology
    RSA-methodology review, DOI `10.1016/j.biopsycho.2005.11.014`.
  - Keep Porges 2025 Clinical Neuropsychiatry with DOI
    `10.36131/cnfioritieditore20250301` as author-side review/defense, not
    independent validation. Cite by DOI. Do not rely on page range until
    reconciled, because public/publisher metadata appears inconsistent.
  - Split the contaminated Hanazawa/Grossman row into Grossman 2023 Biological
    Psychology critique, DOI `10.1016/j.biopsycho.2023.108589`, and Hanazawa
    2022 Brain and Nerve clinical overview, DOI `10.11477/mf.1416202169`.
  - Deduplicate the 2026 Grossman critique rows into one multi-author expert
    critique/commentary record, DOI `10.36131/cnfioritieditore20260110`. Use
    pages 100-112 for the Grossman et al. 2026 article. The 169-184 page range
    refers to the Porges 2025 article named inside the critique title.
  - Add the Porges 2026 response/rebuttal, DOI
    `10.36131/cnfioritieditore20260111`.
  - Correct the Porges 2025 Frontiers row to Stephen W. Porges as sole listed
    author unless a separate source record supports J. Kolacz as coauthor.
  - Add Grossman 2024 Biological Psychology as a separate RSA-methodology source,
    DOI `10.1016/j.biopsycho.2023.108739`.
- Quarantine rule before appraisal: any Elicit row whose title, DOI, authors,
  year, and claim summary do not all refer to the same source must be kept out
  of the candidate role pool until the source record is corrected or discarded.

## 3. Candidate Sources

Candidate author-side theory-position sources:

These are candidates for source appraisal, not gold-set truth. Do not treat
author-side defenses, supportive empirical papers, or theory-position papers as
`gold_sources` until a human reviewer verifies what each source supports and
does not support.

- Source ID: `candidate-porges-2025-current-status`
  - Title: `Polyvagal Theory: Current Status, Clinical Applications, and Future Directions`
  - Authors or authoring body: Stephen W. Porges
  - Year if known: 2025
  - Locator or access note: DOI `10.36131/cnfioritieditore20250301`. Cite by
    DOI. Do not rely on page range until reconciled, because public/publisher
    metadata appears inconsistent.
  - Provisional role: author-side review/defense candidate, not independent
    validation
  - Use as: author-side statement of current theory and clinical framing.
  - Do not use as: independent validation or field consensus.
  - Why it may be central: candidate statement of current theory, clinical
    applications, RSA, social engagement, and responses to critiques.
  - Appraisal status: not appraised
- Source ID: `candidate-porges-2025-journey`
  - Title: `Polyvagal theory: a journey from physiological observation to neural innervation and clinical insight`
  - Authors or authoring body: Stephen W. Porges
  - Year if known: 2025
  - Locator or access note: Frontiers in Behavioral Neuroscience, 19, Article
    1659083. DOI `10.3389/fnbeh.2025.1659083`.
  - Provisional role: author-side theory-articulation or clinical-insight
    candidate
  - Use as: author-side theory articulation and clinical-insight framing.
  - Do not use as: independent adjudication of contested claims.
  - Why it may be central: candidate source for the theory's internal logic
    around vagus-heart-face linkage, social engagement, and clinical insight.
  - Appraisal status: not appraised
- Source ID: `candidate-porges-2026-response`
  - Title: `When a Critique Becomes Untenable: A Scholarly Response to Grossman et al.'s Evaluation of Polyvagal Theory`
  - Authors or authoring body: S. W. Porges
  - Year if known: 2026
  - Locator or access note: Clinical Neuropsychiatry, 23(1), 113-128. DOI
    `10.36131/cnfioritieditore20260111`.
  - Provisional role: author response/rebuttal candidate
  - Use as: author response/rebuttal and clarification of PVT scope.
  - Do not use as: independent validation of the theory.
  - Why it may be central: candidate source for Porges's rebuttal and
    clarifications in response to the multi-author critique.
  - Appraisal status: not appraised

Candidate supportive/theory-adjacent empirical sources:

These are candidates for source appraisal, not gold-set truth. Supportive or
theory-adjacent empirical sources must not be treated as validation of the full
theory unless a human reviewer verifies the specific claim.

- Source ID: `candidate-austin-riniolo-porges-2007-bpd`
  - Title: `Borderline personality disorder and emotion regulation: Insights from the Polyvagal Theory`
  - Authors or authoring body: M. A. Austin; T. C. Riniolo; S. W. Porges
  - Year if known: 2007
  - Locator or access note: Brain and Cognition, 65(1), 69-76. DOI
    `10.1016/j.bandc.2006.05.007`.
  - Provisional role: empirical supportive/suggestive candidate, not
    whole-theory validation
  - Use as: suggestive empirical evidence compatible with PVT.
  - Do not use as: validation of Polyvagal Theory as a whole.
  - Why it may be central: candidate source for PVT-compatible emotion
    regulation and autonomic-state interpretation.
  - Appraisal status: not appraised
- Source ID: `candidate-porges-riniolo-mcbride-campbell-2003-reptiles`
  - Title: `Heart rate and respiration in reptiles: Contrasts between a sit-and-wait predator and an intensive forager`
  - Authors or authoring body: S. W. Porges; T. C. Riniolo; T. McBride; B.
    Campbell
  - Year if known: 2003
  - Locator or access note: Brain and Cognition, 52(1), 88-96. DOI
    `10.1016/S0278-2626(03)00012-5`.
  - Provisional role: author-side comparative empirical support candidate, not
    independent adjudication
  - Use as: author-side comparative/autonomic evidence.
  - Do not use as: independent adjudication of PVT.
  - Why it may be central: candidate source for narrow observations used in
    evolutionary framing; not proof of the full theory without appraisal.
  - Appraisal status: not appraised

Candidate adjacent/supportive sources pending appraisal:

- Source ID: `candidate-obrien-2021-act-rsa`
  - Title: `Respiratory sinus arrhythmia predicts perceived therapy process of a group-based acceptance and commitment therapy intervention`
  - Authors or authoring body: W. H. O'Brien; P. Goetz; A. T. O'Brien; H.
    McCarren; E. Delaney
  - Year if known: 2021
  - Locator or access note: Bulletin of the Menninger Clinic, 85(1), 9-22. DOI
    `10.1521/BUMC.2021.85.1.9`.
  - Provisional role: empirical clinical association / adjacent autonomic
    evidence candidate
  - Use as: clinical-adjacent RSA/autonomic association.
  - Do not use as: Polyvagal-specific mechanistic validation.
  - Why it may be acceptable: candidate source for therapy-process association;
    not a direct validation of PVT mechanisms without appraisal.
  - Appraisal status: not appraised
- Source ID: `candidate-poli-2021-contemplative-review`
  - Title: `A Systematic Review of a Polyvagal Perspective on Embodied Contemplative Practices as Promoters of Cardiorespiratory Coupling and Traumatic Stress Recovery for PTSD and OCD: Research Methodologies and State of the Art`
  - Authors or authoring body: A. Poli; A. Gemignani; F. Soldani; M. Miccoli
  - Year if known: 2021
  - Locator or access note: International Journal of Environmental Research and
    Public Health, 18(22), 11778. DOI `10.3390/ijerph182211778`.
  - Provisional role: systematic review / preliminary clinical-adjacent
    evidence candidate
  - Use as: evidence that clinical-adjacent PVT-framed intervention literature
    is limited or preliminary.
  - Do not use as: strong validation of PVT.
  - Why it may be acceptable: candidate source for preliminary intervention
    literature and methodology limits.
  - Appraisal status: not appraised
- Source ID: `candidate-tonhajzerova-2011-cardiac-vagal-control`
  - Title: `Cardiac Vagal Control in Depression and Attention Deficit/Hyperactivity Disorder`
  - Authors or authoring body: I. Tonhajzerova; I. Ondrejka; K. Javorka; A.
    Calkovska; M. Javorka
  - Year if known: 2011
  - Locator or access note: Acta Medica Martiniana, 11(Suppl. 1). DOI
    `10.2478/v10201-011-0011-y`. Page range unresolved; cite by DOI.
  - Provisional role: background autonomic/clinical review candidate
  - Use as: background autonomic/clinical context.
  - Do not use as: central PVT evidence.
  - Why it may be acceptable: candidate source for broad cardiac vagal control
    relevance; should not be used as proof of the full theory.
  - Appraisal status: not appraised
- Source ID: `candidate-hanazawa-2022-clinical-overview`
  - Title: `[Polyvagal Theory and Its Clinical Potential: An Overview]`
  - Authors or authoring body: H. Hanazawa
  - Year if known: 2022
  - Locator or access note: Brain and Nerve, 74(8), 1011-1016. DOI
    `10.11477/mf.1416202169`.
  - Provisional role: clinical overview / supportive-conceptual candidate
  - Use as: clinical/background overview where metadata or English abstract
    supports classification.
  - Do not use as: central mechanistic evidence or independent validation.
  - Why it may be acceptable: candidate source for clinical framing and
    therapeutic potential, not independent mechanistic validation without
    appraisal.
  - Appraisal status: not appraised

Decoy sources:

Decoy policy:

- Include a small set of popularized trauma-regulation pages as decoy sources
  only. The candidate pool below contains five public-facing decoys plus one
  optional product/intervention-marketing decoy; fixture authoring may select
  the most useful 3-5.
- These are not evidence sources. They test whether the skill can recognize
  popularized, clinical-marketing, institute, training, or self-help language
  and avoid treating it as scholarly support.
- Do not count decoys toward evidence strength.
- Do not use decoys to establish scientific consensus.
- Use decoys only to identify overstatement risks and popularized claims.
- Keep decoys separate from scholarly evidence in appraisal tables.
- Exact URLs and access dates are recorded below from human intake; verify page
  accessibility before fixture authoring.
- Clearly label decoys as popularized, clinical-marketing, training, or
  public-facing sources.

- Source ID: `candidate-decoy-polyvagal-institute-what-is`
  - Title: `What is Polyvagal Theory?`
  - Authors or authoring body: Polyvagal Institute
  - Year if known: not recorded
  - Locator or access note:
    `https://www.polyvagalinstitute.org/whatispolyvagaltheory`; accessed
    2026-05-18.
  - Provisional role: popularized/public-facing decoy candidate
  - Suspected decoy reason: may identify popularized claims, but must not be
    used as evidence for the theory.
  - Appraisal status: not appraised
- Source ID: `candidate-decoy-ifm-ptsd-polyvagal`
  - Title: `Understanding PTSD From a Polyvagal Perspective`
  - Authors or authoring body: The Institute for Functional Medicine; page by
    C. Cart according to human-supplied search result
  - Year if known: updated 2024
  - Locator or access note:
    `https://www.ifm.org/articles/understanding-ptsd-from-a-polyvagal-perspective`;
    accessed 2026-05-18.
  - Provisional role: popularized/clinical-marketing decoy candidate
  - Suspected decoy reason: may identify trauma-regulation overstatement risks,
    but must not be used as evidence for the theory.
  - Appraisal status: not appraised
- Source ID: `candidate-decoy-khiron-ladder`
  - Title: `Polyvagal Theory: A Ladder of Nervous States`
  - Authors or authoring body: Khiron Clinics
  - Year if known: not recorded
  - Locator or access note:
    `https://khironclinics.com/blog/polyvagal-theory-a-ladder-of-nervous-states/`;
    accessed 2026-05-18.
  - Provisional role: popularized/clinical-marketing decoy candidate
  - Suspected decoy reason: may identify simplified ladder framing, but must not
    be used as evidence for the theory.
  - Appraisal status: not appraised
- Source ID: `candidate-decoy-positivepsychology-exercises`
  - Title: `18 Polyvagal Theory & How to Use the Exercises in Therapy`
  - Authors or authoring body: PositivePsychology.com
  - Year if known: 2023; page updated status not fully verified
  - Locator or access note: `https://positivepsychology.com/polyvagal-theory/`;
    accessed 2026-05-18.
  - Provisional role: popularized/public-facing decoy candidate
  - Suspected decoy reason: may identify therapy-exercise overstatement risks,
    but must not be used as evidence for the theory.
  - Appraisal status: not appraised
- Source ID: `candidate-decoy-rhythm-of-regulation-deb-dana`
  - Title: `Rhythm of Regulation`
  - Authors or authoring body: Deb Dana / Rhythm of Regulation
  - Year if known: copyright 2024 on page
  - Locator or access note: `https://www.rhythmofregulation.com/`; accessed
    2026-05-18.
  - Provisional role: popularized/clinical-training decoy candidate
  - Suspected decoy reason: may identify popular clinical framing, but must not
    be used as evidence for the theory.
  - Appraisal status: not appraised
- Source ID: `candidate-decoy-unyte-ssp-product`
  - Title: `Safe and Sound Protocol (SSP): Attune. Re-tune. Connect`
  - Authors or authoring body: Unyte / Integrated Listening
  - Year if known: not recorded
  - Locator or access note:
    `https://integratedlistening.com/products/ssp-safe-sound-protocol/`;
    accessed 2026-05-18.
  - Provisional role: product/intervention-marketing decoy candidate
  - Suspected decoy reason: may identify SSP evidence, product-marketing, and
    mechanism-overstatement risks, but must not be used as evidence for SSP or
    PVT.
  - Appraisal status: not appraised

Disallowed sources:

- True disallowed sources: none identified yet. Policy: add a source here only
  if it is fabricated, retracted, unrecoverable, inaccessible in a way that
  prevents use, or otherwise unusable. Use the quarantine list for corrupted
  Elicit rows whose title, authors, DOI, year, or claim summary conflict.

Candidate critique and contestation sources:

- Source ID: `candidate-grossman-taylor-2007-rsa`
  - Title: `Toward understanding respiratory sinus arrhythmia: Relations to cardiac vagal tone, evolution and biobehavioral functions`
  - Authors or authoring body: P. Grossman; E. W. Taylor
  - Year if known: 2007
  - Locator or access note: Biological Psychology, 74(2), 263-285. DOI
    `10.1016/j.biopsycho.2005.11.014`.
  - Provisional role: methodological critique / RSA measurement caveats
    candidate
  - Use as: RSA measurement caveats and methodological critique.
  - Do not use as: blanket refutation of all autonomic-regulation findings.
  - Why it may be central: candidate source for RSA interpretation limits,
    cardiac vagal tone caveats, evolutionary framing, and overstatement risks.
  - Appraisal status: not appraised
- Source ID: `candidate-grossman-2023-five-premises`
  - Title: `Fundamental challenges and likely refutations of the five basic premises of the polyvagal theory`
  - Authors or authoring body: P. Grossman
  - Year if known: 2023
  - Locator or access note: Biological Psychology, 180, 108589. DOI
    `10.1016/j.biopsycho.2023.108589`.
  - Provisional role: major critique / actively contested candidate
  - Use as: major critique of PVT premises.
  - Do not use as: formal field-wide consensus or dismissal of all clinical
    metaphors.
  - Why it may be central: candidate source for critique of core PVT premises.
  - Appraisal status: not appraised
- Source ID: `candidate-grossman-2024-rsa`
  - Title: `Respiratory sinus arrhythmia (RSA), vagal tone and biobehavioral integration: Beyond parasympathetic function`
  - Authors or authoring body: P. Grossman
  - Year if known: 2024
  - Locator or access note: Biological Psychology, 186, 108739. DOI
    `10.1016/j.biopsycho.2023.108739`.
  - Provisional role: RSA methodology / measurement caveats candidate
  - Use as: RSA/vagal-tone methodology and measurement-caveat source.
  - Do not use as: direct adjudication of all PVT clinical claims.
  - Why it may be central: candidate source for evaluating whether RSA can be
    treated as vagal tone, safety, or a Polyvagal-specific biomarker.
  - Appraisal status: not appraised
- Source ID: `candidate-grossman-2026-untenable`
  - Title: `Why the Polyvagal Theory Is Untenable: An international expert evaluation of the polyvagal theory and commentary upon Porges, S.W. (2025). Polyvagal theory: current status, clinical applications, and future directions. Clin. Neuropsychiatry, 22(3), 169-184.`
  - Authors or authoring body: P. Grossman; G. L. Ackland; A. M. Allen; G. G.
    Berntson; L. C. Booth; G. M. Burghardt; J. Buron; V. Dinets; J. S. Doody;
    M. Dutschmann; D. G. S. Farmer; J. P. Fisher; A. V. Gourine; M. J. Joyner;
    J. M. Karemaker; S. S. Khalsa; E. G. Lakatta; C. A. C. Leite; V. G.
    Macefield; B. H. Machado; R. M. McAllen; C. Menuet; D. Mendelowitz; D. J. A.
    Moraes; W. Neuhuber; M. M. Ottaviani; D. J. Paterson; J. F. Paton; P. R.
    Pellegrino; R. Ramchandra; J. Shanks; J. S. Schwaber; K. Shivkumar; K. M.
    Spyer; E. W. Taylor; J. A. Taylor; T. Wang; S. T. Yao; I. H. Zucker
  - Year if known: 2026
  - Locator or access note: Clinical Neuropsychiatry, 23(1), 100-112. DOI
    `10.36131/cnfioritieditore20260110`.
  - Provisional role: multi-author expert critique/commentary candidate
  - Use as: major critique of core PVT premises by physiology, evolution, and
    autonomic experts.
  - Do not overstate as: formal field-wide consensus process.
  - Why it may be central: candidate source for RSA, vagal tone, neuroanatomy,
    evolution, and vertebrate social behavior critiques.
  - Appraisal status: not appraised
- Source ID: `candidate-doody-burghardt-dinets-2023-sociality`
  - Title: `The Evolution of Sociality and the Polyvagal Theory`
  - Authors or authoring body: J. S. Doody; G. M. Burghardt; V. Dinets
  - Year if known: 2023
  - Locator or access note: Biological Psychology, 180, 108569. DOI
    `10.1016/j.biopsycho.2023.108569`.
  - Provisional role: evolutionary/sociality critique candidate
  - Use as: critique of sociality/evolutionary assumptions.
  - Do not use as: sole refutation of all PVT claims.
  - Why it may be central: candidate source for social-asocial dichotomy and
    evolutionary-claim appraisal.
  - Appraisal status: not appraised
- Source ID: `candidate-walz-grossman-2024-facts`
  - Title: `»Polyvagal«: Die schöne Theorie und die hässlichen Fakten`
  - Authors or authoring body: D. Walz; P. Grossman
  - Year if known: 2024
  - Locator or access note: Psychotherapie. DOI
    `10.30820/2364-1517-2024-2-163`. Language: German.
  - Provisional role: critique / clinical-facing commentary candidate, not
    primary empirical evidence
  - Use as: clinical-facing critique.
  - Do not use as: primary empirical evidence.
  - Why it may be central: candidate source for physiological-foundation and
    clinical-overreach critiques.
  - Appraisal status: not appraised

Candidate sources promoted from unresolved metadata recovery:

- Source ID: `candidate-neuhuber-berthoud-2022-vagus-anatomy`
  - Title: `Functional anatomy of the vagus system: How does the polyvagal theory comply?`
  - Authors or authoring body: Winfried L. Neuhuber; Hans-Rudolf Berthoud
  - Year if known: 2022
  - Locator or access note: Biological Psychology, 174, Article 108425. DOI
    `10.1016/j.biopsycho.2022.108425`. Publisher abstract/metadata
    recoverable; full-text access may depend on subscription.
  - Provisional role: neuroanatomical critique candidate
  - Use as: critique of PVT's functional-anatomical and phylogenetic
    assumptions, especially vagal nuclei, dorsal/ventral vagal mapping, and
    anatomical substrate claims.
  - Do not use as: blanket proof that all clinical or metaphorical uses of PVT
    are invalid.
  - Why it may be central: directly appraises whether PVT's neuroanatomical
    assumptions comply with known vagus-system anatomy.
  - Appraisal status: not appraised
- Source ID: `candidate-neuhuber-berthoud-2023-corrigendum`
  - Title: `Corrigendum to "Functional anatomy of the vagus system: How does the polyvagal theory comply?" [Biological Psychology 174 (2022) 108425]`
  - Authors or authoring body: Winfried L. Neuhuber; Hans-Rudolf Berthoud
  - Year if known: 2023
  - Locator or access note: Biological Psychology, 179, Article 108554. DOI
    `10.1016/j.biopsycho.2023.108554`. Published erratum/corrigendum record;
    the corrected article is DOI `10.1016/j.biopsycho.2022.108425`.
  - Provisional role: correction/corrigendum record candidate
  - Use as: metadata/correction companion to the 2022 neuroanatomy critique.
  - Do not use as: independent evidence beyond the corrected details.
  - Why it may be central: prevents reliance on corrected phrasing about DMX
    cardiac neurons/conduction speed.
  - Appraisal status: not appraised
- Source ID: `candidate-taylor-wang-leite-2022-cardiorespiratory-phylogeny`
  - Title: `An overview of the phylogeny of cardiorespiratory control in vertebrates with some reflections on the 'Polyvagal Theory'`
  - Authors or authoring body: Edwin W. Taylor; Tobias Wang; Cleo A. C. Leite
  - Year if known: 2022
  - Locator or access note: Biological Psychology, 172, Article 108382. DOI
    `10.1016/j.biopsycho.2022.108382`. Open-access publisher page available
    according to human intake.
  - Provisional role: comparative physiology / evolutionary-mechanism critique
    candidate
  - Use as: evidence that cardiorespiratory interactions and RSA-like phenomena
    are not uniquely mammalian and that broad vertebrate comparative physiology
    complicates strong PVT evolutionary claims.
  - Do not use as: full refutation of every PVT claim or clinical application.
  - Why it may be central: directly addresses PVT's evolutionary and
    RSA/cardiorespiratory assumptions.
  - Appraisal status: not appraised
- Source ID: `candidate-monteiro-taylor-sartori-cruz-rantin-leite-2018-lungfish`
  - Title: `Cardiorespiratory interactions previously identified as mammalian are present in the primitive lungfish`
  - Authors or authoring body: Diana A. Monteiro; Edwin W. Taylor; Marina R.
    Sartori; Andre L. Cruz; Francisco T. Rantin; Cleo A. C. Leite
  - Year if known: 2018
  - Locator or access note: Science Advances, 4(2), Article eaaq0800. DOI
    `10.1126/sciadv.aaq0800`. Open-access article available through PMC or
    Science Advances according to human intake.
  - Provisional role: comparative physiology / lungfish evidence candidate
  - Use as: evidence that cardiorespiratory interactions previously framed as
    mammalian are present in lungfish, weakening strong mammalian-uniqueness
    interpretations.
  - Do not use as: standalone appraisal of PVT as a whole.
  - Why it may be central: provides direct comparative physiology evidence used
    in the debate over PVT's evolutionary assumptions.
  - Appraisal status: not appraised
- Source ID: `candidate-porges-et-al-2014-listening-project-protocol`
  - Title: `Reducing auditory hypersensitivities in autistic spectrum disorder: Preliminary findings evaluating the listening project protocol`
  - Authors or authoring body: Stephen W. Porges; Olga V. Bazhenova; Elgiz Bal;
    Nancy Carlson; Yevgeniya Sorokin; Keri J. Heilman; Edwin H. Cook; Gregory F.
    Lewis
  - Year if known: 2014
  - Locator or access note: Frontiers in Pediatrics, 2, Article 80. DOI
    `10.3389/fped.2014.00080`. Open access.
  - Provisional role: precursor acoustic/listening intervention study candidate
  - Use as: preliminary intervention evidence for the Listening Project
    Protocol, a precursor to SSP.
  - Do not use as: strong validation of SSP, PVT mechanisms, or broad clinical
    efficacy.
  - Why it may be central: often cited as early evidence for SSP-like acoustic
    intervention claims.
  - Appraisal status: not appraised
- Source ID: `candidate-kawai-et-al-2023-ssp-adult-autism`
  - Title: `Initial Outcomes of the Safe and Sound Protocol on Patients with Adult Autism Spectrum Disorder: Exploratory Pilot Study`
  - Authors or authoring body: Hiroki Kawai; Makiko Kishimoto; Yuko Okahisa;
    Shinji Sakamoto; Seishi Terada; Manabu Takaki
  - Year if known: 2023
  - Locator or access note: International Journal of Environmental Research and
    Public Health, 20(6), Article 4862. DOI `10.3390/ijerph20064862`. Open
    access.
  - Provisional role: SSP exploratory pilot study candidate
  - Use as: preliminary clinical/acoustic intervention evidence in adults with
    ASD.
  - Do not use as: strong efficacy evidence or PVT-specific mechanistic
    validation.
  - Why it may be central: directly studies SSP but has exploratory-pilot
    limitations.
  - Appraisal status: not appraised
- Source ID: `candidate-heilman-et-al-2023-ssp-autism-single-arm`
  - Title: `Effects of the Safe and Sound Protocol (SSP) on Sensory Processing, Digestive Function and Selective Eating in Children and Adults with Autism: A Prospective Single-Arm Study`
  - Authors or authoring body: Keri J. Heilman; S. Heinrich; M. Achermann; E.
    Nix; H. Kyuchukov
  - Year if known: 2023
  - Locator or access note: Journal on Developmental Disabilities, 28(1), 1-26.
    Zenodo record DOI `10.5281/zenodo.8018744`; parent/concept DOI
    `10.5281/zenodo.8018743`; public OADD PDF is linked from the Zenodo record.
    No separate journal-assigned DOI has been recovered.
  - Provisional role: SSP prospective single-arm study candidate
  - Use as: preliminary clinical/acoustic intervention evidence.
  - Do not use as: randomized evidence, strong causal evidence, or PVT-specific
    mechanistic validation.
  - Why it may be central: directly studies SSP in children/adults with autism
    but is single-arm and requires caution.
  - Appraisal status: not appraised
- Source ID: `candidate-porges-et-al-2019-fni-autonomic-regulation`
  - Title: `Autonomic regulation of preterm infants is enhanced by Family Nurture Intervention`
  - Authors or authoring body: Stephen W. Porges; Maria I. Davila; Gregory F.
    Lewis; Jacek Kolacz; Stephanie Okonmah-Obazee; Amie A. Hane; Katie Y. Kwon;
    Robert J. Ludwig; Michael M. Myers; Martha G. Welch
  - Year if known: 2019
  - Locator or access note: Developmental Psychobiology, 61(6), 942-952. DOI
    `10.1002/dev.21841`. Publisher/metadata recoverable; full text may depend
    on access.
  - Provisional role: FNI autonomic-regulation RCT evidence candidate
  - Use as: evidence that FNI was associated with enhanced autonomic
    regulation/RSA-related outcomes in preterm infants.
  - Do not use as: direct validation of the full Polyvagal Theory or of
    PVT-specific mechanisms.
  - Why it may be central: directly links FNI to autonomic regulation and
    interprets findings partly through PVT.
  - Appraisal status: not appraised
- Source ID: `candidate-welch-et-al-2020-fni-follow-up`
  - Title: `Family nurture intervention in the NICU increases autonomic regulation in mothers and children at 4-5 years of age: Follow-up results from a randomized controlled trial`
  - Authors or authoring body: Martha G. Welch; Joseph L. Barone; Stephen W.
    Porges; Amie A. Hane; Katie Y. Kwon; Robert J. Ludwig; Raymond I. Stark;
    Amanda L. Surman; Jacek Kolacz; Michael M. Myers
  - Year if known: 2020
  - Locator or access note: PLOS ONE, 15(8), Article e0236930. DOI
    `10.1371/journal.pone.0236930`. Open access.
  - Provisional role: FNI follow-up autonomic-regulation evidence candidate
  - Use as: follow-up clinical/autonomic evidence that FNI-NICU was associated
    with higher RSA/autonomic regulation at 4-5 years in a returning subset.
  - Do not use as: direct proof of PVT-specific mechanisms or broad
    trauma-therapy validation.
  - Why it may be central: relevant to co-regulation/autonomic regulation
    claims, while requiring caution because follow-up included only about half
    of the original participants.
  - Appraisal status: not appraised
- Source ID: `candidate-rajabalee-et-al-2022-computer-altered-music-fnd`
  - Title: `Neuromodulation Using Computer-Altered Music to Treat a Ten-Year-Old Child Unresponsive to Standard Interventions for Functional Neurological Disorder`
  - Authors or authoring body: Nadia Rajabalee; Kasia Kozlowska; Seung Yeon
    Lee; Blanche Savage; Clare Hawkes; Daniella Siciliano; Stephen W. Porges;
    Susannah Pick; Souraya Torbey
  - Year if known: 2022
  - Locator or access note: Harvard Review of Psychiatry, 30(5), 303-316. DOI
    `10.1097/HRP.0000000000000341`.
  - Provisional role: case report / acoustic neuromodulation candidate
  - Use as: low-level clinical case evidence involving computer-altered
    music/SSP-like intervention.
  - Do not use as: generalizable evidence of SSP efficacy or PVT-specific
    mechanism.
  - Why it may be central: often cited in SSP evidence summaries, but
    methodologically weak for causal/general claims.
  - Appraisal status: not appraised
- Source ID: `candidate-rogowski-et-al-2024-ajot-ssp-young-children`
  - Title: `An Exploratory Study of the Safe & Sound Protocol in Young Children With Autism`
  - Authors or authoring body: Michelle Rogowski; John A. Damiao; Catherine
    Cavaliere; Nadia Rust; Alyssa Lopez; Rebecca Marash; Amy Zdrodowski
  - Year if known: 2024
  - Locator or access note: American Journal of Occupational Therapy, 78(Suppl.
    2), abstract/poster record PO332. DOI `10.5014/ajot.2024.78S2-PO332`. Do
    not rely on page range without publisher reconciliation.
  - Provisional role: SSP young-children occupational-therapy abstract candidate
  - Use as: possible low-weight conference/poster abstract evidence for SSP used
    with occupational therapy in young children with autism, only after
    appraisal.
  - Do not use as: full peer-reviewed trial evidence, strong efficacy evidence,
    or PVT-specific mechanistic validation.
  - Why it may be central: directly mentions SSP in young children with autism,
    but appears to be an abstract/poster record rather than a full article.
  - Appraisal status: not appraised

Remaining unresolved metadata or blocked-source TODOs:

- Confirm whether `candidate-heilman-et-al-2023-ssp-autism-single-arm` has any
  journal-assigned DOI beyond Zenodo record DOI `10.5281/zenodo.8018744` and
  parent/concept DOI `10.5281/zenodo.8018743`.
- `retired-kishimoto-et-al-2023-ssp-children-autism` is no longer a candidate
  source. Do not use it unless a stable non-Longdom scholarly record is
  recovered and the venue/source-quality concern is resolved.
- Do not add SSP, Rest & Restore, VoicePro, or similar studies mentioned only in
  marketing summaries until stable scholarly metadata is recovered.
- Full content appraisal remains required for every candidate source listed
  above before any source can become appraised evidence.

Quarantined or retired contaminated discovery rows:

- Any raw Elicit row where title, authors, DOI, year, and claim summary do not
  refer to the same source: do not use until corrected against reliable source
  records.
- Original Elicit Grossman/Taylor 2025 row carrying DOI
  `10.36131/cnfioritieditore20250301`: retired as contaminated and replaced by
  `candidate-grossman-taylor-2007-rsa`.
- Original Elicit Hanazawa/Grossman 2023 row: retired as contaminated and split
  into `candidate-grossman-2023-five-premises` and
  `candidate-hanazawa-2022-clinical-overview`.
- Any Grossman 2026 row with the wrong year, truncated author list, or
  unsupported page range: retired until reconciled and represented by
  `candidate-grossman-2026-untenable`.
- Any Porges Frontiers row listing J. Kolacz as coauthor: retired unless a
  reliable publisher record supports that authorship.
- `retired-kishimoto-et-al-2023-ssp-children-autism`: retired from the candidate
  source list because the only recovered record is Longdom-hosted, the
  publisher/PDF-stated DOI `10.35248/2161-0487.23.13.455` did not resolve via
  `doi.org` in this review pass, and the venue/source quality remains
  unresolved. Do not use as evidence. Do not assign DOI
  `10.3390/ijerph20064862`; that DOI belongs to
  `candidate-kawai-et-al-2023-ssp-adult-autism`.

## 4. Expected Gold-Set Behavior

Provisional claims the output is expected to support if confirmed by appraisal:

- Claim: Polyvagal theory is influential and clinically popular.
  - Evidence basis to be supplied by human reviewer:
- Claim: Some adjacent ideas about autonomic regulation and social safety may
  have broader support than the full theory.
  - Evidence basis to be supplied by human reviewer:

Provisional claims the output is expected to reject if confirmed by appraisal:

- Claim: Polyvagal theory is settled neuroscience.
  - Evidence basis to be supplied by human reviewer:
- Claim: General autonomic regulation evidence proves the full Polyvagal theory.
  - Evidence basis to be supplied by human reviewer:
- Claim: Polyvagal theory is entirely useless, disproven, or irrelevant.
  - Evidence basis to be supplied by human reviewer:

Provisional uncertainties the output should preserve if confirmed by appraisal:

- Uncertainty: Which specific mechanistic and evolutionary claims remain
  contested, weakly supported, or outside the reviewed source basis.
  - Evidence basis to be supplied by human reviewer:
- Uncertainty: Whether clinical usefulness claims are supported by direct
  evidence, indirect plausibility, clinician uptake, or popularized framing.
  - Evidence basis to be supplied by human reviewer:

Required distinctions:

- Distinction: well-supported general autonomic nervous system findings versus
  Porges's specific theoretical claims.
  - Evidence basis to be supplied by human reviewer:
- Distinction: clinical or therapeutic usefulness claims versus physiological
  mechanism claims.
  - Evidence basis to be supplied by human reviewer:
- Distinction: popularized trauma-regulation claims versus source-supported
  research claims.
  - Evidence basis to be supplied by human reviewer:
- Distinction: adjacent support for autonomic regulation or social safety versus
  proof of the full Polyvagal theory.
  - Evidence basis to be supplied by human reviewer:
- Distinction: source count or citation count versus reviewed consensus or
  evidence strength.
  - Evidence basis to be supplied by human reviewer:
- Distinction: broad autonomic-regulation findings versus Porges's specific
  contested physiological, mechanistic, and evolutionary claims.
  - Evidence basis to be supplied by human reviewer:

Citation-audit expectations:

- Expectation: Every claim in the gold-standard answer must trace to one or more
  appraised source records. Popularized decoys may be cited only as examples of
  overstatement risk, never as evidence of scientific support. Author-side
  defenses and critique papers must be labeled by source role. Adjacent
  autonomic evidence must not be cited as proof of the full Polyvagal Theory
  unless the reviewed source directly supports the specific claim. Claims about
  consensus must be based on reviewed source appraisal, not source count,
  citation count, popularity, or clinical uptake.
  - Evidence basis: Pending source appraisal.

## 5. Review State

Reviewer status:

- active MVP source-role and scorecard benchmark with search-log waiver

Reviewer uncertainty:

- The target theory, domain, discovery databases, preferred source domains, date
  range, broad inclusion/exclusion criteria, and first-pass search strings are
  now supplied. A third-party discovery synthesis and contaminated Elicit
  discovery export have also been supplied. Search language and access
  boundaries, selected candidate-source metadata corrections, popularized-decoy
  candidates, and exact decoy URLs/access dates have been supplied by human
  intake. Complete source metadata has been supplied for several candidate
  records, including formerly unresolved Neuhuber/Berthoud, Taylor/lungfish,
  Safe and Sound Protocol, Family Nurture Intervention, and selected
  clinical/acoustic intervention candidates. Remaining unresolved items include
  checking whether Heilman et al. 2023 has any separate journal-assigned DOI
  beyond the Zenodo record and parent/concept DOIs, any SSP/Rest &
  Restore/VoicePro studies currently known only from marketing summaries, and
  any source still represented only through temporary synthesis handles.
  Kishimoto et al. 2023 has been retired from the candidate source list unless a
  stable non-Longdom scholarly record is recovered. Selected MVP source
  appraisals, evidence bases, candidate-output scorecards, user-reported
  scorecard review, and a selected-MVP-source access record have been supplied.
  Exact executed search logs have not been supplied and are waived for this MVP
  activation. Activation-ready reviewer approval was supplied on 2026-06-03.

Activation Decision:

- active MVP with executed-search-log waiver

Activation decision rationale:

- The evaluation question, expected calibration, discovery strategy, and
  first-pass exact search strings are defined from human intake, and candidate
  discovery material has been recorded. Several metadata corrections, candidate
  source records, and decoy candidates with URLs/access dates are now recorded
  from human intake. The active MVP fixture now has selected MVP source appraisals,
  source-role evidence bases, scorecard testing against the eight minimum
  failure checks, user-reported scorecard review, and an MVP source-access
  record. The user explicitly approved activation with a waiver for skipped
  executed search-log reconstruction on 2026-06-03. Residual risk: source
  discovery completeness cannot be independently reproduced from this packet
  alone.
