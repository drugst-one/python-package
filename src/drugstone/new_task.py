"""
drugstone.new_task

This module implements the new_task function for the drugstone API.

:copyright: 2022 Institute for Computational Systems Biology by Prof. Dr. Jan Baumbach
:author: Ugur Turhan
"""

from .task.task import Task
from .scripts.normalize_task_parameter import normalize_task_parameter
from .scripts.wait_for_task_to_finish import wait_for_task_to_finish
from .scripts.map_nodes_to_internal_ids import map_nodes_to_internal_ids
from .scripts.start_task import start_task
from .scripts.request_task_result import request_task_result


def new_task(seeds: list, parameters: dict = dict({})) -> Task:
    """Starts a task.

    Starts a task, according to the user given seeds and parameters.
    Returns a :class:`Task` object, representing the task.

    :param list seeds: List of seed nodes for the task.
    :param dict parameters: (optional) Dictionary of parameters for the task. Defaults to an empty dict {}.
    :return: :class:`Task` object
    """

    internal_ids = map_nodes_to_internal_ids(seeds, parameters)
    normalized_params = normalize_task_parameter(parameters, internal_ids)
    token = start_task(normalized_params)
    task_id = normalized_params["parameters"]["task_id"]
    task_info = wait_for_task_to_finish(token, task_id)
    task_params = __create_parameters(task_info)
    if task_info["done"]:
        task_result = request_task_result(token, task_params)
        return Task(result=task_result, info=task_info, params=task_params)
    return Task(info=task_info, params=task_params)


def __create_parameters(info: dict) -> dict:
    algor = info["algorithm"]
    param = info["parameters"]
    param["algorithm"] = algor
    param.pop("inputNetwork")
    return param
