import unittest
from tasklist import filter_tasks

TASKS = [{"id": 1, "status": "open"}, {"id": 2, "status": "done"}]


class FilterTests(unittest.TestCase):
    def test_done_only(self):
        self.assertEqual([t["id"] for t in filter_tasks(TASKS, "Done")], [2])

    def test_all(self):
        self.assertEqual(len(filter_tasks(TASKS)), 2)


if __name__ == "__main__":
    unittest.main()
