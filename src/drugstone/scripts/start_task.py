import requests
from .constants.url import Url


def start_task(params: dict) -> str:
    """
    Starts a task and returns the token for it.
    If there is no token for any reason, an empty str gets returned.
    """

    start_task_response = requests.post(
        Url.TASK,
        verify=False,
        json=params
    )

    token_obj = start_task_response.json()

    return token_obj.get("token", "")
