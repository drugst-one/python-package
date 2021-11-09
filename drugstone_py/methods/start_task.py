import requests
from data.url import Url

"""
Starts a task and returns the token for it.
If there is no token for any reason, an empty str gets returned.
"""
def start_task(ids: list) -> str:

    # algorithms: multisteiner, keypathwayminer, trustrank, closeness,degree, proximity, betweenness
    # ppi_dataset: STRING, BioGRID, APID
    # pdi_dataset: drugbank, chembl, dgidb
    data = {
        "algorithm": "trustrank", 
        "parameters": {"ppi_dataset": "STRING", "pdi_dataset": "drugbank", "seeds": ids}, 
        "target": "drug", 
    }

    start_task_response = requests.post(
        Url.TASK.value,
        verify=False, 
        json=data
        )
    token_obj = start_task_response.json()

    return token_obj.get("token", "")