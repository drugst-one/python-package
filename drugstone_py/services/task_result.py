class TaskResult():
    
    def __init__(self, result: dict) -> None:
        self.result = result

    def get_dict(self) -> dict:
        return self.result