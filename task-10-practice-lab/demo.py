"""Practice-lab demo: feature + bug diagnosis + handoff + rubric, end to end."""
import subprocess
import sys
from pathlib import Path

root = Path(__file__).parent
py = sys.executable


def step(title, *cmd):
    print(f"\n===== {title} =====")
    print("$", " ".join(["python"] + list(cmd[1:])))
    subprocess.run(list(cmd), cwd=root)


step("List (existing behaviour preserved)", py, "-m", "task_tracker", "list")
step("List --status done", py, "-m", "task_tracker", "list", "--status", "done")
step("List --status open", py, "-m", "task_tracker", "list", "--status", "open")
step("Invalid status is rejected", py, "-m", "task_tracker", "list", "--status", "archived")
step("Bug diagnosis", py, "diagnose_bug.py")
step("Tests", py, "-m", "unittest", "discover", "-s", "tests", "-q")
step("PR handoff", py, "generate_handoff.py")
step("Rubric", py, "rubric_check.py")
