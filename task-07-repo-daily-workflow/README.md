# Task 07 - Daily Workflow in a Real Repository

Handbook reference: Page 7 of 10 (*AI Coding Agents - Intern Handbook, Task Tracker learning path*).

Before using AI in a repository, understand its state: existing uncommitted changes may belong to someone else and must not be overwritten or silently included. Flow: instructions + status -> code + criteria -> branch/worktree -> small change -> inspect diff -> checks -> PR review -> exact revision. Local pass, CI pass, merged and deployed are different states.

## What is in this folder
- `demo.py`
- `repo_workflow.py`
- `test_repo_workflow.py`
- `report.pdf` - the PDF report for this task (concept, code screenshots, demo screenshots, evidence report)
- `screenshots/` - PNG screenshots of the code, tests and demo output

## Run
```bash
python demo.py
python -m unittest discover -v
```
Requires Python 3.9+ and nothing else (standard library only).

## Last verified
PASS: Ran 6 tests in 0.791s (content hash `2e4cd042fb37`, 2026-10-13)

## Not run / limitations
- Not run: Hosted CI, merge and deploy (no remote in the demo)
- Limitations: Uses a temporary local repo; no push / PR creation is performed.
