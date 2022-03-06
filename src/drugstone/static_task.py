"""
drugstone.static_task

This module implements the static_task function for the drugstone API.

:copyright: 2022 Institute for Computational Systems Biology by Prof. Dr. Jan Baumbach
:author: Ugur Turhan
"""

from typing import List
from .task.task import Task
from .task.models.drug import Drug
from .task.models.gene import Gene


def static_task(drugs: List[Drug] = list([]),
                genes: List[Gene] = list([])) -> Task:
    """Wraps a :class:`Task` around static data.

    Returns a static :class:`Task` with static data.
    No algorithm or anything will be executed to the data.
    You can use this for e.g. creating a :class:`TaskResult` to visualize data,
    or to use the static data with drugstone task data.

    :param List[Drug] drugs: (optional) List of :class:`Drug` objects. Defaults to an empty list [].
    :param List[Gene] genes: (optional) List of :class:`Gene` objects. Defaults to an empty list [].
    :return: :class:`Task` object
    """

    r_drugs = {}
    r_genes = {}
    for d in drugs:
        r_drugs = {**r_drugs, **d.to_dict()}
    for g in genes:
        r_genes = {**r_genes, **g.to_dict()}

    return Task({"drugs": r_drugs, "genes": r_genes})
