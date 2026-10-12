import argparse
import sys

from .tracker import STATUSES, list_tasks, load_tasks, render_table


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="task_tracker", description="Task Tracker")
    p.add_argument("command", choices=["list"])
    p.add_argument("--status", default="all", help="all | open | done")
    args = p.parse_args(argv)
    try:
        print(render_table(list_tasks(load_tasks(), args.status)))
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
