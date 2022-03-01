import requests
from task.scripts.constants.url import Url
from task.scripts.task_scripts.check_result_size import check_result_size
from task.scripts.task_scripts.normalize_nodes import normalize_nodes


def request_task_result(token: str, params: dict) -> dict:
    """Returns a normalized dict of the results.

    result = {drugs: {}, genes: {}}

    Parameters
    ----------
    token: str
    params: dict

    Returns
    -------

    """
    url_parameter = "?view=&fmt=&token=" + token
    result = requests.get(
        Url.TASK_RESULTS + url_parameter,
        verify=False
    ).json()
    result = normalize_nodes(result)
    result = check_result_size(result, params)
    return result
