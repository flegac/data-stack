from abc import ABC, abstractmethod

import numpy as np
from easy_kit.timing import timing
from scipy.spatial import KDTree


class Spatial(ABC):
    def __init__(self, points: np.ndarray): ...

    @abstractmethod
    def search_in_radius(self, center, radius: float): ...


class KDTreeSpatial(Spatial):
    def __init__(self, points: np.ndarray):
        super().__init__(points)
        self.tree = KDTree(points)

    def search_in_radius(self, center, radius: float):
        return self.tree.query_ball_point(center, radius)


def poisson_disk_sampling(
    points: np.ndarray,
    min_distance: float,
    spatial: type[Spatial] = KDTreeSpatial,
) -> set[int]:
    with timing(f"pds_{spatial.__name__}({min_distance:.2f})"):
        if min_distance == 0.0:
            return set(range(len(points)))
        tree = spatial(points)

        selection: set[int] = set()
        candidates = list(range(len(points)))
        np.random.shuffle(candidates)
        excluded = set()

        for idx in candidates:
            current_point = points[idx]
            if idx in excluded:
                continue

            # Trouver les points voisins dans un rayon de 2 * min_distance
            indices = tree.search_in_radius(current_point, 2 * min_distance)

            # Vérifier si le point actuel est suffisamment éloigné des points échantillonnés
            if not selection.intersection(indices):
                selection.add(idx)
                excluded.update(indices)
        print(
            f"pds_{spatial.__name__}({min_distance:.2f}): points={len(selection)}/{len(points)}"
        )
        return selection
