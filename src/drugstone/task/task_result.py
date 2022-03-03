from pandas.core.frame import DataFrame
from src.drugstone.task.scripts.result_scripts.download_json import download_json
from src.drugstone.task.scripts.result_scripts.download_network_graph import download_network_graph


class TaskResult:

    def __init__(self, drugs: dict = dict({}), genes: dict = dict({})) -> None:
        self.__drugs = drugs
        self.__genes = genes

    def to_dict(self) -> dict:
        """Returns a dict with the result."""
        return {"drugs": self.__drugs, "genes": self.__genes}

    def get_genes(self) -> dict:
        """Returns a dict with the genes."""
        return self.__genes

    def get_drugs(self) -> dict:
        """Returns a dict with the drugs."""
        return self.__drugs

    def download_json(self, path: str, name: str = "result"):
        """Downloads a json file with the results to the given folder."""
        download_json(data=self.to_dict(), path=path, name=name)

    def to_pandas_dataframe(self) -> DataFrame:
        return DataFrame(self.to_dict()).T

    def genes_to_csv(self, path: str, name: str = "proteins") -> None:
        downloads_path = path + name + ".csv"
        df = DataFrame(self.get_genes()).T
        df.sort_values(by="score", ascending=False).to_csv(downloads_path)

    def drugs_to_csv(self, path: str, name: str = "drugs") -> None:
        downloads_path = path + name + ".csv"
        df = DataFrame(self.get_drugs()).T
        if df.empty:
            df.to_csv(downloads_path)
        else:
            df.sort_values(by="score", ascending=False).to_csv(downloads_path)

    def edges_to_csv(self, path: str, name: str = "edges") -> None:
        downloads_path = path + name + ".csv"

        edges = []
        for n in [*self.to_dict()]:
            for e in self.to_dict()[n]["edges"]:
                edges.append([e["from"], e["to"]])

        data = {}
        for n in [*self.to_dict()]:
            data[n] = {}
            for e in [*self.to_dict()]:
                data[n][e] = 1 if [n, e] in edges or [e, n] in edges else 0

        df = DataFrame(data)
        df.to_csv(downloads_path)

    def to_graph(self, path: str, name: str = "graph") -> None:
        """Downloads a graph of the nodes, in a html file."""
        download_network_graph(self.to_dict(), path=path, name=name)
