"""批量标准投影目标构造 (§3.2, 式 3.6–3.7).

职责: 把一批同类型 DER 的原始约束写成 MIA 的 LP 目标（投影/闵可夫斯基和等价形式）。
MIA: 否 — 只构造问题，求解见 mia.solve_mia。

与 models/projection.py 的区别:
  - 本模块: Ch3 初级聚合，输出 ProjectionProblem 供 solve_mia 使用
  - models/projection: Ch2 几何投影 (FME/消元)，精确或低维验证

公开 API (Phase 4):
  - build_batch_projection_problem
  - embed_period_heterogeneity
  - stack_der_constraints
"""

from __future__ import annotations

from tdm.models.der.base import Parameters


def build_batch_projection_problem(
    der_type: str,
    parameters_list: list[Parameters],
    *,
    tau: int,
) -> object:
    """构造一批 DER 的标准投影问题 (3.6)."""
    # TODO: Phase 4.1
    ...


def embed_period_heterogeneity(
    tau_start: int,
    tau_end: int,
    tau_total: int,
) -> object:
    """EV 等时段异质性嵌入矩阵 M_k (3.7b)."""
    # TODO: Phase 4.4
    ...
