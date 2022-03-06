from typing import List
from .task.task import Task
from .task.models.drug import Drug
from .task.models.gene import Gene


def static_task(drugs: List[Drug] = list([]),
                genes: List[Gene] = list([])) -> Task:

    r_drugs = {}
    r_genes = {}
    for d in drugs:
        r_drugs = {**r_drugs, **d.to_dict()}
    for g in genes:
        r_genes = {**r_genes, **g.to_dict()}

    return Task({"drugs": r_drugs, "genes": r_genes})
