import requests
from .constants.url import Url


def request_task_info(token: str) -> dict:
    return requests.get(
        Url.TASK + "?token=" + token,
        verify=False).json()["info"]
