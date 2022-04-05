"""
drugstone.task.task

This module implements the class :class:`Task` for the drugstone API.

:copyright: 2022 Institute for Computational Systems Biology by Prof. Dr. Jan Baumbach
:author: Ugur Turhan
"""

from .task_result import TaskResult


class Task:
    """Represents a task.

    get_result() -> :class:`TaskResult`:
        Returns a :class:`TaskResult` for the result of the task.

    get_info() -> dict:
        Returns a dict with information about the task.

    get_parameters() -> dict:
        Returns a dict with the parameters of the task.
    """

    def __init__(self,
                 result: dict = None,
                 raw_data: dict = dict({}),
                 info: dict = dict({}),
                 params: dict = dict({})) -> None:
        self.__info = info
        self.__params = params
        self.__raw_data = raw_data
        if result is None:
            self.__result = dict({"drugs": {}, "genes": {}})
        else:
            self.__result = result

    def get_result(self) -> TaskResult:
        """Returns a :class:`TaskResult` for the result of the task."""

        return TaskResult(drugs=self.__result["drugs"],
                          genes=self.__result["genes"],
                          raw_data=self.__raw_data)

    def get_info(self) -> dict:
        """Returns a dict with information about the task."""

        return self.__info

    def get_parameters(self) -> dict:
        """Returns a dict with the parameters of the task."""

        return self.__params
