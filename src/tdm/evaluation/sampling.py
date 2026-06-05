"""多面体采样 (§2.5.1, hit-and-run).

TODO (Phase 7):
  [ ] sample_uniform(polytope, n, rng) -> np.ndarray
        实现 polytope.sample_hit_and_run
  [ ] check_backtrack_minkowski(sample, sources) -> bool
        式 (2.31a)
  [ ] check_backtrack_projection(sample, high_dim_poly) -> bool
        式 (2.31b)
"""

from __future__ import annotations

from tdm.models.polytope import Polytope


def sample_uniform(polytope: Polytope, n_samples: int) -> object:
    """在多面体内均匀采样."""
    # TODO
    ...
