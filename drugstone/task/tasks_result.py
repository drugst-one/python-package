from task.task import Task
from task.scripts.download_json import download_json
from task.scripts.make_upsetplot import make_upset_plot


class TasksResult:

    def __init__(self, tasks: list[Task] = []) -> None:
        self.__tasks = tasks

    def get_tasks_list(self) -> list[Task]:
        return self.__tasks

    def to_dict(self) -> dict:
        d = {}
        counter = 0
        for t in self.__tasks:
            d[counter] = {
                "info": t.get_info(),
                "parameters": t.get_parameters(),
                "results": t.get_result().to_dict()
            }
            counter += 1
        return d

    def download_json(self, path: str, name: str = "result"):
        """Downloads a json file with the results to the given folder."""
        download_json(data=self.to_dict(), path=path, name=name)

    def create_upsetplot(self):
        make_upset_plot()
