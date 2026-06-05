"""H 表示多面体及通用代数运算.

已完成:
  [x] Polytope, contains, algebraic_sum (次级聚合 Σb)

TODO:
  [ ] sample_hit_and_run: hit-and-run 均匀采样 (§2.5.1, 评价 GMP/GMVR)
  [ ] 可选: 导出 b 槽位索引工具，供 vpp_standard.parse 使用
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Self

import numpy as np


@dataclass(frozen=True)
class Polytope:
    """多面体 {x | A @ x <= b}."""

    A: np.ndarray
    b: np.ndarray

    def __post_init__(self) -> None:
        object.__setattr__(self, "A", np.asarray(self.A, dtype=float))
        object.__setattr__(self, "b", np.asarray(self.b, dtype=float).reshape(-1))
        if self.A.ndim != 2:
            raise ValueError("A 必须是二维矩阵")
        if self.A.shape[0] != self.b.shape[0]:
            raise ValueError("A 行数必须与 b 长度一致")

    @classmethod
    def from_ab(cls, A: np.ndarray, b: np.ndarray) -> Self:
        """由 (A, b) 构造多面体."""
        return cls(A=A, b=b)

    @property
    def dim(self) -> int:
        """决策变量维度."""
        return int(self.A.shape[1])

    @property
    def n_constraints(self) -> int:
        """约束行数."""
        return int(self.A.shape[0])

    def contains(self, x: np.ndarray, tol: float = 1e-9) -> bool:
        """判断点 x 是否在多面体内."""
        x_arr = np.asarray(x, dtype=float).reshape(-1)
        if x_arr.shape[0] != self.dim:
            return False
        return bool(np.all(self.A @ x_arr <= self.b + tol))

    def algebraic_sum(self, other: Polytope, tol: float = 1e-9) -> Polytope:
        """闵可夫斯基闭族代数聚合: Ω(b1) ⊕ Ω(b2) = Ω(b1 + b2)，要求约束矩阵 A 相同."""
        if self.dim != other.dim:
            raise ValueError("两个多面体维度必须相同")
        if not np.allclose(self.A, other.A, atol=tol, rtol=0):
            raise ValueError("代数聚合要求两个多面体具有相同的约束矩阵 A")
        return Polytope(A=self.A, b=self.b + other.b)

    def sample_hit_and_run(self, n_samples: int, rng: np.random.Generator | None = None) -> np.ndarray:
        """在多面体内均匀采样 (hit-and-run)."""
        ...

    def sample_uniform(self, n_samples: int, rng: np.random.Generator | None = None) -> np.ndarray:
        """sample_hit_and_run 的别名."""
        return self.sample_hit_and_run(n_samples, rng=rng)
