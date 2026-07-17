# Installation guide

Install the full plugin when possible. It keeps the router, orchestrator, shared policies, contracts, and specialist skills on one update path. If an environment accepts only individual skills, use the generated standalone bundles described below.

## Requirements

Python 3.10 or newer is required to install or validate the plugin, build or validate standalone bundles, package the plugin, and run any Python helper included in a generated bundle. An instruction-only generated bundle does not require Python during ordinary use. No pip packages are required; all maintenance scripts and bundled helpers use the Python standard library.

- macOS and Linux installs use Bash through `./install.sh`.
- Windows installs use PowerShell through `.\install.ps1`.
- A local plugin install needs write access to the plugin destination and marketplace JSON.

## Option A: Install as a local plugin

### macOS / Linux

```bash
cd path/to/unzipped-or-cloned-plugin-folder
./install.sh
```

### Windows PowerShell

```powershell
cd path/to/unzipped-or-cloned-plugin-folder
.\install.ps1
```

The installed plugin and marketplace entry are named `research-skills-plugin`; the source checkout or unzipped folder may have a different name.

The installer:

1. validates `.codex-plugin/plugin.json`,
2. validates every `skills/*/SKILL.md`,
3. validates the book artifact schema and shipped artifact examples,
4. copies the plugin to `~/.codex/plugins/research-skills-plugin`,
5. creates or updates `~/.agents/plugins/marketplace.json`,
6. adds the marketplace entry for this plugin.

Restart the app after installation.

Preview the install first if you want to check paths before writing files:

```bash
./install.sh --dry-run
```

More script details are in [`docs/reference/SCRIPTS.md`](../reference/SCRIPTS.md).

## Option B: Manual personal marketplace install

1. Copy this folder to:

```text
~/.codex/plugins/research-skills-plugin
```

2. Create or update:

```text
~/.agents/plugins/marketplace.json
```

3. Add an entry like:

```json
{
  "name": "local-personal-plugins",
  "interface": {
    "displayName": "Local Personal Plugins"
  },
  "plugins": [
    {
      "name": "research-skills-plugin",
      "source": {
        "source": "local",
        "path": "./.codex/plugins/research-skills-plugin"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

4. Restart the app and look for the plugin in the plugin directory.

## Option C: Generated local skill install

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

## Option D: Generated skill upload

Some skill-upload interfaces expect one bundle at a time. Build and validate the generated zip before upload:

```bash
python3 scripts/build_standalone_skill.py --skill <skill-name>
python3 scripts/validate_standalone_skill.py dist/standalone-skills/<skill-name>.zip
```

Upload `dist/standalone-skills/<skill-name>.zip`. See [`docs/user/SKILL_INDEX.md`](SKILL_INDEX.md) when choosing a specialist.

## Build the complete eligible catalog

```bash
python3 scripts/build_standalone_skill.py --all
python3 scripts/validate_standalone_skill.py dist/standalone-skills --registry shared/standalone-skill-registry.json --require-catalog-complete
```

The registry classifies each source skill before generation:

- `self-sufficient` skills can execute from their generated bundle.
- `route-only` means the bundle can recommend a specialist but cannot claim that an absent specialist ran.
- `full-plugin-only` skills require the complete plugin. The builder rejects them without replacing existing output.

## Migrate an older raw-folder install

If you previously copied `skills/<skill-name>` directly, build that skill, validate it, and replace the old folder with the generated directory of the same skill name. Keep the destination name unchanged so existing skill references continue to resolve. Rebuild from the canonical source whenever the source skill, a shared policy, a contract, or a helper changes.

## Validate after install

```bash
python3 scripts/validate_plugin.py .
python3 scripts/check_book_artifact_contract.py --path .
```

For a packaged or installed copy without repo-only test fixtures, run:

```bash
python3 scripts/run_package_checks.py --scope package
```

For a full source-checkout validation, run from the repository root:

```bash
./validate.sh
```

See [`docs/reference/SCRIPTS.md`](../reference/SCRIPTS.md) for the full script list and dependency notes.

## Uninstall

Remove the copied plugin folder:

```bash
rm -rf ~/.codex/plugins/research-skills-plugin
```

Then remove the `research-skills-plugin` entry from `~/.agents/plugins/marketplace.json`.
