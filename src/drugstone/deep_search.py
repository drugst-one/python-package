"""
drugstone.deep_search

This module implements the deep_search function for the drugstone API.

:copyright: 2022 Institute for Computational Systems Biology by Prof. Dr. Jan Baumbach
:author: Ugur Turhan
"""

from .task.task import Task
from .new_task import new_task


def deep_search(seeds: list, parameters: dict = dict({})) -> Task:
    """Performs a drug-target search of the seeds, followed by a drug search on the drug-target results.

    Starts with a drug-target search for the seed genes.
    Then uses the resulting targets to search for drugs.

    :param list seeds: List of seed nodes for the task.
    :param dict parameters: (optional) Dictionary of parameters for the task. Defaults to an empty dict {}.
    :return: :class:`Task` object
    """

    # target search
    t_params = {**parameters, "target": "drug-target"}
    if "target_search" in parameters:
        t_params["algorithm"] = parameters["target_search"]
    t_search = new_task(seeds, t_params)
    targets = t_search.get_result().get_genes()

    # drug search
    d_params = {**parameters, "target": "drug"}
    if "drug_search" in parameters:
        d_params["algorithm"] = parameters["drug_search"]
    d_search = new_task(list(targets.keys()), d_params)
    return d_search
