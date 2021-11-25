import json
import os
import pandas as pd
from pathlib import Path
from pyvis.network import Network
import random



class TaskResult():
    
    def __init__(self, result: dict) -> None:
        self.full_results = result
        self.parameters = result["parameters"]
        self.nodes = self.__normalize_nodes(result, self.parameters)
        self.path_to_download_folder = str(Path.home() / "Downloads/")


    def to_dict(self) -> dict:
        """Returns a dict with the result."""
        return self.nodes


    def get_parameters(self) -> dict:
        """Returns a dict with the parameters of the task."""
        return self.parameters


    def get_full_results(self) -> dict:
        """Returns the unfiltered results, as they come from the server."""
        return self.full_results


    def to_json(self):
        """Downloads a json file with the results to the users downloads folder."""

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


    def to_csv(self):
        # downloads_path = self.path_to_download_folder + "test.csv"
        downloads_path = str(Path.home() / "Downloads/results.csv")
        df = pd.DataFrame(self.nodes).T
        df.to_csv(downloads_path)


    def edges_to_csv(self):
        # downloads_path = self.path_to_download_folder + "edges.xlsx"
        downloads_path = str(Path.home() / "Downloads/edges.csv")

        edges = []
        for n in [*self.nodes]:
            for e in self.nodes[n]["edges"]:
                edges.append([e["from"], e["to"]])

        data = {}
        for n in [*self.nodes]:
            data[n] = {}
            for e in [*self.nodes]:
                data[n][e] = 1 if [n,e] in edges or [e,n] in edges else 0
                    

        # def is_edge(start: str, end: str):
        #     for e in self.nodes[start]["edges"]:
        #         if e["to"] == end:
        #             return 1
        #     return 0

        # for node in [*self.nodes]:
        #     data[node] = {}
        #     for e in [*self.nodes]:
        #         data[node][e] = is_edge(node,e)
        
        df = pd.DataFrame(data)
        df.to_csv(downloads_path)


    def to_excel(self):
        # downloads_path = self.path_to_download_folder + "test.csv"
        downloads_path = str(Path.home() / "Downloads/results.xlsx")
        df = pd.DataFrame(self.nodes).T
        df.to_excel(downloads_path)


    def edges_to_excel(self):
        data = {}
        # downloads_path = self.path_to_download_folder + "edges.xlsx"
        downloads_path = str(Path.home() / "Downloads/edges1.xlsx")
        
        def is_edge(start: str, end: str):
            for e in self.nodes[start]["edges"]:
                if e["to"] == end:
                    return 1
            return 0

        for node in [*self.nodes]:
            data[node] = {}
            for n in [*self.nodes]:
                data[node][n] = is_edge(node,n)
        
        df = pd.DataFrame(data).T
        df.to_excel(downloads_path)

    
    def to_graph(self) -> None:
        "Downloads a praph of the nodes in a html file."

        # The network.
        net = Network(height='90%', width='100%')

        # Adds the nodes to the network with a random color.
        for n in [*self.nodes]:
            hex_color = ["#"+''.join([random.choice('ABCDEF0123456789') for _ in range(6)])]
            net.add_node(n, color=hex_color[0])

        # Adds the edges to the network.
        edges = []
        for n in self.nodes:
            for e in self.nodes[n]["edges"]:
                edges.append((e["from"], e["to"]))
        net.add_edges(edges)

        # net.show_buttons(filter_=['physics'])
        net.set_edge_smooth("cubicBezier")
        net.set_options("""
        var options = {
            "physics": {
                "barnesHut": {
                "gravitationalConstant": -2000,
                "centralGravity": 0,
                "springLength": 20,
                "springConstant": 0.005,
                "avoidOverlap": 1
                },
                "minVelocity": 0.75
            }
        }
        """)
        # net.toggle_physics(False)
        net.show(str(Path.home() / "Downloads/graph.html"))


    

    """
    Returns a normalized dict of the nodes, with their details.
    """
    def __normalize_nodes(self, results: dict, parameters: dict) -> dict:
        nodes = results["nodeAttributes"]["details"]
        node_types = results["nodeAttributes"]["nodeTypes"]
        is_seed = results["nodeAttributes"]["isSeed"]
        node_ids = results["network"]["nodes"]
        edges = results["network"]["edges"]
        identifier = parameters["config"]["identifier"]

        # if "scores"
        scores = results["nodeAttributes"]["scores"]
        max_score = max(list(scores.values()))

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