# un9flow BMS 端到端方法链示例设计稿

日期：2026-04-24
主题：围绕一个“菊花链 AFE 首次拉通后节点枚举不稳定”的 BMS 场景，定义 v6 第一份端到端方法链示例的结构、边界与完成标准。

## 1. 设计结论摘要

本轮设计采用 **端到端案例主文档 + 内嵌关键 artifact 摘要** 的方向，而不是方法卡片集合或纯输出物样例包。

设计结论如下：

- 新增一份主案例文档，放在 `docs/cases/` 下，作为 v6 第一份示例与实战载体。
- 案例选题固定为：**菊花链 AFE 首次拉通后，节点枚举不稳定，伴随偶发 timeout / reset 风险**。
- 案例主线固定串起：
  - `bringup-path`
  - `incident-investigation`
  - watchdog 专项
  - `design-safety-review`
- 文档中嵌入关键 artifact 摘要块，但不拆成十几个独立样例文件。
- 本轮目标是证明“方法链可回放、可阅读、可展示”，不是写完整 BMS 白皮书或培训手册。

一句话总结：

> 先用一个足够真实、足够小的 BMS 场景，把 bring-up → incident → watchdog → safety review 串成一条可回放的方法链样例，让仓库从“方法仓库”开始进入“示例与实战”。

---

## 2. 当前状态与缺口

仓库当前已经具备：

- `skills/bringup-path/SKILL.md`：首次拉通主场景。
- `skills/incident-investigation/SKILL.md`：运行期异常排查主场景。
- `skills/watchdog-timeout-audit/SKILL.md`：watchdog 专项入口。
- `docs/DESIGN_SAFETY_REVIEW.md`：design-time safety review 主场景真源。
- `docs/templates/daisy-chain-isospi-afe-bringup-template.md`：菊花链 / isoSPI / AFE bring-up 模板。
- `docs/templates/watchdog-timeout-audit-findings.md`：watchdog findings 模板。
- `docs/templates/watchdog-timeout-audit-report.md`：watchdog report 模板。
- `tools/generate_watchdog_timeout_audit_report.py`：watchdog 报告生成器。
- `docs/cases/incident-workflow-routing-regression.md` 与 `docs/cases/incident-workflow-dispatch-regression.md`：案例层基线。

但当前仍存在 3 个明确缺口：

1. `v6` 还没有真正意义上的“端到端方法链示例”。
2. 虽然对象层与专项模板已经很多，但还缺一份能说明“什么时候切场景、什么时候切专项、每一步产出什么”的完整样例。
3. 当前仓库对外仍更像“方法与模板集合”，还不像“能演示实际使用方式”的专业能力仓库。

因此，本轮设计的核心不是再补一个对象，而是新增第一份完整示例。

---

## 3. 设计目标

本轮只解决以下问题：

1. 选一个足够真实且范围可控的 BMS 场景。
2. 把 `bringup-path`、`incident-investigation`、watchdog 专项与 `design-safety-review` 串成一条完整方法链。
3. 用一份主案例文档展示每一步输入、输出与切换原因。
4. 让 v6 第一份示例既能阅读、又能对外展示。

本轮不解决：

- 完整 BMS 架构手册
- 全量真实日志与波形库
- 多板型、多硬件版本对比
- 十几个独立 artifact 样例文件
- 培训教材级内容扩展

---

## 4. 边界规则

本轮固定采用以下边界：

1. 这是**一份端到端案例文档**，不是完整项目文档。
2. 这份案例文档重点展示“方法链怎么跑”，不是穷举所有 BMS 功能。
3. 文中可嵌入关键 artifact 摘要，但不拆成一整套独立案例包。
4. 这份案例默认服务仓库对外演示、方法验证与内部复盘。
5. 不把案例写成“所有问题都已解决”的完美故事，必须保留结论边界与未闭合项。

---

## 5. 案例选题设计

建议固定案例题目为：

> **菊花链 AFE 首次拉通后，节点枚举不稳定，伴随偶发 timeout / reset 风险。**

选择这个题目的原因是：

- 能自然连接 `bringup-path` 与新落地的菊花链 / isoSPI / AFE bring-up 模板。
- 能自然引出 `incident-investigation` 的介入条件。
- 能自然接入 watchdog / timeout 专项的 findings、report 与 generator。
- 能在后段自然引出 `design-safety-review` 对风险边界与收敛策略的解释。
- 范围足够小，不需要引入 SOC、均衡、热管理、接触器全链路复杂度。

---

## 6. 文档形态设计

建议新增：

- `docs/cases/bms-daisy-chain-afe-end-to-end-example.md`

该文档的定位是：

- v6 第一份端到端示例主文档
- 面向阅读与展示
- 用正文串起方法链，并嵌入关键 artifact 摘要块

### 为什么不拆成多文件

本轮不建议拆成大量案例文件，原因是：

- 第一份示例更需要可读性，而不是文件体系完整度。
- 一份主文档更容易展示“为什么从 A 切到 B，再切到 C”。
- 若先拆很多文件，阅读门槛会变高，反而不适合作为 v6 起手项。

---

## 7. 案例结构设计

建议主文档至少包含以下 6 段：

### 7.1 `case overview`
说明：
- 系统背景
- 当前硬件阶段
- 初始现象
- 为什么这是个典型 BMS 问题

### 7.2 `bring-up path usage`
展示：
- 为什么先走 `bringup-path`
- 使用了哪些输入
- 建立了什么基线
- 哪些信号说明问题已超出纯 bring-up 动作

### 7.3 `incident handoff`
展示：
- 为什么从 bring-up 升级到 `incident-investigation`
- evidence 如何被整理
- 哪些 specialist 被调用

### 7.4 `watchdog / timeout specialty`
展示：
- 为什么进入 `watchdog-timeout-audit`
- findings 如何形成
- report 如何收口

### 7.5 `design safety review handoff`
展示：
- 为什么问题已触到设计边界
- 哪些内容属于 `design-safety-review`
- 如何解释风险边界与收敛策略

### 7.6 `final outcome`
收口：
- 当前确认了什么
- 仍未确认什么
- 下一步建议是什么
- 这条方法链证明了什么

---

## 8. artifact 呈现方式

本轮建议在主案例文档中嵌入关键 artifact 摘要块，而不是拆成独立完整文件。

建议至少嵌入以下摘要：

- `bringup-baseline` 摘要
- `link-qualification-log` 摘要
- `watchdog-timeout-audit-findings` 摘要
- `watchdog-timeout-audit-report` 摘要
- `risk-boundary-note` 摘要

这些摘要的作用不是替代原始模板，而是帮助读者看到：

- 每一步用了什么
- 每一步产出了什么
- 为什么下一步需要切场景或切专项

---

## 9. 完成标准

这份 v6 第一份示例建议满足以下 4 条：

1. **能完整读通**
   - 不跳大量文件也能理解整条方法链。

2. **能看出阶段切换**
   - 为什么先是 `bringup-path`。
   - 为什么切到 `incident-investigation`。
   - 为什么再进入 watchdog / safety review。

3. **能看出关键 artifact**
   - 每个阶段至少有关键输出摘要。

4. **能看出结论边界**
   - 什么已确认。
   - 什么未确认。
   - 下一步该做什么。

---

## 10. 范围控制

### 本轮做

- 一份主案例文档
- 少量关键 artifact 摘要块
- 清楚的方法链切换说明

### 本轮不做

- 不拆十几个独立案例文件
- 不补完整真实日志集
- 不做多板型对比
- 不做完整 BMS 系统教程
- 不扩成培训手册

---

## 11. 文件落点建议

### 新增

- `docs/cases/bms-daisy-chain-afe-end-to-end-example.md`
- `docs/superpowers/specs/2026-04-24-un9flow-bms-end-to-end-example-design.md`

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

> 用“菊花链 AFE 首次拉通后节点枚举不稳定，伴随偶发 timeout / reset 风险”这个场景，串起 bring-up → incident → watchdog → safety review 的方法链，并以 `docs/cases/` 下的一份主案例文档落地，作为 v6 第一份端到端示例。