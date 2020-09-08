import math
from typing import Union, List, Optional

from diameter.model.graph import AdjacencyMatrix


class Matrices:
    def __init__(self, n, default_value=None):
        self.n = n
        self._matrices: List[List[List[Union[int, float]]]] = []
        for k in range(n):
            matrix = []
            for i in range(n):
                matrix.append([default_value] * n)
            self._matrices.append(matrix)

    def __str__(self):
        def formatted(v):
            if v is None:
                return 'NIL'
            else:
                return str(v)

        return "\n".join("\t".join(map(formatted, i)) for i in self._matrices[-1])

    def get_last(self, i, j) -> Union[int, float]:
        return self._matrices[self.n - 1][i][j]

    def get(self, i, j, k) -> Union[int, float]:
        return self._matrices[k][i][j]

    def set(self, i, j, k, w):
        self._matrices[k][i][j] = w


class ShortestPathMatrices(Matrices):
    def __init__(self, n):
        super().__init__(n, default_value=math.inf)

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
                if i != j and matrix.get_edge(i, j) < math.inf:
                    self.set(i, j, k, i)
                else:
                    self.set(i, j, k, None)


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
        self.init_structures()
        for k in range(1, self.n):
            for i in range(self.n):
                for j in range(self.n):
                    curr_dist = self.d.get(i, j, k - 1)
                    dist_with_intermediate = self.d.get(i, k - 1, k - 1) + self.d.get(k - 1, j, k - 1)
                    if curr_dist <= dist_with_intermediate:
                        w = curr_dist
                        v = self.pred.get(i, j, k - 1)
                    else:
                        w = dist_with_intermediate
                        v = self.pred.get(k - 1, j, k - 1)
                    self.pred.set(i, j, k, v)
                    self.d.set(i, j, k, w)

    def init_structures(self):
        self.d = ShortestPathMatrices(self.n)
        self.d.copy_matrix(0, self.graph)
        self.pred = PredecessorsMatrices(self.n)
        self.pred.init_matrix(0, self.graph)
