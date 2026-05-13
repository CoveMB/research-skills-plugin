# Routing matrix

Use this as the canonical route table for research-book skill selection. The router should choose the smallest useful skill. Use a short sequence only when the request crosses stages.

Accessibility entry rule: use `dictation-to-research-notes`, `reading-load-reducer`, or `dyslexia-friendly-prose-editor` when one clear bottleneck owns the request. Use `dyslexia-research-companion` only when the accessibility bottleneck is mixed, unclear, or explicitly requested as a wrapper.

| Scenario | Route |
|---|---|
| Dictated research thoughts, voice transcripts, speech-to-text output, meeting notes, rambling spoken fragments, or "I talked this out" notes | `dictation-to-research-notes` |
| Reading fatigue, dense article, too much to read, source triage, skim/read/skip decisions, close-reading targets, or reading-priority plan | `reading-load-reducer` |
| Spelling repair, grammar cleanup, dysorthographic prose, sentence-boundary repair, typo-heavy passage, or meaning-preserving edit of existing prose | `dyslexia-friendly-prose-editor` |
| Mixed or unclear accessibility bottleneck, broad dyslexia or dysorthographia support request, overlapping dictation plus reading load, spelling ambiguity plus rough notes, or explicit wrapper request | `dyslexia-research-companion` |
| User asks what research skill or mode to use, route is unclear, or request needs normal versus deep lookup gating | `research-intent-router` |
| Broad multi-stage book task, unclear next step, mixed sources plus argument plus chapters | `research-book-orchestrator` |
| Start research on a subject, broad topic, research question, scope, contribution, audience, evidence plan | `scholarly-research-agenda` |
| Find sources, search strategy, keyword bank, database plan, inclusion rules, citation chaining | `systematic-source-discovery` |
| Candidate source exports, completed search results, bibliography exports, tabular files, duplicate clusters, screening log, search-log update | `discovery-runner-deduper` |
| Reference-manager notes, document highlights, manual annotations, excerpts, or reading notes needing source-bound notes | `annotation-to-source-note` |
| Source notes, annotations, excerpts, or reading notes needing extraction tables, source matrices, or comparison grids | `extraction-table-builder` |
| Source list, field, debate, schools of thought, gaps, consensus, controversy, thesis implications | `literature-review-mapper` |
| Provided sources, citations, abstracts, PDFs, notes, bibliographies needing structured annotations | `annotated-bibliography-builder` |
| Source credibility, method, bias, generalizability, evidence strength, source-claim support | `methodology-source-auditor` |
| Drafts or outlines with major factual, empirical, causal, comparative, conceptual, theoretical, normative, predictive, or field-specific claims | `claim-evidence-ledger` |
| Existing claims needing trace to source notes, citekeys, locators, evidence status, missing links, or orphan-claim repair | `claim-traceability-graph` |
| Thesis tree, warrants, assumptions, claim dependencies, book-level argument structure | `argument-architecture` |
| Challenge this, peer review, rival explanations, missing literatures, brittle thesis, one-sided argument | `counterargument-peer-review` |
| Chapter outline, section sequence, chapter thesis, evidence placement, transitions, chapter function | `chapter-architecture` |
| Research prose clarity, precision, structure, rhythm, compression, readability, or voice | `scholarly-prose-editor` |
| Citation accuracy, unsupported claims, quotes, page numbers, bibliography mismatch, source-claim fit | `citation-integrity-auditor` |
| Figures, tables, charts, captions, axes, screenshots, visual evidence, data provenance, duplicate visual risk, or table/figure claim support | `figure-table-integrity-auditor` |
| Integrity gate, AI research failure modes, hallucinated evidence, methodology fabrication, implementation bug, shortcut reliance, frame-lock, or human checkpoint review | `scholarly-integrity-gate` |
| External sharing, release audit, privacy risk, copyright risk, quotation risk, license mismatch, secrets, credentials, or local metadata risk | `rights-privacy-release-auditor` |
| AI-use disclosure, human decision log, tool use record, override reason, affected sections, or human verification record | `ai-human-workflow-log` |
| Multiple chapters, whole manuscript, contradictions, repetition, concept drift, thesis drift, chapter order | `manuscript-continuity-editor` |
| Case selection, examples, analogies, comparison, counter-cases, cherry-picking risk | `case-study-integration` |
| Book proposal, pitch, contribution, audience, comparable titles, press positioning, chapter summaries | `book-proposal-scholarship` |
| Comparable titles, comps verification, audience claims, market claims, timeliness claims, press positioning | `book-comps-verifier` |

## Suggested next step gates

Use this table only for the optional final `## Suggested next step` section. It must name the risk reduced, use one skill max, and be omitted when it would add noise.

| Risk or prerequisite | Allowed next skill | Blocked early suggestion |
|---|---|---|
| Voice transcript or speech-to-text noise hides claims, questions, or evidence needs | `dictation-to-research-notes` | Prose editing or argument mapping before spoken ideas are segmented |
| Dense material or source volume blocks close reading | `reading-load-reducer` | Literature synthesis before read/skim/park/skip triage |
| Existing prose has spelling, grammar, or sentence-boundary friction | `dyslexia-friendly-prose-editor` | Broad style editing before meaning-preserving repair is done |
| Mixed or unclear accessibility bottleneck blocks the next scholarly action | `dyslexia-research-companion` | Prose editing, source synthesis, or audit before the user's intended claim, route, and ambiguity are clear |
| High-level topic with unstable scope | `scholarly-research-agenda` | Source discovery or citation audit before the research question is stable |
| Stable question, no corpus | `systematic-source-discovery` | Literature mapping or citation audit before a search plan exists |
| Completed candidate export with duplicates or unclear screening | `discovery-runner-deduper` | Adding candidates to a bibliography before dedupe and screening |
| Source annotations with unclear quote, paraphrase, metadata, or locator status | `annotation-to-source-note` | Claim drafting before source-bound notes exist |
| Source notes needing comparison before synthesis | `extraction-table-builder` | Literature synthesis when extraction is uneven |
| Source list or corpus needing field structure | `literature-review-mapper` | Citation audit before there are citations, quotes, page numbers, bibliography entries, or cited claims |
| Source list needing source-level notes | `annotated-bibliography-builder` | Field synthesis when each source's argument, method, and limits are still unclear |
| Draft with claims but weak evidence mapping | `claim-evidence-ledger` | Citation audit before claims and evidence status are separated |
| Claim ledger or cited draft with unclear evidence chain | `claim-traceability-graph` | Treating nearby citations as proof |
| Source credibility or source-claim fit concern | `methodology-source-auditor` | Prose editing that hides evidence-quality problems |
| Cited draft, direct quotes, page numbers, bibliography entries, or cited claims | `citation-integrity-auditor` | Citation audit when only a broad topic, uncited notes, or model knowledge exists |
| Figure/table carries a factual, empirical, comparative, quantitative, rights, or visual-evidence claim | `figure-table-integrity-auditor` | Treating polished visuals as verified evidence |
| AI-assisted analysis, generated synthesis, automated extraction, or computed result is about to support manuscript claims | `scholarly-integrity-gate` | Advancing without checking hallucinated evidence, methodology fabrication, shortcut reliance, frame-lock, or human checkpoints |
| Thesis or argument structure issue | `argument-architecture` | Prose editing before claim dependencies and warrants are clear |
| One-sided or brittle argument | `counterargument-peer-review` | Citation audit when the stronger risk is missing objections or rival explanations |
| Chapter sequence or chapter function issue | `chapter-architecture` | Prose editing before section purpose, evidence placement, and transitions are clear |
| Evidence fixed but prose unclear | `scholarly-prose-editor` | Evidence audit when the remaining risk is readability or precision |
| Proposal comps are unverified or stale | `book-comps-verifier` | Sending proposal positioning with unchecked publication details |
| AI-assisted work is headed to collaborators, reviewers, presses, committees, or public release | `ai-human-workflow-log` | External sharing without tool use, affected sections, human verification, and override reasons recorded |
| Artifact is about to be shared outside the project | `rights-privacy-release-auditor` | Sharing notes or exports before privacy, quote, license, and copied-text risks are checked |
| No unresolved scholarly risk remains | No suggestion | Any skill promotion |

Do not suggest `citation-integrity-auditor` before citations, quotes, page numbers, bibliography entries, or cited claims exist.
