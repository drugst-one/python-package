import requests
import time
import urllib3
import logging
import warnings
from task.scripts.map_nodes_to_internal_ids import map_nodes_to_internal_ids
from task.scripts.start_task import start_task
from task.scripts.constants.url import Url
from task.scripts.constants.task_parameter import TaskParameter
from task.task_result import TaskResult

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.getLogger().setLevel(logging.INFO)


class Task:

    def __init__(self) -> None:
        # The token and the task_name are assigned by the start_task function.
        self.__token: str = ""
        self.task_name: str = ""

    def initiate_new_task(self, seeds: list, params: dict, name: str):
        """
        Mapps the nodes to the internal IDs
        and starts a task.
        """

        # sets the task name 
        self.task_name = name
        
        # looks whether there is an identifier in the params 
        # or else gets the default identifier  
        map_nodes_identifier: str
        if "identifier" in params and hasattr(TaskParameter.IdentifierValues, params["identifier"].upper()):
            map_nodes_identifier = params["identifier"]
        else:
            map_nodes_identifier = self.__normalize_task_parameter({}, [])["parameters"]["config"]["identifier"]
        
        # gets the internal ids for the nodes 
        internal_ids = map_nodes_to_internal_ids(seeds, map_nodes_identifier)

        # calls the start_task function, which starts the task and returns the token 
        # sets the token
        normalized_params = self.__normalize_task_parameter(params, internal_ids)
        self.__token = start_task(normalized_params)

    def get_info(self) -> dict:
        if len(self.__token) == 0:
            warnings.warn("No token. You have to start a task first.")
            return {}
        else: 
            return requests.get(
                Url.TASK + "?token=" + self.__token,
                verify=False).json()["info"]

    def get_progress(self) -> str:
        f_progress = int(self.get_info()["progress"]) * 100
        return str(f_progress) + "%"

    def get_status(self) -> str:
        return self.get_info()["status"]

    def is_done(self) -> bool:
        return self.get_info()["done"]

    def is_failed(self) -> bool:
        return self.get_info()["failed"]

    def wait_for_task_to_finish(self) -> bool:
        while not self.is_done() and not self.is_failed():
            time.sleep(1)
            logging.info(self.task_name + " progress is at: " + str(self.get_progress()))
        if self.is_done():
            logging.info(self.task_name + " is done.")
            return True
        elif self.is_failed():
            warnings.warn(self.task_name + " has failed!")
        return False

    def get_result(self) -> TaskResult:
        if self.wait_for_task_to_finish():
            url_parameter = "?view=&fmt=&token=" + self.__token
            task_result_response = requests.get(
                        Url.TASK_RESULTS + url_parameter, 
                        verify=False
                        )
            return TaskResult(task_result_response.json())
        else:
            return {}

    @staticmethod
    def __normalize_task_parameter(user_params: dict, seeds: list) -> dict:
        """Normalizes the parameter dictionary from the user."""

        normalized_params = {
            "algorithm": "trustrank", 
            "target": "drug",
            "parameters": {
                "target": "drug",
                "ppi_dataset": "STRING", 
                "pdi_dataset": "drugbank",
                "config": {"identifier": "symbol"},
            }
        }

        for key, value in user_params.items():
            if key == "algorithm" and hasattr(TaskParameter.AlgorithmValues, str(value).upper()):
                normalized_params[key] = value
            elif key == "target" and hasattr(TaskParameter.TargetValues, str(value).upper()):
                normalized_params[key] = value
                normalized_params["parameters"][key] = value
            elif key == "identifier" and hasattr(TaskParameter.IdentifierValues, str(value).upper()):
                normalized_params["parameters"]["config"]["identifier"] = value
            elif key == "config" and type(value) is dict and type(dict(value).get("identifier", None)) is str:
                normalized_params["parameters"]["config"]["identifier"] = value["identifier"]
            else:
                normalized_params["parameters"][key] = value

        if (normalized_params["algorithm"] == "keypathwayminer"
                and "k" not in normalized_params["parameters"]):
            normalized_params["parameters"]["k"] = 5
        normalized_params["parameters"]["seeds"] = seeds
        normalized_params["parameters"]["input_network"] = {"nodes": [], "edges": []}

        return normalized_params