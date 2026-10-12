"""Positive, negative and regression cases. Target revision chosen with TRACKER_DIR (default: app/fixed)."""
import importlib.util
import os
import unittest
from pathlib import Path

HERE = Path(__file__).parent
target = Path(os.environ.get("TRACKER_DIR", HERE / "app" / "fixed"))
spec = importlib.util.spec_from_file_location("tracker_under_test", target / "tracker.py")
tracker = importlib.util.module_from_spec(spec); spec.loader.exec_module(tracker)

TASKS = [
    {"id": 1, "title": "write docs", "status": "open"},
    {"id": 2, "title": "ship v1", "status": "done"},
    {"id": 3, "title": "fix bug", "status": "Open"},
    {"id": 4, "title": "retro", "status": "DONE"},
]
ids = lambda rows: [t["id"] for t in rows]


class FilterTests(unittest.TestCase):
    # positive
    def test_done_label_matches_stored_lowercase(self):
        self.assertEqual(ids(tracker.filter_tasks(TASKS, "Done")), [2, 4])

    def test_open_returns_open_in_any_case(self):
        self.assertEqual(ids(tracker.filter_tasks(TASKS, "Open")), [1, 3])

    # negative: the bug in the handbook
    def test_done_never_contains_open(self):
        statuses = {t["status"].lower() for t in tracker.filter_tasks(TASKS, "Done")}
        self.assertNotIn("open", statuses)

    # regression: existing behaviour preserved
    def test_all_returns_everything_in_order(self):
        self.assertEqual(ids(tracker.filter_tasks(TASKS)), [1, 2, 3, 4])

    def test_unknown_status_returns_nothing(self):
        self.assertEqual(tracker.filter_tasks(TASKS, "archived"), [])


if __name__ == "__main__":
    unittest.main()
