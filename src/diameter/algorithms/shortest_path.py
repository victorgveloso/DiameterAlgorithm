from __future__ import absolute_import
import math

from model.graph import AdjacencyMatrix
from itertools import imap


class Matrices(object):
    def __init__(self, n):
        self.n = n
        self._matrices = []
        for k in xrange(n):
            matrix = []
            for i in xrange(n):
                matrix.append([None] * n)
            self._matrices.append(matrix)

    def __str__(self):
        def formatted(v):
            if v is None:
                return u'NIL'
            else:
                return unicode(v)

        return u"\n".join(u"\t".join(imap(formatted, i)) for i in self._matrices[-1])

    def get(self, i, j, k=None):
        k = self.n - 1 if k is None else k
        return self._matrices[k][i][j]

    def set(self, i, j, k, w):
        self._matrices[k][i][j] = w


class ShortestPathMatrices(Matrices):
    def __init__(self, n):
        super(ShortestPathMatrices, self).__init__(n)

    def get(self, i, j, k=None):
        value = super(ShortestPathMatrices, self).get(i, j, k)
        return float("inf") if value is None else value

    def copy_matrix(self, k, matrix):
        for i in xrange(self.n):
            for j in xrange(self.n):
                self.set(i, j, k, matrix.get_edge(i, j))


class PredecessorsMatrices(Matrices):
    def __init__(self, n):
        super(PredecessorsMatrices, self).__init__(n)

    def init_matrix(self, k, matrix):
        for i in xrange(self.n):
            for j in xrange(self.n):
                if matrix.get_edge(i, j) < float("inf") and i != j:
                    self.set(i, j, k, i)
                else:
                    self.set(i, j, k, None)

    def update_predecessors(self, i, j, k, matrices):
        if matrices.get(i, j, k - 1) <= (matrices.get(i, k - 1, k - 1) + matrices.get(k - 1, j, k - 1)):
            self.set(i, j, k, self.get(i, j, k - 1))
        else:
            self.set(i, j, k, self.get(k - 1, j, k - 1))


class FloydWarshall(object):
    def __init__(self, w):
        self.graph = w
        self.n = self.graph.n_vertices
        self.d = None
        self.pred = None
        self._applied = False

    @classmethod
    def from_str(cls, input_, directed = True):
        graph = AdjacencyMatrix.from_str(input_, directed=directed)
        return cls(graph)

    def apply(self):
        if self._applied:
            raise RuntimeError(u'Algorithm already applied')
        self.d = ShortestPathMatrices(self.n)
        self.pred = PredecessorsMatrices(self.n)
        self.d.copy_matrix(0, self.graph)
        self.pred.init_matrix(0, self.graph)
        for k in xrange(1, self.n):
            for i in xrange(self.n):
                for j in xrange(self.n):
                    self.pred.update_predecessors(i, j, k, self.d)
                    dist_with_intermediate = self.d.get(i, k - 1, k - 1) + self.d.get(k - 1, j, k - 1)
                    curr_dist = self.d.get(i, j, k - 1)
                    w = min(curr_dist, dist_with_intermediate)
                    self.d.set(i, j, k, w)
