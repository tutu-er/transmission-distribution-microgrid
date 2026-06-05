"""最大内估计 MIA — 全项目唯一 LP 实现 (§3.3, 算法 3.1).

职责:
  - solve_mia: 核心 LP，固定模板 A + 投影目标 → 最优 b
  - fit_to_template: 通用包装，任意目标可行域拟合到模板（Ch2/Ch3 共用）
  - primary_aggregate: 初级聚合编排（batch_projection → solve_mia）

调用方:
  - aggregation/hierarchical.py  — 分批初级聚合
  - models/heterogeneity.py      — 单体 ESS 功率模板拟合 (§2.3)

不含:
  - 标准投影问题构造 → batch_projection.py
  - 几何/FME 投影     → models/projection.py
  - 次级 Σb           → minkowski.py

注意:
  - F*, G* 已在 A 中固定；MIA 只优化 b（功率界与 f,g 截距）
  - 成本 f,g 由 der/cost.py 直接计算，不经 MIA
"""

from __future__ import annotations

from tdm.models.der.base import Parameters
from tdm.models.polytope import Polytope


def solve_mia(template_a: object, projection_target: object) -> object:
    """算法 3.1: 对标准投影目标求 MIA，返回右端向量 b."""
    # TODO: Phase 4.2 — cvxpy LP
    ...


def fit_to_template(
    target: Polytope | object,
    template: object,
) -> Polytope:
    """将目标可行域内估计到固定模板 A，返回 Polytope(A, b).

    Ch2: ESS 高维 → 通用功率模板 (heterogeneity 调用)
    Ch3: 一批 DER 聚合目标 → 参与模板 (primary_aggregate 内部亦可复用)
    """
    # TODO: projection_target 封装 + solve_mia
    ...


def primary_aggregate(
    der_type: str,
    parameters_list: list[Parameters],
    *,
    template: object,
) -> Polytope:
    """初级聚合: 一批同类型 DER → 一个 Polytope(A, b)."""
    # TODO: Phase 4.3
    # from tdm.aggregation.batch_projection import build_batch_projection_problem
    # target = build_batch_projection_problem(...)
    # b = solve_mia(template.A, target)
    # return Polytope(A=template.A, b=b)
    ...
