"""
drugstone.scripts.request_task_info

This module implements the request_task_info function.

:copyright: 2022 Institute for Computational Systems Biology by Prof. Dr. Jan Baumbach
:author: Ugur Turhan
"""

import requests
from .constants.url import Url


def request_task_info(token: str) -> dict:
    return requests.get(
        Url.TASK + "?token=" + token,
        verify=False).json()["info"]
