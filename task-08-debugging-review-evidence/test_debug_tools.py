import unittest
from debug_tools import (EvidenceReport, HERE, classify_failure, hypothesis_from_shape,
                         inspect_data_shape, revision_hash, run_tests)

BASE, FIXED = HERE / "app" / "base", HERE / "app" / "fixed"


class DebugToolsTests(unittest.TestCase):
    def test_bug_reproduces_on_base(self):
        r = run_tests(BASE)
        self.assertNotEqual(r["rc"], 0)
        self.assertTrue(any("done_label" in f for f in r["failed"]))

    def test_fix_passes_all_cases(self):
        self.assertEqual(run_tests(FIXED)["rc"], 0)

    def test_regression_check_separates_old_and_new_failures(self):
        self.assertIn("no failures", classify_failure(run_tests(BASE), run_tests(FIXED)))
        fake_new = {"failed": ["test_a", "test_b"]}
        fake_base = {"failed": ["test_a"]}
        msg = classify_failure(fake_base, fake_new)
        self.assertIn("REGRESSION", msg); self.assertIn("PRE-EXISTING", msg)

    def test_data_shape_and_hypothesis(self):
        shape = inspect_data_shape([{"status": "done"}, {"status": "open"}, {"status": "done"}])
        self.assertEqual(shape, {"done": 2, "open": 1})
        self.assertIn("case mismatch", hypothesis_from_shape(shape, ["Done", "Open"]))
        self.assertIn("do not guess", hypothesis_from_shape({"done": 1}, ["done"]))

    def test_revision_hash_differs(self):
        self.assertNotEqual(revision_hash(BASE), revision_hash(FIXED))

    def test_report_has_all_template_fields(self):
        txt = EvidenceReport("c", "r", ["x"], "ok", [], [], "review").render()
        for f in ["Change:", "Revision tested:", "Checks run:", "Results:", "Checks not run:",
                  "Known limitations:", "Next required action:"]:
            self.assertIn(f, txt)


if __name__ == "__main__":
    unittest.main()
