# Task 02 - LLM, Context and Memory: the Context Packet

Handbook reference: Page 2 of 10 (*AI Coding Agents - Intern Handbook, Task Tracker learning path*).

An LLM works only on the context it is given (prompt, tokens, a limited context window). Missing API contracts, tests or repo instructions lead to plausible but wrong code. Saved memory is not an automatically current repository record - the source code and repository instructions stay the source of truth. Give **relevant, current, bounded** context, never secrets.

## What is in this folder
- `context_packet.py`
- `demo.py`
- `sample_repo/AGENTS.md`
- `sample_repo/auth.py`
- `sample_repo/billing.py`
- `sample_repo/task_list.py`
- `sample_repo/test_task_list.py`
- `test_context_packet.py`
- `report.pdf` - the PDF report for this task (concept, code screenshots, demo screenshots, evidence report)
- `screenshots/` - PNG screenshots of the code, tests and demo output

## Run
```bash
python demo.py
python -m unittest discover -v
```
Requires Python 3.9+ and nothing else (standard library only).

## Last verified
PASS: Ran 6 tests in 0.003s (content hash `8b683758b6fd`, 2026-10-13)

## Not run / limitations
- Not run: Real tokenizer (token count is an estimate)
- Limitations: Secret detection is regex-based and will miss unusual formats; it is a safety net, not a guarantee.
