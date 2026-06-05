"""VPP 标准化模型 (§2.4.3, 式 2.29–2.30; 参与模板 式 3.32–3.34).

TODO (Phase 1 — 固定约束矩阵 A):
  [ ] StandardTemplate dataclass: tau, A, F_star, G_star, B (式 3.30, a_t=b_t=1)
  [ ] build_template_matrix(tau) -> np.ndarray
        组装 (3.32) 左侧分块；行顺序需与 parse_b 一致
  [ ] template_polytope(b) -> Polytope(A, b)
  [ ] 固定 S0=0, C_t=0 (§3.5.2.2)

TODO (Phase 6 — 从 b 解析市场参数):
  [ ] VPPParticipationParams dataclass: P_bar, P_under, delta, S_bar, f, g ...
  [ ] parse_participation_params(b, tau) -> VPPParticipationParams
        对应式 (3.33)(3.34)
  [ ] relax_unused_features: 无状态/无爬坡 DER 松弛冗余行 (图 2.6)

TODO (Phase 5 — 顶层编排，或放 aggregation/hierarchical):
  [ ] from_der_list(der_specs) -> 调用 aggregate_vpp + parse

依赖:
  der.cost.fixed_price_slopes, der.units, aggregation.hierarchical
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from tdm.models.der.base import Parameters
from tdm.models.polytope import Polytope


@dataclass
class VPPStandardModel:
    """VPP 标准化参与模型参数容器."""

    tau: int
    power_bounds: dict[str, Any] = field(default_factory=dict)
    ramp_bounds: dict[str, Any] = field(default_factory=dict)
    state_bounds: dict[str, Any] = field(default_factory=dict)
    state_equation: dict[str, Any] = field(default_factory=dict)
    power_cost: dict[str, Any] = field(default_factory=dict)
    state_cost: dict[str, Any] = field(default_factory=dict)

    def build_power_polytope(self) -> Polytope:
        """由标准化可行域参数构建功率可行域多面体."""
        # TODO: Phase 6 — 由已解析参数重构 Polytope
        ...

    def build_participation_epigraph(self) -> Polytope:
        """构建功率-成本空间参与模型投影 (2.27)."""
        # TODO: template_polytope(self._b)
        ...


def from_der_list(der_specs: list[tuple[str, Parameters]]) -> VPPStandardModel:
    """由多个 DER 聚合并辨识标准化模型参数."""
    # TODO: aggregate_vpp(der_specs) → parse_participation_params
    ...
