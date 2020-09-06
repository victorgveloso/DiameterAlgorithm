from diameter.algorithms.diameter import DiameterAlgorithm
from diameter.model.graph import AdjacencyMatrix


def check_result(input_: str, expected_output: str):
    graph = DiameterAlgorithm(AdjacencyMatrix.from_str(input_, directed=False))
    graph.apply()
    assert graph.formatted_result() == expected_output


def test_small_input():
    input_ = """4 3
1 2 1
2 3 2
3 4 3"""
    expected_output = """6
1 4
4
1 2 3 4"""
    check_result(input_, expected_output)


def test_avg_input():
    input_ = """4 6
1 2 1
1 3 1
1 4 1
2 3 1
2 4 1
3 4 1"""
    expected_output = """1
1 2
2
1 2"""
    check_result(input_, expected_output)


def test_big_input():
    input_ = """5 8
2 4 64
2 5 62
3 5 41
1 5 40
2 3 70
1 3 62
1 2 4
4 5 99"""
    expected_output = """130
3 4
4
3 1 2 4"""
    check_result(input_, expected_output)
