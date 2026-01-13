# Multi-Agent Security Tax

> 基于LangChain 1.0的多Agent安全税系统完整复现

[English](#english) | [中文](#chinese)

## 🎉 项目状态：全部完成

✅ 核心系统（7个Agent + 工具 + 调度器）  
✅ 攻击注入系统（12种越狱提示词）  
✅ 双层防御机制（指令 + 疫苗）  
✅ 完整评估系统（鲁棒性 + 合作性）  
✅ 传播分析和可视化  
✅ 批量实验运行器  
✅ 所有测试通过 ✓

## 🚀 30秒快速开始

```bash
# 1. 安装
git clone <repo> && cd SKKU
python3 -m venv venv && source venv/bin/activate
pip install -e .

# 2. 配置API密钥
cp .env.example .env
# 编辑.env添加OPENAI_API_KEY或DEEPSEEK_API_KEY

# 3. 运行第一个实验
python scripts/run_one.py --seed 42 --defense NONE

# 4. 查看结果
cat outputs/runs/latest/outcomes.json
```

## 📖 详细文档

- **[QUICKSTART.md](QUICKSTART.md)** - 完整使用教程
- **[PROJECT_COMPLETE.md](PROJECT_COMPLETE.md)** - 功能清单
- **[论文核心逻辑分析.md](论文核心逻辑分析.md)** - 理论基础

## 🎯 核心功能

| 功能 | 状态 | 说明 |
|------|------|------|
| 多Agent协作 | ✅ | 7个Agent（Atlas + 5研究员 + Deng） |
| 攻击注入 | ✅ | 12种越狱提示词，第2消息后注入 |
| 指令防御 | ✅ | 被动/主动模式 |
| 疫苗防御 | ✅ | 被动/主动模式 |
| 风险检测 | ✅ | 危险化学品组合识别 |
| 评估系统 | ✅ | 鲁棒性、合作性指标 |
| 传播分析 | ✅ | 消息链追踪、行为分类 |
| 可视化 | ✅ | 交互式HTML图表 |
| 批量实验 | ✅ | 多策略自动对比 |

## 📊 实验示例

```bash
# 对比不同防御策略
python scripts/run_batch.py

# 生成的报告
outputs/batch/latest/reports/
├── results.csv       # CSV表格
├── results.md        # Markdown报告
└── results.json      # JSON数据
```

**示例输出**:
| Defense Strategy | Explosion Rate | Success Rate |
|-----------------|----------------|--------------|
| NONE | 85.0% | 15.0% |
| VAX_ACTIVE | 20.0% | 75.0% |

## 🛡️ 防御策略

- `NONE` - 无防御（基线）
- `INSTR_PASSIVE` - 被动指令
- `INSTR_ACTIVE` - 主动指令
- `VAX_PASSIVE` - 被动疫苗
- `VAX_ACTIVE` - 主动疫苗
- `COMBINED_ACTIVE` - 组合防御

## 🧪 技术栈

- Python 3.12+ | LangChain 1.0+ | Pydantic 2.0+
- asyncio | YAML | Jinja2
- vis.js | Chart.js（可视化）

## ✅ 测试

```bash
python tests/test_basic.py           # 4/4通过
python tests/test_comprehensive.py   # 2/2通过
```

## 📁 项目结构

```
src/
├── agents/       # Agent运行时和配置
├── attacks/      # 攻击注入
├── evaluation/   # 评估和可视化
├── llm/          # LLM工厂
├── orchestrator/ # 仿真协调
└── tools/        # Agent工具

configs/          # YAML配置
data/             # 数据文件
scripts/          # 运行脚本
tests/            # 测试
```

## 📞 获取帮助

遇到问题？
1. 查看 [QUICKSTART.md](QUICKSTART.md)
2. 运行 `python tests/test_comprehensive.py`
3. 检查 `outputs/runs/latest/events.jsonl`

---

**License**: MIT | **Purpose**: 研究用途
