"""
drugstone.scripts.request_task_result

This module implements the request_task_result function.

:copyright: 2022 Institute for Computational Systems Biology by Prof. Dr. Jan Baumbach
:author: Ugur Turhan
"""

import requests
from .constants.url import Url
from .check_result_size import check_result_size
from .normalize_nodes import normalize_nodes


def request_task_result(token: str, params: dict) -> dict:
    """Returns a normalized dict of the results.

    result = {drugs: {}, genes: {}}
    """
    url_parameter = "?view=&fmt=&token=" + token
    result = requests.get(
        Url.TASK_RESULTS + url_parameter,
        verify=False
    ).json()
    result = normalize_nodes(result)
    result = check_result_size(result, params)
    return result
