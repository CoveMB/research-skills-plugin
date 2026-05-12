# Troubleshooting

## The plugin does not appear

- Restart the app.
- Run `python3 scripts/validate_plugin.py .` from the plugin root.
- Check that `.codex-plugin/plugin.json` exists.
- Check that the marketplace file contains a `scholarly-research-book` entry.
- Check that the plugin folder was copied to `~/.codex/plugins/scholarly-research-book`.

## A skill is not being selected automatically

Skill activation depends heavily on the `description` field. If automatic selection misses, name the skill directly:

```text
Use claim-evidence-ledger on this chapter draft.
```

## Too many skills appear

Install only the core set as direct skills, or use the plugin and name the specific skill you want.

## The agent invents citations

Use `citation-integrity-auditor` and require unverified citation details to stay marked as unverified instead of being filled from memory.

## The prose becomes generic

Use `scholarly-prose-editor` in style-preserving mode and provide a paragraph that represents the voice you want.
