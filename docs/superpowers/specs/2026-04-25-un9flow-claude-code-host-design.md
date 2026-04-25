# un9flow Claude Code host design

## 背景

当前仓库已经完成：

- 三场景总调度基线：`docs/ORCHESTRATION.md`
- 三个主场景真源：`docs/INCIDENT_WORKFLOW.md`、`docs/DESIGN_SAFETY_REVIEW.md`、`docs/BRINGUP_PATH.md`
- 正式 `skills/**/SKILL.md` 入口集合
- 模板生成体系与 generation regression 基线
- 平台方向说明：`docs/PLATFORMS.md`

但 host 接入仍主要停留在“平台方向与非承诺边界”的说明层。当前仓库虽然已经有正式 skill 入口、真源 docs、模板、案例与回归链路，但还没有一份专门面向 Claude Code 的最小接入真源文档，明确说明：Claude Code 到底直接消费什么、哪些目录只是规则支撑层、哪些能力已经可消费、当前明确不承诺什么。

## 目标

新增正式 host 接入真源：

- `docs/CLAUDE_CODE_HOST.md`

把 Claude Code 从“当前优先 host 的文档说明对象”推进为第一个拥有正式接入真源说明的 host。

## 非目标

本轮明确不做：

- 不设计自动安装器
- 不设计自动目录映射脚本
- 不设计一键分发流程
- 不承诺多 host 接入一致性
- 不把 `docs/**` 真源自动转化成宿主可执行对象
- 不设计 OpenClaw 或 multi-host 的统一安装抽象层

## 总体方案

采用“Claude Code first 的最小 host 接入真源”方案：

1. 新增 `docs/CLAUDE_CODE_HOST.md`
2. 用 Claude Code 视角重新解释仓库结构中的三层对象：
   - 直接消费层
   - 真源支撑层
   - 模板 / 案例 / 回归支撑层
3. 明确当前可消费能力与当前明确不承诺的边界
4. 让 `docs/PLATFORMS.md` 继续承担平台战略层，而不是承担 Claude Code 接入细节

## 文档分工

### `docs/PLATFORMS.md`

继续负责：

- 多 host 方向
- host 优先级
- 非承诺边界
- OpenClaw 预留位
- 为什么当前采用 Claude Code first

它是平台战略文档，而不是 Claude Code 的接入真源。

### `docs/SKILL_ARCHITECTURE.md`

继续负责：

- 总入口 / 三子入口 / 辅助 skill / Domain Specialist 的入口规范
- 哪一类 skill 可直接进入，哪一类必须受控进入

它是能力入口架构文档，而不是 host 接入文档。

### `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`

继续负责：

- 宿主与总调度之间的 prompt 输入 / 输出协议

它是调度协议文档，而不是 host 接入骨架说明。

### `skills/**/SKILL.md`

继续负责：

- Claude Code 最终直接消费的正式 skill 入口对象

它们是宿主最终读取对象，但不承担“解释整个 host 如何接入仓库”的职责。

### `docs/CLAUDE_CODE_HOST.md`

新增后只负责：

- Claude Code 如何消费本仓库
- Claude Code 视角下的目录映射
- Claude Code 的最小接入步骤
- 当前可消费能力清单
- 当前明确不承诺的边界
- 与 `docs/PLATFORMS.md`、`docs/SKILL_ARCHITECTURE.md`、`docs/ORCHESTRATOR_PROMPT_CONTRACT.md` 的关系

## Claude Code 视角下的目录映射

### 1. 直接消费层

- `skills/**/SKILL.md`

这是 Claude Code 的正式直接消费入口层。

`docs/CLAUDE_CODE_HOST.md` 应明确：

- Claude Code 直接消费的正式能力入口，以 `skills/**/SKILL.md` 为准
- 当前首批正式入口包括：
  - `skills/orchestration/SKILL.md`
  - `skills/incident-investigation/SKILL.md`
  - `skills/bringup-path/SKILL.md`
  - `skills/design-safety-review/SKILL.md`
  - `skills/evidence-pack/SKILL.md`
  - `skills/incident-review/SKILL.md`
  - 五个 `Domain Specialist`
  - `skills/watchdog-timeout-audit/SKILL.md`

### 2. 真源支撑层

- `docs/ORCHESTRATION.md`
- `docs/INCIDENT_WORKFLOW.md`
- `docs/DESIGN_SAFETY_REVIEW.md`
- `docs/BRINGUP_PATH.md`
- `docs/DOMAIN_SPECIALIST_CONTRACTS.md`
- `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`
- `docs/SKILL_ARCHITECTURE.md`
- `docs/TEMPLATE_GENERATION.md`
- `docs/CONSISTENCY_VALIDATION.md`

这层不是 Claude Code 直接把它们当成 skill 入口来消费，但它们是 skill 解释、宿主接入说明与验证边界的真源支撑层。

### 3. 模板 / 案例 / 回归支撑层

- `docs/templates/**`
- `docs/cases/**`
- `docs/golden-inputs/**`
- `docs/golden-outputs/**`
- `tools/run_generation_regression.py`

这层用于支撑：

- 模板承载
- 示例演示
- 输出回归验证

它们不应被解释为 Claude Code 的直接入口层。

## `docs/CLAUDE_CODE_HOST.md` 建议章节结构

建议至少固定以下章节：

1. `## 目标`
2. `## 宿主定位`
3. `## 目录映射`
4. `## 最小接入步骤`
5. `## 当前可消费能力`
6. `## 当前明确不承诺`
7. `## 与其他文档的关系`

## 宿主定位

`docs/CLAUDE_CODE_HOST.md` 应明确：

- Claude Code 是当前仓库首个 host 接入锚点
- 该文档只说明 Claude Code 维度下的最小接入骨架
- 它不代表多 host 接入已经完成
- 它也不代表当前仓库已经具备官方发行包、自动安装器或自动映射能力

## 最小接入步骤

建议只写到“骨架可消费”，不写成安装器说明。

最小接入步骤至少包括：

1. 准备仓库内容
   - 正式 skill 入口位于 `skills/**/SKILL.md`
   - docs 真源、模板、案例目录与回归链路保持仓库原状

2. 确定宿主直接消费对象
   - Claude Code 直接消费正式 `SKILL.md`
   - 其他 docs 文档作为规则支撑层，不作为宿主直接入口

3. 选择入口方式
   - 优先从：
     - `orchestration`
     - 三个主场景 skill
     开始消费
   - 辅助 skill 与 `Domain Specialist` 不作为全局首入口

4. 按现有文档边界运行
   - 总入口规则遵循 `docs/ORCHESTRATION.md`
   - 入口规范遵循 `docs/SKILL_ARCHITECTURE.md`
   - prompt 协议遵循 `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`

5. 需要验证时使用现有校验链路
   - `tools/validate_consistency.py`
   - `tools/run_generation_regression.py --check`

## 当前可消费能力

建议把“当前可消费能力”定义为：仓库内已经存在正式 `skills/**/SKILL.md` 的对象。

应明确列出：

- 总入口：
  - `orchestration`
- 主场景入口：
  - `incident-investigation`
  - `bringup-path`
  - `design-safety-review`
- 辅助 skill：
  - `evidence-pack`
  - `incident-review`
- `Domain Specialist`：
  - `signal-path-tracer`
  - `register-state-auditor`
  - `state-machine-tracer`
  - `timing-watchdog-auditor`
  - `failsafe-convergence-reviewer`
- formal embedded 专项：
  - `watchdog-timeout-audit`

## 当前明确不承诺

这一段应明确且偏硬边界，至少包括：

- 不提供自动安装器
- 不提供自动目录映射脚本
- 不提供一键分发
- 不承诺多 host 接入一致性
- 不承诺当前仓库已是 Claude Code 官方可发布发行包
- `docs/**` 真源不会自动转化为宿主可执行入口，仍以正式 `skills/**/SKILL.md` 为直接消费入口

## 与其他文档的关系

`docs/CLAUDE_CODE_HOST.md` 应明确回指：

- `docs/PLATFORMS.md`
- `docs/SKILL_ARCHITECTURE.md`
- `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`

并说明：

- 平台战略问题回 `docs/PLATFORMS.md`
- skill 入口边界问题回 `docs/SKILL_ARCHITECTURE.md`
- 调度协议与 prompt 字段问题回 `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`
- Claude Code 如何消费这些对象的问题由 `docs/CLAUDE_CODE_HOST.md` 负责说明

## 建议的后续实施范围

若基于本设计推进实现，建议最小触达这些文件：

- 新增：`docs/CLAUDE_CODE_HOST.md`
- 修改：`docs/PLATFORMS.md`
- 修改：`README.md`
- 视需要修改：`docs/CONSISTENCY_VALIDATION.md`

但本设计本身不要求同步实现自动安装器、目录生成器或 distribution pipeline。

## 验收标准

当以下条件同时满足时，可认为 Claude Code host 接入骨架基线完成：

- 仓库存在 `docs/CLAUDE_CODE_HOST.md`
- 文档中明确区分直接消费层、真源支撑层与模板 / 案例 / 回归支撑层
- 文档中明确 Claude Code 直接消费以 `skills/**/SKILL.md` 为准
- 文档中列出当前可消费能力清单
- 文档中列出当前明确不承诺的边界
- 文档中与 `docs/PLATFORMS.md`、`docs/SKILL_ARCHITECTURE.md`、`docs/ORCHESTRATOR_PROMPT_CONTRACT.md` 的关系被说明清楚
- `README.md` 或平台入口文档已能把 Claude Code host 接入真源暴露为可发现入口
