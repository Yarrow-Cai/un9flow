# un9flow

> **Deterministic Embedded Intelligence**
>
> **我们不堆砌抽象，我们定义可证明的确定性。**

`un9flow` 是一个面向**嵌入式系统 / 电力电子 / BMS / 功能安全场景**的项目仓库。

当前阶段，它还是一个**方法论文档仓库**，用于沉淀哲学、约束、工作流与平台方向；**尚未发布可安装的 skills**。

## 项目定位

`un9flow` 聚焦于**确定性嵌入式工程**：

- 面向安全关键系统的设计与审查
- 强调静态资源模型、显式状态机与可验证时序
- 优先处理寄存器级实现、链路可观测性与 Failsafe 收敛
- 先把方法论写清楚，再把工具和 skills 做出来

一句话概括：

> **以确定性为第一约束，为安全关键系统建立可验证、可诊断、可收敛的工程秩序。**

## 三大核心约束

### 1. un-dynamic → 静态资源优先
- 默认禁止 `malloc` / `free`
- 优先静态分配、显式 section、固定内存布局
- 所有关键缓冲区、状态区和保留区都应可定位、可审计、可复盘

### 2. un-scheduled → 时间确定性优先
- 除非有充分理由，否则优先超级循环、时间片轮询或明确节拍机制
- ISR 必须保持短、快、可退出、不可阻塞
- 时序行为必须能够被解释、测量与验证

### 3. un-linked → 单向数据流优先
- 避免双向耦合、相互等待和隐式共享状态
- 关键状态机必须具备默认安全态与超时退路
- 异常处理必须能够收敛到 Failsafe，而不是悬空停留

## 当前仓库内容

当前仓库主要包含以下文档：

- `docs/PHILOSOPHY.md`：开发哲学
- `docs/WORKFLOW.md`：方法论工作流
- `docs/PLATFORMS.md`：目标平台与后续接入方向
- `docs/ROADMAP.md`：版本路线图
- `AGENTS.md`：仓库内协作约束

## 规划中的能力域

虽然当前还没有正式 skills，但规划中的能力域已经明确：

- `hazard-analysis`
- `deterministic-foundation`
- `link-diagnostics`
- `failsafe-validation`

这些名称当前用于表达未来的能力分层，并不表示仓库已经具备可直接安装的 skill 实现。

## 支持平台方向

未来版本计划面向以下平台生态：

- Claude Code
- OpenAI Codex CLI
- Cursor
- OpenCode
- Factory Droid
- Slate
- Kiro
- OpenClaw

当前阶段仍以文档定义为主，尚未提供自动安装器或平台分发能力。

详见：[`docs/PLATFORMS.md`](docs/PLATFORMS.md)

## 仓库结构

```text
un9flow/
├── README.md
├── .gitignore
├── AGENTS.md
└── docs/
    ├── PHILOSOPHY.md
    ├── WORKFLOW.md
    ├── PLATFORMS.md
    └── ROADMAP.md
```

## 当前阶段目标

当前阶段优先完成以下事情：

- 建立哲学与约束边界
- 建立工作流阶段定义
- 明确未来 skill 能力域命名
- 明确平台兼容方向
- 先形成稳定文档基线，再进入工具化与 skill 化

后续再逐步补齐：

- 正式 skill 文档
- 多 host 安装器
- 模板生成体系
- 专用 safety review / register audit 能力
- 失效模式与寄存器图谱生成工具

详见：[`docs/ROADMAP.md`](docs/ROADMAP.md)
