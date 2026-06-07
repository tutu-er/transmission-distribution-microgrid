"""分层聚合编排 (§3.4) — 调用 ``mia.fit_mia``."""

from __future__ import annotations

from tdm.models.der.base import Parameters
from tdm.models.polytope import Polytope
from tdm.models.vpp_standard import MiaTemplate


def aggregate_batch(
    der_type: str,
    parameters_list: list[Parameters],
    template: MiaTemplate,
) -> Polytope:
    """单批初级聚合."""
    # TODO: Phase 5
    # from tdm.aggregation.batch_projection import build_projection_targets
    # from tdm.aggregation.mia import fit_mia
    # targets = build_projection_targets(der_type, parameters_list, with_cost=template.with_cost)
    # return fit_mia(targets, template)
    raise NotImplementedError


def aggregate_vpp(
    der_specs: list[tuple[str, Parameters]],
    template: MiaTemplate,
    *,
    group_size: int = 10,
) -> Polytope:
    """多批聚合 → 次级 Σb."""
    # TODO: Phase 5
    raise NotImplementedError
