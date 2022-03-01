from task.task import Task
from task.task_result import TaskResult
from task.tasks_result import TasksResult


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
        r_drugs = []
        r_genes = []
        for t in self.__tasks:
            r = t.get_result()
            r_drugs.append(r.get_drugs())
            r_genes.append(r.get_genes())
        return TaskResult(drugs=drugs, genes=genes)

    # if self.__is_wrapper:
    #     if self.__tasks:
    #         drugs = {}
    #         genes = {}
    #         for t in self.__tasks:
    #             r = t.get_result()
    #             drugs = {**drugs, **r.get_drugs()}
    #             genes = {**genes, **r.get_genes()}
    #         return TaskResult(drugs=drugs, genes=genes)
    #     else:
    #         return TaskResult()
