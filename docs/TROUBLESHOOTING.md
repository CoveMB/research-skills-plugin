# Troubleshooting

## The plugin does not appear

- Restart the app.
- Run `python3 scripts/validate_plugin.py .` from the plugin root.
- Check that `.codex-plugin/plugin.json` exists.
- Check that the marketplace file contains a `research-skills-plugin` entry.
- Check that the plugin folder was copied to `~/.codex/plugins/research-skills-plugin`.

## Python is missing or too old

Python is only required for the bundled scripts. If you are copying skill folders by hand, you can skip this section.

The scripts need Python 3.10 or newer. On macOS or Linux, run:

```bash
python3 --version
```

On Windows PowerShell, run:

```powershell
py --version
```

If the command is missing or reports an older version, install a current Python release and make sure the launcher is in `PATH`.

## Install fails with a permission error

Run `./install.sh --dry-run` or `.\install.ps1 --dry-run` to see the paths before writing. The installer needs write access to the plugin destination and marketplace JSON. If you pass `--dest` or `--marketplace`, check those paths first.

## Marketplace JSON cannot be parsed

The installer backs up the existing marketplace file with a timestamped `.backup-*` suffix, then creates a fresh marketplace file. Compare the backup with the new file before deleting anything.

## Package creation fails

`scripts/package_plugin.py` writes the zip to the current directory by default. If that directory is read-only, pass `--out` with a writable path:

```bash
python3 scripts/package_plugin.py --root . --out dist/research-skills-plugin.zip
```

## A script option is unclear

Run the script with `--help`. The common commands and write behavior are also documented in [`docs/SCRIPTS.md`](SCRIPTS.md).

## A skill is not being selected automatically

Skill activation depends heavily on the `description` field. If automatic selection misses, name the skill directly:

```text
Use claim-evidence-ledger on this chapter draft.
```

For mixed or unclear accessibility bottlenecks, name the accessibility companion directly:

```text
Use dyslexia-research-companion. I have rough notes, voice fragments, and too much source material. Route this to the smallest low-load first step without changing my meaning.
```

When the bottleneck is narrower, name the smaller skill directly:

```text
Use dictation-to-research-notes. Turn this transcript into claims, evidence needs, ambiguities, and next actions.
```

```text
Use reading-load-reducer. Tell me what to read closely, skim, park, or skip.
```

```text
Use dyslexia-friendly-prose-editor. Fix spelling and sentence boundaries without changing my argument.
```

## Too many skills appear

Install only the core set as direct skills, or use the plugin and name the specific skill you want.

If the problem is too much text rather than unclear scholarship, start with the smallest accessibility skill before asking for a route or audit.

## The agent invents citations

Use `citation-integrity-auditor` and require unverified citation details to stay marked as unverified instead of being filled from memory.

## The prose becomes generic

Use `scholarly-prose-editor` in style-preserving mode and provide a paragraph that represents the voice you want.

## Rough notes are being overcorrected

Use `dictation-to-research-notes` when transcript cleanup is changing the claim, `dyslexia-friendly-prose-editor` when existing prose repair is changing the argument, or `dyslexia-research-companion` when several accessibility bottlenecks are mixed. Require ambiguity to stay visible when spelling, transcription, or repair could change meaning.
