"""Tiny sample project used as the thing the 'agent' claims to have fixed."""


def filter_tasks(tasks, status="all"):
    status = status.lower()
    if status == "all":
        return list(tasks)
    return [t for t in tasks if t["status"].lower() == status]
