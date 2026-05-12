# Routing matrix

Use this as the canonical route table for research-book skill selection. The router should choose the smallest useful skill. Use a short sequence only when the request crosses stages.

| Scenario | Route |
|---|---|
| Broad multi-stage book task, unclear next step, mixed sources plus argument plus chapters | `research-book-orchestrator` |
| Start research on a subject, broad topic, research question, scope, contribution, audience, evidence plan | `scholarly-research-agenda` |
| Find sources, search strategy, keyword bank, database plan, inclusion rules, citation chaining | `systematic-source-discovery` |
| Source list, field, debate, schools of thought, gaps, consensus, controversy, thesis implications | `literature-review-mapper` |
| Provided sources, citations, abstracts, PDFs, notes, bibliographies needing structured annotations | `annotated-bibliography-builder` |
| Source credibility, method, bias, generalizability, evidence strength, source-claim support | `methodology-source-auditor` |
| Drafts or outlines with major factual, empirical, causal, comparative, conceptual, theoretical, normative, predictive, or field-specific claims | `claim-evidence-ledger` |
| Thesis tree, warrants, assumptions, claim dependencies, book-level argument structure | `argument-architecture` |
| Challenge this, peer review, rival explanations, missing literatures, brittle thesis, one-sided argument | `counterargument-peer-review` |
| Chapter outline, section sequence, chapter thesis, evidence placement, transitions, chapter function | `chapter-architecture` |
| Research prose clarity, precision, structure, rhythm, compression, readability, or voice | `scholarly-prose-editor` |
| Citation accuracy, unsupported claims, quotes, page numbers, bibliography mismatch, source-claim fit | `citation-integrity-auditor` |
| Multiple chapters, whole manuscript, contradictions, repetition, concept drift, thesis drift, chapter order | `manuscript-continuity-editor` |
| Case selection, examples, analogies, comparison, counter-cases, cherry-picking risk | `case-study-integration` |
| Book proposal, pitch, contribution, audience, comparable titles, press positioning, chapter summaries | `book-proposal-scholarship` |

## Suggested next step gates

Use this table only for the optional final `## Suggested next step` section. It must name the risk reduced, use one skill max, and be omitted when it would add noise.

| Risk or prerequisite | Allowed next skill | Blocked early suggestion |
|---|---|---|
| High-level topic with unstable scope | `scholarly-research-agenda` | Source discovery or citation audit before the research question is stable |
| Stable question, no corpus | `systematic-source-discovery` | Literature mapping or citation audit before a search plan exists |
| Source list or corpus needing field structure | `literature-review-mapper` | Citation audit before there are citations, quotes, page numbers, bibliography entries, or cited claims |
| Source list needing source-level notes | `annotated-bibliography-builder` | Field synthesis when each source's argument, method, and limits are still unclear |
| Draft with claims but weak evidence mapping | `claim-evidence-ledger` | Citation audit before claims and evidence status are separated |
| Source credibility or source-claim fit concern | `methodology-source-auditor` | Prose editing that hides evidence-quality problems |
| Cited draft, direct quotes, page numbers, bibliography entries, or cited claims | `citation-integrity-auditor` | Citation audit when only a broad topic, uncited notes, or model knowledge exists |
| Thesis or argument structure issue | `argument-architecture` | Prose editing before claim dependencies and warrants are clear |
| One-sided or brittle argument | `counterargument-peer-review` | Citation audit when the stronger risk is missing objections or rival explanations |
| Chapter sequence or chapter function issue | `chapter-architecture` | Prose editing before section purpose, evidence placement, and transitions are clear |
| Evidence fixed but prose unclear | `scholarly-prose-editor` | Evidence audit when the remaining risk is readability or precision |
| No unresolved scholarly risk remains | No suggestion | Any skill promotion |

Do not suggest `citation-integrity-auditor` before citations, quotes, page numbers, bibliography entries, or cited claims exist.
