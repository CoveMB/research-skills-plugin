# Installation guide

This package is a Codex-compatible plugin plus a portable Agent Skills folder collection.

## Option A: Install as a Codex local plugin

### macOS / Linux

```bash
unzip scholarly-research-book-plugin-v1.0.0.zip
cd scholarly-research-book-plugin
python3 scripts/install_codex_plugin.py
```

### Windows PowerShell

```powershell
Expand-Archive scholarly-research-book-plugin-v1.0.0.zip
cd scholarly-research-book-plugin
py scripts\install_codex_plugin.py
```

The installer does this:

1. validates `.codex-plugin/plugin.json`,
2. validates every `skills/*/SKILL.md`,
3. copies the plugin to `~/.codex/plugins/scholarly-research-book`,
4. creates or updates `~/.agents/plugins/marketplace.json`,
5. adds a marketplace entry for this plugin.

Restart Codex after installation.

## Option B: Manual Codex personal marketplace install

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

4. Restart Codex and look for the plugin in the plugin directory.

## Option C: Direct local skill install

Some agent environments read skills directly from a skills folder. Copy the folders under `skills/` into the environment's skill directory.

For Codex direct user skills, a common target is:

```text
~/.agents/skills
```

Example:

```bash
mkdir -p ~/.agents/skills
cp -R skills/* ~/.agents/skills/
```

## Option D: ChatGPT Skills upload

ChatGPT Skills upload expects skill bundles from the Skills interface. This package is mainly a multi-skill plugin. If your ChatGPT workspace requires one skill per upload, zip an individual folder under `skills/<skill-name>/` and upload that zip. See `docs/SKILL_INDEX.md` to choose the core skills first.

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
