import requests
import time
from methods.map_nodes_to_internal_ids import map_nodes_to_internal_ids
from methods.start_task import start_task
from methods.constants.url import Url

class Task:

    # The token gets assigned by the start_task function.
    token = ""

    """
    Mapps the nodes to the internal IDS
    and starts a task.
    """
    def start_task(self, nodes: list):
        internal_ids = map_nodes_to_internal_ids(nodes)
        self.token = start_task(internal_ids)


    """
    Returns the task, if there is a token.
    """
    def get_task(self):
        if len(self.token) == 0:
            print("You have to start a task first.")
        else: 
            task_obj = None
            task_status = ""
            while task_status != "Done.":
                time.sleep(1)
                task_response = requests.get(
                    Url.TASK + "?token=" + self.token,
                    headers={ 'Content-Type': 'application/json' }, 
                    verify=False
                    )
                task_obj = task_response.json()
                task_info = task_obj.get("info")
                task_status = task_info.get("status", "")
            # print(task_obj)
    

    def get_task_results(self):

        view =  ""
        fmt = "csv"
        url_parameter = "?view=" + view + "&fmt=" + fmt + "&token=" + self.token

        task_results_response = requests.get(
                    Url.TASK_RESULTS + url_parameter,
                    headers={ 'Content-Type': 'application/json' }, 
                    verify=False
                    )

        print(task_results_response.text)