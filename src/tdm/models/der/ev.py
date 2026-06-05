"""EV 功率可行域 (附录 A.5). 功率: MW, 能量: MWh."""

from __future__ import annotations

import numpy as np

from tdm.models.der.base import Parameters, base_polytope, get_tau
from tdm.models.polytope import Polytope


def build_ev_polytope(parameters: Parameters) -> Polytope:
    """构建 EV 端口功率可行域，状态已代数消去 (A.11)."""
    tau = get_tau(parameters)
    p_max = np.asarray(parameters["P_max"], dtype=float).reshape(-1)
    p_min = np.asarray(parameters["P_min"], dtype=float).reshape(-1)
    e_max = np.asarray(parameters["E_max"], dtype=float).reshape(-1)
    e_min = np.asarray(parameters["E_min"], dtype=float).reshape(-1)
    e_0 = float(parameters["E_0"])
    alpha = float(parameters["alpha"])
    delta_tau = float(parameters["delta_tau"])
    eta = float(parameters["eta"])

    _, phi, phi_1 = base_polytope(parameters)

    a = np.concatenate([np.eye(tau), -np.eye(tau), alpha * phi, -alpha * phi], axis=0)
    state_upper = (1 / delta_tau) * (e_max - eta * e_0 * phi_1.ravel())
    state_lower = (1 / delta_tau) * (eta * e_0 * phi_1.ravel() - e_min)
    b = np.concatenate([p_max, -p_min, state_upper, state_lower], axis=0)
    return Polytope.from_ab(a, b)


# 兼容旧函数名
EV_polytope = build_ev_polytope
