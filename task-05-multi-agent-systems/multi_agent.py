"""Task 05 - Multi-agent system with a delegation contract and task graph.

Agents here are simulated roles (plain functions) so the coordination logic is
visible and testable. The contract, conflict detection, scheduling and
file-scope enforcement are real.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Callable, Dict, List


@dataclass
class Contract:
    """Delegation contract: Task, Inputs, Allowed files, Constraints, Output, Verify, Stop."""
    task: str
    inputs: List[str]
    allowed_files: List[str]
    constraints: List[str]
    output: str
    verify: str
    stop: str

    def validate(self) -> List[str]:
        # allowed_files may be empty on purpose: a read-only agent edits nothing
        return [k for k, v in self.__dict__.items() if not v and k != "allowed_files"]


@dataclass
class Node:
    role: str
    contract: Contract
    agent: Callable[[Contract, Dict[str, dict]], dict]    # returns {"touched": [...], "notes": str, ...}
    depends_on: List[str] = field(default_factory=list)


def should_delegate(files_touched: int, clean_boundaries: bool, needs_final_diff: bool) -> str:
    """Handbook table: 'Kab delegate karein?'"""
    if files_touched <= 1 and not clean_boundaries:
        return "ONE AGENT - avoid coordination overhead"
    if needs_final_diff:
        return "SEQUENTIAL - implementation -> review"
    if clean_boundaries:
        return "DELEGATE - feature + tests + review with clean boundaries"
    return "ONE AGENT - boundaries unclear"


def find_conflicts(nodes: Dict[str, Node], parallel_group: List[str]) -> List[str]:
    """Two agents that may edit the same file must NOT run in parallel."""
    out, seen = [], {}
    for name in parallel_group:
        for f in nodes[name].contract.allowed_files:
            if f in seen:
                out.append(f"{f}: both '{seen[f]}' and '{name}' may edit it")
            seen[f] = name
    return out


def levels(nodes: Dict[str, Node]) -> List[List[str]]:
    """Topological levels: nodes in the same level can run in parallel."""
    done, result = set(), []
    remaining = dict(nodes)
    while remaining:
        ready = [n for n, v in remaining.items() if all(d in done for d in v.depends_on)]
        if not ready:
            raise ValueError("dependency cycle")
        result.append(sorted(ready))
        done.update(ready)
        for n in ready:
            remaining.pop(n)
    return result


def enforce_scope(node: Node, report: dict) -> None:
    bad = [f for f in report.get("touched", []) if f not in node.contract.allowed_files]
    if bad:
        raise PermissionError(f"agent '{node.role}' touched files outside contract: {bad}")


def run_graph(nodes: Dict[str, Node], log: Callable[[str], None] = print) -> Dict[str, dict]:
    for n in nodes.values():
        missing = n.contract.validate()
        if missing:
            raise ValueError(f"{n.role}: contract missing {missing}")
    results: Dict[str, dict] = {}
    for lvl in levels(nodes):
        conflicts = find_conflicts(nodes, lvl)
        if conflicts:
            log(f"  conflict -> running level sequentially: {conflicts}")
            groups = [[n] for n in lvl]
        else:
            groups = [lvl]
        for g in groups:
            log(f"  level {'||'.join(g)}" + ("  (parallel)" if len(g) > 1 else ""))
            with ThreadPoolExecutor(max_workers=len(g)) as ex:
                futs = {n: ex.submit(nodes[n].agent, nodes[n].contract, results) for n in g}
                for n, f in futs.items():
                    rep = f.result()
                    enforce_scope(nodes[n], rep)
                    results[n] = rep
    return results


# ------------------------ simulated Task Tracker roles ------------------------
def coordinator(c, r):  return {"touched": [], "notes": "scope fixed: status filter only"}
def implementer(c, r):  return {"touched": ["tracker.py"], "notes": "added status predicate (diff v1)"}
def tester(c, r):       return {"touched": ["test_tracker.py"], "notes": "cases: all/open/done + negative"}
def reviewer(c, r):
    impl = r["implement"]["notes"]
    return {"touched": [], "notes": f"reviewed final diff: '{impl}'. NOTE: reviewer shares implementer assumptions -> not independent proof"}


def task_tracker_graph() -> Dict[str, Node]:
    mk = lambda task, files, out: Contract(task, ["acceptance criteria", "TaskList + tests"], files,
                                            ["no refactor", "existing stack"], out, "focused tests", "blocked / criteria met")
    return {
        "coordinate": Node("Coordinator", mk("define scope", [], "scope note"), coordinator),
        "implement": Node("Implementation", mk("status filter", ["tracker.py"], "diff + notes"), implementer, ["coordinate"]),
        "test": Node("Test", mk("test cases", ["test_tracker.py"], "tests"), tester, ["coordinate"]),
        "review": Node("Review", mk("review diff", [], "findings"), reviewer, ["implement", "test"]),
    }
