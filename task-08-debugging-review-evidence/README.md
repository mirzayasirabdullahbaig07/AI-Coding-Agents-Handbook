# Task 08 - Debugging, Review and Evidence

Handbook reference: Page 8 of 10 (*AI Coding Agents - Intern Handbook, Task Tracker learning path*).

Debugging means narrowing the cause with testable evidence and restoring intended behaviour: reproduce -> relevant error -> hypothesis -> focused change -> verify -> regression check. Do not call a failure 'flaky' without evidence, do not weaken assertions to get green, and remember that tests written with the same wrong assumption can both pass.

## What is in this folder
- `app/base/tracker.py`
- `app/fixed/tracker.py`
- `debug_tools.py`
- `demo.py`
- `test_debug_tools.py`
- `test_filter.py`
- `report.pdf` - the PDF report for this task (concept, code screenshots, demo screenshots, evidence report)
- `screenshots/` - PNG screenshots of the code, tests and demo output

## Run
```bash
python demo.py
python -m unittest discover -v
```
Requires Python 3.9+ and nothing else (standard library only).

## Last verified
PASS: Ran 11 tests in 0.246s (content hash `889c1bbd0b53`, 2026-10-13)

## Not run / limitations
- Not run: Browser/UI tests; Hosted CI
- Limitations: Only case/whitespace differences in status are covered.
