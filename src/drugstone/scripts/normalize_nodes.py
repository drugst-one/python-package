"""
drugstone.scripts.normalize_results

This module implements the normalize_results function.

:copyright: 2024 Institute for Computational Systems Biology by Prof. Dr. Jan Baumbach
 
"""



def normalize_results(results: dict, identifier: str) -> dict:
    """Returns a normalized dict of the drugs and genes."""

    drugs = {}
    genes = {}
    drugstone_drug_id_to_label = {}

    # For all the nodes in the results,
    # differentiates if it's a drug or gene
    # and puts it in the according dict.
    nodes = results["nodeAttributes"]["details"]
    node_types = results["nodeAttributes"]["nodeTypes"]
    for n_id, n_type in node_types.items():
        nodes[n_id]["node_type"] = n_type
    for _, node in nodes.items():
        # init edge list for later
        node['hasEdgesTo'] = []
        node['isResult'] = False
        node['isConnector'] = False
        if node["node_type"] == "drug":
            n_name = node["label"]
            drugs[n_name] = node
            # needed because edge targets are drugstone IDs for drugs and not labels
            drugstone_drug_id_to_label[node['drugstoneId']] = n_name
        elif node["node_type"] == "protein":
            n_name = node[identifier][0]
            genes[n_name] = node

    # Adds to the genes if it's a seed or not.
    is_seed = results["nodeAttributes"]["isSeed"]
    for _, g_details in genes.items():
        g_details["is_seed"] = False if g_details[identifier][0] not in is_seed else is_seed[g_details[identifier][0]]

    # Add information if node is result node
    print('results', results)
    for node in results['targetNodes']:
        try:
            # node is drug
            label = drugstone_drug_id_to_label[node]
            drugs[label]['isResult'] = True
        except KeyError:
            # node is gene
            genes[node]['isResult'] = True

    # add information if node is connector node
    if 'intermediateNodes' in results:
        for node in results['intermediateNodes']:
            genes[node]['isConnector'] = True

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

    for e in edges:
        # test if it is a drug or gene edge
        if any([x in drugstone_drug_id_to_label for x in [e['from'], e['to']]]):
            # drug edge
            if e['from'] in drugstone_drug_id_to_label:
                label = drugstone_drug_id_to_label[e['from']]
                drugs[label]['hasEdgesTo'].append(e['to'])
                e['from'] = drugstone_drug_id_to_label[e['from']]
            else:
                # drug_id is in 'to'
                label = drugstone_drug_id_to_label[e['to']]
                drugs[label]['hasEdgesTo'].append(e['from'])
                e['to'] = drugstone_drug_id_to_label[e['to']]
        else:
            # gene edge
            if any([x not in genes for x in [e['from'], e['to']]]):
                #  some edge targets are somehow not in the network, this should be fixed in the backend
                continue
            genes[e['from']]['hasEdgesTo'].append(e['to'])
    
    
    # Removes unnecessary properties from drugs.
    for _, drug in drugs.items():
        drug.pop("drugstoneId")
        drug.pop("trialLinks")
        drug.pop("node_type")

    # Removes unnecessary properties from genes.
    for _, gene in genes.items():
        gene.pop("drugstoneId")
        gene.pop("node_type")

    return {"drugs": drugs, "genes": genes, "edges" : edges}
