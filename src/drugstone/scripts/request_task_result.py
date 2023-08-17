"""
drugstone.scripts.request_task_result

This module implements the request_task_result function.

:copyright: 2022 Institute for Computational Systems Biology by Prof. Dr. Jan Baumbach
:author: Ugur Turhan
"""

import requests
from .constants.url import Url


def request_task_result(token: str) -> dict:
    """Returns the raw task result."""

    url_parameter = "?view=&fmt=&token=" + token
    return requests.get(
        Url.TASK_RESULTS + url_parameter,
        verify=False
    ).json()
