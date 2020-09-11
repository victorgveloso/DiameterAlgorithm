import math
from typing import Tuple, List

from diameter.algorithms.shortest_path import FloydWarshall
from diameter.model.graph import AdjacencyMatrix


class DiameterAlgorithm(FloydWarshall):
    """
    Implementation of the "Graph Diameter Identifier" algorithm.

    Based on the :class:`~diameter.algorithms.shortest_path.FloydWarshall`
    """

    def __init__(self, w: AdjacencyMatrix):
        super().__init__(w)
        self.max = (0, 0)
        self.diameter_shortest_path = []

    def apply(self):
        """
        Execute method from Command Pattern. Run diameter algorithm.

        1. Run FloydWarshall, an O(n^3) time complexity algorithm;
        2. Then find max value on shortest-path matrix;
        3. Finally generate output's information

        It can be used only once, otherwise it'll raise RuntimeError.
        """
        super().apply()

        for i in range(self.n):
            for j in range(self.n):
                self.update_max(i, j)

        self.diameter_shortest_path = []
        self.store_shortest_path_to_output(*self.max)

    def update_max(self, i, j):
        """
        Check value on cell (i,j) and compare it to the current maximum value.

        :param i: cell's row
        :param j: cell's column
        """
        curr_max = self.d.get_last(self.max[0], self.max[1])
        new_value = self.d.get_last(i, j)
        if new_value != math.inf and new_value > curr_max:
            self.max = (i, j)

    def store_shortest_path_to_output(self, i, j):
        """
        Read each vertex on the shortest-path between diameter vertices

        :param i: origin diameter vertex
        :param j: target diameter vertex
        """
        pred = self.pred.get_last(i, j)
        if i == j:
            self.diameter_shortest_path.append(i)
        elif pred is None:
            raise RuntimeError("There is no path from 'i' to 'j'")
        else:
            self.store_shortest_path_to_output(i, pred)
            self.diameter_shortest_path.append(j)

    def diameter_value(self) -> int:
        """
        :return: Diameter's shortest-path total weight
        """
        return self.d.get_last(*self.max)

    def diameter_vertices(self) -> Tuple[int, int]:
        """
        :return: Both origin and target diameter vertices
        """
        return self.max[0] + 1, self.max[1] + 1

    def minimum_path_size(self) -> int:
        """
        :return: Number of vertices on the shortest-path between diameter vertices
        """
        return len(self.diameter_shortest_path)

    def minimum_path_vertices(self) -> List[int]:
        """
        :return: Each vertex on the shortest-path between diameter vertices
        """
        return [i + 1 for i in self.diameter_shortest_path]

    def formatted_result(self) -> str:
        """
        :return: A formatted text to be outputted
        """
        return f"""{self.diameter_value()}
{" ".join(map(str, self.diameter_vertices()))}
{self.minimum_path_size()}
{" ".join(map(str, self.minimum_path_vertices()))}"""
