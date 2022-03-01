import json
import os


def download_json(path: str, data: dict = dict({}), name: str = "result") -> None:
    """Downloads a json file with the results to the given folder."""

    downloads_path = path + name + ".json"
    path_exists = os.path.exists(downloads_path)
    iterations = 1
    while path_exists:
        if not downloads_path.endswith(").json"):
            downloads_path = downloads_path[:len(downloads_path) - 5] + "(1).json"
        else:
            downloads_path = downloads_path[:len(downloads_path) - 7] + str(iterations) + ").json"
            iterations = iterations + 1
        path_exists = os.path.exists(downloads_path)

    with open(downloads_path, "x") as f:
        json.dump(data, f, indent=4)
