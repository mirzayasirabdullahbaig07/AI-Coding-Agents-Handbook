# Task 04 - What Is the Orchestration Layer?

Handbook reference: Page 4 of 10 (*AI Coding Agents - Intern Handbook, Task Tracker learning path*).

The orchestration layer is the application logic around the model: task routing, context assembly, permissions, reliability (retry, timeout, checkpoints, logging) and completion logic. A smart prompt alone cannot grant file access, enforce permissions, persist state or guarantee tool execution. Even a single agent needs an orchestrator.

## What is in this folder
- `demo.py`
- `orchestrator.py`
- `test_orchestrator.py`
- `report.pdf` - the PDF report for this task (concept, code screenshots, demo screenshots, evidence report)
- `screenshots/` - PNG screenshots of the code, tests and demo output

## Run
```bash
python demo.py
python -m unittest discover -v
```
Requires Python 3.9+ and nothing else (standard library only).

## Last verified
PASS: Ran 8 tests in 1.058s (content hash `af2b4677c6e0`, 2026-10-13)

## Not run / limitations
- Not run: Concurrency / multi-process locking
- Limitations: Timeout uses a thread; a stuck tool thread cannot be force-killed in Python.
