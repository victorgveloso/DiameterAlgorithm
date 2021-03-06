.. Graph Diameter Identifier documentation master file, created by
sphinx-quickstart on Thu Sep 10 17:18:06 2020.
You can adapt this file completely to your liking, but it should at least
contain the root `toctree` directive.

Welcome to Graph Diameter Identifier's documentation!
=====================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Overview
========

How do I install it?
--------------------

#. You should have a python 3 interpreter installed on your machine.
    - `PyPy 3 <https://www.pypy.org/>`_ is recommended (substitute ``<your_python_interpreter>`` with ``pypy3`` for now on)
    - `CPython 3 <https://www.python.org/>`_ is supported (substitute ``<your_python_interpreter>`` with ``python3`` for now on)
#. Then you may choose between three alternatives:
    1. User-specific installation (Recommended for end-users)
        - run ``$ <your_python_interpreter> setup.py install --user``
    2. System-wide installation
        - run ``# <your_python_interpreter> setup.py install`` as administrator
    3. Virtual environment installation (Recommended for development)
        - Create the virtual environment (you must create it at the first time you're installing it): ``$ virtualenv -p `which <your_python_interpreter>` venv``
        - Activate the environment: ``$ source venv/bin/activate``
        - Run: ``$ <your_python_interpreter> setup.py install``
        - Are you done? Do you want to deactivate the environment? So do it through the command ``$ deactivate``


How do I run it?
----------------

#. After installing it, you should have "`diameter`" installed as module.
#. You can see the available commands running ``$ <your_python_interpreter> -m diameter -h``
#. There are two IO options available:
    - Standard Input/Output;
    - File.
#. The graph is undirected by default, but you can specify it as directed through the optional parameter ``--directed-graph`` (write it after ``$ <your_python_interpreter> -m diameter`` and before the IO option choice).
#. Both methods require you to describe a graph (following an :ref:`specific structure <input-structure>`).
#. For "Standard Input/Output":
    - run the following command: ``$ <your_python_interpreter> -m diameter stdio``;
    - the command prompt will be locked and you must type whatever input you want;
    - the output will be printed out on the command prompt after the algorithm execution.
#. For "File":
    - you must specify an input file path and an output file path **(Existing files on output path will be overwritten!)**;
    - run the following command: ``$ <your_python_interpreter> -m diameter file <your_input_file_path> <your_output_file_path>``.


.. _input-structure:

Input structure:
^^^^^^^^^^^^^^^^

1. First line: <Number of vertices> <Number of edges>
2. Following "Number of edges" lines: <Origin vertex> <Target vertex> <Edge weight>

Input example:
^^^^^^^^^^^^^^

.. code-block:: text

   4 3
   1 2 1
   2 3 2
   3 4 3

Understanding the output file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. First line: Distance between the diameter vertices
2. Second line: <origin_diameter_vertex_id> <target_diameter_vertex_id>
3. Third line: Number of vertices on the Shortest Path between the diameter vertices
4. Fourth line: The id of each vertex on the Shortest Path between the diameter vertices

How do I contribute to it?
---------------------------

This is a design and analysis of algorithms work. No maintenance is planned and you shouldn't run it in production.

But **it's open source!** If you're still interested on submitting contributions, then you should open an Issue, create a Pull Request, or contact me by e-mail.

Reference
=========

Algorithms
==========

Shortest Path (FloydWarshall)
-----------------------------

.. automodule:: diameter.algorithms.shortest_path
   :members:

Diameter (FloydWarshall modification)
-------------------------------------

.. automodule:: diameter.algorithms.diameter
   :members:

Model (Data structure)
========================

Adjacency Matrix
----------------

.. automodule:: diameter.model.graph

   .. autoclass:: AdjacencyMatrix
      :members:

      .. automethod:: __init__
