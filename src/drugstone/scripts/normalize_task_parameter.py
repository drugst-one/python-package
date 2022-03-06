"""
drugstone.scripts.normalize_task_parameter

This module implements the normalize_task_parameter function.

:copyright: 2022 Institute for Computational Systems Biology by Prof. Dr. Jan Baumbach
:author: Ugur Turhan
"""


import warnings
from typing import Dict
from .task_id import TaskId
from .constants.task_parameter import TaskParameter


def normalize_task_parameter(user_params: dict, seeds: list) -> dict:
    """Normalizes the parameter dictionary from the user."""

    normalized_params: Dict[str, any] = {
        "algorithm": "trustrank",
        "target": "drug",
        "parameters": {
            "target": "drug",
            "ppi_dataset": "STRING",
            "pdi_dataset": "drugbank",
            "result_size": 20,
            "config": {"identifier": "symbol"},
        }
    }

    for key, value in user_params.items():
        if key == "algorithm":
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
        elif key == "ppi_dataset":
            if value in TaskParameter.PpiValues.PPI_VALUES:
                normalized_params["parameters"]["ppi_dataset"] = value
            else:
                warnings.warn("The PPI-dataset: " + str(value) + " is not known to Drugstone!"
                              + " The PPI-dataset is changed to "
                              + normalized_params["parameters"]["ppi_dataset"] + "!    ")
        elif key == "pdi_dataset":
            if value in TaskParameter.PdiValues.PDI_VALUES:
                normalized_params["parameters"]["pdi_dataset"] = value
            else:
                warnings.warn("The PDI-dataset: " + str(value) + " is not known to Drugstone!"
                              + " The PDI-dataset is changed to "
                              + normalized_params["parameters"]["pdi_dataset"] + "!    ")
        elif key == "result_size":
            if isinstance(value, int):
                normalized_params["parameters"]["result_size"] = value
            else:
                warnings.warn("Invalid result_size: " + str(value) + ", has to be an integer!"
                              + " The result_size is changed to "
                              + str(normalized_params["parameters"]["result_size"]) + "!    ")
        else:
            normalized_params["parameters"][key] = value

    if normalized_params["algorithm"] == "keypathwayminer" and "k" not in normalized_params["parameters"]:
        normalized_params["parameters"]["k"] = 5
    if normalized_params["target"] == "drug-target" and normalized_params["algorithm"] == "proximity":
        warnings.warn("Network Proximity is not capable for Drug-Search!"
                      + " Drug-Search algorithm is changed to TrustRank!    ")
        normalized_params["algorithm"] = "trustrank"
    normalized_params["parameters"]["seeds"] = seeds
    normalized_params["parameters"]["input_network"] = {"nodes": [], "edges": []}
    alg = normalized_params["algorithm"]
    normalized_params["parameters"]["task_id"] = TaskId.get(alg, 4)

    return normalized_params
