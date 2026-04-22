---
name: timing-watchdog-auditor
description: Audit timing windows, ISR/main-loop responsibilities, and watchdog behavior to expose reset, timeout, and scheduling risks.
---

# timing-watchdog-auditor

## 目标
- 聚焦节拍、timeout、watchdog 与 ISR / main loop 责任划分，识别 reset、卡顿与调度不稳风险。

## 适用边界
- 只作为 `Domain Specialist` 使用，由场景内调度器或主场景 skill 明确分派。
- 默认首先服务 `incident-investigation`，也可被 `bringup-path` 与 `design-safety-review` 复用。
- 不作为总路由入口，不替代主场景 skill。

## 默认落点 Phase
- `failsafe-validation`
- `deterministic-foundation`

## 输入契约
- 节拍信息
- ISR / main loop 责任划分
- timeout / watchdog 行为
- 复位 / 卡顿 / 偶发失效证据
- 与喂狗、超时、调度抖动相关的时序窗口

## 输出 Artifact
- `timeout-watchdog-risk-table`
- `isr-mainloop-conflict-note`
- `timing-instability-hypothesis`

## 线内专项扩展
- `ISR / main loop` 职责冲突检查属于 `timing-watchdog-auditor` 线内专项扩展，不单独派生新的 `Domain Specialist`。
- 当异常表现为 reset、喂狗不稳、timeout 失真、节拍抖动或“系统失活但仍能喂狗”时，必须优先通过 `isr-mainloop-conflict-note` 收口，而不是新造入口名。

## 不负责什么
- 不替代状态机语义审查。
- 不替代寄存器配置真值判断。
- 不直接给出系统级根因定论。
- 不把单次 reset 现象直接包装成确定性结论。

## 回交条件
- 已明确 timeout / watchdog 风险路径，或已明确还缺哪些时序证据。

## 与真源文档的关系
- specialist 契约真源见 `docs/DOMAIN_SPECIALIST_CONTRACTS.md`
- 场景内交接边界见 `docs/INCIDENT_WORKFLOW.md`
- 总调度与 phase / dispatch 规则见 `docs/ORCHESTRATION.md`
- 专项方法真源见 `docs/WATCHDOG_TIMEOUT_AUDIT.md`
- 对应输出模板见 `docs/templates/timing-watchdog-audit-pack.md`

## Claude Code 宿主附录
- 仅在场景内调度明确分派后进入本 skill。
