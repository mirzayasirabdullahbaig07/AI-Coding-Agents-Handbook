import contextlib
import io
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from task_tracker.cli import main  # noqa: E402


def run(*argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = main(list(argv))
    return rc, out.getvalue(), err.getvalue()


class CliTests(unittest.TestCase):
    def test_default_lists_all(self):
        rc, out, _ = run("list")
        self.assertEqual(rc, 0); self.assertEqual(out.count("\n"), 2 + 6)

    def test_done_filter(self):
        rc, out, _ = run("list", "--status", "done")
        self.assertIn("Ship v0.1", out); self.assertNotIn("Fix login redirect", out)

    def test_bad_status_exit_code(self):
        rc, _, err = run("list", "--status", "weird")
        self.assertEqual(rc, 2); self.assertIn("unknown status", err)


if __name__ == "__main__":
    unittest.main()
