---
name: watchdog-timeout-audit
description: Use when design-safety-review 需要对 watchdog/timeout 风险做专项审计，并以轻量 findings 快速收口时间保护、喂狗路径、阻塞风险、reset 链与 failsafe 收敛问题。
---

# watchdog-timeout-audit

## 目标
- 面向 watchdog / timeout 专项审计，快速收口时间保护、喂狗路径、阻塞风险、reset 链与 failsafe 收敛问题。

## 适用边界
- 默认首先服务 `design-safety-review`。
- 不作为新的主场景，不参与总路由竞争。
- 不是新的 `Domain Specialist`，不替代 `timing-watchdog-auditor`。

## 最小输入要求
- `incident-summary` 或等价问题摘要。
- 至少一份 timeout / watchdog 相关证据（日志、时序片段、配置、代码片段、复位记录之一）。
- 当前审计目标（例如：确认喂狗链路、确认 reset chain、确认 failsafe 收敛性）。

## 默认依赖
- 流程真源：`docs/WATCHDOG_TIMEOUT_WORKFLOW.md`
- `docs/WATCHDOG_TIMEOUT_AUDIT.md`
- `skills/timing-watchdog-auditor/SKILL.md`
- `docs/templates/timing-watchdog-audit-pack.md`
- `docs/templates/watchdog-timeout-audit-findings.md`

## 输出
- `timing-watchdog-audit-pack`
- `watchdog-timeout-audit-findings`

## 不负责什么
- 不替代 `timing-watchdog-auditor` 的完整 specialist 审计职责。
- 不直接替代主场景的 phase 规划与总调度决策。
- 不在证据不足时给出确定性系统级根因结论。