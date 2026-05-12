# Troubleshooting

## The plugin does not appear in Codex

- Restart Codex.
- Run `python3 scripts/validate_plugin.py .` from the plugin root.
- Check that `.codex-plugin/plugin.json` exists.
- Check that the marketplace file contains a `scholarly-research-book` entry.
- Check that the plugin folder was copied to `~/.codex/plugins/scholarly-research-book`.

## A skill is not being selected automatically

Skill activation depends heavily on the `description` field. Explicitly mention a skill by name, for example:

```text
Use claim-evidence-ledger on this chapter draft.
```

## Too many skills appear

Install only the core set as direct skills, or use the plugin and invoke the specific skill explicitly.

## The agent invents citations

Use `citation-integrity-auditor` and require the agent to mark unverified citation details instead of completing them from memory.

## The prose becomes generic

Use `scholarly-prose-editor` in style-preserving mode and provide a paragraph that represents your desired voice.
