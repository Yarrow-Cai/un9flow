# watchdog-timeout-audit-report

- 方法真源：docs/WATCHDOG_TIMEOUT_AUDIT.md
- 生成约定真源：docs/TEMPLATE_GENERATION.md
- 共享生成内核：tools/generation_core.py
- 主输入：watchdog-timeout-audit-findings
- 补充输入：timing-watchdog-audit-pack
- 输出：watchdog-timeout-audit-report
- 输出类型：单文件

## audit summary
- 主循环喂狗依赖单一通信分支，超时退化路径不完整。

## key findings
- `feed_watchdog()` 仅在 CAN 正常时调用。
- 超时恢复与 failsafe 进入条件未对齐。

## evidence highlights
- `main_loop.c`: watchdog feed path
- `can_timeout.c`: bus-off timeout handling
- `diag_log.txt`: reset before failsafe transition

## risk assessment
- 可能出现通信中断后看门狗复位先于受控降级。

## recommended actions
- 将喂狗前提从“通信成功”改为“主循环活性 + 安全条件成立”。

## verification gaps
- 缺少故障注入日志与 reset 前最后一次调度证据。
