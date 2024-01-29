"""
drugstone

The python package for the https://drugst.one/ platform.
This package offers tools for drug-repurposing.
This is a programmatic approach to the functionality of the web portal.
For more information visit: https://drugst.one/

:copyright: 2024 Institute for Computational Systems Biology by Prof. Dr. Jan Baumbach
 
"""

from .external_scripts.map_nodes_to_internal_ids import map_nodes_to_internal_ids as map_nodes
from .external_scripts.build_network import build_network
import urllib3
import logging

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.getLogger().setLevel(logging.INFO)


from .new_task import new_task
from .new_tasks import new_tasks
from .deep_search import deep_search
from .task.models.drug import Drug
from .task.models.gene import Gene
from . import fetching
from .license import print_license, accept_license, license
from .scripts.constants.url import set_api
