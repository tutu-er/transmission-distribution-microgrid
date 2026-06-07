"""参与模板成本块 (§2.28, 式 3.32 成本行)：固定 ``A_cost`` 与 ``b_cost``.

约束（功率成本行）::

    −ψ_{P,t} + F*_k·P_t ≤ −f_{t,k}

含状态成本时 S 不显式入列，经 B 映射 (式 3.33d) S = B P::

    −ψ_{S,t} + G*_k·(B P)_t ≤ −g_{t,k}

变量顺序（与 ``cost_epigraph.stack_participation_h`` 拼接约定）::

    仅功率成本:  x = [ψ_P(τ), P(τ)]
    含状态成本:  x = [ψ_P(τ), ψ_S(τ), P(τ)]

本模块**不**含功率界/爬坡/状态界；上层执行 ``[A_cost; 0, A_p] x ≤ [b_cost; b_p]``。
``A_p`` 通常仅作用于 P 列（如 HVAC 已消去物理状态）。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np

from tdm.models.der.base import Parameters, build_B, get_tau
from tdm.models.der.cost import (
    PhysicalCostModel,
    _comfort_temperature,
    _param_at_t,
    _quadratic_coeff,
    build_physical_cost,
)
from tdm.models.der.units import N_PRICE_SEGMENTS, PRICE_SEGMENTS_MWH

RhsSource = Literal["direct", "mia"]
_SEG = np.array(PRICE_SEGMENTS_MWH, dtype=float)


@dataclass(frozen=True)
class ParticipationRhs:
    """成本截距 f,g（形状 τ×n_seg）；``b_cost = −flatten(f[, g])``."""

    tau: int
    power_f: np.ndarray | None
    state_g: np.ndarray | None
    source: RhsSource

    def b_cost(self) -> np.ndarray:
        if self.power_f is None:
            raise ValueError("mia 路径截距未确定，需 solve_mia 后 resolve")
        parts = [-np.asarray(self.power_f, dtype=float).reshape(-1)]
        if self.state_g is not None:
            parts.append(-np.asarray(self.state_g, dtype=float).reshape(-1))
        return np.concatenate(parts)


def build_cost_A(tau: int, *, with_state: bool = False) -> np.ndarray:
    """固定成本模板 ``A_cost``（系数含 F*/G*，状态成本经 G*·B 作用在 P 上）."""
    n_seg = N_PRICE_SEGMENTS
    if not with_state:
        a = np.zeros((tau * n_seg, 2 * tau))
        for t in range(tau):
            for k, fk in enumerate(_SEG):
                row = t * n_seg + k
                a[row, t] = -1.0
                a[row, tau + t] = fk
        return a
    B = build_B(tau)
    a = np.zeros((2 * tau * n_seg, 3 * tau))
    p0 = 2 * tau
    for t in range(tau):
        for k, fk in enumerate(_SEG):
            rp = t * n_seg + k
            a[rp, t] = -1.0
            a[rp, p0 + t] = fk
            rs = tau * n_seg + t * n_seg + k
            a[rs, tau + t] = -1.0
            a[rs, p0 : p0 + tau] = fk * B[t]
    return a


def build_participation_rhs(
    parameters: Parameters,
    *,
    rhs_source: RhsSource = "direct",
    with_state: bool = False,
) -> ParticipationRhs:
    tau = get_tau(parameters)
    if rhs_source == "mia":
        return ParticipationRhs(tau, None, None, "mia")
    pf = fit_direct_intercepts(build_physical_cost(parameters, kind="power"))
    sg = None
    if with_state:
        ps = build_physical_cost(parameters, kind="state")
        if ps.kind != "zero":
            sg = fit_direct_intercepts(ps)
    return ParticipationRhs(tau, pf, sg, "direct")


def resolve_mia(rhs: ParticipationRhs, power_f: np.ndarray, state_g: np.ndarray | None = None) -> ParticipationRhs:
    if rhs.source != "mia":
        raise ValueError("仅 mia 占位可 resolve")
    return ParticipationRhs(rhs.tau, np.asarray(power_f, dtype=float), state_g, "mia")


def fit_direct_intercepts(physical: PhysicalCostModel, slopes: np.ndarray | None = None) -> np.ndarray:
    slopes = _SEG if slopes is None else np.asarray(slopes, dtype=float).reshape(-1)
    return np.vstack([_margin_row(physical, t, slopes) for t in range(physical.tau)])


def _margin_row(physical: PhysicalCostModel, t: int, slopes: np.ndarray) -> np.ndarray:
    x_lo, x_hi = physical.domain_at(t)
    h = physical.evaluate_period
    xs = [x_lo, x_hi]
    if physical.kind == "abs_power" and x_lo < 0.0 < x_hi:
        xs.append(0.0)
    elif physical.kind == "comfort_state":
        tc = float(_comfort_temperature(physical.parameters, physical.tau)[t])
        if x_lo < tc < x_hi:
            xs.append(tc)
    p = physical.parameters
    rows = []
    for F in slopes:
        F = float(F)
        x_star = None
        if physical.kind == "quadratic_power":
            x_star = (F - _param_at_t(p, "unit_cost", t, default=0.0)) / (2.0 * _quadratic_coeff(p, t))
        cand = list(xs)
        if x_star is not None and x_lo <= x_star <= x_hi:
            cand.append(x_star)
        rows.append(min(h(t, x) - F * x for x in cand))
    return np.array(rows)
