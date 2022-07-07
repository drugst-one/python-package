"""
drugstone.scripts.constants.url

This module implements the class Url.

:copyright: 2022 Institute for Computational Systems Biology by Prof. Dr. Jan Baumbach
:author: Ugur Turhan
"""


class Url:
    BASE = "https://api.drugst.one/"
    # BASE = "localhost:8001/"
    MAP_NODES = BASE + "map_nodes/"
    TASK = BASE + "task/"
    TASKS = BASE + "tasks/"
    TASK_RESULTS = BASE + "task_result/"
    FETCH_EDGES = BASE + "fetch_edges/"
