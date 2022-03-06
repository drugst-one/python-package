"""
drugstone.scripts.check_result_size

This module implements the check_result_size function.

:copyright: 2022 Institute for Computational Systems Biology by Prof. Dr. Jan Baumbach
:author: Ugur Turhan
"""


def check_result_size(result: dict, parameters: dict) -> dict:
    """Returns the results according to the result_size.

    Only edits the targeted results,
    e.g. for a drug-search, only the drugs will be edited.

    :param dict result: Dictionary of the result.
    :param dict parameters: Dictionary of the task parameters.
    :return: Dictionary of the results, according to the result_size.
    """

    target = parameters["target"]
    result_size = parameters["resultSize"]
    algorithm = ["algorithm"]

    drugs = result["drugs"]
    genes = result["genes"]

    if target == "drug":
        if len(drugs) <= result_size:
            return {"drugs": drugs, "genes": genes}
        if len(drugs) > result_size:
            sorted_drugs_list = sorted(drugs.values(), key=lambda item: item['score'])
            if algorithm != "proximity":
                # drugs are sorted from low to high score
                # usually the highest scored drugs are wanted
                # so sorted_drugs is reversed
                # only with the proximity algorithm
                # the lowest scored drugs are wanted
                sorted_drugs_list.reverse()
            resized_drugs = {}
            for drug in sorted_drugs_list[0:result_size]:
                label = drug["label"]
                resized_drugs[label] = drug
            drug_filtered_genes = {}
            for gene, detail in genes.items():
                old_edges = detail["has_edges_to"]
                new_edges = []
                for edge in old_edges:
                    if edge in resized_drugs.keys():
                        new_edges.append(edge)
                drug_filtered_genes[gene] = {
                    **detail,
                    "has_edges_to": new_edges
                }
            all_edges = []
            for _, gene in drug_filtered_genes.items():
                for e in gene["has_edges_to"]:
                    all_edges.append(e)
            filtered_genes = {}
            for gene, detail in drug_filtered_genes.items():
                if detail["is_seed"] or detail["has_edges_to"] or gene in all_edges:
                    filtered_genes[gene] = detail
            return {"drugs": resized_drugs, "genes": filtered_genes}

    if target == "drug-target":
        resized_genes = {}
        non_seed = []

        for gene, detail in genes.items():
            if detail["is_seed"]:
                resized_genes[gene] = detail
            else:
                non_seed.append(detail)

        if len(non_seed) <= result_size:
            for gene in non_seed:
                symbol = gene["symbol"]
                resized_genes[symbol] = gene

        if len(non_seed) > result_size:
            sorted_genes = sorted(non_seed, key=lambda item: item['score'])
            sorted_genes.reverse()
            for i in range(result_size):
                symbol = sorted_genes[i]["symbol"]
                resized_genes[symbol] = sorted_genes[i]
            for gene, detail in resized_genes.items():
                old_edges = detail["has_edges_to"]
                new_edges = []
                for edge in old_edges:
                    if edge in resized_genes.keys():
                        new_edges.append(edge)
                resized_genes[gene]["has_edges_to"] = new_edges

        return {"drugs": drugs, "genes": resized_genes}

    return {"drugs": drugs, "genes": genes}
