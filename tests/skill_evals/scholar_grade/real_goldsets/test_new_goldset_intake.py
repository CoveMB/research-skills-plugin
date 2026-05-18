"""Tests for real-source gold-set intake scaffolding."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parent))
from new_goldset_intake import create_intake_packet


class NewGoldsetIntakeTests(unittest.TestCase):
    def test_create_intake_packet_copies_templates_without_activating_fixture(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            packet = create_intake_packet(
                goldset_id="urban-dashboard-retrieval",
                title="Urban Dashboard Retrieval",
                output_root=Path(temporary_directory),
            )

            self.assertEqual(packet.name, "urban-dashboard-retrieval")
            self.assertTrue((packet / "goldset_intake.md").exists())
            self.assertTrue((packet / "source_appraisal.md").exists())
            self.assertTrue((packet / "reviewer_checklist.md").exists())

            intake_text = (packet / "goldset_intake.md").read_text(encoding="utf-8")
            self.assertIn("Urban Dashboard Retrieval", intake_text)
            self.assertIn("urban-dashboard-retrieval", intake_text)
            self.assertIn("Activation Decision", intake_text)
            self.assertNotIn("status: active", intake_text.lower())


if __name__ == "__main__":
    unittest.main()
