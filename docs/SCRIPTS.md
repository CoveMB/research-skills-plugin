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
| Run the full package check | `./validate.sh` | Runs the shared full validation suite through `scripts/run_package_checks.py`. |
| Run shared package checks directly | `python3 scripts/run_package_checks.py --scope full --root .` | Runs either the full validation suite or the smaller install preflight with `--scope install`. |
| Validate plugin structure | `python3 scripts/validate_plugin.py .` | Checks the manifest, skill folders, skill frontmatter, skill README files, agent metadata, duplicate prompts, and local docs links. |
| Validate book artifacts | `python3 scripts/check_book_artifact_contract.py --path .` | Checks the shared book artifact schema, artifact-specific field boundaries, optional handoff passport shape, and every JSON example under `examples/book_artifacts/`. |
| Check behavior fixtures | `python3 scripts/check_research_behavior_fixtures.py --fixtures examples/evals/research-skill-behavior-fixtures.json` | Checks high-risk behavior fixture shape; add `--outputs-dir path/to/outputs` to check captured local outputs. |
| Summarize behavior calibration | `python3 scripts/summarize_research_behavior_evals.py --fixtures examples/evals/research-skill-behavior-fixtures.json --outputs-dir examples/evals/outputs` | Reports fixture coverage, route coverage, compact-output coverage, and captured-output validation status. |
| Build behavior harness report | `python3 scripts/research_behavior_eval_harness.py --fixtures examples/evals/research-skill-behavior-fixtures.json --outputs-dir examples/evals/outputs` | Produces a deterministic JSON report; add `--format markdown` for a manual or live-run capture runbook. |
| Check source candidates | `python3 scripts/check_source_candidates.py --input path/to/source-candidates.json` | Parses local JSON or CSV candidate exports, clusters duplicates, and gates completed-search claims without network access. |
| Check citation metadata | `python3 scripts/check_citation_metadata.py --input path/to/public-metadata.json` | Compares local public metadata fields for DOI, ISBN, arXiv ID, PMID, OCLC, LCCN, normalized title, author-year, and venue mismatch risk. Default mode uses no network. |
| Run unit tests | `python3 -m unittest discover -s scripts -p 'test_*.py'` | Runs the script and package policy tests. |
| Package a zip | `python3 scripts/package_plugin.py --root .` | Writes a versioned zip in the current directory unless `--out` is supplied. |

## Script details

### Installer wrappers

`./install.sh` and `.\install.ps1` are thin wrappers around the Python installer. They select a Python executable, print a dry-run hint, and return the Python script exit code. Use `--dry-run` before a real install if you want to see the destination paths first.

The installer backs up an existing marketplace file before rewriting it. If the existing marketplace JSON cannot be parsed, it writes a timestamped backup and creates a fresh marketplace file.

### Validator

`scripts/run_package_checks.py` is the shared validation runner. `--scope install` runs the pre-install checks used by the local installer. `--scope full` runs plugin validation, artifact contract validation, behavior fixture validation, the behavior harness, and the unit test suite.

`scripts/validate_plugin.py` validates the package shape. It does not write files. It reports all validation errors it finds before exiting with status 1.

The validator checks:

- `.codex-plugin/plugin.json` exists and points to a local skills folder.
- each skill folder has `SKILL.md`, `README.md`, and `agents/openai.yaml`.
- each skill name is lowercase kebab-case and matches its folder.
- skill descriptions and agent metadata are present and stay aligned.
- agent policy metadata matches the shared per-skill lookup and privacy profile.
- local Markdown links and path references resolve inside the package.

### Book artifact contract checker

`scripts/check_book_artifact_contract.py` validates the shared artifact schema and shipped examples. It supports the schema keywords used by this package rather than acting as a full JSON Schema implementation. It also rejects fields that belong to another artifact type and validates `process_passport` shape when that optional handoff field is present.

Use this script after changing `shared/contracts/book/book_artifact.schema.json` or any file in `examples/book_artifacts/`.

### Research behavior fixture checker

`scripts/check_research_behavior_fixtures.py` validates prompt fixtures under `examples/evals/`. With `--outputs-dir`, it also checks one captured Markdown output per fixture id for required markers, forbidden claims, and compact-output result-use boundaries.

The checker is deterministic and no-network. It does not run a model or verify source truth; it only checks local fixture documents and local captured outputs.

`scripts/summarize_research_behavior_evals.py` writes a local JSON calibration report for the same fixture set. It reports fixture count, expected-route coverage, covered risks, compact fixture count, captured-output presence, and captured-output validation errors. This is a local benchmark report only: it does not run a model, verify source truth, or certify scholarly correctness.

`scripts/research_behavior_eval_harness.py` builds on the same deterministic checks and adds a per-fixture runbook. The JSON format is useful for automation; `--format markdown` prints the prompt, expected route, required markers, forbidden claims, output file name, manual/live capture expectations, and explicit limits for each fixture. Use `--quiet` when only the validation exit code matters. This harness does not run a model or call external services. It is meant to make manual or future live-run captures auditable while keeping the default package validation no-network and reproducible.

### Source candidate checker

`scripts/check_source_candidates.py` parses local JSON or CSV candidate exports into normalized candidate records and duplicate clusters. It dedupes by DOI or stable identifier first, then by normalized title as a review-needed cluster. It also rejects private text fields and flags records that claim a completed search without `search_venue`, `query`, and `date_searched`. Default mode is deterministic and no-network; use `--quiet` when only the validation exit code matters.

### Citation metadata checker

`scripts/check_citation_metadata.py` compares local JSON or CSV metadata exports. It checks format and exact normalized matches for public identifiers (`claimed_doi`/`authoritative_doi`, `claimed_isbn`/`authoritative_isbn`, `claimed_arxiv_id`/`authoritative_arxiv_id`, `claimed_pmid`/`authoritative_pmid`, `claimed_oclc`/`authoritative_oclc`, and `claimed_lccn`/`authoritative_lccn`) plus normalized title, author-year, and venue, then flags mismatch or identifier-hijack risk.

Default mode is deterministic and no-network. It rejects private fields such as `full_text`, `excerpt`, `abstract`, `notes`, `source_text`, and `private_notes`; pass public citation metadata only.

Optional public lookup is consent-gated. `--lookup-provider crossref --allow-network` can enrich missing authoritative metadata from Crossref by submitting DOI identifiers only. Do not pass draft text, source text, abstracts, notes, private fields, or manuscript excerpts to the checker.

### Packager

`scripts/package_plugin.py` writes a zip file for distribution. By default the file name is based on the repository folder and manifest version. Pass `--out path/to/file.zip` to choose a different output path.

The packager excludes generated files and local state, including `.git`, caches, virtual environments, build output, coverage output, logs, temporary files, and existing zip files.

### Tests

The test files under `scripts/` are part of the package quality gate. They check executable safeguards, plugin structure rules, source policy text, routing policy text, and book artifact validation behavior.

Run the full suite with `./validate.sh` before packaging or installing a changed copy.
