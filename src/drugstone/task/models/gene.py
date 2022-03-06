"""
drugstone.task.models.gene

This module implements the class Gene for the drugstone API.

:copyright: 2022 Institute for Computational Systems Biology by Prof. Dr. Jan Baumbach
:author: Ugur Turhan
"""

from typing import List


class Gene:

    def __init__(self,
                 symbol: str = None,
                 protein_name: str = None,
                 has_edges_to: List[str] = None,
                 uniprot_ac: str = None,
                 entrez: str = None,
                 ensg: List[str] = None):
        self.__symbol = symbol
        self.__protein_name = protein_name
        self.__uniprot_ac = uniprot_ac
        self.__entrez = entrez
        self.__ensg = ensg
        if has_edges_to is None:
            self.__has_edges_to = []
        else:
            self.__has_edges_to = has_edges_to

    def to_dict(self):
        return {
            self.__symbol: {
                "symbol": self.__symbol,
                "protein_name": self.__protein_name,
                "uniprot_ac": self.__uniprot_ac,
                "entrez": self.__entrez,
                "ensg": self.__ensg,
                "is_seed": False,
                "has_edges_to": self.__has_edges_to
            }
        }
