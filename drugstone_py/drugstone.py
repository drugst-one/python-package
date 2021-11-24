from services.task import Task
from services.methods.constants.task_parameter import TaskParameter

class Drugstone:

    def __init__(self) -> None:
        self.number_of_tasks = 1
    
    def new_task(self, nodes: list, params: dict={}, name:str=""):
        """Takes a list of nodes, a dict with parameters and a name for the task 
        and returns a task object with the running task."""

        name = name if name != "" else "Task" + str(self.number_of_tasks)
        t = Task()
        t.initiate_new_task(nodes=nodes, params=params, name=name)
        return t

    def get_task_parameters(self) -> TaskParameter:
        """Returns an object of task parameters."""
        
        return TaskParameter()