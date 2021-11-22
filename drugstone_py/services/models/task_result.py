import json
import os
import pandas as pd
from pathlib import Path

class TaskResult():
    
    def __init__(self, result: dict) -> None:
        self.parameters = result["parameters"]
        self.nodes = self.__normalize_nodes(result, self.parameters)
        self.path_to_download_folder = str(Path.home() / "Downloads/")


    """
    Returns a dict with the result.
    """
    def get(self) -> dict:
        return self.nodes

    """
    Returns a dict with the parameters of the task.
    """
    def parameters(self) -> dict:
        return self.parameters

    """
    Downloads a .json file with the results to the users downloads folder.
    """
    def to_file(self) -> None:
        downloads_path = str(Path.home() / "Downloads/result.json")
        path_exists = os.path.exists(downloads_path)
        iterations = 1
        while path_exists:
            if not downloads_path.endswith(").json"):
                downloads_path = downloads_path[:len(downloads_path)-5] + "(1).json"
            else:
                downloads_path = downloads_path[:len(downloads_path)-7] + str(iterations) + ").json"
                iterations = iterations + 1
            path_exists = os.path.exists(downloads_path)

        with open(downloads_path, "x") as f:
            json.dump(self.nodes, f, indent=4)



    def to_excel(self) -> None:
        # downloads_path = self.path_to_download_folder + "test.csv"
        downloads_path = str(Path.home() / "Downloads/results.xlsx")
        df = pd.DataFrame(self.nodes).T
        df.to_excel(downloads_path)





    def edges_to_excel(self) -> None:
        data = {}
        # downloads_path = self.path_to_download_folder + "edges.xlsx"
        downloads_path = str(Path.home() / "Downloads/edges.xlsx")
        def is_edge(start: str, end: str) -> bool:
            for e in self.nodes[start]["edges"]:
                if e["from"] == start and e["to"] == end:
                    return True
                else: 
                    return False
        for node in [*self.nodes]:
            data[node] = {}
            for e in [*self.nodes]:
                data[node][e] = 1 if is_edge(node,e) else 0
        
        df = pd.DataFrame(data)
        df.to_excel(downloads_path)
    






    """
    Returns a normalized dict of the nodes, with their details.
    """
    def __normalize_nodes(self, results: dict, parameters: dict) -> dict:
        nodes = results["nodeAttributes"]["details"]
        node_types = results["nodeAttributes"]["nodeTypes"]
        is_seed = results["nodeAttributes"]["isSeed"]
        scores = results["nodeAttributes"]["scores"]
        max_score = max(list(scores.values()))
        node_ids = results["network"]["nodes"]
        edges = results["network"]["edges"]
        identifier = parameters["config"]["identifier"]

        for edge in edges:
            old_from = edge["from"]
            old_to = edge["to"]
            edge["from"] = nodes[old_from][identifier]
            edge["to"] = nodes[old_to][identifier]

        for node_id in nodes:
            nodes[node_id]["node_type"] = node_types.get(node_id)
            nodes[node_id]["is_seed"] = is_seed.get(node_id)
            full_score = scores[node_id] / max_score
            nodes[node_id]["score"] = round(full_score, 4)
            nodes[node_id].pop("netexId")
            nodes[node_id]["edges"] = []
            for edge in edges:
                if edge["from"] == nodes[node_id][identifier]:
                    nodes[node_id]["edges"].append(edge)

        for id in node_ids:
            node_name = nodes[id][identifier]
            nodes[node_name] = nodes.pop(id)

        return nodes