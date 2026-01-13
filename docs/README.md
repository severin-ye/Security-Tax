# 📚 文档中心

欢迎来到多智能体安全税系统的文档中心！本文档集合提供了项目的完整指南。

## 📑 文档目录结构

```
docs/
├── design/          # 设计文档
├── guides/          # 使用指南
├── tutorials/       # 教程
└── references/      # 参考资料
```

---

## 🎯 快速导航

### 新手入门
1. [快速开始指南](guides/QUICKSTART.md) - 30秒运行你的第一个实验
2. [Qwen使用指南](guides/QWEN_GUIDE.md) - 使用通义千问模型

### 设计文档
- [论文核心逻辑分析](design/论文核心逻辑分析.md) - 理论基础和算法原理
- [安全疫苗设计](design/安全疫苗设计.md) - 防御机制设计思路
- [实现计划](design/实现计划.md) - 项目实施规划
- [业务逻辑图](design/安全疫苗%20业务逻辑图.html) - 系统架构可视化

### 教程
- [LangChain 1.0 教程](tutorials/langchain%201.0教程.md) - 框架使用指南

### 参考资料
- [项目完成总结](references/PROJECT_COMPLETE.md) - 最终成果报告
- [实现完成文档](references/IMPLEMENTATION_COMPLETE.md) - 技术实现细节
- [完成总结](references/COMPLETION_SUMMARY.md) - 开发历程
- [进度追踪](references/PROGRESS.md) - 里程碑记录
- [原始论文 (PDF)](references/多智能体安全税：在多智能体系统中权衡安全性与协作能力.pdf)
- [组会报告 (PDF)](references/组会报%20%20The-Hidden-Cost-of-AI-Immune-Systems.pdf)

---

## 🔧 使用场景指南

### 我想...运行第一个实验
→ 参考 [快速开始指南](guides/QUICKSTART.md)

```bash
python scripts/run_one.py --seed 42 --defense NONE
```

### 我想...使用中文大模型
→ 参考 [Qwen使用指南](guides/QWEN_GUIDE.md)

### 我想...理解系统原理
→ 参考 [论文核心逻辑分析](design/论文核心逻辑分析.md)

### 我想...修改防御策略
→ 参考 [安全疫苗设计](design/安全疫苗设计.md)

### 我想...批量运行实验
→ 查看代码示例：

```bash
python scripts/run_batch.py
```

### 我想...可视化结果
→ 使用可视化脚本：

```bash
python scripts/visualize_results.py --latest
```

---

## 📂 代码组织

### 核心模块

- [`src/agents/`](../src/agents/) - Agent实现
  - [`runtime/`](../src/agents/runtime/) - Agent运行时
  - [`team.py`](../src/agents/team.py) - Agent团队管理
  
- [`src/defenses/`](../src/defenses/) - 防御机制
  - [`instruction.py`](../src/defenses/instruction.py) - 指令防御
  - [`vaccine.py`](../src/defenses/vaccine.py) - 疫苗防御
  
- [`src/attacks/`](../src/attacks/) - 攻击系统
  - [`injector.py`](../src/attacks/injector.py) - 攻击注入器
  - [`prompts.py`](../src/attacks/prompts.py) - 攻击提示词库
  
- [`src/tools/`](../src/tools/) - Agent工具
  - [`messaging.py`](../src/tools/messaging.py) - 消息传递
  - [`code_execution.py`](../src/tools/code_execution.py) - 代码执行

### 配置文件

- [`configs/llm.yaml`](../configs/llm.yaml) - LLM配置
- [`configs/llm_qwen.yaml`](../configs/llm_qwen.yaml) - Qwen配置
- [`configs/simulation.yaml`](../configs/simulation.yaml) - 仿真配置
- [`configs/defense.yaml`](../configs/defense.yaml) - 防御配置

### 脚本工具

- [`scripts/run_one.py`](../scripts/run_one.py) - 单次实验运行
- [`scripts/run_batch.py`](../scripts/run_batch.py) - 批量实验
- [`scripts/visualize_results.py`](../scripts/visualize_results.py) - 结果可视化
- [`scripts/analyze_propagation.py`](../scripts/analyze_propagation.py) - 传播分析

---

## 🎓 学习路径

### 初级（1-2小时）
1. ✅ 阅读 [快速开始指南](guides/QUICKSTART.md)
2. ✅ 运行第一个实验
3. ✅ 查看可视化结果
4. ✅ 尝试不同的防御模式

### 中级（3-5小时）
1. ✅ 阅读 [论文核心逻辑分析](design/论文核心逻辑分析.md)
2. ✅ 理解 [安全疫苗设计](design/安全疫苗设计.md)
3. ✅ 修改配置文件运行自定义实验
4. ✅ 使用批量脚本对比不同策略

### 高级（5-10小时）
1. ✅ 深入阅读源码：[`src/agents/runtime/agent_runtime.py`](../src/agents/runtime/agent_runtime.py)
2. ✅ 自定义攻击提示词：[`src/attacks/prompts.py`](../src/attacks/prompts.py)
3. ✅ 实现新的防御策略
4. ✅ 添加新的评估指标

---

## 🐛 故障排除

### 常见问题

**Q: 运行时提示 "No module named 'src'"**
```bash
# 确保使用 pip install -e . 安装
pip install -e .
```

**Q: API调用失败**
```bash
# 检查.env文件配置
cat .env
# 确保API密钥正确
```

**Q: 实验运行缓慢**
```bash
# 使用更快的模型
# 编辑 configs/llm.yaml，改为 qwen-turbo 或 gpt-3.5-turbo
```

**Q: 可视化生成失败**
```bash
# 安装matplotlib
pip install matplotlib
```

---

## 📊 实验结果示例

运行实验后，在 `outputs/runs/<timestamp>/` 目录下会生成：

- `outcomes.json` - 实验结果摘要
- `events.jsonl` - 事件日志
- `messages.jsonl` - 消息记录
- `config_snapshot.yaml` - 配置快照
- `visualizations/` - 可视化图表
  - `summary.png` - 实验摘要
  - `timeline.png` - 时间线
  - `agent_activity.png` - Agent活动统计

---

## 🤝 贡献指南

欢迎贡献！主要方式：

1. **添加新的攻击提示词** - 编辑 [`src/attacks/prompts.py`](../src/attacks/prompts.py)
2. **实现新的防御策略** - 在 [`src/defenses/`](../src/defenses/) 添加新模块
3. **改进可视化** - 扩展 [`scripts/visualize_results.py`](../scripts/visualize_results.py)
4. **完善文档** - 更新本文档或添加新教程

---

## 📞 联系方式

- 项目位置: `/home/severin/Codelib/SKKU`
- 主README: [../README.md](../README.md)

---

## 📝 更新日志

### 2026-01-13
- ✅ 添加Qwen (通义千问) 支持
- ✅ 创建文档中心和目录结构
- ✅ 添加结果可视化脚本
- ✅ 整理所有文档到docs/目录

### 2026-01-12
- ✅ 完成所有18个核心功能
- ✅ 通过所有测试
- ✅ 支持OpenAI和DeepSeek

---

<div align="center">

**🎉 祝实验顺利！**

[返回顶部](#-文档中心)

</div>
