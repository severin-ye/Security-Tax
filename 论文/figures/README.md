# 图表文件说明

本目录存放论文中引用的所有图表文件。

## 📊 需要的图表

### 1. architecture.png
**内容**：多智能体系统架构图
- 展示7个Agent的层次结构
- Atlas（项目经理）→ 5个研究员 → Deng（执行者）
- 标注消息队列和工具调用关系

**建议工具**：
- Draw.io
- Microsoft Visio
- Python + Graphviz

**参考**：项目文档 `/docs/CN/design/安全疫苗 业务逻辑图.html`

---

### 2. security_tax.png
**内容**：安全税权衡曲线图
- X轴：协作性（Cooperation）0-100%
- Y轴：鲁棒性（Robustness）0-100%
- 5个数据点：NONE, INSTR_PASSIVE, INSTR_ACTIVE, VAX_PASSIVE, VAX_ACTIVE
- 理想点：右上角（高鲁棒性+高协作性）

**数据**：
| 策略 | 鲁棒性 | 协作性 |
|------|--------|--------|
| NONE | 20 | 100 |
| INSTR_PASSIVE | 60 | 80 |
| INSTR_ACTIVE | 80 | 66.7 |
| VAX_PASSIVE | 75 | 90 |
| VAX_ACTIVE | 95 | 86.7 |

**生成代码示例**：
```python
import matplotlib.pyplot as plt

strategies = ['NONE', 'INSTR_PASSIVE', 'INSTR_ACTIVE', 'VAX_PASSIVE', 'VAX_ACTIVE']
robustness = [20, 60, 80, 75, 95]
cooperation = [100, 80, 66.7, 90, 86.7]

plt.figure(figsize=(8, 6))
plt.scatter(cooperation, robustness, s=100)
for i, txt in enumerate(strategies):
    plt.annotate(txt, (cooperation[i], robustness[i]))
plt.xlabel('Cooperation (%)')
plt.ylabel('Robustness (%)')
plt.title('Security Tax: Robustness vs Cooperation Trade-off')
plt.grid(True, alpha=0.3)
plt.savefig('security_tax.png', dpi=300, bbox_inches='tight')
```

---

### 3. behavior_distribution.png
**内容**：智能体行为等级分布柱状图
- X轴：5种防御策略
- Y轴：行为等级占比（-2到+2）
- 堆叠柱状图，不同颜色表示不同行为等级
  - 红色：+2（主动传播）
  - 橙色：+1（被动传播）
  - 灰色：0（中立）
  - 浅绿：-1（拒绝）
  - 深绿：-2（拒绝并通报）

**数据来源**：
运行可视化脚本生成：
```bash
python scripts/visualize_results.py --latest
```

---

## 🎨 设计规范

根据论文样式要求：

1. **图片清晰度**：最小300 DPI
2. **标题位置**：图片下方左对齐
3. **标题格式**：`Fig. 1. Title of figure`（英文）
4. **内容标记**：图中所有文字使用英文
5. **字体大小**：确保缩小后仍清晰可读
6. **颜色方案**：适合黑白打印（使用不同图案/线型）

## 📁 文件命名规范

- 使用英文小写，单词用下划线分隔
- PNG格式（推荐）或PDF格式
- 示例：`agent_architecture.png`, `robustness_comparison.png`

## 🛠️ 快速生成图表

### 使用项目已有的可视化工具

```bash
# 运行实验并生成可视化
cd /home/severin/Codelib/SKKU
python scripts/run_one.py --seed 42 --defense VAX_ACTIVE
python scripts/visualize_results.py --latest

# 生成的图表位置
ls outputs/runs/latest/visualizations/
# - summary.png（可用作补充材料）
# - timeline.png
# - agent_activity.png
```

### 从outputs目录提取数据

```bash
# 提取实验结果用于绘图
python -c "
import json
from pathlib import Path

# 读取outcomes.json
outcomes = json.load(open('outputs/runs/latest/outcomes.json'))
print('Robustness:', outcomes.get('robustness'))
print('Cooperation:', outcomes.get('cooperation'))
"
```

## ✅ 检查清单

在论文提交前，确保：

- [ ] 所有图片文件存在且可打开
- [ ] 图片分辨率≥300 DPI
- [ ] 图中文字全部为英文
- [ ] 标题格式符合规范（Fig. X. Title）
- [ ] LaTeX文件中的\includegraphics路径正确
- [ ] 图片在编译后的PDF中显示正常

## 💡 提示

如果没有时间制作复杂图表，可以：
1. 使用简单的表格代替
2. 暂时注释掉\includegraphics行
3. 使用文字描述替代可视化
