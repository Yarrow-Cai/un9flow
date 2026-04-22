# incident-workflow-dispatch-regression

- 角色说明：本文件在统一校验体系中作为 incident workflow 的 dispatch 回归基线，用于验证 phase、specialist、Artifact 与 control signal 的组合是否仍然闭环。
- 规则来源：`docs/INCIDENT_WORKFLOW.md`、`docs/ORCHESTRATION.md`、`docs/DOMAIN_SPECIALIST_CONTRACTS.md`

## regression case

### `INC-DISPATCH-001`
- `case id`: `INC-DISPATCH-001`
- `input summary`: 量产运行中的 BMS 柜在最近一周出现偶发 isoSPI 掉线、CRC 错误与少量 reset，当前需要先缩小故障半径，再确认是否影响 failsafe 收敛。
- `normalized case`: 已稳定运行系统中的 active incident，优先走 `incident-investigation` 主链，不把其误判为 bringup 或纯 review 任务。
- `evidence profile`: 运行期日志、AFE 快照、链路心跳丢失记录、reset reason、安全态记录、已有复现实验描述
- `evidence gaps`: 缺少精确链路波形、watchdog 喂狗窗口与链路丢失时的状态迁移证据
- `reroute / upgrade triggers`: 若发现系统从未建立稳定基线，则 `reroute-to-bringup-path`；若发现收敛策略本身存在设计缺口，则 `upgrade-to-design-safety-review`
- `primary scenario`: `incident-investigation`
- `secondary candidates`: `design-safety-review`
- `routing rationale`: 系统原本可运行，当前以运行期异常解释、故障半径缩小与根因定位为主。
- `expected phase backbone`: `hazard-analysis` -> `link-diagnostics` -> `deterministic-foundation` -> `failsafe-validation`
- `expected specialists`: `signal-path-tracer` / `register-state-auditor` / `state-machine-tracer` / `timing-watchdog-auditor` / `failsafe-convergence-reviewer`
- `expected artifacts`: `incident-summary` / `evidence-package` / `segmented-failure-path` / `register-bitfield-map` / `state-transition-chain` / `timeout-watchdog-risk-table` / `failsafe-convergence-note` / `incident-diagnosis-pack`
- `expected control signal`: `continue-current-route`
- `review gate expectation`: 关键缺口被关闭后，允许进入 `enter-review-gate` 并生成 `incident-review-memo`
