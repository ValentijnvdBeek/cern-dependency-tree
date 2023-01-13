"""Implements the Kahn algorithm for topological sorting."""
from ..graph import Graph


class KahnAlgorithm:
    """Kahn's algorithm for topological sorting.

    This algorithm is adapted from the wikipedia page on topological
    sorting: https://en.wikipedia.org/wiki/Topological_sorting#Kahn's_algorithm
    """
    @staticmethod
    def run(data):
        """Starts an iterative algorithm to solve the dependency graph problem.

        Args:
          data: dictionary containing the dependencies.

        Raises:
          Exception if there is a cycle in the graph

        Returns:
          A graph object with edges for all dependencies
        """
        graph = Graph([], [])
        outnodes = set()

        # First we setup a basic graph by adding nodes for each
        # package and edge for each dependency. We also keep track
        # of all nodes which have something depending on it.
        for node, dependencies in data.items():
            graph.add_node(node)
            for dep in dependencies:
                graph.add_edge(node, dep)
                outnodes.add(dep)

        # We copy the graph over since we don't print the result here.
        workgraph = Graph(graph._nodes.keys(), graph._edges.copy())
        sort = []
        nodes = set(data.keys()) ^ outnodes

        while len(nodes) != 0:
            node = nodes.pop()
            sort.append(node)

            # We remove all edges from this node and add the target
            # node of the edge to the set if there are no more edges.
            # If there is a cycle somewhere, one node must never be
            # have no edges and therefore is never removed.
            for e in workgraph.get_edges_source(node):
                workgraph._edges.remove(e)
                if len(workgraph.get_edges_target(e.target)) == 0:
                    nodes.add(e.target.name)

        if len(workgraph._edges) != 0:
            raise Exception("Cycle in graph detected!")

        return graph
