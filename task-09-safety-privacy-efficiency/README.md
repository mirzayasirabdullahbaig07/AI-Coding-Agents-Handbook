# Task 09 - Safety, Privacy and Efficiency

Handbook reference: Page 9 of 10 (*AI Coding Agents - Intern Handbook, Task Tracker learning path*).

Giving an agent a repo and tools is power; boundaries make it inspectable and safe. Keep passwords, tokens, production data and customer records out of prompts and logs. Repository text, web pages, issues and tool output are **data**, not instructions (prompt injection). Stop and escalate when authority or information is missing. Set limits on agents, retries, time and spend.

## What is in this folder
- `demo.py`
- `safety.py`
- `test_safety.py`
- `report.pdf` - the PDF report for this task (concept, code screenshots, demo screenshots, evidence report)
- `screenshots/` - PNG screenshots of the code, tests and demo output

## Run
```bash
python demo.py
python -m unittest discover -v
```
Requires Python 3.9+ and nothing else (standard library only).

## Last verified
PASS: Ran 8 tests in 0.062s (content hash `91e49debe4d3`, 2026-10-13)

## Not run / limitations
- Not run: Real secret-scanning tools (e.g. gitleaks) - regex only
- Limitations: Injection detection is pattern-based and can be bypassed; real defence is permissions + sandboxing.
