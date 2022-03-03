from src.drugstone.task.task import Task
from src.drugstone.task.scripts.task_scripts.normalize_task_parameter import normalize_task_parameter
from src.drugstone.task.scripts.task_scripts.wait_for_task_to_finish import wait_for_task_to_finish
from src.drugstone.task.scripts.network_scripts.map_nodes_to_internal_ids import map_nodes_to_internal_ids
from src.drugstone.task.scripts.network_scripts.start_task import start_task
from src.drugstone.task.scripts.network_scripts.request_task_result import request_task_result


def initiate_new_task(seeds: list, user_params: dict, task_id: int = None) -> Task:
    """Initiates a new task and returns a Task, representing it.

    Starts a task in the backend with the user given seeds and parameters.
    Parameters
    ----------
    seeds
    user_params
    task_id

    Returns
    -------

    """

    internal_ids = map_nodes_to_internal_ids(nodes=seeds, params=user_params)
    normalized_params = normalize_task_parameter(user_params, internal_ids)
    token = start_task(normalized_params)
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
