"""
drugstone.network

Uploads networks to the drugstone server to view them in the web interface, and prunes networks.

:copyright: 2024 Institute for Computational Systems Biology by Prof. Dr. Jan Baumbach

"""

import math
import requests
from .scripts.constants.url import api


def create_network(network: dict, config: dict = None, groups: dict = None) -> str:
    """Stores a network on the server and returns its id.

    The network can be viewed in the web interface, see :func:`get_network_link`.
    It is stored on the server and can be loaded by anyone who knows the id.
    Only the fields the web interface needs are sent: id, label and group of nodes, from, to and group
    of edges. The web interface maps the nodes again; other fields (e.g. booleans) would break loading.

    :param dict network: {"nodes": [{"id": ..., "group": ...}, ...], "edges": [{"from": ..., "to": ...}, ...]}
    :param dict config: (optional) drugstone config for the web interface, e.g. {"identifier": "symbol"}.
    :param dict groups: (optional) node and edge groups, e.g. {"nodeGroups": {...}, "edgeGroups": {...}}.
    :return: id of the stored network.
    """
    network = {
        'nodes': [{k: n[k] for k in ('id', 'label', 'group') if k in n} for n in network.get('nodes', [])],
        'edges': [{k: e[k] for k in ('from', 'to', 'group') if k in e} for e in network.get('edges', [])],
    }
    payload = {'network': network, 'config': config or {}, 'groups': groups or {}}
    response = requests.post(f'{api.BASE}create_network', json=payload)
    response.raise_for_status()
    return response.json()


def load_network(network_id: str) -> dict:
    """Returns a network stored with :func:`create_network`, with its config and groups."""
    response = requests.get(f'{api.BASE}load_network', params={'id': network_id})
    response.raise_for_status()
    return response.json()


def get_network_link(network_id: str, web_url: str = 'https://drugst.one/standalone') -> str:
    """Returns the link to view a stored network in the web interface.

    :param str web_url: (optional) standalone page of the web interface that uses the same server.
    """
    return f'{web_url}?id={network_id}'


def get_pruning_range(nodes: list, attribute: str) -> dict:
    """Returns the type and range (min/max) or unique values of a node attribute in "properties"."""
    response = requests.post(f'{api.BASE}prepare_pruning/', json={'nodes': nodes, 'pruning_attribute': attribute})
    response.raise_for_status()
    return response.json()


def prune_network(network: dict, attribute: str, cutoff: float = None, direction: str = 'greater',
                  unique_values: list = None, prune_orphan_nodes: bool = False) -> dict:
    """Keeps the nodes whose attribute in "properties" passes the cutoff or is one of the unique values.

    :param dict network: {"nodes": [...], "edges": [...]}, nodes with a "properties" dict.
    :param str attribute: name of the attribute in the nodes' "properties".
    :param float cutoff: (optional) keep nodes with a value >= cutoff ("greater") or <= cutoff ("lesser").
    :param str direction: (optional) "greater" or "lesser".
    :param list unique_values: (optional) keep nodes with one of these values, instead of a cutoff.
    :param bool prune_orphan_nodes: (optional) also remove kept nodes without kept edges.
    :return: {"network": all nodes, marked with "toBePruned", "prunedNetwork": the kept nodes and edges}
    """
    payload = {'network': network, 'pruning_attribute': attribute, 'cutoff': cutoff,
               'pruningDirection': direction, 'unique_values': unique_values or [],
               'pruneOrphanNodes': prune_orphan_nodes}
    response = requests.post(f'{api.BASE}prune/', json=payload)
    response.raise_for_status()
    return response.json()


def update_result_network(token: str, network: dict, cutoff: float = None, prune_orphan_nodes: bool = False) -> None:
    """Replaces the network of a task result, e.g. with a pruned first-neighbor network.

    The web interface does this after pruning a first-neighbor result; viewing the task afterwards
    shows the new network. The previous network of the task result is overwritten.

    :param str token: Token of the task, see Task.get_token().
    :param dict network: {"nodes": [...], "edges": [...]}, e.g. "prunedNetwork" of :func:`prune_network`.
    :param float cutoff: (optional) cutoff used for pruning, stored with the result.
    :param bool prune_orphan_nodes: (optional) whether orphan nodes were pruned, stored with the result.
    """
    payload = {'token': token, 'network': network, 'pruneOrphanNodes': prune_orphan_nodes}
    if cutoff is not None:
        payload['cutoff'] = cutoff
    response = requests.post(f'{api.BASE}update_result_network/', json=payload)
    response.raise_for_status()


def get_pruning_distribution(nodes: list, attribute: str, path: str = None, cutoff: float = None) -> dict:
    """Returns the distribution of a numeric node attribute in "properties", as in the web interface.

    :param list nodes: nodes with a "properties" dict.
    :param str attribute: name of the attribute in the nodes' "properties".
    :param str path: (optional) file to save a plot of the histogram and the sorted values to,
        e.g. "distribution.png" or ".svg".
    :param float cutoff: (optional) cutoff to mark in the plot.
    :return: count, missing (nodes without a numeric value), min, max, bins (from, to, count),
        sorted_values (ascending) and, with a path, plot.
    """
    values, missing = [], 0
    for node in nodes:
        value = (node.get('properties') or {}).get(attribute)
        if isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value):
            values.append(value)
        else:
            missing += 1
    values.sort()
    result = {'attribute': attribute, 'count': len(values), 'missing': missing, 'bins': [], 'sorted_values': values}
    if values:
        low, high = values[0], values[-1]
        # same binning as the web interface
        bin_count = min(30, max(5, math.ceil(math.sqrt(len(values)))))
        width = (high - low) / bin_count or 1
        bins = [{'from': low + i * width, 'to': low + (i + 1) * width, 'count': 0} for i in range(bin_count)]
        for value in values:
            bins[min(int((value - low) / width), bin_count - 1)]['count'] += 1
        result.update({'min': low, 'max': high, 'bins': bins})
    if path:
        # a Figure without pyplot does not change the caller's matplotlib backend
        from matplotlib.figure import Figure
        figure = Figure(figsize=(10, 4))
        histogram, ranked = figure.subplots(1, 2)
        histogram.bar([b['from'] for b in result['bins']], [b['count'] for b in result['bins']],
                      width=[b['to'] - b['from'] for b in result['bins']], align='edge', edgecolor='white')
        histogram.set(title=f'Distribution of {attribute}', xlabel=attribute, ylabel='nodes')
        ranked.plot(range(1, len(values) + 1), values, marker='.')
        ranked.set(title='Sorted values', xlabel='rank', ylabel=attribute)
        if cutoff is not None:
            histogram.axvline(cutoff, color='red', linestyle='--', label=f'cutoff {cutoff}')
            ranked.axhline(cutoff, color='red', linestyle='--')
            histogram.legend()
        figure.tight_layout()
        figure.savefig(path)
        result['plot'] = path
    return result


def overlay_directed_edges(network: dict, identifier: str = 'symbol') -> list:
    """Annotates existing edges with OmniPath direction, stimulation and inhibition.

    Node IDs and edge endpoints use identifier (symbol, uniprot, entrez or ensg).
    Only edges between proteins are annotated; edges to other nodes (e.g. drugs) are returned
    unchanged. Both directions may be returned, the reverse one with "_rev" appended to the
    edge id. Edges absent from OmniPath are retained unchanged. The input network is not modified.
    Returns the annotated edge list.
    """
    from .external_scripts.map_nodes_to_internal_ids import map_nodes_to_internal_ids
    mapped = map_nodes_to_internal_ids([n['id'] for n in network['nodes']],
                                      {'identifier': identifier}, quiet=True)
    nodes = {n['id']: n for n in mapped if n.get('drugstoneType') == 'protein' and n.get('drugstoneId')}
    edges = [dict(edge, id=edge.get('id', i)) for i, edge in enumerate(network.get('edges', []))]
    # the backend uses edge ids as strings, so send them as strings and restore the originals afterwards
    original_ids = {str(edge['id']): edge['id'] for edge in edges}
    protein_edges = [dict(edge, id=str(edge['id'])) for edge in edges
                     if edge['from'] in nodes and edge['to'] in nodes]
    other_edges = [edge for edge in edges if edge['from'] not in nodes or edge['to'] not in nodes]
    if not protein_edges:
        return other_edges
    response = requests.post(f'{api.BASE}overlay_directed_edges/', json={
        'ppi_dataset': 'OmniPath', 'licenced': False, 'edges': protein_edges, 'nodes_mapped_dict': nodes,
        'drugstone_mapping': {n['drugstoneId'][0]: key for key, n in nodes.items()}})
    response.raise_for_status()
    result = response.json()
    for edge in result:
        edge['id'] = original_ids.get(edge.get('id'), edge.get('id'))
    return result + other_edges


def recalculate_statistics(network: dict, config: dict) -> list:
    """Returns nodes with recalculated properties, without updating a saved task.

    Nodes must be mapped (identifier fields are lists); edge endpoints use that identifier.
    Config uses web-interface keys: identifier, interactionProteinProtein,
    interactionDrugProtein, licensedDatasets, reviewed, custom_edges and
    exclude_drugstone_ppi_edges. calculateProperties is always enabled here.
    With custom_edges and exclude_drugstone_ppi_edges, PPI degree is measured on the custom
    graph. Only proteins in the server's selected background graph are evaluated.
    The backend treats network topology as undirected.
    """
    response = requests.post(f'{api.BASE}recalculate_statistics/',
                             json={'network': network, 'config': {**config, 'calculateProperties': True}})
    response.raise_for_status()
    return response.json()
