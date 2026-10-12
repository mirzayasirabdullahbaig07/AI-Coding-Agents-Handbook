"""Task 07 - Daily workflow in a REAL git repository.

1 instructions + status -> 2 code + criteria -> 3 branch -> 4 small change
5 inspect diff -> 6 checks -> 7 PR review -> 8 exact revision

Everything here shells out to real `git`. It never overwrites uncommitted work
that isn't yours; it reports it instead.
"""
from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import List, Optional

INSTRUCTION_FILES = ["AGENTS.md", "CLAUDE.md", "CONTRIBUTING.md"]


def git(repo: Path, *args: str) -> str:
    cp = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True)
    if cp.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {cp.stderr.strip()}")
    return cp.stdout.strip()


@dataclass
class Preflight:
    instructions: List[str]
    branch: str
    uncommitted: List[str]           # someone else's work - do NOT overwrite / silently include
    clean: bool


def preflight(repo: Path) -> Preflight:
    instr = [f for f in INSTRUCTION_FILES if (repo / f).exists()]
    status = git(repo, "status", "--porcelain")
    changed = [l[3:] for l in status.splitlines()]
    return Preflight(instr, git(repo, "rev-parse", "--abbrev-ref", "HEAD"), changed, not changed)


def create_branch(repo: Path, name: str) -> None:
    pf = preflight(repo)
    if not pf.clean:
        raise RuntimeError(f"refusing to branch with uncommitted changes that are not ours: {pf.uncommitted}")
    git(repo, "checkout", "-b", name)


@dataclass
class DiffReport:
    files: List[str]
    insertions: int
    deletions: int
    out_of_scope: List[str]

    @property
    def bounded(self) -> bool:
        return not self.out_of_scope


def inspect_diff(repo: Path, base: str, allowed: List[str]) -> DiffReport:
    names = git(repo, "diff", "--name-only", base).splitlines()
    ins = dele = 0
    for line in git(repo, "diff", "--numstat", base).splitlines():
        a, d, _ = line.split("\t", 2)
        ins += int(a) if a.isdigit() else 0
        dele += int(d) if d.isdigit() else 0
    return DiffReport(names, ins, dele, [n for n in names if n not in allowed])


def run_checks(repo: Path, commands: List[List[str]]) -> List[dict]:
    out = []
    for cmd in commands:
        cp = subprocess.run(cmd, cwd=repo, capture_output=True, text=True)
        out.append({"cmd": " ".join(["python" if cmd[0] == sys.executable else cmd[0], *cmd[1:]]),
                    "rc": cp.returncode,
                    "tail": (cp.stdout + cp.stderr).strip().splitlines()[-1:] or [""]})
    return out


class State(Enum):
    LOCAL_TESTS_PASS = "Local tests pass: selected checks pass on the tested revision"
    HOSTED_CI_PASS = "Hosted CI pass: CI checked this specific revision/config"
    MERGED = "Merged: integrated into base branch"
    DEPLOYED = "Deployed: released to a runtime; behaviour still needs observing"


@dataclass
class Handoff:
    revision: str
    checks: List[dict]
    states: List[State]
    not_run: List[str]
    limitations: List[str] = field(default_factory=list)

    def render(self) -> str:
        lines = [f"Exact revision tested: {self.revision}", "Checks run:"]
        lines += [f"  - `{c['cmd']}` -> rc={c['rc']} ({c['tail'][0]})" for c in self.checks]
        lines.append("Delivery states EVIDENCED: " + (", ".join(s.name for s in self.states) or "none"))
        lines.append("Delivery states NOT evidenced: " +
                     ", ".join(s.name for s in State if s not in self.states))
        lines.append("Checks not run: " + ("; ".join(self.not_run) or "none"))
        lines.append("Limitations: " + ("; ".join(self.limitations) or "none stated"))
        return "\n".join(lines)


def make_handoff(repo: Path, checks: List[dict], not_run: List[str], limitations: Optional[List[str]] = None) -> Handoff:
    if git(repo, "status", "--porcelain"):
        raise RuntimeError("working tree is dirty: evidence would not belong to a single exact revision")
    rev = git(repo, "rev-parse", "--short", "HEAD")
    states = [State.LOCAL_TESTS_PASS] if checks and all(c["rc"] == 0 for c in checks) else []
    return Handoff(rev, checks, states, not_run, limitations or [])
