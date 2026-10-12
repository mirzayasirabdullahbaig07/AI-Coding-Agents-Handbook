import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from repo_workflow import (State, create_branch, git, inspect_diff, make_handoff, preflight, run_checks)


def new_repo() -> Path:
    d = Path(tempfile.mkdtemp())
    git(d, "init", "-q", "-b", "main")
    git(d, "config", "user.email", "t@example.com"); git(d, "config", "user.name", "t")
    (d / ".gitignore").write_text("__pycache__/\n")
    (d / "AGENTS.md").write_text("rules\n")
    (d / "tracker.py").write_text("x = 1\n")
    (d / "test_t.py").write_text("import unittest\nclass T(unittest.TestCase):\n    def test(self): self.assertTrue(True)\n")
    git(d, "add", "."); git(d, "commit", "-qm", "init")
    return d


class WorkflowTests(unittest.TestCase):
    def test_preflight_sees_instructions_and_foreign_changes(self):
        d = new_repo()
        (d / "notes.txt").write_text("someone else's wip")
        pf = preflight(d)
        self.assertEqual(pf.instructions, ["AGENTS.md"]); self.assertFalse(pf.clean)
        self.assertEqual(pf.uncommitted, ["notes.txt"])

    def test_branching_refused_when_dirty(self):
        d = new_repo(); (d / "tracker.py").write_text("x = 2\n")
        with self.assertRaises(RuntimeError):
            create_branch(d, "feature/filter")

    def test_diff_scope_detection(self):
        d = new_repo(); create_branch(d, "feature/f")
        (d / "tracker.py").write_text("x = 2\n"); (d / "billing.py").write_text("sneaky = 1\n")
        git(d, "add", "-A")
        git(d, "commit", "-qm", "wip")
        rep2 = inspect_diff(d, "main", ["tracker.py"])
        self.assertEqual(rep2.out_of_scope, ["billing.py"]); self.assertFalse(rep2.bounded)

    def test_handoff_requires_clean_tree(self):
        d = new_repo(); (d / "tracker.py").write_text("x = 3\n")
        with self.assertRaises(RuntimeError):
            make_handoff(d, [], [])

    def test_handoff_states_only_what_is_evidenced(self):
        d = new_repo()
        checks = run_checks(d, [[sys.executable, "-m", "unittest", "-q"]])
        h = make_handoff(d, checks, ["hosted CI (not available locally)"])
        self.assertEqual(h.states, [State.LOCAL_TESTS_PASS])
        self.assertIn("NOT evidenced: HOSTED_CI_PASS, MERGED, DEPLOYED", h.render())
        self.assertEqual(h.revision, git(d, "rev-parse", "--short", "HEAD"))

    def test_failing_check_gives_no_pass_state(self):
        d = new_repo()
        checks = run_checks(d, [[sys.executable, "-c", "raise SystemExit(1)"]])
        self.assertEqual(make_handoff(d, checks, []).states, [])


if __name__ == "__main__":
    unittest.main()
