# Installation guide

This package can be installed as a local plugin or used as a portable collection of skill folders.

## Option A: Install as a local plugin

### macOS / Linux

```bash
cd scholarly-research-book-plugin
python3 scripts/install_codex_plugin.py
```

### Windows PowerShell

```powershell
cd scholarly-research-book-plugin
py scripts\install_codex_plugin.py
```

The installer:

1. validates `.codex-plugin/plugin.json`,
2. validates every `skills/*/SKILL.md`,
3. copies the plugin to `~/.codex/plugins/scholarly-research-book`,
4. creates or updates `~/.agents/plugins/marketplace.json`,
5. adds the marketplace entry for this plugin.

Restart the app after installation.

## Option B: Manual personal marketplace install

1. Copy this folder to:

```text
~/.codex/plugins/scholarly-research-book
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
      "name": "scholarly-research-book",
      "source": {
        "source": "local",
        "path": "./.codex/plugins/scholarly-research-book"
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

## Option C: Direct local skill install

Some agent environments read skills directly from a skills folder. Copy the folders under `skills/` into that environment's skill directory.

A common target for direct user skills is:

```text
~/.agents/skills
```

Example:

```bash
mkdir -p ~/.agents/skills
cp -R skills/* ~/.agents/skills/
```

## Option D: ChatGPT Skills upload

Some skill-upload interfaces expect one skill bundle at a time. This package is mainly a multi-skill plugin. If your workspace requires one skill per upload, zip an individual folder under `skills/<skill-name>/` and upload that zip. See `docs/SKILL_INDEX.md` to choose the core skills first.

## Validate after install

```bash
python3 scripts/validate_plugin.py .
python3 scripts/check_book_artifact_contract.py --path .
```

For a full local package check, run:

```bash
./validate.sh
```

## Uninstall

Remove the copied plugin folder:

```bash
rm -rf ~/.codex/plugins/scholarly-research-book
```

Then remove the `scholarly-research-book` entry from `~/.agents/plugins/marketplace.json`.
