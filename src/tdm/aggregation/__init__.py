"""VPP 资源聚合 (论文第 3 章).

模块职责
--------
mia.py
    ★ 唯一 MIA 实现: solve_mia, fit_to_template, primary_aggregate
batch_projection.py
    批量标准投影目标 (3.6)(3.7)；不含 MIA 求解
hierarchical.py
    分层编排: 分组 → 初级 MIA → 次级 Σb
minkowski.py
    次级代数聚合: 同 A 下 b_VPP = Σ b_g

典型调用链
----------
aggregate_vpp (hierarchical)
  → primary_aggregate (mia) × 每批
       → build_batch_projection_problem (batch_projection)
       → solve_mia (mia)
  → algebraic_minkowski_sum (minkowski)

Ch2 单体 ESS 拟合不走本包编排，但同样调用 mia.fit_to_template。
几何投影 (FME) 在 models/projection.py，与 batch_projection 无关。
"""

from tdm.aggregation.batch_projection import (
    build_batch_projection_problem,
    embed_period_heterogeneity,
)
from tdm.aggregation.minkowski import algebraic_minkowski_sum, minkowski_sum

__all__ = [
    "algebraic_minkowski_sum",
    "build_batch_projection_problem",
    "embed_period_heterogeneity",
    "minkowski_sum",
]

# Phase 4/5 完成后取消注释:
# from tdm.aggregation.hierarchical import aggregate_vpp
# from tdm.aggregation.mia import fit_to_template, primary_aggregate, solve_mia
