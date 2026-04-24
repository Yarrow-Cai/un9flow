# un9flow 故障注入报告示例设计稿

日期：2026-04-24
主题：围绕一个“末端节点通信间歇失联”的 BMS 故障注入场景，定义一份 incident 语义的故障注入报告示例结构、边界与完成标准。

## 1. 设计结论摘要

本轮设计采用 **incident 语义主案例文档 + 内嵌关键 artifact 摘要** 的方向，而不是完整试验数据库、验证平台输出或 safety case 全文。

设计结论如下：

- 新增一份主案例文档，放在 `docs/cases/` 下，作为 v6 下一份示例与实战载体。
- 案例选题固定为：**在 BMS 菊花链场景中，主动注入末端节点通信间歇失联，观察 timeout、重试、watchdog 风险与收口报告。**
- 案例主线默认挂在 `incident-investigation` 语义下，重点展示：
  - 故障注入目标
  - 注入方式与约束
  - 观察到的行为
  - evidence 如何整理
  - findings / report 如何收口
- 文档中嵌入少量关键 artifact 摘要块，但不拆成大量实验样例文件。
- 本轮目标是证明“故障注入结果如何被方法链吸收和收口”，不是构建完整验证平台。

一句话总结：

> 用一个“末端节点通信间歇失联”的注入场景，做一份可回放、可阅读、可展示的 incident 语义故障注入报告样例，证明 evidence → specialist → findings → report 的收口链条是可用的。

---

## 2. 当前状态与缺口

仓库当前已经具备：

- `skills/incident-investigation/SKILL.md`：incident 主场景入口。
- `skills/watchdog-timeout-audit/SKILL.md`：watchdog 专项入口。
- `docs/templates/watchdog-timeout-audit-findings.md`：专项 findings 模板。
- `docs/templates/watchdog-timeout-audit-report.md`：专项 report 模板。
- `tools/generate_watchdog_timeout_audit_report.py`：report 生成器。
- `docs/cases/bms-daisy-chain-afe-end-to-end-example.md`：第一份端到端 BMS 示例。
- `docs/cases/power-board-bringup-example.md`：第二份 bring-up 示例。

但当前仍存在 3 个明确缺口：

1. v6 还没有一份明确偏 **故障注入结果收口** 的示例。
2. 当前仓库已有 report / findings / workflow / generator，但缺少一份说明“注入了什么、观察到什么、如何收口”的报告型案例。
3. 仓库对外仍缺少一个说明 incident 语义下如何使用 watchdog 专项对象完成验证性案例收口的样例。

因此，本轮设计的核心不是增加新对象，而是新增一份结果导向的案例文档。

---

## 3. 设计目标

本轮只解决以下问题：

1. 选一个足够真实且范围可控的故障注入场景。
2. 用一份主案例文档展示注入目标、观察结果、incident 解释与 watchdog 专项收口。
3. 让读者能看出 evidence、findings、report 是如何串起来的。
4. 让 v6 的示例从“流程案例”扩展到“报告案例”。

本轮不解决：

- 完整试验数据库
- 大量原始日志/波形归档
- 多种注入手法对比
- safety case 全文
- 自动化故障注入平台

---

## 4. 边界规则

本轮固定采用以下边界：

1. 这是 **incident 语义的报告型案例文档**。
2. 重点展示“注入 → 观察 → evidence → findings → report”的链条，不扩成验证平台说明书。
3. 文中可嵌入关键 artifact 摘要，但不拆成大量实验文件。
4. 必须保留结论边界，不能把结果写成“所有风险都已闭环”。
5. 不把它写成完整 safety case 或完整测试计划。

---

## 5. 案例选题设计

建议固定案例题目为：

> **在 BMS 菊花链场景中，主动注入末端节点通信间歇失联，观察 timeout、重试、watchdog 风险与收口报告。**

选择这个题目的原因是：

- 能自然连接现有的 BMS 端到端案例。
- 能自然引出 `incident-investigation` 作为主场景。
- 能直接复用 watchdog findings、report 与 report generator。
- 范围足够小，不需要引入完整硬件试验体系。

---

## 6. 文档形态设计

建议新增：

- `docs/cases/fault-injection-report-example.md`

该文档的定位是：

- v6 下一份主案例文档
- 面向阅读与展示
- 用正文串起注入目标、注入方式、观察行为、incident 解释与 watchdog 收口

### 为什么不拆成多文件

本轮不建议拆成多文件，原因是：

- 这份示例更需要可读性，而不是实验资产管理能力。
- 一份主案例更容易展示“注入了什么 → 看到了什么 → 为什么这样收口”。
- 若先拆成多个文件，会弱化方法链的直观性。

---

## 7. 案例结构设计

建议主文档至少包含以下 6 段：

### 7.1 `case overview`
说明：
- 被测对象
- 注入目标
- 初始风险假设
- 为什么做这次故障注入

### 7.2 `injection setup`
记录：
- 注入方式
- 注入时机
- 注入范围
- 当前约束与安全边界
- 停止条件

### 7.3 `observed behavior`
记录注入后看到的现象：
- timeout
- 重试
- 节点失联
- reset
- watchdog 行为
- 是否进入安全态

### 7.4 `incident interpretation`
展示：
- 为什么它属于 `incident-investigation`
- evidence 如何整理
- 哪些 specialist 被调用
- 哪些初始假设被保留或排除

### 7.5 `watchdog / report synthesis`
展示：
- findings 如何形成
- report 如何收口
- 哪些风险已确认
- 哪些风险仍未闭合

### 7.6 `final outcome`
收口：
- 本次故障注入证明了什么
- 哪些边界被验证了
- 哪些地方还需要补试验
- 下一步建议是什么

---

## 8. artifact 呈现方式

本轮建议嵌入少量关键 artifact 摘要，而不是拆成完整案例包。

建议至少嵌入：

- `evidence-package` 摘要
- `watchdog-timeout-audit-findings` 摘要
- `watchdog-timeout-audit-report` 摘要
- 如有必要，再嵌一个 `incident-review-memo` 或 `risk-boundary-note` 摘要

这些摘要的目标是帮助读者理解：
- 注入了什么
- 观察到什么
- 如何被 incident / watchdog 方法链吸收和收口

---

## 9. 完成标准

这份 v6 下一项示例建议满足以下 4 条：

1. **能完整读通**
   - 不跳大量文件也能理解注入与收口主线。

2. **能看出注入与观察关系**
   - 读者能明确看出注入目标、观察窗口与主要现象。

3. **能看出收口链条**
   - 读者能理解 evidence 如何进入 findings，再进入 report。

4. **能看出结论边界**
   - 明确什么已确认、什么未确认、下一步怎么做。

---

## 10. 范围控制

### 本轮做

- 一份主案例文档
- 少量关键 artifact 摘要块
- 注入、观察、incident 解释与 watchdog 收口说明

### 本轮不做

- 不构建实验数据库
- 不补全量原始波形/日志
- 不做多种注入手法对比
- 不扩成完整测试计划
- 不扩成完整 safety case

---

## 11. 文件落点建议

### 新增

- `docs/cases/fault-injection-report-example.md`
- `docs/superpowers/specs/2026-04-24-un9flow-fault-injection-report-example-design.md`

### 修改

- `docs/ROADMAP.md`
- `README.md`（如需入口）

---

## 12. 实现顺序建议

建议固定为：

1. 先写主案例文档
2. 再补最小入口与路线图同步
3. 最后确认文档自洽与对外可读性

原因是：
- 先把案例本体写清楚
- 再决定如何暴露入口
- 最后让路线图跟上

---

## 13. 最终结论

本轮推荐方向固定为：

> 用“末端节点通信间歇失联”的场景，新增一份 incident 语义的故障注入报告主文档，重点展示注入、观察、evidence 收口、watchdog findings / report 收口以及结论边界。