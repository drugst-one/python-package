from typing import Dict
from task.scripts.constants.task_parameter import TaskParameter


def normalize_task_parameter(user_params: dict, seeds: list) -> dict:
    """Normalizes the parameter dictionary from the user."""

    normalized_params: Dict[str, any] = {
        "algorithm": "trustrank",
        "target": "drug",
        "parameters": {
            "target": "drug",
            "ppi_dataset": "STRING",
            "pdi_dataset": "drugbank",
            "config": {"identifier": "symbol"},
        }
    }

    for key, value in user_params.items():
        if key == "algorithm" and hasattr(TaskParameter.AlgorithmValues, str(value).upper()):
            normalized_params[key] = value
        elif key == "target" and hasattr(TaskParameter.TargetValues, str(value).upper()):
            normalized_params[key] = value
            normalized_params["parameters"][key] = value
        elif key == "identifier" and hasattr(TaskParameter.IdentifierValues, str(value).upper()):
            normalized_params["parameters"]["config"]["identifier"] = value
        elif key == "config" and type(value) is dict and type(dict(value).get("identifier", None)) is str:
            normalized_params["parameters"]["config"]["identifier"] = value["identifier"]
        else:
            normalized_params["parameters"][key] = value

    if (normalized_params["algorithm"] == "keypathwayminer"
            and "k" not in normalized_params["parameters"]):
        normalized_params["parameters"]["k"] = 5
    normalized_params["parameters"]["seeds"] = seeds
    normalized_params["parameters"]["input_network"] = {"nodes": [], "edges": []}

    return normalized_params
