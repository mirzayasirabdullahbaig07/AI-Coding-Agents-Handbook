"""Task 03 - The agent working loop.

Task -> Inspect -> Propose -> Policy check -> Execute -> Observe -> Adjust -> Verify -> Handoff

IMPORTANT: ScriptedModel is a deterministic stand-in for an LLM so the demo is
reproducible offline. The loop, policy, tools and observations are real: files
really change and tests really run. Swap ScriptedModel for any class with a
`propose(history) -> Action` method to plug in a real LLM.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, List, Optional


@dataclass
class Action:
    tool: str                      # read_file | edit_file | run_tests | shell | finish
    args: Dict = field(default_factory=dict)
    why: str = ""


@dataclass
class Step:
    n: int
    phase: str
    text: str


class Policy:
    """Policy check = the orchestration layer's gate, NOT the model's opinion."""
    ALLOWED_TOOLS = {"read_file", "edit_file", "run_tests", "finish"}
    EDITABLE = {"tracker.py"}      # bounded scope: only this file may change

    def check(self, a: Action) -> Optional[str]:
        if a.tool not in self.ALLOWED_TOOLS:
            return f"tool '{a.tool}' is not authorised"
        if a.tool == "edit_file" and a.args.get("path") not in self.EDITABLE:
            return f"edit outside allowed scope: {a.args.get('path')}"
        return None


class Tools:
    def __init__(self, root: Path):
        self.root = root

    def read_file(self, path: str) -> str:
        return (self.root / path).read_text()

    def edit_file(self, path: str, old: str, new: str) -> str:
        p = self.root / path
        text = p.read_text()
        if old not in text:
            return "ERROR: text to replace not found"
        p.write_text(text.replace(old, new))
        return "edited"

    def run_tests(self) -> str:
        cp = subprocess.run([sys.executable, "-m", "unittest", "-q"], cwd=self.root,
                            capture_output=True, text=True, timeout=60)
        out = (cp.stdout + cp.stderr).strip()
        return f"rc={cp.returncode}\n{out}"


class ScriptedModel:
    """Deterministic 'LLM': proposes the next action from the observation history."""

    def __init__(self):
        self.stage = 0

    def propose(self, history: List[Step]) -> Action:
        last = history[-1].text if history else ""
        if self.stage == 0:
            self.stage = 1
            return Action("read_file", {"path": "tracker.py"}, "inspect the filter")
        if self.stage == 1:
            self.stage = 2
            return Action("shell", {"cmd": "rm -rf ."}, "(bad idea) clean workspace first")
        if self.stage == 2:
            self.stage = 3
            return Action("edit_file", {"path": "tracker.py", "old": 'if status == "all":',
                                        "new": 'status = status.lower()\n    if status == "all":'},
                          "first attempt: lower-case the requested status")
        if self.stage == 3:
            self.stage = 4
            return Action("run_tests", {}, "check focused tests")
        if self.stage == 4:
            self.stage = 5
            return Action("edit_file", {"path": "tracker.py", "old": 't["status"] == status',
                                        "new": 't["status"].lower() == status'},
                          "stored status is mixed case too: normalise both sides")
        if self.stage == 5:
            self.stage = 6
            return Action("run_tests", {}, "re-run after adjustment")
        return Action("finish", {}, "criteria met")


def run_loop(model, workspace: Path, max_steps: int = 12, max_retries_same: int = 1) -> List[Step]:
    tmp = Path(tempfile.mkdtemp())
    root = tmp / "ws"
    shutil.copytree(workspace, root, ignore=shutil.ignore_patterns("__pycache__"))
    tools, policy, log = Tools(root), Policy(), []
    history: List[Step] = []

    def note(phase, text):
        s = Step(len(log) + 1, phase, text)
        log.append(s)
        history.append(s)

    note("TASK", "Done filter shows wrong tasks. Fix with bounded change; verify.")
    last_action, repeats = None, 0
    for _ in range(max_steps):
        action = model.propose(history)
        note("PROPOSE", f"{action.tool} {action.args if action.tool != 'edit_file' else action.args.get('path')} - {action.why}")
        key = (action.tool, tuple(sorted(action.args.items())))
        repeats = repeats + 1 if key == last_action else 0
        last_action = key
        if repeats > max_retries_same:
            note("ESCALATE", "same action repeated with no change -> stop, ask a human")
            break
        blocked = policy.check(action)
        if blocked:
            note("POLICY", f"BLOCKED: {blocked}")
            note("OBSERVE", "action was NOT executed; model must propose something else")
            continue
        note("POLICY", "allowed")
        if action.tool == "finish":
            tests = [x.text for x in log if x.phase == "OBSERVE" and x.text.startswith("rc=")]
            ok = bool(tests) and tests[-1].startswith("rc=0")
            note("VERIFY", "latest test run is green (rc=0)" if ok else "NOT VERIFIED: no passing test run observed")
            note("HANDOFF", "report exact revision + checks + limitations")
            break
        if action.tool == "read_file":
            out = tools.read_file(**action.args)
        elif action.tool == "edit_file":
            out = tools.edit_file(**action.args)
        else:
            out = tools.run_tests()
        note("EXECUTE", f"{action.tool} executed")
        note("OBSERVE", out.replace("\n", " | ")[:300])
    shutil.rmtree(tmp, ignore_errors=True)
    return log
