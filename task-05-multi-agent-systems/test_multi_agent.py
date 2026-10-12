import unittest
from multi_agent import (Contract, Node, find_conflicts, levels, run_graph, should_delegate,
                         task_tracker_graph)


def quiet(_): pass


class MultiAgentTests(unittest.TestCase):
    def test_levels_parallel_impl_and_test_then_review(self):
        self.assertEqual(levels(task_tracker_graph()),
                         [["coordinate"], ["implement", "test"], ["review"]])

    def test_review_runs_after_implementation(self):
        res = run_graph(task_tracker_graph(), quiet)
        self.assertIn("status predicate", res["review"]["notes"])

    def test_same_file_conflict_detected_and_serialised(self):
        g = task_tracker_graph()
        g["test"].contract.allowed_files = ["tracker.py", "test_tracker.py"]  # overlaps implementer
        self.assertTrue(find_conflicts(g, ["implement", "test"]))
        logs = []
        run_graph({k: g[k] for k in g}, logs.append)
        self.assertTrue(any("conflict" in l for l in logs))

    def test_agent_outside_contract_is_rejected(self):
        g = task_tracker_graph()
        g["implement"].agent = lambda c, r: {"touched": ["tracker.py", "billing.py"]}
        with self.assertRaises(PermissionError):
            run_graph(g, quiet)

    def test_incomplete_contract_rejected(self):
        g = task_tracker_graph()
        g["test"].contract.stop = ""
        with self.assertRaises(ValueError):
            run_graph(g, quiet)

    def test_cycle_detected(self):
        g = task_tracker_graph()
        g["coordinate"].depends_on = ["review"]
        with self.assertRaises(ValueError):
            levels(g)

    def test_delegation_table(self):
        self.assertIn("ONE AGENT", should_delegate(1, False, False))
        self.assertIn("SEQUENTIAL", should_delegate(4, True, True))
        self.assertIn("DELEGATE", should_delegate(4, True, False))


if __name__ == "__main__":
    unittest.main()
