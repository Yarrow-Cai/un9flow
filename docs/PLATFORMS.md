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

目前仓库已包含文档真源与正式 `SKILL.md` 入口，但仍不提供以下能力：

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

## 第一版接入优先级

第一版采用 **incident-first / gstack-compatible first** 策略，第一阶段仅对齐以下三点：

- workflow orchestration 思路
- Claude Code / skill 入口习惯
- 后续目录组织方式
- host 接入目标是同时对齐 `docs/ORCHESTRATION.md`（总调度）与场景文档（如 `docs/INCIDENT_WORKFLOW.md`），而非只绑定单一 scenario 文档

第一版不意味着：
- 复用 gstack 命名体系
- 复制人格化 specialist
- 现阶段直接继承 gstack 安装器
- 不承诺现阶段具备安装器、分发、目录映射或广泛 host 兼容能力
- 其中“目录映射”在当前语境下，特指多 host 目录生成与自动安装目录映射；Claude Code 的最小目录映射说明单独见 `docs/CLAUDE_CODE_HOST.md`

命名纪律：`Scenario / Phase / Domain Specialist / Artifact`

host 优先级：
1. Claude Code —— 首个 host 锚点与优先落地对象，其最小接入骨架、目录映射、当前可消费能力与非承诺边界详见 `docs/CLAUDE_CODE_HOST.md`
2. gstack 风格 skill 编排环境
3. OpenClaw 作为外层调度预留位
4. 其他 host 在核心 workflow 稳定后推进

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
