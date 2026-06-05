"""分层聚合编排 (§3.4, Fig 3.5) — 不含 MIA 求解.

职责:
  - group_der_list: 按类型与批次划分 (50 EV → 5×10)
  - aggregate_by_type: 每类多批 primary_aggregate → 类内 Σb
  - secondary_aggregate / aggregate_vpp: 顶层编排

MIA: 否（本文件）。初级聚合委托 aggregation.mia.primary_aggregate。

依赖:
  mia.primary_aggregate          — 每批一次 MIA
  minkowski.algebraic_minkowski_sum — 次级 Σb
  vpp_standard.parse_participation_params — 输出解析
"""

from __future__ import annotations

from tdm.models.der.base import Parameters
from tdm.models.polytope import Polytope


def group_der_list(
    der_specs: list[tuple[str, Parameters]],
    *,
    max_group_size: int = 12,
) -> list[list[tuple[str, Parameters]]]:
    """按类型与批次划分 DER 列表."""
    # TODO: Phase 5.1
    ...


def aggregate_by_type(
    der_specs: list[tuple[str, Parameters]],
    *,
    template: object,
    group_size: int = 10,
) -> dict[str, Polytope]:
    """按资源类型初级聚合，返回每类一个 Polytope."""
    # TODO: Phase 5.2 — 每批调用 mia.primary_aggregate
    ...


def secondary_aggregate(polytopes: list[Polytope]) -> Polytope:
    """次级聚合: b_VPP = Σ b_g（要求 A 相同）."""
    # TODO: Phase 5.3 — 委托 algebraic_minkowski_sum
    ...


def aggregate_vpp(
    der_specs: list[tuple[str, Parameters]],
    *,
    template: object,
    group_size: int = 10,
) -> Polytope:
    """VPP 节点层级完整聚合."""
    # TODO: Phase 5.4
    ...
