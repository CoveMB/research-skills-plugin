# Installation guide

Install the full plugin from its public Git marketplace when possible. This keeps the router, orchestrator, shared policies, contracts, and specialist skills on one versioned update path. Generated standalone bundles remain available for environments that accept only individual skills.

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
