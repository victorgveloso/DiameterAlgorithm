import pytest
from pytest import fixture

from diameter.model.graph import AdjacencyMatrix


@fixture
def graph():
    input_ = '''4 3
1 2 1
2 3 2
3 4 3'''
    return AdjacencyMatrix.from_str(input_)


def test_weight(graph):
    assert graph.get_edge(0, 1) == 1
    assert graph.get_edge(1, 2) == 2
    assert graph.get_edge(2, 3) == 3


def test_sizes(graph):
    assert graph.n_vertices == 4
    assert graph.m_edges == 3


def test_place_exceeding_edge(graph):
    with pytest.raises(ValueError) as er:
        graph.place_edge(3, 1, 4)
        assert "All edges have been placed" in str(er.value)


def test_remaining_edges_placing():
    with pytest.raises(ValueError) as er:
        AdjacencyMatrix(4, 4).get_edge(1, 2)
        assert "edges left unplaced" in str(er.value)
