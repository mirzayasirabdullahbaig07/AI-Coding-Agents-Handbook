import sys, tempfile
from pathlib import Path
from repo_workflow import create_branch, git, inspect_diff, make_handoff, preflight, run_checks

repo = Path(tempfile.mkdtemp())
git(repo, "init", "-q", "-b", "main"); git(repo, "config", "user.email", "intern@example.com"); git(repo, "config", "user.name", "Intern")
(repo / ".gitignore").write_text("__pycache__/\n")
(repo / "AGENTS.md").write_text("Run: python -m unittest\nNo unrelated refactors.\n")
(repo / "tracker.py").write_text('def filter_tasks(tasks, status="all"):\n    return list(tasks)\n')
(repo / "test_tracker.py").write_text("import unittest\nfrom tracker import filter_tasks\n\nclass T(unittest.TestCase):\n    def test_all(self):\n        self.assertEqual(len(filter_tasks([1, 2])), 2)\n")
git(repo, "add", "."); git(repo, "commit", "-qm", "baseline")

print("1) Instructions + status  (someone else left uncommitted work)")
(repo / "colleague_notes.txt").write_text("wip")
pf = preflight(repo)
print(f"   instructions={pf.instructions} branch={pf.branch} clean={pf.clean} uncommitted={pf.uncommitted}")
try:
    create_branch(repo, "feature/status-filter")
except RuntimeError as e:
    print("   REFUSED:", e)
(repo / "colleague_notes.txt").unlink()           # (colleague finished; tree is clean again)

print("\n3) Branch")
create_branch(repo, "feature/status-filter"); print("   on", preflight(repo).branch)

print("\n4) Small change")
(repo / "tracker.py").write_text('def filter_tasks(tasks, status="all"):\n    if status == "all":\n        return list(tasks)\n    return [t for t in tasks if t["status"].lower() == status.lower()]\n')
print("5) Inspect diff")
d = inspect_diff(repo, "HEAD", allowed=["tracker.py", "test_tracker.py"])
print(f"   files={d.files} +{d.insertions}/-{d.deletions} bounded={d.bounded}")
git(repo, "commit", "-qam", "Add status filter")

print("\n6) Checks / 8) Exact revision handoff")
checks = run_checks(repo, [[sys.executable, "-m", "unittest", "-q"]])
print(make_handoff(repo, checks, ["hosted CI - no remote configured"], ["only 'all' regression test exists locally"]).render())
