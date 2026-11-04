# Troubleshooting

## The plugin does not appear

- Confirm that Codex knows about the marketplace:

```bash
codex plugin marketplace list --json
```

- Confirm that the plugin is installed from `covemb-research-skills`:

```bash
codex plugin list --json
```

- If the marketplace exists but the plugin is missing, run:

```bash
codex plugin marketplace upgrade covemb-research-skills
codex plugin add research-skills-plugin@covemb-research-skills
```

- Restart Codex or start a new task. Existing tasks may retain an older skill inventory.

## The marketplace cannot be added

Check Git access first:

```bash
git ls-remote https://github.com/CoveMB/research-skills-plugin.git
```

If Git cannot reach the public repository, resolve the network, proxy, or Git configuration problem before retrying `codex plugin marketplace add`. Do not put access tokens in the marketplace URL or repository files.

## The installed version is stale

Refresh the marketplace before reinstalling:

```bash
codex plugin marketplace upgrade covemb-research-skills
codex plugin add research-skills-plugin@covemb-research-skills
codex plugin list --json
```

The marketplace upgrade refreshes the catalog. The second command reinstalls the plugin version named by the refreshed catalog.

## Python is missing or too old

Git marketplace installation does not require Python. You need Python only when running repository maintenance scripts, building standalone bundles, or using a bundled Python helper.

The scripts need Python 3.10 or newer. On macOS or Linux, run:

```bash
python3 --version
```

On Windows PowerShell, run:

```powershell
py --version
```

If the command is missing or reports an older version, install a current Python release and make sure the launcher is in `PATH`.

## Package creation fails

Without `--portable`, `scripts/package_plugin.py` writes the zip to the current directory by default. If that directory is read-only, pass `--out` with a writable path:

```bash
python3 scripts/package_plugin.py --root . --out dist/research-skills-plugin.zip
```

Portable output defaults under `dist/portable-plugin/`. If it already exists, choose a new `--out`; do not delete an unrelated output to make the build pass. Symlinked output paths are refused, including parent aliases; use the real directory path. Missing, ambiguous, excluded, or symlinked resource dependencies fail the build. Repair the canonical dependency rather than copying private files into the archive.

## OpenCode v2 or Antigravity cannot find the full catalog

Follow the [full-catalog installation guide](INSTALLATION.md#opencode-v2-and-antigravity-full-catalog). Use the generated export and keep its whole directory intact. OpenCode v2 needs the absolute extracted `skills` path in its additive `skills` array. Antigravity needs the extracted local plugin with its generated manifest; the unbuilt Git repository is not an Antigravity installation artifact.

Validate the extracted tree with its `scripts/portable_plugin.py --check` command and package checks, then inspect the host's inventory in a new session. Look for duplicate IDs from earlier standalone or full installations. Try `@research-intent-router` in OpenCode v2 or `/research-intent-router` in Antigravity. Native discovery and invocation have not yet been verified by this project.

If a helper cannot find a user file, resolve the bundled Python script to an absolute path and run it from the user's workspace. Preserve a filename containing spaces as one quoted argument. Missing Python, unavailable lookup, or denied permissions must be reported as blockers; neither a successful package check nor Codex agent metadata grants access in another host.

## A script option is unclear

Run the script with `--help`. The common commands and write behavior are also documented in [`docs/reference/SCRIPTS.md`](../reference/SCRIPTS.md).

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
