"""BASELINE (before the feature): the list shows every task. Kept for the scope/preservation check."""
import json
from pathlib import Path


def load_tasks(path=None):
    path = Path(path or Path(__file__).parent / "data.json")
    return json.loads(path.read_text())


def list_tasks(tasks):
    return list(tasks)
