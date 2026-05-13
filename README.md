# Research Book Skills

Version: 1.0.0

Research Book Skills is a local skills plugin for people writing scholarly nonfiction, research monographs, long-form essays, or book proposals. It helps turn loose research work into concrete artifacts: low-load research notes, dictation notes, reading triage, meaning-preserving prose repair, a research agenda, source discovery log, source notes, extraction tables, literature map, thesis tree, chapter brief, claim ledger, claim traceability graph, citation audit, figure/table integrity audit, scholarly integrity gate, AI/human workflow log, release audit, continuity review, comparable-title check, and proposal.

The package assumes a person is still doing the research. It can sort, pressure-test, and clean up the work, but it will not treat model memory as source verification. It keeps asking practical scholarly questions: what kind of claim is this, what evidence can support it, where is the argument too strong, and what would an expert reader challenge?

It also includes accessibility skills for dyslexic, dysorthographic, dictation-heavy, or reading-fatigued authors. These skills turn rough thoughts, typo-heavy notes, voice transcripts, dense material, and existing prose into short tables, repair passes, and next actions without changing the author's meaning.

## Install in 30 seconds

If you use this as a collection of skill folders, you do not need Python. Python 3.10 or newer is only needed for the bundled install, validation, and packaging scripts. Those scripts use the Python standard library, so there is no dependency install step.

From the unzipped folder:

```bash
./install.sh
```

On Windows PowerShell:

```powershell
.\install.ps1
```

The installer validates the package, copies it to your local plugin directory, and updates your personal marketplace file. Restart the app after installation, then enable **Research Book Skills** from the plugin directory.

Preview the install first:

```bash
./install.sh --dry-run
```

Full manual install paths are in [`docs/INSTALLATION.md`](docs/INSTALLATION.md). The manual guide covers personal marketplace install, direct skill-folder install, upload notes for single-skill environments, validation, and uninstall steps.

## Try it first

Use `research-intent-router` when the next skill is unclear:

```text
Use research-intent-router. I want to write a research book about urban climate adaptation. Route this request and tell me the smallest useful next step.
```

Use the narrower accessibility skills when the bottleneck is clear:

```text
Use dictation-to-research-notes. Turn this voice transcript into claims, questions, evidence needs, ambiguities, and next actions.
```

```text
Use reading-load-reducer. Tell me what to read closely, skim, park, or skip for this chapter.
```

```text
Use dyslexia-friendly-prose-editor. Fix spelling and sentence boundaries without changing my argument.
```

Use `dyslexia-research-companion` when the accessibility bottleneck is mixed or unclear:

```text
Use dyslexia-research-companion. I have rough notes, dictation fragments, and too much source material. Choose the smallest low-load first step without changing my meaning.
```

For a full project plan:

```text
Use research-book-orchestrator. I am writing a research nonfiction book about urban climate adaptation. Build a staged research and writing workflow with quality gates.
```

For an existing draft:

```text
Use claim-evidence-ledger. Audit this chapter for unsupported claims, overclaiming, and citation needs.
```

For citation problems:

```text
Use citation-integrity-auditor. Check whether the citations in this draft support the claims they are attached to.
```

For figure, table, or AI workflow integrity:

```text
Use figure-table-integrity-auditor. Check these figures and tables for data provenance, caption accuracy, axis issues, and duplicate visual risk.
```

```text
Use scholarly-integrity-gate. Check this AI-assisted analysis for hallucinated evidence, methodology fabrication, shortcut reliance, frame-lock, and human checkpoint gaps.
```

```text
Use ai-human-workflow-log. Record tool use, affected sections, human decisions, verification responsibilities, and AI-use disclosure notes for this project.
```

For source notes:

```text
Use annotation-to-source-note. Turn these document highlights into source-bound notes and flag missing locators.
```

For release review:

```text
Use rights-privacy-release-auditor. Check this proposal packet before I share it outside the project.
```

## What it helps with

Use this package when the project needs clearer research structure, stricter source discipline, stronger argument design, or manuscript repair. It works before drafting, while drafting, and after a draft exists.

Typical jobs:

- turn a broad book idea into research questions, scope boundaries, and contribution claims
- turn rough notes, dictation, fragments, or dense source material into low-load research structures
- turn voice transcripts into structured scholarly notes
- reduce dense source material into read/skim/park/skip triage
- repair spelling, grammar, and sentence boundaries without changing meaning
- design a repeatable source search instead of collecting sources randomly
- dedupe candidate source exports and keep search logs honest
- turn annotations and highlights into source-bound notes
- build extraction tables before trying to synthesize uneven notes
- map a literature into schools, debates, gaps, and usable chapter logic
- build a thesis tree with warrants, assumptions, evidence, and counterarguments
- audit claims for evidence strength, citation needs, and overstatement
- trace claims to source notes, citekeys, locators, and repair actions
- check citation/source fit without inventing page numbers or fake references
- audit figures and tables for data provenance, captions, axes, duplicate visual risk, and claim support
- run an integrity gate before AI-assisted analyses or generated syntheses support manuscript claims
- record AI/human workflow decisions, affected sections, verification responsibilities, overrides, and disclosure notes
- audit release packets for privacy, copyright, quote, license, and local metadata risks
- verify comparable titles before proposal submission
- keep chapters consistent across concepts, tone, thesis, and structure
- shape a research book proposal around the actual argument and source base

## Choose a workflow

Use [`docs/SKILL_INDEX.md`](docs/SKILL_INDEX.md) for the full skill list and [`docs/ROUTING_MATRIX.md`](docs/ROUTING_MATRIX.md) for canonical routing. The short version is:

- voice transcript only: use `dictation-to-research-notes`
- too much to read: use `reading-load-reducer`
- existing prose needs spelling or sentence repair: use `dyslexia-friendly-prose-editor`
- mixed or unclear accessibility bottleneck: start with `dyslexia-research-companion`
- unclear request: start with `research-intent-router`
- whole-project planning: use `research-book-orchestrator`
- source, note, extraction, argument, chapter, claim, citation, figure/table, integrity, AI/human log, release, continuity, and proposal work: choose the narrow specialist in the skill index

Every skill folder has its own `README.md` with example requests, useful inputs, expected outputs, and common failure modes.

## Mode and automation summary

This package does not install scheduled background jobs. Its "automation" is routing: the router and orchestrator decide which workflow should run, how deep source lookup should go, and what artifact should come next.

The common route modes are `accessibility-companion`, `dictation-notes`, `reading-load`, `accessible-prose-repair`, `research-route-normal`, and `research-route-deep`. See `MODE_REGISTRY.md` for the full registry and [`docs/ROUTING_MATRIX.md`](docs/ROUTING_MATRIX.md) for routing rules.

## Source lookup modes

Normal mode is the default. It classifies the task and chooses the smallest useful skill before doing any deep lookup. It escalates only when source finding, source existence, quote/page verification, current facts, or high-risk claims make lookup necessary.

Deep mode always attempts lookup after routing and after forming a concrete lookup target object. If lookup tools, source access, full text, or a concrete target are unavailable, the result stays marked as unverified.

Use these prompts:

```text
Use research-intent-router in normal mode. Route this research request first.
```

```text
Use research-intent-router in deep mode. Route this request and attempt source lookup where available.
```

## Artifacts and examples

The plugin includes a shared book artifact schema at [`shared/contracts/book/book_artifact.schema.json`](shared/contracts/book/book_artifact.schema.json). Example artifacts live in [`examples/book_artifacts/`](examples/book_artifacts/):

- `book-research-agenda.json`
- `source-discovery-log.json`
- `literature-map.json`
- `thesis-tree.json`
- `chapter-brief.json`
- `claim-evidence-ledger.json`
- `source-note.json`
- `extraction-table.json`
- `claim-traceability-graph.json`
- `citation-integrity-audit.json`
- `figure-table-integrity-audit.json`
- `scholarly-integrity-audit.json`
- `ai-human-workflow-log.json`
- `rights-privacy-release-audit.json`
- `comps-verification.json`
- `continuity-review.json`
- `book-proposal.json`

These artifacts are useful when a project needs to stay coherent across sessions, tools, or chapter drafts.

## Limits

Research Book Skills is strict about source truth:

- no fabricated citations, page numbers, quotes, DOI metadata, or bibliographic claims
- no model memory treated as source verification
- no claims about field consensus without a representative source set or lookup result
- no overwriting manuscript files, source files, bibliography databases, or plugin files unless you ask for that directly

It also does not replace a researcher, editor, advisor, peer reviewer, or fact-checker.

## Package layout

```text
scholarly-research-book-plugin/
  .codex-plugin/plugin.json
  skills/
    dyslexia-research-companion/
    dictation-to-research-notes/
    reading-load-reducer/
    dyslexia-friendly-prose-editor/
    research-intent-router/
    research-book-orchestrator/
    scholarly-research-agenda/
    ...
  docs/
  examples/
  shared/
  scripts/
```

The package works as a local plugin and as a portable collection of `SKILL.md` folders.

## Validate

Run the full local check:

```bash
./validate.sh
```

Or run the checks one by one:

```bash
python3 scripts/validate_plugin.py .
python3 scripts/check_book_artifact_contract.py --path .
python3 -m unittest discover -s scripts -p 'test_*.py'
```

Script details, arguments, side effects, and dependency notes are in [`docs/SCRIPTS.md`](docs/SCRIPTS.md).

## Useful docs

- [`docs/INSTALLATION.md`](docs/INSTALLATION.md): manual install options and uninstall steps
- [`docs/SKILL_INDEX.md`](docs/SKILL_INDEX.md): all skills and when to use them
- [`docs/SCRIPTS.md`](docs/SCRIPTS.md): script commands, requirements, and write behavior
- [`docs/WORKFLOW_PLAYBOOK.md`](docs/WORKFLOW_PLAYBOOK.md): practical book workflows
- [`docs/QUALITY_STANDARD.md`](docs/QUALITY_STANDARD.md): source, claim, and citation standards
- [`docs/SOURCE_LIMITS.md`](docs/SOURCE_LIMITS.md): what counts as verified source access
- [`docs/ROUTING_MATRIX.md`](docs/ROUTING_MATRIX.md): canonical route choices, including accessibility entry points
- [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md): common setup and routing issues

## License

MIT. See [`LICENSE`](LICENSE).
