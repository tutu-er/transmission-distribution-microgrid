"""MATPOWER / PYPOWER 算例读取接口."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
from pandapower.converter.pypower import to_ppc
from pandapower.networks.power_system_test_cases import case33bw as _pp_case33bw

from tdm.models.network import Bus, Line, Network

# MATPOWER bus 列索引
BUS_I = 0
BUS_TYPE = 1
BUS_PD = 2
BUS_QD = 3
BUS_BASE_KV = 9

# MATPOWER branch 列索引
BR_F_BUS = 0
BR_T_BUS = 1
BR_R = 2
BR_X = 3

_BUS_TYPE_MAP = {1: "PQ", 2: "PV", 3: "Slack"}


@dataclass
class MatpowerCase:
    """MATPOWER mpc 算例容器（与 PYPOWER 格式兼容）."""

    name: str
    base_mva: float
    bus: np.ndarray
    branch: np.ndarray
    gen: np.ndarray
    gencost: np.ndarray | None = None
    version: str = "2"
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mpc(
        cls,
        mpc: dict[str, Any],
        name: str = "case",
        metadata: dict[str, Any] | None = None,
    ) -> MatpowerCase:
        """从 mpc 字典构建算例."""
        extra = {
            key: value
            for key, value in mpc.items()
            if key not in {"baseMVA", "bus", "branch", "gen", "gencost", "version"}
        }
        if metadata:
            extra.update(metadata)

        return cls(
            name=name,
            base_mva=float(mpc["baseMVA"]),
            bus=np.asarray(mpc["bus"], dtype=float),
            branch=np.asarray(mpc["branch"], dtype=float),
            gen=np.asarray(mpc["gen"], dtype=float),
            gencost=np.asarray(mpc["gencost"], dtype=float) if "gencost" in mpc else None,
            version=str(mpc.get("version", "2")),
            metadata=extra,
        )

    @property
    def n_bus(self) -> int:
        return int(self.bus.shape[0])

    @property
    def n_branch(self) -> int:
        return int(self.branch.shape[0])

    def to_mpc(self) -> dict[str, Any]:
        """导出为 PYPOWER / MATPOWER mpc 字典."""
        mpc: dict[str, Any] = {
            "version": self.version,
            "baseMVA": self.base_mva,
            "bus": self.bus,
            "branch": self.branch,
            "gen": self.gen,
        }
        if self.gencost is not None:
            mpc["gencost"] = self.gencost
        mpc.update(self.metadata)
        return mpc

    def to_network(self) -> Network:
        """转换为项目内部的简化网络拓扑模型."""
        network = Network(name=self.name)

        for row in self.bus:
            bus_id = int(row[BUS_I])
            bus_type = _BUS_TYPE_MAP.get(int(row[BUS_TYPE]), "PQ")
            network.add_bus(
                Bus(
                    id=bus_id,
                    name=f"Bus{bus_id}",
                    voltage_kv=float(row[BUS_BASE_KV]),
                    bus_type=bus_type,
                )
            )

        for idx, row in enumerate(self.branch, start=1):
            network.add_line(
                Line(
                    id=idx,
                    from_bus=int(row[BR_F_BUS]),
                    to_bus=int(row[BR_T_BUS]),
                    resistance=float(row[BR_R]),
                    reactance=float(row[BR_X]),
                )
            )

        return network


def load_case33bw() -> MatpowerCase:
    """读取 IEEE 33 节点配电网算例（Baran & Wu, case33bw）.

    该算例通过 pandapower 标准测试库加载，并转换为 MATPOWER mpc 格式，
    可直接用于 PYPOWER 潮流/优化或本项目 Network 模型。
    """
    net = _pp_case33bw()
    mpc = to_ppc(net, init="flat")
    return MatpowerCase.from_mpc(
        mpc,
        name="case33bw",
        metadata={
            "source": "pandapower.networks.case33bw",
            "description": "IEEE 33-bus radial distribution feeder (Baran & Wu)",
            "frequency_hz": float(net.f_hz),
        },
    )


def load_matpower_case(name: str) -> MatpowerCase:
    """按名称加载内置 MATPOWER 算例.

    当前支持:
        - ``case33bw`` / ``case33``: IEEE 33 节点配电网
    """
    key = name.lower().removesuffix(".m")
    if key in {"case33bw", "case33"}:
        return load_case33bw()
    raise ValueError(f"不支持的算例名称: {name}")


def load_matpower_file(path: str | Path) -> MatpowerCase:
    """从 MATPOWER .m 或 PYPOWER .py 算例文件加载."""
    from pypower.api import loadcase

    case_path = Path(path)
    if not case_path.exists():
        raise FileNotFoundError(f"算例文件不存在: {case_path}")

    mpc = loadcase(str(case_path))
    return MatpowerCase.from_mpc(mpc, name=case_path.stem)
