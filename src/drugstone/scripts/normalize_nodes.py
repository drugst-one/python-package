"""
drugstone.scripts.normalize_nodes

This module implements the normalize_nodes function.

:copyright: 2022 Institute for Computational Systems Biology by Prof. Dr. Jan Baumbach
:author: Ugur Turhan
"""


def normalize_nodes(results: dict) -> dict:
    """Returns a normalized dict of the drugs and genes."""

    drugs = {}
    genes = {}

    # For all the nodes in the results,
    # differentiates if it's a drug or gene
    # and puts it in the according dict.
    nodes = results["nodeAttributes"]["details"]
    node_types = results["nodeAttributes"]["nodeTypes"]
    for n_id, n_type in node_types.items():
        nodes[n_id]["node_type"] = n_type
    for _, node in nodes.items():
        if node["node_type"] == "drug":
            n_name = node["label"]
            drugs[n_name] = node
        elif node["node_type"] == "protein":
            n_name = node["symbol"]
            genes[n_name] = node

    # Adds to the genes if it's a seed or not.
    is_seed = results["nodeAttributes"]["isSeed"]
    for _, g_details in genes.items():
        g_details["is_seed"] = is_seed[g_details["netexId"]]

    # Normalizes the scores for the drugs.
    drug_scores = []
    for _, drug in drugs.items():
        if "score" in drug:
            drug_scores.append(drug["score"])
    if drug_scores:
        max_drug_score = max([x for x in drug_scores if x is not None])
    for _, drug in drugs.items():
        if "score" in drug and (type(drug["score"]) == int
                                or type(drug["score"]) == float):
            old_score = drug["score"]
            new_score = round(old_score / max_drug_score, 4)
            drug["score"] = new_score
        else:
            drug["score"] = None

    # sorts drugs without a score out
    none_score_drugs = []
    for drug, detail in drugs.items():
        if detail["score"] is None:
            none_score_drugs.append(drug)
    for x in none_score_drugs:
        drugs.pop(x)

    # Normalizes the scores for the genes.
    gene_scores = [1]
    for _, gene in genes.items():
        if "score" in gene:
            gene_scores.append(gene["score"])
    max_gene_score = max([x for x in gene_scores if x is not None])
    for _, gene in genes.items():
        if "score" in gene and (type(gene["score"]) == int
                                or type(gene["score"]) == float):
            old_score = gene["score"]
            new_score = round(old_score / max_gene_score, 4)
            gene["score"] = new_score
        else:
            gene["score"] = None

    # Adds the edges to the genes.
    edges = results["network"]["edges"]
    for _, gene in genes.items():
        edges_dict = [x for x in edges if x["from"] == gene["netexId"]]
        edges_netex_id = []
        edges_normalized = []
        for e in edges_dict:
            edges_netex_id.append(e["to"])
        for e in edges_netex_id:
            if str(e).startswith("p"):
                for _, g in genes.items():
                    if e == g["netexId"]:
                        edges_normalized.append(g["symbol"])
            elif str(e).startswith("d"):
                for _, d in drugs.items():
                    if e == d["netexId"]:
                        edges_normalized.append(d["label"])
            else:
                edges_normalized.append(e)
        gene["has_edges_to"] = edges_normalized

    # Removes unnecessary properties from drugs.
    for _, drug in drugs.items():
        drug.pop("netexId")
        drug.pop("trialLinks")
        drug.pop("node_type")

    # Removes unnecessary properties from genes.
    for _, gene in genes.items():
        gene.pop("netexId")
        gene.pop("node_type")

    return {"drugs": drugs, "genes": genes}
