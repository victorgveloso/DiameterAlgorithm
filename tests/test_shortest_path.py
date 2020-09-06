import math

from pytest import fixture

from diameter.algorithms.shortest_path import FloydWarshall


@fixture
def floyd_warshall():
    input_ = '''4 3
1 2 1
2 3 2
3 4 3'''
    graph = FloydWarshall.from_str(input_)
    graph.apply()
    return graph


@fixture
def undirected_floyd_warshall():
    input_ = '''4 3
1 2 1
2 3 2
3 4 3'''
    graph = FloydWarshall.from_str(input_, directed=False)
    graph.apply()
    return graph


@fixture
def undirected_big_floyd_warshall():
    input_ = """5 8
2 4 64
2 5 62
3 5 41
1 5 40
2 3 70
1 3 62
1 2 4
4 5 99"""
    graph = FloydWarshall.from_str(input_, directed=False)
    graph.apply()
    return graph


def test_shortest_path_str(floyd_warshall: FloydWarshall):
    occurrences = {}
    shortest_path = floyd_warshall.d
    for i in str(shortest_path).split('\n'):
        for weight in i.split():
            if weight in occurrences:
                occurrences[weight] += 1
            else:
                occurrences[weight] = 1
    assert occurrences[str(math.inf)] == 6
    assert occurrences['0'] == 4
    assert occurrences['3'] == 2
    assert occurrences['1'] == occurrences['2'] == occurrences['5'] == occurrences['6'] == 1


def test_shortest_path(floyd_warshall: FloydWarshall):
    shortest_path = floyd_warshall.d
    assert shortest_path.get(0, shortest_path.n - 1) == 6


def test_predecessor(floyd_warshall: FloydWarshall):
    assert floyd_warshall.pred.get(2, 3) == 2
    assert floyd_warshall.pred.get(0, 3) == 2
    assert floyd_warshall.pred.get(1, 2) == 1
    assert floyd_warshall.pred.get(0, 2) == 1
    assert floyd_warshall.pred.get(0, 1) == 0


def test_shortest_path_undirected(undirected_floyd_warshall: FloydWarshall):
    occurrences = {}
    shortest_path = undirected_floyd_warshall.d
    for i in str(shortest_path).split('\n'):
        for weight in i.split():
            if weight in occurrences:
                occurrences[weight] += 1
            else:
                occurrences[weight] = 1
    assert str(math.inf) not in occurrences
    assert occurrences['0'] == 4
    assert occurrences['3'] == 4
    assert occurrences['1'] == occurrences['2'] == occurrences['5'] == occurrences['6'] == 2


def test_shortest_path_undirected_big_graph(undirected_big_floyd_warshall: FloydWarshall):
    shortest_path = undirected_big_floyd_warshall.d
    assert shortest_path.get(0, 4) == 40
    assert shortest_path.get(3, 4) == 99
    assert shortest_path.get(3, 2) == 130
