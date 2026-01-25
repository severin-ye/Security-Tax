# 论文目录结构说明

## 📁 总体结构（方案1：按语言版本分离）

```
论文/
├── zh-CN/                    # 🇨🇳 中文版专属
│   ├── 论文初稿_中文.tex
│   └── output/
│       ├── 论文初稿_中文.pdf
│       └── build/           # 编译产物
│
├── ko-KR/                    # 🇰🇷 韩文版专属
│   ├── 论文初稿_韩文.tex
│   ├── output/
│   │   ├── 논문초고_한글.pdf
│   │   └── build/
│   └── tests/               # 测试文件
│
├── shared/                   # 🔗 共享资源
│   ├── figures/             # 图表（所有版本通用）
│   ├── scripts/             # 工具脚本
│   └── references/          # 参考文献
│
├── docs/                     # 📝 项目文档
│   ├── COMPILATION_STATUS.md
│   ├── 参考文献验证报告.md
│   └── ...
│
├── README.md                 # 项目说明
└── .gitignore
```

## 📋 各目录说明

### zh-CN/ - 中文版
- **论文初稿_中文.tex**: 中文版LaTeX源文件
- **output/**: 编译输出
  - `论文初稿_中文.pdf`: 最终PDF文件
  - `build/`: 编译过程产生的辅助文件(.aux, .log等)

### ko-KR/ - 韩文版
- **论文初稿_韩文.tex**: 韩文版LaTeX源文件（使用UnDinaru字体）
- **output/**: 编译输出
  - `논문초고_한글.pdf`: 最终PDF文件
  - `build/`: 编译辅助文件
- **tests/**: 测试版本和实验文件

### shared/ - 共享资源
- **figures/**: 所有版本通用的图表
  - `architecture.png`: 系统架构图
  - `security_tax.png`: 保安税分析图
  - `behavior_distribution.png`: 行为分布图
- **scripts/**: Python工具脚本
  - `generate_figures.py`: 图表生成脚本
  - `wrap_korean.py`: 韩文文本包裹工具
- **references/**: 参考文献和投稿要求文档

### docs/ - 项目文档
- 编译状态记录
- 参考文献验证报告
- 图表生成报告
- 投稿要求合规性检查
- 页数压缩修改记录
- 论文撰写总结

## 🚀 编译指南

### 中文版
```bash
cd zh-CN
xelatex -interaction=nonstopmode 论文初稿_中文.tex
xelatex -interaction=nonstopmode 论文初稿_中文.tex  # 第二次更新引用
```

### 韩文版
```bash
cd ko-KR
xelatex -interaction=nonstopmode 论文初稿_韩文.tex
xelatex -interaction=nonstopmode 论文初稿_韩文.tex
```

## 💡 设计理念

本结构采用**多语言并行架构**，优点：
- ✅ 语言版本清晰隔离，易于独立维护
- ✅ 每个版本可独立编译、发布
- ✅ 共享资源统一管理，避免重复
- ✅ 易于扩展（如添加英文版）
- ✅ 编译产物集中管理，不污染源码目录

## 📝 维护说明

1. **添加新图表**: 放入 `shared/figures/`，所有版本都可引用
2. **更新脚本**: 统一放在 `shared/scripts/`
3. **编译产物**: 自动生成在各语言版本的 `output/build/`
4. **文档更新**: 添加到 `docs/`，按主题分类
5. **版本管理**: 使用 `.gitignore` 排除编译产物

---

*最后更新: 2026-01-25*
