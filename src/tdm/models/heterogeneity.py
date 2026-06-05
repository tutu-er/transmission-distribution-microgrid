"""Ch2 状态异质性消去工作流 (§2.3.2) — 不实现 MIA，只编排调用.

职责:
  - eliminate_state_heterogeneity: ESS 等复杂 DER → 通用功率模板 Polytope
  - build_general_der_template: 通用 DER 功率模板 (功率界+爬坡+状态差分)

MIA: 否（本文件）。内估计统一调用 aggregation.mia.fit_to_template。

流程:
  ess.build_ess_polytope
    → models/projection.project_polytope  (可选，降维)
    → eliminate_state_heterogeneity
         → aggregation.mia.fit_to_template(source, template)

与 primary_aggregate 的区别:
  - 本模块: 单个 DER，Ch2 图 2.9
  - primary_aggregate: 一批同类型 DER，Ch3 初级聚合
  - 二者共用 aggregation/mia.py 的 LP 内核
"""

from __future__ import annotations

from tdm.models.der.base import Parameters
from tdm.models.polytope import Polytope


def build_general_der_template(tau: int) -> Polytope:
    """通用 DER 功率模板，约束矩阵 A 固定、b 待定."""
    # TODO
    ...


def eliminate_state_heterogeneity(
    source: Polytope,
    parameters: Parameters,
    *,
    template: Polytope | None = None,
) -> Polytope:
    """复杂 DER 投影拟合为通用模板多面体（委托 mia.fit_to_template）."""
    # TODO:
    # tpl = template or build_general_der_template(get_tau(parameters))
    # from tdm.aggregation.mia import fit_to_template
    # return fit_to_template(source, tpl)
    ...
