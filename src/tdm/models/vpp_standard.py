"""VPP 标准化参与模板 (§2.29–2.30, 式 3.32).

MIA 固定矩阵 ``A`` 由 ``build_mia_template`` 生成；右端 ``b`` 由 ``aggregation.mia.solve_mia`` 优化。
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class MiaTemplate:
    """MIA 固定模板：仅 ``A`` 与 ``b`` 行语义切片."""

    A: np.ndarray
    tau: int
    with_cost: bool
    cost_b_rows: slice | None = None  # with_cost=True 时，b 中 −f/−g 行


def build_mia_template(tau: int, *, with_cost: bool = False, with_state: bool = False) -> MiaTemplate:
    """构造 MIA 用固定 ``A``.

    with_cost=False（无 ψ 列）
      TODO: Phase 1 — ``A_feas = [I; -I; Ξ; -Ξ; B; -B]`` (3.32)，x = P(τ)
      状态 S = B @ P（式 3.33d），不显式入列

    with_cost=True
      TODO: Phase 1 — ``A = [A_cost; 0, A_feas]``，x = [ψ_P, ψ_S?, P]
      状态成本行用 G*·B 而非 G*·S；``cost_b_rows`` 标出 −f/−g 行
    """
    raise NotImplementedError
