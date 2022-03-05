import os


def create_path(path: str, name: str, file_type: str) -> str:
    f_type = "." + file_type
    n_path = os.path.join(path, name+f_type)
    path_exists = os.path.exists(n_path)
    iterations = 1
    while path_exists:
        if not n_path.endswith(")" + f_type):
            n_path = n_path[:len(n_path) - len(f_type)] + "(1)" + f_type
        else:
            n_path = n_path[:len(n_path) - len(f_type) - 2] + str(iterations) + ")" + f_type
            iterations += 1
        path_exists = os.path.exists(n_path)
    return n_path
