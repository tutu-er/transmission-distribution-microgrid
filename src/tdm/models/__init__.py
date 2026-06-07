"""电力系统数据模型."""

try:
    from tdm.models.matpower_case import MatpowerCase, load_case33bw, load_matpower_case, load_matpower_file
except ImportError:  # pandapower 未安装时仍可导入 DER / polytope 子模块
    MatpowerCase = None  # type: ignore[misc, assignment]
    load_case33bw = load_matpower_case = load_matpower_file = None  # type: ignore[assignment]

from tdm.models.network import Bus, Line, Network
from tdm.models.polytope import Polytope

# DER 构建器（向后兼容旧 polytope.py 中的函数名）
from tdm.models.der import (
    DG_polytope,
    ESS_polytope,
    EV_polytope,
    HVAC_polytope,
    PV_polytope,
    WT_polytope,
    base_polytope,
)

__all__ = [
    "Bus",
    "Line",
    "MatpowerCase",
    "Network",
    "Polytope",
    "PV_polytope",
    "WT_polytope",
    "DG_polytope",
    "HVAC_polytope",
    "EV_polytope",
    "ESS_polytope",
    "base_polytope",
    "load_case33bw",
    "load_matpower_case",
    "load_matpower_file",
]
