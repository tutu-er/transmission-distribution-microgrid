"""der/cost.py、participation_rhs.py、cost_epigraph 组装测试."""

import numpy as np
import pytest

from tdm.models.cost_epigraph import build_der_participation_model, stack_participation_h
from tdm.models.der.cost import build_physical_cost, evaluate_cost
from tdm.models.der.dg import build_dg_polytope
from tdm.models.der.base import build_B
from tdm.models.der.participation_rhs import (
    ParticipationRhs,
    build_cost_A,
    build_participation_rhs,
    fit_direct_intercepts,
    resolve_mia,
)
from tdm.models.der.reference_params import (
    table_2_5_3_dg_params,
    table_2_5_3_ess_params,
    table_2_5_3_hvac_params,
)
from tdm.models.der.units import N_PRICE_SEGMENTS, PRICE_SEGMENTS_MWH


def test_zero_cost_intercepts() -> None:
    params = {"tau_start": 0, "tau_end": 3, "P_min": np.zeros(3), "P_max": np.zeros(3)}
    rhs = build_participation_rhs(params)
    assert isinstance(rhs, ParticipationRhs)
    assert rhs.power_f.shape == (3, N_PRICE_SEGMENTS)
    assert np.allclose(rhs.power_f, 0.0)


def test_cost_A_fixed_template() -> None:
    a = build_cost_A(3)
    assert a.shape == (15, 6)
    assert a[0, 0] == -1.0
    assert a[0, 3] == PRICE_SEGMENTS_MWH[0]


def test_dg_exact_feasibility_and_cost() -> None:
    params = table_2_5_3_dg_params(tau=3)
    dg = build_dg_polytope(params)
    power = np.array([40.0, 70.0, 80.0]) * 1e-3
    assert dg.contains(power)
    assert np.isclose(evaluate_cost(power, None, params), 75.0 * power.sum())


def test_stack_participation_h() -> None:
    """[A_cost; 0,A_p] 拼接后 DG 功率轨迹可行."""
    params = table_2_5_3_dg_params(tau=3)
    dg = build_dg_polytope(params)
    rhs = build_participation_rhs(params)
    poly = stack_participation_h(build_cost_A(3), rhs.b_cost(), dg.A, dg.b)
    assert poly.dim == 6
    assert poly.n_constraints == 15 + dg.n_constraints
    x = np.zeros(6)
    x[3:6] = np.array([50.0, 80.0, 80.0]) * 1e-3
    x[:3] = 1e6
    assert poly.contains(x)


def test_build_der_participation_model() -> None:
    params = table_2_5_3_dg_params(tau=3)
    poly = build_der_participation_model(params, build_dg_polytope(params))
    assert poly.dim == 6


def test_ess_aging_cost_symmetry() -> None:
    params = table_2_5_3_ess_params(tau=2)
    assert build_physical_cost(params).kind == "abs_power"
    p_pos = np.array([0.05, 0.0])
    p_neg = np.array([-0.05, 0.0])
    assert np.isclose(evaluate_cost(p_pos, None, params), evaluate_cost(p_neg, None, params))


def test_hvac_state_cost() -> None:
    params = table_2_5_3_hvac_params(tau=3)
    rhs = build_participation_rhs(params, with_state=True)
    assert rhs.state_g is not None
    tau = 3
    a = build_cost_A(tau, with_state=True)
    assert a.shape == (30, 9)
    B = build_B(tau)
    rs = tau * N_PRICE_SEGMENTS + 2 * N_PRICE_SEGMENTS
    assert np.allclose(a[rs, 2 * tau : 3 * tau], PRICE_SEGMENTS_MWH[0] * B[2])


def test_mia_path_and_resolve() -> None:
    params = table_2_5_3_dg_params()
    pending = build_participation_rhs(params, rhs_source="mia")
    with pytest.raises(ValueError, match="未确定"):
        pending.b_cost()
    resolved = resolve_mia(pending, fit_direct_intercepts(build_physical_cost(params)))
    assert resolved.b_cost().shape == (15,)


def test_quadratic_power_stationary() -> None:
    params = {
        "tau_start": 0,
        "tau_end": 1,
        "P_min": np.array([0.0]),
        "P_max": np.array([2.0]),
        "quadratic_coeff": 1.0,
    }
    ic = fit_direct_intercepts(build_physical_cost(params), slopes=np.array([1.0]))
    assert np.isclose(ic[0, 0], -0.25)


def test_inner_approx_on_grid() -> None:
    params = {
        "tau_start": 0,
        "tau_end": 1,
        "P_min": np.array([0.0]),
        "P_max": np.array([2.0]),
        "quadratic_coeff": 1.0,
        "unit_cost": 3.0,
    }
    physical = build_physical_cost(params)
    rhs = build_participation_rhs(params)
    x_lo, x_hi = physical.domain_at(0)
    for x in np.linspace(x_lo, x_hi, 40):
        envelope = float(np.max(np.array(PRICE_SEGMENTS_MWH) * x + rhs.power_f[0]))
        assert envelope <= physical.evaluate_period(0, float(x)) + 1e-9
