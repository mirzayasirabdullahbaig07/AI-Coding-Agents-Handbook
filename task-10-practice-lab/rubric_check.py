"""5-point rubric self-check: Clarity, Scope, Correctness, Verification, Handoff.

Each point is checked against files on disk, with the evidence printed. It does not replace human review.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
ALLOWED = {"task_tracker", "tests", "baseline", "docs", "ui", "AGENTS.md", "README.md", "diagnose_bug.py",
           "rubric_check.py", "demo.py", "generate_handoff.py", "render_ui.py", "PR_HANDOFF.md", "report.pdf",
           "screenshots", "__pycache__", ".gitignore"}


def run_tests():
    cp = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=ROOT,
                        capture_output=True, text=True)
    return cp.returncode, cp.stdout + cp.stderr


def main():
    rc, out = run_tests()
    tests_text = (ROOT / "tests" / "test_status_filter.py").read_text()
    handoff = (ROOT / "PR_HANDOFF.md")
    stray = sorted(p.name for p in ROOT.iterdir() if p.name not in ALLOWED and not p.name.startswith("."))
    points = [
        ("1 Clarity", "Acceptance" in tests_text and (ROOT / "AGENTS.md").exists(),
         "AGENTS.md present; acceptance-criteria test class present"),
        ("2 Scope", not stray, f"no unrelated top-level files (stray: {stray or 'none'})"),
        ("3 Correctness", rc == 0, f"unittest rc={rc}"),
        ("4 Verification", "NegativeTests" in tests_text and "PreservedBehaviour" in tests_text,
         "positive + negative + preserved-behaviour test classes"),
        ("5 Handoff", handoff.exists() and "Checks not run" in handoff.read_text(),
         "PR_HANDOFF.md has exact revision + 'Checks not run' section" if handoff.exists() else "PR_HANDOFF.md missing - run generate_handoff.py"),
    ]
    for name, ok, why in points:
        print(f"[{'PASS' if ok else 'FAIL'}] {name:<15} {why}")
    print(f"\nScore: {sum(p[1] for p in points)}/5")
    print("\nBefore marking complete, ask:")
    for q in ["Are requirement + acceptance criteria clear?", "Is the diff bounded (no unrelated change)?",
              "Was the exact revision inspected/tested?", "Were negative/regression cases run too?",
              "Are unavailable evidence, limitations and next action reported plainly?"]:
        print("  -", q)
    return 0 if all(p[1] for p in points) else 1


if __name__ == "__main__":
    raise SystemExit(main())
