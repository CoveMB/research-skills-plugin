"""Tests for skill evaluation hashing."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parent))
from skill_evaluation_hashes import skill_instruction_sha256


def skill_text(version: str = "1.0.0", *, category: str = "research", body: str = "Do the work.") -> str:
    return (
        "---\n"
        "name: test-skill\n"
        "description: Test skill.\n"
        "metadata:\n"
        f'  version: "{version}"\n'
        f"  category: {category}\n"
        "---\n"
        "\n"
        f"{body}\n"
    )


class TestSkillEvaluationHashes(unittest.TestCase):
    def hash_text(self, text: str) -> str:
        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "SKILL.md"
            path.write_text(text, encoding="utf-8")
            return skill_instruction_sha256(path)

    def test_release_version_does_not_change_instruction_hash(self) -> None:
        self.assertEqual(self.hash_text(skill_text("1.0.0")), self.hash_text(skill_text("1.1.0")))

    def test_instruction_or_other_frontmatter_change_changes_hash(self) -> None:
        original = self.hash_text(skill_text())

        self.assertNotEqual(original, self.hash_text(skill_text(body="Do different work.")))
        self.assertNotEqual(original, self.hash_text(skill_text(category="integrity")))

    def test_version_like_body_line_is_preserved(self) -> None:
        original = self.hash_text(skill_text(body='version: "body-one"'))

        self.assertNotEqual(original, self.hash_text(skill_text(body='version: "body-two"')))

    def test_malformed_or_ambiguous_frontmatter_fails_closed(self) -> None:
        invalid_documents = [
            "No frontmatter.\n",
            "---\nname: test-skill\n",
            "---\nname: test-skill\n---\nBody.\n",
            skill_text().replace('  version: "1.0.0"\n', ""),
            skill_text().replace('  version: "1.0.0"\n', "  version:malformed\n"),
            skill_text().replace('  version: "1.0.0"\n', "  version: [unterminated\n"),
            skill_text().replace('  version: "1.0.0"\n', '  version: "1.0"\n'),
            skill_text().replace('  version: "1.0.0"\n', '  version: "1.0.0"\n  version: "1.1.0"\n'),
        ]

        for document in invalid_documents:
            with self.subTest(document=document), self.assertRaises(ValueError):
                self.hash_text(document)


if __name__ == "__main__":
    unittest.main()
