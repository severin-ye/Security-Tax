# 多智能体安全税论文 / Multi-Agent Security Tax Research

本项目包含学术论文的多语言版本（中文、韩文）及相关文档。

## 📁 目录结构

```
论文/
├── README.md                    # 项目说明（本文件）
├── STRUCTURE.md                 # 详细目录结构文档
├── .gitignore                   # Git忽略配置
│
├── shared/                      # 共享资源
│   ├── figures/                 # 图片资源（各语言版本共用）
│   │   ├── architecture.png         # 系统架构图 (256KB)
│   │   ├── security_tax.png         # 安全税散点图 (355KB)
│   │   └── behavior_distribution.png # 行为分布图 (300KB)
│   └── references/              # 参考资料
│       ├── requirements/        # 论文格式要求
│       │   ├── 2025_最终论文样式(韩文)..md
│       │   ├── 2025_审查用_论文投稿样式(韩文).md
│       │   ├── RAG 기반 시스템의 신뢰성과 Jailbreaking 보안 취약성 분석.hwp
│       │   └── 教授kakao消息.md
│       └── *.pdf                # 相关论文资料
│
├── zh-CN/                       # 中文版论文
│   ├── 论文初稿_中文.tex          # LaTeX源文件
│   └── output/                  # 编译输出
│       ├── 论文初稿_中文.pdf      # 最终PDF (7页)
│       └── build/               # 编译临时文件
│           ├── *.aux
│           ├── *.log
│           └── *.out
│
├── ko-KR/                       # 韩文版论文（投稿用）
│   ├── 韩文初稿.tex               # LaTeX源文件
│   └── output/                  # 编译输出
│       ├── 韩文初稿.pdf           # 最终PDF (7页, 1.1MB)
│       └── build/               # 编译临时文件
│           ├── *.aux
│           ├── *.log
│           └── *.out
│
└── docs/                        # 文档资料
    └── 目录结构.txt              # 原始目录记录
```

## 🚀 快速开始

### 编译韩文版（投稿版本）

```bash
cd ko-KR
xelatex -interaction=nonstopmode 韩文初稿.tex
xelatex -interaction=nonstopmode 韩文初稿.tex  # 第二遍解决引用

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
- **主办方**: 한국융합학회 (Korea Convergence Society)
- **语言**: 韩文/英文

### 韩文版提交前检查清单
- [ ] 所有表格和图片标题改为英文
- [ ] 添加首页期刊信息（Vol, ISSN, DOI）
- [ ] 添加通讯作者脚注（Corresponding Author）
- [ ] 页数压缩至6页（当前7页）
- [ ] 添加作者照片占位符（23×30mm）
- [x] 双栏排版
- [x] 韩文/英文摘要（各7-9行）
- [x] 主题词5-6个
- [x] 参考文献格式

### 中文版检查清单
- [x] 图表生成
- [x] 参考文献验证（19篇）
- [ ] 英文摘要润色
- [ ] 压缩至6页

## 📚 参考文献

**总计**: 19篇（已全部验证真实性）

- arXiv预印本: 14篇
- 顶级期刊 (Nature, Science): 2篇  
- 物理学期刊 (PRL): 2篇
- 会议论文 (USENIX): 1篇

详见论文参考文献部分。

## 🔧 维护与更新

### 清理编译产物

```bash
# 清理韩文版
cd ko-KR
rm -f output/build/*

# 清理中文版
cd ../zh-CN
rm -f output/build/*
```

### 重新编译

```bash
# 韩文版
cd ko-KR
xelatex -interaction=nonstopmode 韩文初稿.tex
xelatex -interaction=nonstopmode 韩文初稿.tex

# 中文版
cd ../zh-CN
xelatex -interaction=nonstopmode 论文初稿_中文.tex
xelatex -interaction=nonstopmode 论文初稿_中文.tex
```

## 📖 项目文档

详细文档位于 `docs/` 目录。

## ⚠️ 注意事项

1. **字体要求**: 
   - 韩文版：使用kotex包（Linux自动配置韩文字体）
   - 中文版：使用xeCJK包（需安装中文字体）
2. **编译器**: 必须使用XeLaTeX，pdfLaTeX不支持CJK字符
3. **图片路径**: 所有版本共用 `shared/figures/` 目录
4. **编译次数**: 至少2次以解决交叉引用
5. **文件编码**: 所有.tex文件使用UTF-8编码

## 🎯 下一步工作

### 韩文版（投稿优先）
1. 修改所有表格图片标题为英文
2. 添加首页期刊信息和通讯作者标注
3. 压缩页数至6页
4. 提交前最终格式检查

### 中文版（参考存档）
1. 内容已完整
2. 可选：同步韩文版修改

---

**最后更新**: 2026-01-25  
**韩文版状态**: ✅ 可编译 | ⚠️ 需格式调整  
**中文版状态**: ✅ 已完成
