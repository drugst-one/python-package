

def add_edges_to_genes(
        genes: list,
        edges: list, ) -> dict:

    for gene in genes:
        if "netexId" in gene:
            netex_edges = [n["proteinB"] for n in edges if gene["netexId"] == n["proteinA"]]
            symbol_edges = []
            for e in netex_edges:
                for g in genes:
                    if "symbol" in g and "netexId" in g and e == g["netexId"]:
                        symbol_edges.append(g["symbol"])
            gene["has_edges_to"] = symbol_edges
        else:
            gene["has_edges_to"] = []

    result = {"drugs": {}, "genes": {}}

    for gene in genes:
        gene.pop("netexId", None)
        result["genes"][gene["id"]] = gene

    return result
