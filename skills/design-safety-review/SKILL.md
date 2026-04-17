# design-safety-review

## 目标
- 面向设计阶段的风险边界、收敛路径、`timeout` / `watchdog` / `failsafe` 策略复核。

## 适用边界
- 当前无活跃故障排查压力。
- 不替代 active incident 排障。

## 直进边界
### 允许直进
- 当前无活跃故障排查压力。
- 目标是审查风险边界、收敛路径、timeout / watchdog / failsafe 策略。

### 不该误进
- 当前存在 active incident 的症状链。
- 当前任务实际处于 bring-up 首次拉通阶段。

### 应回总入口
- 用户目标与证据特征明显冲突时，回总入口重新路由。

## 最小输入要求
- 设计目标
- 当前方案说明
- 状态机 / timeout / failsafe 约束
- 当前风险边界

## 默认 Phase 骨架
1. `hazard-analysis`
2. `deterministic-foundation`
3. `failsafe-validation`
4. `link-diagnostics`（按需补）

## 默认 specialist 偏向
- `state-machine-tracer`
- `timing-watchdog-auditor`
- `failsafe-convergence-reviewer`
- `register-state-auditor`
- `signal-path-tracer`（按需）

## 主要 Artifact
- `design-review-summary`
- `risk-boundary-note`
- `convergence-strategy-review`
- `failsafe-check-matrix`

## 场景特化段
### 方案复核与边界审查说明
- 本场景从设计输入出发，先在 `hazard-analysis` 收敛核心风险面，再在 `deterministic-foundation` 固定状态可观测性与边界条件。
- 默认 specialist 装配与总调度规则保持一致：`hazard-analysis` 关注 `signal-path-tracer` 与 `state-machine-tracer`，`deterministic-foundation` 默认引入 `register-state-auditor`，`failsafe-validation` 默认引入 `failsafe-convergence-reviewer` 与 `timing-watchdog-auditor`。
- `failsafe-validation` 应形成 `failsafe-check-matrix`；若存在阻断项，再汇总进 `design-review-summary` 与 `risk-boundary-note`。
- `link-diagnostics` 与 `signal-path-tracer` 只在链路健康已成为设计关键前提时按需补充，不替代线上排障路径。

## 不负责什么
- 不替代活跃故障排查。
- 不在缺乏证据时充当 incident 根因定位器。

## 与总入口 / prompt 契约的关系
- 与总入口路由和字段归并规则遵循 `docs/ORCHESTRATION.md`。
- 与输入/输出字段约束遵循 `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`。

## Claude Code 宿主附录
- 当前任务以设计复核为主，且无活跃 incident 约束时可直接进入本 skill。