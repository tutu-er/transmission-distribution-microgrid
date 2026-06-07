"""DER 精确运行成本 h(x) (§2.6–2.8).

与 ``der/*.py`` 端口功率可行域共同构成**精确 DER 问题**：

- 可行性：``build_dg_polytope(params).contains(P)`` 等（H 表示，仅功率/状态变量）
- 运行成本：``evaluate_cost(P, S, params)``（本模块，非多面体）

参与模板 H 由 ``participation_rhs`` 的 ``A_cost,b_cost`` 与 ``cost_epigraph.stack_participation_h`` 拼接 ``A_p,b_p`` 得到。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Literal

import numpy as np

from tdm.models.der.base import Parameters, get_tau

CostKind = Literal["power", "state"]
PhysicalCostKind = Literal["zero", "linear_power", "abs_power", "quadratic_power", "comfort_state"]

_DOMAIN_KEYS: dict[CostKind, tuple[str, str]] = {
    "power": ("P_min", "P_max"),
    "state": ("T_min", "T_max"),
}


@dataclass(frozen=True)
class PhysicalCostModel:
    """单时段物理成本 h_t(x)；x 为功率 P 或状态 T/S."""

    kind: PhysicalCostKind
    cost_kind: CostKind
    tau: int
    parameters: Parameters

    def domain_at(self, t: int) -> tuple[float, float]:
        lo_key, hi_key = _DOMAIN_KEYS[self.cost_kind]
        lo = _param_at_t(self.parameters, lo_key, t, default=0.0)
        hi = _param_at_t(self.parameters, hi_key, t, default=0.0)
        return (hi, lo) if lo > hi else (lo, hi)

    def evaluate_period(self, t: int, x: float) -> float:
        return self.convex_fn_at(t)(x)

    def evaluate(self, x: np.ndarray) -> float:
        arr = np.asarray(x, dtype=float).reshape(-1)
        if arr.shape[0] != self.tau:
            raise ValueError(f"期望长度 {self.tau}，得到 {arr.shape[0]}")
        return float(sum(self.evaluate_period(t, arr[t]) for t in range(self.tau)))

    def convex_fn_at(self, t: int) -> Callable[[float], float]:
        p = self.parameters
        match self.kind:
            case "zero":
                return lambda _x: 0.0
            case "linear_power":
                return lambda x: float(p["unit_cost"]) * x
            case "abs_power":
                return lambda x: float(p["aging_lambda"]) * abs(x)
            case "quadratic_power":
                q = _quadratic_coeff(p, t)
                c = _param_at_t(p, "unit_cost", t, default=0.0)
                return lambda x: q * x * x + c * x
            case "comfort_state":
                lam = float(p["comfort_lambda"])
                tc = float(_comfort_temperature(p, self.tau)[t])
                return lambda x: lam * abs(x - tc)
            case _:
                raise ValueError(f"未知物理成本类型: {self.kind}")


def build_physical_cost(parameters: Parameters, *, kind: CostKind = "power") -> PhysicalCostModel:
    """由 parameters 推断成本类型并构造 PhysicalCostModel."""
    if kind == "power":
        if "quadratic_coeff" in parameters:
            pkind: PhysicalCostKind = "quadratic_power"
        elif "unit_cost" in parameters:
            pkind = "linear_power"
        elif "aging_lambda" in parameters:
            pkind = "abs_power"
        else:
            pkind = "zero"
    elif "comfort_lambda" in parameters:
        pkind = "comfort_state"
    else:
        pkind = "zero"
    return PhysicalCostModel(pkind, kind, get_tau(parameters), parameters)


def evaluate_cost(power: np.ndarray, state: np.ndarray | None, parameters: Parameters) -> float:
    """精确总运行成本 = 功率成本 +（可选）状态成本."""
    total = build_physical_cost(parameters, kind="power").evaluate(power)
    if state is not None:
        total += build_physical_cost(parameters, kind="state").evaluate(state)
    return total


def _quadratic_coeff(parameters: Parameters, t: int) -> float:
    q = _param_at_t(parameters, "quadratic_coeff", t)
    if q <= 0.0:
        raise ValueError(f"quadratic_coeff 须为正（凸成本），得到 {q}")
    return q


def _param_at_t(parameters: Parameters, key: str, t: int, *, default: float = 0.0) -> float:
    if key not in parameters:
        return default
    arr = np.asarray(parameters[key], dtype=float).reshape(-1)
    return float(arr[0] if arr.size == 1 else arr[t])


def _comfort_temperature(parameters: Parameters, tau: int) -> np.ndarray:
    if "T_comf" in parameters:
        t = np.asarray(parameters["T_comf"], dtype=float).reshape(-1)
        return np.full(tau, float(t[0])) if t.size == 1 else t[:tau]
    if "T_comf_a" in parameters and "T_comf_b" in parameters:
        omega = np.asarray(parameters["omega"], dtype=float).reshape(-1)[:tau]
        return float(parameters["T_comf_a"]) * omega + float(parameters["T_comf_b"])
    if "T_0" in parameters:
        return np.full(tau, float(parameters["T_0"]))
    raise KeyError("舒适度成本需要 T_comf、T_comf_a/T_comf_b 或 T_0")
