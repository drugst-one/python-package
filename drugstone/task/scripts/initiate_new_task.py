from task.scripts.constants.task_parameter import TaskParameter
from task.scripts.normalize_task_parameter import normalize_task_parameter
from task.scripts.map_nodes_to_internal_ids import map_nodes_to_internal_ids
from task.scripts.start_task import start_task


def initiate_new_task(seeds: list, params: dict) -> str:

    # looks whether there is an identifier in the params
    # or else gets the default identifier
    map_nodes_identifier: str
    if "identifier" in params and hasattr(
            TaskParameter.IdentifierValues,
            params["identifier"].upper()):
        map_nodes_identifier = params["identifier"]
    else:
        parameters = normalize_task_parameter({}, [])
        identifier = parameters["parameters"]["config"]["identifier"]
        map_nodes_identifier = identifier

    # gets the internal ids for the nodes
    internal_ids = map_nodes_to_internal_ids(seeds, map_nodes_identifier)

    # calls the start_task function, which starts the task and returns the token
    normalized_params = normalize_task_parameter(params, internal_ids)
    token = start_task(normalized_params)
    return token
