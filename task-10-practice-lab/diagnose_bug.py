"""Bug diagnosis demo: the first (naive) filter returned NOTHING for 'Done'.

Reproduce -> inspect data shape -> hypothesis -> focused change -> positive/negative check.
"""
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from task_tracker import filter_tasks, load_tasks  # noqa: E402


def naive_filter(tasks, status):          # first attempt (the buggy one)
    return [t for t in tasks if t["status"] == status]


tasks = load_tasks()
print("1) REPRODUCE   naive_filter(tasks, 'Done') ->", [t["id"] for t in naive_filter(tasks, "Done")], " expected [2, 4, 6]")
print("2) DATA SHAPE  stored statuses            ->", dict(Counter(t["status"] for t in tasks)))
print("3) HYPOTHESIS  UI label 'Done' vs stored 'done'/'DONE' (case mismatch), not a missing-data problem")
print("4) FIX         normalise both sides with .strip().lower()")
print("5) VERIFY      filter_tasks(tasks, 'Done') ->", [t["id"] for t in filter_tasks(tasks, "Done")])
print("   NEGATIVE    Open tasks inside Done result:", [t["id"] for t in filter_tasks(tasks, "Done") if t["status"].lower() == "open"] or "none")
