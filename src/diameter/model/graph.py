import math
from typing import Union


class AdjacencyMatrix:
    """
    The main graph Data Structure.
    """

    def __init__(self, n_vertices=0, m_edges=0, directed=True):
        """
        The AdjacencyMatrix's main constructor.

        The created graph doesn't contain any edges yet, those should be added using :func:`.place_edge`

        :param n_vertices: Number of vertices
        :param m_edges: Number of edges
        :param directed: A flag indicating whether the graph is directed or not
        """
        self.directed = directed
        self._n_vertices = n_vertices
        self._m_edges = m_edges
        self._edges_left = m_edges
        self._matrix = []
        for i in range(n_vertices):
            line = [math.inf] * n_vertices
            line[i] = 0  # diagonal principal = 0
            self._matrix.append(line)

    def __str__(self):
        """
        A textual representation of the graph

        :return: A string containing the elements in a matrix-like representation
        """
        return "\n".join("\t".join(map(str, i)) for i in self._matrix)

    @classmethod
    def from_str(cls, input_path: str, directed=True):
        """
        An static factory method that reads graph info from a file

        :param input_path: Path to input graph description file
        :param directed: A flag indicating whether the graph is directed or not
        :return: AdjacencyMatrix object populated with data extracted from file
        """
        lines = input_path.split('\n')
        n_vertices, m_edges = map(int, lines[0].split(" "))
        graph = cls(n_vertices, m_edges, directed=directed)
        for line in lines[1:]:
            if line == '':
                continue
            from_vertex, to_vertex, weight = map(int, line.split(' '))
            graph.place_edge(from_vertex - 1, to_vertex - 1, weight)
        return graph

    @property
    def n_vertices(self):
        return self._n_vertices

    @property
    def m_edges(self):
        return self._m_edges

    def place_edge(self, from_vertex, to_vertex, weight):
        """
        Place an expected edge with a given weight.

        If edge placing exceeds "Number of Edges" specified on construction, the an ValueError is raised

        :param from_vertex: Origin vertex
        :param to_vertex: Target vertex
        :param weight: Edge's weight
        """
        if self._edges_left >= 1:
            self._edges_left -= 1
        else:
            raise ValueError('All edges have been placed')
        self._matrix[from_vertex][to_vertex] = weight
        if not self.directed:
            self._matrix[to_vertex][from_vertex] = weight

    def get_edge(self, from_vertex: int, to_vertex: int) -> Union[int, float]:
        if self._edges_left >= 1:
            raise ValueError(f"{self._edges_left} edges left unplaced")
        return self._matrix[from_vertex][to_vertex]
