import unittest
from pathlib import Path

from agent_loop import Action, Policy, ScriptedModel, run_loop

WS = Path(__file__).parent / "workspace"


class LoopTests(unittest.TestCase):
    def setUp(self):
        self.log = run_loop(ScriptedModel(), WS)
        self.text = "\n".join(f"{s.phase}: {s.text}" for s in self.log)

    def test_dangerous_shell_is_blocked_not_executed(self):
        self.assertIn("BLOCKED: tool 'shell' is not authorised", self.text)

    def test_first_attempt_fails_then_adjusts_then_passes(self):
        observes = [s.text for s in self.log if s.phase == "OBSERVE" and s.text.startswith("rc=")]
        self.assertTrue(observes[0].startswith("rc=1"))
        self.assertTrue(observes[-1].startswith("rc=0"))

    def test_ends_with_verify_and_handoff(self):
        self.assertEqual([s.phase for s in self.log][-2:], ["VERIFY", "HANDOFF"])

    def test_policy_scope(self):
        p = Policy()
        self.assertIsNone(p.check(Action("edit_file", {"path": "tracker.py"})))
        self.assertIsNotNone(p.check(Action("edit_file", {"path": "test_tracker.py"})))

    def test_repeating_same_failing_action_escalates(self):
        class Stuck:
            def propose(self, h):
                return Action("run_tests")
        log = run_loop(Stuck(), WS)
        self.assertEqual(log[-1].phase, "ESCALATE")

    def test_original_workspace_untouched(self):
        self.assertIn('t["status"] == status', (WS / "tracker.py").read_text())


if __name__ == "__main__":
    unittest.main()
