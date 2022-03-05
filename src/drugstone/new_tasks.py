
from typing import Union, List
from .task.tasks import Tasks
from .new_task import new_task


def new_tasks(seeds: list, params: Union[dict, List[dict]] = dict({})) -> Tasks:
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
                t = new_task(seeds, t_param)
                tasks.append(t)
            return Tasks(tasks)
    elif isinstance(params, list):
        tasks = []
        for p in params:
            t = new_task(seeds, p)
            tasks.append(t)
        return Tasks(tasks)
    return Tasks([new_task(seeds, params)])
