import requests
from data.url import Url

    
"""
Maps the given nodes to the internal IDs.
Returns a list of the internal IDs for 
"""
def map_nodes_to_internal_ids(nodes: list) -> list:

    formatted_nodes = []
    for node in nodes:
        formatted_nodes.append({"id": str(node)})
    
    # identifier: symbol, uniprot, ensemble
    data = {
        "nodes": formatted_nodes, 
        "identifier": "symbol"
        }
    
    """
    Sends the nodes to the drugst.one API
    and recieves an extendet list with the internal IDs
    """
    extended_node_ids = requests.post(
        Url.MAP_NODES.value,
        verify=False, 
        json=data
        )

    internal_ids = []
    for n in extended_node_ids.json():
        if "netexId" in n:
            internal_ids.append(n["netexId"])

    return internal_ids