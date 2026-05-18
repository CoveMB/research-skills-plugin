# Gold-Set Intake

Gold-set ID: polyvagal-theory-consensus-overstatement
Gold-set title: Polyvagal Theory Consensus Overstatement
Status: intake-draft, not active

Do not use this file as source truth by itself. A human reviewer must check what
each source does and does not support before any fixture can become active.

## 1. Evaluation Frame

Narrow research or evaluation question:

- Can the skill avoid overstating consensus around Polyvagal theory in clinical
  psychology, trauma therapy, and affective neuroscience?
- Focus areas: autonomic nervous system regulation, vagal tone, social
  engagement, trauma responses, and therapeutic applications.
- Human narrowing still required: executed search record, actual source corpus,
  source-access boundaries, and reviewer appraisal before fixture authoring.

Scholarly failure mode being tested:

- Field uncertainty collapsed into an overstated consensus claim.
- Related risks: cherry-picking, source-type confusion, decoy source accepted,
  and inaccurate synthesis.
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
- Language scope:
- Discipline or venue scope: clinical psychology, trauma therapy, affective
  neuroscience, autonomic physiology, psychophysiology, attachment, and
  behavioral science.
- Access limits:

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
  searches, search dates, reviewer identity, candidate source list, and
  unresolved access gaps still need to be recorded.
- Discovery material supplied so far:
  - ChatGPT Deep Research synthesis pasted by human reviewer. Treat as an
    unverified synthesis aid only; temporary citation handles in that output are
    not recoverable source metadata.
  - Elicit CSV at
    `/Users/CoveMB/Downloads/Elicit - Polyvagal Theory evidence and critiques.csv`,
    inspected as a 13-row candidate source export. Treat Elicit classifications
    as provisional until a human reviewer verifies metadata and source content.
- The search goal is not to collect only supportive or only critical papers. The
  gold set must include foundational/supportive sources, serious critiques,
  empirical tests, reviews, clinical-application papers, and adjacent autonomic
  nervous system literature that is often confused with proof of the full
  theory.
- Do not treat broad evidence for autonomic regulation, HRV, vagal tone, stress
  physiology, or social safety as direct confirmation of Polyvagal Theory unless
  the paper directly supports the specific claim being evaluated.
- Metadata drift to resolve before appraisal:
  - The Elicit export lists `10.36131/cnfioritieditore20250301` for both a
    Grossman/Taylor row and a Stephen W. Porges row with the same title. Verify
    authorship, title, and DOI from publisher records.
  - The Elicit row titled `FUNDAMENTAL CHALLENGES AND LIKELY REFUTATIONS OF THE
    FIVE BASIC PREMISES OF THE POLYVAGAL THEORY` appears to conflict with its
    exported claim summary. Verify title, authorship, and classification before
    assigning source role.
  - Porges response papers and Grossman critique papers mentioned in the pasted
    synthesis need recoverable metadata before they can be used as source
    evidence.

## 3. Candidate Sources

Candidate gold sources:

- Source ID: `candidate-porges-2025-current-status`
  - Title: `Polyvagal Theory: Current Status, Clinical Applications, and Future Directions`
  - Authors or authoring body: Stephen W. Porges
  - Year if known: 2025
  - Locator or access note: DOI `10.36131/cnfioritieditore20250301` from Elicit
    export; verify because the CSV contains a metadata conflict for this DOI.
  - Provisional role: foundational/supportive or author-side defense candidate
  - Why it may be central: candidate statement of current theory, clinical
    applications, RSA, social engagement, and responses to critiques.
  - Appraisal status: not appraised
- Source ID: `candidate-porges-kolacz-2025-journey`
  - Title: `Polyvagal theory: a journey from physiological observation to neural innervation and clinical insight`
  - Authors or authoring body: S. Porges; J. Kolacz
  - Year if known: 2025
  - Locator or access note: DOI `10.3389/fnbeh.2025.1659083` from Elicit export
  - Provisional role: foundational/supportive or theory-articulation candidate
  - Why it may be central: candidate source for the theory's internal logic
    around vagus-heart-face linkage, social engagement, and clinical insight.
  - Appraisal status: not appraised
- Source ID: `candidate-austin-riniolo-porges-2007-bpd`
  - Title: `Borderline personality disorder and emotion regulation: Insights from the Polyvagal Theory`
  - Authors or authoring body: M. Austin; T. C. Riniolo; S. Porges
  - Year if known: 2007
  - Locator or access note: DOI `10.1016/j.bandc.2006.05.007` from Elicit export
  - Provisional role: supportive empirical candidate
  - Why it may be central: candidate source for PVT-compatible emotion
    regulation and autonomic-state interpretation.
  - Appraisal status: not appraised
- Source ID: `candidate-porges-riniolo-mcbride-campbell-2003-reptiles`
  - Title: `Heart rate and respiration in reptiles: contrasts between a sit-and-wait predator and an intensive forager`
  - Authors or authoring body: S. Porges; T. C. Riniolo; T. McBride; B. Campbell
  - Year if known: 2003
  - Locator or access note: DOI `10.1016/S0278-2626(03)00012-5` from Elicit export
  - Provisional role: foundational/supportive comparative physiology candidate
  - Why it may be central: candidate source for narrow observations used in
    evolutionary framing; not proof of the full theory without appraisal.
  - Appraisal status: not appraised

Acceptable sources:

- Source ID: `candidate-obrien-2021-act-rsa`
  - Title: `Respiratory sinus arrhythmia predicts perceived therapy process of a group-based acceptance and commitment therapy intervention`
  - Authors or authoring body: W. O'Brien; P. W. Goetz; A. T. O'Brien; H.
    McCarren; E. Delaney
  - Year if known: 2021
  - Locator or access note: DOI `10.1521/bumc.2021.85.1.9` from Elicit export
  - Provisional role: clinical-process or adjacent RSA candidate
  - Why it may be acceptable: candidate source for therapy-process association;
    not a direct validation of PVT mechanisms without appraisal.
  - Appraisal status: not appraised
- Source ID: `candidate-poli-2021-contemplative-review`
  - Title: `A Systematic Review of a Polyvagal Perspective on Embodied Contemplative Practices as Promoters of Cardiorespiratory Coupling and Traumatic Stress Recovery for PTSD and OCD: Research Methodologies and State of the Art`
  - Authors or authoring body: A. Poli; A. Gemignani; F. Soldani; M. Miccoli
  - Year if known: 2021
  - Locator or access note: DOI `10.3390/ijerph182211778` from Elicit export
  - Provisional role: clinical-application review candidate
  - Why it may be acceptable: candidate source for preliminary intervention
    literature and methodology limits.
  - Appraisal status: not appraised
- Source ID: `candidate-tonhajzerova-2011-cardiac-vagal-control`
  - Title: `Cardiac Vagal Control in Depression and Attention Deficit/Hyperactivity Disorder`
  - Authors or authoring body: I. Tonhajzerova; I. Ondrejka; Kamil Javorka; A.
    Calkovska; M. Javorka
  - Year if known: 2011
  - Locator or access note: DOI `10.2478/v10201-011-0011-y` from Elicit export
  - Provisional role: adjacent autonomic regulation background candidate
  - Why it may be acceptable: candidate source for broad cardiac vagal control
    relevance; should not be used as proof of the full theory.
  - Appraisal status: not appraised

Decoy sources:

- Source ID: `candidate-grossman-taylor-2025-metadata-conflict`
  - Title: `Polyvagal Theory: Current Status, Clinical Applications, and Future Directions`
  - Authors or authoring body: P. Grossman; E. Taylor
  - Year if known: 2025
  - Locator or access note: DOI `10.36131/cnfioritieditore20250301` from Elicit
    export; verify because this conflicts with another row's authorship.
  - Provisional role: metadata-conflict decoy candidate until verified
  - Suspected decoy reason: likely metadata drift or duplicate/incorrect author
    attribution in export; do not use until publisher metadata is checked.
  - Appraisal status: not appraised
- Source ID: `candidate-hanazawa-2023-fundamental-challenges`
  - Title: `FUNDAMENTAL CHALLENGES AND LIKELY REFUTATIONS OF THE FIVE BASIC PREMISES OF THE POLYVAGAL THEORY`
  - Authors or authoring body: H. Hanazawa
  - Year if known: 2023
  - Locator or access note: DOI `10.1016/j.biopsycho.2023.108589` from Elicit export
  - Provisional role: metadata/classification-conflict candidate
  - Suspected decoy reason: exported title suggests critique, while exported
    claim summary says the theory offers a useful clinical framework; verify
    source metadata and classify after appraisal.
  - Appraisal status: not appraised
- Source ID: `candidate-popular-trauma-regulation-sources`
  - Title: not yet supplied
  - Authors or authoring body: not yet supplied
  - Year if known: not yet supplied
  - Locator or access note: to be collected only if needed to test popularized
    overstatement
  - Provisional role: popularized-claim decoy candidate
  - Suspected decoy reason: therapy training pages, institute marketing,
    coaching blogs, podcasts, YouTube, social media, and unsourced summaries may
    identify overstatement risks but must not be evidence for the theory.
  - Appraisal status: not appraised

Disallowed sources:

- Source ID: none supplied yet
  - Title:
  - Authors or authoring body:
  - Year if known:
  - Locator or access note:
  - Provisional role:
  - Suspected disallow reason:
  - Appraisal status: not appraised

Candidate critique and contestation sources:

- Source ID: `candidate-grossman-2026-untenable`
  - Title: `Why The Polyvagal Theory Is Untenable`
  - Authors or authoring body: P. Grossman; Elicit export also has a `P.
    Grossman et al.` row with the same title and DOI.
  - Year if known: 2026
  - Locator or access note: DOI `10.36131/cnfioritieditore20260110` from Elicit
    export; verify author list and whether duplicate rows should be merged.
  - Provisional role: serious critique candidate
  - Why it may be central: candidate source for RSA, vagal tone, neuroanatomy,
    evolution, and vertebrate social behavior critiques.
  - Appraisal status: not appraised
- Source ID: `candidate-doody-burghardt-dinets-2023-sociality`
  - Title: `The Evolution of Sociality and the Polyvagal Theory`
  - Authors or authoring body: J. Doody; G. Burghardt; V. Dinets
  - Year if known: 2023
  - Locator or access note: DOI `10.1016/j.biopsycho.2023.108569` from Elicit export
  - Provisional role: evolutionary critique candidate
  - Why it may be central: candidate source for social-asocial dichotomy and
    evolutionary-claim appraisal.
  - Appraisal status: not appraised
- Source ID: `candidate-walz-grossman-2024-facts`
  - Title: `»Polyvagal«: Die schöne Theorie und die hässlichen Fakten`
  - Authors or authoring body: D. Walz; P. Grossman
  - Year if known: 2024
  - Locator or access note: DOI `10.30820/2364-1517-2024-2-163` from Elicit export
  - Provisional role: critique candidate
  - Why it may be central: candidate source for physiological-foundation and
    clinical-overreach critiques.
  - Appraisal status: not appraised

Candidate sources mentioned by the pasted synthesis but not yet represented as
verified CSV rows:

- Porges 2026 response to Grossman et al. critique; recover publisher metadata
  before using.
- Grossman 2007, 2023, and 2024 RSA/vagal-tone critique literature; recover
  exact metadata before using.
- Neuhuber and Berthoud neuroanatomical critique; recover exact metadata before
  using.
- Taylor comparative physiology review and lungfish/cardiorespiratory
  interaction literature; recover exact metadata before using.
- Safe and Sound Protocol, Family Nurture Intervention, and other clinical or
  acoustic intervention studies; recover exact metadata and appraise as
  clinical-usefulness evidence, not mechanistic proof.

## 4. Expected Gold-Set Behavior

Claims the output must support:

- Claim: Polyvagal theory is influential and clinically popular.
  - Evidence basis to be supplied by human reviewer:
- Claim: Some adjacent ideas about autonomic regulation and social safety may
  have broader support than the full theory.
  - Evidence basis to be supplied by human reviewer:

Claims the output must reject:

- Claim: Polyvagal theory is settled neuroscience.
  - Evidence basis to be supplied by human reviewer:
- Claim: General autonomic regulation evidence proves the full Polyvagal theory.
  - Evidence basis to be supplied by human reviewer:
- Claim: Polyvagal theory is entirely useless, disproven, or irrelevant.
  - Evidence basis to be supplied by human reviewer:

Claims that must remain uncertain:

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

- Expectation:
  - Evidence basis to be supplied by human reviewer:

## 5. Review State

Reviewer status:

- not started

Reviewer uncertainty:

- The target theory, domain, discovery databases, preferred source domains, date
  range, broad inclusion/exclusion criteria, and first-pass search strings are
  now supplied. A third-party discovery synthesis and Elicit candidate export
  have also been supplied. Exact executed search logs, verified source metadata,
  reviewed source roles, evidence bases, decoy reasons, and source-access limits
  have not been supplied yet.

Activation Decision:

- needs metadata verification and source appraisal

Activation decision rationale:

- The evaluation question, expected calibration, discovery strategy, and
  first-pass exact search strings are defined from human intake, and candidate
  discovery material has been recorded. The fixture still lacks human-reviewed
  source truth, verified metadata, executed search records, candidate source
  appraisals, decoy reasons, and evidence bases.
