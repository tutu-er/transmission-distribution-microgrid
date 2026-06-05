"""DG 功率可行域 (附录 A.3). 功率: MW, 爬坡: MW/h."""

from __future__ import annotations

import numpy as np

from tdm.models.der.base import Parameters, base_polytope, get_tau
from tdm.models.polytope import Polytope


def build_dg_polytope(parameters: Parameters) -> Polytope:
    """构建 DG 端口功率可行域，含爬坡约束 (A.7)."""
    tau = get_tau(parameters)
    p_max = np.asarray(parameters["P_max"], dtype=float).reshape(-1)
    p_min = np.asarray(parameters["P_min"], dtype=float).reshape(-1)
    r_up = np.asarray(parameters["R_up"], dtype=float).reshape(-1)
    r_down = np.asarray(parameters["R_down"], dtype=float).reshape(-1)

    xi, _, _ = base_polytope(parameters)

    a = np.concatenate([np.eye(tau), -np.eye(tau), xi, -xi], axis=0)
    b = np.concatenate([p_max, -p_min, r_up, -r_down], axis=0)
    return Polytope.from_ab(a, b)


# 兼容旧函数名
DG_polytope = build_dg_polytope
