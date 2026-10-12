"""Create PR_HANDOFF.md from REAL results: exact revision + exact checks + honest 'not run'."""
import hashlib
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent


def revision():
    try:
        sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
        dirty = subprocess.run(["git", "status", "--porcelain", "--", "task_tracker", "tests"], cwd=ROOT,
                               capture_output=True, text=True).stdout.strip()
        return f"git {sha}" + (" (+ uncommitted changes in task_tracker/tests!)" if dirty else "")
    except Exception:
        h = hashlib.sha256()
        for p in sorted(list((ROOT / "task_tracker").glob("*.py")) + list((ROOT / "tests").glob("*.py"))):
            h.update(p.read_bytes())
        return f"content-hash {h.hexdigest()[:12]} (not a git repository yet - re-run after your first commit)"


cp = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=ROOT, capture_output=True, text=True)
out = cp.stdout + cp.stderr
summary = [l for l in out.splitlines() if l.startswith("Ran ")][0]
result = "PASS" if cp.returncode == 0 else "FAIL"

(ROOT / "PR_HANDOFF.md").write_text(f"""# PR handoff: Task Tracker status filter

**Change:** add `All / Open / Done` status filter (`task_tracker/tracker.py`, `task_tracker/cli.py`) + tests.
Default behaviour (no filter = all tasks, original order) is preserved.

**Revision tested:** {revision()}
**Date:** {date.today().isoformat()}

## Checks run
- `python -m unittest discover -s tests -v` -> **{result}** ({summary})

## Results (key output)
```
{chr(10).join(l for l in out.splitlines() if l.endswith(('ok', 'FAIL', 'ERROR')) or l.startswith(('Ran', 'OK', 'FAILED'))) }
```

## Bug diagnosis
See `docs/BUG_DIAGNOSIS.md` (case mismatch between UI label `Done` and stored `done`/`DONE`).

## Checks not run
- Hosted CI: not run from this environment (runs on GitHub after push via `.github/workflows/ci.yml`)
- Browser/manual UI test: only a static HTML render was produced (`render_ui.py`)

## Known limitations
- Only the statuses `open` and `done` exist; any other value is rejected with an error (by design).
- Tests prove the behaviour they cover; they are not proof of everything.

## Next required action
Human code review, then CI on the pull request.
""")
print("wrote PR_HANDOFF.md ->", result, "|", summary)
