# Task 01 - Coding Agent Basics: Suggestion vs Verified Result

Handbook reference: Page 1 of 10 (*AI Coding Agents - Intern Handbook, Task Tracker learning path*).

A coding agent is a supervised engineering assistant: model + instructions + context + authorised tools in an execution loop. It is not a chatbot, not autocomplete and not a human developer. The key rule of the page: a model **proposing** a command and the application **executing** it are different things. 'I ran the test' is a verified claim only if an observable tool result exists.

## What is in this folder
- `demo.py`
- `evidence.py`
- `sample_project/tasklist.py`
- `sample_project/test_tasklist.py`
- `test_evidence.py`
- `report.pdf` - the PDF report for this task (concept, code screenshots, demo screenshots, evidence report)
- `screenshots/` - PNG screenshots of the code, tests and demo output

## Run
```bash
python demo.py
python -m unittest discover -v
```
Requires Python 3.9+ and nothing else (standard library only).

## Last verified
PASS: Ran 6 tests in 1.097s (content hash `0fc202efbe9a`, 2026-10-13)

## Not run / limitations
- Not run: Real LLM calls (the demo uses fixed example claims)
- Limitations: Revision = content hash of .py files; in a git repo use the commit SHA (see Task 07).
