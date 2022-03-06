"""
drugstone.task.scripts.download_network_graph

This module implements the download_network_graph function.

:copyright: 2022 Institute for Computational Systems Biology by Prof. Dr. Jan Baumbach
:author: Ugur Turhan
"""

from pyvis.network import Network
from .create_path import create_path


def download_network_graph(nodes: dict, path: str = "", name: str = "graph") -> None:
    """Downloads a html file with a graph of the nodes."""

    # The network.
    net = Network(height='90%', width='100%')

    # Adds the nodes to the network.
    for g_name, gene in nodes["genes"].items():
        if gene["is_seed"]:
            net.add_node(g_name, g_name + " (seed)", color="blue", shape="dot")
        elif not gene["is_seed"]:
            net.add_node(g_name, color="green", shape="triangle")
    for drug in nodes["drugs"]:
        net.add_node(drug, color="red", shape="square")

    # Adds the edges to the network.
    edges = []
    for n, gene in nodes["genes"].items():
        for e in gene["has_edges_to"]:
            edges.append((n, e))
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
    downloads_path = create_path(path, name, "html")
    net.show(downloads_path)
