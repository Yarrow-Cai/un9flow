# un9flow Domain Specialist Contracts

## 目标
为第一批 `Domain Specialist` 固定输入契约、输出 Artifact、禁止项与回交条件，让 specialist 层成为独立于 `Scenario / Skill / Artifact` 的稳定真源。

## 适用范围
- 当前覆盖第一批 5 个 specialist：
  - `signal-path-tracer`
  - `register-state-auditor`
  - `state-machine-tracer`
  - `timing-watchdog-auditor`
  - `failsafe-convergence-reviewer`
- 当前首先服务 `incident-investigation`，也可被 `bringup-path` 与 `design-safety-review` 在总调度规则下复用。
- 本文只定义 specialist 契约，不定义总路由规则，不替代场景工作流，也不展开 host-specific prompt 绑定。
- 总调度规则见 `docs/ORCHESTRATION.md`；prompt 字段协议见 `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`；incident pipeline 交接边界见 `docs/INCIDENT_WORKFLOW.md`。

## 统一契约规则
- specialist 只对自己的证据域与分析动作负责，不替代 scenario 入口、总调度或 review gate。
- specialist 的输入必须来自已归一化 case：至少包含 `incident-summary`、`evidence-package`、dispatch reason 与当前风险边界。
- specialist 的输出必须是明确 `Artifact`，不能只留一段不可复核的分析文字。
- specialist 输出必须显式说明：
  - 当前结论的置信度
  - 仍未解释的缺口或假设
  - 结论回链到哪些证据
  - 建议 orchestrator 下一步继续什么
- 若证据不足，specialist 必须输出缺口与保守判断，而不是越级给出高置信根因结论。
- specialist 名称只属于 `Domain Specialist` 层，不得冒充 `Scenario`、`Phase` 或 `Artifact`。

## 通用输入基线
- `incident-summary` 或当前场景摘要
- `evidence-package`
- `phase objective`
- `dispatch reason`
- `initial-risk-note` 或当前风险边界 / 安全态判断
- 与 specialist 证据域直接相关的原始证据或上游 Artifact

## 通用回交基线
- primary artifacts
- confidence
- unresolved gaps
- evidence backlinks
- next suggestion for orchestrator

## 第一批 Domain Specialist 契约

### `signal-path-tracer`

#### 默认落点 Phase
- `hazard-analysis`
- `link-diagnostics`
- `deterministic-foundation`（支撑定位）

#### 输入契约
- `incident-summary` 中的症状描述
- `evidence-package` 中与通信 / 采样 / 控制路径相关的证据
- 路径拓扑、器件分段、板级连接关系
- 波形观测点、链路状态、收发错误或掉线证据
- 当前风险边界与安全态假设

#### 输出 Artifact
- `segmented-failure-path`：按链路分段后的疑点路径
- `observability-point-list`：仍需补充的观测点、采样窗口或探针位置
- `path-suspicion-ranking`：按优先级排序的可疑路径段

#### 不负责什么
- 不替代寄存器配置审计
- 不替代状态迁移追踪
- 不直接给出最终根因定论
- 不修改 Scenario 路由、Phase 次序或 review 结论

#### 回交条件
- 已明确主要可疑路径段，或已明确下一轮必须补的观测点与链路证据

### `register-state-auditor`

#### 默认落点 Phase
- `deterministic-foundation`
- `hazard-analysis`（支撑配置风险判断）

#### 输入契约
- 寄存器快照
- 关键配置项与使能位
- 默认值 / 目标值 / 当前值
- 异常现象与保护触发背景
- 与寄存器行为直接相关的时序或复位证据

#### 输出 Artifact
- `register-bitfield-map`：关键寄存器位域与预期解释
- `register-anomaly-list`：异常位、冲突位或不合理状态清单
- `config-mismatch-note`：配置值与目标设计不一致的记录

#### 不负责什么
- 不替代路径分段定位
- 不替代完整状态机迁移分析
- 不把配置异常直接包装成最终根因结论
- 不越权定义新的保护策略

#### 回交条件
- 已明确寄存器层异常、配置偏移或当前快照无法解释的位域缺口

### `state-machine-tracer`

#### 默认落点 Phase
- `hazard-analysis`
- `deterministic-foundation`
- `failsafe-validation`（验证异常收敛路径）

#### 输入契约
- 状态定义与状态枚举
- 转移条件与保护分支
- 当前症状对应的状态表现
- 超时 / 退出条件
- 当前安全态、降级态与恢复条件说明

#### 输出 Artifact
- `state-transition-chain`：关键状态迁移链与证据对照
- `stuck-state-list`：疑似卡死、循环或无法退出的状态点
- `safety-state-gap-note`：状态机与安全态设计之间的缺口说明

#### 不负责什么
- 不替代寄存器位级审计
- 不替代 watchdog / timeout 时序分析
- 不直接裁定链路故障半径
- 不跳过 evidence gap 直接给出收敛结论

#### 回交条件
- 已明确异常状态迁移链，或已明确缺少哪些状态 / 退出条件证据

### `timing-watchdog-auditor`

#### 默认落点 Phase
- `failsafe-validation`
- `deterministic-foundation`

#### 输入契约
- 节拍信息
- ISR / main loop 责任划分
- timeout / watchdog 行为
- 复位 / 卡顿 / 偶发失效证据
- 与喂狗、超时、调度抖动相关的时序窗口

#### 输出 Artifact
- `timeout-watchdog-risk-table`：超时与 watchdog 风险项表
- `isr-mainloop-conflict-note`：ISR 与主循环职责冲突说明；该 Artifact 归属 `timing-watchdog-auditor`，不得拆成新的 specialist
- `timing-instability-hypothesis`：时序不稳定假设与验证入口

#### 不负责什么
- 不替代状态机语义审查
- 不替代寄存器配置真值判断
- 不直接给出系统级根因定论
- 不把单次 reset 现象直接包装成确定性结论

#### 回交条件
- 已明确 timeout / watchdog 风险路径，或已明确还缺哪些时序证据

### `failsafe-convergence-reviewer`

#### 默认落点 Phase
- `failsafe-validation`
- `hazard-analysis`（用于校验默认安全态假设）

#### 输入契约
- 当前故障链假设
- 当前安全态信息
- 降级 / 停机 / limp-home 行为
- 当前风险边界与不可突破约束
- 恢复条件、保持条件与收敛预期

#### 输出 Artifact
- `failsafe-convergence-note`：当前收敛路径是否成立的说明
- `unsafe-persistence-risk`：异常下继续运行的风险记录
- `convergence-expectation-check`：收敛预期与实际行为对照

#### 不负责什么
- 不替代前置 specialist 的证据采样与定位工作
- 不把安全审查意见包装成主路由裁决
- 不在证据不足时宣告系统“安全通过”
- 不替代 `design-safety-review`

#### 回交条件
- 已明确当前异常是否收敛到安全态，或已明确阻断收敛判断的缺口

## specialist 与 incident pipeline 的关系
- specialist 消费的是 orchestrator 交付的场景内调度上下文，不直接消费用户原始自由描述。
- specialist 产出的 Artifact 由 `incident-orchestrator` 汇总进入 `incident-diagnosis-pack`，并在 `incident-review` 阶段接受 second opinion。
- specialist 可以要求补证据，但不能自己冒充 `evidence-pack`。
- specialist 可以指出设计安全边界问题，但不能自己冒充 `design-safety-review`。
