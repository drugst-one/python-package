import requests
import warnings
from src.drugstone.task.scripts.constants.url import Url
from src.drugstone.task.scripts.constants.task_parameter import TaskParameter
from src.drugstone.task.scripts.task_scripts.normalize_task_parameter import normalize_task_parameter


def map_nodes_to_internal_ids(
        nodes: list,
        identifier: str = None,
        params: dict = dict({})) -> list:
    """
    Maps the given nodes to the internal IDs.
    Returns a list of the internal IDs for
    Parameters:
        * nodes: list of nodes
        * identifier: defaults to 'symbol'

    Parameters
    ----------
    nodes
    identifier
    params
    """

    if identifier is None:
        if "identifier" in params:
            if params["identifier"] in TaskParameter.IdentifierValues.IDENTIFIER_VALUES:
                identifier = params["identifier"]
            else:
                default_id = get_default_identifier()
                identifier = default_id
                warnings.warn("The identifier: " + str(params["identifier"])
                              + "is not known to Drugstone!"
                              + " The identifier is changed to "
                              + str(default_id) + "!")
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
