
from .task.task import Task
from .new_task import new_task


def deep_search(seeds: list, params: dict = dict({})) -> Task:
    # target search
    t_params = {**params, "target": "drug-target"}
    if "target_search" in params:
        t_params["algorithm"] = params["target_search"]
    t_search = new_task(seeds, t_params)
    targets = t_search.get_result().get_genes()

    # drug search
    d_params = {**params, "target": "drug"}
    if "drug_search" in params:
        d_params["algorithm"] = params["drug_search"]
    d_search = new_task(list(targets.keys()), d_params)
    return d_search
