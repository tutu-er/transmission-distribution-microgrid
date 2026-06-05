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

推荐使用 Conda 环境 `tdm`（项目已配置为默认解释器）：

```bash
# 克隆仓库
git clone https://github.com/tutu-er/transmission-distribution-microgrid.git
cd transmission-distribution-microgrid

# 创建并激活 conda 环境
conda env create -f environment.yml
conda activate tdm
```

在 Cursor / VS Code 中打开本项目后，将自动选用 `tdm` 环境；新开终端也会自动激活。

### 运行

```bash
# 查看帮助
tdm --help

# 运行测试
pytest
```

## 许可证

MIT License
