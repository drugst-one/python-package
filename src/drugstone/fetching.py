import requests
import json
from .scripts.constants.url import api

def getAdjacentDrugs(normalized_params, extended_genes):
    url = f'{api.BASE}adjacent_drugs/'
    seed_drugstone_ids = []
    for gene in extended_genes:
        if 'drugstoneId' not in gene:
            continue
        seed_drugstone_ids.extend(gene['drugstoneId'])
    seed_drugstone_ids = [x[1:] for x in seed_drugstone_ids] # remove prefix p
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