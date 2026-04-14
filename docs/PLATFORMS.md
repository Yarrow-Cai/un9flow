# un9flow 支持平台与使用方式

`un9flow` 当前仍处于**文档基线阶段**。

这意味着：

- 已有哲学、工作流、平台方向与路线图文档
- 尚未发布可安装的正式 skills
- 尚未提供自动安装器、模板生成器或多 host setup 脚本

## 目标平台

未来计划面向以下 AI coding agent 平台：

- Claude Code
- OpenAI Codex CLI
- Cursor
- OpenCode
- Factory Droid
- Slate
- Kiro
- OpenClaw（作为调度或外层代理）

## 当前状态

目前仓库中只有方法论文档，不提供以下能力：

- 可直接安装的 slash skill
- 自动创建 skill 目录映射
- 多平台分发脚本
- 自动发现与安装流程

## 规划中的能力域

以下名称是**未来计划中的能力域**，当前仍是概念层定义：

- `hazard-analysis`
- `deterministic-foundation`
- `link-diagnostics`
- `failsafe-validation`

## 后续接入方向

当项目进入工具化阶段后，预计会按以下方向接入目标平台：

### Claude Code
- 将能力域拆分为独立 skill 入口
- 支持短名 / 前缀名策略
- 通过标准 skills 目录接入

### Codex CLI / Cursor / OpenCode / Factory / Slate / Kiro
- 采用与目标平台兼容的目录映射方式
- 保持 Markdown-first 的文档组织
- 逐步补齐平台特定安装流程

### OpenClaw
- 作为外层调度入口
- 按任务类型路由到未来的专业能力域

## 项目特点

- 先建立工程哲学，再做工具实现
- 先定义约束边界，再做交互包装
- 先稳定文档语义，再进入技能化和自动化
- 重点覆盖 bring-up、寄存器级约束、链路诊断和功能安全

## 后续计划

后续版本会逐步补齐：

- 正式 skills
- `setup` 脚本
- 多 host 目录生成
- 文档模板化生成
- 嵌入式专用 review / audit 能力
- 示例工程与 checklist 模板
