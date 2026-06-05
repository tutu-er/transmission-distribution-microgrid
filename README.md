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

本项目**必须使用 Conda 环境 `tdm`**，不要直接使用系统 Python 或 `base` 环境。

| 项目 | 说明 |
|------|------|
| 环境名称 | `tdm` |
| Python | >= 3.10（environment.yml 固定为 3.12） |
| 依赖清单 | `environment.yml` |
| IDE 配置 | `.vscode/settings.json` 已指定解释器与默认终端 |

### 安装

```bash
# 克隆仓库
git clone https://github.com/tutu-er/transmission-distribution-microgrid.git
cd transmission-distribution-microgrid

# 创建 conda 环境（仅需一次）
conda env create -f environment.yml

# 手动使用时激活
conda activate tdm
```

### 在 Cursor / VS Code 中使用

1. 用 Cursor 打开本项目根目录 `TDM/`
2. 右下角 Python 解释器应显示 **`tdm`**（路径含 `envs/tdm`）
3. 新建终端（`` Ctrl+` ``）应自动执行 `conda activate tdm`，提示符出现 `(tdm)`

若未自动激活，请检查：

- 是否打开了项目根目录（含 `environment.yml` 和 `.vscode/`）
- 是否已安装 **Python** 扩展
- 命令面板 → **Python: Select Interpreter** → 选择 `tdm`
- 命令面板 → **Developer: Reload Window** 重载窗口

若 Conda 安装路径不是 `D:\apps\miniconda3`，请修改 `.vscode/settings.json` 中的 `python.defaultInterpreterPath` 和 `python.condaPath`。

### 运行

```bash
# 查看帮助
tdm --help

# 运行测试
pytest
```

## 许可证

MIT License
