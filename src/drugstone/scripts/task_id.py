"""
drugstone.scripts.task_id

This module implements the class TaskId.

:copyright: 2024 Institute for Computational Systems Biology by Prof. Dr. Jan Baumbach
 
"""


class TaskId:
    """Creates unique ids.

    The ids are just integers, starting with 1 and counting up.
    """

    __u_id = 0

    @classmethod
    def get(cls) -> str:
        cls.__u_id += 1
        return str(cls.__u_id)
