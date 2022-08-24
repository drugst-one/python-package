

def add_edges_to_genes(
        genes: list,
        edges: list, ) -> dict:

    for gene in genes:
        if "drugstoneId" in gene:
            netex_edges = [n["proteinB"] for n in edges if gene["drugstoneId"] == n["proteinA"]]
            symbol_edges = []
            for e in netex_edges:
                for g in genes:
                    if "symbol" in g and "drugstoneId" in g and e == g["drugstoneId"]:
                        symbol_edges.append(g["symbol"])
            gene["has_edges_to"] = symbol_edges
        else:
            gene["has_edges_to"] = []

    result = {"drugs": {}, "genes": {}}

    for gene in genes:
        gene.pop("drugstoneId", None)
        result["genes"][gene["id"]] = gene

    return result
