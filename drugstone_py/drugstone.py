from services.task import Task

class Drugstone:
    
    """
    Takes a list of nodes as a input parameter and starts a task mith the nodes.
    Returns the running task.
    """
    def start_task(self, nodes: list):
        t = Task()
        t.start_task(nodes)
        return t