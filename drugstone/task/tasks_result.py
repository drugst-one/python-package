import json
from typing import List
from .task import Task
from .scripts.create_path import create_path
from .scripts.make_upsetplot import make_upset_plot


class TasksResult:

    def __init__(self, tasks: List[Task] = []) -> None:
        self.__tasks = tasks

    def get_tasks_list(self) -> List[Task]:
        return self.__tasks

    def to_dict(self) -> dict:
        d = {}
        for t in self.__tasks:
            d[t.get_parameters()["taskId"]] = {
                "info": t.get_info(),
                "parameters": t.get_parameters(),
                "results": t.get_result().to_dict()
            }
        return d

    def download_json(self, path: str = "", name: str = "result"):
        """Downloads a json file with the results to the given folder."""
        path = create_path(path, name, "json")
        with open(path, "x") as f:
            json.dump(self.to_dict(), f, indent=4)

    def create_upsetplot(self):
        make_upset_plot(self.to_dict())
