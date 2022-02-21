import json
import os
from pandas.core.frame import DataFrame
from task.scripts.check_result_size import check_result_size
from task.scripts.normalize_nodes import normalize_nodes
from task.scripts.download_network_graph import download_network_graph


class TaskResult:

    def __init__(self, result: dict) -> None:
        self.__full_results = result
        self.__parameters = result["parameters"]
        self.__nodes = check_result_size(
            nodes=normalize_nodes(result),
            parameters=self.__parameters
        )

    def to_dict(self) -> dict:
        """Returns a dict with the result."""
        return self.__nodes

    def get_parameters(self) -> dict:
        """Returns a dict with the parameters of the task."""
        return self.__parameters

    def get_full_results(self) -> dict:
        """Returns the unfiltered results, as they come from the server."""
        return self.__full_results

    def to_json(self, path: str, name: str = "result"):
        """Downloads a json file with the results to the given folder."""

        downloads_path = path + name + ".json"
        path_exists = os.path.exists(downloads_path)
        iterations = 1
        while path_exists:
            if not downloads_path.endswith(").json"):
                downloads_path = downloads_path[:len(downloads_path) - 5] + "(1).json"
            else:
                downloads_path = downloads_path[:len(downloads_path) - 7] + str(iterations) + ").json"
                iterations = iterations + 1
            path_exists = os.path.exists(downloads_path)

        with open(downloads_path, "x") as f:
            json.dump(self.__nodes, f, indent=4)

    def to_pandas_dataframe(self) -> DataFrame:
        return DataFrame(self.__nodes).T

    def proteins_to_csv(self, path: str, name: str = "proteins") -> None:
        downloads_path = path + name + ".csv"
        df = DataFrame(self.__nodes["genes"]).T
        df.sort_values(by="score", ascending=False).to_csv(downloads_path)

    def drugs_to_csv(self, path: str, name: str = "drugs") -> None:
        downloads_path = path + name + ".csv"
        df = DataFrame(self.__nodes["drugs"]).T
        if df.empty:
            df.to_csv(downloads_path)
        else:
            df.sort_values(by="score", ascending=False).to_csv(downloads_path)

    def edges_to_csv(self, path: str, name: str = "edges") -> None:
        downloads_path = path + name + ".csv"

        edges = []
        for n in [*self.__nodes]:
            for e in self.__nodes[n]["edges"]:
                edges.append([e["from"], e["to"]])

        data = {}
        for n in [*self.__nodes]:
            data[n] = {}
            for e in [*self.__nodes]:
                data[n][e] = 1 if [n, e] in edges or [e, n] in edges else 0

        df = DataFrame(data)
        df.to_csv(downloads_path)

    def to_graph(self, path: str, name: str = "graph") -> None:
        """Downloads a graph of the nodes, in a html file."""
        download_network_graph(self.__nodes, path=path, name=name)
