class TaskList:
    """Holds tasks and renders them. Status filter lives here."""

    def __init__(self, tasks):
        self.tasks = tasks

    def visible(self):
        return list(self.tasks)  # currently shows ALL tasks
