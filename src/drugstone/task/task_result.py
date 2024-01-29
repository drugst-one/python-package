"""
drugstone.task.task_result

This module implements the class :class:`TaskResult` for the drugstone API.

:copyright: 2024 Institute for Computational Systems Biology by Prof. Dr. Jan Baumbach
 
"""

import json
from pandas.core.frame import DataFrame
from .scripts.download_network_graph import download_network_graph
from .scripts.create_path import create_path


class TaskResult:
    """Represents the results of a task.

    get_genes() -> dict:
        Returns a dict with the genes.

    get_drugs() -> dict:
        Returns a dict with the drugs.

    to_dict() -> dict:
        Returns a dict with the result.

    to_pandas_dataframe() -> DataFrame:
        Returns a pandas :class:`DataFrame` of the result.

    download_json(path: str, name: str) -> None:
        Downloads a json file with the result.

    download_genes_csv(path: str, name: str) -> None:
        Downloads a csv file with the genes of the result.

    download_drugs_csv(path: str, name: str) -> None:
        Downloads a csv file with the drugs of the result.

    download_edges_csv(path: str, name: str) -> None:
        Downloads a csv file with the edges of the result.

    download_graph(path: str, name: str) -> None:
        Downloads a html file with a graph of the nodes.
    """

    def __init__(
            self,
            edges: list = list(),
            drugs: dict = dict(),
            genes: dict = dict(),
            raw_data: dict = dict()) -> None:
        self.__edges = edges
        self.__drugs = drugs
        self.__genes = genes
        self.__raw_data = raw_data
    
    def get_genes(self) -> dict:
        """Returns a dict with the genes."""

        return self.__genes

    def get_drugs(self) -> dict:
        """Returns a dict with the drugs."""

        return self.__drugs

    def get_raw_result(self) -> dict:
        """Returns the raw data of the task."""
        return self.__raw_data
    
    def get_edges(self) -> list:
        """Returns  the raw data of the Task"""
        return self.__edges
    
    def to_dict(self) -> dict:
        """Returns a dict with the result."""

        return {"drugs": self.__drugs, "genes": self.__genes}

    def to_pandas_dataframe(self) -> DataFrame:
        """Returns a pandas :class:`DataFrame` of the result."""

        return DataFrame(self.to_dict()).T

    def download_json(self, path: str = "", name: str = "result") -> None:
        """Downloads a json file with the result.

        :param str path: (optional) Path, where to download the file. Defaults to the current path.
        :param str name: (optional) Name for the file. Defaults to 'result'.
        """

        path = create_path(path, name, "json")
        with open(path, "x") as f:
            json.dump(self.to_dict(), f, indent=4)

    def download_raw_json(self, path: str = "", name: str = "raw_data") -> None:
        """Downloads a json file with the unprocessed results,
        as they are received from the backend.

        :param str path: (optional) Path, where to download the file. Defaults to the current path.
        :param str name: (optional) Name for the file. Defaults to 'raw_data'.
        """

        path = create_path(path, name, "json")
        with open(path, "x") as f:
            json.dump(self.get_raw_result(), f, indent=4)

    def download_genes_csv(self, path: str = "", name: str = "genes") -> None:
        """Downloads a csv file with the genes of the result.

        :param str path: (optional) Path, where to download the file. Defaults to the current path.
        :param str name: (optional) Name for the file. Defaults to 'genes'.
        """

        downloads_path = create_path(path, name, "csv")
        df = DataFrame(self.get_genes()).T
        df.to_csv(downloads_path)

    def download_drugs_csv(self, path: str = "", name: str = "drugs") -> None:
        """Downloads a csv file with the drugs of the result.

        :param str path: (optional) Path, where to download the file. Defaults to the current path.
        :param str name: (optional) Name for the file. Defaults to 'drugs'.
        """

        downloads_path = create_path(path, name, "csv")
        df = DataFrame(self.get_drugs()).T
        df.to_csv(downloads_path)

    def download_edges_csv(self, path: str = "", name: str = "edges") -> None:
        """Downloads a csv file with the edges of the result.

        :param str path: (optional) Path, where to download the file. Defaults to the current path.
        :param str name: (optional) Name for the file. Defaults to 'edges'.
        """

        edges = []
        for g in self.get_genes():
            for e in self.get_genes()[g]["hasEdgesTo"]:
                edges.append([g, e])
        data = {}
        for g in self.get_genes():
            data[g] = {}
            for e in self.get_genes():
                data[g][e] = 1 if [g, e] in edges or [e, g] in edges else 0
        df = DataFrame(data)
        downloads_path = create_path(path, name, "csv")
        df.to_csv(downloads_path)

    def download_graph(self, path: str = "", name: str = "graph") -> None:
        """Downloads a html file with a graph of the nodes.

        :param str path: (optional) Path, where to download the file. Defaults to the current path.
        :param str name: (optional) Name for the file. Defaults to 'graph'.
        """

        download_network_graph(self.to_dict(), path=path, name=name)
