"""功率-成本空间中成本上境图 (§2.4.2, 式 2.20–2.27).

TODO (Phase 3 — 组装单体参与模型，不经 MIA):
  [ ] build_der_epigraph_rhs(power_poly, f, g, template) -> np.ndarray
        将 der/*.py 的功率 (A_p,b_p) 与 cost.py 的 f,g 填入模板 b 的对应槽位
  [ ] build_der_participation_model(der_type, params, template) -> Polytope
        统一入口: 原始功率多面体 + cost RHS → Polytope(A_template, b_k)
  [ ] 与 vpp_standard.build_template_matrix 对齐行顺序

可选 (Ch2 验证 / 理论对照，非主流程):
  [ ] aggregate_cost_epigraph: 上境图闵可夫斯基和 (2.26)，主流程改用分层 MIA+Σb
  [ ] project_epigraph_to_power: 上境图投影回功率子空间

主流程位置:
  der/*.py (功率) + der/cost.py (f,g) → 本模块 → batch_projection → mia.solve_mia
MIA: 否（本模块）；初级 MIA 见 aggregation/mia.py
"""

from __future__ import annotations

from tdm.models.der.base import Parameters
from tdm.models.polytope import Polytope


def build_cost_epigraph(
    power_polytope: Polytope,
    parameters: Parameters,
    *,
    der_type: str,
) -> Polytope:
    """构建单体 DER 在功率-成本空间中的成本上境图可行域."""
    # TODO: 改用 build_der_participation_model；本函数可保留为别名
    ...


def aggregate_cost_epigraph(epigraphs: list[Polytope]) -> Polytope:
    """聚合成本上境图：单体上境图的闵可夫斯基和 (2.26)."""
    # TODO: 可选；主路径见 aggregation/hierarchical.py
    ...


def project_epigraph_to_power(epigraph: Polytope) -> Polytope:
    """将成本上境图投影到端口功率子空间."""
    # TODO: Ch2 图 2.10 验证用
    ...
