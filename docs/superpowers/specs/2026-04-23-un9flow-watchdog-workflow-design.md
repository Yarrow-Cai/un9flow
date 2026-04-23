# un9flow watchdog 专项 workflow 设计稿

日期：2026-04-23
主题：围绕现有 `watchdog-timeout-audit` formal skill、findings、report 与 report generator，定义更重型 watchdog / timeout 专项执行 workflow 的流程骨架、gate 与挂接关系。

## 1. 设计结论摘要

本轮设计采用 **专用 workflow 真源文档** 的方向，而不是继续扩对象模板，或一次性把批量报告流水线与专项 workflow 一起做成大系统。

设计结论如下：

- 新增一个 watchdog / timeout 专项 workflow 真源文档：`docs/WATCHDOG_TIMEOUT_WORKFLOW.md`。
- 该 workflow 默认挂在 `skills/watchdog-timeout-audit/SKILL.md` 下，作为 watchdog 专项执行骨架。
- 该 workflow **不替代主场景总路由**，也**不是新的主场景**或新的 `Domain Specialist`。
- 该 workflow 固定执行顺序为：
  - checklist
  - pack
  - findings
  - report
- 该 workflow 固定两个 gate：
  - evidence sufficiency gate
  - completion / escalation gate
- `design-safety-review` 是它的默认上游；`incident-investigation` 与 `bringup-path` 可以复用它，但不由它反向接管主场景编排。

一句话总结：

> 把 watchdog / timeout 从“对象齐全”推进到“流程齐全”，新增一个专项 workflow 真源文档，把 checklist → pack → findings → report 串成正式执行骨架，同时保持总路由仍由主场景决定。

---

## 2. 当前状态与缺口

仓库当前已经具备：

- `docs/WATCHDOG_TIMEOUT_AUDIT.md`：watchdog / timeout 方法真源。
- `skills/watchdog-timeout-audit/SKILL.md`：watchdog formal skill 入口。
- `docs/templates/watchdog-timeout-audit-checklist.md`：专项 checklist。
- `docs/templates/timing-watchdog-audit-pack.md`：完整 specialist 输出模板。
- `docs/templates/watchdog-timeout-audit-findings.md`：轻量 findings 模板。
- `docs/templates/watchdog-timeout-audit-report.md`：最终专项报告模板。
- `tools/generate_watchdog_timeout_audit_report.py`：报告生成器。
- `docs/CONSISTENCY_VALIDATION.md` 与 `tools/validate_consistency.py`：已纳管上述对象。

但当前仍存在 3 个明确缺口：

1. 虽然对象已经齐全，但还缺少一个**把这些对象串起来的正式执行 workflow**。
2. 当前 watchdog 专项的执行顺序、gate、回退条件与升级规则仍分散在多个对象中，没有一个单独真源进行总收口。
3. 现在的 formal skill、findings、report、generator 更像“对象层完整”，还不是“流程层完整”。

因此，本轮设计的核心不是新增更多对象，而是新增一层流程真源。

---

## 3. 设计目标

本轮只解决以下问题：

1. watchdog / timeout 专项 workflow 应该放在哪里。
2. workflow 应该固定哪些 phase、gate 与输出顺序。
3. workflow 与 `design-safety-review`、`incident-investigation`、`bringup-path` 如何分工。
4. 现有 consistency / CI 如何以最小成本纳管该 workflow 真源文档。

本轮不解决：

- 新的主场景设计
- 新的 `Domain Specialist` 设计
- 批量报告流水线
- 自动裁决器
- 独立 watchdog 专项 GitHub workflow

---

## 4. 边界规则

本轮固定采用以下边界：

1. `WATCHDOG_TIMEOUT_WORKFLOW.md` 不是新的主场景。
2. `WATCHDOG_TIMEOUT_WORKFLOW.md` 不是新的 `Domain Specialist`。
3. 该 workflow 默认挂在 `watchdog-timeout-audit` formal skill 下。
4. 该 workflow 不替代主场景总路由。
5. `timing-watchdog-auditor` 仍然是 watchdog 专项分析动作的执行核心。
6. `watchdog-timeout-audit-report` 仍然只是报告载体，不是自动裁决器。

---

## 5. workflow 对象设计

### 5.1 定位

建议新增：

- `docs/WATCHDOG_TIMEOUT_WORKFLOW.md`

这个对象的定位是：

- watchdog / timeout 的专项执行流程真源
- 用于固定 phase、gate、control signal、输出顺序与升级规则
- 用于把现有 checklist / pack / findings / report 串成正式执行骨架

### 5.2 为什么不用继续堆对象

因为当前仓库已具备：
- 方法真源
- formal skill
- findings
- report
- report generator

下一步最缺的是：

> 这些对象到底按照什么顺序、在什么 gate 下、由谁驱动执行。

所以本轮最合理的是新增流程真源，而不是继续增对象。

---

## 6. workflow 结构设计

建议固定为 **4 个 phase + 2 个 gate**。

### 6.1 Phase 1：`scope framing`
输入：
- 当前审计目标
- 当前风险边界
- 最小证据集
- 当前主场景语义

作用：
- 收口本次 watchdog 审计范围
- 初始化 checklist 范围
- 明确这次是 watchdog / timeout 专项，而不是泛化 incident 根因缩圈

建议输出：
- checklist 起始状态
- 当前 audit scope

### 6.2 Phase 2：`specialist execution`
执行核心：
- `timing-watchdog-auditor`

覆盖重点：
- timing baseline
- watchdog feed path
- blocking / starvation
- reset chain
- failsafe convergence
- ISR / main loop 冲突

建议输出：
- `timing-watchdog-audit-pack`

### 6.3 Gate A：`evidence sufficiency`
判断：
- 当前证据是否足够继续收口 findings / report

分支：
- 若不足：
  - 回补证据
  - 不进入正式报告生成
- 若足够：
  - 进入 findings consolidation

目的：
- 防止证据不足时硬生成 findings / report

### 6.4 Phase 3：`findings consolidation`
作用：
- 从 checklist + pack 中提炼问题清单
- 收束 blocking 项、优先级、next action、verification gaps

建议输出：
- `watchdog-timeout-audit-findings`

### 6.5 Phase 4：`report generation`
执行核心：
- `tools/generate_watchdog_timeout_audit_report.py`

输入：
- findings 为主输入
- pack 为补充输入

建议输出：
- `watchdog-timeout-audit-report`

### 6.6 Gate B：`completion / escalation`
判断：
- 当前 watchdog 专项是否可作为本轮结果收口
- 或是否应升级到更高层场景

分支：
- 若仍存在重大未闭合风险或 blocking 项：
  - 保留“未闭合”状态
  - 升级到 `incident-investigation` 或 `design-safety-review`
- 若已收口：
  - 允许归档专项报告

目的：
- 防止“有报告 = 已解决”

---

## 7. 固定输出顺序

本轮建议固定 watchdog 专项执行顺序为：

1. `watchdog-timeout-audit-checklist`
2. `timing-watchdog-audit-pack`
3. `watchdog-timeout-audit-findings`
4. `watchdog-timeout-audit-report`

这条顺序必须在 workflow 真源中明确写死，避免后续对象漂移。

---

## 8. 与现有场景的分工关系

### 8.1 与 `design-safety-review` 的关系

- `design-safety-review` 是默认上游。
- 当主问题已明确是 watchdog / timeout 风险时，`design-safety-review` 可把专项执行委托给 watchdog workflow。

### 8.2 与 `incident-investigation` 的关系

- `incident-investigation` 可调用 watchdog workflow。
- 但 watchdog workflow 不反向接管 incident 的总体编排与场景路由。

### 8.3 与 `bringup-path` 的关系

- `bringup-path` 可在首次拉通时复用 watchdog workflow。
- 但 watchdog workflow 不替代 bring-up 总流程，也不负责首次建链本身。

---

## 9. consistency / CI 最小纳管

### 9.1 consistency

本轮建议最小新增：

- `docs/WATCHDOG_TIMEOUT_WORKFLOW.md` 必须存在并可读。
- 该文档必须回指：
  - `docs/WATCHDOG_TIMEOUT_AUDIT.md`
  - `skills/watchdog-timeout-audit/SKILL.md`
  - `docs/templates/watchdog-timeout-audit-checklist.md`
  - `docs/templates/timing-watchdog-audit-pack.md`
  - `docs/templates/watchdog-timeout-audit-findings.md`
  - `docs/templates/watchdog-timeout-audit-report.md`
  - `tools/generate_watchdog_timeout_audit_report.py`
- 该文档必须显式声明：
  - 不是新的主场景
  - 不是新的 `Domain Specialist`
  - 默认服务 `design-safety-review`
  - 可被 `incident-investigation` / `bringup-path` 复用
  - 固定顺序：checklist → pack → findings → report

### 9.2 CI

本轮继续保持：
- PR / main 跑 `python tools/validate_consistency.py`
- 不新增第二套 watchdog 专项 workflow

也就是说，本轮的“workflow 落地”在 CI 层依然是：

> 先把流程真源纳入 consistency / 现有 workflow，而不是先做新的自动执行流水线。

---

## 10. 文件落点建议

### 新增

- `docs/WATCHDOG_TIMEOUT_WORKFLOW.md`
- `docs/superpowers/specs/2026-04-23-un9flow-watchdog-workflow-design.md`

### 修改

- `skills/watchdog-timeout-audit/SKILL.md`
- `docs/WATCHDOG_TIMEOUT_AUDIT.md`
- `docs/CONSISTENCY_VALIDATION.md`
- `tools/validate_consistency.py`
- `docs/ROADMAP.md`

### 视需要修改

- `README.md`

---

## 11. 实现顺序建议

建议固定为：

1. 先新增 `WATCHDOG_TIMEOUT_WORKFLOW.md`
2. 再在 watchdog formal skill / 方法真源中补 workflow 回指
3. 再扩 consistency 文档与 CLI 检查
4. 最后同步 `ROADMAP.md` 与必要入口文档

原因是：
- 先把流程真源定义清楚
- 再定义它与现有对象的关系
- 最后让校验与路线图跟上

---

## 12. 最终结论

本轮推荐方向固定为：

> 把 watchdog / timeout 从“对象齐全”推进到“流程齐全”，新增一个挂在 `watchdog-timeout-audit` formal skill 下的 workflow 真源文档，固定 checklist → pack → findings → report 的执行骨架与两个 gate，同时保持总路由仍由主场景决定。