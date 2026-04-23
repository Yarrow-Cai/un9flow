# un9flow

> **Deterministic Embedded Intelligence**
>
> **我们不堆砌抽象，我们定义可证明的确定性。**

`un9flow` 是一个面向**嵌入式系统 / 电力电子 / BMS / 功能安全场景**的项目仓库。

当前阶段，它以**文档真源 + 正式 skill 入口文件 + 一致性校验基线**为主：已经落地第一批正式 `SKILL.md`、incident / orchestrator / consistency / watchdog 相关模板与方法基线，以及本地 `consistency validation` CLI 与 GitHub workflow；但**尚未进入可安装分发阶段**。

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

当前仓库主要包含以下文档与目录：

- `docs/PHILOSOPHY.md`：开发哲学
- `docs/WORKFLOW.md`：方法论工作流
- `docs/INCIDENT_WORKFLOW.md`：incident-first 故障排查工作流基线
- `docs/DESIGN_SAFETY_REVIEW.md`：design-safety-review 主场景真源，固定功能安全复核的 phase / specialist / artifact 对齐关系
- `docs/ORCHESTRATION.md`：三场景并列的 orchestrator 总调度规则；负责总调度规则，`docs/INCIDENT_WORKFLOW.md` 负责 incident 场景专属闭环。
- `docs/DOMAIN_SPECIALIST_CONTRACTS.md`：5 个 `Domain Specialist` 的输入 / 输出契约、禁止项与回交条件真源
- `docs/SKILL_ARCHITECTURE.md`：总入口、三子入口与辅助 skill 的结构关系与边界基线；作为 skill **入口规范**（`SKILL.md` 前置基线）。
- `docs/WATCHDOG_TIMEOUT_AUDIT.md`：`design-safety-review` 下的 watchdog / timeout 专项审计方法真源
- `docs/REGISTER_STATE_AUDIT.md`：`register-state-auditor` 的寄存器审计方法真源，固定默认值 / 目标值 / 当前值 / 复位后值、位语义与复位返回风险的复核方式
- `docs/templates/watchdog-timeout-audit-checklist.md`：watchdog / timeout 专项审计检查清单模板（轻量检查导向，承接方法真源）
- `skills/watchdog-timeout-audit/SKILL.md`：watchdog / timeout 正式专项 skill 入口（非主场景、非 Domain Specialist）
- `docs/templates/watchdog-timeout-audit-findings.md`：watchdog / timeout 轻量 findings 模板
- `skills/`：首批正式 skill 文件目录（含 `skills/orchestration/SKILL.md` 总入口、主场景 / 辅助入口 skill，以及 5 个 `Domain Specialist` skill），用于承接路由、场景执行与产物补齐。
- `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`：un9flow orchestrator 与 scenario prompt 的输入输出与控制信号约束，定义统一**调度协议**。
- `docs/CONSISTENCY_VALIDATION.md`：docs / skills / templates / cases / 过程文档的统一一致性校验总文档
- `tools/validate_consistency.py`：当前本地一致性校验 CLI
- `tools/generate_incident_case_bundle.py`：基于现有模板生成 incident workflow 主线文档 bundle 的脚本
- `.github/workflows/consistency-validation.yml`：当前一致性校验 CLI 的 PR / main 门禁 workflow
- `docs/PLATFORMS.md`：目标平台与后续接入方向
- `docs/ROADMAP.md`：版本路线图
- `docs/cases/`：incident workflow 回归样本（入口路由与 dispatch 期望基线）
- `docs/templates/`：incident / orchestrator / consistency / specialist 输出模板（incident summary、evidence package、diagnosis pack、review memo；orchestrator-routing-matrix、orchestrator-dispatch-plan、prompt-contract-checklist、skill-boundary-checklist、skill-routing-matrix、consistency-review-checklist、validation-findings，以及 5 个 `*-pack.md` specialist 输出模板）
- `AGENTS.md`：仓库内协作约束

## 规划中的能力域

当前阶段虽然有第一批正式 skill 文档，整体仍以文档基线为主；规划中的能力域已经明确：

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
├── .github/
│   └── workflows/
│       └── consistency-validation.yml
├── docs/
│   ├── PHILOSOPHY.md
│   ├── WORKFLOW.md
│   ├── INCIDENT_WORKFLOW.md
│   ├── DESIGN_SAFETY_REVIEW.md
│   ├── ORCHESTRATION.md
│   ├── DOMAIN_SPECIALIST_CONTRACTS.md
│   ├── PLATFORMS.md
│   ├── ROADMAP.md
│   ├── SKILL_ARCHITECTURE.md
│   ├── ORCHESTRATOR_PROMPT_CONTRACT.md
│   ├── CONSISTENCY_VALIDATION.md
│   ├── WATCHDOG_TIMEOUT_AUDIT.md
│   ├── cases/
│   │   ├── incident-workflow-routing-regression.md
│   │   └── incident-workflow-dispatch-regression.md
│   ├── templates/
│   │   ├── watchdog-timeout-audit-checklist.md
│   │   ├── incident-summary.md
│   │   ├── evidence-package.md
│   │   ├── incident-diagnosis-pack.md
│   │   ├── incident-review-memo.md
│   │   ├── signal-path-trace-pack.md
│   │   ├── register-state-audit-pack.md
│   │   ├── state-machine-trace-pack.md
│   │   ├── timing-watchdog-audit-pack.md
│   │   ├── failsafe-convergence-review-pack.md
│   │   ├── orchestrator-routing-matrix.md
│   │   ├── orchestrator-dispatch-plan.md
│   │   ├── prompt-contract-checklist.md
│   │   ├── skill-boundary-checklist.md
│   │   ├── skill-routing-matrix.md
│   │   ├── consistency-review-checklist.md
│   │   └── validation-findings.md
│   └── superpowers/
│       ├── specs/
│       └── plans/
├── tools/
│   ├── validate_consistency.py
│   └── generate_incident_case_bundle.py
└── skills/
    ├── orchestration/
    │   └── SKILL.md
    ├── incident-investigation/
    │   └── SKILL.md
    ├── design-safety-review/
    │   └── SKILL.md
    ├── bringup-path/
    │   └── SKILL.md
    ├── evidence-pack/
    │   └── SKILL.md
    ├── incident-review/
    │   └── SKILL.md
    ├── signal-path-tracer/
    │   └── SKILL.md
    ├── register-state-auditor/
    │   └── SKILL.md
    ├── state-machine-tracer/
    │   └── SKILL.md
    ├── timing-watchdog-auditor/
    │   └── SKILL.md
    └── failsafe-convergence-reviewer/
        └── SKILL.md
```

## 当前完成情况

### 已完成

- 已建立 README、哲学、工作流、平台、路线图、orchestration、prompt contract、skill architecture 等文档基线
- 已落地首批正式 `skills/` 入口文件（总入口 + 主场景 / 辅助入口）
- 已落地 5 个 `Domain Specialist` 正式 skill 文件，与 `docs/DOMAIN_SPECIALIST_CONTRACTS.md` 保持一一映射
- 已补齐第一批 incident / orchestrator / consistency / watchdog 相关模板与方法真源
- 已落地 `docs/cases/incident-workflow-routing-regression.md` 与 `docs/cases/incident-workflow-dispatch-regression.md`，作为 incident workflow 示例任务回归基线
- 已落地 5 个 `Domain Specialist` 输出模板（`docs/templates/*-pack.md`），承接 specialist Artifact、置信度、缺口与回交建议
- 仓库当前已包含本地 `consistency validation` CLI（`tools/validate_consistency.py`）与最小 GitHub workflow 门禁（`.github/workflows/consistency-validation.yml`）
- 已落地 `tools/generate_incident_case_bundle.py`，可基于现有模板生成 incident workflow 主线文档 bundle
- 已落地 `docs/WATCHDOG_TIMEOUT_AUDIT.md` 与 `docs/templates/watchdog-timeout-audit-checklist.md`，作为 watchdog / timeout 专项方法与 checklist 基线
- 已固化 `docs/DOMAIN_SPECIALIST_CONTRACTS.md` 与 `docs/INCIDENT_WORKFLOW.md` 中的第一批 `Domain Specialist` 契约及 incident pipeline 输入输出边界
- 已在 `docs/PLATFORMS.md` 固化第一阶段 host 对齐边界、`gstack-compatible first` 非承诺项与 `OpenClaw` 预留位
- 已落地 `docs/DESIGN_SAFETY_REVIEW.md`，把 design-time safety review 的 phase / specialist / Artifact 对齐固定为主场景真源

### 进行中

- 继续从文档真源推进到 incident pipeline 的完整 skill 化
- 继续把文档生成脚本与更完整回归校验补齐
- 继续收敛 orchestration 边界、场景职责与校验规则之间的一致性

### 规划中

- host 安装与分发能力
- 多 host 接入 / 安装器
- 模板生成体系与更完整的回归校验
- 专用 safety review / register audit 能力扩展
- 失效模式与寄存器图谱生成工具
- 示例与实战案例

## 当前阶段重点

当前阶段重点不是扩大发布面，而是继续把以下基线钉稳：

- 稳定 incident-first 与 orchestration 的文档真源
- 把正式 `SKILL.md` 入口、模板与一致性校验继续对齐
- 在不夸大 host 兼容与安装能力的前提下，逐步推进 tool 化与 skill 化
- 先把方法边界、命名纪律、调度协议和 reviewable artifacts 讲清、定稳、再继续向外扩展

## 演进顺序

- v1：incident-first 规格定义
- v2：incident pipeline skill 化
- v3：host 接入
- v4：模板生成与一致性校验
- v5：嵌入式专用能力外扩

当前优先级不是多 host 分发，而是先把第一条 incident workflow 讲清、定稳、再技能化。

详见：[`docs/ROADMAP.md`](docs/ROADMAP.md)
