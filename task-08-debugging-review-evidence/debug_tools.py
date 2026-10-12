"""Task 08 - Debugging, review and evidence.

reproduce -> relevant error -> hypothesis -> focused change -> verify -> regression check
"""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List

HERE = Path(__file__).parent


def run_tests(revision_dir: Path, pattern: str = "test_filter.py") -> dict:
    """Run the SAME tests against a given revision of the code."""
    env = dict(os.environ, TRACKER_DIR=str(revision_dir))
    cp = subprocess.run([sys.executable, "-m", "unittest", pattern, "-v"], cwd=HERE, env=env,
                        capture_output=True, text=True)
    text = cp.stdout + cp.stderr
    failed = [l.split(" ")[0] for l in text.splitlines() if l.endswith("... FAIL") or l.endswith("... ERROR")]
    return {"rc": cp.returncode, "failed": failed, "text": text}


def inspect_data_shape(tasks: List[dict]) -> Dict[str, int]:
    """Don't treat the error as the cause: look at the real data first."""
    return dict(Counter(t["status"] for t in tasks))


def hypothesis_from_shape(shape: Dict[str, int], ui_labels: List[str]) -> str:
    hits = [(lbl, s) for lbl in ui_labels for s in shape if s != lbl and s.lower() == lbl.lower()]
    if hits:
        lbl, s = hits[0]
        return f"UI label '{lbl}' != stored value '{s}' (case mismatch) -> normalise before comparing"
    return "no case-mismatch found; keep investigating (do not guess)"


def revision_hash(path: Path) -> str:
    return hashlib.sha256((path / "tracker.py").read_bytes()).hexdigest()[:10]


@dataclass
class EvidenceReport:
    """Handbook template: Change / Revision / Checks run / Results / Not run / Limitations / Next."""
    change: str
    revision: str
    checks_run: List[str]
    results: str
    checks_not_run: List[str]
    limitations: List[str]
    next_action: str

    def render(self) -> str:
        rows = [("Change", self.change), ("Revision tested", self.revision),
                ("Checks run", "; ".join(self.checks_run)), ("Results", self.results),
                ("Checks not run", "; ".join(self.checks_not_run) or "none"),
                ("Known limitations", "; ".join(self.limitations) or "none stated"),
                ("Next required action", self.next_action)]
        return "\n".join(f"{k + ':':<22}{v}" for k, v in rows)


def classify_failure(base_result: dict, new_result: dict) -> str:
    """If the failure also happens on the unchanged base, it is NOT a regression from our change."""
    new_f, base_f = set(new_result["failed"]), set(base_result["failed"])
    if not new_f:
        return "no failures on new revision"
    same = new_f & base_f
    regress = new_f - base_f
    parts = []
    if regress:
        parts.append(f"REGRESSION (new failures): {sorted(regress)}")
    if same:
        parts.append(f"PRE-EXISTING (also fail on base): {sorted(same)}")
    return "; ".join(parts)
