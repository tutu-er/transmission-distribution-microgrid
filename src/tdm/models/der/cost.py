"""DER 运行成本模型 (§2.2.2, 式 2.6–2.8). 价格单位: $/MWh.

TODO (Phase 2 — 独立于 MIA):
  [ ] PiecewiseLinearCost dataclass: slopes (固定 F*), intercepts (f 或 g)
  [ ] zero_cost(tau): PV/WT/EV(无V2G) 返回全零截距
  [ ] build_power_cost_rhs(params):
        - 线性: unit_cost ($/MWh) → 五档 F* 下的 f_t
        - ESS: aging_lambda * |P| → 分段线性 (2.7)
        - 输入示例: {"cost_type": "linear", "unit_cost": 75.0}
  [ ] build_state_cost_rhs(params):
        - HVAC: comfort_lambda, T_comf (2.8) → g_t
  [ ] evaluate_cost(power, state, params): 验证用，单位 MW/MWh → $
  [ ] 测试: 表 2.5.3 (DG 发电成本、HVAC 舒适度成本)

注意:
  - F*, G* 由 fixed_price_slopes() 固定，不在 MIA 中求解
  - 此处产出单体 DER 的 f_k, g_k；VPP 级截距在分层聚合后由 Σb 或 (2.23) 得到
  - 依赖: der.units.PRICE_SEGMENTS_MWH
"""

from __future__ import annotations

import numpy as np

from tdm.models.der.base import Parameters
from tdm.models.der.units import PRICE_SEGMENTS_MWH

CostSegments = dict[str, np.ndarray]


def fixed_price_slopes() -> np.ndarray:
    """返回固定的五档边际价格 F* = G* ($/MWh)."""
    return np.array(PRICE_SEGMENTS_MWH, dtype=float)


def zero_cost(tau: int) -> CostSegments:
    """零成本 DER (PV, WT 等)."""
    # TODO: 返回 n_seg=5 的零截距，形状 (tau, n_seg) 或等价结构
    ...


def build_power_cost(parameters: Parameters) -> CostSegments:
    """分段线性功率成本，由 parameters 直接计算 f_t (2.28a)，不经 MIA."""
    # TODO: 读取 unit_cost / aging_lambda 等，结合 fixed_price_slopes() 算截距
    ...


def build_state_cost(parameters: Parameters) -> CostSegments:
    """分段线性状态成本，由 parameters 直接计算 g_t (2.28b)，不经 MIA."""
    # TODO: HVAC comfort_lambda, T_comf_t 等
    ...


def evaluate_cost(power: np.ndarray, state: np.ndarray | None, parameters: Parameters) -> float:
    """给定功率(MW)/状态(MWh)向量计算总运行成本 ($)."""
    # TODO: 可选验证函数
    ...
