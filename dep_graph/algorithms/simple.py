"""Simple recursive algorithm for solving dependency trees."""
from typing import Dict
from typing import List

from ..graph import Graph


class SimpleAlgorithm:
    """Basic algorithm to generate a dependency graph.

    The algorithm recurses to the entire tree and adds an edge for
    each dependencies. Once a dependency is added to the tree it is
    added to the trace of the exeuction. If a dependency was already
    in the trace then we know that there is a cycle and we stop
    executing.
    """
    @staticmethod
    def run(data):
        """Starts a recursive algorithm to solve the dependency graph problem.

        Args:
          data: dictionary containing the dependencies.

        Throws:
          Exception if there is a cycle in the graph

        Returns:
          A graph object with edges for all dependencies
        """
        g = Graph()
        for package, deps in data.items():
            g.add_node(package)
            SimpleAlgorithm._recurse(package,
                                     data, [package],
                                     deps,
                                     g,
                                     level=1)
        return g

    @staticmethod
    def _recurse(source: str,
                 data: Dict[str, List[str]],
                 seen: List[str],
                 dependencies: List[str],
                 graph: Graph,
                 level: int = 0) -> None:
        for dep in dependencies:
            if dep in seen:
                raise Exception("Cycle in graph!")

            graph.add_edge(source, dep)
            SimpleAlgorithm._recurse(dep,
                                     data,
                                     seen + [dep],
                                     data[dep],
                                     graph,
                                     level=level + 1)
