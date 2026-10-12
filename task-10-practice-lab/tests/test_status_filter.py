import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "baseline"))

from task_tracker import filter_tasks, list_tasks, load_tasks  # noqa: E402
import tracker_before  # noqa: E402

TASKS = load_tasks()
ids = lambda rows: [t["id"] for t in rows]


class AcceptanceCriteria(unittest.TestCase):
    """All / Open / Done behave as specified."""

    def test_all_returns_every_task(self):
        self.assertEqual(ids(filter_tasks(TASKS, "all")), [1, 2, 3, 4, 5, 6])

    def test_open_returns_open_tasks_any_case(self):
        self.assertEqual(ids(filter_tasks(TASKS, "open")), [1, 3, 5])

    def test_done_returns_done_tasks_any_case(self):
        self.assertEqual(ids(filter_tasks(TASKS, "done")), [2, 4, 6])

    def test_ui_labels_with_capital_letters_work(self):
        self.assertEqual(ids(filter_tasks(TASKS, "Done")), [2, 4, 6])
        self.assertEqual(ids(filter_tasks(TASKS, " OPEN ")), [1, 3, 5])


class NegativeTests(unittest.TestCase):
    def test_done_filter_never_contains_open(self):
        for t in filter_tasks(TASKS, "Done"):
            self.assertEqual(t["status"].lower(), "done")

    def test_open_filter_never_contains_done(self):
        for t in filter_tasks(TASKS, "open"):
            self.assertNotEqual(t["status"].lower(), "done")

    def test_unknown_status_is_rejected_not_silently_empty(self):
        with self.assertRaises(ValueError):
            filter_tasks(TASKS, "archived")

    def test_open_and_done_partition_all(self):
        self.assertEqual(sorted(ids(filter_tasks(TASKS, "open")) + ids(filter_tasks(TASKS, "done"))),
                         sorted(ids(TASKS)))


class PreservedBehaviour(unittest.TestCase):
    """Existing behaviour must not change."""

    def test_default_list_equals_baseline(self):
        self.assertEqual(list_tasks(TASKS), tracker_before.list_tasks(TASKS))

    def test_order_preserved(self):
        self.assertEqual(ids(filter_tasks(TASKS)), ids(TASKS))

    def test_input_not_mutated(self):
        before = json.dumps(TASKS)
        filter_tasks(TASKS, "done")
        self.assertEqual(json.dumps(TASKS), before)

    def test_empty_list(self):
        self.assertEqual(filter_tasks([], "done"), [])


if __name__ == "__main__":
    unittest.main()
