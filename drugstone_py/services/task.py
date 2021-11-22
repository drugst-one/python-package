import requests
import time
import urllib3
import logging
import warnings
from services.methods.map_nodes_to_internal_ids import map_nodes_to_internal_ids
from services.methods.start_task import start_task
from services.methods.constants.url import Url
from services.methods.constants.task_parameter import TaskParameter
from services.models.task_result import TaskResult

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.getLogger().setLevel(logging.INFO)

class Task:

    # The token gets assigned by the start_task function.
    __token = ""

    """
    Mapps the nodes to the internal IDS
    and starts a task.
    """
    def new_task(self, nodes: list, params: dict):
        map_nodes_identifier = ""
        if "identifier" in params and hasattr(TaskParameter.IdentifierValues, str(params["identifier"]).upper()):
            map_nodes_identifier = params["identifier"]
        else:
            map_nodes_identifier = self.__normalize_task_parameter({}, [])["parameters"]["config"]["identifier"]
        internal_ids = map_nodes_to_internal_ids(nodes, map_nodes_identifier)
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


    def get_progress(self) -> float:
        return self.get_info()["progress"]

    
    def get_status(self) -> str:
        return self.get_info()["status"]

    
    def is_done(self) -> bool:
        return self.get_info()["done"]

    
    def is_failed(self) -> bool:
        return self.get_info()["failed"]

    
    def wait_for_task_to_finish(self) -> bool:
        while not self.is_done() and not self.is_failed():
            time.sleep(1)
            logging.info("Task progress is at: " + str(self.get_progress()))
        if self.is_done():
            logging.info("The task is done.")
            return True
        elif self.is_failed():
            warnings.warn("The task is failed!")
            return False
        
    def get_result(self) -> TaskResult:
        if self.is_done():
            url_parameter = "?view=&fmt=&token=" + self.__token
            task_result_response = requests.get(
                        Url.TASK_RESULTS + url_parameter, 
                        verify=False
                        )
            return TaskResult(task_result_response.json())
        elif self.is_failed():
            logging.warning("The task failed!")
        else:
            logging.warning(
                """The task was not done! 
                Could not return the result dictionary! 
                Wait for the task to finish!"""
                )
            return {}
    
    """
    Normalizes the parameter dictionary from the user.
    """
    def __normalize_task_parameter(self, user_params: dict, seeds: list) -> dict:

        normalized_params = {
            "algorithm": "trustrank", 
            "target": "drug-target", 
            "parameters": {
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
            elif key == "identifier" and hasattr(TaskParameter.IdentifierValues, str(value).upper()):
                normalized_params["parameters"]["config"]["identifier"] = value
            elif key == "config" and type(value) is dict and type(dict(value).get("identifier", None)) is str:
                normalized_params["parameters"]["config"]["identifier"] = value["identifier"]
            else:
                normalized_params["parameters"][key] = value

        normalized_params["parameters"]["seeds"] = seeds
        normalized_params["parameters"]["input_network"] = {"nodes": [], "edges": []}

        return normalized_params