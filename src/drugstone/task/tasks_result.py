"""
drugstone.task.tasks_result

This module implements the class :class:`TasksResult` for the drugstone API.

:copyright: 2022 Institute for Computational Systems Biology by Prof. Dr. Jan Baumbach
:author: Ugur Turhan
"""

import sys
import json
import logging
from typing import List
from .task import Task
from .scripts.create_path import create_path
from .scripts.make_upsetplot import make_upset_plot


class TasksResult:
    """Represents the results of a list of :class:`Task` objects.

    get_tasks_list() -> List[:class:`Task`]:
        Returns the list of tasks.

    to_dict() -> dict:
        Returns a dict with the results of the tasks.

    download_json(path: str, name: str) -> None:
        Downloads a json file with the results.

    create_upset_plot() -> None:
        Opens a new window with an upset plot of the results.
    """

    def __init__(self, tasks: List[Task] = []) -> None:
        self.__tasks = tasks

    def get_tasks_list(self) -> List[Task]:
        """Returns the list of tasks."""

        return self.__tasks

    def to_dict(self) -> dict:
        """Returns a dict with the results of the tasks."""

        d = {}
        for t in self.__tasks:
            d[t.get_parameters()["taskId"]] = {
                "info": t.get_info(),
                "parameters": t.get_parameters(),
                "results": t.get_result().to_dict()
            }
        return d

    def download_json(self, path: str = "", name: str = "result") -> None:
        """Downloads a json file with the results.

        :param str path: (optional) Path, where to download the file. Defaults to the current path.
        :param str name: (optional) Name for the file. Defaults to 'result'.
        """

        path = create_path(path, name, "json")
        with open(path, "x") as f:
            json.dump(self.to_dict(), f, indent=4)

    def create_upset_plot(self) -> None:
        """Opens a new window with an upset plot of the results.

        This is only available with python 3.6!
        """

        if sys.version_info[:2] == (3, 6):
            make_upset_plot(self.to_dict())
        else:
            logging.warn("create_upset_plot() is only compatible with Python 3.6!")
