"""
drugstone.scripts.request_task_info

This module implements the request_task_info function.

:copyright: 2024 Institute for Computational Systems Biology by Prof. Dr. Jan Baumbach
 
"""

import requests
from .constants.url import api


def request_task_info(token: str) -> dict:
    return requests.get(
        api.TASK + "?token=" + token,
        verify=False).json()["info"]
