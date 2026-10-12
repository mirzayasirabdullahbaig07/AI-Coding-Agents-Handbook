# PR handoff: Task Tracker status filter

**Change:** add `All / Open / Done` status filter (`task_tracker/tracker.py`, `task_tracker/cli.py`) + tests.
Default behaviour (no filter = all tasks, original order) is preserved.

**Revision tested:** content-hash e5d9a63b9ed1 (not a git repository yet - re-run after your first commit)
**Date:** 2026-10-13

## Checks run
- `python -m unittest discover -s tests -v` -> **PASS** (Ran 15 tests in 0.003s)

## Results (key output)
```
test_bad_status_exit_code (test_cli.CliTests.test_bad_status_exit_code) ... ok
test_default_lists_all (test_cli.CliTests.test_default_lists_all) ... ok
test_done_filter (test_cli.CliTests.test_done_filter) ... ok
test_all_returns_every_task (test_status_filter.AcceptanceCriteria.test_all_returns_every_task) ... ok
test_done_returns_done_tasks_any_case (test_status_filter.AcceptanceCriteria.test_done_returns_done_tasks_any_case) ... ok
test_open_returns_open_tasks_any_case (test_status_filter.AcceptanceCriteria.test_open_returns_open_tasks_any_case) ... ok
test_ui_labels_with_capital_letters_work (test_status_filter.AcceptanceCriteria.test_ui_labels_with_capital_letters_work) ... ok
test_done_filter_never_contains_open (test_status_filter.NegativeTests.test_done_filter_never_contains_open) ... ok
test_open_and_done_partition_all (test_status_filter.NegativeTests.test_open_and_done_partition_all) ... ok
test_open_filter_never_contains_done (test_status_filter.NegativeTests.test_open_filter_never_contains_done) ... ok
test_unknown_status_is_rejected_not_silently_empty (test_status_filter.NegativeTests.test_unknown_status_is_rejected_not_silently_empty) ... ok
test_default_list_equals_baseline (test_status_filter.PreservedBehaviour.test_default_list_equals_baseline) ... ok
test_empty_list (test_status_filter.PreservedBehaviour.test_empty_list) ... ok
test_input_not_mutated (test_status_filter.PreservedBehaviour.test_input_not_mutated) ... ok
test_order_preserved (test_status_filter.PreservedBehaviour.test_order_preserved) ... ok
Ran 15 tests in 0.003s
OK
```

## Bug diagnosis
See `docs/BUG_DIAGNOSIS.md` (case mismatch between UI label `Done` and stored `done`/`DONE`).

## Checks not run
- Hosted CI: not run from this environment (runs on GitHub after push via `.github/workflows/ci.yml`)
- Browser/manual UI test: only a static HTML render was produced (`render_ui.py`)

## Known limitations
- Only the statuses `open` and `done` exist; any other value is rejected with an error (by design).
- Tests prove the behaviour they cover; they are not proof of everything.

## Next required action
Human code review, then CI on the pull request.
