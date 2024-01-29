"""
drugstone.deep_search

This module implements the deep_search function for the drugstone API.

:copyright: 2024 Institute for Computational Systems Biology by Prof. Dr. Jan Baumbach
 
"""

from typing import Union, List
from .task.task import Task
from .new_task import new_task


def deep_search(seeds: list, parameters: Union[dict, List[dict]] = dict({})) -> Task:
    """Performs a drug-target search of the seeds, followed by a drug search on the drug-target results.

    Starts with a drug-target search for the seed genes.
    Then uses the resulting targets to search for drugs.

    :param list seeds: List of seed nodes for the task.
    :param dict parameters: (optional) Dictionary of parameters for the task. Defaults to an empty dict {}.
    :return: :class:`Task` object
    """

    # task parameters
    t_params = {"algorithm": "keypathwayminer", "k": 10}
    d_params = {}

    if isinstance(parameters, list):
        if len(parameters) == 2:
            t_params = {**t_params, **parameters[0]}
            d_params = {**d_params, **parameters[1]}
        elif len(parameters) == 1:
            t_params = {**t_params, **parameters[0]}
            d_params = {**d_params, **parameters[0]}

    if isinstance(parameters, dict):
        for key, value in parameters.items():
            if isinstance(value, list) and len(value) > 1:
                t_params[key] = value[0]
                d_params[key] = value[1]
            else:
                t_params[key] = value
                d_params[key] = value

    t_params["target"] = "drug-target"
    d_params["target"] = "drug"
    if t_params.get("algorithm", None) == d_params.get("algorithm", None):
        t_params["has_duplicate_algorithms"] = True
        d_params["has_duplicate_algorithms"] = True

    # target search
    t_search = new_task(seeds, t_params)
    t_result = t_search.get_result().get_genes()
    # # keypathwayminer sometimes does not return all seeds
    targets = list({*seeds, *list(t_result.keys())})

    # drug search
    d_search = new_task(targets, d_params)
    return d_search
