from agbenchmark.utils.dependencies.graphs import get_roots
from typing import Dict, Set

def test_get_roots() -> None:
    """Test the get_roots function with a simple graph."""
    graph: Dict = {
        "nodes": [
            {"id": "A", "data": {"category": []}},
            {"id": "B", "data": {"category": []}},
            {"id": "C", "data": {"category": []}},
            {"id": "D", "data": {"category": []}},
        ],
        "edges": [
            {"from": "A", "to": "B"},
            {"from": "B", "to": "C"},
        ],
    }

    result: Set[str] = get_roots(graph)
    expected_result: Set[str] = {"A", "D"}
    assert result == expected_result, (
        f"Expected roots to be {expected_result}, but got {result}"
    )


def test_no_roots() -> None:
    """Test the get_roots function with a fully connected graph."""
    graph: Dict = {
        "nodes": [
            {"id": "A", "data": {"category": []}},
            {"id": "B", "data": {"category": []}},
            {"id": "C", "data": {"category": []}},
        ],
        "edges": [
            {"from": "A", "to": "B"},
            {"from": "B", "to": "C"},
            {"from": "C", "to": "A"},
        ],
    }

    result: Set[str] = get_roots(graph)
    assert not result, "Expected no roots, but found some"


def test_no_roots_empty_graph() -> None:
    """Test the get_roots function with an empty graph."""
    graph: Dict = {
        "nodes": [],
        "edges": [],
    }

    result: Set[str] = get_roots(
