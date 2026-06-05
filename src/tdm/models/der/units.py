"""DER 模型统一单位约定 (项目默认采用 SI 派生单位，功率基准为 MW)."""

from __future__ import annotations

# 功率: MW
# 能量 / 状态(储能): MWh
# 爬坡速率: MW/h  (对应 Δτ 以小时计)
# 温度(HVAC): °C
# 时间步长: h
# 运行成本价格档: $/MWh
# 环境温度 ω: °C

DEFAULT_DELTA_TAU_H: float = 1.0

# 论文 §2.5.4 / §3.5.2 固定五档边际价格 ($/MWh)
PRICE_SEGMENTS_MWH: tuple[float, ...] = (-80.0, -40.0, 0.0, 40.0, 80.0)
N_PRICE_SEGMENTS: int = len(PRICE_SEGMENTS_MWH)

# kW/kWh 算例换算至 MW/MWh 时的比例
KW_TO_MW: float = 1e-3
KWH_TO_MWH: float = 1e-3

# HVAC 状态方程中 α 的量纲为 °C/(MW·h)。
# 论文表 2.4 给出的是 kW 情形下的 α (°C/(kW·h))，换算为 MW 时需乘以 1000。
HVAC_ALPHA_KW_TO_MW: float = 1e3
