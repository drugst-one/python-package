import random
from pyvis.network import Network
from pathlib import Path


def download_network_graph(nodes: dict) -> None:
    """Downloads a graph of the nodes in a html file."""

    # The network.
    net = Network(height='90%', width='100%')

    # Adds the nodes to the network with a random color.
    for name, details in nodes.items():
        if details["node_type"] == "protein" and details["is_seed"]:
            net.add_node(name, name+" (seed)", color="blue", shape="dot")
        elif details["node_type"] == "protein" and not details["is_seed"]:
            net.add_node(name, color="green", shape="triangle")
        elif details["node_type"] == "drug" and details["is_seed"]:
            net.add_node(name, name+" (seed)", color="yellow", shape="star")
        elif details["node_type"] == "drug" and not details["is_seed"]:
            net.add_node(name, color="red", shape="square")
    
    # Adds the edges to the network.
    edges = []
    for n in nodes:
        for e in nodes[n]["edges"]:
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
