CERN Dependency Tree
================================================
A small Python project written for a CERN job application. The module
aims to solve dependencies trees given to it as a json file. This file
is then parsed into a graph, checked for cycles and printed as a
topologically sorted graph.

Dependencies
------------

- Python standard library
- tkinter (graph drawer)
- pytest (unit tests)
- pre-commit (static analysis test)
- yapf (auto-format code)
- flake8 (stylechecker pep8)
- mypy (type checking)
- autoflake (auto-formatter)
- sphinx (documentation)

Features
--------
- Two algorithms (DFS/Custom/Simple & Kahn)
- Graph drawer using Tkinter
- Additional helper features to support Python dictionaries
- Print graphs from json data over CLI or file

How to run
----------
Example commands that can be used to run the program or to gain
information about the health of the program.

**Print graph**

.. code-block:: bash

   python -m dep_graph


***Run tests with coverage**

.. code-block:: bash

   pytest --cov=dep_graph --cov-report html

**Run static analysis tools**

.. code-block:: bash

   pre-commit run --all

**Generate HTML documentation**

.. code-block:: bash

   make html

Command-line options
--------------------
- `--help`: help message
- `--algorithm [simple, kahn]`: cycle detection algorithm to be used
- `--graph`: show graph directly rather than printing it
- `--filename`: filename of the json data
- `--data`: json data to generate graph, cannot be used with `--filename`

Example input
-------------

.. code-block:: json

   {
        "pkg1": ["pkg2", "pkg3", "pkg4"],
        "pkg2": ["pkg3", "pkg4"],
        "pkg3": ["pkg7"],
        "pkg4": [],
        "pkg6": ["pkg7"],
        "pkg7": []
   }


Example output
--------------
.. code-block:: text

   - pkg1
     - pkg2
       - pkg3
         - pkg7
       - pkg4
    - pkg3
       - pkg7
    - pkg4
  - pkg2
    - pkg3
      - pkg7
    - pkg4
  - pkg3
      - pkg7
  - pkg4
  - pkg6
     - pkg7
  - pkg7

Example cycle
-------------

.. code-block:: json
   {
       "pkg1": ["pkg2", "pkg3"],
       "pkg2": ["pkg4"],
       "pkg3": ["pkg3"],
       "pkg4": ["pkg5"],
       "pkg5": []
   }

Contents
--------
.. toctree::
   :maxdepth: 2

   main.rst
   algorithms.rst
   graph.rst


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
