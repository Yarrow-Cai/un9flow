# un9flow watchdog 自动报告设计稿

日期：2026-04-23
主题：围绕现有 watchdog formal skill、findings 与 pack，定义 watchdog / timeout 自动报告模板与 consistency/CI 最小纳管方式。

## 1. 设计结论摘要

本轮设计采用 **自动报告优先，findings 为主输入、pack 为补充输入** 的方向，而不是先扩独立 workflow 或把 checklist / pack / findings 三者同时做成复杂编排系统。

设计结论如下：

- 新增一个 watchdog / timeout 自动报告模板，用于把 findings 与 pack 收束成一份可交付、可审查、可归档的专项报告。
- 该报告的**主输入**是 `watchdog-timeout-audit-findings`，**补充输入**是 `timing-watchdog-audit-pack`。
- 自动报告不是新的裁决器，不自动发明风险等级，不替代 specialist、review gate 或主场景。
- consistency CLI 与现有 GitHub workflow 继续沿用最小门禁模式；本轮只增加“报告模板存在性与映射关系”的检查，不新增第二套 CI。
- 本轮交付物固定为：**watchdog 自动报告模板 + 真源/校验/路线图对齐**。

一句话总结：

> 先把 watchdog / timeout 从“formal skill + findings”推进到“可自动汇总的专项报告模板 + consistency/CI 最小纳管”，让专项输出从问题清单进一步变成可归档的报告载体。

---

## 2. 当前状态与缺口

仓库当前已经具备：

- `skills/watchdog-timeout-audit/SKILL.md`：watchdog / timeout formal skill。
- `docs/templates/watchdog-timeout-audit-findings.md`：轻量 findings 模板。
- `docs/templates/timing-watchdog-audit-pack.md`：完整 specialist 输出模板。
- `docs/templates/watchdog-timeout-audit-checklist.md`：执行提示模板。
- `docs/WATCHDOG_TIMEOUT_AUDIT.md`：方法真源。
- `docs/CONSISTENCY_VALIDATION.md` 与 `tools/validate_consistency.py`：已纳管 formal skill / findings 基线。

但当前仍存在 3 个明确缺口：

1. 仍缺一个**对外可交付的 watchdog 自动报告载体**；目前只有 checklist、findings、pack 三类中间或半收口对象。
2. findings 已能承接问题清单，pack 已能承接完整 specialist 输出，但两者之间还缺一个“最终专项报告”层。
3. consistency / CI 还不能检查 watchdog 自动报告模板对象。

因此，本轮设计的核心不是新建编排系统，而是新增一个最终报告载体。

---

## 3. 设计目标

本轮只解决以下问题：

1. watchdog 自动报告模板应该放在哪里。
2. watchdog 自动报告如何消费 findings 与 pack。
3. 自动报告与 checklist / findings / pack 的边界如何固定。
4. 现有 consistency / CI 如何以最小成本纳管它。

本轮不解决：

- 新的主场景设计
- 新的 `Domain Specialist` 设计
- 独立 watchdog 专项 workflow / GitHub Action
- 自动风险分级引擎
- 自动根因裁决器
- checklist / findings / pack 三者的复杂冲突消解逻辑

---

## 4. 边界规则

本轮固定采用以下边界：

1. 自动报告不是新的主场景。
2. 自动报告不是新的 `Domain Specialist`。
3. 自动报告不是自动裁决器，不发明新的系统级结论。
4. `watchdog-timeout-audit-findings` 是主输入。
5. `timing-watchdog-audit-pack` 是补充输入。
6. `watchdog-timeout-audit-checklist.md` 继续只承担执行提示，不直接作为自动报告主输入。

---

## 5. 自动报告对象设计

### 5.1 定位

建议新增：

- `docs/templates/watchdog-timeout-audit-report.md`

这个对象的定位是：

- watchdog / timeout 的最终专项报告模板
- 用于收束 findings 与 pack
- 供 review、归档、提交物整理和后续报告生成逻辑使用

### 5.2 输入关系

#### 主输入
- `docs/templates/watchdog-timeout-audit-findings.md`

#### 补充输入
- `docs/templates/timing-watchdog-audit-pack.md`

### 5.3 为什么不用 checklist 作为主输入

本轮不建议把 checklist 作为自动报告主输入，原因是：

- checklist 更偏执行提示与逐项填写；
- findings 更接近问题清单；
- pack 更接近完整 specialist 输出；
- 自动报告应建立在“已收口的问题”之上，而不是建立在“仍在填写过程”的执行模板之上。

---

## 6. 报告结构设计

自动报告模板建议至少包含以下 6 段：

### 6.1 `audit summary`
- 审计对象
- 审计范围
- 总体结论
- 当前总体风险等级（仅承接已有结论，不自动发明）

### 6.2 `key findings`
- blocking 项
- 高优先级问题
- 当前必须处理的问题

### 6.3 `evidence highlights`
- 从 pack 中抽 timeout / baseline / feed path / blocking / reset / failsafe 的关键信息
- 必要时吸收 ISR / main loop 冲突结论

### 6.4 `risk assessment`
- 当前已确认风险
- 当前未闭合风险
- 对 bring-up / release / safety review 的影响

### 6.5 `recommended actions`
- 基于 findings 中的 `next action` 统一整理建议动作
- 不自动推断超出输入之外的新动作

### 6.6 `verification gaps`
- 明确当前仍缺什么证据
- 明确哪些结论仍是保守判断

---

## 7. 与 checklist / findings / pack 的分工

### `docs/templates/watchdog-timeout-audit-checklist.md`
负责：
- 逐项执行提示
- 审计过程中的填写引导

### `docs/templates/watchdog-timeout-audit-findings.md`
负责：
- 问题清单化收口
- severity / blocking / next action / verification status

### `docs/templates/timing-watchdog-audit-pack.md`
负责：
- 完整 specialist 输出
- 更强的上下文、证据链、confidence、gaps、backlinks

### `docs/templates/watchdog-timeout-audit-report.md`
负责：
- 对外专项报告
- 把 findings 与 pack 汇总为可交付、可审查、可归档的报告

一句话分工：

- checklist：怎么查
- findings：查出了什么问题
- pack：完整 specialist 上下文
- report：最终专项报告

---

## 8. consistency / CI 最小纳管

### 8.1 总体策略

本轮不新增 watchdog 专项 workflow；继续复用：

- `tools/validate_consistency.py`
- `.github/workflows/consistency-validation.yml`

### 8.2 需要新增的最小检查

consistency 需要新增以下对象检查：

1. `docs/templates/watchdog-timeout-audit-report.md` 必须存在并可读。
2. 报告模板必须显式回指：
   - `docs/WATCHDOG_TIMEOUT_AUDIT.md`
   - `docs/templates/watchdog-timeout-audit-findings.md`
   - `docs/templates/timing-watchdog-audit-pack.md`
3. 报告模板必须包含固定结构段：
   - `audit summary`
   - `key findings`
   - `evidence highlights`
   - `risk assessment`
   - `recommended actions`
   - `verification gaps`
4. `docs/WATCHDOG_TIMEOUT_AUDIT.md` 应补充对 watchdog report 模板的回指。

### 8.3 CI 集成策略

CI 继续保持：

- PR / main 跑 `python tools/validate_consistency.py`
- 只要 consistency 规则覆盖新增对象，GitHub workflow 就会自动把它纳入门禁

这意味着本轮的“自动报告能力”在 CI 层的实现方式是：

> 先把报告模板对象纳入 consistency / 现有 workflow，而不是先做真正的自动报告生成器。

---

## 9. 文件落点建议

### 新增

- `docs/templates/watchdog-timeout-audit-report.md`
- `docs/superpowers/specs/2026-04-23-un9flow-watchdog-report-design.md`

### 修改

- `docs/WATCHDOG_TIMEOUT_AUDIT.md`
- `docs/CONSISTENCY_VALIDATION.md`
- `tools/validate_consistency.py`
- `docs/ROADMAP.md`

### 视需要修改

- `README.md`
- `skills/watchdog-timeout-audit/SKILL.md`

---

## 10. 实现顺序建议

建议固定为：

1. 先新增 watchdog report 模板
2. 再补 `WATCHDOG_TIMEOUT_AUDIT.md` 的 report 回指关系
3. 再扩 consistency 文档与 CLI 检查
4. 最后同步 `ROADMAP.md` 与必要入口文档

原因是：
- 先定义最终报告对象
- 再定义它与 findings / pack / 方法真源的关系
- 最后让校验与路线图跟上

---

## 11. 最终结论

本轮推荐方向固定为：

> 把 watchdog / timeout 从“formal skill + findings”推进到“自动报告模板 + consistency/CI 最小纳管”，同时继续保持 findings 为主输入、pack 为补充输入，不把自动报告做成新的主场景、specialist 或自动裁决器。