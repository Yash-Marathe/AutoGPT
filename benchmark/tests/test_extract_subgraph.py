import pytest
from typing import Dict, List, Tuple

from agbenchmark.utils.dependencies.graphs import extract_subgraph_based_on_category


def extract_subgraph_based_on_category(
    graph: Dict, category: str
) -> Tuple[List[Dict], List[Dict]]:
    """
    Extract a subgraph from the given graph based on the specified category.

    :param graph: The graph to extract the subgraph from.
    :param category: The category to filter the nodes and edges by.
    :return: A tuple containing the nodes and edges of the subgraph.
    """
    nodes = [node for node in graph["nodes"] if node["data"]["category"] == [category]]
    edges = [
        edge for edge in graph["edges"] if edge["from"] in [node["id"] for node in nodes]
    ]
    return nodes, edges


@pytest.fixture
def curriculum_graph() -> Dict:
    return {
        "edges": [
            {"from": "Calculus", "to": "Advanced Calculus"},
            {"from": "Algebra", "to": "Calculus"},
            {"from": "Biology", "to": "Advanced Biology"},
            {"from": "World History", "to": "Modern History"},
        ],
        "nodes": [
            {"data": {"category": ["math"]}, "id": "Calculus", "label": "Calculus"},
            {
                "data": {"category": ["math"]},
                "id": "Advanced Calculus",
                "label": "Advanced Calculus",
            },
            {"data": {"category": ["math"]}, "id": "Algebra", "label": "Algebra"},
            {"data": {"category": ["science"]}, "id": "Biology", "label": "Biology"},
            {
                "data": {"category": ["science"]},
                "id": "Advanced Biology",
                "label": "Advanced Biology",
            },
            {
                "data": {"category": ["history"]},
                "id": "World History",
                "label": "World History",
            },
            {
                "data": {"category": ["history"]},
                "id": "Modern History",
                "label": "Modern History",
            },
        ],
    }


graph_example = {
    "nodes": [
        {"id": "A", "data": {"category": []}},
        {"id": "B", "data": {"category": []}},
        {"id": "C", "data": {"category": ["math"]}},
    ],
    "edges": [{"from": "B", "to": "C"}, {"from": "A", "to": "C"}],
}


def test_dfs_category_math(curriculum_graph: dict) -> None:
    result_graph = extract_subgraph_based_on_category(curriculum_graph, "math")

    # Expected nodes: Algebra, Calculus, Advanced Calculus
    # Expected edges: Algebra->Calculus, Calculus->Advanced Calculus

    expected_nodes = ["Algebra", "Calculus", "Advanced Calculus"]
    expected_edges = [
        {"from": "Algebra", "to": "Calculus"},
        {"from": "Calculus", "to": "Advanced Calculus"},
    ]

    assert set(node["id"] for node in result_graph[0]) == set(expected_nodes)
    assert set((edge["from"], edge["to"]) for edge in result_graph[1]) == set(
        (edge["from"], edge["to"]) for edge in expected_edges
    )
    assert result_graph[0] == expected_nodes
    assert result_graph[1] == expected_edges


def test_extract_subgraph_math_category() -> None:
    subgraph = extract_subgraph_based_on_category(graph_example, "math")
    assert set(
        (node["id"], tuple(node["data"]["category"])) for node in subgraph[0]
    ) == set(
        (node["id"], tuple(node["data"]["category"])) for node in graph_example["nodes"]
    )
    assert set((edge["from"], edge["to"]) for edge in subgraph[1]) == set(
        (edge["from"], edge["to"]) for edge in graph_example["edges"]
    )
    assert subgraph
