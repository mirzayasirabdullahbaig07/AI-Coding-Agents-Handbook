"""Task Tracker (buggy baseline used by the agent loop demo)."""


def filter_tasks(tasks, status="all"):
    if status == "all":
        return list(tasks)
    return [t for t in tasks if t["status"] == status]
