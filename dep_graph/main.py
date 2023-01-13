"""Contains the public API for generating and printing dependency graphs."""
import json
import os
import tempfile

from .algorithms.kahn import KahnAlgorithm
from .algorithms.simple import SimpleAlgorithm
from .graph import Graph


def _load_json(filename: str):
    """Loads json data from a file and returns it."""
    data = None
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def _create_temp_file(content):
    _, name = tempfile.mkstemp()
    with open(name, "w") as f:
        f.write(content)

    return name


def _delete_temp_file(filename):
    os.unlink(filename)


def generate_graph(filename: str, algorithm="simple") -> Graph:
    """Generates a graph from a file containing json data."""
    data = _load_json(filename)

    graph = None
    if algorithm == "simple":
        graph = SimpleAlgorithm.run(data)
    elif algorithm == "kahn":
        graph = KahnAlgorithm.run(data)
    else:
        raise Exception(f"No such algorithm: {algorithm}")
    return graph


def get_graph(content, algorithm="simple"):
    """Generates graphs based on Python dictionaries.

    Writes a Python dictionary describing a dependency graph onto a
    temporary file. The main algorithm is then run on the file and the
    file is deleted, yielding a correctly generated graph.
    """
    filename = _create_temp_file(json.dumps(content))
    graph = generate_graph(filename, algorithm)
    _delete_temp_file(filename)
    return graph
