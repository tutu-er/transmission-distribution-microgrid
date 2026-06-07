"""VPP 资源聚合 (论文第 3 章)."""

from tdm.aggregation.batch_projection import build_projection_targets, embed_period_matrix
from tdm.aggregation.mia import DerType, ProjectionTarget, fit_mia, solve_mia
from tdm.aggregation.minkowski import algebraic_minkowski_sum, minkowski_sum

__all__ = [
    "DerType",
    "ProjectionTarget",
    "algebraic_minkowski_sum",
    "build_projection_targets",
    "embed_period_matrix",
    "fit_mia",
    "minkowski_sum",
    "solve_mia",
]
