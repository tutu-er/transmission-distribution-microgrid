"""电网拓扑数据模型."""

from dataclasses import dataclass, field


@dataclass
class Bus:
    """母线节点."""

    id: int
    name: str
    voltage_kv: float = 10.0
    bus_type: str = "PQ"  # PQ / PV / Slack


@dataclass
class Line:
    """输电线路."""

    id: int
    from_bus: int
    to_bus: int
    resistance: float = 0.0
    reactance: float = 0.0


@dataclass
class Network:
    """电网拓扑."""

    name: str = "default-network"
    buses: list[Bus] = field(default_factory=list)
    lines: list[Line] = field(default_factory=list)

    def add_bus(self, bus: Bus) -> None:
        self.buses.append(bus)

    def add_line(self, line: Line) -> None:
        self.lines.append(line)
