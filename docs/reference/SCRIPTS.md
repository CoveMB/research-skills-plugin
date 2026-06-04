# Script guide

Use these commands from the repository root unless a command says otherwise.

## Script requirements

These requirements apply only when you run the scripts. If you copy or upload skill folders by hand, you do not need Python.

- Python 3.10 or newer.
- No pip packages are required. The Python scripts use the standard library.
- `./install.sh` and `./validate.sh` need Bash on macOS or Linux.
- `.\install.ps1` needs PowerShell on Windows and one Python launcher in `PATH`: `py`, `python3`, or `python`.
- Install commands need write access to the local plugin directory and marketplace file.

## Common commands

| Task | Command | What it checks or writes |
| --- | --- | --- |
| Preview local install | `./install.sh --dry-run` | Validates the package and prints the install plan without copying files or writing marketplace JSON. |
| Install locally on macOS or Linux | `./install.sh` | Validates the package, copies it to the local plugin directory, and updates the personal marketplace file. |
| Install locally on Windows | `.\install.ps1` | Same installer flow through PowerShell. |
| Run source-checkout validation | `./validate.sh` | Runs the shared full validation suite when `tests/skill_evals` is present; falls back to the package-safe scope in packaged or installed copies. |
| Run shared package checks directly | `python3 scripts/run_package_checks.py --scope full --root .` | Runs the full source-checkout validation suite. Use `--scope package` for a packaged or installed copy without repo-only tests, or `--scope install` for the smaller install preflight. |
| Validate plugin structure | `python3 scripts/validate_plugin.py .` | Checks the manifest, skill folders, skill frontmatter, skill README files, agent metadata, duplicate prompts, and local docs links. |
| Validate book artifacts | `python3 scripts/check_book_artifact_contract.py --path .` | Checks the shared book artifact schema, artifact-specific field boundaries, conditional handoff passport requirements, every valid JSON example under `examples/book_artifacts/`, and expected-failing invalid examples under `examples/book_artifacts/invalid/`. |
| Check behavior fixtures | `python3 scripts/check_research_behavior_fixtures.py --fixtures tests/skill_evals/research_behavior/fixtures.json` | Checks high-risk behavior fixture shape; add `--outputs-dir path/to/outputs` to check captured local outputs and `--traces-dir path/to/traces` to check hash-linked route trace JSON. |
| Check workflow passports | `python3 scripts/check_workflow_passport_fixtures.py --fixtures tests/skill_evals/workflow_passports/fixtures.json` | Checks adjacent multi-skill handoff fixtures so downstream artifacts preserve unresolved risks, partial source access, human-review requirements, and unverified claim or locator-gap status. |
| Check workflow traceability | `python3 scripts/check_workflow_traceability.py --trace tests/skill_evals/workflow_traces/claim-lineage-fixture/workflow-trace.json` | Checks one deterministic multi-stage claim-lineage trace for artifact SHA-256 continuity, previous-artifact hash links, claim-ID/link integrity, tracked claim preservation, and non-upgrade of unresolved risks, partial-source labels, evidence status, locator gaps, and human-review requirements. |
| Summarize behavior calibration | `python3 scripts/summarize_research_behavior_evals.py --fixtures tests/skill_evals/research_behavior/fixtures.json --outputs-dir tests/skill_evals/research_behavior/outputs --traces-dir tests/skill_evals/research_behavior/traces` | Reports fixture coverage, route coverage, compact-output coverage, captured-output validation status, and route-trace validation status. |
| Build behavior harness report | `python3 scripts/research_behavior_eval_harness.py --fixtures tests/skill_evals/research_behavior/fixtures.json --outputs-dir tests/skill_evals/research_behavior/outputs --traces-dir tests/skill_evals/research_behavior/traces` | Produces a deterministic JSON report with output and hash-linked route-trace validation; add `--format markdown` for a manual or live-run capture runbook. |
| Build scholar-grade scorecard | `python3 tests/skill_evals/scholar_grade/scholar_grade_eval_harness.py --fixtures tests/skill_evals/scholar_grade/fixtures.json --outputs-dir tests/skill_evals/scholar_grade/outputs --manifests-dir tests/skill_evals/scholar_grade/manifests --scores-dir tests/skill_evals/scholar_grade/scores --format markdown` | Checks strict source-packet fixtures, captured outputs, run manifests, and review scores, then prints a rubric scorecard for human review. |
| Require live scholar-grade captures | `python3 tests/skill_evals/scholar_grade/scholar_grade_eval_harness.py --fixtures tests/skill_evals/scholar_grade/fixtures.json --outputs-dir tests/skill_evals/scholar_grade/outputs --manifests-dir tests/skill_evals/scholar_grade/manifests --scores-dir tests/skill_evals/scholar_grade/scores --require-live-captures --quiet` | Fails unless every run manifest records a manual or automated live skill capture with a real model and capture interface. |
| Validate one live scholar-grade capture | `python3 tests/skill_evals/scholar_grade/scholar_grade_eval_harness.py --fixtures tests/skill_evals/scholar_grade/fixtures.json --outputs-dir /tmp/scholar-live/outputs --manifests-dir /tmp/scholar-live/manifests --scores-dir /tmp/scholar-live/scores --fixture-id unsupported-causal-claim --require-live-captures --quiet` | Uses `--fixture-id` to validate an incremental live-capture subset while the rest of the suite is still deterministic. |
| Generate live capture protocol | `python3 tests/skill_evals/scholar_grade/live_capture_protocol.py --fixtures tests/skill_evals/scholar_grade/fixtures.json --root . --out-dir /tmp/scholar-live-capture` | Writes operator-facing prompt packets plus manifest, score, and automated trace templates without exposing hidden answer keys; add repeated `--fixture-id` values for a pilot subset. |
| Record live capture artifacts | `python3 tests/skill_evals/scholar_grade/run_live_capture.py --fixtures tests/skill_evals/scholar_grade/fixtures.json --root . --out-root tests/skill_evals/scholar_grade --fixture-id unsupported-causal-claim --captured-output /tmp/unsupported-causal-claim.md --interface codex-app --model gpt-5.4 --date 2026-05-14 --operator "Reviewer Name" --decision "Cannot support"` | Writes the prompt packet, captured output, run manifest, and score template with hashes; refuses to overwrite existing artifacts unless `--overwrite` is supplied. |
| Calibrate live pilot | `python3 tests/skill_evals/scholar_grade/live_pilot_calibration.py --format markdown` | Reports missing pilot artifacts, validation failures, and live-score regressions against deterministic baseline review scores; add `--strict` to fail when calibration is not ready. |
| Validate active real-source gold sets | `python3 scripts/run_package_checks.py --scope real-goldsets` | Validates real-source gold-set JSON and active local live-test readiness, including grader-field prompt leakage checks and reviewed candidate-output pass/fail coverage. |
| Check source candidates | `python3 scripts/check_source_candidates.py --input path/to/source-candidates.json` | Parses local JSON or CSV candidate exports, suggests duplicate or near-duplicate records, labels human-review needs, and gates completed-search claims without network access. |
| Check citation metadata | `python3 scripts/check_citation_metadata.py --input path/to/public-metadata.json` | Checks local public citation/source metadata for identifier format, internal consistency, missing fields, source-access labels, locator-support gaps, and cross-record conflict risk. Default mode uses no network. |
| Check figure/table provenance | `python3 scripts/check_figure_table_provenance.py --input path/to/figure-table-provenance.json` | Checks local figure, chart, and table provenance records for missing IDs, data source, source access, dataset version/date, transformations, denominators, aggregation, axes, units, caption/source consistency, uncertainty notes, rights, origin, unresolved gaps, and human-review need. Default mode uses no network. |
| Run unit tests | `python3 -m unittest discover -s scripts -p 'test_*.py' && python3 -m unittest discover -s tests -p 'test_*.py'` | Runs the script, package policy, and skill-evaluation tests. |
| Run package checks | `python3 scripts/run_package_checks.py --scope full` | Runs deterministic source-checkout validation plus the strict v3 additive live-pilot gate and active real-source gold-set readiness. Use `--scope package` for a packaged or installed copy without repo-only tests, `--scope live-pilot` for the original additive pilot report, `--scope live-pilot-v2` for the historical calibrated v2 pilot gate, `--scope live-pilot-v3` for the current strict calibrated recapture pilot, `--scope real-goldsets` for active real-source readiness, or `--scope live` only after replacing the shipped deterministic references with recorded live skill captures. |
| Package a zip | `python3 scripts/package_plugin.py --root .` | Writes a versioned zip in the current directory unless `--out` is supplied. |

## Script details

### Installer wrappers

`./install.sh` and `.\install.ps1` are thin wrappers around the Python installer. They select a Python executable, print a dry-run hint, and return the Python script exit code. Use `--dry-run` before a real install if you want to see the destination paths first.

The installer backs up an existing marketplace file before rewriting it. If the existing marketplace JSON cannot be parsed, it writes a timestamped backup and creates a fresh marketplace file.

### Validator

`scripts/run_package_checks.py` is the shared validation runner. `--scope install` runs the pre-install checks used by the local installer. `--scope package` runs the package-safe checks that work from a packaged or installed copy without repo-only `tests/` assets. `--scope full` runs source-checkout validation: plugin validation, artifact contract validation, behavior fixture validation, the behavior harness, workflow passport fixture validation, deterministic workflow traceability validation, scholar-grade skill evaluation checks, strict additive live-pilot v3 calibration, active real-source gold-set readiness, and the unit test suite. `--scope live-pilot` reports the original additive pilot recorded under `tests/skill_evals/scholar_grade/live_pilot/` without enforcing readiness, so historical stale-capture actions stay visible. `--scope live-pilot-v2` validates and strictly calibrates the recorded v2 pilot under `tests/skill_evals/scholar_grade/live_pilot_v2/`. `--scope live-pilot-v3` validates and strictly calibrates the current recapture root under `tests/skill_evals/scholar_grade/live_pilot_v3/`. `--scope real-goldsets` validates real-source gold-set JSON and active local live-test readiness; it does not run a model or certify source truth. `--scope live` runs the stricter recorded-live-capture gate for the whole scholar-grade suite and should be used after replacing deterministic reference manifests with real live capture artifacts. It is not part of the default CI gate and is expected to fail while the main scholar-grade manifests remain `deterministic-reference` records.

`scripts/validate_plugin.py` validates the package shape. It does not write files. It reports all validation errors it finds before exiting with status 1.

The validator checks:

- `.codex-plugin/plugin.json` exists and points to a local skills folder.
- each skill folder has `SKILL.md`, `README.md`, and `agents/openai.yaml`.
- each skill name is lowercase kebab-case and matches its folder.
- skill descriptions and agent metadata are present and stay aligned.
- agent policy metadata matches the shared per-skill lookup and privacy profile.
- local Markdown links and path references resolve inside the package.

### Book artifact contract checker

`scripts/check_book_artifact_contract.py` validates the shared artifact schema and shipped examples. It supports the schema keywords used by this package rather than acting as a full JSON Schema implementation. It also rejects fields that belong to another artifact type and validates `process_passport` shape when present.

Durable handoff artifacts use `handoff_artifact: true`; that conditional marker requires `process_passport`. Draft, casual, non-persisted, or non-handoff artifacts can still validate without a passport. Invalid examples under `examples/book_artifacts/invalid/` must be valid JSON but fail schema validation; the shipped invalid examples currently keep missing-passport coverage executable, while fake-verification and unsupported-upgrade coverage lives in the workflow passport and traceability checkers.

Use this script after changing `shared/contracts/book/book_artifact.schema.json`, `docs/policy/PROCESS_PASSPORT.md`, or any file in `examples/book_artifacts/`.

### Research behavior fixture checker

`scripts/check_research_behavior_fixtures.py` validates prompt fixtures under `tests/skill_evals/research_behavior/`. With `--outputs-dir`, it also checks one captured Markdown output per fixture id for selected-skill evidence, required markers, forbidden claims, and compact-output result-use boundaries. With `--traces-dir`, it checks one route trace JSON per fixture id using `schema_version: research-behavior-route-trace-v2`, matching `fixture_id`, matching `selected_skill`, matching `prompt_sha256`, and true `skill_invoked`, `prompt_supplied`, and `output_captured` flags. When both `--outputs-dir` and `--traces-dir` are supplied, it also checks `output_sha256` against the captured Markdown file so stale traces fail validation.

The checker is deterministic and no-network. It does not run a model or verify source truth; it only checks local fixture documents and local captured outputs.

`scripts/summarize_research_behavior_evals.py` prints a JSON calibration report for the same fixture set to stdout; redirect the command output if a local file is needed. It reports fixture count, expected-route coverage, covered risks, compact fixture count, captured-output presence, captured-output validation errors, route-trace presence, and route-trace validation errors. This is a local benchmark report only: it does not run a model, verify source truth, or certify scholarly correctness.

`scripts/research_behavior_eval_harness.py` builds on the same deterministic checks and adds a per-fixture runbook. The JSON format is useful for automation; `--format markdown` prints the prompt, expected route, required markers, forbidden claims, output file name, route trace file name, manual/live capture expectations, and explicit limits for each fixture. Use `--quiet` when only the validation exit code matters. This harness does not run a model or call external services. It is meant to make manual or future live-run captures auditable while keeping the default package validation no-network and reproducible. Route traces are evidence about activation and capture provenance; they do not certify source truth or scholarly correctness.

### Workflow passport fixture checker

`scripts/check_workflow_passport_fixtures.py` validates `tests/skill_evals/workflow_passports/fixtures.json`. Each fixture pairs an upstream handoff artifact with an expected downstream artifact and requires both to include process passports. The checker verifies that the input artifact includes unresolved risks, a partial-source access label, human-review need, and an unverified claim or locator gap, then checks that the downstream artifact preserves those limits unless a fixture explicitly records a justified resolution. It also mutates each expected output to confirm that removing unresolved risks, upgrading partial source access to full-text verification, or dropping human-review requirements would fail the fixture.

The workflow passport checker is deterministic and no-network. It validates adjacent handoff preservation; it does not run a skill, verify source truth, or prove end-to-end claim lineage across a complete book workflow.

### Workflow traceability checker

`scripts/check_workflow_traceability.py` validates `tests/skill_evals/workflow_traces/claim-lineage-fixture/workflow-trace.json`. The shipped trace follows one synthetic claim through source discovery, extraction, literature mapping, argument architecture, claim ledger, citation audit, chapter-draft, and integrity-gate trace artifacts. These trace artifacts use `schema_version: workflow-trace-artifact-v1`; they are not valid `book-artifact-v1` contract examples. Each stage records the artifact path, artifact SHA-256, previous artifact id, and previous artifact SHA-256; each downstream passport also records the previous artifact hash in `input_artifact_hashes`.

The checker rejects stale artifact hashes, missing parent hashes, duplicate claim IDs within an artifact, claim IDs referenced by traceability links but not defined, defined claims that are neither tracked nor linked, dropped tracked claim IDs, silent claim-text changes, evidence-status upgrades without a scoped verification event or justification, source locator removal, source-basis label removal, unresolved-risk removal without a valid verification event, claim-type changes without explanation, same-source reuse across different claim types without a source-claim-fit note, partial-source-to-full-text upgrades, locator-gap upgrades, and erased human-review requirements.

This is deterministic and no-network. It checks structural traceability and status consistency only. It does not judge whether an argument is good, verify source truth, measure source retrieval quality, assess source-claim fit, or prove that a real book workflow has been correctly researched.

### Scholar-grade evaluation harness

`tests/skill_evals/scholar_grade/scholar_grade_eval_harness.py` validates stricter fixtures in `tests/skill_evals/scholar_grade/fixtures.json`. These fixtures add a local controlled source packet, source access level, reviewed `resource_basis`, expected decision, required uncertainties, allowed and disallowed claims, hard-fail regexes, rubric dimensions, minimum score, and a human-review flag. Shipped `resource_basis` slugs are checked against `tests/skill_evals/scholar_grade/resource-basis.json`, which records source titles, URLs, usage notes, and access dates or snapshot hashes.

Each controlled source packet directory must include visible `source-packet.md` material, hidden `answer-key.md` evaluation prose, and hidden `answer-key.json` fields for `must_support`, `must_reject`, and `must_remain_uncertain`. With `--outputs-dir tests/skill_evals/scholar_grade/outputs`, the harness checks one captured Markdown output per fixture id for required markers, required source anchors, required uncertainties, allowed-claim boundaries, expected decision text, disallowed claims, hidden evaluation markers such as `answer-key.md`, global hard-fail patterns, private-text external-submission claims, fixture-specific hard-fail patterns, and semantic fail patterns for paraphrased overclaims. Global hard-fail phrase checks ignore directly negated uses such as `not safe to publish` so correct blocking language is not penalized. Fixture `score_anchors` must cover every rubric dimension with non-empty anchors for scores 3, 4, and 5. With `--manifests-dir tests/skill_evals/scholar_grade/manifests`, it also validates one run manifest per fixture id for capture metadata, real calendar dates, source/prompt/output/skill hashes, structured reviewer decisions, stricter `private-no-external` network/tool boundaries, `TODO_*` placeholder residue, and trace evidence for `automated-live-capture`. The manifest `prompt_packet_sha256` must match an existing sibling `prompts/<fixture-id>.md` packet; a missing prompt packet fails manifest validation. Automated trace files must stay inside the repository, match `trace_sha256`, and identify the fixture, skill, model, selected skill, tool/network permissions, skill invocation, source-packet supply, output capture, tool/command counts, and token usage. Add `--require-live-captures` when the goal is to validate actual skill behavior rather than deterministic reference fixtures; that mode rejects `deterministic-reference`, `not-run`, and local-fixture capture metadata. Add one or more `--fixture-id` values to validate an incremental subset. With `--scores-dir tests/skill_evals/scholar_grade/scores`, it validates one review score per fixture id against rubric dimensions, rejects `TODO_*` reviewer/rationale placeholders, requires one non-placeholder rationale per rubric dimension, requires evidence notes and answer-key findings, requires real calendar review dates, binds the score to the reviewed output hash, and requires every dimension, not only the average, to meet `minimum_score`. Use `--format markdown` to print a reviewer scorecard that includes score anchors. The scorecard supports human or future live-run review; it does not run a model or certify source truth. In a source checkout, see `tests/skill_evals/README.md` for the pass/fail standard.

`tests/skill_evals/scholar_grade/live_capture_protocol.py` creates live/manual capture scaffolds. `--check` validates that generated prompt packets do not expose `answer-key.md`, hidden field names, or fixture-specific hidden values such as expected decisions, required uncertainties, disallowed claims, hard-fail patterns, semantic fail patterns, and rubric dimensions unless those values already appear in the visible source packet. Disallowed-claim and fail-pattern values may also appear when they are already part of the user prompt because adversarial prompts often quote the bad claim the skill must reject. With `--out-dir`, it writes `capture-plan.json`, one prompt packet per fixture, one run-manifest template per fixture, one review-score template per fixture, and one automated trace template per fixture. Add one or more `--fixture-id` values to generate only a pilot subset. These template files intentionally contain `TODO_*` placeholders and must be completed before they are copied into harness `manifests/` or `scores/`. For automated captures, complete the trace template with selected skill, tool/network permissions, tool/command counts, and token usage, then save it at the manifest `trace_file` path and record `trace_sha256`.

`tests/skill_evals/scholar_grade/run_live_capture.py` records one completed capture at a time. Use `--dry-run` first to inspect the target prompt, output, manifest, and score-template paths. A real record requires an explicit `--fixture-id`, captured Markdown output, live model, interface, operator, date, and structured decision; the script then writes the prompt packet, `outputs/<fixture-id>.md`, `manifests/<fixture-id>.json`, and `score-templates/<fixture-id>.json` with source, prompt, skill, output, reviewed-output hashes, per-dimension rationale placeholders, evidence-note placeholders, and answer-key-finding placeholders. For `automated-live-capture`, pass `--trace-source` so the completed trace is written under `traces/` and the manifest receives a root-relative `trace_file` plus `trace_sha256`. Existing artifacts are protected unless `--overwrite` is supplied.

`tests/skill_evals/scholar_grade/live_pilot_calibration.py` reports whether an additive live pilot is ready for score calibration. By default it reads `live_pilot/fixture-ids.json`; pass `--pilot-plan` and `--live-root` to calibrate another additive root such as `live_pilot_v2` or the completed `live_pilot_v3` recapture root. It checks recorded pilot artifacts with the scholar-grade harness in live-capture mode, compares live review scores against deterministic baseline scores, and emits actions for missing captures, missing baseline review scores, validation failures, or score regressions. Default mode exits 0 so the report can be generated before captures exist; pass `--strict` after recording the pilot to make missing artifacts, missing baselines, validation failures, or regressions fail the command.

### Source candidate checker

`scripts/check_source_candidates.py` parses local JSON or CSV candidate exports into normalized candidate records, candidate duplicate clusters, metadata warnings, and search-status validation. It suggests duplicates; it does not merge records, verify citation truth, run searches, or add records to a bibliography.

Duplicate labels are deterministic screening labels:

- `exact_duplicate`: exact DOI, normalized DOI, or stable identifier match with no visible false-merge warning.
- `probable_duplicate`: normalized-title match or author-year-title similarity at or above `0.86`.
- `possible_duplicate`: title-only similarity at or above `0.82`.
- `related_but_distinct`: duplicate-like title or identifier evidence with false-merge warnings such as conflicting author/year metadata, edition/version distinction, or preprint/published distinction.
- `insufficient_metadata`: a record lacks enough title or identifier metadata for reliable dedupe review.

Every duplicate cluster includes `match_basis`, `match_reasons`, `confidence`, `human_review_required`, `preserve_records`, and `false_merge_warnings`. The helper treats title-only matches, conflicting metadata, edition/version distinctions, preprint/published pairs, and translated or alternate-title cases as review-required. Default mode is deterministic and no-network; use `--quiet` when only the validation exit code matters.

### Citation metadata checker

`scripts/check_citation_metadata.py` checks local JSON or CSV metadata exports. It checks format and exact normalized matches for public identifiers (`claimed_doi`/`authoritative_doi`, `claimed_isbn`/`authoritative_isbn`, `claimed_arxiv_id`/`authoritative_arxiv_id`, `claimed_pmid`/`authoritative_pmid`, `claimed_oclc`/`authoritative_oclc`, and `claimed_lccn`/`authoritative_lccn`) plus normalized title, author-year, and venue, then flags mismatch or identifier-hijack risk.

It also performs deterministic local checks for missing title, missing source access level, missing author/editor where the source type requires one, impossible or suspicious publication years, DOI field variants that disagree, venue or publisher field variants that disagree, suspicious page ranges, locator claims without page/section/paragraph/locator support, repeated citation keys pointing to different works, the same DOI attached to conflicting titles, and the same normalized title attached to conflicting DOI, author, or year metadata.

The report separates:

- `metadata_consistency_status`: whether the provided fields are internally consistent, partly unchecked, or issue-bearing.
- `external_verification_status`: whether an allowed metadata lookup was performed. In default local mode this remains `not_verified`.
- `source_existence_status`: whether the helper has external source-existence evidence. In default local mode this remains `not_verified`.
- `source_claim_support_status`: always `not_checked`; metadata cannot prove that a source supports a manuscript claim.
- `source_access_status`: a normalized access label such as `citation_only`, `abstract_only`, `public_metadata_only`, or `not_specified`.

Default mode is deterministic and no-network. It rejects private fields such as `full_text`, `excerpt`, `abstract`, `notes`, `source_text`, and `private_notes`; pass public citation metadata only. Input fields that claim a prior lookup do not set the checker-attested `external_verification_status` or `source_existence_status`; those fields are derived only from the current run's consented lookup state.

Optional public lookup is consent-gated. `--lookup-provider crossref --allow-network` can enrich missing authoritative metadata from Crossref by submitting DOI identifiers only; use `--lookup-timeout seconds` to keep that explicit lookup bounded. Do not pass draft text, source text, abstracts, notes, private fields, or manuscript excerpts to the checker.

Limitations: a syntactically valid DOI is not evidence that the DOI is real. An internally consistent citation is not evidence that the source exists. A source-existence check is not evidence that the source supports a claim, quote, paraphrase, page number, or method characterization. Locator-dependent claims still require source content and stable locator support.

### Figure/table provenance checker

`scripts/check_figure_table_provenance.py` checks local JSON or CSV records for figures, tables, charts, graphs, maps, and generated visual/table evidence. It accepts a list or an object with `records`, `figures`, `tables`, `objects`, or `figure_table_checks`.

The checker validates structural provenance fields: figure/table ID, data source, source access level, date accessed or dataset version, transformation or calculation notes, denominator or sample-size fields when relevant, aggregation level, axis labels, units, caption/source consistency, uncertainty or confidence-interval notes when relevant, rights or license status, whether the object is original/adapted/reproduced/generated, unresolved provenance gaps, and human-review requirement.

The checker reports `provenance_complete` only when no deterministic gaps are visible. It reports `provenance_gaps` with issue codes such as `missing_data_source`, `missing_denominator_or_sample_size`, `caption_source_mismatch`, `unknown_rights_or_license`, and `generated_without_provenance`. The shipped examples are `examples/figure_table_provenance/valid-provenance.json` and `examples/figure_table_provenance/invalid-provenance.json`.

Default mode is deterministic and no-network. It does not inspect image pixels, verify data truth, recompute calculations, clear rights, or judge whether the object supports a manuscript claim. Data-value verification requires supplied source data plus reproducible calculation records; otherwise `data_value_verification_status` remains `not_checked`.

### Packager

`scripts/package_plugin.py` writes a zip file for distribution. By default the file name is `<manifest-name>-v<manifest-version>.zip`. Pass `--out path/to/file.zip` to choose a different output path.

The packager excludes generated files and local state, including `.git`, caches, virtual environments, build output, coverage output, logs, temporary files, and existing zip files.

### Tests

The test files under `scripts/` are part of the package quality gate. They check executable safeguards, plugin structure rules, source policy text, routing policy text, and book artifact validation behavior.

Run the full source-checkout suite with `./validate.sh` before packaging or installing a changed copy. Packaged or installed copies without `tests/skill_evals` should use `python3 scripts/run_package_checks.py --scope package`.
