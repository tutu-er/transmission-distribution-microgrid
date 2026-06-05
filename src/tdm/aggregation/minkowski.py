"""次级代数聚合 (§2.4.1, 式 2.14; §3.4 次级层).

职责:
  - algebraic_minkowski_sum: 同 A 下 b_VPP = Σ b_k（已完成）
  - sum_b_vectors: 薄封装别名

MIA: 否。次级层只做代数求和，不再调用 solve_mia。

已完成:
  [x] algebraic_minkowski_sum / Polytope.algebraic_sum

TODO:
  [ ] minkowski_sum: A 不同时的通用闵可夫斯基和（低维精确算法，非主流程）
"""

from __future__ import annotations

from tdm.models.polytope import Polytope


def algebraic_minkowski_sum(polytopes: list[Polytope]) -> Polytope:
    """最小表示多面体族代数聚合: Ω(b1) ⊕ ... ⊕ Ω(bn) = Ω(Σ bi)."""
    if not polytopes:
        raise ValueError("至少需要一个多面体")
    result = polytopes[0]
    for poly in polytopes[1:]:
        result = result.algebraic_sum(poly)
    return result


def sum_b_vectors(polytopes: list[Polytope]) -> Polytope:
    """次级聚合别名：同 A 下合并右端项."""
    return algebraic_minkowski_sum(polytopes)


def minkowski_sum(polytopes: list[Polytope]) -> Polytope:
    """A 不同时的一般闵可夫斯基和（非 VPP 主流程，低维研究用）."""
    # TODO: 低维精确算法；主流程用 batch_projection + solve_mia
    ...
