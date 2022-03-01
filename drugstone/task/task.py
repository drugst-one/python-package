from task.task_result import TaskResult


class Task:

    def __init__(self,
                 result: dict = None,
                 info: dict = dict({}),
                 params: dict = dict({})) -> None:
        self.__info = info
        self.__params = params
        if result is None:
            self.__result = dict({"drugs": {}, "genes": {}})
        else:
            self.__result = result

    @classmethod
    def import_data(cls) -> "Task":
        return cls()

    def get_result(self) -> TaskResult:
        return TaskResult(drugs=self.__result["drugs"],
                          genes=self.__result["genes"])

    def get_info(self) -> dict:
        return self.__info

    def get_parameters(self) -> dict:
        return self.__params
