"""Run the unit tests of every task folder. Exit code 1 if any task fails."""
import subprocess
import sys
from pathlib import Path

root = Path(__file__).parent
failed = []
for task in sorted(root.glob("task-*")):
    args = [sys.executable, "-m", "unittest", "discover", "-q"]
    if task.name.startswith("task-10"):
        args = [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-q"]
    cp = subprocess.run(args, cwd=task, capture_output=True, text=True)
    last = (cp.stderr.strip().splitlines() or ["?"])[-1] if cp.returncode else "OK"
    ran = [l for l in cp.stderr.splitlines() if l.startswith("Ran ")]
    print(f"{'PASS' if cp.returncode == 0 else 'FAIL'}  {task.name:<42} {ran[0] if ran else ''} {last if cp.returncode else ''}")
    if cp.returncode:
        failed.append(task.name)
        print(cp.stderr)
sys.exit(1 if failed else 0)
