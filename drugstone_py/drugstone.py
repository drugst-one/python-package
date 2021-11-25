from task.task import Task
from task.scripts.constants.task_parameter import TaskParameter


class Drugstone:
    """The starting point of the Drugstone package.

    Create a Drugstone Object to start tasks with it.
    
    For example: 
    ds = Drugstone()
    task = ds.new_task(["BRCA1", "BRCA2"])

    Attributes
    ----------
    __number_of_tasks : int
        The number of tasks the Drugstone object has started.

    Methods
    -------
    new_task(seeds: list, params:dict = {}, name:str = "") : Task
        Returns a task object with the running task.
    get_task_parameters() : TaskParameter
        Returns an TaskParameter object.
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

        t = Task()
        name = name if name != "" else "Task" + str(self.__number_of_tasks)
        t.initiate_new_task(seeds, params, name)
        return t

    @staticmethod
    def get_task_parameters() -> TaskParameter:
        """Returns an TaskParameter object."""
        return TaskParameter()
