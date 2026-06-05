"""ESS 功率可行域 (附录 A.6, 式 2.9, 2.12). 功率: MW, 能量: MWh.

已完成:
  [x] build_ess_polytope: 松弛模型 (2.9) H 表示，变量 [P_in; P_out]

TODO:
  [ ] apply_charge_discharge_correction: 叠加修正约束 (2.12)，§2.5.2.1 算例
  [ ] project_ess_to_port_power: [P_in;P_out] → 端口净功率 P (τ 维)
        低维 FME (models/projection) 或 heterogeneity → mia.fit_to_template
"""

from __future__ import annotations

import numpy as np

from tdm.models.der.base import Parameters, base_polytope, get_tau
from tdm.models.polytope import Polytope


def build_ess_polytope(parameters: Parameters, *, apply_correction: bool = False) -> Polytope:
    """构建 ESS 可行域 H 表示.

    变量 x = [P_in; P_out] ∈ R^{2τ}，净功率 P = P_out - P_in (A.13).
    apply_correction=True 时叠加充放电互斥修正约束 (2.12)（待实现）.
    """
    tau = get_tau(parameters)
    p_max = np.asarray(parameters["P_max"], dtype=float).reshape(-1)
    p_min = np.asarray(parameters["P_min"], dtype=float).reshape(-1)
    e_max = np.asarray(parameters["E_max"], dtype=float).reshape(-1)
    e_min = np.asarray(parameters["E_min"], dtype=float).reshape(-1)
    e_0 = float(parameters["E_0"])
    alpha_in = float(parameters["alpha_in"])
    alpha_out = float(parameters["alpha_out"])
    delta_tau = float(parameters["delta_tau"])
    eta = float(parameters["eta"])

    _, phi, phi_1 = base_polytope(parameters)
    i_tau = np.eye(tau)

    # Pin/Pout 能量约束（附录 A.6 第一组矩阵不等式）
    a_pin_pout = np.concatenate(
        [
            np.concatenate([alpha_in * phi, -alpha_out * phi], axis=1),
            np.concatenate([-alpha_in * phi, alpha_out * phi], axis=1),
        ],
        axis=0,
    )
    b_pin_pout = np.concatenate(
        [
            (1 / delta_tau) * (e_max - eta * e_0 * phi_1.ravel()),
            (1 / delta_tau) * (eta * e_0 * phi_1.ravel() - e_min),
        ],
        axis=0,
    )

    # 净功率 P = P_out - P_in 上下界
    a_power = np.concatenate(
        [
            np.concatenate([-i_tau, i_tau], axis=1),
            np.concatenate([i_tau, -i_tau], axis=1),
        ],
        axis=0,
    )
    b_power = np.concatenate([p_max, -p_min], axis=0)

    # 净功率 P 的凸松弛能量约束
    a_energy_p = np.concatenate([alpha_in * phi, -alpha_in * phi], axis=1)
    b_energy_p = (1 / delta_tau) * (e_max - eta * e_0 * phi_1.ravel())

    a = np.concatenate([a_pin_pout, a_power, a_energy_p], axis=0)
    b = np.concatenate([b_pin_pout, b_power, b_energy_p], axis=0)

    polytope = Polytope.from_ab(a, b)
    if apply_correction:
        polytope = apply_charge_discharge_correction(polytope, parameters)
    return polytope


def apply_charge_discharge_correction(polytope: Polytope, parameters: Parameters) -> Polytope:
    """叠加 ESS 充放电互斥修正约束 (2.12)."""
    raise NotImplementedError("ESS 充放电互斥修正约束 (2.12) 尚未实现")


def project_ess_to_port_power(polytope: Polytope, parameters: Parameters) -> Polytope:
    """将 ESS [P_in; P_out] 空间可行域投影到端口净功率 P 空间."""
    raise NotImplementedError("ESS 端口功率投影尚未实现")


# 兼容旧函数名
ESS_polytope = build_ess_polytope
