import unittest
from task_list import TaskList


class TaskListTests(unittest.TestCase):
    def test_visible_returns_all(self):
        self.assertEqual(len(TaskList([1, 2]).visible()), 2)
