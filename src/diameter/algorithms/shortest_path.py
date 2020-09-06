import math
from typing import Union, List, Optional

from diameter.model.graph import AdjacencyMatrix


class Matrices:
    def __init__(self, n):
        self.n = n
        self._matrices: List[List[List[Union[int, float]]]] = []
        for k in range(n):
            matrix = []
            for i in range(n):
                matrix.append([None] * n)
            self._matrices.append(matrix)

    def __str__(self):
        def formatted(v):
            if v is None:
                return 'NIL'
            else:
                return str(v)

        return "\n".join("\t".join(map(formatted, i)) for i in self._matrices[-1])

    def get(self, i, j, k=None) -> Union[int, float]:
        k = self.n - 1 if k is None else k
        return self._matrices[k][i][j]

    def set(self, i, j, k, w):
        self._matrices[k][i][j] = w


class ShortestPathMatrices(Matrices):
    def __init__(self, n):
        super().__init__(n)

    def get(self, i, j, k=None) -> Union[int, float]:
        value = super(ShortestPathMatrices, self).get(i, j, k)
        return math.inf if value is None else value

    def copy_matrix(self, k, matrix: AdjacencyMatrix):
        for i in range(self.n):
            for j in range(self.n):
                self.set(i, j, k, matrix.get_edge(i, j))


class PredecessorsMatrices(Matrices):
    def __init__(self, n):
        super().__init__(n)

    def init_matrix(self, k, matrix: AdjacencyMatrix):
        for i in range(self.n):
            for j in range(self.n):
                if matrix.get_edge(i, j) < math.inf and i != j:
                    self.set(i, j, k, i)
                else:
                    self.set(i, j, k, None)

    def update_predecessors(self, i, j, k, matrices: ShortestPathMatrices):
        if matrices.get(i, j, k - 1) <= (matrices.get(i, k - 1, k - 1) + matrices.get(k - 1, j, k - 1)):
            self.set(i, j, k, self.get(i, j, k - 1))
        else:
            self.set(i, j, k, self.get(k - 1, j, k - 1))


class FloydWarshall:
    def __init__(self, w: AdjacencyMatrix):
        self.graph = w
        self.n: int = self.graph.n_vertices
        self.d: Optional[ShortestPathMatrices] = None
        self.pred: Optional[PredecessorsMatrices] = None
        self._applied = False

    @classmethod
    def from_str(cls, input_: str, directed: bool = True):
        graph = AdjacencyMatrix.from_str(input_, directed=directed)
        return cls(graph)

    def apply(self):
        if self._applied:
            raise RuntimeError('Algorithm already applied')
        self.d = ShortestPathMatrices(self.n)
        self.pred = PredecessorsMatrices(self.n)
        self.d.copy_matrix(0, self.graph)
        self.pred.init_matrix(0, self.graph)
        for k in range(1, self.n):
            for i in range(self.n):
                for j in range(self.n):
                    self.pred.update_predecessors(i, j, k, self.d)
                    dist_with_intermediate = self.d.get(i, k - 1, k - 1) + self.d.get(k - 1, j, k - 1)
                    curr_dist = self.d.get(i, j, k - 1)
                    w = min(curr_dist, dist_with_intermediate)
                    self.d.set(i, j, k, w)
