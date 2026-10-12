import json
import tempfile
import time
import unittest
from pathlib import Path

from orchestrator import Orchestrator, Permissions, TransientError


def make(tools, perms, **kw):
    d = Path(tempfile.mkdtemp())
    return Orchestrator(tools, perms, d / "audit.jsonl", d / "state.json", **kw), d


class OrchTests(unittest.TestCase):
    def test_retry_only_transient_then_succeed(self):
        calls = {"n": 0}

        def flaky():
            calls["n"] += 1
            if calls["n"] < 3:
                raise TransientError("net")
            return "ok"
        o, _ = make({"flaky": flaky}, Permissions({"flaky"}))
        r = o.run([{"id": "s1", "tool": "flaky"}], lambda s: "s1" in s["done"])
        self.assertEqual(r["status"], "COMPLETE"); self.assertEqual(calls["n"], 3)

    def test_retries_are_bounded(self):
        def always():
            raise TransientError("down")
        o, _ = make({"t": always}, Permissions({"t"}), max_retries=1)
        r = o.run([{"id": "s1", "tool": "t"}], lambda s: True)
        self.assertEqual(r["status"], "ESCALATE")

    def test_non_transient_error_is_not_retried(self):
        n = {"c": 0}

        def bug():
            n["c"] += 1
            raise ValueError("logic bug")
        o, _ = make({"b": bug}, Permissions({"b"}))
        with self.assertRaises(ValueError):
            o.run([{"id": "s", "tool": "b"}], lambda s: True)
        self.assertEqual(n["c"], 1)

    def test_permission_denied_outside_scope(self):
        o, _ = make({"write": lambda path, text: None}, Permissions({"write"}, ["src/"]))
        r = o.run([{"id": "w", "tool": "write", "args": {"path": "/etc/passwd", "text": "x"}}], lambda s: True)
        self.assertEqual(r["status"], "DENIED")

    def test_human_required_tool_escalates(self):
        o, _ = make({"deploy_prod": lambda: 1}, Permissions({"deploy_prod"}, needs_human={"deploy_prod"}))
        self.assertEqual(o.run([{"id": "d", "tool": "deploy_prod"}], lambda s: True)["status"], "ESCALATE")

    def test_timeout_escalates(self):
        o, _ = make({"slow": lambda: time.sleep(1)}, Permissions({"slow"}), timeout_s=0.1)
        self.assertEqual(o.run([{"id": "x", "tool": "slow"}], lambda s: True)["status"], "ESCALATE")

    def test_checkpoint_resume_skips_done_steps(self):
        n = {"a": 0}

        def a():
            n["a"] += 1
            return 1
        o, d = make({"a": a, "b": lambda: 2}, Permissions({"a", "b"}))
        o.run([{"id": "1", "tool": "a"}], lambda s: True)
        o2 = Orchestrator({"a": a, "b": lambda: 2}, Permissions({"a", "b"}), d / "audit.jsonl", d / "state.json",
                          state=Orchestrator.resume_state(d / "state.json"))
        o2.run([{"id": "1", "tool": "a"}, {"id": "2", "tool": "b"}], lambda s: len(s["done"]) == 2)
        self.assertEqual(n["a"], 1)

    def test_audit_log_written(self):
        o, d = make({"t": lambda: 1}, Permissions({"t"}))
        o.run([{"id": "s", "tool": "t"}], lambda s: True)
        rows = [json.loads(l) for l in (d / "audit.jsonl").read_text().splitlines()]
        self.assertEqual(rows[0]["status"], "ok")


if __name__ == "__main__":
    unittest.main()
