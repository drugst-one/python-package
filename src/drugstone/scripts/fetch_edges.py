"""
src.drugstone.scripts.fetch_edges

This module implements the fetch_edges function.

:copyright: 2022 Institute for Computational Systems Biology by Prof. Dr. Jan Baumbach
:author: Ugur Turhan
"""

import requests
from .constants.url import Url
from ..license import license


def fetch_edges(internal_ids: list, ppi_dataset: str):

    n_ids = []

    for i in internal_ids:
        n_ids.append({"drugstoneId": i})

    data = {
        "nodes": n_ids,
        "dataset": ppi_dataset,
        "licenced": license.accepted
    }
    edges = requests.post(
        Url.FETCH_EDGES,
        verify=False,
        json=data
    )
    return edges.json()
