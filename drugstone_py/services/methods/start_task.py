import requests
from services.methods.constants.url import Url

"""
Starts a task and returns the token for it.
If there is no token for any reason, an empty str gets returned.
Parameters:
    * ids: list of node ids
    * algorithm: defaults to 'trustrank'
    * ppi: defaults to 'STRING'
    * pdi: defaults to 'drugbank'
    * identifier: defaults to 'symbol'
    * max_deg: defaults to 'None'
    * include_indirect_drugs: defaults to 'None'
    * hub_penalty: defaults to 'None'
    * result_size: defaults to 'None'
    * include_non_approved_drugs: defaults to 'None'
    * filter_paths: defaults to 'None'
    * damping_factor: defaults to 'None'
    * num_trees: defaults to 'None'
    * tolerance: defaults to 'None'
    * k: defaults to 'None'
    * target: defaults to 'drug-target'
"""
def start_task(
    ids: list, 
    algorithm:str, 
    ppi:str, 
    pdi:str, 
    identifier:str,  
    max_deg:int, 
    include_indirect_drugs:bool,
    hub_penalty: int,
    result_size: int,
    include_non_approved_drugs:bool,
    filter_paths: bool,
    damping_factor:float,
    num_trees: int,
    tolerance: int,
    k: int,
    target:str) -> str:

    data = {
        "algorithm": algorithm, 
        "parameters": {
            "ppi_dataset": ppi, 
            "pdi_dataset": pdi, 
            "input_network": {"nodes": [], "edges": []},
            "config": {"identifier": identifier},
            "seeds": ids
        }, 
        "target": target, 
    }

    if max_deg is not None:
        data["parameters"]["max_deg"] = max_deg

    if include_indirect_drugs is not None:
        data["parameters"]["include_indirect_drugs"] = include_indirect_drugs
    
    if hub_penalty is not None:
        data["parameters"]["hub_penalty"] = hub_penalty

    if result_size is not None:
        data["parameters"]["result_size"] = result_size
    
    if include_non_approved_drugs is not None:
        data["parameters"]["include_non_approved_drugs"] = include_non_approved_drugs
    
    if filter_paths is not None:
        data["parameters"]["filter_paths"] = filter_paths

    if algorithm == "trustrank" and damping_factor is not None:
        data["parameters"]["damping_factor"] = damping_factor
    
    if algorithm == "multisteiner" and num_trees is not None:
        data["parameters"]["num_trees"] = num_trees

    if algorithm == "multisteiner" and tolerance is not None:
        data["parameters"]["tolerance"] = tolerance
    
    if algorithm == "keypathwayminer" and k is not None:
        data["parameters"]["k"] = k
    
    start_task_response = requests.post(
        Url.TASK,
        verify=False, 
        json=data
        )
    token_obj = start_task_response.json()

    return token_obj.get("token", "")