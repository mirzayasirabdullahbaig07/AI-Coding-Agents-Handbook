# Bug diagnosis note

**Symptom:** while adding the status filter, selecting **Done** returned no tasks (and an early variant showed wrong rows).

**Reproduce:** `python diagnose_bug.py` -> naive filter `t["status"] == "Done"` returns `[]`, expected `[2, 4, 6]`.

**Error is not the cause.** Data shape inspected first: stored statuses are `open`, `Open`, `done`, `DONE`.

**Hypothesis:** UI label `Done` != stored value `done`/`DONE` (case mismatch). Tested by normalising both sides.

**Focused change:** `.strip().lower()` on the requested status and the stored status (one function, `filter_tasks`).

**Checks:** positive (`Done` -> 2,4,6; `Open` -> 1,3,5), negative (Done never contains Open), regression
(default list == baseline, order preserved, input not mutated).

**Limitations:** tests and implementation were written with the same assumption (two statuses). Unknown statuses
raise `ValueError` rather than returning an empty list so the assumption fails loudly.
