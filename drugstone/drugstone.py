import urllib3
import logging
from typing import Union
from task.task import Task
from task.tasks import Tasks
from task.task_result import TaskResult
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

    __number_of_tasks: int = 0

    def new_task(self, seeds: list, params: dict = dict({})) -> Task:
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
        """
        self.__number_of_tasks += 1
        token = initiate_new_task(seeds, params)
        return Task(token, self.__number_of_tasks)

    def new_tasks(self, seeds: list, params: Union[dict, list[dict]] = dict({})) -> Tasks:
        if isinstance(params, dict):
            algorithm = "algorithm"
            if "algorithm" in params:
                algorithm = params["algorithm"]
            elif "algorithms" in params:
                algorithm = params["algorithms"]
            if isinstance(algorithm, list):
                tasks = []
                for alg in algorithm:
                    t_param = {**params, "algorithm": alg}
                    t = self.new_task(seeds, t_param)
                    tasks.append(t)
                return Tasks(tasks)
        elif isinstance(params, list):
            tasks = []
            for p in params:
                t = self.new_task(seeds, p)
                tasks.append(t)
            return Tasks(tasks)
        return Tasks([self.new_task(seeds, params)])

    def deep_search(self, seeds: list, params: dict = dict({})) -> Task:
        # target search
        t_params = {**params, "target": "drug-target"}
        if "target_search" in params:
            t_params["algorithm"] = params["target_search"]
        t_search = self.new_task(seeds, t_params)
        targets = t_search.get_result().get_genes()

        # drug search
        d_params = {**params, "target": "drug"}
        if "drug_search" in params:
            d_params["algorithm"] = params["drug_search"]
        d_search = self.new_task(list(targets.keys()), d_params)
        return d_search
