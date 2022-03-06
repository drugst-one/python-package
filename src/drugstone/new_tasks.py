"""
drugstone.new_tasks

This module implements the new_tasks function for the drugstone API.

:copyright: 2022 Institute for Computational Systems Biology by Prof. Dr. Jan Baumbach
:author: Ugur Turhan
"""

from typing import Union, List
from .task.tasks import Tasks
from .new_task import new_task


def new_tasks(seeds: list, parameters: Union[dict, List[dict]] = dict({})) -> Tasks:
    """Starts multiple tasks.

    Starts multiple tasks, according to the user given seeds and parameters.
    Returns a :class:`Tasks` object, wrapping the individual the tasks.

    :param list seeds: List of seed nodes for the tasks.
    :param dict parameters: (optional) Dictionary of parameters for the tasks. Defaults to an empty dict {}.
    :return: :class:`Tasks` object
    """

    if isinstance(parameters, list):
        # returns a Tasks with a task for every parameter in the list of parameters
        tasks = []
        for p in parameters:
            t = new_task(seeds, p)
            tasks.append(t)
        return Tasks(tasks)

    if isinstance(parameters, dict):
        # returns a Tasks with a task ...
        algorithm = None
        if "algorithm" in parameters:
            algorithm = parameters["algorithm"]
        elif "algorithms" in parameters:
            algorithm = parameters["algorithms"]
        if isinstance(algorithm, list):
            # ... for every algorithm in the list of algorithms
            tasks = []
            for alg in algorithm:
                t_param = {**parameters, "algorithm": alg}
                t = new_task(seeds, t_param)
                tasks.append(t)
            return Tasks(tasks)

    # or else returns a Tasks with just a single task
    task = new_task(seeds, parameters)
    return Tasks([task])
