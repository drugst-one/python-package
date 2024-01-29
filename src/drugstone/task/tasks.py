"""
drugstone.task.tasks

This module implements the class :class:`Tasks` for the drugstone API.

:copyright: 2024 Institute for Computational Systems Biology by Prof. Dr. Jan Baumbach
 
"""

from typing import List
from .task import Task
from .task_result import TaskResult
from .tasks_result import TasksResult


class Tasks:
    """Wraps a list of :class:`Task` objects.

    get_result() -> :class:`TasksResult`:
        Returns a :class:`TasksResult` for the list of tasks.

    get_union() -> :class:`TaskResult`:
        Returns a :class:`TaskResult` with the union of the tasks.

    get_intersection() -> :class:`TaskResult`:
        Returns a :class:`TaskResult` with the intersection of the tasks.
    """

    def __init__(self, tasks: List[Task] = []) -> None:
        self.__tasks = tasks

    def get_result(self) -> TasksResult:
        """Returns a :class:`TasksResult` for the list of tasks."""

        return TasksResult(self.__tasks)

    def get_union(self) -> TaskResult:
        """Returns a :class:`TaskResult` with the union of the tasks."""

        drugs = {}
        genes = {}
        for t in self.__tasks:
            r = t.get_result()
            drugs = {**drugs, **r.get_drugs()}
            for gene, detail in r.get_genes().items():
                if gene not in genes:
                    genes = {**genes, gene: detail}
                else:
                    edges_a = genes[gene]["hasEdgesTo"]
                    edges_b = detail["hasEdgesTo"]
                    new_edges = list(set(edges_a + edges_b))
                    genes[gene]["hasEdgesTo"] = new_edges
        for d in drugs:
            if "score" in d:
                drugs[d].pop("score")
        for g in genes:
            if "score" in g:
                genes[g].pop("score")
        return TaskResult(drugs=drugs, genes=genes)

    def get_intersection(self) -> TaskResult:
        """Returns a :class:`TaskResult` with the intersection of the tasks."""

        drugs = {}
        genes = {}
        first = True
        for t in self.__tasks:
            r = t.get_result()
            if first:
                drugs = r.get_drugs()
                genes = r.get_genes()
                first = False
            else:
                drugs = {d: drugs[d] for d in drugs if d in r.get_drugs()}
                genes_intersection = {}
                for gene, detail in r.get_genes().items():
                    if gene in genes:
                        genes_intersection = {**genes_intersection, gene: detail}
                        edges_a = genes[gene]["hasEdgesTo"]
                        edges_b = detail["hasEdgesTo"]
                        new_edges = list(set(edges_a) & set(edges_b))
                        genes_intersection[gene]["hasEdgesTo"] = new_edges
                genes = genes_intersection.copy()
        for d in drugs:
            if "score" in d:
                drugs[d].pop("score")
        for g in genes:
            if "score" in g:
                genes[g].pop("score")
        return TaskResult(drugs=drugs, genes=genes)
