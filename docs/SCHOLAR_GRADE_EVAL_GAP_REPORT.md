# Scholar-Grade Evaluation Gap Report

Date: 2026-05-18

This report audits the current evaluation system for Research Book Skills as a scholar-grade validation stack. It does not claim the current automated suite proves scholarly truth. The current harness is best understood as deterministic validation plus selected live/manual behavior samples.

## Audit basis

Inspected:

- `README.md`
- `tests/skill_evals/README.md`
- `tests/skill_evals/research_behavior/`
- `tests/skill_evals/scholar_grade/`
- `tests/skill_evals/scholar_grade/live_pilot/`
- `tests/skill_evals/scholar_grade/live_pilot_v2/`
- `scripts/run_package_checks.py`
- `validate.sh`
- evaluation coverage tests and harness code under `scripts/` and `tests/skill_evals/`

Observed local state:

- `tests/skill_evals/research_behavior/fixtures.json` contains 35 deterministic behavior fixtures covering 29 expected routes, with captured outputs and route traces present.
- `tests/skill_evals/scholar_grade/fixtures.json` contains 46 scholar-grade fixtures covering 29 skills, including 8 controlled adversarial-pressure fixtures under `tests/skill_evals/scholar_grade/adversarial_pressure/`.
- Scholar-grade source access coverage is mostly `controlled-packet` fixtures, with two `private-no-external` fixtures and one each for `prompt-only`, `public-metadata-only`, and `external-lookup-consented`.
- Every scholar-grade fixture has `human_review_required: true`, a `minimum_score` of 4, required source anchors, and semantic fail patterns.
- Default scholar-grade manifests are `deterministic-reference` with `model: not-run`; `live_pilot_v2` has 15 `manual-live-capture` artifacts, all from `codex-app`, `gpt-5`, one operator, and one capture date.
- At the time of the original audit, `live_pilot_v2` calibration reported ready with no actions or regressions. A later local recheck on 2026-05-20 found `prose-edit-changes-meaning` live-pilot manifests with stale `skill_file_sha256` values after a `dyslexia-friendly-prose-editor` skill change. Per the live-pilot docs, the correct repair is a new additive live capture root, not overwriting the original blind captures.

No material documentation/code drift was found in the evaluated area at the time of the original audit. The README, eval README, harness limits, `run_package_checks.py`, and `validate.sh` consistently describe default validation as deterministic and no-network, with live/manual capture separated from source-truth claims. Current live-pilot readiness must be rechecked after skill instruction changes.

## What the Current Suite Validates Well

The current suite is already strong for deterministic source-boundary discipline.

- `scripts/check_research_behavior_fixtures.py` validates fixture shape, expected route evidence, required output markers, forbidden claims, compact-output marker count, route trace schema, selected skill, prompt hash, output hash, and capture flags.
- `scripts/research_behavior_eval_harness.py` makes the deterministic/manual boundary explicit: it checks local captures and route traces, but does not run a model or verify source truth.
- `tests/skill_evals/test_skill_eval_coverage.py` requires every `skills/*/SKILL.md` route to have both a research-behavior fixture and a scholar-grade fixture.
- `tests/skill_evals/scholar_grade/scholar_grade_eval_harness.py` validates controlled packet structure, hidden `answer-key.md`, machine-checkable `answer-key.json`, source-packet leakage boundaries, resource-basis registry entries, required source anchors, required uncertainties, allowed-claim boundaries, disallowed claims, hard-fail patterns, semantic fail patterns, private-no-external policy, manifests, scores, and output hash binding.
- `tests/skill_evals/scholar_grade/live_capture_protocol.py` generates operator-facing prompt packets and checks that hidden answer-key values do not leak into live prompts.
- `tests/skill_evals/scholar_grade/run_live_capture.py` records prompt packets, captured outputs, manifests, score templates, and optional automated traces without overwriting by default.
- `tests/skill_evals/scholar_grade/live_pilot_calibration.py` compares live-pilot review scores against deterministic baseline scores and reports missing artifacts, validation failures, and score regressions.
- `tests/skill_evals/scholar_grade/mediocre_controls/` plus `test_shipped_mediocre_control_fails_review_score_gate` gives one intentional negative control proving that a basic marker-passing output can still fail the score gate.

This is a good deterministic validation base. It is especially good at preventing false confidence from fabricated citations, missing locators, overclaiming, compact-output blocker loss, privacy-boundary violations, unlogged AI workflow claims, and missing provenance in controlled local packets.

## What It Does Not and Cannot Validate

The current suite does not run the skills by default. Default package validation checks shipped artifacts and deterministic references. It can prove that the fixture and grader system is internally consistent; it cannot prove a current model will behave the same way.

The controlled packets are synthetic/local. They are useful for testing boundary discipline, but they do not establish real-world source truth, field consensus, citation existence, methodology validity, legal clearance, or publication readiness.

Marker and regex checks are useful but incomplete. Semantic fail patterns reduce false passes from paraphrased overclaims, but they cannot catch every subtle omission, hedged bad answer, misleading synthesis, or strategically vague output.

Review score files are human-entered but currently single-reviewer artifacts. The harness validates score completeness, hash binding, rationales, evidence notes, and minimum thresholds; it does not measure reviewer agreement.

The live pilot is a behavior sample, not stability evidence. `live_pilot_v2` covers 15 high-risk fixtures, but it uses one model family, one capture date, one interface, and one operator. It does not test repeated sessions, model drift, or operator variance.

Retrieval quality is mostly separate from synthesis quality. `scripts/check_source_candidates.py` validates local candidate exports, private field exclusion, completed-search evidence fields, metadata normalization, and duplicate clusters. It does not measure search recall, precision, source selection quality, or whether a source set is representative.

Long workflow traceability is not yet tested end to end. The suite checks per-fixture outputs, manifests, traces, and example artifact schemas. It does not follow a claim across router, discovery, notes, extraction table, literature map, claim ledger, traceability graph, and integrity gate in one auditable workflow.

## Validation Layer Distinctions

Deterministic fixture validation:

This is the default CI/package layer. It includes `research_behavior`, `scholar_grade`, deterministic reference outputs, manifests, score files, coverage tests, the v2 pilot gate, and active real-source gold-set readiness in `scripts/run_package_checks.py --scope full`. It validates local artifacts and harness integrity. It does not run a model and does not certify source truth.

Live skill behavior validation:

This is represented by `live_pilot/`, `live_pilot_v2/`, `run_live_capture.py`, `live_capture_protocol.py`, and `--require-live-captures`. It validates captured behavior from a real interface/model under recorded permissions. It is evidence about skill behavior in a specific run, not proof that the scholarly claim is true.

Source-truth validation:

This is not a mature layer yet. Current controlled packets have hidden answer keys, but they are mostly synthetic local truth sets. Real-source MVP gold sets can now validate recorded human-reviewed source-role packets and local live-test readiness, but that remains bounded to each packet and any explicit waiver. Mature source-truth validation would require public, licensed, or metadata-only gold sets where the expected claim/source relationship is independently known and auditable.

Human expert review:

The current score files enforce human review structure, but not independent expert judgment or inter-rater reliability. Expert review remains necessary for high-stakes claims about method validity, citation fit, publication readiness, privacy/legal clearance, and field consensus.

## Gap Table

| Gap | Why it matters | Current coverage, if any | Proposed test artifact | Proposed command or harness integration | Priority |
| --- | --- | --- | --- | --- | --- |
| Near-miss evaluator sensitivity beyond one negative control | A suite can pass marker-rich but substantively weak outputs unless it proves sensitivity to subtle bad answers. This is the highest risk for overclaiming scholar-grade defensibility. | `semantic_fail_patterns` exist on all scholar-grade fixtures; `tests/skill_evals/scholar_grade/mediocre_controls/` has one control for `unsupported-causal-claim`; `test_shipped_mediocre_control_fails_review_score_gate` verifies that one score failure. | Expand `tests/skill_evals/scholar_grade/mediocre_controls/` with near-miss outputs/scores/manifests for `quote-without-locator`, `literature-map-overstates-consensus`, `prose-edit-changes-meaning`, `book-comps-stale-mismatch`, and `claim-traceability-nearby-citation`. | Add a small expected-failure check in `tests/skill_evals/scholar_grade/test_scholar_grade_eval_harness.py` or a focused future negative-control checker that asserts these controls fail for the intended reasons. | P0 |
| Real-source gold sets for source-truth boundaries | "Scholar-grade" claims need at least some known real-source cases. Synthetic packets test discipline but not real citation/source fit. | `source-packet.md` plus hidden answer keys test local controlled truth; `resource-basis.json` documents justification sources; `scripts/check_source_candidates.py` checks local candidate exports only. | Add `tests/skill_evals/source_truth/fixtures.json` and `tests/skill_evals/source_truth/corpora/<fixture-id>/` using public-domain, permissively licensed, or metadata-only records. Store short permitted excerpts or source identifiers/checksums, not private or copyrighted full text. | Add `scripts/check_source_truth_fixtures.py --fixtures tests/skill_evals/source_truth/fixtures.json --outputs-dir tests/skill_evals/source_truth/outputs --quiet`; keep it separate from `--scope full` until stable. | P0 |
| Retrieval quality separated from synthesis quality | A skill may synthesize cautiously while retrieving a weak or biased source set. Current checks do not measure recall, precision, or representativeness. | `tests/skill_evals/source-candidates.json` and `scripts/check_source_candidates.py` validate local candidate hygiene, duplicate clusters, private fields, and completed-search evidence fields. | Add `tests/skill_evals/retrieval_quality/queries.json`, `gold-candidates.json`, and captured candidate exports for systematic-source-discovery and discovery-runner-deduper cases. | Either extend `scripts/check_source_candidates.py` with `--gold tests/skill_evals/retrieval_quality/gold-candidates.json` or add a future retrieval-quality checker; report precision/recall as diagnostic, not as a pass/fail truth certificate at first. | P0 |
| Adversarial user pressure and compliance pressure | Scholar-grade tools must refuse unsafe shortcuts when the user pushes for clearance, certainty, speed, or private-text submission. | Partially addressed by 8 synthetic scholar-grade fixtures under `tests/skill_evals/scholar_grade/adversarial_pressure/`, covering weak-evidence certainty, placeholder citations, hidden limitations, private-text online search, invented page locators, consensus overclaiming, compact-output blocker loss, and prose-repair claim strengthening. | Remaining future work, if needed, is matching research-behavior route fixtures or live captures for the same pressure families. Do not treat the synthetic packets as source-truth gold sets. | Existing scholar-grade harness and mutation checks validate the controlled pressure layer with no harness refactor. | P1 |
| Inter-rater reliability | Single-reviewer score files can encode one person's calibration. Scholar-grade claims need evidence that the rubric is understandable and stable across reviewers. | `scores/*.json` require rationales and evidence notes; baseline and live scores each have one reviewer label. No agreement check exists. | Add `tests/skill_evals/scholar_grade/reviewer_panels/live_pilot_v2/<reviewer-id>/<fixture-id>.json` for a small shared subset. | Add `scripts/check_reviewer_agreement.py --panel tests/skill_evals/scholar_grade/reviewer_panels/live_pilot_v2 --fixtures tests/skill_evals/scholar_grade/fixtures.json`; start with exact agreement and within-one-point agreement before considering heavier statistics. | P1 |
| Repeated live-run stability across models/sessions | One successful live capture does not show robustness. Model changes, session context, and operator behavior can change outputs. | `live_pilot/` has 8 manual captures for `gpt-5-codex`; `live_pilot_v2/` has 15 manual captures for `gpt-5`; both are additive roots and can be calibrated. | Add future additive roots such as `tests/skill_evals/scholar_grade/live_matrix/<model>-<date>/` or `live_pilot_v3/` with the same P0 fixture subset repeated across at least two sessions/models. | Reuse `live_pilot_calibration.py --pilot-plan ... --live-root ...`; add `scripts/compare_live_capture_roots.py --roots ...` only after two or more roots exist. | P1 |
| Long workflow traceability | Research-book work fails when claims lose provenance across multiple artifacts, not only in one isolated answer. | Per-fixture route traces, run manifests, and example book artifacts exist; no chained workflow trace follows a claim across skills. | Add one scenario under `tests/skill_evals/workflow_traces/<scenario-id>/` with `workflow-trace.json`, source packet hashes, artifact hashes, and a final claim ledger/traceability graph. | Add `scripts/check_workflow_traceability.py --trace tests/skill_evals/workflow_traces/<scenario-id>/workflow-trace.json`; validate hash continuity, claim IDs, source-note IDs, locators, and unresolved uncertainty propagation. | P1 |
| Automated live trace coverage | The harness supports automated trace validation, but current v2 pilot artifacts are manual captures, so tool counts, command counts, and token counts are not exercised by live artifacts. | `scholar_grade_eval_harness.py` validates `automated-live-capture` traces when present; `live_capture_protocol.py` writes trace templates; `live_pilot_v2` uses manual manifests. | Add two automated captures in a future additive root under `tests/skill_evals/scholar_grade/live_pilot_v3/traces/`, preferably `private-manuscript-search-consent` and `metadata-lookup-consented-identifiers`. | Existing scholar-grade harness with `--require-live-captures` validates automated traces. No new script needed unless comparing trace metrics over time. | P2 |
| Expert review records for publication-facing claims | Some claims require domain, legal, privacy, or methodology expertise. Automated and internal reviewer checks should not be presented as expert clearance. | `human_review_required` is true for all 46 fixtures; score files enforce rationale and evidence notes but not expert credentials or independent review. | Add optional `tests/skill_evals/scholar_grade/expert_reviews/<fixture-id>.json` for a small high-risk subset and a future scholar expert review protocol explaining when expert review is required. | Keep expert review outside default CI; optionally add a schema-only check later. | P2 |
| Discipline/source-type breadth | Current risks are well chosen for general research-book workflows, but not all disciplines, languages, archival materials, quantitative methods, or legal/privacy regimes are represented. | Existing fixtures cover broad source discipline, citation, privacy, figure/table, AI workflow, method, prose, and routing risks. | Add discipline extensions only when real use reveals a gap, e.g. `tests/skill_evals/scholar_grade/extensions/archival-locators/` or `extensions/quant-methods/`. | Run as optional extension fixtures with the existing scholar-grade harness before adding to full validation. | P2 |

## Highest-Risk Gaps

P0 gaps should be addressed before stronger public claims about scholar-grade defensibility:

- Near-miss evaluator sensitivity. The current single mediocre control is valuable but too narrow. Add expected-failing controls for multiple risk families before expanding broad fixture volume.
- Real-source gold sets. Synthetic packets are appropriate for local deterministic testing, but scholar-grade source defensibility needs a small, carefully licensed real-source layer.
- Retrieval quality split. Discovery and dedupe skills need candidate-level quality checks so cautious synthesis is not mistaken for a good search.

P1 gaps should follow once the P0 layer is stable:

- Adversarial pressure cases are now covered for the controlled scholar-grade fixture layer; remaining work would be route or live-capture coverage if needed.
- Reviewer agreement.
- Repeated live-run stability across models and sessions.
- Long workflow traceability across chained artifacts.

P2 gaps are useful but not blockers for the next defensibility layer:

- Automated trace coverage for selected live captures.
- Optional expert review record schema.
- Discipline/source-type extension packs.

## Recommended Implementation Sequence

1. Strengthen negative controls first. Expand `tests/skill_evals/scholar_grade/mediocre_controls/` and add an expected-failure check so the suite proves it can reject plausible weak outputs, not only accept good references.
2. Add a small source-truth layer. Start with 3 to 5 public or metadata-only cases under `tests/skill_evals/source_truth/`; do not put private, paywalled, or copyrighted full text into fixtures.
3. Split retrieval quality from synthesis quality. Add candidate-level gold checks for source discovery and dedupe before using live search outputs as evidence of scholarly quality.
4. Adversarial pressure cases now exist for the scholar-grade controlled-fixture layer. If the pressure layer needs to expand later, add matching `research_behavior` or live-capture coverage rather than adding more synthetic variants without a new failure mode.
5. Repeat the high-risk live subset across at least two additive live roots. Use existing `live_pilot_calibration.py` per root; only add a comparison script after there are multiple roots to compare.
6. Add a reviewer-panel layer for the same high-risk subset. Keep the first agreement metric simple: exact agreement, within-one-point agreement, and hard-fail agreement.
7. Add one long workflow trace. Do not build a full workflow simulator. Validate hash and claim lineage across a small staged scenario.

## Do Not Overbuild

Do not replace human review with an LLM judge. A judge model may be useful later as a triage aid, but it should not be the authority for source truth, methodology validity, or publication readiness.

Do not move live or source-truth checks into default `./validate.sh` until they are stable, deterministic enough for local use, and safe with no private data. The current default deterministic gate should stay fast, no-network, and reproducible.

Do not add broad "more tests for every skill" work without a named risk and a failure mode. Coverage already exists for every skill route; the next value is sensitivity and truth calibration, not fixture volume.

Do not include private manuscripts, unpublished source text, paywalled full text, or long copyrighted excerpts in fixtures. Use public metadata, permitted excerpts, checksums, or synthetic packets where appropriate.

Do not rename existing fixtures, scripts, or skills to make a cleaner taxonomy. The current layout is usable; the next layer should be additive.

Do not build dashboards, statistical reliability packages, or large benchmark machinery before the P0 controls exist. The immediate need is concrete failure sensitivity and small source-truth gold sets.

## Bottom Line

The current suite is merge-ready as a deterministic validation system for source-boundary discipline, capture provenance, fixture coverage, and reviewer-score completeness. It is not yet enough to defend broad "scholar-grade" claims about real source accuracy, retrieval quality, repeated model behavior, reviewer agreement, or long workflow provenance.

The smallest useful next move is not a broad refactor. It is an additive P0 layer: more expected-failing near-miss controls, a small real-source truth set, and retrieval-quality checks separated from synthesis-quality checks.
