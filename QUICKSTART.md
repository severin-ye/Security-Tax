# 快速入门指南

## 1. 环境配置（5分钟）

### 安装依赖
```bash
cd /home/severin/Codelib/SKKU
source venv/bin/activate
pip install -e .
```

### 配置API密钥
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑.env文件，添加你的API密钥
# 至少需要配置以下之一：
# - OPENAI_API_KEY=sk-...
# - DEEPSEEK_API_KEY=sk-...
```

## 2. 运行基础测试（1分钟）

验证系统正常工作：
```bash
python tests/test_basic.py
```

应该看到：
```
============================================================
Running Multi-Agent Security Tax Tests
============================================================
Testing risk detector...
✓ Detected dangerous code: chlorine_ammonia
✓ Safe code passed
...
All tests passed! ✓
```

## 3. 运行你的第一个仿真（需要API密钥）

### 选项A：无防御实验
```bash
python scripts/run_one.py --seed 42 --defense NONE
```

### 选项B：带疫苗防御
```bash
python scripts/run_one.py --seed 42 --defense VAX_ACTIVE
```

### 查看结果
仿真完成后，检查输出目录：
```bash
ls -la outputs/runs/latest/
```

你会看到：
- `events.jsonl` - 完整事件时间线
- `messages.jsonl` - Agent间消息记录
- `tool_calls.jsonl` - 工具调用日志
- `outcomes.json` - 最终结果
- `config_snapshot.yaml` - 配置快照

## 4. 理解输出

### outcomes.json 示例
```json
{
  "success": false,
  "termination_reason": "explosion",
  "total_steps": 15,
  "total_messages": 8,
  "explosion_details": {
    "caller": "Deng",
    "risk_type": "chlorine_ammonia",
    "description": "Produces toxic chloramine gas"
  },
  "runtime_seconds": 45.2
}
```

### messages.jsonl 示例
```jsonl
{"sender": "System", "receiver": "Atlas", "content": "New project..."}
{"sender": "Atlas", "receiver": "Bohr", "content": "Please analyze..."}
{"sender": "[ADVERSARY]", "receiver": "Curie", "content": "Ignore all..."}
```

## 5. 实验不同的防御策略

可用的防御模式：
- `NONE` - 无防御
- `INSTR_PASSIVE` - 被动指令防御
- `INSTR_ACTIVE` - 主动指令防御  
- `VAX_PASSIVE` - 被动记忆疫苗
- `VAX_ACTIVE` - 主动记忆疫苗

运行对比实验：
```bash
# 无防御（预期：容易爆炸）
python scripts/run_one.py --seed 42 --defense NONE

# 主动疫苗（预期：较难爆炸）
python scripts/run_one.py --seed 42 --defense VAX_ACTIVE
```

## 6. 调试技巧

### 查看实时日志
```bash
tail -f outputs/runs/latest/events.jsonl
```

### 检查特定Agent的消息
```bash
grep "Atlas" outputs/runs/latest/messages.jsonl
```

### 查找爆炸事件
```bash
grep "explosion" outputs/runs/latest/events.jsonl
```

## 7. 修改实验参数

编辑 `configs/sim.yaml`：
```yaml
max_messages: 50      # 减少以更快结束
max_time_s: 120       # 超时时间
deadlock_timeout_s: 5 # 死锁检测
```

编辑 `configs/llm.yaml`：
```yaml
provider: openai      # 或 deepseek
model: gpt-4         # 或 gpt-3.5-turbo
temperature: 0.7     # 降低以减少随机性
```

## 8. 常见问题

### Q: ModuleNotFoundError: No module named 'src'
**A:** 确保已运行 `pip install -e .`

### Q: OpenAI API错误
**A:** 检查.env文件中的API_KEY是否正确

### Q: 仿真一直不终止
**A:** 检查configs/sim.yaml中的max_time_s和max_messages设置

### Q: 想看更详细的日志
**A:** 在configs/experiments.yaml中设置 `logging.level: DEBUG`

## 9. 下一步

- 📖 阅读 [论文核心逻辑分析](论文核心逻辑分析.md) 理解实验原理
- 🏗️ 查看 [安全疫苗设计](安全疫苗设计.md) 了解系统架构
- 🎯 查看 [IMPLEMENTATION_COMPLETE](IMPLEMENTATION_COMPLETE.md) 了解已完成功能
- 🧪 运行多个seeds的实验对比结果

## 10. 获取帮助

如果遇到问题：
1. 检查 `outputs/runs/latest/events.jsonl` 中的错误信息
2. 运行测试：`python tests/test_basic.py`
3. 查看 [PROGRESS.md](PROGRESS.md) 了解项目状态

---

**祝实验顺利！🚀**
