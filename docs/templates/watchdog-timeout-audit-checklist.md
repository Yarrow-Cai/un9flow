# watchdog-timeout-audit-checklist

## audit scope
- 项目/模块:
- 审计对象版本:
- 审计时间:
- 审计人:
- 备注:

## 1. timeout definition
- 检查提示：
  - timeout 定义源是否可追溯到需求/安全目标/故障树条目，而非仅来自经验常量。
  - 是否识别并纳入所有关键等待路径（锁等待、队列等待、通信应答、外设就绪、状态机等待）到 timeout 定义范围。
  - 单位与基准（ms/tick/cycle）在规格、配置、代码、日志中是否一致，是否存在隐式换算。
  - 默认值是否有定量依据（最坏执行时间、通信周期、安全反应时间）以及上下限边界说明。
  - timeout 变更入口（编译开关/配置表/在线参数）是否具备范围校验与版本追踪。
- finding:
- evidence:
- risk:
- next action:

## 2. timing baseline
- 检查提示：
  - 时基来源（独立硬件定时器/RTC/OS tick）及其时钟树依赖是否明确。
  - 时基与漂移依据是否基于可测量、可复现实测数据，而非仅凭经验估计。
  - 是否单一可信时基；若存在多时基，是否定义主从关系与切换策略。
  - 漂移/偏移（温漂、校准误差、tick 丢失）是否被量化并计入 timeout 裕量。
  - 中断关闭、临界区、总线阻塞、低功耗切换时，计时是否停摆或失真。
- finding:
- evidence:
- risk:
- next action:

## 3. watchdog feed path
- 检查提示：
  - 喂狗路径必须唯一，避免多入口并行喂狗掩盖局部失效。
  - 喂狗前置条件是否绑定关键健康信号（主循环推进、任务心跳、关键状态机前进、通信有效）。
  - 喂狗位置是否放在关键检查之后，避免在定时中断/空转路径无条件喂狗。
  - 多任务/多核下喂狗权限是否收敛，是否存在单点任务代喂造成假健康。
  - 故障注入（卡死、死循环、队列堵塞）时喂狗是否会停止，且喂狗行为可观察、可审计（日志/计数器/事件链可追踪）。
- finding:
- evidence:
- risk:
- next action:

## 4. blocking / starvation risk
- 检查提示：
  - 阻塞调用上限（锁等待、IO 等待、重试循环）是否有明确超时与上界证明。
  - 是否存在长不退出路径（等待标志、状态机悬停、递归/重入）且无逃逸条件。
  - 任务优先级配置是否可能引发优先级反转或低优先级饥饿，进而影响喂狗/timeout 检查执行。
  - 当调度停滞、时基异常或关键中断被屏蔽时，timeout/watchdog 失效条件是否已识别并有补偿措施。
- finding:
- evidence:
- risk:
- next action:

## 5. reset chain
- 检查提示：
  - watchdog 触发到复位执行链（触发源→复位控制器→启动路径）是否完整且可验证。
  - 复位后状态（外设、执行器、功率级）是否进入默认安全态，且与上电路径一致。
  - sticky/noinit/backup 区域是否存在危险残留，哪些字段必须清零/保留是否有规则与校验。
  - reset 证据（reset reason、故障计数、最后心跳、关键寄存器快照）是否可回放并关联时间线。
- finding:
- evidence:
- risk:
- next action:

## 6. failsafe convergence
- 检查提示：
  - timeout/watchdog 触发后的收敛路径是否定义为有限步骤，并给出最大收敛时间。
  - 降级路径（降功率、断输出、锁定状态、人工复位）是否明确且与 hazard 等级匹配。
  - 收敛过程中是否存在危险中间态（输出抖动、反复上电、状态震荡）及抑制策略。
  - 退出条件（恢复判据、人工确认、冷启动）是否明确，避免自动重试回到风险态。
- finding:
- evidence:
- risk:
- next action:

## blocking items
- item:
- owner:
- due date:
- unblock criteria:

## recommended actions
- priority:
- action:
- owner:
- target date:
- verification:
