"""电网模型测试."""

from tdm.models.network import Bus, Line, Network


def test_network_topology() -> None:
    net = Network(name="test-net")
    net.add_bus(Bus(id=1, name="Bus1", voltage_kv=110.0))
    net.add_bus(Bus(id=2, name="Bus2", voltage_kv=10.0))
    net.add_line(Line(id=1, from_bus=1, to_bus=2, resistance=0.01, reactance=0.05))

    assert len(net.buses) == 2
    assert len(net.lines) == 1
