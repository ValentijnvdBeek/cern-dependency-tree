from itertools import chain
from pprint import pprint

import pytest

from .context import dep_graph

Edge = dep_graph.Edge
Node = dep_graph.Node
Graph = dep_graph.Graph
get_graph = dep_graph.get_graph


def compare_list(l1, l2):
    diff = set(l1) ^ set(l2)
    assert not diff


def test_given_example():
    example = {"pkg1": ["pkg2", "pkg3"], "pkg2": ["pkg3"], "pkg3": []}

    graph = get_graph(example)
    expected = Graph(
        ["pkg1", "pkg2", "pkg3"],
        [Edge("pkg1", "pkg2"),
         Edge("pkg1", "pkg3"),
         Edge("pkg2", "pkg3")])

    assert (graph == expected)


def test_no_dependencies():
    nodes = ["pkg1", "pkg2", "pkg3", "pkg4", "pkg5"]
    graph = get_graph(dict(zip(nodes, [[]] * len(nodes))))
    expected = Graph(nodes, [])
    assert (graph._nodes == expected._nodes)


def test_one_common():
    content = {"pkg14": []}
    for i in range(0, 12):
        content[f"pkg{i}"] = ["pkg14"]

    graph = get_graph(content)

    expected = Graph(
        content.keys(),
        [Edge(n, "pkg14") for n in content.keys() if n != "pkg14"])

    compare_list(expected._nodes, graph._nodes)
    compare_list(expected._edges, graph._edges)


def test_all_different():
    content = {}
    for i in range(0, 20):
        deps = [f"pkg{i + 100}", f"pkg{i + 200}", f"pkg{i + 300}"]
        content.update(dict(zip(deps, [[]] * len(deps))))
        content[f"pkg{i}"] = deps

    graph = get_graph(content)
    edges = [[Edge(source, target) for target in targets]
             for source, targets in content.items()]
    expected = Graph(content.keys(), chain(*edges))
    compare_list(expected._nodes, graph._nodes)
    compare_list(expected._edges, graph._edges)


def test_disjoint_trees():
    content = {
        "pkg1": ["pkg2", "pkg3"],
        "pkg2": ["pkg7"],
        "pkg3": ["pkg4", "pkg5"],
        "pkg4": [],
        "pkg5": ["pkg6"],
        "pkg6": [],
        "pkg7": [],
        "pkg8": ["pkg9", "pkg12", "pkg13"],
        "pkg9": ["pkg10"],
        "pkg10": ["pkg11"],
        "pkg11": [],
        "pkg12": [],
        "pkg13": ["pkg14"],
        "pkg14": []
    }

    graph = get_graph(content)
    edges = [
        Edge("pkg1", "pkg2"),
        Edge("pkg1", "pkg3"),
        Edge("pkg2", "pkg7"),
        Edge("pkg3", "pkg4"),
        Edge("pkg3", "pkg5"),
        Edge("pkg5", "pkg6"),
        Edge("pkg8", "pkg9"),
        Edge("pkg9", "pkg10"),
        Edge("pkg10", "pkg11"),
        Edge("pkg8", "pkg12"),
        Edge("pkg8", "pkg13"),
        Edge("pkg13", "pkg14")
    ]

    expected = Graph(content.keys(), edges)
    assert (graph == expected)


def test_long_way_home():
    content = {
        "pkg1": ["pkg2", "pkg3"],
        "pkg2": ["pkg4"],
        "pkg3": [],
        "pkg4": ["pkg5"],
        "pkg5": ["pkg6"],
        "pkg6": ["pkg7"],
        "pkg7": ["pkg8"],
        "pkg8": ["pkg9"],
        "pkg9": ["pkg3"]
    }

    graph = get_graph(content)
    edges = [
        Edge("pkg1", "pkg2"),
        Edge("pkg1", "pkg3"),
        Edge("pkg2", "pkg4"),
        Edge("pkg4", "pkg5"),
        Edge("pkg5", "pkg6"),
        Edge("pkg6", "pkg7"),
        Edge("pkg7", "pkg8"),
        Edge("pkg8", "pkg9"),
        Edge("pkg9", "pkg3")
    ]

    expected = Graph(content.keys(), edges)
    compare_list(graph._edges, expected._edges)


def test_maximum_connected():
    content = {
        "pkg1": ["pkg2", "pkg3", "pkg4", "pkg5"],
        "pkg2": ["pkg3", "pkg4", "pkg5"],
        "pkg3": ["pkg4", "pkg5"],
        "pkg4": ["pkg5"],
        "pkg5": []
    }

    graph = get_graph(content)
    edges = [
        Edge("pkg1", "pkg2"),
        Edge("pkg1", "pkg3"),
        Edge("pkg1", "pkg4"),
        Edge("pkg1", "pkg5"),
        Edge("pkg2", "pkg3"),
        Edge("pkg2", "pkg4"),
        Edge("pkg2", "pkg5"),
        Edge("pkg3", "pkg4"),
        Edge("pkg3", "pkg5"),
        Edge("pkg4", "pkg5")
    ]

    expected = Graph(content.keys(), edges)
    compare_list(graph._edges, expected._edges)


def test_cycle():
    content = {"pkg1": ["pkg1"]}

    with pytest.raises(Exception):
        get_graph(content)


def test_long_cycle():
    content = {
        "pkg1": ["pkg2", "pkg3"],
        "pkg2": ["pkg4"],
        "pkg3": [],
        "pkg4": ["pkg5"],
        "pkg5": ["pkg6"],
        "pkg6": ["pkg7"],
        "pkg7": ["pkg8"],
        "pkg8": ["pkg9"],
        "pkg9": ["pkg2"]
    }

    with pytest.raises(Exception):
        get_graph(content)


def test_complicated():
    content = {
        "p1": ["p2", "p3"],
        "p2": ["p5"],
        "p3": ["p5"],
        "p4": ["p12", "p11"],
        "p5": ["p6", "p7"],
        "p6": ["p4"],
        "p7": ["p8", "p9", "p10"],
        "p8": ["p11", "p12"],
        "p10": [],
        "p11": ["p13"],
        "p12": [],
        "p13": ["p14"],
        "p14": ["p4"]
    }

    with pytest.raises(Exception):
        get_graph(content)
