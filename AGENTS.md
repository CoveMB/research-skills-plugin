# AGENTS.md

This repository is a Codex-compatible plugin package. When modifying it:

- Keep `.codex-plugin/plugin.json` valid JSON.
- Keep every skill folder name equal to its `SKILL.md` frontmatter `name`.
- Keep skill names lowercase kebab-case.
- Keep descriptions specific enough for implicit invocation.
- Run `python3 scripts/validate_plugin.py .` before packaging.
- Do not add fabricated citations, example sources, page numbers, or bibliographic claims to skill instructions.
