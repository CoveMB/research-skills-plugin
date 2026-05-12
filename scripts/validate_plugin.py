#!/usr/bin/env python3
"""Validate a Codex/Agent Skills plugin package.

Checks:
- .codex-plugin/plugin.json exists and points to skills
- every skills/<name>/SKILL.md has valid frontmatter
- skill name matches folder name
- required name/description fields are present
- names satisfy Agent Skills naming constraints
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening YAML frontmatter delimiter")
    data: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return data
        if not line.strip() or line.startswith("  "):
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip().strip('"').strip("'")
    raise ValueError("missing closing YAML frontmatter delimiter")


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").expanduser().resolve()
    errors: list[str] = []

    manifest_path = root / ".codex-plugin" / "plugin.json"
    if not manifest_path.exists():
        errors.append("Missing .codex-plugin/plugin.json")
    else:
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            for field in ["name", "version", "description", "skills"]:
                if field not in manifest:
                    errors.append(f"plugin.json missing required/recommended field: {field}")
            if not NAME_RE.match(manifest.get("name", "")):
                errors.append("plugin.json name should be kebab-case lowercase")
        except Exception as exc:
            errors.append(f"plugin.json parse error: {exc}")

    skills_dir = root / "skills"
    if not skills_dir.exists():
        errors.append("Missing skills/ directory")
    else:
        skill_dirs = sorted(p for p in skills_dir.iterdir() if p.is_dir())
        if not skill_dirs:
            errors.append("skills/ directory contains no skill folders")
        seen = set()
        for sd in skill_dirs:
            smd = sd / "SKILL.md"
            if not smd.exists():
                errors.append(f"{sd.name}: missing SKILL.md")
                continue
            try:
                fm = parse_frontmatter(smd)
            except Exception as exc:
                errors.append(f"{sd.name}: frontmatter error: {exc}")
                continue
            name = fm.get("name", "")
            desc = fm.get("description", "")
            if not name:
                errors.append(f"{sd.name}: missing name")
            if not desc:
                errors.append(f"{sd.name}: missing description")
            if len(desc) > 1024:
                errors.append(f"{sd.name}: description exceeds 1024 characters")
            if name != sd.name:
                errors.append(f"{sd.name}: frontmatter name '{name}' does not match folder")
            if not NAME_RE.match(name):
                errors.append(f"{sd.name}: invalid skill name '{name}'")
            if name in seen:
                errors.append(f"duplicate skill name: {name}")
            seen.add(name)

    if errors:
        print("Validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1
    print(f"Validation passed: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
