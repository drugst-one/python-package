

def normalize_nodes(results: dict, parameters: dict) -> dict:
    """Returns a normalized dict of the nodes, with their details.

    Parameters
    ----------
    results
    parameters
    """

    nodes = results["nodeAttributes"]["details"]
    node_types = results["nodeAttributes"]["nodeTypes"]
    is_seed = results["nodeAttributes"]["isSeed"]
    node_ids = results["network"]["nodes"]
    edges = results["network"]["edges"]

    has_score = False
    scores = []
    max_score = None
    if "scores" in results["nodeAttributes"]:
        has_score = True
        scores = results["nodeAttributes"]["scores"]
        max_score = max([x for x in list(scores.values()) if x is not None])

    # Iterates the edges and replaces the netexId with the common name.
    for edge in edges:
        old_from = edge["from"]
        old_to = edge["to"]
        if str(old_from).startswith("p"):
            edge["from"] = nodes[old_from]["symbol"]
        elif str(old_from).startswith("d"):
            edge["from"] = nodes[old_from]["label"]
        if str(old_to).startswith("p"):
            edge["to"] = nodes[old_to]["symbol"]
        elif str(old_to).startswith("d"):
            edge["to"] = nodes[old_to]["label"]

    for node_id in nodes:
        nodes[node_id]["node_type"] = node_types.get(node_id)
        nodes[node_id]["is_seed"] = is_seed.get(node_id)
        nodes[node_id].pop("netexId")
        nodes[node_id]["edges"] = []
        if has_score:
            if scores[node_id] is not None:
                full_score = scores[node_id] / max_score
                nodes[node_id]["score"] = round(full_score, 4)
            else:
                nodes[node_id]["score"] = None
        for edge in edges:
            if ((str(node_id).startswith("p") and edge["from"] == nodes[node_id]["symbol"]) or
            (str(node_id).startswith("d") and edge["from"] == nodes[node_id]["label"])):
                nodes[node_id]["edges"].append(edge)

    for i in node_ids:
        if str(i).startswith("p"):
            node_name = nodes[i]["symbol"]
        elif str(i).startswith("d"):
            node_name = nodes[i]["label"]
        nodes[node_name] = nodes.pop(i)

    return nodes
