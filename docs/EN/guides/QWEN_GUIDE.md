# 🚀 Guide to Running Experiments with Qwen

## ✅ Configuration Complete

Your Qwen API has been successfully configured and tested!

## 🎯 Running Experiments

### Method 1: Using Qwen Configuration File

```bash
# Single experiment
python scripts/run_one.py \
  --seed 42 \
  --defense NONE \
  --llm-config configs/llm_qwen.yaml

# Experiment with defense
python scripts/run_one.py \
  --seed 42 \
  --defense VAX_ACTIVE \
  --llm-config configs/llm_qwen.yaml
```

### Method 2: Directly Modify Default Configuration

Edit `configs/llm.yaml`:
```yaml
provider: qwen
model: qwen-plus
temperature: 0.7
max_tokens: 2000
```

Then run normally:
```bash
python scripts/run_one.py --seed 42 --defense NONE
```

### Method 3: Batch Experiments

Edit `configs/experiments.yaml` to ensure Qwen configuration is used:
```yaml
experiments:
  llm_config_file: configs/llm_qwen.yaml  # Add this line
  defense_strategies:
    - NONE
    - VAX_ACTIVE
  seeds: [42, 43, 44]
  task_file: data/tasks/lab_task_mof.json
```

Run batch experiments:
```bash
python scripts/run_batch.py
```

## 📊 Qwen Model Selection

| Model | Characteristics | Use Case |
|------|------|----------|
| `qwen-turbo` | Fast, economical | Simple tasks, quick testing |
| `qwen-plus` | Balanced performance and cost | **Recommended for this project** |
| `qwen-max` | Best performance | Complex reasoning tasks |
| `qwen-long` | Extra-long context | Handling large message histories |

## 🧪 Test API Connection

```bash
python scripts/test_qwen.py
```

## 💡 Common Questions

### Q: How to switch to other models?
A: Modify the `model` field in `configs/llm_qwen.yaml`

### Q: How to adjust generation parameters?
A: Modify the configuration file:
- `temperature`: Controls randomness (0-1)
- `max_tokens`: Maximum generation length
- `top_p`: Nucleus sampling parameter

### Q: What to do if encountering API errors?
A: Check:
1. Whether `QWEN_API_KEY` in `.env` file is correct
2. Whether network connection is normal
3. Whether API quota is sufficient

## 📝 Example: Complete Experiment Workflow

```bash
# 1. Test API
python scripts/test_qwen.py

# 2. Run single experiment
python scripts/run_one.py --seed 42 --defense NONE

# 3. View results
cat outputs/runs/latest/outcomes.json

# 4. Run batch comparison
python scripts/run_batch.py

# 5. View reports
cat outputs/batch/latest/reports/results.md
```

## 🎉 It's That Simple!

Now you can run all experiments using Qwen (通义千问). The system is fully configured, start exploring!
