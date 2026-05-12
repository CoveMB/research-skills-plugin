# Scholarly Research Book Skills Plugin

Version: 1.0.0

A local Agent Skills / Codex plugin for serious scholarly nonfiction and research book writing. It bundles 15 focused `SKILL.md` workflows for research agenda design, systematic source discovery, literature review mapping, source auditing, argument architecture, chapter structure, prose editing, citation integrity, manuscript continuity, case-study integration, and book proposal development.

## What this is

This is a **plugin package** with this structure:

```text
scholarly-research-book-plugin/
  .codex-plugin/plugin.json
  skills/
    scholarly-book-orchestrator/SKILL.md
    scholarly-research-agenda/SKILL.md
    ...
  docs/
  examples/
  scripts/
```

The plugin is designed for Codex-compatible local plugin installation and for any agent environment that supports the open `SKILL.md` folder convention.

## Fast install for Codex local plugin use

From the unzipped folder:

```bash
python3 scripts/install_codex_plugin.py
```

On Windows PowerShell:

```powershell
py scripts\install_codex_plugin.py
```

The installer validates the plugin, copies it to your local plugin directory, and creates or updates a personal marketplace file so Codex can discover it.

## Manual install options

See `docs/INSTALLATION.md` for:

- Codex personal marketplace install
- Codex repo marketplace install
- Direct local skill folder install
- ChatGPT upload notes
- Validation commands

## Skills included

See `docs/SKILL_INDEX.md` for the complete skill list and suggested use cases.

## Recommended first workflow

1. `scholarly-research-agenda`
2. `systematic-source-discovery`
3. `literature-review-mapper`
4. `argument-architecture`
5. `chapter-architecture`
6. `claim-evidence-ledger`
7. `counterargument-peer-review`
8. `citation-integrity-auditor`
9. `manuscript-continuity-editor`

## Quality standard

This plugin is designed to make the agent more rigorous, not merely faster. It repeatedly asks:

- What kind of claim is this?
- What source type can support it?
- What would an expert object to?
- Is the claim stronger than the evidence?
- Are citations real, relevant, and accurately used?

## Validation

```bash
python3 scripts/validate_plugin.py .
```

## License

MIT. See `LICENSE`.
