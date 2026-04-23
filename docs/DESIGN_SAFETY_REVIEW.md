# un9flow Design Safety Review

## 目标

把 `design-safety-review` 固定为可复用、可审查的主场景真源：在没有活跃 incident 压力时，围绕设计输入、状态机、安全边界、timeout / watchdog / failsafe 策略，形成一条可回放的功能安全复核主线。

## 场景定位

- 它是 `docs/ORCHESTRATION.md` 下三主场景之一，不是 incident 辅助 skill，也不是 specialist。
- 它继承 `docs/ORCHESTRATOR_PROMPT_CONTRACT.md` 的字段协议与控制信号，不重写总调度协议。
- 它复用 `docs/DOMAIN_SPECIALIST_CONTRACTS.md` 中已有的 `Domain Specialist` 契约与 `docs/templates/*-pack.md` 输出模板。
- `docs/WATCHDOG_TIMEOUT_AUDIT.md` 是它在 `failsafe-validation` 段下的专项方法真源。
- 对于 Keil Scatter / Linker Script 的静态内存布局审查，可优先使用 `docs/templates/keil-scatter-linker-review-template.md` 固定 memory region、section placement、deterministic invariants、evidence inputs 与升级规则。

## 进入边界与换轨

### 允许直进

- 当前无活跃 incident 压力，目标是审查风险边界、收敛路径、timeout / watchdog / failsafe 策略。
- 输入材料以设计说明、状态机、关键约束、保护策略、时序预算为主。

### 不该误进

- 当前主要问题是线上症状链、复现异常、链路掉线、CRC 错误或偶发 reset 的根因缩小。
- 当前任务仍处于首次 bring-up、稳定基线尚未建立的阶段。

### 升级 / 换轨条件

- 若设计复核中发现新的真实症状链、回归现象或失效扩散迹象，应回到 `incident-investigation`。
- 若发现问题本质是首次建链、首次采样、首次上电的稳定性缺口，应换轨到 `bringup-path`。
- 若 specialist 输出不足以支撑继续复核，应沿用 `fallback-for-more-evidence` 或 `fallback-reorder-specialists`，而不是跳过 review gate。

## 默认 Phase 骨架

1. `hazard-analysis`
2. `deterministic-foundation`
3. `failsafe-validation`
4. `link-diagnostics`（按需补）

## 默认 specialist 装配

### `hazard-analysis`

- `signal-path-tracer`
- `state-machine-tracer`

### `deterministic-foundation`

- `register-state-auditor`

### `failsafe-validation`

- `failsafe-convergence-reviewer`
- `timing-watchdog-auditor`

### `link-diagnostics`（按需补）

- `signal-path-tracer`

## 主 Artifact 与 specialist 输出对齐

### 主 Artifact

- `design-review-summary`
- `risk-boundary-note`
- `convergence-strategy-review`
- `failsafe-check-matrix`

### 对齐规则

- `risk-boundary-note` 应汇总 `segmented-failure-path`、`observability-point-list`、`state-transition-chain`、`safety-state-gap-note` 与 `register-anomaly-list` 中直接影响风险边界的结论。
- `convergence-strategy-review` 应汇总 `state-transition-chain`、`stuck-state-list`、`failsafe-convergence-note`、`unsafe-persistence-risk` 与 `convergence-expectation-check`，说明异常进入安全态的路径是否成立。
- `failsafe-check-matrix` 应吸收 `timeout-watchdog-risk-table`、`isr-mainloop-conflict-note`、`timing-instability-hypothesis` 与 `config-mismatch-note`，把触发条件、保护动作、终态、退出条件与证据缺口列成可复核矩阵。
- `design-review-summary` 只能在前三个主 Artifact 已具备 reviewable 结论后收口；若仍有关键证据缺口，必须显式保留 `unresolved_gaps`。

## Phase 执行重点

### `hazard-analysis`

- 先界定系统要防什么错下去，而不是先猜根因。
- 输出应明确风险边界、关键观察点与安全态预期。

### `deterministic-foundation`

- 固定关键状态、寄存器、时序前提与配置一致性。
- 若关键保护建立在不可观察或不可验证的配置前提上，必须直接记入 `risk-boundary-note`。

### `failsafe-validation`

- 核查 timeout / watchdog / reset / degrade / failover 是否形成可判定收敛链。
- `docs/WATCHDOG_TIMEOUT_AUDIT.md` 中的 timeout definition、timing baseline、watchdog feed path、blocking / starvation risk、reset chain、failsafe convergence 六项，应在这里作为专项展开。

### `link-diagnostics`（按需补）

- 只在通信链路、采样链路或控制链路本身构成安全前提时补充。
- 它用于补强设计边界，不替代 incident 排障。

## Review Gate

- 只有当 `risk-boundary-note`、`convergence-strategy-review` 与 `failsafe-check-matrix` 三者都已形成可复核结论时，才允许进入 `design-review-summary`。
- 若任何一项仍依赖未验证假设，应保守返回 `fallback-for-more-evidence`，或升级到更合适的主场景。

## 不负责什么

- 不替代活跃 incident 排障。
- 不替代首次 bring-up 路径。
- 不允许 specialist 直接冒充主场景结论。
- 不在证据不足时给出高置信安全背书。
