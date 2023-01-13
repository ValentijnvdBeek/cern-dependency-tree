"""Main function that is run on module execution."""
import argparse
import json

from .main import generate_graph
from .main import get_graph

# pragma: no cover
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Solve dependency trees from the terminal")

    parser.add_argument('--algorithm',
                        metavar='m',
                        type=str,
                        action='store',
                        default='simple',
                        choices=['simple', 'kahn'],
                        help='algorithm used to detect cycles in the graph')
    parser.add_argument(
        '--graph',
        action='store_true',
        default=False,
        help='prints the graph as a graph rather than as a file.')

    # Either we can load data from file or use json data directly
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--filename',
                       metavar='f',
                       type=str,
                       action='store',
                       help='filename that is read',
                       default='/tmp/deps.json')
    group.add_argument('--data',
                       metavar='d',
                       type=str,
                       action='store',
                       help="json graph object")

    # Parse the args and generate the graphs
    args = parser.parse_args()
    if args.data is not None:
        g = get_graph(json.loads(args.data), args.algorithm)
    else:
        g = generate_graph(args.filename, args.algorithm)

    if args.graph:
        print(g)
    else:
        g.topo_print()
