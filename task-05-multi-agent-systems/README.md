# Task 05 - How a Multi-Agent System Is Built

Handbook reference: Page 5 of 10 (*AI Coding Agents - Intern Handbook, Task Tracker learning path*).

A multi-agent system has several agent instances with defined responsibilities and communication rules - possibly the same model. More agents are not automatically faster, cheaper or more accurate. Implementation and test planning can run in parallel when inputs are stable; review depends on the final diff. Two agents editing the same file conflict.

## What is in this folder
- `demo.py`
- `multi_agent.py`
- `test_multi_agent.py`
- `report.pdf` - the PDF report for this task (concept, code screenshots, demo screenshots, evidence report)
- `screenshots/` - PNG screenshots of the code, tests and demo output

## Run
```bash
python demo.py
python -m unittest discover -v
```
Requires Python 3.9+ and nothing else (standard library only).

## Last verified
PASS: Ran 7 tests in 0.004s (content hash `7537920ef876`, 2026-10-13)

## Not run / limitations
- Not run: Real LLM agents (roles are simulated functions)
- Limitations: Parallelism uses threads on simple functions; real agents would need isolated worktrees.
