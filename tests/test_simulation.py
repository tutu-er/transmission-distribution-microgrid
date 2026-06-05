"""仿真引擎测试."""

from tdm.models.network import Bus, Network
from tdm.simulation.engine import SimulationEngine


def test_simulation_step() -> None:
    net = Network()
    net.add_bus(Bus(id=1, name="Bus1"))
    engine = SimulationEngine(network=net, time_step_s=0.5)

    result = engine.step()
    assert result["buses"] == 1
    assert result["time_step_s"] == 0.5
    assert len(engine.results) == 1
