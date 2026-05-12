"""Structure tests for plugin skill routing and naming."""
from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"


def read_text_files() -> list[tuple[Path, str]]:
    files: list[tuple[Path, str]] = []
    for path in sorted(ROOT.rglob("*")):
        if ".git" in path.parts or path.is_dir():
            continue
        if path == Path(__file__).resolve():
            continue
        if path.suffix in {".md", ".json", ".yaml", ".yml", ".sh", ".py"}:
            files.append((path, path.read_text(encoding="utf-8")))
    return files


def frontmatter_name(skill_markdown: str) -> str:
    match = re.search(r"^name:\s*([a-z0-9-]+)\s*$", skill_markdown, re.MULTILINE)
    return match.group(1) if match else ""


class TestPluginStructure(unittest.TestCase):
    def test_research_book_orchestrator_replaces_old_skill_name(self) -> None:
        old_skill_name = "-".join(["scholar" + "ly", "book", "orchestrator"])
        skill_path = SKILLS_DIR / "research-book-orchestrator" / "SKILL.md"
        self.assertTrue(skill_path.is_file())
        self.assertFalse((SKILLS_DIR / old_skill_name).exists())
        self.assertEqual(frontmatter_name(skill_path.read_text(encoding="utf-8")), "research-book-orchestrator")

        stale_references = [
            str(path.relative_to(ROOT))
            for path, text in read_text_files()
            if old_skill_name in text
        ]
        self.assertEqual(stale_references, [])


if __name__ == "__main__":
    unittest.main()
