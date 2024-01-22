def add_edges_to_genes(
        genes: list,
        edges: list, 
        ) -> dict:

    result = []

    drugstone_id_to_network_id = {}
    for gene in genes:
        if 'drugstoneId' not in gene:
            continue
        for drugstone_id in gene['drugstoneId']:
            if drugstone_id in drugstone_id_to_network_id:
                drugstone_id_to_network_id[drugstone_id].append(gene['id'])
            else:
                drugstone_id_to_network_id[drugstone_id] = [gene['id']]
                
    drugstone_id_to_edges = {}
    for edge in edges:
        if edge['proteinA'] not in drugstone_id_to_edges:
            drugstone_id_to_edges[edge['proteinA']] = []
        drugstone_id_to_edges[edge['proteinA']].extend(
            drugstone_id_to_network_id.get(edge['proteinB'], []))
        
        if edge['proteinB'] not in drugstone_id_to_edges:
            drugstone_id_to_edges[edge['proteinB']] = []
        drugstone_id_to_edges[edge['proteinB']].extend(
            drugstone_id_to_network_id.get(edge['proteinA'], []))
        
    for gene in genes:
        gene["hasEdgesTo"] = []
        if "drugstoneId" in gene:
            for drugstone_id in gene['drugstoneId']:
                gene["hasEdgesTo"].extend(list(
                    set(drugstone_id_to_edges.get(drugstone_id, []))))
                        
        result.append(gene)

    return result
