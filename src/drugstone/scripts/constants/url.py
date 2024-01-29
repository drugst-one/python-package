"""
drugstone.scripts.constants.url

This module implements the class Url.

:copyright: 2024 Institute for Computational Systems Biology by Prof. Dr. Jan Baumbach
 
"""


class Url:
    
    def __init__(self, url="https://api.drugst.one/") -> None:
        self.set_api(url)
        
    def set_api(self, base_url: str):
        self.BASE = base_url
        self.MAP_NODES =  self.BASE + "map_nodes/"
        self.TASK =  self.BASE + "task/"
        self.TASKS = self.BASE + "tasks/"
        self.TASK_RESULTS =  self.BASE + "task_result/"
        self.FETCH_EDGES = self.BASE + "fetch_edges/"
        
api = Url()

def set_api(base_url: str):
    global api
    api.set_api(base_url)
