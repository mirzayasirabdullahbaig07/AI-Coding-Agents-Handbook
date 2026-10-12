import tempfile
import unittest
from pathlib import Path

from evidence import (BLOCKED, FAILED, NOT_EXECUTED, VERIFIED, Claim, Evidence,
                      judge, run_check, revision_of, PYTHON)

HERE = Path(__file__).parent / "sample_project"


class EvidenceTests(unittest.TestCase):
    def test_claim_without_execution_is_not_verified(self):
        self.assertEqual(judge(Claim("I ran the tests")), NOT_EXECUTED)

    def test_passing_command_is_verified(self):
        ev = run_check([PYTHON, "-m", "unittest", "-q"], HERE)
        self.assertEqual(judge(Claim("tests pass", ev)), VERIFIED)

    def test_failing_command_is_failed_not_verified(self):
        ev = run_check([PYTHON, "-c", "import sys; sys.exit(3)"], HERE)
        self.assertEqual(judge(Claim("tests pass", ev)), FAILED)

    def test_missing_binary_is_blocked(self):
        ev = run_check(["definitely-not-a-real-binary"], HERE)
        self.assertEqual(judge(Claim("lint ok", ev)), BLOCKED)

    def test_timeout_is_blocked(self):
        ev = run_check([PYTHON, "-c", "import time; time.sleep(5)"], HERE, timeout=1)
        self.assertEqual(judge(Claim("slow check", ev)), BLOCKED)

    def test_revision_changes_when_code_changes(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "a.py"
            p.write_text("x = 1\n")
            r1 = revision_of(Path(d))
            p.write_text("x = 2\n")
            self.assertNotEqual(r1, revision_of(Path(d)))


if __name__ == "__main__":
    unittest.main()
