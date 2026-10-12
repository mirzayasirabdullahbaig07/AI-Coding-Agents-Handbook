# Task 06 - Communicating with AI: Weak -> Better -> Strong

Handbook reference: Page 6 of 10 (*AI Coding Agents - Intern Handbook, Task Tracker learning path*).

Reusable structure: Goal -> Context -> Scope -> Constraints -> Acceptance criteria -> Verification -> Required response. A strong request gives the agent both freedom and boundaries. Ask for assumptions, evidence, trade-offs and uncertainty - not for hidden chain-of-thought.

## What is in this folder
- `demo.py`
- `prompt_kit.py`
- `test_prompt_kit.py`
- `report.pdf` - the PDF report for this task (concept, code screenshots, demo screenshots, evidence report)
- `screenshots/` - PNG screenshots of the code, tests and demo output

## Run
```bash
python demo.py
python -m unittest discover -v
```
Requires Python 3.9+ and nothing else (standard library only).

## Last verified
PASS: Ran 7 tests in 0.002s (content hash `14d348e6ce22`, 2026-10-13)

## Not run / limitations
- Not run: Sending prompts to a real model
- Limitations: The grader is keyword-based: a quick teaching aid, not a quality guarantee.
