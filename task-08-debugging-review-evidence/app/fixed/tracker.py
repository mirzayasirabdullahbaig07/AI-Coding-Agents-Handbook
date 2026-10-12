"""FIXED revision: focused normalisation change (one line of logic)."""


def filter_tasks(tasks, status="all"):
    if status == "all":
        return list(tasks)
    wanted = status.strip().lower()
    return [t for t in tasks if t["status"].strip().lower() == wanted]
