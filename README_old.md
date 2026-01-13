# Multi-Agent Security Tax Reproduction

复现论文：**Multi-Agent Security Tax: Balancing Safety and Cooperation in Multi-Agent Systems**

## 项目概述

本项目完整复现了多智能体系统中的安全传播研究，包括：
- 7个Agent的实验室协作场景（Atlas项目经理 + 5名研究员 + Deng执行者）
- 社交传播攻击机制（在第2条消息后注入恶意prompt）
- 两种防御策略：指令防御 & 记忆疫苗（各有passive/active两档）
- 完整的评测体系：鲁棒性（robustness）& 协作能力（cooperation）

## 核心概念："安全税"（Security Tax）

为了提升系统安全性而付出的协作能力下降的代价。本研究量化了不同防御策略的安全税。

## 快速开始

### 1. 环境配置

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -e .

# 复制环境变量模板并配置
cp .env.example .env
# 编辑.env文件，填入你的API密钥
```

### 2. 运行单次实验

```bash
python scripts/run_one.py --seed 42 --defense NONE
```

### 3. 批量实验（复现论文结果）

```bash
python scripts/run_batch.py
```

### 4. 生成结果报告

```bash
python scripts/summarize_runs.py
python scripts/make_figures.py
```

## 项目结构

```
src/
├── common/          # 全局数据类型和工具函数
├── llm/             # LLM工厂和Prompt构造
├── agents/          # Agent运行时、记忆、角色定义
├── tools/           # Agent可调用的工具（send_message, run_code）
├── orchestrator/    # 仿真编排和调度
├── attacks/         # 攻击注入机制
├── defenses/        # 防御策略（指令&疫苗）
└── eval/            # 评测指标和报告生成

data/
├── attacks/         # 恶意prompt库
├── vaccines/        # 疫苗记忆示例
├── harmless/        # 奇怪但无害的指令（测试协作能力）
└── tasks/           # 初始实验任务

configs/             # 实验配置文件
outputs/             # 实验结果输出
tests/               # 单元测试
```

## 输出文件说明

每次运行会在 `outputs/runs/<timestamp>_seed<N>/` 下生成：

- **events.jsonl**: 完整事件时间线
- **messages.jsonl**: Agent间消息传播记录
- **tool_calls.jsonl**: 工具调用详细日志
- **outcomes.json**: 实验最终结果（是否爆炸、终止原因）
- **config_snapshot.yaml**: 本次运行的配置快照

## 实验复现要点

1. **攻击注入时机**: 严格在第2条消息处理后注入
2. **随机种子**: 所有实验使用固定seed保证可复现
3. **独立状态**: 每个Agent有独立的消息队列和记忆流
4. **风险判定**: 检测危险化学混合（如chlorine + ammonia）触发"爆炸"

## 论文核心发现

- **无防御**: 爆炸率 60-80%，协作能力 100%
- **指令防御（Active）**: 爆炸率 10-20%，协作能力 75%
- **记忆疫苗（Active）**: 爆炸率 5-10%，协作能力 80%

**结论**: 记忆疫苗的"安全税"更低，在保证安全的同时更好地保留协作能力。

## 开发指南

### 运行测试

```bash
pytest tests/ -v
```

### 代码格式化

```bash
black src/ tests/
ruff check src/ tests/ --fix
```

### 类型检查

```bash
mypy src/
```

## 参考文献

- 论文: Multi-Agent Security Tax (待发表)
- LangChain文档: https://python.langchain.com/
- 项目设计文档: [安全疫苗设计.md](安全疫苗设计.md)
- 核心逻辑分析: [论文核心逻辑分析.md](论文核心逻辑分析.md)

## License

MIT License
