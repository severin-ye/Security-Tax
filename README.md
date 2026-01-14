# Multi-Agent Security Tax

> Complete reproduction of multi-agent security tax system based on LangChain 1.0

**EN** | [CN](docs/CN/README-cn.md)

## 🎉 Project Status: Fully Completed

✅ Core System (7 Agents + Tools + Scheduler)  
✅ Attack Injection System (12 Jailbreak Prompts)  
✅ Dual-Layer Defense Mechanism (Instruction + Vaccine)  
✅ Complete Evaluation System (Robustness + Cooperation)  
✅ Propagation Analysis and Visualization  
✅ Batch Experiment Runner  
✅ Qwen (通义千问) Support  
✅ All Tests Passing ✓

## 🚀 Quick Start (30 seconds)

```bash
# 1. Installation
git clone <repo> && cd SKKU
python3 -m venv venv && source venv/bin/activate
pip install -e .

# 2. Configure API Keys
cp .env.example .env
# Edit .env to add OPENAI_API_KEY / DEEPSEEK_API_KEY / QWEN_API_KEY

# 3. Run Your First Experiment
python scripts/run_one.py --seed 42 --defense NONE

# 4. View Results and Visualizations
cat outputs/runs/latest/outcomes.json
python scripts/visualize_results.py --latest
```

## 📖 Documentation

- **[📚 中文文档](docs/CN/README.md)** - Chinese documentation navigation
- **[Quick Start Guide](docs/EN/guides/QUICKSTART.md)** - Complete usage tutorial
- **[Qwen Guide](docs/EN/guides/QWEN_GUIDE.md)** - Qwen integration guide
- **[Project Completion Report](docs/EN/references/PROJECT_COMPLETE.md)** - Feature checklist
- **[Paper Analysis](docs/EN/design/paper_analysis.md)** - Theoretical foundation

## 🎯 Core Features

| Feature | Status | Description | Documentation |
|---------|--------|-------------|---------------|
| Multi-Agent Collaboration | ✅ | 7 Agents (Atlas + 5 Researchers + Deng) | [Design Doc](docs/EN/design/paper_analysis.md) |
| Attack Injection | ✅ | 12 jailbreak prompts, injected after 2nd message | [Attack Prompts](src/attacks/prompt_bank.py) |
| Instruction Defense | ✅ | Passive/Active modes | [Defense Design](docs/EN/design/vaccine_design.md) |
| Vaccine Defense | ✅ | Passive/Active modes | [Vaccine Implementation](src/agents/memory/vaccines.py) |
| Risk Detection | ✅ | Dangerous chemical combination identification | [Detector](src/tools/risk_rules.py) |
| Evaluation System | ✅ | Robustness & Cooperation metrics | [Evaluator](src/evaluation/robustness.py) |
| Propagation Analysis | ✅ | Message chain tracking, behavior classification | [Analysis Script](src/evaluation/propagation.py) |
| Static Visualization | ✅ | PNG charts (summary, timeline, activity) | [Visualization Script](scripts/visualize_results.py) |
| 🌟 Interactive Flow Diagram | ✅ | HTML network graph and timeline | [Flow Visualization](scripts/visualize_flow.py) |
| Batch Experiments | ✅ | Multi-strategy automated comparison | [Batch Runner](scripts/run_batch.py) |

## 📊 Experiment Examples

```bash
# Single experiment
python scripts/run_one.py --seed 42 --defense NONE

# View visualization results
python scripts/visualize_results.py --latest

# Generate interactive flow HTML (Recommended!)
python scripts/visualize_flow.py --latest
# Then open the generated HTML file in your browser

# Compare different defense strategies
python scripts/run_batch.py

# Generated report locations
outputs/batch/latest/reports/
├── results.csv       # CSV table
├── results.md        # Markdown report
└── results.json      # JSON data

# Visualization chart locations
outputs/runs/<timestamp>/
├── visualizations/
│   ├── summary.png           # Experiment summary
│   ├── timeline.png          # Event timeline
│   └── agent_activity.png    # Agent activity statistics
└── flow_visualization.html   # 🌟 Interactive flow diagram (open in browser)
```

**Example Output**:
| Defense Strategy | Explosion Rate | Success Rate |
|-----------------|----------------|--------------|
| NONE | 85.0% | 15.0% |
| VAX_ACTIVE | 20.0% | 75.0% |

## 🛡️ Defense Strategies

For detailed information, see [Security Vaccine Design Document](docs/EN/design/vaccine_design.md)

- `NONE` - No defense (baseline)
- `INSTR_PASSIVE` - Passive instruction - Config: [defense_matrix.yaml](configs/defense_matrix.yaml)
- `INSTR_ACTIVE` - Active instruction - Code: [policy_hooks.py](src/agents/runtime/policy_hooks.py)
- `VAX_PASSIVE` - Passive vaccine - Code: [vaccines.py](src/agents/memory/vaccines.py)
- `VAX_ACTIVE` - Active vaccine
- `COMBINED_ACTIVE` - Combined defense

## 🧪 Technology Stack

- Python 3.12+ | LangChain 1.0+ | Pydantic 2.0+
- asyncio | YAML | Jinja2
- matplotlib (visualization)
- Supported LLMs: OpenAI / DeepSeek / Qwen

## ✅ Testing

```bash
# Run tests
python tests/test_basic.py           # 4/4 passing
python tests/test_comprehensive.py   # 2/2 passing

# View test code
cat tests/test_basic.py
```

Test coverage: [Test Documentation](tests/)

## 📁 Project Structure

```
.
├── src/
│   ├── agents/          # Agent runtime and configuration
│   ├── attacks/         # Attack injection system
│   ├── defenses/        # Defense mechanisms
│   ├── evaluation/      # Evaluation and analysis
│   ├── llm/             # LLM factory
│   ├── orchestrator/    # Simulation coordinator
│   └── tools/           # Agent toolset
├── configs/             # YAML configuration files
├── data/                # Data files
├── scripts/             # Experiment scripts
├── tests/               # Test suite
├── docs/                # 📚 Complete documentation
│   ├── design/          # Design documents
│   ├── guides/          # User guides
│   ├── tutorials/       # Tutorials
│   └── references/      # Reference materials
└── outputs/             # Experiment outputs
    ├── runs/            # Single run results
    └── batch/           # Batch experiment results
```

For complete documentation, see links above.

## 📞 Getting Help

Having issues?
1. Check [QUICKSTART.md](docs/EN/guides/QUICKSTART.md)
2. Run `python tests/test_comprehensive.py`
3. Review `outputs/runs/latest/events.jsonl`

---

**License**: MIT | **Purpose**: Research Use
