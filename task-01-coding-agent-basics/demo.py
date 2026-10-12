"""Demo: three claims an agent might make, judged by evidence."""
from pathlib import Path

from evidence import Claim, PYTHON, render_report, run_check

project = Path(__file__).parent / "sample_project"

print("=== Agent says: 'filter fix proposed' (suggestion only) ===")
claims = [
    Claim("I ran the focused filter test and it passes"),            # no evidence at all
]
print("=== Application executes the command (observable result) ===")
claims.append(Claim("focused filter test passes",
                    run_check([PYTHON, "-m", "unittest", "-v"], project)))
print("=== An attempt that failed / was blocked is NOT a completed action ===")
claims.append(Claim("lint passes", run_check(["no-such-linter", "."], project)))
claims.append(Claim("integration suite passes",
                    run_check([PYTHON, "-c", "import sys; sys.exit(1)"], project)))
print()
print(render_report(claims))
