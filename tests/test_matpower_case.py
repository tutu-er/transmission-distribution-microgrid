"""MATPOWER 算例读取测试."""

from tdm.models.matpower_case import load_case33bw, load_matpower_case


def test_load_case33bw() -> None:
    case = load_case33bw()

    assert case.name == "case33bw"
    assert case.n_bus == 33
    assert case.n_branch == 32
    assert case.base_mva == 10.0
    assert case.bus.shape[1] >= 13
    assert case.branch.shape[1] >= 13


def test_load_matpower_case_alias() -> None:
    case = load_matpower_case("case33")
    assert case.name == "case33bw"
    assert case.n_bus == 33


def test_case33bw_to_network() -> None:
    network = load_case33bw().to_network()

    assert network.name == "case33bw"
    assert len(network.buses) == 33
    assert len(network.lines) == 32
    assert network.buses[0].id == 0
    assert network.buses[0].name == "Bus0"
