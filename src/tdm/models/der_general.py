"""DER 通用模型统一接口 (表 2.1, §2.2).

TODO:
  [ ] build_power_polytope(der_type, params) -> Polytope
        分发至 der/pv_wt, dg, hvac, ev, ess；ESS 可先走 heterogeneity
  [ ] build_cost_epigraph_for_der(der_type, params) -> Polytope
        委托 cost_epigraph.build_der_participation_model
  [ ] relax_unused_features(poly, has_state, has_ramp) -> Polytope
        图 2.6 参数松弛

定位: 对外统一入口，内部调用 der/* + cost + cost_epigraph
MIA: 否；聚合见 aggregation/hierarchical，LP 内核见 aggregation/mia
"""

from __future__ import annotations

from tdm.models.der.base import Parameters
from tdm.models.polytope import Polytope


def build_power_polytope(der_type: str, parameters: Parameters) -> Polytope:
    """按 DER 类型构建端口功率可行域."""
    # TODO
    ...


def build_cost_epigraph_for_der(der_type: str, parameters: Parameters) -> Polytope:
    """构建单体 DER 参与模型 Polytope(A_template, b)."""
    # TODO
    ...


def relax_unused_features(
    polytope: Polytope, *, has_state: bool = False, has_ramp: bool = False
) -> Polytope:
    """对不含某类灵活性特征的 DER，松弛对应约束 (图 2.6)."""
    # TODO
    ...
