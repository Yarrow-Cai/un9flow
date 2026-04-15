# incident-investigation 工作流

## 目标
围绕 `incident-investigation` 形成首个可复用的 embedded 故障排查闭环：以证据驱动判断风险、定位路径、核对确定性结构，最终给出可复核的 review 输出。

## 五层结构（执行结构）
- Scenario 入口
- Orchestrator（执行拓扑中的调度角色）
- Phase 骨架
- Domain Specialist
- Artifact / Review 输出

说明：这里的“五层结构”是执行结构；命名纪律为四层（Scenario / Phase / Domain Specialist / Artifact），其中 Orchestrator 只是调度角色，不单独构成命名层。

## Scenario 入口
- 对外入口 skill（负责发起/整理/复核，不产出审计结论）：
  - `incident-investigation`
  - `evidence-pack`
  - `incident-review`

- Artifact 输出（可审计沉淀结果）：
  - `incident-summary`
  - `evidence-inventory`
  - `evidence-package`
  - `incident-diagnosis-pack`
  - `incident-review-memo`

- 证据流转说明：
  - `incident-investigation` 在 intake 阶段先产出 `evidence-inventory`，这是已知证据盘点清单（Artifact）。
  - 当盘点项杂乱或格式不统一时，由 `evidence-pack` 这个 Scenario 入口 skill 负责整理。
  - `evidence-pack` skill 的输出是 `evidence-package`，它是供 `incident-orchestrator` 直接消费的结构化证据包（Artifact）。

## Orchestrator
- `incident-orchestrator`
- 职责：
  - 接收 `incident-summary` 与标准化后的 `evidence-package`（结构化证据包），而非原始零散证据描述，建立 case 目标边界
  - 选择并编排 `hazard-analysis` / `deterministic-foundation` / `link-diagnostics` / `failsafe-validation` 的执行顺序
  - 分派对应 specialist 并记录证据缺口
  - 汇总中间结果，维护置信度与升级条件
  - 在 `Incident Review` 前完成结果聚合并输出下一步建议

## 第一批 specialist
- `signal-path-tracer`
- `register-state-auditor`
- `state-machine-tracer`
- `timing-watchdog-auditor`
- `failsafe-convergence-reviewer`

## incident 工作流链
```text
Incident Intake
  -> Hazard Framing
    -> Path Localization
      -> Deterministic Audit
        -> Convergence Check
          -> Incident Review
```

- 该链是 `incident-investigation` 的执行步骤，不替代或覆盖 un9flow 的 phase 命名（Phase 名来自 Orchestrator）。
- 映射关系（步骤名 -> phase）：
  - `Hazard Framing` 对应 `hazard-analysis`
  - `Path Localization` 主要落在 `link-diagnostics`
  - `Deterministic Audit` 对应 `deterministic-foundation`
  - `Convergence Check` 对应 `failsafe-validation`
  - `Incident Intake` 是 scenario intake，不单独作为 phase
  - `Incident Review` 是 review gate，不单独作为 phase

## 最低标准输出物
- `Scenario` 入口（`incident-investigation` / `evidence-pack` / `incident-review`）负责发起、整理与复核，不直接充当 Artifact 名称。
- `evidence-inventory` 为盘点清单；`evidence-package` 为由 `evidence-pack` skill 产出的结构化证据包，供 `incident-orchestrator` 消费。
- `incident-summary`
- `evidence-inventory`
- `evidence-package`
- `register-bitfield-map`
- `segmented-failure-path`
- `timeout-watchdog-risk-table`
- `incident-diagnosis-pack`
- `incident-review-memo`
- `failsafe-convergence-note`

## skill / agent 契约

- `incident-investigation`
  - 输入：故障现象、触发条件、影响范围、已知证据、风险认知、安全态状态
  - 输出：`incident-summary`、`evidence-inventory`、`missing-evidence-list`、`initial-risk-note`

- `evidence-pack`
  - 输入：杂乱证据、日志摘要、寄存器快照、波形描述、实验记录
  - 输出：`evidence-package`、`evidence-gap-note`

- `incident-orchestrator`
  - 输入：`incident-summary`、`evidence-package`、`initial-risk-note`
  - 输出：`phase-plan`、`specialist-dispatch-list`、`incident-diagnosis-pack`、`next-step-decision`

- `signal-path-tracer`
  - 输出：`segmented-failure-path`、`observability-point-list`、`path-suspicion-ranking`

- `register-state-auditor`
  - 输出：`register-bitfield-map`、`register-anomaly-list`、`config-mismatch-note`

- `state-machine-tracer`
  - 输出：`state-transition-chain`、`stuck-state-list`、`safety-state-gap-note`

- `timing-watchdog-auditor`
  - 输出：`timeout-watchdog-risk-table`、`isr-mainloop-conflict-note`、`timing-instability-hypothesis`

- `failsafe-convergence-reviewer`
  - 输出：`failsafe-convergence-note`、`unsafe-persistence-risk`、`convergence-expectation-check`

- `incident-review`
  - 输出：`incident-review-memo`、`confidence-gap-summary`、`recommended-next-action`

## 命名与分层规则

- `incident 工作流链`的执行步骤名和 un9flow `Phase` 名来自不同层级定义，不可互换。
- Scenario：用户任务入口，例如 `incident-investigation`
- Phase：方法论骨架，例如 `hazard-analysis`
- Domain Specialist：证据域与分析动作，例如 `register-state-auditor`
- Artifact：可审计输出物，例如 `register-bitfield-map`

- 规则
  - 不让 skill 伪装成 phase：`incident-investigation`、`evidence-pack`、`incident-review` 只承担输入/输出边界定义，不作为阶段名。
  - 不让 agent 命名成 artifact：`register-state-auditor`、`state-machine-tracer`、`signal-path-tracer` 作为执行角色（Domain Specialist），不作为沉淀物名称。
  - 不把 scenario 和 domain 混成一层：`incident-orchestrator` 负责编排路径，`register-state-auditor` 负责寄存器域审计，边界不可互换。