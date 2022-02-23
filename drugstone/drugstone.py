import urllib3
import logging
from task.task import Task
from task.scripts.make_upsetplot import make_upset_plot
from task.scripts.initiate_new_task import initiate_new_task

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.getLogger().setLevel(logging.INFO)


class Drugstone:
    """The starting point of the Drugstone package.

    Create a Drugstone Object to start tasks with it.

    For example:

    ds = Drugstone()

    task = ds.new_task(["BRCA1", "BRCA2"])

    Methods
    -------
    new_task(seeds: list, params:dict = {}, name:str = "") : Task
        Returns a task object with the running task.
    """

    __number_of_tasks: int = 1
    
    def new_task(self, seeds: list, params: dict = dict({}), name: str = "") -> Task:
        """Returns a task object with the running task.
        
        Initializes a new Task object 
        and initiates a new task on it.
        Returns the new task object with the running task.

        Parameters
        ----------
        seeds : list
            A list of seed nodes for the task.
        params : dict, optional
            A dict of parameters for the task.
            Default is an empty dict {}.
        name : str, optional
            A name for the task.
            Default is an empty string.
        """

        name = name if name != "" else "Task" + str(self.__number_of_tasks)
        self.__number_of_tasks += 1
        token = initiate_new_task(seeds=seeds, params=params)
        t = Task(name=name, token=token)
        return t

    def deep_search(self, seeds: list, params: dict = dict({}), name: str = "") -> Task:
        # target search
        t_search_name = self.__create_deep_search_name_for("target", name)
        t_search_params = self.__create_deep_search_parameters_for("drug-target", params)
        t_search = self.new_task(seeds, t_search_params, t_search_name)
        t_search_results = t_search.get_result()
        targets = t_search_results.get_genes()

        # drug search
        d_search_name = self.__create_deep_search_name_for("drug", name)
        d_search_params = self.__create_deep_search_parameters_for("drug", params)
        d_search = self.new_task(list(targets.keys()), d_search_params, d_search_name)
        return d_search

    def create_upsetplot(self):
        make_upset_plot()

    def __create_deep_search_parameters_for(self, target: str, params: dict) -> dict:
        params["target"] = target
        if target == "drug-target" and "target_search" in params:
            params["algorithm"] = params["target_search"]
        elif target == "drug" and "drug_search" in params:
            params["algorithm"] = params["drug_search"]
        else:
            params["algorithm"] = "trustrank"
        return params

    def __create_deep_search_name_for(self, target: str, name: str) -> str:
        if name == "":
            new_name = " DeepSearch-" + target + " " + str(self.__number_of_tasks)
        else:
            new_name = " " + name + "-" + target
        return new_name
