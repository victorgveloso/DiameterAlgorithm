from pytest import fixture

from diameter.algorithms.diameter import DiameterAlgorithm


@fixture
def algorithm():
    input_ = '''4 3
1 2 1
2 3 2
3 4 3'''
    graph = DiameterAlgorithm.from_str(input_)
    graph.apply()
    return graph


def test_max(algorithm: DiameterAlgorithm):
    assert algorithm.max == (0, 3)
    assert algorithm.d.get_last(*algorithm.max) == 6


def test_diameter_value(algorithm: DiameterAlgorithm):
    assert algorithm.diameter_value() == 6


def test_diameter_vertices(algorithm: DiameterAlgorithm):
    assert algorithm.diameter_vertices() == (1, 4)


def test_diameter_shortest_path(algorithm: DiameterAlgorithm):
    assert algorithm.minimum_path_vertices() == [1, 2, 3, 4]


def test_diameter_shortest_path_size(algorithm: DiameterAlgorithm):
    assert algorithm.minimum_path_size() == 4
