import requests
import time
import logging
import warnings
from task.task_result import TaskResult
from task.scripts.check_result_size import check_result_size
from task.scripts.normalize_nodes import normalize_nodes
from task.scripts.constants.url import Url


class Task:

    def __init__(self, token: str, number: int = None) -> None:
        # The order is important here!
        self.__token = token
        self.__number = number
        self.__info = self.__request_info()
        self.__parameters = self.__create_parameters()
        self.__wait_for_task_to_finish()

    def get_result(self) -> TaskResult:
        if self.is_done():
            result = self.__request__result()
            result = normalize_nodes(result)
            result = check_result_size(result, self.get_parameters())
            return TaskResult(drugs=result["drugs"], genes=result["genes"])
        else:
            return TaskResult()

    def get_info(self) -> dict:
        return self.__info

    def get_parameters(self) -> dict:
        return self.__parameters

    def get_algorithm(self) -> str:
        return self.__parameters["algorithm"]

    def get_progress(self) -> str:
        f_progress = int(self.__info["progress"]) * 100
        return str(f_progress) + "%"

    def get_status(self) -> str:
        return self.__info["status"]

    def is_done(self) -> bool:
        return self.__info["done"]

    def is_failed(self) -> bool:
        return self.__info["failed"]

    def __request_info(self) -> dict:
        return requests.get(
                Url.TASK + "?token=" + self.__token,
                verify=False).json()["info"]

    def __request__result(self) -> dict:
        url_parameter = "?view=&fmt=&token=" + self.__token
        return requests.get(
            Url.TASK_RESULTS + url_parameter,
            verify=False
        ).json()

    def __create_parameters(self) -> dict:
        t_alg = self.__info["algorithm"]
        param = self.__info["parameters"]
        param["algorithm"] = t_alg
        param.pop("inputNetwork")
        return param

    def __wait_for_task_to_finish(self) -> bool:
        name = self.get_algorithm()
        if self.__number is not None:
            name += "-" + str(self.__number)
        while not self.is_done() and not self.is_failed():
            logging.info(name + " progress is at: " + str(self.get_progress()))
            time.sleep(2)
            self.__info = self.__request_info()
        if self.is_done():
            logging.info(name + " is done.")
            return True
        elif self.is_failed():
            warnings.warn(name + " has failed!")
        return False
