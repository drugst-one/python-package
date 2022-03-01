import warnings
from task.scripts.normalize_task_parameter import normalize_task_parameter
from task.scripts.map_nodes_to_internal_ids import map_nodes_to_internal_ids
from task.scripts.start_task import start_task

identifier_values = ["symbol", "uniprot", "ensg"]


def initiate_new_task(seeds: list, params: dict) -> str:
    # looks whether there is an identifier in the params
    # or else gets the default identifier
    map_nodes_identifier: str
    if "identifier" in params:
        if params["identifier"] in identifier_values:
            map_nodes_identifier = params["identifier"]
        else:
            default_id = __get_default_identifier()
            map_nodes_identifier = default_id
            warnings.warn("The identifier: " + str(params["identifier"]) + "is not known to Drugstone!"
                          + " The identifier is changed to " + str(default_id) + "!")
    else:
        map_nodes_identifier = __get_default_identifier()

    # gets the internal ids for the nodes
    internal_ids = map_nodes_to_internal_ids(seeds, map_nodes_identifier)

    # calls the start_task function, which starts the task and returns the token
    normalized_params = normalize_task_parameter(params, internal_ids)
    token = start_task(normalized_params)
    return token


def __get_default_identifier() -> str:
    parameters = normalize_task_parameter({}, [])
    return parameters["parameters"]["config"]["identifier"]
