"""几何投影与状态消去 (§2.3.2, §2.5.2.1) — 不含 MIA.

职责:
  - eliminate_state_by_gaussian: 状态方程代数消元
  - project_fourier_motzkin: 低维精确投影 (FME)
  - project_polytope: 子空间投影接口

MIA: 否。高维内估计改由 models/heterogeneity → aggregation/mia.fit_to_template。

与 aggregation/batch_projection.py 的区别:
  - 本模块: 单个多面体的变量消去 / 精确几何投影 (Ch2 验证)
  - batch_projection: 一批 DER 写成 Ch3 标准投影 LP 目标

典型路径:
  ess.build_ess_polytope
    → project_fourier_motzkin (低维验证)
    → 或 heterogeneity.eliminate_state_heterogeneity (高维 → 调用 mia)
"""

from __future__ import annotations

import numpy as np

from tdm.models.polytope import Polytope


def eliminate_state_by_gaussian(polytope: Polytope, state_dim: int) -> Polytope:
    """对含等式状态方程的模型，利用高斯消元消去状态维度."""
    # TODO
    ...


def project_polytope(polytope: Polytope, retain_dims: slice | np.ndarray) -> Polytope:
    """将高维多面体投影到指定子空间（低维优先 FME）."""
    # TODO: 低维 → project_fourier_motzkin；高维 → 委托 heterogeneity
    ...


def project_fourier_motzkin(polytope: Polytope, eliminate_dims: slice | np.ndarray) -> Polytope:
    """FME 精确投影（仅适用于低维场景）."""
    # TODO: §2.5.2.1 ESS 算例
    ...
