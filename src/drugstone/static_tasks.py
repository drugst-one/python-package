from typing import List
from .task.task import Task
from .task.tasks import Tasks


def static_tasks(tasks: List[Task]) -> Tasks:
    return Tasks(tasks)
