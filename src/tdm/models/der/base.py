"""DER 公共矩阵构造与参数工具 (附录 A.1).

统一单位约定 (见 ``der.units``):
    - 端口功率 P: MW
    - 储能能量 E / VPP 状态 S: MWh
    - 爬坡 R: MW/h
    - 时间步长 delta_tau: h
    - HVAC 温度 T / 环境温度 omega: °C
    - HVAC 系数 alpha: °C/(MW·h)
"""

from __future__ import annotations

from typing import Any

import numpy as np

Parameters = dict[str, Any]


def get_tau(parameters: Parameters) -> int:
    """时段数 τ = τ_end - τ_start."""
    return int(parameters["tau_end"] - parameters["tau_start"])


def build_xi(tau: int) -> np.ndarray:
    """爬坡差分矩阵 Ξ ∈ R^{(τ-1)×τ} (附录 A.2)."""
    if tau < 1:
        raise ValueError("tau 必须 >= 1")
    if tau == 1:
        return np.zeros((0, 1))
    return np.eye(tau)[: tau - 1] - np.eye(tau, k=1)[: tau - 1]


def build_phi(tau: int, eta: float) -> tuple[np.ndarray, np.ndarray]:
    """状态递推矩阵 Φ 及其首列 Φ_1 (附录 A.3)."""
    i, j = np.indices((tau, tau))
    phi = np.where(i >= j, eta ** (i - j), 0.0)
    phi_1 = phi[:, [0]]
    return phi, phi_1


def base_polytope(parameters: Parameters) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """返回 (Ξ, Φ, Φ_1)，兼容旧接口命名 Theta/Lambda/Lambda_1."""
    tau = get_tau(parameters)
    eta = float(parameters["eta"])
    xi = build_xi(tau)
    phi, phi_1 = build_phi(tau, eta)
    return xi, phi, phi_1
