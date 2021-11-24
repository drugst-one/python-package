import json
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

    def __init__(self) -> None:
        # The token and the task_name are assigned by the start_task function.
        self.token: str
        self.task_name: str

    
    def initiate_new_task(self, nodes: list, params: dict, name: str):
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
        internal_ids = map_nodes_to_internal_ids(nodes, map_nodes_identifier)

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
            logging.info(self.task_name + " progress is at: " + str(self.get_progress()))
        if self.is_done():
            logging.info(self.task_name + " is done.")
            return True
        elif self.is_failed():
            warnings.warn(self.task_name + " has failed!")
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
            logging.warning(self.task_name + " has failed!")
        else:
            logging.warning(
                self.task_name + 
                """ was not done! 
                Could not return the result dictionary! 
                Wait for the task to finish!"""
                )
            return {}
    

    def __normalize_task_parameter(self, user_params: dict, seeds: list) -> dict:
        """Normalizes the parameter dictionary from the user."""

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