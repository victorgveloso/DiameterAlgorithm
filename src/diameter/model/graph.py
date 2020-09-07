from __future__ import absolute_import
import math
from itertools import imap


class AdjacencyMatrix(object):
    def __init__(self, n_vertices=0, m_edges=0, directed=True):
        self.directed = directed
        self._n_vertices = n_vertices
        self._m_edges = m_edges
        self._edges_left = m_edges
        self._matrix = []
        for i in xrange(n_vertices):
            line = [float("inf")] * n_vertices
            line[i] = 0  # diagonal principal = 0
            self._matrix.append(line)

    def __str__(self):
        return u"\n".join(u"\t".join(imap(unicode, i)) for i in self._matrix)

    @classmethod
    def from_str(cls, input_, directed=True):
        lines = input_.split(u'\n')
        n_vertices, m_edges = imap(int, lines[0].split(u" "))
        graph = cls(n_vertices, m_edges, directed=directed)
        for line in lines[1:]:
            from_vertex, to_vertex, weight = imap(int, line.split(u' '))
            graph.place_edge(from_vertex - 1, to_vertex - 1, weight)
        return graph

    @property
    def n_vertices(self):
        return self._n_vertices

    @property
    def m_edges(self):
        return self._m_edges

    def place_edge(self, from_vertex, to_vertex, weight):
        if self._edges_left >= 1:
            self._edges_left -= 1
        else:
            raise ValueError(u'All edges have been placed')
        self._matrix[from_vertex][to_vertex] = weight
        if not self.directed:
            self._matrix[to_vertex][from_vertex] = weight

    def get_edge(self, from_vertex, to_vertex):
        if self._edges_left >= 1:
            raise ValueError("{} edges left unplaced".format(self._edges_left))
        return self._matrix[from_vertex][to_vertex]
