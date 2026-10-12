"""BASE revision: contains the bug. UI label is 'Done' but stored status is lowercase 'done'."""


def filter_tasks(tasks, status="all"):
    if status == "all":
        return list(tasks)
    return [t for t in tasks if t["status"] == status]
