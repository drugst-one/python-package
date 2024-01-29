"""
drugstone.task.scripts.create_path

This module defines the create_path function.

:copyright: 2024 Institute for Computational Systems Biology by Prof. Dr. Jan Baumbach
 
"""

import os


def create_path(path: str, name: str, file_type: str) -> str:
    """Concatenates a path with a filename and a filetype.

    :param str path: A path.
    :param str name: A filename.
    :param str file_type: A filetype.
    :return: str: Resulting path.
    """
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
