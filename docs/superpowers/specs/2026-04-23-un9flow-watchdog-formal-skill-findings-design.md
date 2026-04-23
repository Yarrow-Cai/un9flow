# un9flow watchdog formal skill / findings / CI 设计稿

日期：2026-04-23
主题：围绕 `WATCHDOG_TIMEOUT_AUDIT` 方法真源，定义 watchdog / timeout 正式专项 skill、findings 载体与 consistency/CI 最小集成方式。

## 1. 设计结论摘要

本轮设计采用 **formal skill + findings 优先，CI 最小接入** 的方向，而不是先扩复杂 CI 或一次性引入新的主场景 / specialist。

设计结论如下：

- 新增一个 watchdog / timeout 专项正式 skill 入口，但它**不是新的主场景**，也**不是新的 `Domain Specialist`**。
- 新增一个 watchdog / timeout findings 模板，用于承接轻量专项问题清单；它不替代 `timing-watchdog-audit-pack.md`。
- `timing-watchdog-auditor` 仍然是 watchdog 专项分析动作的专业执行核心；formal skill 只负责专项入口、输入边界、输出落点和与主场景的衔接说明。
- consistency CLI 与现有 GitHub workflow 继续沿用最小门禁模式；本轮只增加对象映射检查，不新增第二套 CI。
- 本轮交付物固定为：**正式 watchdog 专项 skill + findings 模板 + 真源/校验/路线图对齐**。

一句话总结：

> 先把 watchdog / timeout 从“方法真源 + specialist pack”推进到“正式专项 skill + findings 载体 + consistency/CI 最小纳管”，而不是先扩主场景或新 specialist。

---

## 2. 当前状态与缺口

仓库当前已经具备：

- `docs/WATCHDOG_TIMEOUT_AUDIT.md`：watchdog / timeout 方法真源。
- `skills/timing-watchdog-auditor/SKILL.md`：watchdog 相关 `Domain Specialist` skill。
- `docs/templates/timing-watchdog-audit-pack.md`：完整 specialist 输出模板。
- `docs/templates/watchdog-timeout-audit-checklist.md`：专项 checklist。
- `docs/CONSISTENCY_VALIDATION.md` 与 `tools/validate_consistency.py`：已覆盖 watchdog 方法真源与 specialist/template 映射。

但当前仍存在 3 个明确缺口：

1. watchdog / timeout 仍缺一个**正式专项 skill 入口**，导致用户若想直接做 watchdog 审计，只能绕行主场景文档或 specialist skill。
2. 当前只有完整 pack 与 checklist，仍缺一个**轻量 findings 载体**，不利于专项问题清单化收口、review 记录与 CI 门禁承接。
3. consistency / CI 已能检查 watchdog 方法真源与 pack 映射，但还不能检查“正式专项 skill + findings 模板”这两个新增对象。

因此，本轮设计的核心不是重写已有 watchdog 主线，而是补齐专项入口与轻量收口物。

---

## 3. 设计目标

本轮只解决以下问题：

1. watchdog / timeout 正式专项 skill 入口应该如何定位。
2. watchdog findings 载体应该放在哪里、如何与 pack/checklist 分工。
3. 现有 consistency / CI 应该如何以最小成本纳管这两个新增对象。
4. 路线图如何更新，避免与当前已落地状态冲突。

本轮不解决：

- 新的主场景设计
- 新的 `Domain Specialist` 设计
- 独立 watchdog 专项 workflow / GitHub Action
- 自动生成 findings 报告器
- artifact 内容正确性的语义自动判定

---

## 4. 边界规则

本轮固定采用以下边界：

1. `watchdog-timeout-audit` **不是新的主场景**。
2. `watchdog-timeout-audit` **不是新的 `Domain Specialist`**。
3. `timing-watchdog-auditor` 仍然是 watchdog 专项分析动作的执行核心。
4. findings 是轻量收口物，不替代 `timing-watchdog-audit-pack.md`。
5. checklist 继续承担“逐项审计执行提示”，findings 负责“问题清单化落点”，pack 负责“完整 specialist 输出”。

---

## 5. 正式 watchdog 专项 skill 设计

### 5.1 定位

建议新增：

- `skills/watchdog-timeout-audit/SKILL.md`

这个 skill 的定位是：

- watchdog / timeout 审计的专项入口
- 默认首先服务 `design-safety-review`
- 可在已知主要问题是 timeout / watchdog / reset / feed-path / blocking / starvation 风险时直接进入
- 不与 `incident-investigation` 争夺主路由，不与 `timing-watchdog-auditor` 争夺 specialist 身份

### 5.2 它负责什么

formal skill 负责：

- 定义 watchdog 专项入口边界
- 说明最小输入要求
- 指明默认会调用/复用 `timing-watchdog-auditor`
- 说明会产出哪些主要 Artifact / findings
- 说明与 `design-safety-review`、`incident-investigation`、`timing-watchdog-auditor` 的关系

### 5.3 它不负责什么

formal skill 不负责：

- 充当新的 `Domain Specialist`
- 替代 `timing-watchdog-auditor` 的输入/输出契约
- 改写主场景路由规则
- 独立生成系统级根因结论

### 5.4 建议输出

这个 skill 建议默认对齐两类输出：

- 完整输出：`timing-watchdog-audit-pack`
- 轻量输出：`watchdog-timeout-audit-findings`

---

## 6. findings 载体设计

### 6.1 定位

建议新增：

- `docs/templates/watchdog-timeout-audit-findings.md`

该模板的定位是：

- watchdog / timeout 专项问题清单模板
- 比 `timing-watchdog-audit-pack.md` 更轻量
- 比 checklist 更接近结论收口物
- 用于 review、门禁、专项结论提炼

### 6.2 与 pack / checklist 的分工

#### `docs/templates/watchdog-timeout-audit-checklist.md`
负责：
- 执行检查提示
- 引导审计过程
- 逐项填写 `finding/evidence/risk/next action`

#### `docs/templates/timing-watchdog-audit-pack.md`
负责：
- specialist 的完整输入快照
- 证据链、主 Artifact、confidence、gaps、backlinks、next suggestion
- 更完整的 dispatch 结果承接

#### `docs/templates/watchdog-timeout-audit-findings.md`
负责：
- 把专项问题收束为轻量 findings 列表
- 承接阻断项、优先级、建议动作与验证状态
- 给 CI / review 一个明确落点

一句话分工：

- checklist：怎么查
- pack：查完的完整 specialist 输出
- findings：查出的问题清单

### 6.3 建议字段

findings 模板建议至少包含：

- audit scope
- finding id
- section / audit dimension
- finding
- evidence
- risk
- severity
- blocking
- next action
- owner
- verification status

本轮不要求设计复杂 schema，但必须能稳定承接 watchdog 专项问题。

---

## 7. consistency / CI 最小集成

### 7.1 总体策略

本轮不新建 watchdog 专项 workflow；继续复用：

- `tools/validate_consistency.py`
- `.github/workflows/consistency-validation.yml`

### 7.2 需要新增的最小检查

consistency 需要新增以下对象映射检查：

1. `skills/watchdog-timeout-audit/SKILL.md` 必须存在并可读。
2. 该 skill 必须明确：
   - 不作为新的主场景
   - 不作为新的 `Domain Specialist`
   - 回指 `docs/WATCHDOG_TIMEOUT_AUDIT.md`
   - 回指 `docs/templates/timing-watchdog-audit-pack.md`
   - 回指 `docs/templates/watchdog-timeout-audit-findings.md`
3. `docs/templates/watchdog-timeout-audit-findings.md` 必须存在并可读。
4. findings 模板必须显式回指：
   - `docs/WATCHDOG_TIMEOUT_AUDIT.md`
   - `skills/watchdog-timeout-audit/SKILL.md`
5. `docs/WATCHDOG_TIMEOUT_AUDIT.md` 应补充对 watchdog formal skill / findings 的回指。

### 7.3 CI 接入策略

CI 继续保持：

- PR / main 跑 `python tools/validate_consistency.py`
- 只要 consistency 规则覆盖新增对象，GitHub workflow 就会自动把它们纳入门禁

这意味着本轮的“CI 集成”本质上是：

> 让 watchdog formal skill 与 findings 成为 consistency CLI 可检查对象，从而自动被现有 workflow 纳管。

---

## 8. 文件落点建议

### 新增

- `skills/watchdog-timeout-audit/SKILL.md`
- `docs/templates/watchdog-timeout-audit-findings.md`
- `docs/superpowers/specs/2026-04-23-un9flow-watchdog-formal-skill-findings-design.md`

### 修改

- `docs/WATCHDOG_TIMEOUT_AUDIT.md`
- `docs/CONSISTENCY_VALIDATION.md`
- `tools/validate_consistency.py`
- `docs/ROADMAP.md`

### 视需要修改

- `README.md`
- `docs/DESIGN_SAFETY_REVIEW.md`

---

## 9. 实现顺序建议

建议固定为：

1. 先新增 watchdog formal skill 与 findings 模板
2. 再补 `WATCHDOG_TIMEOUT_AUDIT.md` 的回指关系
3. 再扩 consistency 文档与 CLI 检查
4. 最后同步 `ROADMAP.md` 与必要入口文档

原因是：
- 先定义对象
- 再定义对象间映射
- 最后让校验和路线图跟上

---

## 10. 最终结论

本轮推荐方向固定为：

> 把 watchdog / timeout 从“方法真源 + specialist pack”推进到“正式专项 skill + findings 载体 + consistency/CI 最小纳管”，同时继续保持 `timing-watchdog-auditor` 作为执行核心，不新增主场景或新的 `Domain Specialist`。
