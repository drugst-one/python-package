from src.drugstone.task.task import Task
from src.drugstone.task.task_result import TaskResult
from src.drugstone.task.tasks_result import TasksResult


class Tasks:

    def __init__(self, tasks: list[Task] = []) -> None:
        self.__tasks = tasks

    def get_result(self) -> TasksResult:
        return TasksResult(self.__tasks)

    def get_union(self) -> TaskResult:
        drugs = {}
        genes = {}
        for t in self.__tasks:
            r = t.get_result()
            drugs = {**drugs, **r.get_drugs()}
            r_genes = r.get_genes()
            for gene, detail in r_genes.items():
                if gene not in genes:
                    genes = {**genes, gene: detail}
                else:
                    edges_a = genes[gene]["has_edges_to"]
                    edges_b = detail["has_edges_to"]
                    new_edges = list(set(edges_a + edges_b))
                    genes[gene]["has_edges_to"] = new_edges
        for d in drugs:
            drugs[d].pop("score")
        for g in genes:
            genes[g].pop("score")
        return TaskResult(drugs=drugs, genes=genes)

    def get_intersection(self) -> TaskResult:
        drugs = {}
        genes = {}
        first = True
        for t in self.__tasks:
            r = t.get_result()
            if first:
                drugs = r.get_drugs()
                genes = r.get_genes()
                first = False
            else:
                drugs = {d: drugs[d] for d in drugs if d in r.get_drugs()}
                genes_intersection = {}
                for gene, detail in r.get_genes().items():
                    if gene in genes:
                        genes_intersection = {**genes_intersection, gene: detail}
                        edges_a = genes[gene]["has_edges_to"]
                        edges_b = detail["has_edges_to"]
                        new_edges = list(set(edges_a) & set(edges_b))
                        genes_intersection[gene]["has_edges_to"] = new_edges
                genes = genes_intersection.copy()
        for d in drugs:
            drugs[d].pop("score")
        for g in genes:
            genes[g].pop("score")
        return TaskResult(drugs=drugs, genes=genes)
