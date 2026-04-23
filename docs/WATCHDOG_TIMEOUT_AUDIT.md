# un9flow Watchdog Timeout Audit

## 目标

将 watchdog / timeout 审计能力固定为 `design-safety-review` 下的专项方法真源，用于审查系统是否具备可解释、可验证、可收敛的时间保护机制。

## 定位与边界

### 它属于什么

- `design-safety-review` 下的专项能力
- 围绕时间保护与复位收敛机制展开
- 关注在异常条件下，系统是否能够阻止继续错下去

### 它不属于什么

- 不是独立主场景
- 不是通用性能分析
- 不是任意异常排障入口
- 不是所有保护逻辑的大杂烩

## 与 specialist / 模板 / 主场景的关系
- specialist 契约真源：`docs/DOMAIN_SPECIALIST_CONTRACTS.md`
- 对应 `Domain Specialist`：`timing-watchdog-auditor`
- 正式专项 skill：`skills/watchdog-timeout-audit/SKILL.md`
- 对应输出模板：`docs/templates/timing-watchdog-audit-pack.md`
- 轻量 findings 模板：`docs/templates/watchdog-timeout-audit-findings.md`
- 最终专项报告模板：`docs/templates/watchdog-timeout-audit-report.md`
- 报告生成器脚本：`tools/generate_watchdog_timeout_audit_report.py`
- 主要复用主场景：`docs/DESIGN_SAFETY_REVIEW.md`

报告生成器说明：`tools/generate_watchdog_timeout_audit_report.py` 以 `watchdog-timeout-audit-findings` 为主输入、以 `timing-watchdog-audit-pack` 为补充输入，生成最终 `watchdog-timeout-audit-report`。

职责分工固定为：
- 本文档回答“审什么、为什么审、失败态是什么”。
- `docs/templates/watchdog-timeout-audit-checklist.md` 负责逐项审计执行提示。
- `docs/templates/timing-watchdog-audit-pack.md` 负责完整 specialist 输出。
- `docs/templates/watchdog-timeout-audit-findings.md` 负责专项问题清单化收口。
- `docs/templates/watchdog-timeout-audit-report.md` 负责把 findings 与 pack 收束成可交付、可审查、可归档的专项报告。

## 关键边界句

watchdog / timeout 审计能力的核心，不是解释“哪里坏了”，而是验证“时间保护机制是否足以在坏掉时阻止系统继续错下去”。

## 审计对象范围

1. timeout 触发源
2. 计时基线
3. 喂狗路径
4. 阻塞 / 饥饿风险
5. 复位链
6. failsafe 收敛

## ISR / main loop 职责冲突

### 审计重点
- ISR 必须保持短、快、可退出；不得承担长阻塞、完整状态推进或无边界重试。
- main loop 只能消费已归一化事件；不得承担依赖硬实时保证却没有固定节拍约束的关键动作。
- 若 watchdog feed path 位于 ISR 或空转路径，必须直接记为假健康风险。
- 若冲突会导致 timeout 检查失真、喂狗责任漂移或 reset 链解释中断，必须升级为阻断项。

### 最低输出
- `isr-mainloop-conflict-note` 至少回答：
  - ISR 侧越权动作是什么
  - main loop 侧缺口是什么
  - 被破坏的确定性约束是什么
  - 可能导致的 reset / timeout / 饥饿风险是什么
  - 仍缺哪些证据

## 核心检查项骨架

### 1) timeout definition（timeout 触发源）

关键检查点：
- timeout definition 是否明确且可追溯到具体模块/状态
- 触发条件是否可验证（条件、阈值、优先级）
- 是否存在未纳入 timeout 定义的关键等待路径

输出结构：
- `finding`
- `evidence`
- `risk`
- `next action`

### 2) timing baseline（计时基线）

关键检查点：
- timing baseline 是否基于可测量、可复现实测数据
- 基线与系统时钟源、调度节拍、计数粒度是否一致
- 基线偏移/漂移对保护触发边界是否有量化说明

输出结构：
- `finding`
- `evidence`
- `risk`
- `next action`

### 3) watchdog feed path（喂狗路径）

关键检查点：
- watchdog feed path 是否唯一、可观察、可审计
- 喂狗动作是否绑定健康条件而非无条件执行
- 喂狗链路是否覆盖关键状态机与关键任务活性

输出结构：
- `finding`
- `evidence`
- `risk`
- `next action`

### 4) blocking / starvation risk（阻塞 / 饥饿风险）

关键检查点：
- blocking / starvation risk 是否覆盖任务阻塞、锁竞争、优先级反转
- 是否存在“系统失活但仍可喂狗”的错误通路
- 是否定义了阻塞上限与超时回退路径

输出结构：
- `finding`
- `evidence`
- `risk`
- `next action`

### 5) reset chain（复位链）

关键检查点：
- reset chain 是否明确从触发到执行的完整链路
- 复位后关键状态、寄存器、通信链路是否进入可控初始态
- 复位证据是否可记录、可回放、可复盘

输出结构：
- `finding`
- `evidence`
- `risk`
- `next action`

### 6) failsafe convergence（failsafe 收敛）

关键检查点：
- failsafe convergence 是否定义可判定的收敛终态
- 异常持续时是否防止反复抖动或错误重入
- 收敛策略是否具备降级路径与退出条件

输出结构：
- `finding`
- `evidence`
- `risk`
- `next action`
