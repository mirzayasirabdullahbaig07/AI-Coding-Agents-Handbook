# Task 03 - The Agent Working Loop

Handbook reference: Page 3 of 10 (*AI Coding Agents - Intern Handbook, Task Tracker learning path*).

The agent works in a loop: Task -> Inspect -> Propose -> Policy check -> Execute -> Observe -> Adjust -> Verify -> Handoff. The model proposes, the orchestration layer checks policy, tools execute, a human sets intent and approval limits. Retries must be bounded - repeating the same failing action only adds cost and confusion.

## What is in this folder
- `agent_loop.py`
- `demo.py`
- `test_agent_loop.py`
- `workspace/test_tracker.py`
- `workspace/tracker.py`
- `report.pdf` - the PDF report for this task (concept, code screenshots, demo screenshots, evidence report)
- `screenshots/` - PNG screenshots of the code, tests and demo output

## Run
```bash
python demo.py
python -m unittest discover -v
```
Requires Python 3.9+ and nothing else (standard library only).

## Last verified
PASS: Ran 6 tests in 0.811s (content hash `6af4c281d357`, 2026-10-13)

## Not run / limitations
- Not run: A real LLM (ScriptedModel is deterministic so the demo is reproducible)
- Limitations: Policy is a simple allow-list + single editable file; real systems need richer permission models.
