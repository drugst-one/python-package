
from .map_nodes_to_internal_ids import map_nodes_to_internal_ids
from ..scripts.fetch_edges import fetch_edges
from ..scripts.add_edges_to_genes import add_edges_to_genes

def build_network(
        nodes: list,
        parameters: dict = dict({})) -> list:
        
    dataset = parameters.get('ppiDataset', 'nedrex')

    mapped_nodes = map_nodes_to_internal_ids(nodes, parameters)
    internal_ids = [gene['drugstoneId']
                    for gene in mapped_nodes if gene['drugstoneType'] == 'protein']
    edges = fetch_edges(internal_ids, dataset)

    task_result = add_edges_to_genes(
        mapped_nodes, edges)
    
    # remove drugstone ids
#     for node in task_result:
#         if 'drugstoneId' in node:
#             del node['drugstoneId']
    
    return task_result
    
    
    
