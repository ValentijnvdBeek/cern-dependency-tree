==========
Algorithms
==========
This section describes in short the two algorithms used to detect
directed acyclic graphs. At the moment, two algorithms are
implemented: Kahn's Algorithm & custom Simple Algorithm based on Depth
First Search.

----------------
Simple Algorithm
----------------
A custom algorithm to solve the problem which is based on Depth First
Search and recursion. It starts with an graph with no edges and node
for each input package. For each package dependency it will recurse
depth first until it reaches a dependency with no other
dependencies. It will then return until it hits it's base case or
until it has seen the same package twice on it's path.

The algorithm solves the DAG problem in :math:`\mathcal{O}(N^2)` [1]
time since it needs to recurse over each node and each edge
seperately. However this solution does feature three drawbacks: it
takes :math:`\mathcal{O}(N^2)` space on the stack, is limited by the
smaller stack size limit and slower to execute. These problems are,
however, caused not by the algorithm but rather to the lack of tail
call optimization in Python.

For this proof there are two cases:
1. A graph which has no cycle.
2. A graph which has at least one cycle.

**Case 1: Graph with no cycle**

Assume an input graph G with no cycle and :math:`N` nodes. In the
worst case, the first node depends on all nodes that are not itself or
:math:`N-1` nodes. Since :math:`N_0` depends on :math:`N_1`,
:math:`N_1` cannot depend on :math:`N_0` and hence it can in the worst
case depend on :math:`N-2`. From here it is trivial to deduce that, in
the worst case, the number of total dependencies is equal to
:math:`\sum_{i=0}^N N-i` or :math:`N^2` by Gauss summation.

**Case 2: Graph with at least one cycle**

Assume the minimum graph with a cycle. From the first case, we know
that such a graph can have at most N! edges. Since a cycle will be
detected at :math:`N^2+1`, the worst case of is remains :math:`\mathcal{O}(N^2)`

Members
-------

.. automodule:: dep_graph.algorithms.simple
   :members:
   :undoc-members:
   :show-inheritance:

----------------
Kahn's Algorithm
----------------
The description of the algorithm is taken from
[Wikipedia][https://en.wikipedia.org/wiki/Topological_sorting#Depth-first_search]. The
algorithm was invented by Kahn in 1962 and is iterative in nature.

First all nodes are found which have no incoming edges. All edges with
that node as a source are removed from the graph. Any node with no
incoming edges are then added to the queue and the process is repeated
until the queue is exhausted. If there any edges remaining, then there
must be a cycle since all "free-standing" nodes are removed. The
complexity of this algorithm is :math:`\mathcal{O}(N^2)` since in the
worst case each free node frees only one other node. The rest follows
trivially from the proof above.

However although the complexity is the same, this is variant does
perform significantly better than the recursive variant since it does
not need to create space on the stack for each iteration.

Members
-------
.. automodule:: dep_graph.algorithms.kahn
   :members:
   :undoc-members:
   :show-inheritance:
