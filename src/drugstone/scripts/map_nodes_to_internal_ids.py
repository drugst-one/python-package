"""
drugstone.scripts.map_nodes_to_internal_ids

This module implements the map_nodes_to_internal_ids function.

:copyright: 2022 Institute for Computational Systems Biology by Prof. Dr. Jan Baumbach
:author: Ugur Turhan
"""

import requests
import warnings
from .constants.url import Url
from .constants.task_parameter import TaskParameter
from .normalize_task_parameter import normalize_task_parameter


def map_nodes_to_internal_ids(
        nodes: list,
        params: dict = dict({})) -> list:
    """Maps the given nodes to the internal IDs.

    Returns a list of the internal IDs.
    """

    if "identifier" in params:
        if params["identifier"] in TaskParameter.IdentifierValues.IDENTIFIER_VALUES:
            identifier = params["identifier"]
        else:
            identifier = get_default_identifier()
            warnings.warn("The identifier: " + str(params["identifier"])
                          + "is not known to Drugstone!"
                          + " The identifier is changed to "
                          + str(identifier) + "!")
    else:
        identifier = get_default_identifier()

    formatted_nodes = []
    for node in nodes:
        formatted_nodes.append({"id": str(node)})

    data = {
        "nodes": formatted_nodes,
        "identifier": identifier
    }

    # Sends the nodes to the drugstone API
    # and receives an extended list with the internal IDs.
    extended_node_ids = requests.post(
        Url.MAP_NODES,
        verify=False,
        json=data
    )

    internal_ids = []
    for n in extended_node_ids.json():
        if "netexId" in n:
            internal_ids.append(n["netexId"])

    return internal_ids


def get_default_identifier() -> str:
    parameters = normalize_task_parameter({}, [])
    return parameters["parameters"]["config"]["identifier"]
