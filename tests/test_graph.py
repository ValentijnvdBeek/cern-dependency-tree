from itertools import chain
from pprint import pprint

import pytest

from .context import dep_graph

Edge = lambda x, y: dep_graph.Edge(Node(x), Node(y))
Node = dep_graph.Node
Graph = dep_graph.Graph
get_graph = dep_graph.get_graph


def test_node():
    node = Node("Hannover")
    assert (node.__repr__() == "Node(Hannover)")
    assert (node.__str__() == "[Hannover]")


def test_nodes():
    nodes = [Node("Delft"), Node("Amsterdam"), Node("Haarlem")]
    assert (
        nodes.__repr__() == "[Node(Delft), Node(Amsterdam), Node(Haarlem)]")
    assert ([x.__str__() for x in nodes
             ].__str__() == "['[Delft]', '[Amsterdam]', '[Haarlem]']")


def test_algorithm_nonexistent():
    with pytest.raises(Exception):
        get_graph({}, algorithm='P4')


def test_edge():
    edge = Edge("Hannover", "Delft")
    assert (edge.__repr__() == "Edge([Hannover], [Delft])")
    assert (edge.__str__() == "[Hannover] → [Delft]")


def test_graph():
    graph = Graph(["Hannover", "Delft"], [Edge("[Hannover]", "[Delft]")])
    assert (graph.__str__() ==
            "Nodes:\n[Delft]\n[Hannover]\n\nEdges:\n[[Hannover]] → [[Delft]]")
    assert (graph.__repr__() ==
            "Graph(['Hannover', 'Delft'], ['Edge([[Hannover]], [[Delft]])'])")


def test_print(capsys):
    example = {"pkg1": ["pkg2", "pkg3"], "pkg2": ["pkg3"], "pkg3": []}

    graph = get_graph(example)
    graph.topo_print()
    captured = capsys.readouterr()
    assert captured.out == """- pkg1
  - pkg2
    - pkg3
  - pkg3
- pkg2
  - pkg3
- pkg3
"""
