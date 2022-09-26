

import string


def add_edges_to_genes(
        genes: list,
        edges: list, 
        identifier: string
        ) -> dict:

    for gene in genes:
        if "drugstoneId" in gene:
            netex_edges = [n["proteinB"] for n in edges if gene["drugstoneId"] == n["proteinA"]]
            symbol_edges = []
            for e in netex_edges:
                for g in genes:
                    if identifier in g and "drugstoneId" in g and e == g["drugstoneId"]:
                        symbol_edges.append(g[identifier])
            gene["hasEdgesTo"] = symbol_edges
        else:
            gene["hasEdgesTo"] = []

    result = {"drugs": {}, "genes": {}}

    for gene in genes:
        gene.pop("drugstoneId", None)
        result["genes"][gene["id"]] = gene

    return result
