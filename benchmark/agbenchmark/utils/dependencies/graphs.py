import math
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from pyvis.network import Network

from agbenchmark.generate_test import DATA_CATEGORY
from agbenchmark.utils.utils import write_pretty_json


def bezier_curve(src: np.ndarray, ctrl: List[float], dst: np.ndarray) -> List[np.ndarray]:
    curve = []
    for t in np.linspace(0, 1, num=100):
        curve_point = (
            np.outer((1 - t) ** 2, src)
            + 2 * np.outer((1 - t) * t, ctrl)
            + np.outer(t**2, dst)
        )
        curve.append(curve_point[0])
    return curve


def curved_edges(G: nx.Graph, pos: Dict[Any, Tuple[float, float]], dist: float = 0.2) -> None:
    ax = plt.gca()
    for u, v, data in G.edges(data=True):
        src = np.array(pos[u])
        dst = np.array(pos[v])

        same_level = abs(src[1] - dst[1]) < 0.01

        if same_level:
            control = [(src[0] + dst[0]) / 2, src[1] + dist]
            curve = bezier_curve(src, control, dst)
            arrow = patches.FancyArrowPatch(
                posA=curve[0],  # type: ignore
                posB=curve[-1],  # type: ignore
              
