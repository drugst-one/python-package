import requests
from task.scripts.constants.url import Url

"""
Starts a task and returns the token for it.
If there is no token for any reason, an empty str gets returned.
"""
def start_task(params: dict) -> str:

    start_task_response = requests.post(
        Url.TASK,
        verify=False, 
        json=params
        )

    token_obj = start_task_response.json()

    return token_obj.get("token", "")