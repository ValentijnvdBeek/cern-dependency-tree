"""Contains a graph object with nodes and edges between nodes."""
from typing import List


class Node:
    """Simple node class."""
    def __init__(self, name: str):
        """Intialized a node."""
        self.name = name

    def __repr__(self):
        """Evaluable reprenstation of a node."""
        return f"Node({self.name})"

    def __str__(self):
        """String representation of an edge."""
        return f"[{self.name}]"

    def __eq__(self, other):
        """Compare identity by checking if they have the same name."""
        if type(other) == str:
            return self.name == other

        return other.name == self.name


class Edge:
    """An directed edge between two nodes."""
    def __init__(self, source: Node, target: Node):
        """Create an edge between a `source` and `target` node."""
        self.source = source
        self.target = target

    def __str__(self):
        """String representatin of an edge."""
        return f"{self.source} → {self.target}"

    def __repr__(self):
        """Evaluatable representation of an edge."""
        return f"Edge({self.source}, {self.target})"

    def __eq__(self, other):
        """Checks edge equality by comparing the source and the target.

        Since it is a directed edge Edge(a, b) != Edge(b, a)
        """
        return self.source == other.source and self.target == other.target

    def __hash__(self):
        """Hash to compare the edges."""
        return hash(str(self))


class Graph:
    """Graph containing nodes and edges."""
    def __init__(self, nodes: list[str], edges: list[Edge]):
        """Creates a graph.

        Args:
           nodes: List of node names
           edges: Edges between nodes
        """
        self._nodes = dict([(n, Node(n)) for n in nodes])
        self._edges = edges

    def add_edge(self, source: str, target: str):
        """Creates an edge between a `source` and `target` node."""
        edge = Edge(Node(source), Node(target))
        if edge not in self._edges:
            self._edges.append(edge)

    def add_node(self, name: str):
        """Adds a node to the graph."""
        self._nodes[name] = Node(name)

    def __str__(self):
        """String representation of the grraph."""
        nodes = '\n'.join(sorted([n.__str__() for n in self._nodes.values()]))
        edges = '\n'.join(sorted([e.__str__() for e in self._edges]))

        return f"Nodes:\n{nodes}\n\nEdges:\n{edges}"

    def __repr__(self):
        """Evaluatable representation of the graph."""
        nodes = list(self._nodes.keys())
        edges = [e.__repr__() for e in self._edges]
        return f"Graph({nodes}, {edges})"

    def _get_edges(self, node: Node):
        """Gets all the edges for the given node is the source."""
        return [e for e in self._edges if e.source == node]

    def _topo_print_helper(self, edges: List[Edge], times: int = 1):
        """Prints all the edges in the graph at the right level."""
        for edge in edges:
            print(f"{'  ' * times}- {edge.target.name}")
            self._topo_print_helper(self._get_edges(edge.target),
                                    times=times + 1)

    def topo_print(self):
        """Prints the graph using the topological order."""
        for node in self._nodes:
            print(f"- {node}")
            self._topo_print_helper(self._get_edges(node))

    def __eq__(self, other):
        """Checks equality of graphs by comparing the edges & nodes."""
        diff_nodes = set(self._nodes) ^ set(other._nodes)
        diff_edges = set(self._edges) ^ set(other._edges)
        return not (diff_nodes or diff_edges)
