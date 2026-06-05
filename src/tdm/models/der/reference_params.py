"""论文算例参数 (已统一换算为 MW / MWh / MW·h⁻¹)."""

from __future__ import annotations

import numpy as np

from tdm.models.der.base import Parameters
from tdm.models.der.units import DEFAULT_DELTA_TAU_H, HVAC_ALPHA_KW_TO_MW, KWH_TO_MWH, KW_TO_MW


def table_2_2_ess_params(tau: int = 2) -> Parameters:
    """表 2.2 非理想 ESS (原 kW/kWh 算例 ×0.001)."""
    return {
        "tau_start": 0,
        "tau_end": tau,
        "eta": 0.95,
        "delta_tau": DEFAULT_DELTA_TAU_H,
        "P_max": np.full(tau, 50.0 * KW_TO_MW),
        "P_min": np.full(tau, -50.0 * KW_TO_MW),
        "E_max": np.full(tau, 100.0 * KWH_TO_MWH),
        "E_min": np.full(tau, 0.0),
        "E_0": 80.0 * KWH_TO_MWH,
        "alpha_in": 0.9,
        "alpha_out": 1.1,
    }


def table_2_4_dg_params(tau: int = 3) -> Parameters:
    """表 2.4 DG (原 kW / kW·h⁻¹ 算例 ×0.001)."""
    return {
        "tau_start": 0,
        "tau_end": tau,
        "eta": 1.0,
        "delta_tau": DEFAULT_DELTA_TAU_H,
        "P_max": np.full(tau, 80.0 * KW_TO_MW),
        "P_min": np.full(tau, 40.0 * KW_TO_MW),
        "R_up": np.full(max(tau - 1, 0), 30.0 * KW_TO_MW),
        "R_down": np.full(max(tau - 1, 0), 30.0 * KW_TO_MW),
    }


def table_2_4_hvac_params(tau: int = 3) -> Parameters:
    """表 2.4 HVAC (功率换 MW，α 按 °C/(MW·h) 缩放)."""
    return {
        "tau_start": 0,
        "tau_end": tau,
        "eta": 1.04,
        "alpha": -0.05 * HVAC_ALPHA_KW_TO_MW,
        "delta_tau": DEFAULT_DELTA_TAU_H,
        "P_max": np.full(tau, 110.0 * KW_TO_MW),
        "P_min": np.zeros(tau),
        "T_max": np.full(tau, 26.0),
        "T_min": np.full(tau, 22.0),
        "T_0": 26.0,
        "omega": np.array([32.4, 34.4, 34.9])[:tau],
    }
