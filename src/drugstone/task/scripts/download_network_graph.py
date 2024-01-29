"""
drugstone.task.scripts.download_network_graph

This module implements the download_network_graph function.

:copyright: 2024 Institute for Computational Systems Biology by Prof. Dr. Jan Baumbach
 
"""

from pyvis.network import Network
from .create_path import create_path


def download_network_graph(nodes: dict, path: str = "", name: str = "graph") -> None:
    """Downloads a html file with a graph of the nodes."""

    # The network.
    net = Network(height='90%', width='100%')

    # Adds the nodes to the network.
    for g_name, gene in nodes["genes"].items():
        if "is_seed" in gene:
            if gene["is_seed"]:
                # net.add_node(g_name, g_name + " (seed)", color="blue", shape="dot")
                net.add_node(g_name, " ", color="blue", shape="dot")
            elif not gene["is_seed"]:
                # net.add_node(g_name, shape="triangle")
                net.add_node(g_name, " ", shape="triangle")
        else:
            net.add_node(g_name, g_name + " (static)", color="gray", shape="dot")
    for drug in nodes["drugs"]:
        net.add_node(drug, color="red", shape="square")

    # Adds the edges to the network.
    edges = []
    for n, gene in nodes["genes"].items():
        for e in gene["hasEdgesTo"]:
            edges.append((n, e))
    net.add_edges(edges)

    # net.show_buttons(filter_=['physics'])
    net.set_edge_smooth("cubicBezier")
    net.set_options("""
    var options = {
        "physics": {
            "enabled": true,
            "solver": "barnesHut",
            "barnesHut": {
                "gravitationalConstant": -250,
                "centralGravity": 0.001,
                "springLength": 50,
                "springConstant": 0.005,
                "avoidOverlap": 0.5
            },
            "stabilization": {
                "enabled": true,
                "iterations": 250
            }
        }
    }
    """)
    # net.toggle_physics(False)
    downloads_path = create_path(path, name, "html")
    net.show(downloads_path)

# private static analysisPhysics = {
#     enabled: true,
#     solver: 'barnesHut',
#     barnesHut: {
#       theta: 0.1,
#       gravitationalConstant: -50000,
#       centralGravity: 5,
#       springLength: 100,
#       springConstant: 0.8,
#       damping: 0.5,
#       avoidOverlap: 1,
#     },
#     stabilization: {
#       enabled: true,
#       iterations: 250
#     }
#   };

# "physics": {
#             "barnesHut": {
#             "gravitationalConstant": -250,
#             "centralGravity": 0,
#             "springLength": 50,
#             "springConstant": 0.005,
#             "avoidOverlap": 0.5
#             },
#             "minVelocity": 0.75
#         }
