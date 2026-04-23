# un9flow Watchdog Timeout Workflow

## 目标

为 watchdog / timeout 专项审计提供固定执行流程，确保在不同入口下都能按统一顺序完成范围界定、证据收敛、结论输出与报告生成。

## 定位与边界

- 这不是新的主场景。
- 这不是新的 `Domain Specialist`。
- 默认挂在 `watchdog-timeout-audit` formal skill 下。
- 默认服务 `design-safety-review`。
- 可被 `incident-investigation` 与 `bringup-path` 复用。
- 不替代主场景总路由。

## 固定输出顺序

固定顺序：checklist → pack → findings → report。

1. checklist
2. pack
3. findings
4. report

## Phase 1: scope framing

- 接收 `incident-summary` 或等价问题描述。
- 明确本轮审计目标（如喂狗链路、reset chain、failsafe 收敛性）。
- 确认可用证据范围与缺口，建立 checklist 执行边界。
- 输出进入审计执行前的范围声明，避免跨域扩张。

## Phase 2: specialist execution

- 依托 `timing-watchdog-auditor` 执行 watchdog / timeout 六大检查对象。
- 按模板沉淀 checklist 与 pack，保持 finding-evidence-risk-next action 的可追溯结构。
- 对 ISR / main loop 冲突、阻塞 / 饥饿、假健康喂狗路径进行强制标注。

## Gate A: evidence sufficiency

- 判断证据是否足以支撑 findings 与结论。
- 若证据不足，必须显式列出缺口与补证动作，不输出确定性根因断言。
- Gate A 通过后才允许进入 findings consolidation。

## Phase 3: findings consolidation

- 将 checklist 与 pack 中的关键问题收束为 `watchdog-timeout-audit-findings`。
- 去重并合并同源问题，保留风险优先级与影响面。
- 明确每条 finding 的证据锚点与下一步行动责任。

## Phase 4: report generation

- 使用报告模板与生成脚本将 findings + pack 汇总成最终专项报告。
- 报告需可交付、可审查、可归档，并能回指原始证据。
- 统一报告结构，避免不同入口产生格式漂移。

## Gate B: completion / escalation

- 若 findings 已闭环且风险处置路径明确，则标记 completion。
- 若存在阻断项、关键证据缺失或跨主场景决策需求，则升级 escalation。
- escalation 仅上推决策，不改写主场景总路由职责边界。

## 相关对象回指

- `docs/WATCHDOG_TIMEOUT_AUDIT.md`
- `skills/watchdog-timeout-audit/SKILL.md`
- `docs/templates/watchdog-timeout-audit-checklist.md`
- `docs/templates/timing-watchdog-audit-pack.md`
- `docs/templates/watchdog-timeout-audit-findings.md`
- `docs/templates/watchdog-timeout-audit-report.md`
- `tools/generate_watchdog_timeout_audit_report.py`
