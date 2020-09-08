import math
from typing import Tuple, List

from diameter.algorithms.shortest_path import FloydWarshall
from diameter.model.graph import AdjacencyMatrix


class DiameterAlgorithm(FloydWarshall):
    def __init__(self, w: AdjacencyMatrix):
        super().__init__(w)
        self.max = (0, 0)
        self.output = []

    def apply(self):
        super().apply()

        for i in range(self.n):
            for j in range(self.n):
                self.update_max(i, j)

        self.output = []
        self.store_shortest_path_to_output(*self.max)

    def update_max(self, i, j):
        curr_max = self.d.get_last(self.max[0], self.max[1])
        new_value = self.d.get_last(i, j)
        if new_value != math.inf and new_value > curr_max:
            self.max = (i, j)

    def store_shortest_path_to_output(self, i, j):
        pred = self.pred.get_last(i, j)
        if i == j:
            self.output.append(i)
        elif pred is None:
            raise RuntimeError("There is no path from 'i' to 'j'")
        else:
            self.store_shortest_path_to_output(i, pred)
            self.output.append(j)

    def diameter_value(self) -> int:
        return self.d.get_last(*self.max)

    def diameter_vertices(self) -> Tuple[int, int]:
        return self.max[0] + 1, self.max[1] + 1

    def minimum_path_size(self) -> int:
        return len(self.output)

    def minimum_path_vertices(self) -> List[int]:
        return [i + 1 for i in self.output]

    def formatted_result(self) -> str:
        return f"""{self.diameter_value()}
{" ".join(map(str, self.diameter_vertices()))}
{self.minimum_path_size()}
{" ".join(map(str, self.minimum_path_vertices()))}"""
