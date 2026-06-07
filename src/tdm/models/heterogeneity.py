"""Ch2 状态异质性消去 (§2.3.2) — 输出单条 ``ProjectionTarget``."""

from __future__ import annotations

from tdm.aggregation.mia import DerType, ProjectionTarget
from tdm.models.der.base import Parameters
from tdm.models.polytope import Polytope


def build_projection_target(
    der_type: DerType,
    source: Polytope,
    parameters: Parameters,
) -> ProjectionTarget:
    """ESS 等高维多面体 → ``ProjectionTarget``（仅携带 ``parameters``）."""
    # TODO: Phase 2 — 投影/消去后可更新 parameters（如收紧 P 界），不存 G/h
    raise NotImplementedError
