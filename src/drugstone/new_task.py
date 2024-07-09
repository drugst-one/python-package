"""
drugstone.new_task

This module implements the new_task function for the drugstone API.

:copyright: 2024 Institute for Computational Systems Biology by Prof. Dr. Jan Baumbach
 
"""

import warnings
from typing import List
from .task.task import Task
from .task.models.drug import Drug
from .task.models.gene import Gene
from .scripts.normalize_task_parameter import normalize_task_parameter
from .scripts.wait_for_task_to_finish import wait_for_task_to_finish
from .external_scripts.map_nodes_to_internal_ids import map_nodes_to_internal_ids
from .scripts.start_task import start_task
from .scripts.request_task_result import request_task_result
from .scripts.fetch_edges import fetch_edges
from .scripts.add_edges_to_genes import add_edges_to_genes
from .scripts.merge_results import merge_results
from .scripts.normalize_nodes import normalize_results
from .license import license
import copy


def new_task(
        seeds: list = list([]),
        parameters: dict = dict({}),
        static: bool = False,
        static_result: dict = dict({}),
        static_drugs: List[Drug] = list([]),
        static_genes: List[Gene] = list([])) -> Task:
    """Returns a task.

    Starts a task, according to the user given seeds and parameters.
    Returns a :class:`Task` object, representing the task.

    :param list seeds: List of seed nodes for the task.
    :param dict parameters: (optional) Dictionary of parameters for the task. Defaults to an empty dict {}.
    :param bool static: (optional)
    :param dict static_result: (optional)
    :param List[Drug] static_drugs: (optional)
    :param List[Gene] static_genes: (optional)
    :return: :class:`Task` object
    """

    parameters = copy.deepcopy(parameters)
    
    extended_genes = map_nodes_to_internal_ids(seeds, parameters)
    if 'identifier' not in parameters:
        parameters['identifier'] = 'symbol'

    # in case of custom network input
    ids = set()
    if 'custom_edges' in parameters:
        #  are a list of dicts like [{"fom":..., "to":...}, ...]
        # we need to make the identifiers to internal ids
        edge_node_ids = set([*(map(lambda x: x['from'], parameters['custom_edges'])), *(map(lambda x: x['to'], parameters['custom_edges']))])
        for x in edge_node_ids:
            ids.add(x)
    if 'network_nodes' in parameters:
        #  are a list of strings
        for node in parameters['network_nodes']:
            ids.add(node)
    if len(ids) > 0:
        background_network_ids = map_nodes_to_internal_ids(ids, parameters)
        print(background_network_ids)
        background_network_id_map = {
            n['id']: n[parameters['identifier']][0] for n in background_network_ids if n['drugstoneType'] == 'protein'}

    # map the custom edges and custom nodes to drugstone Ids
    if 'custom_edges' in parameters:
        mapped_custom_edges = []
        for edge in parameters['custom_edges']:
            from_internal = background_network_id_map.get(edge['from'], False)
            to_internal = background_network_id_map.get(edge['to'], False)
            if from_internal is False or to_internal is False:
                warnings.warn(f"Could not map edge {edge['from']} - {edge['to']}.")
                continue
            edge['from'] = from_internal
            edge['to'] = to_internal
            mapped_custom_edges.append(edge)
        parameters['custom_edges'] = mapped_custom_edges
    if 'network_nodes' in parameters:
        mapped_custom_nodes = []
        for node in parameters['network_nodes']:
            internal_id = background_network_id_map.get(node, False)
            if internal_id is False:
                warnings.warn(f"Could not map node {node}.")
                continue
            mapped_custom_nodes.append(
                internal_id)
        parameters['network_nodes'] = mapped_custom_nodes
       
    internal_ids = [n[parameters['identifier']][0] for n in extended_genes if n['drugstoneType'] == 'protein']
    normalized_params = normalize_task_parameter(parameters, internal_ids)
    if parameters['algorithm'] == 'adjacentDrugs':
        from .fetching import getAdjacentDrugs
        result = getAdjacentDrugs(normalized_params, extended_genes)
        return Task(result=result, params=normalized_params, raw_data=result)

    # static task
    if static:
        warnings.warn("Static option is deprecated.")
        # dataset = normalized_params["parameters"]["ppiDataset"]
        # edges = fetch_edges(internal_ids, dataset)
        # task_result = add_edges_to_genes(extended_genes, edges, parameters['identifier'])
        # task_result['drugs'] = {}
        # genes_drugs = __get_dict_for_genes_and_drugs(static_drugs, static_genes)
        # task_result = merge_results(task_result, genes_drugs)
        # task_result = merge_results(task_result, static_result)
        # return Task(result=task_result, params=normalized_params)
        return

    # no seeds and no static
    if not static and not seeds:
        warnings.warn("Something went wrong! "
                      + "Maybe you forgot to pass seed genes, "
                      + "or forgot to set static to True.")
        return Task()

    # dynamic task
    token = start_task(normalized_params)
    task_id = normalized_params["parameters"]["task_id"]
    task_info = wait_for_task_to_finish(token, task_id)
    task_params = __create_parameters(task_info)
    if task_info["done"]:
        raw_data = request_task_result(token)
        task_result = normalize_results(raw_data, parameters['identifier'])
        return Task(result=task_result, raw_data=raw_data, info=task_info, params=task_params)
    return Task(info=task_info, params=task_params)


def __create_parameters(info: dict) -> dict:
    algor = info["algorithm"]
    param = info["parameters"]
    param["algorithm"] = algor
    del param["inputNetwork"]
    return param


def __get_dict_for_genes_and_drugs(drugs: List[Drug], genes: List[Gene]) -> dict:
    r_drugs = {}
    r_genes = {}

    for d in drugs:
        r_drugs = {**r_drugs, **d.to_dict()}
    for g in genes:
        r_genes = {**r_genes, **g.to_dict()}

    return {"drugs": r_drugs, "genes": r_genes}
