"""
drugstone

The python package for the https://drugst.one/ platform.
This package offers tools for drug-repurposing.
This is a programmatic approach to the functionality of the web portal.
For more information visit: https://drugst.one/

:copyright: 2022 Institute for Computational Systems Biology by Prof. Dr. Jan Baumbach
:author: Ugur Turhan
"""

import urllib3
import logging

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.getLogger().setLevel(logging.INFO)


from .new_task import new_task
from .new_tasks import new_tasks
from .deep_search import deep_search
from .static_task import static_task
from .static_tasks import static_tasks
from .task.models.drug import Drug
from .task.models.gene import Gene
