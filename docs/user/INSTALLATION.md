# Installation guide

For Codex, install the full plugin from its public Git marketplace when possible. This keeps the router, orchestrator, shared policies, contracts, and specialist skills on one versioned update path. OpenCode v2 and Antigravity use the generated full-catalog export below. Generated standalone bundles remain available for environments that accept only individual skills.

## Requirements

- A Codex release that provides `codex plugin` and `codex plugin marketplace` commands.
- Git access to `https://github.com/CoveMB/research-skills-plugin.git`.

The Git marketplace installation does not require Python. Python 3.10 or newer is required only for repository validation, packaging, standalone bundle generation, and Python helpers used by some skills. An instruction-only generated bundle does not require Python during ordinary use. No pip packages are required; repository maintenance scripts use the Python standard library.

## Install from the Git marketplace

Add the repository as a marketplace source:

```bash
codex plugin marketplace add https://github.com/CoveMB/research-skills-plugin.git --ref main
```

Install the plugin from the marketplace:

```bash
codex plugin add research-skills-plugin@covemb-research-skills
```

Confirm the installation:

```bash
codex plugin list --json
```

The installed entry should report:

- plugin name `research-skills-plugin`
- marketplace name `covemb-research-skills`
- the version declared in `.codex-plugin/plugin.json`

Restart Codex or start a new task after installation. Existing tasks may retain the skill inventory that was loaded when the task began.

The marketplace catalog follows `main`, but each released plugin entry points to an immutable `v<version>` Git tag. Adding the marketplace does not install an unpublished branch or an untagged working tree.

## Update

Refresh the Git marketplace snapshot:

```bash
codex plugin marketplace upgrade covemb-research-skills
```

Reinstall the plugin from the refreshed marketplace:

```bash
codex plugin add research-skills-plugin@covemb-research-skills
```

Verify the installed version:

```bash
codex plugin list --json
```

Start a new task after the reinstall so Codex loads the updated skills.

## OpenCode v2 and Antigravity full catalog

From the source checkout, build with Python 3.10 or newer:

```bash
python3 scripts/package_plugin.py --portable
```

The output is `dist/portable-plugin/research-skills-plugin-v1.1.0-portable.zip`. Choose a new `--out /absolute/path/candidate.zip` if that output already exists. Portable builds refuse existing outputs, symlinked destinations, and destinations inside source areas other than `dist/`. They never replace a previous candidate. Build from canonical source; an extracted portable export cannot be used to generate another portable export.

Extract into a new directory you choose; do not extract over an existing installation. Replace the two absolute paths below with your archive and fresh destination:

```bash
python3 -m zipfile -e /absolute/path/candidate.zip /absolute/path/new-installation
python3 /absolute/path/new-installation/research-skills-plugin/scripts/portable_plugin.py --check /absolute/path/new-installation/research-skills-plugin
python3 /absolute/path/new-installation/research-skills-plugin/scripts/run_package_checks.py --scope package
```

Keep the entire extracted `research-skills-plugin` directory together. It contains all 29 skills and their shared policies, schemas, references, templates, and Python helpers. The standalone catalog still has 28 eligible bundles: 27 `self-sufficient` skills and a `route-only` router; the `full-plugin-only` orchestrator is available in this complete export.

### OpenCode v2

Add the absolute extracted skills directory to the `skills` array in your existing `opencode.json` or `opencode.jsonc`, preserving its other entries and settings:

```json
{
  "skills": ["/absolute/path/new-installation/research-skills-plugin/skills"]
}
```

OpenCode v2 combines configured arrays; relative paths resolve from the active working directory. Later sources win when skill IDs collide, so avoid registering both a standalone and full-catalog copy of the same skill. Start a fresh session and check the discovered inventory. Invoke `@research-intent-router` or `@research-book-orchestrator` explicitly. These are v2 instructions; do not substitute the v1 `skills.paths` configuration. See the [OpenCode v2 skill documentation](https://opencode.ai/v2/docs/skills/).

### Antigravity

The generated manifest is `.antigravity-plugin/plugin.json`, with components at the extracted plugin root. Direct installation of this unbuilt Git repository is unsupported: build and extract first.

With an already installed Antigravity CLI, you can validate and install that local directory yourself:

```bash
agy plugin validate --strict /absolute/path/new-installation/research-skills-plugin
agy plugin install /absolute/path/new-installation/research-skills-plugin
agy plugin list --json
```

The interactive CLI also supports `/plugin install <local-path>`. For App or standalone IDE manual loading, place the complete plugin directory in a fresh workspace `.agents/plugins/` location or a fresh `~/.gemini/config/plugins/` location; inspect existing installations first. App plugins are managed under Customizations → Installed. Invoke `/research-intent-router` or `/research-book-orchestrator` in a new session and check that all 29 skills are available. See the [native plugin guide](https://antigravity.google/docs/plugins/) and [manifest/validation guide](https://antigravity.google/docs/build-plugins/).

For individual bundles only, App/IDE global skills use `~/.gemini/config/skills`, while CLI global skills use `~/.gemini/antigravity-cli/skills`. These are separate from the full-plugin installation above. See [skills by surface](https://antigravity.google/docs/skills/).

### Permissions, updates, and evidence

Host instructions were checked against official documentation on 2026-10-30. Native OpenCode/Antigravity discovery and invocation remain unverified. Package validation is deterministic structural evidence; historical Codex captures do not certify the transformed runtime. The candidate keeps version `1.1.0` and does not create a release or update a marketplace tag.

The host must provide file access and, when needed, Python execution or consented lookup. Missing tools or denied permissions are blockers, not verification. The preserved `agents/openai.yaml` research fields are not claimed to be permissions enforced by other hosts. Resolve bundled helper paths to absolute paths while keeping the user's workspace as the working directory, so user input/output paths keep their meaning. Do not bypass host permission prompts.

For updates, build and validate a fresh candidate and extract into a new directory before changing host registration or replacing a live installation. Keep the previous candidate for rollback, avoid duplicate IDs, and check the inventory in a fresh session after switching. Edit canonical sources and rebuild; do not maintain generated instructions separately.

## Generated local skill install

Some agent environments read individual skills from a skills directory. Build one dependency-closed bundle from the repository root:

```bash
python3 scripts/build_standalone_skill.py --skill <skill-name>
python3 scripts/validate_standalone_skill.py dist/standalone-skills/<skill-name>
```

The builder writes a generated directory and a generated zip to `dist/standalone-skills`. Install the generated directory, not the canonical folder under `skills/`.

A common target for direct user skills is:

```text
~/.agents/skills
```

Example:

```bash
mkdir -p ~/.agents/skills
cp -R dist/standalone-skills/<skill-name> ~/.agents/skills/
```

## Generated skill upload

Some skill-upload interfaces expect one bundle at a time. Build and validate the generated zip before upload:

```bash
python3 scripts/build_standalone_skill.py --skill <skill-name>
python3 scripts/validate_standalone_skill.py dist/standalone-skills/<skill-name>.zip
```

Upload `dist/standalone-skills/<skill-name>.zip`. See [`SKILL_INDEX.md`](SKILL_INDEX.md) when choosing a specialist.

## Build the complete eligible catalog

```bash
python3 scripts/build_standalone_skill.py --all
python3 scripts/validate_standalone_skill.py dist/standalone-skills --registry shared/standalone-skill-registry.json --require-catalog-complete
```

The registry classifies each source skill before generation:

- `self-sufficient` skills can execute from their generated bundle.
- `route-only` bundles can recommend a specialist but cannot claim that an absent specialist ran.
- `full-plugin-only` skills require the complete plugin. The builder rejects them without replacing existing output.

Rebuild a generated bundle whenever its source skill, shared policy, contract, or helper changes. Replace the older generated directory with the new directory of the same skill name.

## Validate a source checkout

Run the marketplace and plugin checks before creating a release:

```bash
python3 scripts/check_marketplace.py --root .
python3 scripts/validate_plugin.py .
./validate.sh
```

For a packaged or installed plugin copy without repository-only test fixtures, run:

```bash
python3 scripts/run_package_checks.py --scope package
```

See [`../reference/SCRIPTS.md`](../reference/SCRIPTS.md) for the full script list.

## Uninstall

Remove the installed plugin:

```bash
codex plugin remove research-skills-plugin@covemb-research-skills
```

Remove the marketplace only when no installed plugin still depends on it:

```bash
codex plugin marketplace remove covemb-research-skills
```

Restart Codex or start a new task after removal.
