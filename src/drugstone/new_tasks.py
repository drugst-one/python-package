"""
drugstone.new_tasks

This module implements the new_tasks function for the drugstone API.

:copyright: 2024 Institute for Computational Systems Biology by Prof. Dr. Jan Baumbach
 
"""

import warnings
from typing import Union, List
from .new_task import new_task
from .task.task import Task
from .task.tasks import Tasks
from .scripts.normalize_task_parameter import normalize_task_parameter
import copy

def new_tasks(
        seeds: list = list([]),
        parameters: Union[dict, List[dict]] = dict({}),
        static: bool = False,
        static_tasks: List[Task] = list([])) -> Tasks:
    """Starts multiple tasks.

    Starts multiple tasks, according to the user given seeds and parameters.
    Returns a :class:`Tasks` object, wrapping the individual the tasks.

    :param list seeds: (optional) List of seed nodes for the tasks.
    :param dict parameters: (optional) Dictionary of parameters for the tasks. Defaults to an empty dict {}.
    :param bool static: (optional)
    :param List[Task] static_tasks: (optional)
    :return: :class:`Tasks` object
    """
    parameters = copy.deepcopy(parameters)
    
    # static list of tasks
    if static:
        return Tasks(static_tasks)

    # no seeds and no static
    if not static and not seeds:
        warnings.warn("Something went wrong! "
                      + "Maybe you forgot to pass seed genes, "
                      + "or forgot to set static to True.")
        return Tasks()

    # tasks with a list of parameter dictionaries
    if isinstance(parameters, list):
        algs = []
        for p in parameters:
            if "algorithm" in p:
                algs.append(p["algorithm"])
            elif "algorithms" in p:
                algs.append(p["algorithms"])
            else:
                algs.append(normalize_task_parameter({}, [])["algorithm"])
        has_duplicates = len(algs) != len(set(algs))
        tasks = []
        for p in parameters:
            new_p = {**p, "has_duplicate_algorithms": has_duplicates}
            t = new_task(seeds, new_p)
            tasks.append(t)
        return Tasks(tasks)

    # tasks with a list of algorithms
    if isinstance(parameters, dict):
        algorithms = None
        if "algorithm" in parameters:
            algorithms = parameters["algorithm"]
        elif "algorithms" in parameters:
            algorithms = parameters["algorithms"]
        if isinstance(algorithms, list):
            has_duplicates = len(algorithms) != len(set(algorithms))
            tasks = []
            for alg in algorithms:
                t_param = {
                    **parameters,
                    "algorithm": alg,
                    "has_duplicate_algorithms": has_duplicates
                }
                t_param.pop("algorithms", None)
                t = new_task(seeds, t_param)
                tasks.append(t)
            return Tasks(tasks)

    # Tasks with just a single task
    task = new_task(seeds, parameters)
    return Tasks([task])
