"""
drugstone.task.models.drug

This module implements the class Drug for the drugstone API.

:copyright: 2024 Institute for Computational Systems Biology by Prof. Dr. Jan Baumbach
 
"""


class Drug:

    def __init__(self,
                 label: str = None,
                 drug_id: str = None,
                 status: str = None):
        self.__label = label
        self.__drug_id = drug_id
        self.__status = status

    def to_dict(self):
        return {
            self.__label: {
                "label": self.__label,
                "drugId": self.__drug_id,
                "status": self.__status,
            }
        }
