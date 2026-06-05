"""多面体估计评价指标 (§2.5.1).

TODO (Phase 7):
  [ ] precision(target, estimate, mode="minkowski"|"projection") -> float
        回溯 LP (2.31a/b)
  [ ] gmvr(poly_a, poly_b, n_samples) -> float  (2.32)
  [ ] gmp(...) -> float
  [ ] gmpg(power_params_est, power_params_ref) -> float  (2.33)

依赖:
  evaluation.sampling, cvxpy (回溯 LP)
"""

from __future__ import annotations

from tdm.models.polytope import Polytope


def geometric_mean_volume_ratio(reference: Polytope, estimate: Polytope, n_samples: int) -> float:
    """GMVR (2.32)."""
    # TODO
    ...
