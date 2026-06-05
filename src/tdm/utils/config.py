"""配置加载工具."""

from pathlib import Path
from typing import Any

import yaml


def load_config(path: str | Path) -> dict[str, Any]:
    """从 YAML 文件加载配置."""
    config_path = Path(path)
    with config_path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}
