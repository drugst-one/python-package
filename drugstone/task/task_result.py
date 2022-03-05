import json
from pandas.core.frame import DataFrame
from .scripts.download_network_graph import download_network_graph
from .scripts.create_path import create_path


class TaskResult:

    def __init__(self, drugs: dict = dict({}), genes: dict = dict({})) -> None:
        self.__drugs = drugs
        self.__genes = genes

    def get_genes(self) -> dict:
        """Returns a dict with the genes."""
        return self.__genes

    def get_drugs(self) -> dict:
        """Returns a dict with the drugs."""
        return self.__drugs

    def to_dict(self) -> dict:
        """Returns a dict with the result."""
        return {"drugs": self.__drugs, "genes": self.__genes}

    def to_pandas_dataframe(self) -> DataFrame:
        return DataFrame(self.to_dict()).T

    def download_json(self, path: str = "", name: str = "result"):
        """Downloads a json file with the results to the given folder."""
        path = create_path(path, name, "json")
        with open(path, "x") as f:
            json.dump(self.to_dict(), f, indent=4)

    def download_genes_csv(self, path: str, name: str = "proteins") -> None:
        downloads_path = create_path(path, name, "csv")
        df = DataFrame(self.get_genes()).T
        df.sort_values(by="score", ascending=False).to_csv(downloads_path)

    def download_drugs_csv(self, path: str, name: str = "drugs") -> None:
        downloads_path = create_path(path, name, "csv")
        df = DataFrame(self.get_drugs()).T
        if df.empty:
            df.to_csv(downloads_path)
        else:
            df.sort_values(by="score", ascending=False).to_csv(downloads_path)

    def download_edges_csv(self, path: str, name: str = "edges") -> None:
        edges = []
        for g in self.get_genes():
            for e in self.get_genes()[g]["has_edges_to"]:
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
        """Downloads a graph of the nodes, in a html file."""
        download_network_graph(self.to_dict(), path=path, name=name)
