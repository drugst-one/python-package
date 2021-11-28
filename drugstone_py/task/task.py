import requests
import time
import urllib3
import logging
import warnings
from task.scripts.constants.url import Url
from task.task_result import TaskResult

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.getLogger().setLevel(logging.INFO)


class Task:

    def __init__(self, name: str, token: str) -> None:
        self.__task_name = name
        self.__token = token

    def get_result(self) -> TaskResult:
        if self.__wait_for_task_to_finish():
            url_parameter = "?view=&fmt=&token=" + self.__token
            task_result_response = requests.get(
                        Url.TASK_RESULTS + url_parameter,
                        verify=False
                        )
            return TaskResult(task_result_response.json())
        else:
            # TODO: add returning empty TaskResult
            return {}

    def get_info(self) -> dict:
        if len(self.__token) == 0:
            warnings.warn("No token. You have to start a task first.")
            return {}
        else: 
            return requests.get(
                Url.TASK + "?token=" + self.__token,
                verify=False).json()["info"]

    def get_progress(self) -> str:
        f_progress = int(self.get_info()["progress"]) * 100
        return str(f_progress) + "%"

    def get_status(self) -> str:
        return self.get_info()["status"]

    def is_done(self) -> bool:
        return self.get_info()["done"]

    def is_failed(self) -> bool:
        return self.get_info()["failed"]

    def __wait_for_task_to_finish(self) -> bool:
        while not self.is_done() and not self.is_failed():
            time.sleep(1)
            logging.info(self.__task_name + " progress is at: " + str(self.get_progress()))
        if self.is_done():
            logging.info(self.__task_name + " is done.")
            return True
        elif self.is_failed():
            warnings.warn(self.__task_name + " has failed!")
        return False
