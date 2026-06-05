"""HVAC 功率可行域 (附录 A.4). 功率: MW, 温度: °C, alpha: °C/(MW·h)."""

from __future__ import annotations

import numpy as np

from tdm.models.der.base import Parameters, base_polytope, get_tau
from tdm.models.polytope import Polytope


def build_hvac_polytope(parameters: Parameters) -> Polytope:
    """构建 HVAC 端口功率可行域，状态已代数消去 (A.9)."""
    tau = get_tau(parameters)
    p_max = np.asarray(parameters["P_max"], dtype=float).reshape(-1)
    p_min = np.asarray(parameters["P_min"], dtype=float).reshape(-1)
    t_max = np.asarray(parameters["T_max"], dtype=float).reshape(-1)
    t_min = np.asarray(parameters["T_min"], dtype=float).reshape(-1)
    t_0 = float(parameters["T_0"])
    omega = np.asarray(parameters["omega"], dtype=float).reshape(-1)
    alpha = float(parameters["alpha"])
    delta_tau = float(parameters["delta_tau"])
    eta = float(parameters["eta"])

    _, phi, phi_1 = base_polytope(parameters)

    a = np.concatenate([np.eye(tau), -np.eye(tau), alpha * phi, -alpha * phi], axis=0)
    state_upper = (1 / delta_tau) * (
        t_max - eta * t_0 * phi_1.ravel() - (1 - eta) * (phi @ omega)
    )
    state_lower = (1 / delta_tau) * (
        eta * t_0 * phi_1.ravel() + (1 - eta) * (phi @ omega) - t_min
    )
    b = np.concatenate([p_max, -p_min, state_upper, state_lower], axis=0)
    return Polytope.from_ab(a, b)


# 兼容旧函数名
HVAC_polytope = build_hvac_polytope
