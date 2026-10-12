"""Task 01 - Suggestion vs verified result.

A model PROPOSING a command is not the same as the application EXECUTING it.
"I ran the tests" is only a verified claim if an observable tool result exists.
This module records execution evidence and checks claims against it.
"""
from __future__ import annotations

import hashlib
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

VERIFIED = "VERIFIED"
FAILED = "FAILED (attempt ran, result is a failure)"
NOT_EXECUTED = "NOT VERIFIED (no execution evidence)"
BLOCKED = "NOT VERIFIED (command blocked / timed out)"


@dataclass
class Evidence:
    """Observable result of a command that was really executed."""
    command: List[str]
    returncode: Optional[int]          # None => never finished (timeout / blocked)
    stdout: str = ""
    stderr: str = ""
    started_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec="seconds"))
    revision: str = ""                 # exact code revision the evidence belongs to
    note: str = ""

    @property
    def finished(self) -> bool:
        return self.returncode is not None

    @property
    def passed(self) -> bool:
        return self.returncode == 0


def revision_of(path: Path) -> str:
    """Content hash of every .py file => 'exact revision' when git is not used."""
    h = hashlib.sha256()
    for p in sorted(Path(path).rglob("*.py")):
        h.update(p.name.encode())
        h.update(p.read_bytes())
    return h.hexdigest()[:12]


def run_check(command: List[str], cwd: Path, timeout: int = 30) -> Evidence:
    """Actually execute a command and capture what happened."""
    rev = revision_of(cwd)
    try:
        cp = subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return Evidence(command, cp.returncode, cp.stdout, cp.stderr, revision=rev)
    except subprocess.TimeoutExpired:
        return Evidence(command, None, revision=rev, note=f"timeout after {timeout}s")
    except (FileNotFoundError, PermissionError) as exc:
        return Evidence(command, None, revision=rev, note=f"blocked: {exc}")


@dataclass
class Claim:
    text: str
    evidence: Optional[Evidence] = None


def judge(claim: Claim) -> str:
    """Return the honest status of a claim."""
    ev = claim.evidence
    if ev is None:
        return NOT_EXECUTED
    if not ev.finished:
        return BLOCKED
    return VERIFIED if ev.passed else FAILED


def render_report(claims: List[Claim]) -> str:
    lines = []
    for i, c in enumerate(claims, 1):
        status = judge(c)
        lines.append(f"[{i}] claim : {c.text}")
        lines.append(f"    status: {status}")
        if c.evidence:
            e = c.evidence
            shown = [Path(e.command[0]).name] + e.command[1:]
            lines.append(f"    cmd   : {' '.join(shown)}")
            lines.append(f"    rc    : {e.returncode}   revision: {e.revision}   {e.note}".rstrip())
            tail = (e.stderr or e.stdout).strip().splitlines()[-1:] or [""]
            lines.append(f"    output: {tail[0]}")
        lines.append("")
    return "\n".join(lines)


PYTHON = sys.executable
