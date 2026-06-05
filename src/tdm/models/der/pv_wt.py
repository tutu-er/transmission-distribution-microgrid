"""PV / WT 功率可行域 (附录 A.2). 功率单位: MW."""

from __future__ import annotations

import numpy as np

from tdm.models.der.base import Parameters, get_tau
from tdm.models.polytope import Polytope


def build_pv_polytope(parameters: Parameters) -> Polytope:
    """构建 PV/WT 端口功率可行域 (A.5)."""
    tau = get_tau(parameters)
    p_max = np.asarray(parameters["P_max"], dtype=float).reshape(-1)
    p_min = np.asarray(parameters["P_min"], dtype=float).reshape(-1)

    a = np.concatenate([np.eye(tau), -np.eye(tau)], axis=0)
    b = np.concatenate([p_max, -p_min], axis=0)
    return Polytope.from_ab(a, b)


# 兼容旧函数名
PV_polytope = build_pv_polytope
WT_polytope = build_pv_polytope
