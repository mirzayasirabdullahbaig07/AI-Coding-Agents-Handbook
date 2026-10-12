import unittest
from prompt_kit import BETTER, DAILY, STRONG, TEMPLATES, WEAK, PromptSpec, grade, lint_response_request


class PromptTests(unittest.TestCase):
    def test_levels_ordering(self):
        w, b, s = grade(WEAK), grade(BETTER), grade(STRONG)
        self.assertLess(w["score"], b["score"]); self.assertLess(b["score"], s["score"])
        self.assertEqual((w["level"], b["level"], s["level"]), ("Weak", "Better", "Strong"))

    def test_strong_has_all_sections(self):
        self.assertEqual(grade(STRONG)["missing"], [])

    def test_weak_lists_missing_sections(self):
        self.assertIn("acceptance", grade(WEAK)["missing"])

    def test_render_contains_every_section(self):
        txt = PromptSpec("g", "c", "s", "k", "a", "v", "r").render()
        for label in ["Goal:", "Context:", "Scope:", "Constraints:", "Acceptance criteria:", "Verification:", "Required response:"]:
            self.assertIn(label, txt)

    def test_templates_forbid_edits_when_read_only(self):
        self.assertIn("Do not modify", TEMPLATES["explain"])
        self.assertIn("without modifying", TEMPLATES["review_diff"])

    def test_daily_template_fills(self):
        self.assertIn("Goal: add filter", DAILY.format(task="add filter", context="c", scope="s", acceptance="a"))

    def test_chain_of_thought_request_flagged(self):
        self.assertTrue(lint_response_request("show your hidden chain-of-thought"))
        self.assertFalse(lint_response_request("give a concise rationale and verification steps"))


if __name__ == "__main__":
    unittest.main()
