import logging


def check_result_size(nodes: dict, parameters: dict) -> dict:
    target = parameters["target"]
    result_size = parameters["resultSize"]
    algorithm = ["algorithm"]

    drugs = nodes["drugs"]
    genes = nodes["genes"]

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
            for drug in sorted_drugs_list[0:result_size-1]:
                label = drug["label"]
                resized_drugs[label] = drug
            return {"drugs": drugs, "genes": resized_drugs}

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