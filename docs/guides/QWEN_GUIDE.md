# 🚀 使用Qwen运行实验指南

## ✅ 配置已完成

你的Qwen API已成功配置并测试通过！

## 🎯 运行实验

### 方法1: 使用Qwen配置文件

```bash
# 单次实验
python scripts/run_one.py \
  --seed 42 \
  --defense NONE \
  --llm-config configs/llm_qwen.yaml

# 带防御的实验
python scripts/run_one.py \
  --seed 42 \
  --defense VAX_ACTIVE \
  --llm-config configs/llm_qwen.yaml
```

### 方法2: 直接修改默认配置

编辑 `configs/llm.yaml`:
```yaml
provider: qwen
model: qwen-plus
temperature: 0.7
max_tokens: 2000
```

然后正常运行：
```bash
python scripts/run_one.py --seed 42 --defense NONE
```

### 方法3: 批量实验

编辑 `configs/experiments.yaml`，确保使用Qwen配置：
```yaml
experiments:
  llm_config_file: configs/llm_qwen.yaml  # 添加这一行
  defense_strategies:
    - NONE
    - VAX_ACTIVE
  seeds: [42, 43, 44]
  task_file: data/tasks/lab_task_mof.json
```

运行批量实验：
```bash
python scripts/run_batch.py
```

## 📊 Qwen模型选择

| 模型 | 特点 | 适用场景 |
|------|------|----------|
| `qwen-turbo` | 快速、经济 | 简单任务、快速测试 |
| `qwen-plus` | 平衡性能和成本 | **推荐用于本项目** |
| `qwen-max` | 最强性能 | 复杂推理任务 |
| `qwen-long` | 超长上下文 | 需要处理大量历史消息 |

## 🧪 测试API连接

```bash
python scripts/test_qwen.py
```

## 💡 常见问题

### Q: 如何切换到其他模型？
A: 修改 `configs/llm_qwen.yaml` 中的 `model` 字段

### Q: 如何调整生成参数？
A: 修改配置文件中的：
- `temperature`: 控制随机性（0-1）
- `max_tokens`: 最大生成长度
- `top_p`: 核采样参数

### Q: 遇到API错误怎么办？
A: 检查：
1. `.env` 文件中的 `QWEN_API_KEY` 是否正确
2. 网络连接是否正常
3. API配额是否充足

## 📝 示例：完整实验流程

```bash
# 1. 测试API
python scripts/test_qwen.py

# 2. 运行单个实验
python scripts/run_one.py --seed 42 --defense NONE

# 3. 查看结果
cat outputs/runs/latest/outcomes.json

# 4. 运行批量对比
python scripts/run_batch.py

# 5. 查看报告
cat outputs/batch/latest/reports/results.md
```

## 🎉 就这么简单！

现在你可以使用Qwen（通义千问）运行所有实验了。系统已完全配置好，开始探索吧！
