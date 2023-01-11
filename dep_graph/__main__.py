"""Main function that is run on module execution."""
import sys

from .main import main

if __name__ == "__main__":
    if len(sys.argv) == 1:
        main("/tmp/deps.json")
    else:
        main(sys.argv[1])
