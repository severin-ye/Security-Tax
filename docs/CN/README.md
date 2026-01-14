# 📚 文档中心

[EN](../../README.md) | **CN**

欢迎使用多智能体安全税系统文档！本文档提供完整的项目指南和参考资料。

## 📖 快速导航

### 🚀 入门指南

- **[快速开始](guides/QUICKSTART.md)** - 30秒上手，完整使用教程
- **[Qwen集成指南](guides/QWEN_GUIDE.md)** - 通义千问模型使用指南

### 🎨 设计文档

- **[论文核心逻辑分析](design/论文核心逻辑分析.md)** - 理论基础与核心概念
- **[安全疫苗设计](design/安全疫苗设计.md)** - 防御机制详细说明
- **[实现计划](design/实现计划.md)** - 项目实现路线图

### 📚 参考资料

- **[项目完成报告](references/PROJECT_COMPLETE.md)** - 功能清单与完成状态
- **[实现完成总结](references/IMPLEMENTATION_COMPLETE.md)** - 实现细节总结
- **[完成总结](references/COMPLETION_SUMMARY.md)** - 项目里程碑
- **[进度跟踪](references/PROGRESS.md)** - 开发进度记录

### 📖 教程

- **[LangChain 1.0 教程](tutorials/langchain%201.0教程.md)** - LangChain 1.0 框架使用指南

## 🎯 核心功能一览

| 模块 | 功能 | 文档链接 |
|------|------|---------|
| **多智能体系统** | 7个协作Agent（Atlas + 5研究员 + Deng） | [论文分析](design/论文核心逻辑分析.md) |
| **攻击注入** | 12种越狱提示词，智能注入策略 | [快速开始](guides/QUICKSTART.md) |
| **防御机制** | 指令防御 + 疫苗防御（被动/主动） | [疫苗设计](design/安全疫苗设计.md) |
| **评估系统** | 鲁棒性、合作性、传播分析 | [项目完成](references/PROJECT_COMPLETE.md) |
| **可视化** | PNG图表 + 交互式HTML流程图 | [快速开始](guides/QUICKSTART.md) |

## 📂 文档结构

```
docs/CN/
├── README.md                    # 本文件 - 文档导航
├── guides/                      # 使用指南
│   ├── QUICKSTART.md           # 快速开始教程
│   └── QWEN_GUIDE.md           # Qwen集成指南
├── design/                      # 设计文档
│   ├── 论文核心逻辑分析.md      # 理论基础
│   ├── 安全疫苗设计.md          # 防御机制设计
│   └── 实现计划.md             # 实现路线图
├── references/                  # 参考资料
│   ├── PROJECT_COMPLETE.md     # 功能完成清单
│   ├── IMPLEMENTATION_COMPLETE.md
│   ├── COMPLETION_SUMMARY.md
│   └── PROGRESS.md
└── tutorials/                   # 教程
    └── langchain 1.0教程.md
```

## 🔗 相关链接

- **[返回主README](../../README.md)** - 项目主页（English）
- **[源代码](../../src/)** - 源码目录
- **[配置文件](../../configs/)** - 配置文件
- **[实验脚本](../../scripts/)** - 运行脚本

## 💡 使用建议

1. **新手入门**: 从 [快速开始](guides/QUICKSTART.md) 开始
2. **理解原理**: 阅读 [论文核心逻辑分析](design/论文核心逻辑分析.md)
3. **深入研究**: 查看 [安全疫苗设计](design/安全疫苗设计.md) 和源代码
4. **使用 Qwen**: 参考 [Qwen指南](guides/QWEN_GUIDE.md)
5. **查看进度**: 浏览 [项目完成报告](references/PROJECT_COMPLETE.md)

---

**最后更新**: 2026-01-14 | **文档版本**: v1.0
