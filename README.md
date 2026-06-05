# TDM — Transmission-Distribution-Microgrid Coordination

**主配微协调** — 输配电与微电网协调优化平台

## 简介

TDM（Transmission-Distribution-Microgrid）面向输电网、配电网与微电网的协同运行与优化调度，提供统一的建模、仿真与协调控制框架。

## 项目结构

```
tdm/
├── src/tdm/          # 核心源码
│   ├── core/         # 协调控制核心逻辑
│   ├── models/       # 电力系统数据模型
│   ├── simulation/   # 仿真引擎
│   └── utils/        # 工具函数
├── tests/            # 单元测试
├── config/           # 配置文件
└── docs/             # 文档
```

## 快速开始

### 环境要求

- Python >= 3.10

### 安装

```bash
# 克隆仓库
git clone https://github.com/tutu-er/transmission-distribution-microgrid.git
cd transmission-distribution-microgrid

# 创建虚拟环境
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # Linux/macOS

# 安装（开发模式）
pip install -e ".[dev]"
```

### 运行

```bash
# 查看帮助
tdm --help

# 运行测试
pytest
```

## 许可证

MIT License
