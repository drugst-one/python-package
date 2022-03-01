import warnings
from typing import Dict

drug_target_search_values = ["multisteiner", "keypathwayminer", "trustrank",
                             "closeness", "degree", "betweenness"]
drug_search_values = ["trustrank", "closeness", "degree", "proximity"]
target_values = ["drug", "drug-target"]
identifier_values = ["symbol", "uniprot", "ensg"]
ppi_values = ["STRING", "BioGRID", "APID"]
pdi_values = ["drugbank", "chembl", "dgidb"]


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
            if value in drug_target_search_values or value in drug_search_values:
                normalized_params["algorithm"] = value
            else:
                warnings.warn(str(value) + "-algorithm is not known to Drugstone!"
                              + " The algorithm is changed to "
                              + normalized_params["algorithm"] + "!    ")
        elif key == "target":
            if value in target_values:
                normalized_params["target"] = value
                normalized_params["parameters"]["target"] = value
            else:
                warnings.warn("The target: " + str(value) + " is not known to Drugstone!"
                              + " The target is changed to "
                              + normalized_params["target"] + "!    ")
        elif key == "identifier":
            if value in identifier_values:
                normalized_params["parameters"]["config"]["identifier"] = value
            else:
                warnings.warn("The identifier: " + str(value) + " is not known to Drugstone!"
                              + " The identifier is changed to "
                              + normalized_params["parameters"]["config"]["identifier"] + "!    ")
        elif key == "ppi_dataset":
            if value in ppi_values:
                normalized_params["parameters"]["ppi_dataset"] = value
            else:
                warnings.warn("The PPI-dataset: " + str(value) + " is not known to Drugstone!"
                              + " The PPI-dataset is changed to "
                              + normalized_params["parameters"]["ppi_dataset"] + "!    ")
        elif key == "pdi_dataset":
            if value in pdi_values:
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

    return normalized_params
