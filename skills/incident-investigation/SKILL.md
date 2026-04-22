---
name: incident-investigation
description: Investigate active incidents in an already-running system by narrowing symptoms, evidence, and root-cause direction.
---

# incident-investigation

## 目标
- 面向现网或验收阶段的异常闭环，解释现象、缩小故障半径，并形成可复核的 incident 证据链。

## 适用边界
- 系统原本可运行，当前目标是解释现象与定位根因。
- 不用于从零建立基线。
- 不替代完整设计评审。

## 直进边界
### 允许直进
- 系统原本可运行。
- 当前有运行期异常。
- 目标是解释现象、缩小故障半径、定位根因。

### 不该误进
- 系统尚未建立稳定运行基线。
- 当前任务本质是设计评审，而非 active incident。

### 应回总入口
- incident / bringup / review 场景交叉且无法直接裁决时，回总入口重新路由。

## 最小输入要求
- 当前症状
- 触发条件
- 影响范围
- 已知证据
- 当前安全态判断

## 默认 Phase 骨架
1. `hazard-analysis`
2. `link-diagnostics`
3. `deterministic-foundation`
4. `failsafe-validation`

## 默认 specialist 偏向
- `hazard-analysis`：`signal-path-tracer`、`state-machine-tracer`
- `link-diagnostics`：`signal-path-tracer`
- `deterministic-foundation`：`register-state-auditor`、`signal-path-tracer`
- `failsafe-validation`：`timing-watchdog-auditor`、`failsafe-convergence-reviewer`

## 主要 Artifact
- `incident-summary`
- `evidence-inventory`
- `evidence-package`
- `incident-diagnosis-pack`
- `incident-review-memo`

## 场景特化段
### 证据流转与收敛说明
- 先对症状与约束做时间窗切片，形成 `evidence-inventory`，把可复核数据（日志、寄存器快照、链路状态、看门狗记录）按时间归一。
- 以 `evidence-inventory` 驱动 `link-diagnostics` 与 `deterministic-foundation` 的关键假设验证，任何假设必须落到可验证证据。
- 每轮得到的诊断发现都回填 `evidence-package`，并以最小增量更新 `incident-diagnosis-pack`，保持根因方向单向收敛。
- 当安全态有疑似异常时优先触发 `failsafe-validation`，用 `incident-review-memo` 记录收敛失败或边界外结果，避免过度断言。

## 不负责什么
- 不负责从零拉通系统。
- 不替代 `design-safety-review`。

## 与总入口 / prompt 契约的关系
- 与总入口调度、字段映射、路由回传关系遵循 `docs/ORCHESTRATION.md` 的总入口决策链路。
- 与输入输出字段约束遵循 `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`。

## Claude Code 宿主附录
- 用户明确要排查运行期异常时可直接进入本 skill。
