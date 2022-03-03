from src.drugstone.task.drug import Drug
from src.drugstone.task.gene import Gene
from src.drugstone.task.task_result import TaskResult


class Task:

    def __init__(self,
                 result: dict = None,
                 info: dict = dict({}),
                 params: dict = dict({})) -> None:
        self.__info = info
        self.__params = params
        if result is None:
            self.__result = dict({"drugs": {}, "genes": {}})
        else:
            self.__result = result

    @classmethod
    def import_data(cls,
                    drugs: list[Drug] = list([]),
                    genes: list[Gene] = list([])) -> "Task":
        r_drugs = {}
        r_genes = {}
        for drug in drugs:
            r_drugs = {**r_drugs, **drug.to_dict()}
        for gene in genes:
            r_genes = {**r_genes, **gene.to_dict()}
        return cls(result={"drugs": r_drugs, "genes": r_genes})

    def get_result(self) -> TaskResult:
        return TaskResult(drugs=self.__result["drugs"],
                          genes=self.__result["genes"])

    def get_info(self) -> dict:
        return self.__info

    def get_parameters(self) -> dict:
        return self.__params
