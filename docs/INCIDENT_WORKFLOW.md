# incident-investigation 工作流

## 目标
围绕 `incident-investigation` 形成首个可复用的 embedded 故障排查闭环：以证据驱动判断风险、定位路径、核对确定性结构，最终给出可复核的 review 输出。

说明：三场景共用的 orchestrator 总调度规则统一见 `docs/ORCHESTRATION.md`，incident 文档仅保留 incident 场景专属内容。
在该文档中，不重复定义 `Scenario / Phase / Domain Specialist / Artifact` 的总规则，只说明 incident 内的落地方式。

## incident 场景内调度器边界
- 总调度外壳在 `docs/ORCHESTRATION.md` 先决定主场景、全局路由和控制信号。
- `incident-orchestrator` 是 `incident-investigation` 的**场景内调度器**，在主场景已确认后承担：
  - phase 排序与可重排
  - specialist 分派
  - artifact 汇总与缺口跟踪
  - review gate 前的结果收口与下一步建议

## incident 场景主入口与辅助 skill
- 对外 skill 入口（负责发起/整理/复核，不产出审计结论）：
  - 主场景入口：`incident-investigation`
  - 辅助 skill：`evidence-pack`、`incident-review`

- Artifact 输出（可审计沉淀结果）：
  - `incident-summary`
  - `evidence-inventory`
  - `evidence-package`
  - `incident-diagnosis-pack`
  - `incident-review-memo`

- 证据流转说明：
  - `incident-investigation` 在 intake 阶段先产出 `evidence-inventory`，这是已知证据盘点清单（Artifact）。
  - 当盘点项杂乱或格式不统一时，由辅助 skill `evidence-pack` 负责整理。
  - `evidence-pack` 的输出是 `evidence-package`，它是供 `incident-orchestrator` 直接消费的结构化证据包（Artifact）。

## Orchestrator（场景内）
- `incident-orchestrator`
- 职责：
  - 接收 `incident-summary` 与标准化后的 `evidence-package`（结构化证据包），建立 case 目标边界
  - 按已由总调度外壳确认的场景目标执行 `hazard-analysis` / `deterministic-foundation` / `link-diagnostics` / `failsafe-validation` 的 phase 排序与重排
  - 调用对应 specialist 并记录证据缺口
  - 汇总场景内中间结果，维护置信度与升级条件
  - `Incident Review` 前完成结果聚合并给出收口建议

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
- incident 场景内的 skill 入口（`incident-investigation` / `evidence-pack` / `incident-review`）负责发起、整理与复核，不直接充当 Artifact 名称。
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
  - 其中 `next-step-decision` 应映射到总调度控制信号集合（见 `docs/ORCHESTRATION.md`）

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

## 命名与分层约束（继承总则）

- 该文档不重复展开共性约束：`Scenario / Phase / Domain Specialist / Artifact` 的详细定义与总命名纪律，沿用 `docs/ORCHESTRATION.md`。
- 在 incident 场景内保留最小边界：`incident-investigation`、`evidence-pack`、`incident-review` 仅作为场景内 skill / 输入输出入口，不作为全局主路由对象；`register-state-auditor`、`state-machine-tracer`、`signal-path-tracer` 仅作为 Domain Specialist。