import logging
import warnings
import time
from task.scripts.network_scripts.request_task_info import request_task_info


def wait_for_task_to_finish(token: str, task_id: int = None) -> dict:
    """
    Waits for the Task to finish and returns the task information.
    Parameters
    ----------
    token
    task_id

    Returns
    -------
    dict: task information
    """

    info = request_task_info(token)
    name = info["algorithm"]
    if task_id is not None:
        name += "-" + str(task_id)
    while not info["done"] and not info["failed"]:
        logging.info(name + " progress is at: " + str(__get_progress(info)))
        time.sleep(2)
        info = request_task_info(token)
    if info["done"]:
        logging.info(name + " is done.")
    elif info["failed"]:
        warnings.warn(name + " has failed!")
    return info


def __get_progress(info: dict) -> str:
    f_progress = int(info["progress"]) * 100
    return str(f_progress) + "%"
