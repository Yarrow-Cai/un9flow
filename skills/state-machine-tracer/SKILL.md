---
name: state-machine-tracer
description: Trace state definitions, transitions, and exit conditions to expose stuck states, invalid transitions, and safety-state gaps.
---

# state-machine-tracer

## 目标
- 聚焦状态定义、转移条件与退出路径，识别卡态、异常迁移链与安全态缺口。

## 适用边界
- 只作为 `Domain Specialist` 使用，由场景内调度器或主场景 skill 明确分派。
- 默认首先服务 `incident-investigation`，也可被 `bringup-path` 与 `design-safety-review` 复用。
- 不作为总路由入口，不替代主场景 skill。

## 默认落点 Phase
- `hazard-analysis`
- `deterministic-foundation`
- `failsafe-validation`（验证异常收敛路径）

## 输入契约
- 状态定义与状态枚举
- 转移条件与保护分支
- 当前症状对应的状态表现
- 超时 / 退出条件
- 当前安全态、降级态与恢复条件说明

## 输出 Artifact
- `state-transition-chain`
- `stuck-state-list`
- `safety-state-gap-note`

## 不负责什么
- 不替代寄存器位级审计。
- 不替代 watchdog / timeout 时序分析。
- 不直接裁定链路故障半径。
- 不跳过 evidence gap 直接给出收敛结论。

## 回交条件
- 已明确异常状态迁移链，或已明确缺少哪些状态 / 退出条件证据。

## 与真源文档的关系
- specialist 契约真源见 `docs/DOMAIN_SPECIALIST_CONTRACTS.md`
- 场景内交接边界见 `docs/INCIDENT_WORKFLOW.md`
- 总调度与 phase / dispatch 规则见 `docs/ORCHESTRATION.md`

## Claude Code 宿主附录
- 仅在场景内调度明确分派后进入本 skill。
