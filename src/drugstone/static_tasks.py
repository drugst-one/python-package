"""
drugstone.static_tasks

This module implements the static_tasks function for the drugstone API.

:copyright: 2022 Institute for Computational Systems Biology by Prof. Dr. Jan Baumbach
:author: Ugur Turhan
"""

from typing import List
from .task.task import Task
from .task.tasks import Tasks


def static_tasks(tasks: List[Task]) -> Tasks:
    """Returns a :class:`Tasks` with a list of :class:`Task` objects.

    Use this for e.g. returning a :class:`TasksResult` or to compare tasks.

    :param List[Task] tasks: List of :class:`Task` objects.
    :return: :class:`Tasks` object
    """

    return Tasks(tasks)
