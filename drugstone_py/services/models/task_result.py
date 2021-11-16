from pathlib import Path
import json
import os

class TaskResult():
    
    def __init__(self, result: dict) -> None:
        self.result = result

    def get_dict(self) -> dict:
        return self.result

    def get_file(self) -> None:
        downloads_path = str(Path.home() / "Downloads/result.json")
        path_exists = os.path.exists(downloads_path)
        iterations = 1
        while path_exists:
            if not downloads_path.endswith(").json"):
                downloads_path = downloads_path[:len(downloads_path)-5] + "(1).json"
            else:
                downloads_path = downloads_path[:len(downloads_path)-7] + str(iterations) + ").json"
                iterations = iterations + 1
            path_exists = os.path.exists(downloads_path)

        with open(downloads_path, "x") as f:
            json.dump(self.result, f, indent=4)