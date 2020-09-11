import math
from typing import Union, Optional

from diameter.model.graph import AdjacencyMatrix


class Matrices:
    """
    A base class for Shortest Path output structures (both contain N square matrices of size N).

    It's optimized for space and time complexity (using two unidimensional lists instead of N bidimensional ones).
    """

    def __init__(self, n, default_value=None):
        """
        Main constructor for Matrices

        :param n: Square matrices' size
        :param default_value: Symbol/Text by which empty cells should be represented
        """
        self.last = -1
        self._next_matrix = []
        self._prev_matrix = []
        self._default_value = default_value

        self.n = n

    def __str__(self):
        """
        A textual representation of the nth matrix

        :return: A string containing the elements from the last matrix
        """

        def formatted(v):
            if v is None:
                return 'NIL'
            else:
                return str(v)

        arr = (map(formatted, self._next_matrix[i:i + self.n]) for i in range(0, len(self._next_matrix), self.n))
        return "\n".join(map('\t'.join, arr))

    def get_last(self, i, j) -> Union[int, float]:
        """
        Getter for a cell from the nth matrix whose position is specified

        :param i: cell's row number
        :param j: cell's column number
        :return: cell or default_value (value representing empty cell)
        """
        return self._next_matrix[self._get_pos(i, j)]

    def _get_pos(self, i, j):
        """
        Convert from bidimensional to unidimensional index

        :param i: first dimension's index
        :param j: second dimension's index
        :return: an unique unidimensional index equivalent to (i,j)
        """
        return i * self.n + j

    def get(self, i, j, k) -> Union[int, float]:
        """
        Getter for a cell whose position and matrix-index are specified

        :param i: cell's row number
        :param j: cell's column number
        :param k: matrix-index where cell is located
        :return: cell or default_value (value representing empty cell)
        """
        pos = self._get_pos(i, j)
        return self._next_matrix[pos] if k == self.last else self._prev_matrix[pos]

    def set(self, i, j, k, w):
        """
        Setter for a given cell on a given matrix

        :param i: cell's row number
        :param j: cell's column number
        :param k: matrix-index where cell is located
        :param w: new weight cell should be set
        """
        if k > self.last:
            self.last = k
            self._prev_matrix = self._next_matrix
            self._next_matrix = [self._default_value] * (self.n ** 2)
        self._next_matrix[self._get_pos(i, j)] = w


class ShortestPathMatrices(Matrices):
    """
    A specialization of :class:`.Matrices` for shortest-path matrix representation
    """

    def __init__(self, n):
        super().__init__(n, default_value=math.inf)

    def copy_matrix(self, k, matrix: AdjacencyMatrix):
        for i in range(self.n):
            for j in range(self.n):
                self.set(i, j, k, matrix.get_edge(i, j))


class PredecessorsMatrices(Matrices):
    """
    A specialization of :class:`.Matrices` for predecessors matrix representation
    """

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
    """
    An implementation of the FloydWarshall Algorithm
    """

    def __init__(self, w: AdjacencyMatrix):
        """
        Initial configuration required for FloydWarshall execution

        :param w: The input graph
        """
        self.graph = w
        self.n: int = self.graph.n_vertices
        self.d: Optional[ShortestPathMatrices] = None
        self.pred: Optional[PredecessorsMatrices] = None
        self._applied = False

    @classmethod
    def from_str(cls, input_path: str, directed: bool = True):
        """
        An static factory method that reads input graph from a file

        :param input_path: Path to input graph description file
        :param directed: A flag indicating whether the graph is directed or not
        :return: A configured object of FloydWarshall ready to be applied
        """
        graph = AdjacencyMatrix.from_str(input_path, directed=directed)
        return cls(graph)

    def apply(self):
        """
        FloydWarshall's main method. It can be used only once, otherwise it'll raise RuntimeError.
        """
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
        """
        Output structures (shortest-path matrices and predecessors matrices) initialization.
        """
        self.d = ShortestPathMatrices(self.n)
        self.d.copy_matrix(0, self.graph)
        self.pred = PredecessorsMatrices(self.n)
        self.pred.init_matrix(0, self.graph)
