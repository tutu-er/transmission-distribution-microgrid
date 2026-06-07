"""批量标准投影目标 (§3.2, 式 3.6–3.7) — 不含 MIA 求解.

每台 DER 输出一条 ``ProjectionTarget(der_type, parameters, …)``，供 ``solve_mia`` 数组合并。
"""

from __future__ import annotations

import numpy as np

from tdm.aggregation.mia import DerType, ProjectionTarget
from tdm.models.der.base import Parameters


def build_projection_targets(
    der_type: DerType,
    parameters_list: list[Parameters],
    *,
    with_cost: bool = False,
) -> list[ProjectionTarget]:
    """一批同类型 DER → ``ProjectionTarget`` 数组（每台一条）.

    TODO: Phase 4.1
      - 每台 DER 封装 ``ProjectionTarget(der_type, parameters)``
      - ESS 保留完整 parameters（``build_ess_polytope`` 用 [P_in; P_out]）
      - EV：``embed_period_matrix`` 嵌入时段后再构造 parameters (3.7b)
    """
    raise NotImplementedError


def embed_period_matrix(tau_start: int, tau_end: int, tau_total: int) -> np.ndarray:
    """EV 等时段异质性嵌入矩阵 M_k (3.7b)."""
    # TODO: Phase 4.4
    raise NotImplementedError
