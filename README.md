# AI Coding Agents - Intern Handbook: Complete Code Pack

One folder per handbook page/task. Every task has its **own code, tests, demo, screenshots and PDF report**.
Pure Python 3.9+ standard library - nothing to install to run the tasks.

| # | Folder | Handbook topic | Report |
|---|--------|----------------|--------|
| 01 | `task-01-coding-agent-basics` | Suggestion vs verified result (evidence recorder) | `report.pdf` |
| 02 | `task-02-llm-context-memory` | Context packet, secret scan, token budget | `report.pdf` |
| 03 | `task-03-agent-working-loop` | Propose -> policy -> execute -> observe -> verify loop | `report.pdf` |
| 04 | `task-04-orchestration-layer` | Permissions, bounded retries, checkpoints, audit log | `report.pdf` |
| 05 | `task-05-multi-agent-systems` | Delegation contract, task graph, conflict detection | `report.pdf` |
| 06 | `task-06-ai-communication` | Prompt builder + Weak/Better/Strong grader | `report.pdf` |
| 07 | `task-07-repo-daily-workflow` | Real git workflow, exact-revision handoff | `report.pdf` |
| 08 | `task-08-debugging-review-evidence` | Reproduce, hypothesis, fix, regression, evidence report | `report.pdf` |
| 09 | `task-09-safety-privacy-efficiency` | Redaction, prompt-injection, escalate vs continue, budgets | `report.pdf` |
| 10 | `task-10-practice-lab` | Task Tracker status filter + PR handoff + rubric | `report.pdf` |

Each task folder contains: source code, `test_*.py`, `demo.py`, `README.md`, `report.pdf`, `screenshots/*.png`.

## Quick start
```bash
python run_all.py                 # runs every task's tests
cd task-03-agent-working-loop
python demo.py                    # run one task's demo
```

## Put it on GitHub
```bash
unzip ai-coding-agents-handbook.zip
cd ai-coding-agents-handbook
git init -b main
git add .
git commit -m "Add AI Coding Agents handbook tasks"
git remote add origin https://github.com/<your-user>/<your-repo>.git
git push -u origin main
```
`.github/workflows/ci.yml` runs all tests on GitHub Actions automatically after the push.

## Honest notes
- Agents/models in tasks 03 and 05 are **scripted stand-ins** so demos are reproducible offline; the loop, policies, tools, tests and git actions are real.
- The `report.pdf` evidence sections use a content hash as the revision. After you commit, re-run `python tools/make_reports.py` if you want the commit SHA (optional).
- Regenerate screenshots/reports (needs `pip install -r requirements-tools.txt` and Chromium for Playwright):
  `python tools/make_screenshots.py && python tools/make_reports.py`
- Not run here: hosted CI (it runs on GitHub after you push).
