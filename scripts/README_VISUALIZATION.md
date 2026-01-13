# 🎨 可视化工具

本目录包含两个可视化脚本，用于展示多Agent系统的运行结果。

## 📊 静态图表 - visualize_results.py

生成PNG格式的统计图表。

**使用方法：**
```bash
python scripts/visualize_results.py --latest
```

**输出文件：**
- `summary.png` - 实验摘要（统计数据、结果、配置）
- `timeline.png` - 事件时间线
- `agent_activity.png` - Agent活动统计

**适用场景：**
- 快速查看实验概况
- 导出图片用于报告/论文
- 批量对比多个实验

---

## 🌐 交互式流程图 - visualize_flow.py ⭐

生成交互式HTML可视化，展示完整的系统运行流程。**支持中英文双语版本！**

**使用方法：**
```bash
# 生成中英文双语HTML
python scripts/visualize_flow.py --latest

# 自动生成两个文件:
# - flow_visualization.html (英文版，默认)
# - flow_visualization-CN.html (中文版)
```

**新功能亮点：**

### 🌍 双语支持
- **自动生成两个版本**：英文和中文
- **一键切换语言**：点击右上角语言按钮
- **完整翻译**：所有界面元素均已本地化

### 🖱️ 增强的交互功能
- **鼠标悬停显示详情**：
  - 节点：显示角色类型和名称
  - 连接线：显示发送者、接收者和消息数量
- **可拖拽网络图**：自由调整节点位置
- **缩放和平移**：探索大型网络
- **导航按钮**：快速缩放和居中

**功能特性：**

### 1️⃣ 消息网络图
- 🌐 可交互的Agent网络拓扑
- 🔴 攻击路径高亮显示
- 📊 消息流量可视化
- 🖱️ **鼠标悬停查看节点/连接详情** ⭐ 新增
- 🔍 支持缩放和拖拽
- 🧭 导航按钮辅助

### 2️⃣ 事件时间线
- ⏱️ 按时间顺序展示所有事件
- 🎯 攻击注入时刻标记
- 📍 关键节点高亮
- 🔍 可缩放查看细节

### 3️⃣ 事件详细日志
- 📋 完整的事件列表
- 🔍 每个事件的详细信息
- 🎨 颜色区分不同类型
- ⚠️ 攻击事件特殊标注

### 4️⃣ 流程分析
- 📈 事件统计图表
- 💬 消息流向分析
- ⚙️ 配置信息展示
- 📊 数据汇总

### 5️⃣ 语言切换 ⭐ 新增
- 🌍 支持中英文双语
- 🔄 一键切换（右上角按钮）
- 📝 完整本地化

**适用场景：**
- 深入理解系统运行过程
- 分析Agent交互模式
- 追踪攻击传播路径
- 演示和展示成果

---

## 🎯 使用示例

### 完整工作流

```bash
# 1. 运行实验
python scripts/run_one.py --seed 42 --defense VAX_ACTIVE

# 2. 生成静态图表
python scripts/visualize_results.py --latest

# 3. 生成交互式HTML
python scripts/visualize_flow.py --latest

# 4. 在浏览器中打开HTML文件
# Linux/Mac:
xdg-open outputs/runs/*/flow_visualization.html
# 或直接用浏览器打开文件
```

### 指定特定运行结果

```bash
# 可视化特定目录的结果
python scripts/visualize_flow.py --run-dir outputs/runs/20260113_222022_seed42

# 自定义输出路径
python scripts/visualize_flow.py --latest --output my_visualization.html
```

---

## 📸 预览

### 交互式HTML包含：

**顶部统计卡片**
- 总步数、消息数、Agent数量
- 运行时长
- 实验结果（成功/失败）

**标签页1：消息网络**
- Agent节点（蓝色）
- 系统节点（绿色）
- 攻击者节点（红色）
- 消息流向箭头

**标签页2：时间线**
- 横向时间轴
- 事件点标注
- 可缩放时间范围

**标签页3：事件日志**
- 时间戳
- 事件类型
- 详细描述
- 攻击事件高亮

**标签页4：流程分析**
- 事件类型统计
- 消息流向统计
- 配置信息

---

## 🔧 技术细节

### visualize_results.py
- **依赖**: matplotlib
- **输出格式**: PNG (300 DPI)
- **特点**: 轻量级、适合批处理

### visualize_flow.py
- **依赖**: 仅需Python标准库
- **输出格式**: 单个HTML文件
- **前端库**: vis-network, vis-timeline (CDN)
- **特点**: 无需安装额外依赖，可离线查看

---

## 💡 提示

1. **HTML文件是独立的**：可以直接分享给他人，在任何浏览器中打开
2. **支持所有现代浏览器**：Chrome、Firefox、Safari、Edge
3. **交互式探索**：拖拽、缩放、点击查看详情
4. **适合演示**：美观的渐变色设计，适合展示和汇报

---

## 🆘 故障排除

**Q: PNG图表无法生成？**
```bash
pip install matplotlib
```

**Q: HTML文件打不开？**
- 确保使用现代浏览器
- 检查文件路径中是否有特殊字符
- 尝试直接拖拽到浏览器窗口

**Q: 网络图显示不正常？**
- 等待几秒让物理引擎稳定
- 刷新页面重新加载
- 检查浏览器控制台是否有错误

---

<div align="center">

**🎨 享受可视化探索之旅！**

[返回主文档](../README.md) | [返回文档中心](../docs/README.md)

</div>
