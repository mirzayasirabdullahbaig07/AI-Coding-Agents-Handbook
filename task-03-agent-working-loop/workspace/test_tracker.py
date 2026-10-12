import unittest
from tracker import filter_tasks

TASKS = [
    {"id": 1, "title": "write docs", "status": "open"},
    {"id": 2, "title": "ship v1", "status": "done"},
    {"id": 3, "title": "fix bug", "status": "Open"},
]


class FilterTests(unittest.TestCase):
    def test_all(self):
        self.assertEqual(len(filter_tasks(TASKS, "all")), 3)

    def test_done_case_insensitive(self):
        self.assertEqual([t["id"] for t in filter_tasks(TASKS, "Done")], [2])

    def test_open_includes_mixed_case_and_excludes_done(self):
        self.assertEqual([t["id"] for t in filter_tasks(TASKS, "open")], [1, 3])


if __name__ == "__main__":
    unittest.main()
