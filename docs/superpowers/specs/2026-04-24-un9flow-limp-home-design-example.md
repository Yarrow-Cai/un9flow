# un9flow limp-home 设计说明示例稿

日期：2026-04-24
主题：围绕 `design-safety-review` 主场景，定义一份 limp-home 设计说明示例的结构、边界与完成标准。

## 1. 设计结论摘要

本轮设计采用 **挂在 `design-safety-review` 语义下、落在 `docs/cases/` 中的设计说明示例** 方向，而不是写成 incident 恢复脚本说明或独立通用 design note。

设计结论如下：

- 新增一份主文档，放在 `docs/cases/` 下，作为 v6 下一份示例与实战载体。
- 文档主题固定为 limp-home：说明系统在部分故障下如何以受限能力继续运行。
- 该文档默认服务 `design-safety-review` 语义，重点回答：
  - 何时进入 limp-home
  - 哪些能力可保留
  - 哪些能力必须降级或关闭
  - 风险边界如何保持成立
  - 什么时候允许退出 limp-home
- 文档本质是**受限运行策略设计说明**，不是异常处理脚本、不是营销式“系统仍可运行”的故事。

一句话总结：

> 先把 limp-home 做成一份挂在 `design-safety-review` 语义下的设计说明示例，重点固定进入条件、保留能力、禁止能力、风险边界、退出条件和验证点，而不是先写成 incident 恢复流程或完整 safety case。

---

## 2. 当前状态与缺口

仓库当前已经具备：

- `docs/DESIGN_SAFETY_REVIEW.md`：design-time safety review 主场景真源。
- `docs/WATCHDOG_TIMEOUT_AUDIT.md`：watchdog / timeout 方法真源。
- `docs/WATCHDOG_TIMEOUT_WORKFLOW.md`：watchdog 专项流程真源。
- `docs/templates/watchdog-timeout-audit-findings.md`、`docs/templates/watchdog-timeout-audit-report.md`：专项收口对象。
- `docs/cases/bms-daisy-chain-afe-end-to-end-example.md`：v6 第一份端到端方法链示例。
- `docs/cases/power-board-bringup-example.md`：v6 第二份 bring-up 示例。
- `docs/cases/fault-injection-report-example.md`：v6 第三份 incident 语义的报告型示例。

但当前仍存在 3 个明确缺口：

1. v6 还没有一份明确偏 **受限运行策略设计** 的示例。
2. 当前仓库已有 bring-up、incident、watchdog、report 等对象，但还缺一份说明“在部分故障下如何保留有限能力”的设计型样例。
3. 仓库对外仍缺少一个说明 limp-home 何时进入、保留什么、禁止什么、何时退出的文档级示例。

因此，本轮设计的核心不是新增新对象，而是新增一份设计说明型案例文档。

---

## 3. 设计目标

本轮只解决以下问题：

1. 选一个足够真实且范围可控的 limp-home 场景。
2. 用一份主文档展示进入条件、保留能力、禁止能力、风险边界与退出条件。
3. 让读者能看出 limp-home 不是“继续凑合跑”，而是带约束的受限运行策略。
4. 让 v6 从流程案例、报告案例进一步扩展到设计说明案例。

本轮不解决：

- 完整 safety case
- 完整控制策略实现文档
- 运行时自动恢复脚本
- 全量验证计划
- 多场景 limp-home 策略全集

---

## 4. 边界规则

本轮固定采用以下边界：

1. 这是 **design-safety-review 语义下的设计说明示例**。
2. 重点展示“进入条件 → 保留能力 → 禁止能力 → 风险边界 → 退出条件 → 验证点”。
3. 文档应强调约束与可接受边界，而不是写成乐观叙事。
4. 不把 limp-home 写成“异常后继续试试看”的松散策略。
5. 不把它扩成完整 safety case 或实现细节文档。

---

## 5. 场景选题设计

建议固定题目为：

> **在部分传感链路异常与单路功率受限的条件下，系统进入 limp-home，仅保留最小可接受驱动能力与观测能力。**

选择这个题目的原因是：

- 能自然连接 `design-safety-review` 的风险边界语义。
- 能清晰区分“可保留能力”与“必须禁用能力”。
- 能引出 watchdog / timeout / failsafe 对 limp-home 边界的影响。
- 范围足够小，不需要展开完整控制系统设计。

---

## 6. 文档形态设计

建议新增：

- `docs/cases/limp-home-design-example.md`

该文档的定位是：

- v6 下一份主案例文档
- 面向阅读与展示
- 用正文串起 limp-home 进入条件、运行边界、退出条件与验证点

### 为什么仍放在 `docs/cases/`

原因是：

- v6 当前几份示例都放在案例层，便于统一对外展示。
- 这份文档虽然偏设计说明，但仍然是一个“示例与实战”载体。
- 若未来要抽成更正式的 design note，再迁移也更容易。

---

## 7. 文档结构设计

建议主文档至少包含以下 7 段：

### 7.1 `scenario background`
说明：
- 系统背景
- 当前故障模型
- 为什么需要 limp-home
- 不进入 limp-home 会发生什么

### 7.2 `entry conditions`
明确：
- 哪些故障允许进入 limp-home
- 哪些故障不允许进入 limp-home
- 进入前必须满足哪些最小安全条件

### 7.3 `retained capabilities`
说明 limp-home 下还能保留什么：
- 基本运行能力
- 受限输出能力
- 最小观测 / 通信能力
- 必要告警能力

### 7.4 `degraded / disabled capabilities`
说明哪些能力必须降级或关闭：
- 高风险动作
- 高功率输出
- 某些自动恢复行为
- 某些非关键功能

### 7.5 `risk boundary`
明确：
- limp-home 下仍然接受哪些风险
- 明确不接受哪些风险
- 为什么这样的边界仍可接受

### 7.6 `exit conditions`
说明：
- 什么时候允许退出 limp-home
- 谁来判定退出
- 是否允许自动退出
- 是否必须人工确认

### 7.7 `verification points`
列出后续必须验证的点：
- 进入行为
- 保留能力行为
- 降级行为
- 退出行为
- 边界是否被破坏

---

## 8. artifact 呈现方式

本轮建议在主文档中嵌入少量关键设计摘要，而不是拆成大量附录。

建议至少嵌入：

- `risk-boundary-note` 摘要
- `convergence-strategy-review` 摘要
- `failsafe-check-matrix` 摘要（如有必要）

这些摘要的目标是帮助读者理解：
- limp-home 的边界是如何被定义的
- 为什么保留某些能力
- 为什么禁止某些能力
- 退出条件如何被审查

---

## 9. 完成标准

这份 v6 下一项示例建议满足以下 4 条：

1. **能完整读通**
   - 不跳很多文件也能理解 limp-home 的设计逻辑。

2. **能看出进入 / 保留 / 禁止 / 退出结构**
   - 读者能明确理解 limp-home 是一组带边界的决策，而不是模糊策略。

3. **能看出风险边界**
   - 读者能理解哪些风险仍可接受，哪些风险不可接受。

4. **能看出验证点**
   - 文档不是停在理念层，而是能指出后续必须验证什么。

---

## 10. 范围控制

### 本轮做

- 一份主设计说明文档
- 少量关键设计摘要块
- 进入、保留、降级、退出、验证点说明

### 本轮不做

- 不写完整 safety case
- 不补全量验证计划
- 不写运行时代码实现
- 不扩成大而全的控制设计手册
- 不展开多种 limp-home 模式全集

---

## 11. 文件落点建议

### 新增

- `docs/cases/limp-home-design-example.md`
- `docs/superpowers/specs/2026-04-24-un9flow-limp-home-design-example.md`

### 修改

- `docs/ROADMAP.md`
- `README.md`（如需入口）

---

## 12. 实现顺序建议

建议固定为：

1. 先写主文档
2. 再补最小入口与路线图同步
3. 最后确认文档自洽与对外可读性

原因是：
- 先把设计说明本体写清楚
- 再决定如何暴露入口
- 最后让路线图跟上

---

## 13. 最终结论

本轮推荐方向固定为：

> 把 limp-home 先落成一份挂在 `design-safety-review` 语义下、但放在 `docs/cases/` 中的设计说明示例，重点展示进入条件、保留能力、禁止能力、风险边界、退出条件与验证点，而不是先做完整 safety case 或运行时恢复脚本。