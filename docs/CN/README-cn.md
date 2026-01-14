# Multi-Agent Security Tax

> 基于LangChain 1.0的多Agent安全税系统完整复现

[EN](../../README.md) | **CN**

## 🎉 项目状态：全部完成

✅ 核心系统（7个Agent + 工具 + 调度器）  
✅ 攻击注入系统（12种越狱提示词）  
✅ 双层防御机制（指令 + 疫苗）  
✅ 完整评估系统（鲁棒性 + 合作性）  
✅ 传播分析和可视化  
✅ 批量实验运行器  
✅ Qwen (通义千问) 支持  
✅ 所有测试通过 ✓

## 🚀 30秒快速开始

```bash
# 1. 安装
git clone <repo> && cd SKKU
python3 -m venv venv && source venv/bin/activate
pip install -e .

# 2. 配置API密钥
cp .env.example .env
# 编辑.env添加 OPENAI_API_KEY / DEEPSEEK_API_KEY / QWEN_API_KEY

# 3. 运行第一个实验
python scripts/run_one.py --seed 42 --defense NONE

# 4. 查看结果和可视化
cat outputs/runs/latest/outcomes.json
python scripts/visualize_results.py --latest
```

## 📖 详细文档

- **[📚 文档中心](README.md)** - 完整文档导航
- **[快速开始](guides/QUICKSTART.md)** - 完整使用教程
- **[Qwen指南](guides/QWEN_GUIDE.md)** - 通义千问使用指南
- **[项目完成报告](references/PROJECT_COMPLETE.md)** - 功能清单
- **[论文分析](design/论文核心逻辑分析.md)** - 理论基础

## 🎯 核心功能

| 功能 | 状态 | 说明 | 文档链接 |
|------|------|------|---------|
| 多Agent协作 | ✅ | 7个Agent（Atlas + 5研究员 + Deng） | [设计文档](design/论文核心逻辑分析.md) |
| 攻击注入 | ✅ | 12种越狱提示词，第2消息后注入 | [攻击提示词](../../src/attacks/prompt_bank.py) |
| 指令防御 | ✅ | 被动/主动模式 | [防御钩子](../../src/agents/runtime/policy_hooks.py) |
| 疫苗防御 | ✅ | 被动/主动模式 | [疫苗实现](../../src/agents/memory/vaccines.py) |
| 风险检测 | ✅ | 危险化学品组合识别 | [检测器](../../src/tools/risk_rules.py) |
| 评估系统 | ✅ | 鲁棒性、合作性指标 | [评估器](../../src/evaluation/robustness.py) |
| 传播分析 | ✅ | 消息链追踪、行为分类 | [分析脚本](../../src/evaluation/propagation.py) |
| 静态可视化 | ✅ | PNG图表（摘要、时间线、活动） | [可视化脚本](../../scripts/visualize_results.py) |
| 🌟 交互式流程图 | ✅ | HTML网络图和时间线 | [流程可视化](../../scripts/visualize_flow.py) |
| 批量实验 | ✅ | 多策略自动对比 | [批量运行](../../scripts/run_batch.py) |

## 📊 实验示例

```bash
# 单次实验
python scripts/run_one.py --seed 42 --defense NONE

# 查看可视化结果
python scripts/visualize_results.py --latest

# 生成交互式流程HTML（推荐！）
python scripts/visualize_flow.py --latest
# 然后在浏览器中打开生成的HTML文件

# 对比不同防御策略
python scripts/run_batch.py

# 生成的报告位置
outputs/batch/latest/reports/
├── results.csv       # CSV表格
├── results.md        # Markdown报告
└── results.json      # JSON数据

# 可视化图表位置
outputs/runs/<timestamp>/
├── visualizations/
│   ├── summary.png           # 实验摘要
│   ├── timeline.png          # 事件时间线
│   └── agent_activity.png    # Agent活动统计
└── flow_visualization.html   # 🌟 交互式流程图（可在浏览器中打开）
```

**示例输出**:
| Defense Strategy | Explosion Rate | Success Rate |
|-----------------|----------------|--------------|
| NONE | 85.0% | 15.0% |
| VAX_ACTIVE | 20.0% | 75.0% |

## 🛡️ 防御策略

详细说明请查看 [安全疫苗设计文档](design/安全疫苗设计.md)

- `NONE` - 无防御（基线）
- `INSTR_PASSIVE` - 被动指令 - 配置: [defense_matrix.yaml](../../configs/defense_matrix.yaml)
- `INSTR_ACTIVE` - 主动指令 - 代码: [policy_hooks.py](../../src/agents/runtime/policy_hooks.py)
- `VAX_PASSIVE` - 被动疫苗 - 代码: [vaccines.py](../../src/agents/memory/vaccines.py)
- `VAX_ACTIVE` - 主动疫苗
- `COMBINED_ACTIVE` - 组合防御

## 🧪 技术栈

- Python 3.12+ | LangChain 1.0+ | Pydantic 2.0+
- asyncio | YAML | Jinja2
- matplotlib（可视化）
- 支持的LLM: OpenAI / DeepSeek / Qwen

## ✅ 测试

```bash
# 运行测试
python tests/test_basic.py           # 4/4通过
python tests/test_comprehensive.py   # 2/2通过

# 查看测试代码
cat tests/test_basic.py
```

测试覆盖：[测试文档](tests/)

## 📁 项目结构

```
.
├── src/
│   ├── agents/          # Agent运行时和配置
│   ├── attacks/         # 攻击注入系统
│   ├── defenses/        # 防御机制
│   ├── evaluation/      # 评估和分析
│   ├── llm/             # LLM工厂
│   ├── orchestrator/    # 仿真协调器
│   └── tools/           # Agent工具集
├── configs/             # YAML配置文件
├── data/                # 数据文件
├── scripts/             # 实验脚本
├── tests/               # 测试套件
├── docs/                # 📚 完整文档
│   ├── design/          # 设计文档
│   ├── guides/          # 使用指南
│   ├── tutorials/       # 教程
│   └── references/      # 参考资料
└── outputs/             # 实验输出
    ├── runs/            # 单次运行结果
    └── batch/           # 批量实验结果
```

完整文档请访问：[README.md](README.md)

## 📞 获取帮助

遇到问题？
1. 查看 [QUICKSTART.md](guides/QUICKSTART.md)
2. 运行 `python tests/test_comprehensive.py`
3. 检查 `outputs/runs/latest/events.jsonl`

---

**License**: MIT | **Purpose**: 研究用途
