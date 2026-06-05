"""仿真引擎."""

from dataclasses import dataclass, field
from typing import Any

from tdm.models.network import Network


@dataclass
class SimulationEngine:
    """主配微协调仿真引擎."""

    network: Network
    time_step_s: float = 1.0
    results: list[dict[str, Any]] = field(default_factory=list)

    def step(self) -> dict[str, Any]:
        """推进一个仿真时间步."""
        result = {
            "time_step_s": self.time_step_s,
            "buses": len(self.network.buses),
            "lines": len(self.network.lines),
        }
        self.results.append(result)
        return result
