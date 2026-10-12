# Task 10 - Practice Lab: Task Tracker Status Filter + PR Handoff

Handbook reference: Page 10 of 10 (*AI Coding Agents - Intern Handbook, Task Tracker learning path*).

Exercise: add a status filter to the existing Task Tracker, preserve current behaviour, diagnose one relevant bug and prepare an evidence-backed PR handoff. Acceptance: All / Open / Done behave per criteria; a Done filter must never contain Open tasks. Complete means: diff reviewed, selected checks recorded, exact revision and limitations reported.

## What is in this folder
- `AGENTS.md`
- `PR_HANDOFF.md`
- `baseline/tracker_before.py`
- `demo.py`
- `diagnose_bug.py`
- `docs/BUG_DIAGNOSIS.md`
- `generate_handoff.py`
- `render_ui.py`
- `rubric_check.py`
- `task_tracker/__init__.py`
- `task_tracker/__main__.py`
- `task_tracker/cli.py`
- `task_tracker/data.json`
- `task_tracker/tracker.py`
- `tests/test_cli.py`
- `tests/test_status_filter.py`
- `ui/tracker_all.html`
- `ui/tracker_done.html`
- `ui/tracker_open.html`
- `report.pdf` - the PDF report for this task (concept, code screenshots, demo screenshots, evidence report)
- `screenshots/` - PNG screenshots of the code, tests and demo output

## Run
```bash
python demo.py
python -m unittest discover -s tests -v
```
Requires Python 3.9+ and nothing else (standard library only).

## Last verified
PASS: Ran 15 tests in 0.002s (content hash `775c3c4cc5fb`, 2026-10-13)

## Not run / limitations
- Not run: Hosted CI (runs on GitHub after push); Manual browser testing (static HTML render only)
- Limitations: Only two statuses exist; the rubric is an automated aid, not a replacement for review.
