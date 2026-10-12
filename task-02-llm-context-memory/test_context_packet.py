import unittest
from pathlib import Path

from context_packet import ContextPacket, prepare, scan_secrets, select_relevant_files

REPO = Path(__file__).parent / "sample_repo"


def full():
    return ContextPacket("add status filter", ["task_list.py"], "shows all", "selected status only",
                         "no refactor", "All/Open/Done")


class ContextTests(unittest.TestCase):
    def test_complete_packet_ok(self):
        self.assertTrue(prepare(full())["ok"])

    def test_missing_fields_reported(self):
        p = full(); p.acceptance = ""
        r = prepare(p)
        self.assertFalse(r["ok"]); self.assertIn("acceptance", r["problems"][0])

    def test_secret_blocks_packet(self):
        p = full(); p.current = "key is sk-demo-FAKEKEY0123456789abcdef"
        self.assertFalse(prepare(p)["ok"])

    def test_scan_secrets_variants(self):
        self.assertIn("password assignment", scan_secrets('password = "hunter2!"'))
        self.assertEqual(scan_secrets("plain text"), [])

    def test_selection_prefers_relevant_and_skips_secret_files(self):
        chosen = select_relevant_files(REPO, ["task", "filter", "status"])
        self.assertIn("task_list.py", chosen)
        self.assertIn("AGENTS.md", chosen)
        self.assertNotIn("auth.py", chosen)       # contains a secret
        self.assertNotIn("billing.py", chosen)    # irrelevant

    def test_budget_is_respected(self):
        chosen = select_relevant_files(REPO, ["task"], budget_tokens=30)
        self.assertLessEqual(sum(chosen.values()), 30)


if __name__ == "__main__":
    unittest.main()
