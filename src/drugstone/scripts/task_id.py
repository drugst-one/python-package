"""
drugstone.scripts.task_id

This module implements the class TaskId.

:copyright: 2022 Institute for Computational Systems Biology by Prof. Dr. Jan Baumbach
:author: Ugur Turhan
"""

import random
import string


class TaskId:
    """Creates unique ids and memorizes them in '__ids'."""

    __ids = []

    @classmethod
    def get(cls, pre: str, length: int) -> str:
        chars = string.ascii_letters + string.digits
        t_id = pre + "-" + "".join(random.choice(chars) for _ in range(length))
        while t_id in cls.__ids:
            t_id = pre + "-" + "".join(random.choice(chars) for _ in range(length))
        cls.__ids.append(t_id)
        return t_id
