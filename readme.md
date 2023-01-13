# CERN Dependency Tree Assignment
A small Python project written for a CERN job application. The module
aims to solve dependencies trees given to it as a json file. This file
is then parsed into a graph, checked for cycles and printed as a
topologically sorted graph.

# Dependencies
- Python standard library
- tkinter (graph drawer)
- pytest (unit tests)
- pre-commit (static analysis test)
- yapf (auto-format code)
- flake8 (stylechecker pep8)
- mypy (type checking)
- autoflake (auto-formatter)
- sphinx (documentation)

# Features
- Two algorithms (DFS/Custom/Simple & Kahn)
- Graph drawer using Tkinter
- Additional helper features to support Python dictionaries
- Print graphs from json data over CLI or file

# How to run
**Print graph**
```bash
python -m dep_graph
```

**Run tests with coverage**
```bash
pytest --cov=dep_graph --cov-report html
```

**Run static analysis tools**
```bash
pre-commit run --all
```

**Generate HTML documentation**
```bash
make html
```

# Command-line options
- `--help`: help message
- `--algorithm [simple, kahn]`: cycle detection algorithm to be used
- `--graph`: show graph directly rather than printing it
- `--filename`: filename of the json data
- `--data`: json data to generate graph, cannot be used with `--filename`

# Algorithm description
This section describes in short the two algorithms used to detect
directed acyclic graphs. At the moment, two algorithms are
implemented: Kahn's Algorithm & custom Simple Algorithm based on Depth
First Search.

## Simple algorithm
A custom algorithm to solve the problem which is based on Depth First
Search and recursion. It starts with an graph with no edges and node
for each input package. For each package dependency it will recurse
depth first until it reaches a dependency with no other
dependencies. It will then return until it hits it's base case or
until it has seen the same package twice on it's path.

The algorithm solves the DAG problem in O(N^2)[1] time since it needs
to recurse over each node and each edge seperately. However this
solution does feature three drawbacks: it takes O(N^2) space on the
stack, is limited by the smaller stack size limit and slower to
execute. These problems are, however, caused not by the algorithm but
rather to the lack of tail call optimization in Python.

### For fun: Justification O(N^2)
For this proof there are two cases:
1. A graph which has no cycle.
2. A graph which has a cycle.

**Case 1: Graph with no cycle**

Assume an input graph G with no cycle and N nodes. In the worst case,
the first node depends on all nodes that are not itself or N-1
nodes. Since N0 depends on N1, N1 cannot depend on N0 and hence it can
in the worst case depend on N-2. From here it is trivial to deduce
that, in the worst case, the number of total dependencies is equal to
_Sum(N-i)_ or _N^2_ by Gauss summation.

**Case 2: Graph with a cycle**
Assume the minimum graph with a cycle. From the first case, we know
that such a graph can have at most N! edges. Since a cycle will be
detected at N^2+1, the worst case of is remains O(N^2)

## Khan's Algorithm
The description of the algorithm is taken from
[Wikipedia][https://en.wikipedia.org/wiki/Topological_sorting#Depth-first_search]. The
algorithm was invented by Kahn in 1962 and is iterative in nature.

First all nodes are found which have no incoming edges. All edges with
that node as a source are removed from the graph. Any node with no
incoming edges are then added to the queue and the process is repeated
until the queue is exhausted. If there any edges remaining, then there
must be a cycle since all "free-standing" nodes are removed. The
complexity of this algorithm is O(N^2) since in the worst case each
free node frees only one other node. The rest follows trivially from
the proof above.

However although the complexity is the same, this is variant does
perform significantly better than the recursive variant since it does
not need to create space on the stack for each iteration.

## Printing
Printing is done using a recursive method that prints all edges in
order.

# File format description
## BNF
```text
<name> ::= <alphanum>
<dependency> :: <name>*
```

## JSON Example
```json
{
    "pkg1": ["pkg2", "pkg3", "pkg4"],
    "pkg2": ["pkg3", "pkg4"],
    "pkg3": ["pkg5", "pkg7"],
    "pkg4": ["pkg7"],
    "pkg5": [],
    "pkg6": ["pkg7"],
    "pkg7": []
}
```

## Example Output
```
- pkg1
  - pkg2
    - pkg3
      - pkg5
      - pkg7
    - pkg4
      - pkg7
  - pkg3
    - pkg5
    - pkg7
  - pkg4
    - pkg7
- pkg2
  - pkg3
    - pkg5
    - pkg7
  - pkg4
    - pkg7
- pkg3
  - pkg5
  - pkg7
- pkg4
  - pkg7
- pkg5
- pkg6
  - pkg7
- pkg7
```

### Example cycle
```json
{
    "pkg1": ["pkg2", "pkg3"],
    "pkg2": ["pkg4"],
    "pkg3": ["pkg3"],
    "pkg4": ["pkg5"],
    "pkg5": []
}
```
