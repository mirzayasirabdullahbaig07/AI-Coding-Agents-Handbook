"""Task Tracker core. Feature added in this lab: status filter (All / Open / Done)."""
import json
from pathlib import Path
from typing import Dict, List, Optional

STATUSES = ("all", "open", "done")
DATA_FILE = Path(__file__).with_name("data.json")


def load_tasks(path: Optional[Path] = None) -> List[Dict]:
    return json.loads(Path(path or DATA_FILE).read_text())


def filter_tasks(tasks: List[Dict], status: str = "all") -> List[Dict]:
    """Return the tasks matching `status` ('all' | 'open' | 'done', case-insensitive).

    * never mutates `tasks`, keeps original order
    * stored statuses may be 'open', 'Open', 'DONE'... so both sides are normalised
      (this is the bug diagnosed in docs/BUG_DIAGNOSIS.md)
    """
    wanted = (status or "all").strip().lower()
    if wanted not in STATUSES:
        raise ValueError(f"unknown status '{status}'. Choose from {', '.join(STATUSES)}")
    if wanted == "all":
        return list(tasks)
    return [t for t in tasks if t["status"].strip().lower() == wanted]


def list_tasks(tasks: List[Dict], status: str = "all") -> List[Dict]:
    """Existing entry point. Default argument keeps the OLD behaviour (show everything)."""
    return filter_tasks(tasks, status)


def render_table(tasks: List[Dict]) -> str:
    if not tasks:
        return "(no tasks)"
    rows = [f"{t['id']:>3}  {t['status'].lower():<5}  {t['title']}" for t in tasks]
    return "\n".join(["ID   STAT   TITLE", "---  -----  -----", *rows])
