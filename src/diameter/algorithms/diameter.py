from __future__ import absolute_import
import math

from algorithms.shortest_path import FloydWarshall
from model.graph import AdjacencyMatrix


class DiameterAlgorithm(FloydWarshall):
    def __init__(self, w):
        super(DiameterAlgorithm, self).__init__(w)
        self.max = (0, 0)
        self.output = []

    def apply(self):
        super(DiameterAlgorithm, self).apply()

        for i in xrange(self.n):
            for j in xrange(self.n):
                self.update_max(i, j)

        self.output = []
        self.store_shortest_path_to_output(*self.max)

    def update_max(self, i, j):
        curr_max = self.d.get(self.max[0], self.max[1])
        new_value = self.d.get(i, j)
        if new_value != float("inf") and new_value > curr_max:
            self.max = (i, j)

    def store_shortest_path_to_output(self, i, j):
        pred = self.pred.get(i, j)
        if i == j:
            self.output.append(i)
        elif pred is None:
            raise RuntimeError(u"There is no path from 'i' to 'j'")
        else:
            self.store_shortest_path_to_output(i, pred)
            self.output.append(j)

    def diameter_value(self):
        return self.d.get(*self.max)

    def diameter_vertices(self):
        return self.max[0] + 1, self.max[1] + 1

    def minimum_path_size(self):
        return len(self.output)

    def minimum_path_vertices(self):
        return [i + 1 for i in self.output]

    def formatted_result(self):
        return """{}
{}
{}
{}""".format(self.diameter_value()," ".join(map(str, self.diameter_vertices())),self.minimum_path_size()," ".join(map(str, self.minimum_path_vertices())))
