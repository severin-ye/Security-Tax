# 多智能体安全税论文

本目录包含论文的LaTeX源文件、生成脚本和相关文档。

## 📁 目录结构

```
论文/
├── README.md                    # 本文件
├── .gitignore                   # Git忽略规则
├── 论文初稿_中文.tex            # LaTeX源文件
│
├── figures/                     # 图片资源
│   ├── architecture.png         # 系统架构图 (256KB)
│   ├── security_tax.png         # 安全税散点图 (355KB)
│   └── behavior_distribution.png # 行为分布图 (300KB)
│
├── scripts/                     # 生成脚本
│   └── generate_figures.py     # 图表生成脚本
│
├── output/                      # 编译输出
│   ├── 论文初稿_中文.pdf        # 最终PDF (1.2MB, 9页)
│   └── build/                   # 编译中间文件
│       ├── *.aux
│       ├── *.log
│       └── *.out
│
├── docs/                        # 文档和报告
│   ├── COMPILATION_STATUS.md    # 编译状态报告
│   ├── 参考文献验证报告.md       # 文献验证记录
│   ├── 图表生成报告.md          # 图表生成说明
│   └── 论文撰写总结.md          # 撰写总结
│
└── references/                  # 参考资料
    └── requirements/            # 期刊投稿要求
        ├── 2025_最终论文样式(韩文).md
        ├── 2025_审查用_论文投稿样式(韩文).md
        ├── RAG 기반 시스템...hwp  # 参考论文样例
        └── 教授kakao消息.md
```

## 🚀 快速开始

### 编译论文

```bash
# 方法1: XeLaTeX（推荐）
cd /home/severin/Codelib/SKKU/论文
xelatex 论文初稿_中文.tex
xelatex 论文初稿_中文.tex  # 第二次解决交叉引用

# 方法2: 使用latexmk自动化
latexmk -xelatex -synctex=1 -interaction=nonstopmode 论文初稿_中文.tex

# 输出: output/论文初稿_中文.pdf
```

### 生成图表

```bash
cd /home/severin/Codelib/SKKU
source venv/bin/activate
python 论文/scripts/generate_figures.py
```

## 📋 系统要求

### LaTeX环境

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install texlive-xetex texlive-lang-chinese texlive-latex-extra latexmk

# 验证安装
xelatex --version
```

### Python环境（图表生成）

```bash
pip install matplotlib numpy
```

## 📊 论文内容

### 章节结构

| 章节 | 标题 | 内容概要 |
|------|------|---------|
| 1 | 引言 | 研究背景、动机、贡献 |
| 2 | 相关工作 | 多智能体系统、LLM安全、传播模型 |
| 3 | 系统架构 | 7智能体层级结构（Atlas→5研究员→Deng） |
| 4 | 防御机制 | 指令防御vs记忆疫苗（被动/主动模式） |
| 5 | 实验设计 | 攻击模型、评估指标、安全税定义 |
| 6 | 实验结果 | 鲁棒性(95%)、协作性(86.7%)、安全税(13.3%) |
| 7 | 讨论 | 发现总结、局限性、未来工作 |
| 8 | 结论 | 主要贡献与研究意义 |

### 核心数据

- **防御策略**: 5种（NONE, INSTR_PASSIVE/ACTIVE, VAX_PASSIVE/ACTIVE）
- **最优策略**: VAX_ACTIVE（95%鲁棒性 + 86.7%协作性）
- **安全税**: 13.3%（相比INSTR_ACTIVE降低60%）
- **实验规模**: 20次攻击测试 + 30条无害指令测试

### 图表说明

1. **图1 系统架构** - 展示7个智能体的消息流和攻击路径
2. **图2 安全税散点** - 5种策略的鲁棒性-协作性权衡
3. **图3 行为分布** - 智能体响应的5级分类统计

## 📝 投稿信息

### 目标期刊
- **期刊名**: 未来技术融合论文志（Journal of Advanced Technology Convergence）
- **出版方**: 韩国
- **级别**: SCOPUS索引

### 格式要求
- **页数**: 基本6页（当前9页需压缩）
- **纸张**: 188mm × 258mm
- **排版**: 双栏，20mm边距
- **摘要**: 中英文双语（各7-9行）
- **字体**: Times New Roman（英文）+ 中文字体
- **最终格式**: PDF或HWP

### 提交前检查清单
- [ ] 压缩至6页
- [x] 生成真实图表
- [x] 验证参考文献（19篇）
- [ ] 英文摘要润色
- [ ] 检查格式符合期刊要求
- [ ] 转换为HWP格式（如需要）

## 📚 参考文献

**总计**: 19篇（已全部验证真实性）

- arXiv预印本: 14篇
- 顶级期刊 (Nature, Science): 2篇  
- 物理学期刊 (PRL): 2篇
- 会议论文 (USENIX): 1篇

详见: [docs/参考文献验证报告.md](docs/参考文献验证报告.md)

## 🔧 维护与更新

### 清理编译产物

```bash
cd /home/severin/Codelib/SKKU/论文
rm -f output/build/*
latexmk -C 论文初稿_中文.tex
```

### 重新生成所有内容

```bash
# 1. 生成图表
python scripts/generate_figures.py

# 2. 编译论文
xelatex 论文初稿_中文.tex
xelatex 论文初稿_中文.tex

# 3. 检查输出
ls -lh output/论文初稿_中文.pdf
pdfinfo output/论文初稿_中文.pdf
```

## 📖 相关文档

- [编译状态报告](docs/COMPILATION_STATUS.md) - 详细的编译历史和问题解决
- [图表生成报告](docs/图表生成报告.md) - 图表数据来源和技术实现
- [参考文献验证](docs/参考文献验证报告.md) - 文献真实性验证记录
- [撰写总结](docs/论文撰写总结.md) - 论文撰写过程总结

## ⚠️ 注意事项

1. **中文支持**: 必须使用XeLaTeX编译，pdfLaTeX不支持中文
2. **图片路径**: 相对路径为`figures/`，移动文件后需更新LaTeX
3. **编译次数**: 至少编译2次以解决交叉引用
4. **版本控制**: 临时文件已加入.gitignore，仅提交源文件

---

**最后更新**: 2025-01-25  
**状态**: ✅ 可编译，图表完整，文献已验证
