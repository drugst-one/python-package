import requests
import time
from services.methods.map_nodes_to_internal_ids import map_nodes_to_internal_ids
from services.methods.start_task import start_task
from services.methods.constants.url import Url
from services.methods.constants.task_parameters import TaskParameters
from services.models.task_result import TaskResult
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Task:

    # The token gets assigned by the start_task function.
    __token = ""

    # General parameters for the task, with their default value.
    # Can be updated with the corresponding setter function.
    __identifier = "symbol"
    __algorithm = "trustrank"
    __ppi = "STRING"
    __pdi = "drugbank"
    __target = "drug-target"
    __max_deg = None
    __include_indirect_drugs = None
    __hub_penalty = None
    __result_size = None
    __include_non_approved_drugs = None
    __filter_paths = None

    # Spezial parameter for the trustrank algorithm, with its default value.
    # Can be updated with the corresponding setter function.
    __damping_factor = None

    # Spezial parameters for the multi steiner algorithm, with their default value.
    # Can be updated with the corresponding setter function.
    __num_trees = None
    __tolerance = None

    # Spezial parameter for the keypathwayminer algorithm, with its default value.
    # Can be updated with the corresponding setter function.
    __k = None


    """
    Mapps the nodes to the internal IDS
    and starts a task.
    """
    def start_task(self, nodes: list):
        internal_ids = map_nodes_to_internal_ids(nodes, self.__identifier)
        self.__token = start_task(
            ids=internal_ids, 
            algorithm = self.__algorithm, 
            ppi = self.__ppi, 
            pdi = self.__pdi, 
            identifier = self.__identifier, 
            max_deg = self.__max_deg, 
            include_indirect_drugs = self.__include_indirect_drugs,
            hub_penalty = self.__hub_penalty,
            result_size = self.__result_size,
            include_non_approved_drugs = self.__include_non_approved_drugs,
            filter_paths = self.__filter_paths,
            damping_factor = self.__damping_factor, 
            num_trees = self.__num_trees,
            tolerance = self.__tolerance,
            k = self.__k,
            target = self.__target)


    """
    Returns True, only if a task has a status of 'Done.'
    and False if the task has failed or there is no token.
    Waits for the task to be done or failed.
    """
    def __task_is_done(self) -> bool:
        if len(self.__token) == 0:
            print("You have to start a task first.")
            return False
        else: 
            task_obj = None
            task_status = ""
            while task_status != "Done.":
                time.sleep(1)
                task_response = requests.get(
                    Url.TASK + "?token=" + self.__token,
                    headers={ 'Content-Type': 'application/json' }, 
                    verify=False
                    )
                task_obj = task_response.json()
                task_info = task_obj.get("info")
                task_status = task_info.get("status", "")
                task_failed = task_info.get("failed")
                if task_failed:
                    return False
            return True
    

    """
    Returns a dictionary with the task result.
    """
    def get_result(self) -> TaskResult:
        if self.__task_is_done():
            view =  ""
            fmt = "csv"
            url_parameter = "?view=" + view + "&fmt=" + fmt + "&token=" + self.__token

            task_result_response = requests.get(
                        Url.TASK_RESULTS + url_parameter,
                        headers={ 'Content-Type': 'application/json' }, 
                        verify=False
                        )

            task_result_dict = task_result_response.json()
            return TaskResult(task_result_dict)
        else:
            print("Task was not done.")


    # Collection of setters, to set the parameters for the task.
    # The parameters have to be set, before the task is startet.
    def set_identifier(self, value: str) -> None:
        if value in TaskParameters.IDENTIFIER:
            self.__identifier = value

    def set_algorithm(self, value: str) -> None:
        if value in TaskParameters.ALGORITHM:
            self.__algorithm = value

    def set_ppi(self, value: str) -> None:
        if value in TaskParameters.PPI:
            self.__ppi = value
    
    def set_pdi(self, value: str) -> None:
        if value in TaskParameters.PDI:
            self.__pdi = value

    def set_max_deg(self, value: int) -> None:
        if type(value) is int and value >= 0:
            self.__max_deg = value

    def set_target(self, value: str) -> None:
        if value in TaskParameters.TARGET:
            self.__target = value

    def set_include_indirect_drugs(self, value:bool) -> None:
        if type(value) is bool:
            self.__include_indirect_drugs = value
    
    def set_hub_penalty(self, value:int) -> None:
        if type(value) is int and value >= 0:
            self.__hub_penalty = value
    
    def set_result_size(self, value:int) -> None:
        if type(value) is int and value >= 0:
            self.__result_size = value
    
    def set_include_non_approved_drugs(self, value:bool) -> None:
        if type(value) is bool:
            self.__include_non_approved_drugs = value

    def set_filter_paths(self, value: bool) -> None:
        if type(value) is bool:
            self.__filter_paths = value

    def set_damping_factor(self, value: float) -> None:
        if type(value) is float and value >= 0:
            self.__damping_factor = value
    
    def set_num_trees(self, value:int) -> None:
        if type(value) is int and value >= 0:
            self.__num_trees = value
    
    def set_tolerance(self, value:int) -> None:
        if type(value) is int and value >= 0:
            self.__tolerance = value

    def set_k(self, value:int) -> None:
        if type(value) is int and value >= 0:
            self.__k = value