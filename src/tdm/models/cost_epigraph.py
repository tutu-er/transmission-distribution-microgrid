"""功率-成本参与模型组装 (§2.4, 式 2.28).

``participation_rhs`` 提供固定 ``A_cost, b_cost``；``der/*.py`` 提供 ``A_p, b_p``；
本模块负责拼接::

    A = [A_cost;  0, A_p] ,   b = [b_cost; b_p]

变量 x 前导列为 ψ（成本上境），后接 P；状态成本经 B 映射写入 P 列，与 ``build_cost_A`` 列序一致。
"""

from __future__ import annotations

import numpy as np

from tdm.models.der.base import Parameters, get_tau
from tdm.models.der.participation_rhs import (
    ParticipationRhs,
    build_cost_A,
    build_participation_rhs,
)
from tdm.models.polytope import Polytope


def stack_participation_h(
    A_cost: np.ndarray,
    b_cost: np.ndarray,
    A_p: np.ndarray,
    b_p: np.ndarray,
) -> Polytope:
    """``[A_cost; 0, A_p] x ≤ [b_cost; b_p]``，``A_cost`` 列数 = ``n_ψ + A_p.shape[1]``."""
    A_cost = np.asarray(A_cost, dtype=float)
    b_cost = np.asarray(b_cost, dtype=float).reshape(-1)
    A_p = np.asarray(A_p, dtype=float)
    b_p = np.asarray(b_p, dtype=float).reshape(-1)
    n_psi = A_cost.shape[1] - A_p.shape[1]
    if n_psi < 0:
        raise ValueError("A_cost 列数须不少于 A_p 列数")
    pad = np.zeros((A_p.shape[0], n_psi))
    A = np.vstack([A_cost, np.hstack([pad, A_p])])
    b = np.concatenate([b_cost, b_p])
    return Polytope.from_ab(A, b)


def build_der_participation_model(
    parameters: Parameters,
    power_poly: Polytope,
    *,
    with_state: bool = False,
    rhs: ParticipationRhs | None = None,
) -> Polytope:
    """单体 DER：``A_cost,b_cost`` + 功率可行 ``A_p,b_p`` → 完整 H 表示."""
    tau = get_tau(parameters)
    rhs = rhs or build_participation_rhs(parameters, with_state=with_state)
    return stack_participation_h(
        build_cost_A(tau, with_state=with_state),
        rhs.b_cost(),
        power_poly.A,
        power_poly.b,
    )


