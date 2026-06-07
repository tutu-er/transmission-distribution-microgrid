"""最大内估计 MIA — 全项目唯一 LP 实现 (§3.3, 算法 3.1).

编写位置
--------
* **本文件** — ``solve_mia`` / ``fit_mia``（LP 内核与输出 Polytope）
* ``vpp_standard.build_mia_template`` — 固定 ``A``（``with_cost`` 开关）
* ``batch_projection.build_batch_projection_target`` — 投影目标（含/不含物理成本）
* ``hierarchical.aggregate_by_type`` — 分批调用 ``fit_mia``

模板
----
* ``with_cost=False`` — 仅可行域行（Ch2 ESS 拟合、纯功率初级聚合）
* ``with_cost=True``  — 含 ``A_cost`` 行；``b`` 中成本截距由 MIA 优化（批量初级聚合）
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Literal

import numpy as np

from tdm.models.cost_epigraph import build_der_participation_model
from tdm.models.der.base import Parameters, build_B, build_xi, get_tau
from tdm.models.der.dg import build_dg_polytope
from tdm.models.der.ess import build_ess_polytope
from tdm.models.der.ev import build_ev_polytope
from tdm.models.der.hvac import build_hvac_polytope
from tdm.models.der.participation_rhs import (
    ParticipationRhs,
    build_cost_A,
    build_participation_rhs,
)
from tdm.models.der.pv_wt import build_pv_polytope
from tdm.models.der.units import N_PRICE_SEGMENTS
from tdm.models.polytope import Polytope
from tdm.models.vpp_standard import MiaTemplate

from gurobipy import GRB, Model, quicksum

DerType = Literal["dg", "ess", "ev", "hvac", "pv", "wt"]

_PORT_POWER_BUILDERS: dict[DerType, Callable[[Parameters], Polytope]] = {
    "dg": build_dg_polytope,
    "pv": build_pv_polytope,
    "wt": build_pv_polytope,
    "hvac": build_hvac_polytope,
    "ev": build_ev_polytope,
}


def build_cost_part_A(T: int, *, with_state: bool = True) -> np.ndarray:
    """标准模板成本块；与 ``participation_rhs.build_cost_A`` 共用实现."""
    return build_cost_A(T, with_state=with_state)


def _build_feasibility_A(T: int) -> np.ndarray:
    """可行域块 (式 3.32)：仅 P 为决策变量，状态界经 B 映射."""
    xi = build_xi(T)
    B = build_B(T)
    return np.vstack([np.eye(T), -np.eye(T), xi, -xi, B, -B])



@dataclass(frozen=True)
class ProjectionTarget:
    """单台 DER 投影目标：供 ``der/*.py`` 直接使用的 ``parameters``.

    不含 ``G,h``；可行域由 ``build_*_polytope(parameters)`` 在 ``build_der_constraints``
    内按需构造。ESS 原生变量为 ``[P_in; P_out]``，模板净功率 ``P = P_out − P_in``.
    """

    der_type: DerType
    parameters: Parameters
    power_f: np.ndarray | None = None
    state_g: np.ndarray | None = None

    def __post_init__(self) -> None:
        if self.power_f is not None:
            pf = np.asarray(self.power_f, dtype=float)
            if pf.shape[1] != N_PRICE_SEGMENTS:
                raise ValueError(f"power_f 第二维须为 {N_PRICE_SEGMENTS}")
            object.__setattr__(self, "power_f", pf)
        if self.state_g is not None:
            sg = np.asarray(self.state_g, dtype=float)
            if sg.shape[1] != N_PRICE_SEGMENTS:
                raise ValueError(f"state_g 第二维须为 {N_PRICE_SEGMENTS}")
            object.__setattr__(self, "state_g", sg)

    @property
    def tau(self) -> int:
        return get_tau(self.parameters)


def solve_mia(A: np.ndarray, targets: Sequence[ProjectionTarget]) -> np.ndarray:
    """算法 3.1：固定 ``A``，在投影目标下最大化右端 ``b``（内估计）.

    TODO: Phase 4.2
      - 建立 LP：变量 b，目标 max 1'b（或分块加权）
      - 内估计包含约束：目标多面体 ⊆ {x | A x ≤ b}
      - ``target.with_cost`` 为 False 时，仅优化可行域行；成本行可固定/屏蔽
      - ``target.with_cost`` 为 True 时，成本行 b 参与优化（物理成本进目标）
    """
    raise NotImplementedError

def construct_A(have_cost: bool, T: int, *, with_state_cost: bool = True) -> np.ndarray:
    """完整模板 A (式 3.32)；含 cost 时 vstack [A_cost; 0, A_feas]，ψ 列前置."""
    A_feas = _build_feasibility_A(T)
    if not have_cost:
        return A_feas
    A_cost = build_cost_part_A(T, with_state=with_state_cost)
    n_psi = A_cost.shape[1] - A_feas.shape[1]
    pad = np.zeros((A_feas.shape[0], n_psi))
    return np.vstack([A_cost, np.hstack([pad, A_feas])])


def initial_solve(
    i: int,
    T: int,
    A: np.ndarray,
    targets: Sequence[ProjectionTarget],
    *,
    with_cost: bool = True,
) -> np.ndarray:
    """初值/可行性探测：为每台 DER 建立模板坐标约束 (ψ, P)."""

    if A.shape[1] != 3 * T:
        raise ValueError(f"含成本模板 A 须为 {3 * T} 列，得到 {A.shape[1]}")

    model = Model(f"mia_init_{i}")
    model.Params.OutputFlag = 0
    x = model.addVars(3 * T, lb=-GRB.INFINITY, name=f"x_tpl_{i}")

    p_list = []
    psi_p_list = []
    psi_s_list = []
    for idx, der in enumerate(targets):
        if der.tau != T:
            raise ValueError(f"targets[{idx}].tau={der.tau} 与 T={T} 不一致")
        psi_p = model.addVars(T, lb=-GRB.INFINITY, name=f"psi_p_{idx}")
        psi_s = model.addVars(T, lb=-GRB.INFINITY, name=f"psi_s_{idx}")
        p = model.addVars(T, lb=-GRB.INFINITY, name=f"p_{idx}")
        p_list.append(p); psi_p_list.append(psi_p); psi_s_list.append(psi_s);
        build_der_constraints(model, der, T, psi_p, psi_s, p, idx=idx, with_cost=with_cost)

    model.addConstr(x[0:T] == quicksum(psi_p_list[idx] for idx in range(len(targets))))
    model.addConstr(x[T:2*T] == quicksum(psi_s_list[idx] for idx in range(len(targets))))
    model.addConstr(x[2*T:3*T] == quicksum(p_list[idx] for idx in range(len(targets))))

    model.optimize( - A[i, :] @ x)
    if model.Status != GRB.OPTIMAL:
        raise RuntimeError(f"initial_solve 未得最优解，status={model.Status}")
    return A[i, :] @ x.X


def _resolve_rhs(der: ProjectionTarget, *, with_state: bool) -> ParticipationRhs:
    if der.power_f is not None or der.state_g is not None:
        return ParticipationRhs(
            der.tau,
            der.power_f,
            der.state_g if with_state else None,
            "direct",
        )
    return build_participation_rhs(der.parameters, with_state=with_state)


def _add_polytope_le(model, poly: Polytope, var_blocks: Sequence) -> None:
    """把 ``Polytope(A,b)`` 逐行写入 Gurobi：``A x ≤ b``."""
    from gurobipy import quicksum

    cols = [var_blocks[i][t] for i in range(len(var_blocks)) for t in range(len(var_blocks[i]))]
    if len(cols) != poly.A.shape[1]:
        raise ValueError(
            f"变量列数 {len(cols)} 与 A 列数 {poly.A.shape[1]} 不一致"
        )
    for row in range(poly.A.shape[0]):
        model.addConstr(
            quicksum(float(poly.A[row, j]) * cols[j] for j in range(poly.A.shape[1]))
            <= float(poly.b[row])
        )


def build_der_constraints(
    model,
    der: ProjectionTarget,
    T: int,
    psi_p,
    psi_s,
    p,
    *,
    idx: int = 0,
    with_cost: bool = True,
) -> None:
    """调用 ``der/*.py`` + ``cost_epigraph`` 的 H 表示，写入 Gurobi 约束."""
    # 是否含状态成本 g：由 parameters / state_g 决定，非 der_type 硬编码
    with_state_cost = der.state_g is not None or (
        build_participation_rhs(der.parameters, with_state=True).state_g is not None
    )
    use_state_epigraph = with_cost and with_state_cost

    if der.der_type == "ess":
        # ESS (A.13)：原生变量 [P_in; P_out]，模板净功率 P = P_out − P_in
        ess_poly = build_ess_polytope(der.parameters)
        p_in = model.addVars(T, lb=0.0, name=f"p_in_{idx}")
        p_out = model.addVars(T, lb=0.0, name=f"p_out_{idx}")
        model.addConstrs((p[t] == p_out[t] - p_in[t] for t in range(T)))
        # 列序与 build_ess_polytope 一致：[P_in(τ), P_out(τ)]
        _add_polytope_le(model, ess_poly, [p_in, p_out])
        if with_cost:
            rhs = _resolve_rhs(der, with_state=use_state_epigraph)
            cost_poly = Polytope.from_ab(
                build_cost_A(T, with_state=use_state_epigraph),
                rhs.b_cost(),
            )
            ncol = cost_poly.A.shape[1]
            blocks = [psi_p, psi_s, p] if ncol == 3 * T else [psi_p, p]
            _add_polytope_le(model, cost_poly, blocks)
    else:
        builder = _PORT_POWER_BUILDERS.get(der.der_type)
        if builder is None:
            raise ValueError(f"未知 der_type: {der.der_type}")
        power_poly = builder(der.parameters)
        if with_cost:
            rhs = _resolve_rhs(der, with_state=use_state_epigraph)
            poly = build_der_participation_model(
                der.parameters,
                power_poly,
                with_state=use_state_epigraph,
                rhs=rhs,
            )
        else:
            poly = power_poly

        ncol = poly.A.shape[1]
        if ncol == T:
            blocks = [p]
        elif ncol == 2 * T:
            blocks = [psi_p, p]
        elif ncol == 3 * T:
            blocks = [psi_p, psi_s, p]
        else:
            raise ValueError(f"不支持的 A 列数 {ncol}（T={T}）")
        _add_polytope_le(model, poly, blocks)

    # 未写入状态成本行时，状态成本上境恒为 0
    if not use_state_epigraph:
        model.addConstrs((psi_s[t] == 0.0 for t in range(T)))


def fit_mia(targets: Sequence[ProjectionTarget], template: MiaTemplate) -> Polytope:
    """``solve_mia`` → ``Polytope(template.A, b)``."""
    # TODO: Phase 4.2 — 校验 targets 与 template.with_cost 一致
    # b = solve_mia(template.A, targets)
    # return Polytope.from_ab(template.A, b)
    raise NotImplementedError
