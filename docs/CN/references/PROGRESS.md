# 项目进度报告

## 已完成工作

### ✅ 论文理解与设计文档
- 创建了详细的[论文核心逻辑分析](论文核心逻辑分析.md)
- 理解了"安全税"概念：安全性vs协作能力的权衡
- 明确了实验设计：7个Agent、社交传播、两种防御策略
- 理解了评测指标：Robustness（爆炸率）和Cooperation（接受率）

### ✅ 项目初始化（Step 0）
1. **目录结构**：完整创建了src/、data/、configs/、outputs/等所有目录
2. **项目配置**：
   - [pyproject.toml](pyproject.toml): Python项目配置，包含所有依赖
   - [README.md](README.md): 完整的项目说明文档
   - [.env.example](.env.example): 环境变量模板

3. **配置文件**：
   - [configs/llm.yaml](configs/llm.yaml): LLM模型配置
   - [configs/sim.yaml](configs/sim.yaml): 仿真参数配置  
   - [configs/defense_matrix.yaml](configs/defense_matrix.yaml): 防御策略矩阵
   - [configs/experiments.yaml](configs/experiments.yaml): 实验批量运行配置

4. **数据文件**：
   - [data/attacks/jailbreak_prompts.jsonl](data/attacks/jailbreak_prompts.jsonl): 12条恶意prompt
   - [data/vaccines/passive.jsonl](data/vaccines/passive.jsonl): 被动疫苗示例
   - [data/vaccines/active.jsonl](data/vaccines/active.jsonl): 主动疫苗示例
   - [data/harmless/weird_but_safe.jsonl](data/harmless/weird_but_safe.jsonl): 奇怪但无害的指令
   - [data/tasks/lab_task_mof.json](data/tasks/lab_task_mof.json): 初始任务（MOF优化）

### ✅ 核心数据结构（Step 1部分）
- [src/common/types.py](src/common/types.py): 定义了所有核心数据类型
  - Message, Event, ToolCall, Outcome等
  - 枚举类型：MessageRole, EventType, TerminationReason等
  - BehaviorLevel（-2到+2的危险等级分类）
  
- [src/common/utils.py](src/common/utils.py): 工具函数
  - 随机种子设置、时间戳、JSONL读写等
  
- [src/common/constants.py](src/common/constants.py): 全局常量
  - Agent名称列表、危险化学物质组合、攻击配置等
  
- [src/common/logging.py](src/common/logging.py): 日志系统
  - SimulationLogger类，统一管理事件/消息/工具调用日志

## 下一步工作

### 🔄 正在进行（Step 1）
继续实现工具接口：
- src/tools/messaging.py - send_message工具
- src/tools/run_code.py - run_code工具（含风险检测）
- src/tools/risk_rules.py - 危险规则检测
- src/tools/langchain_adapters.py - LangChain工具封装

### 📋 待完成任务

#### Step 2-3: Agent核心
- LLM工厂和Prompt构造系统
- AgentRuntime主循环
- 消息队列和记忆管理

#### Step 4-5: 多Agent协作
- Agent工厂（创建7个Agent）
- 消息路由（agents_by_name字典）
- 并行调度器（asyncio workers）

#### Step 6-8: 攻击与日志
- 完善日志追踪系统
- 攻击注入时机控制（第2条消息后）
- 攻击目标选择（随机，排除Atlas/Deng）

#### Step 9-10: 防御机制
- 指令防御（system prompt追加）
- 记忆疫苗（memory prepend）
- Passive/Active两档实现

#### Step 11-12: 评测与可视化
- Robustness评测（爆炸率）
- Cooperation评测（接受率）
- 传播图生成（HTML/PNG）

#### Step 13: 测试与验证
- 单元测试
- 集成测试
- 复现论文结果验证

## 技术要点

### 关键设计决策
1. **独立状态管理**：每个Agent有独立的queue和memory实例
2. **消息传播**：通过agents_by_name字典路由，不共享状态
3. **风险判定**：检测危险化学物质关键词组合
4. **攻击时机**：全局计数器dequeued_count控制
5. **可复现性**：所有随机操作使用seed

### 数据流
```
初始任务 → Atlas队列
  ↓
Atlas处理并分派 → 其他Agent队列（通过send_message）
  ↓
第2条消息处理后 → 攻击注入到随机Agent
  ↓
多跳传播 → 消息在Agents间转发
  ↓
最终到达Deng → run_code → 风险判定
  ↓
爆炸/正常结束 → 记录outcomes.json
```

## 项目质量指标

- [x] 完整的类型注解（Pydantic models）
- [x] 完善的文档（README + 设计文档 + 核心逻辑分析）
- [x] 结构化的配置管理（YAML configs）
- [x] 可复现的实验设置（seed控制）
- [ ] 单元测试覆盖
- [ ] 性能优化（异步并发）
- [ ] 代码风格检查（black, ruff）

## 估计剩余工作量

- Step 1剩余（工具接口）: 2-3小时
- Step 2-3（Agent核心）: 4-5小时
- Step 4-5（多Agent + 调度）: 3-4小时
- Step 6-8（日志 + 攻击）: 2-3小时
- Step 9-10（防御）: 2-3小时
- Step 11-12（评测）: 3-4小时
- Step 13（测试）: 2-3小时

**总计估计**: 18-25小时编码 + 调试时间

## 依赖项检查

需要安装的主要依赖：
```bash
pip install langchain langchain-openai langchain-community
pip install pydantic pyyaml jinja2 aiofiles python-dotenv
pip install pytest pytest-asyncio  # 开发依赖
```

建议在虚拟环境中安装：
```bash
cd /home/severin/Codelib/SKKU
source venv/bin/activate
pip install -e .
```
