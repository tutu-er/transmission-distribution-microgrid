"""多面体与 DER 可行域构建测试 (单位: MW / MWh)."""

import numpy as np

from tdm.aggregation.minkowski import algebraic_minkowski_sum
from tdm.models.der import (
    build_dg_polytope,
    build_ess_polytope,
    build_hvac_polytope,
    build_pv_polytope,
    fixed_price_slopes,
    table_2_2_ess_params,
    table_2_4_dg_params,
    table_2_4_hvac_params,
)
from tdm.models.der.base import build_xi, get_tau
from tdm.models.der.units import KW_TO_MW, PRICE_SEGMENTS_MWH
from tdm.models.polytope import Polytope


def test_polytope_contains() -> None:
    poly = Polytope.from_ab(np.eye(2), np.array([1.0, 1.0]))
    assert poly.contains(np.array([0.5, 0.5]))
    assert not poly.contains(np.array([1.5, 0.0]))


def test_algebraic_minkowski_sum() -> None:
    a = np.array([[1.0, 0.0], [0.0, 1.0], [-1.0, 0.0], [0.0, -1.0]])
    p1 = Polytope.from_ab(a, np.array([1.0, 1.0, 0.0, 0.0]))
    p2 = Polytope.from_ab(a, np.array([0.5, 0.5, 0.0, 0.0]))
    summed = algebraic_minkowski_sum([p1, p2])
    assert np.allclose(summed.b, np.array([1.5, 1.5, 0.0, 0.0]))


def test_dg_polytope_shape() -> None:
    params = table_2_4_dg_params(tau=3)
    poly = build_dg_polytope(params)
    assert poly.dim == 3
    assert poly.n_constraints == 4 * 3 - 2


def test_dg_polytope_mw_magnitudes() -> None:
    """表 2.4 DG 功率边界应为 MW 量级."""
    tau = 3
    params = table_2_4_dg_params(tau=tau)
    poly = build_dg_polytope(params)
    assert np.isclose(poly.b[0], 80.0 * KW_TO_MW)
    assert np.isclose(poly.b[tau], -(40.0 * KW_TO_MW))  # -P_min 块


def test_pv_polytope_shape() -> None:
    tau = 2
    params = {
        "tau_start": 0,
        "tau_end": tau,
        "P_max": np.full(tau, 0.1),  # MW
        "P_min": np.zeros(tau),
    }
    poly = build_pv_polytope(params)
    assert poly.dim == tau
    assert poly.n_constraints == 2 * tau


def test_build_xi_shape() -> None:
    xi = build_xi(3)
    assert xi.shape == (2, 3)


def test_hvac_polytope_table_2_4() -> None:
    """表 2.4 HVAC，单位 MW / °C."""
    params = table_2_4_hvac_params(tau=3)
    poly = build_hvac_polytope(params)
    assert get_tau(params) == 3
    assert poly.dim == 3
    assert poly.n_constraints == 4 * 3
    assert np.isclose(params["P_max"][0], 110.0 * KW_TO_MW)


def test_ess_polytope_table_2_2() -> None:
    """表 2.2 ESS，单位 MW / MWh."""
    params = table_2_2_ess_params(tau=2)
    poly = build_ess_polytope(params)
    assert poly.dim == 4  # [P_in; P_out], 2τ
    assert np.isclose(params["E_0"], 80.0 * KW_TO_MW)  # 0.08 MWh


def test_hvac_kw_mw_equivalence() -> None:
    """kW 参数换算为 MW 后，功率可行域在 P_mw = P_kw/1000 映射下等价."""
    tau = 3
    kw_params = {
        "tau_start": 0,
        "tau_end": tau,
        "eta": 1.04,
        "alpha": -0.05,
        "delta_tau": 1.0,
        "P_max": np.full(tau, 110.0),
        "P_min": np.zeros(tau),
        "T_max": np.full(tau, 26.0),
        "T_min": np.full(tau, 22.0),
        "T_0": 26.0,
        "omega": np.array([32.4, 34.4, 34.9]),
    }
    mw_params = table_2_4_hvac_params(tau=3)
    poly_kw = build_hvac_polytope(kw_params)
    poly_mw = build_hvac_polytope(mw_params)

    # 功率边界块按 1/1000 缩放，状态约束块不变
    assert np.allclose(poly_mw.b[: 2 * tau], poly_kw.b[: 2 * tau] * KW_TO_MW)
    assert np.allclose(poly_mw.b[2 * tau :], poly_kw.b[2 * tau :])

    sample_kw = np.array([40.0, 55.0, 110.0])
    assert poly_kw.contains(sample_kw) == poly_mw.contains(sample_kw * KW_TO_MW)


def test_fixed_price_slopes() -> None:
    slopes = fixed_price_slopes()
    assert slopes.shape == (5,)
    assert np.allclose(slopes, PRICE_SEGMENTS_MWH)
