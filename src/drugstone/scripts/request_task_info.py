"""
drugstone.scripts.request_task_info

This module implements the request_task_info function.

:copyright: 2024 Institute for Computational Systems Biology by Prof. Dr. Jan Baumbach
 
"""

import requests
from .constants.url import api
import logging
import time

def request_task_info(token: str) -> dict:
    for _ in range(3):
        # 3 attempts due to possible connection issues
        try:
            return requests.get(
                api.TASK + "?token=" + token,
                verify=False).json()["info"]
        except Exception as e:
            logging.warning('ConnectionError occurred. Retrying...')
            time.sleep(2)
            pass