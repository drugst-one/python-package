"""
drugstone.scripts.start_task

This module implements the start_task function.

:copyright: 2022 Institute for Computational Systems Biology by Prof. Dr. Jan Baumbach
:author: Ugur Turhan
"""

import requests
from .constants.url import Url


def start_task(params: dict) -> str:
    """Starts a task and returns the token for it.

    If there is no token for any reason, an empty str gets returned.
    """

    start_task_response = requests.post(
        Url.TASK,
        verify=False,
        json=params
    )

    token_obj = start_task_response.json()

    return token_obj.get("token", "")
