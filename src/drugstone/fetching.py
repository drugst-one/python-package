import requests
import json
from .scripts.constants.url import api
from .scripts.request_task_result import request_task_result


def _strip_prefix(ids, prefix: str) -> list:
    """Returns drugstone IDs as the backend expects them, without 'p' (proteins) or 'dr' (drugs)."""
    return [i[len(prefix):] if isinstance(i, str) and i.startswith(prefix) else i for i in ids]


def getAdjacentDrugs(normalized_params, extended_genes):
    url = f'{api.BASE}adjacent_drugs/'
    seed_drugstone_ids = []
    for gene in extended_genes:
        if 'drugstoneId' not in gene:
            continue
        seed_drugstone_ids.extend(gene['drugstoneId'])
    seed_drugstone_ids = _strip_prefix(seed_drugstone_ids, 'p')
    payload = {
        'proteins': seed_drugstone_ids,
        'pdi_dataset': normalized_params['parameters']['pdiDataset'],
        'licenced': normalized_params['parameters']['licenced']
    }
    payload = json.dumps(payload)
    headers = {'Content-Type': 'application/json; charset=UTF-8'}
    response = requests.post(url=url, data=payload, headers=headers)
    # format result into task result format
    result = response.json()
    result['genes'] = extended_genes
    return result


def getAdjacentDisorders(normalized_params, extended_genes):
    """Returns the disorders associated with the seed proteins, with the mapped seeds as 'genes'."""
    seed_drugstone_ids = _strip_prefix([x for gene in extended_genes for x in gene.get('drugstoneId', [])], 'p')
    result = _post_adjacent_disorders({'proteins': seed_drugstone_ids},
                                      normalized_params['parameters'].get('associatedProteinDisorder'),
                                      normalized_params['parameters']['licenced'])
    result['genes'] = extended_genes
    return result


def get_adjacent_disorders_of_drugs(drugstone_ids: list, dataset: str = None, licenced: bool = False) -> dict:
    """Returns the disorders the given drugs are indicated for.

    :param list drugstone_ids: Drugstone IDs of drugs as in task results, e.g. "dr9774".
    :param str dataset: (optional) Drug-disorder indication dataset, defaults to the server's default.
    :param bool licenced: (optional) Use licensed datasets.
    :return: dict with "edges" (drug, disorder) and "disorders".
    """
    return _post_adjacent_disorders({'drugs': _strip_prefix(drugstone_ids, 'dr')}, dataset, licenced)


def _post_adjacent_disorders(nodes: dict, dataset: str, licenced: bool) -> dict:
    payload = {**nodes, 'licenced': licenced}
    if dataset:
        payload['dataset'] = dataset
    response = requests.post(f'{api.BASE}adjacent_disorders/', json=payload)
    response.raise_for_status()
    return response.json()

def get_pathway_network(token: str, geneset: str, pathway: str, summary: bool = False) -> dict:
    """Computes the network of one pathway of a finished pathway-enrichment task.

    :param str token: Token of the pathway-enrichment task, see Task.get_token().
    :param str geneset: Source of the pathway as in the result's tableView: "kegg", "reactome" or "wiki".
    :param str pathway: Name of the pathway as in the result's tableView.
    :param bool summary: (optional) If True, returns only geneset, pathway, the pathway's statistics
        from the tableView (without the gene details, which are in the network), the PPI dataset,
        network and isSeed.
    :return: The task's raw result, now including the pathway "network".

    The server stores one pathway network per task: a later call replaces it, also in the web view.
    """
    response = requests.put(
        f'{api.BASE}calculate_result_for_pathway/',
        params={'token': token, 'geneset': geneset, 'pathway': pathway})
    # an already computed pathway is returned directly; after computing a new one the server answers
    # "worked!" and stores it in the task result; on errors the result is read to explain them
    result = response.json() if response.ok and response.text.strip().startswith('{') else None
    if result is None:
        result = request_task_result(token)
    rows = result.get('tableView')
    if rows is None:
        raise ValueError('The task has no pathway enrichment result (no tableView).')
    row = next((r for r in rows if r['geneset'] == geneset and r['pathway'] == pathway), None)
    if row is None:
        raise ValueError(f'Pathway {pathway!r} from {geneset!r} is not in the task result; '
                         'use a geneset and pathway pair from its tableView.')
    response.raise_for_status()
    if summary:
        return {'geneset': result['geneset'], 'pathway': result['pathway'],
                'statistics': {k: v for k, v in row.items() if k != 'genes'},
                'geneInteractionDataset': result.get('geneInteractionDataset'),
                'network': result['network'], 'isSeed': result.get('nodeAttributes', {}).get('isSeed', {})}
    return result


def get_pathway_sources() -> list:
    """Returns the pathway sources used by pathway enrichment, each with label and url."""
    response = requests.get(f'{api.BASE}get_pathway_sources')
    response.raise_for_status()
    return response.json()


def get_datasets() -> dict:
    """Returns the datasets of the server with name, version and whether they are licensed.

    Grouped by "protein-protein", "protein-drug", "protein-disorder" and "drug-disorder".
    The names can be used as ppiDataset, pdiDataset, associatedProteinDisorder or as dataset of
    get_adjacent_disorders_of_drugs.
    """
    response = requests.get(f'{api.BASE}get_datasets/')
    response.raise_for_status()
    return response.json()


def get_tissues() -> list:
    """Returns available tissues with their internal ID and name."""
    response = requests.get(f'{api.BASE}tissues/')
    response.raise_for_status()
    return response.json()


def get_tissue_expression(tissue: str, proteins: list = None, identifier: str = 'symbol',
                          token: str = None) -> dict:
    """Returns expression by internal protein ID (p-prefixed), with None for missing values.

    Supply either protein identifiers or a task token. Protein identifiers are mapped using
    the existing mapping; unmapped inputs are logged and one-to-many mappings are retained.
    With a token, the proteins of the task result are used, whatever identifier the task used.
    Tissue IDs come from get_tissues(). No license is accepted by this function.
    """
    if (proteins is None) == (token is None):
        raise ValueError('Supply either proteins or token, not both.')
    payload = {'tissue': tissue}
    if proteins is not None:
        from .external_scripts.map_nodes_to_internal_ids import map_nodes_to_internal_ids
        mapped = map_nodes_to_internal_ids(proteins, {'identifier': identifier}, quiet=True)
        ids = sorted(set(_strip_prefix([i for node in mapped if node.get('drugstoneType') == 'protein'
                                        for i in node.get('drugstoneId', [])], 'p')))
        if not ids:
            return {}
        # The backend expects a JSON-encoded list even inside a JSON request body.
        payload['proteins'] = json.dumps(ids)
    else:
        # The backend's token route only finds proteins of tasks run with UniProt IDs,
        # so send the drugstone IDs of the result's proteins instead.
        result = request_task_result(token)
        attributes = result.get('nodeAttributes') or {}
        details = attributes.get('details') or {}
        protein_ids = [i for key, node_type in (attributes.get('nodeTypes') or {}).items()
                       if node_type == 'protein' for i in details.get(key, {}).get('drugstoneId', [])]
        protein_ids += [i for node in (result.get('network') or {}).get('nodes', [])
                        if isinstance(node, dict) and node.get('drugstoneType') == 'protein'
                        for i in node.get('drugstoneId', [])]
        ids = sorted(set(_strip_prefix([i for i in protein_ids if isinstance(i, str) and i.startswith('p')], 'p')))
        if not ids:
            return {}
        payload['proteins'] = json.dumps(ids)
    response = requests.post(f'{api.BASE}tissue_expression/', json=payload)
    response.raise_for_status()
    return response.json()


def get_tissue_proteins(tissue_id: str, threshold: float) -> list:
    """Returns proteins whose expression in the tissue is at least threshold."""
    response = requests.post(f'{api.BASE}query_tissue_proteins/',
                             json={'tissue_id': tissue_id, 'threshold': threshold})
    response.raise_for_status()
    return response.json()


def get_max_tissue_expression(tissue: str) -> dict:
    """Returns {'max': value} for a tissue, or {'max': None} if no values exist."""
    response = requests.get(f'{api.BASE}tissue_max_expression/', params={'tissue': tissue})
    response.raise_for_status()
    return response.json()
