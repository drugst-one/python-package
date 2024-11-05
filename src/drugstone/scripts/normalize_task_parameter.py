"""
drugstone.scripts.normalize_task_parameter

This module implements the normalize_task_parameter function.

:copyright: 2024 Institute for Computational Systems Biology by Prof. Dr. Jan Baumbach
 
"""


import warnings
from typing import Dict
from .task_id import TaskId
from .constants.task_parameter import TaskParameter
from ..license import license
import copy

def normalize_task_parameter(user_params: dict, seeds: list) -> dict:
    """Normalizes the parameter dictionary from the user."""
    # default parameters
    normalized_params: Dict[str, any] = {
        "algorithm": "trustrank",
        "target": "drug",
        "parameters": {
            "target": "drug",
            "ppiDataset": "nedrex",
            "pdiDataset": "nedrex",
            "licenced": license.accepted,
            "resultSize": 20,
            "config": {"identifier": "symbol"},
        }
    }

    for key, value in user_params.items():
        if key == "algorithm" or key == "algorithms":
            if value in TaskParameter.AlgorithmValues.ALGORITHM_VALUES:
                normalized_params["algorithm"] = value
            else:
                warnings.warn(str(value) + "-algorithm is not known to Drugstone!"
                              + " The algorithm is changed to "
                              + normalized_params["algorithm"] + "!    ")
        elif key == "target":
            if value in TaskParameter.TargetValues.TARGET_VALUES:
                normalized_params["target"] = value
                normalized_params["parameters"]["target"] = value
            else:
                warnings.warn("The target: " + str(value) + " is not known to Drugstone!"
                              + " The target is changed to "
                              + normalized_params["target"] + "!    ")
        elif key == "identifier":
            if value in TaskParameter.IdentifierValues.IDENTIFIER_VALUES:
                normalized_params["parameters"]["config"]["identifier"] = value
            else:
                warnings.warn("The identifier: " + str(value) + " is not known to Drugstone!"
                              + " The identifier is changed to "
                              + normalized_params["parameters"]["config"]["identifier"] + "!    ")
        elif key == "ppiDataset":
            if value.lower() in TaskParameter.PpiValues.PPI_VALUES:
                normalized_params["parameters"]["ppiDataset"] = value
            else:
                warnings.warn("The PPI-dataset: " + str(value) + " is not known to Drugstone!"
                              + " The PPI-dataset is changed to "
                              + normalized_params["parameters"]["ppiDataset"] + "!    ")
        elif key == "pdiDataset":
            if value.lower() in TaskParameter.PdiValues.PDI_VALUES:
                normalized_params["parameters"]["pdiDataset"] = value
            else:
                warnings.warn("The PDI-dataset: " + str(value) + " is not known to Drugstone!"
                              + " The PDI-dataset is changed to "
                              + normalized_params["parameters"]["pdiDataset"] + "!    ")
        elif key == "resultSize":
            if isinstance(value, int):
                normalized_params["parameters"]["resultSize"] = value
            else:
                warnings.warn("Invalid result_size: " + str(value) + ", has to be an integer!"
                              + " The result_size is changed to "
                              + str(normalized_params["parameters"]["resultSize"]) + "!    ")
        else:
            normalized_params["parameters"][key] = value

    if normalized_params["algorithm"] == "keypathwayminer" and "k" not in normalized_params["parameters"]:
        normalized_params["parameters"]["k"] = 5
    if normalized_params["target"] == "drug-target" and normalized_params["algorithm"] == "proximity":
        warnings.warn("Network Proximity is not capable of Drug-Target-Search!"
                      + " Algorithm is changed to TrustRank.    ")
        normalized_params["algorithm"] = "trustrank"
    if normalized_params["target"] == "drug-target" and normalized_params["algorithm"] == "adjacentDrugs":
        warnings.warn("First neighbour drugs is not capable of Drug-Target-Search!"
                      + " Target is changed to 'drug'.")
        normalized_params["target"] = "drug"

    normalized_params["parameters"]["seeds"] = seeds
    normalized_params["parameters"]["input_network"] = {"nodes": [], "edges": []}
    if "custom_edges" in normalized_params["parameters"]:
        # move custom_edges to input_network to support old parameter structure
        normalized_params["parameters"]["input_network"]["edges"] = copy.deepcopy(normalized_params["parameters"]["custom_edges"])
        normalized_params["parameters"]["custom_edges"] = True
        
    alg = normalized_params["algorithm"]
    if "has_duplicate_algorithms" in user_params:
        if user_params["has_duplicate_algorithms"]:
            task_id = alg + "-" + TaskId.get()
            normalized_params["parameters"]["task_id"] = task_id
        else:
            normalized_params["parameters"]["task_id"] = alg
    else:
        normalized_params["parameters"]["task_id"] = alg
        
    print('normalized_params', normalized_params)
    return normalized_params
