from services.task import Task
from services.methods.constants.task_parameter import TaskParameter

class Drugstone:
    
    """
    Takes a list of nodes as a input parameter and starts a task mith the nodes.
    Returns the running task.
    """
    def new_task(self, nodes: list, params: dict):
        t = Task()
        t.initiate_new_task(nodes, params)
        return t

    """
    Returns an object of task parameters.
    """
    def get_task_parameters(self) -> TaskParameter:
        return TaskParameter()