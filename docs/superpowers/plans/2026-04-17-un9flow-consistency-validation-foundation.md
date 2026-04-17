# un9flow Consistency Validation Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 un9flow 建立 docs 为主真源的统一一致性校验体系，覆盖 docs / skills / templates / routing cases / 过程文档。

**Architecture:** 这一轮仍以文档与模板为主，不写自动校验脚本。核心做法是新增 `docs/CONSISTENCY_VALIDATION.md` 作为总校验真源，再补两个模板：`consistency-review-checklist.md` 与 `validation-findings.md`；同时同步 `README.md`、`docs/ROADMAP.md`、`docs/WORKFLOW.md`、`docs/PLATFORMS.md` 这些受 docs 真源层约束的入口/派生文档，并把 `docs/templates/skill-routing-matrix.md` 明确为案例层模板，让校验对象分层、失败等级、review 执行方式和 findings 记录方式成为稳定流程。

**Tech Stack:** Markdown, git, Claude Code, un9flow 文档仓库

---

## File Structure

### Existing files to modify

- `README.md` — 顶层导航需要纳入统一校验体系文档与模板入口。
- `docs/ROADMAP.md` — 需要把 v4 从泛化“模板生成与一致性校验”推进为统一校验体系基线。
- `docs/templates/skill-routing-matrix.md` — 继续作为案例层模板，需要在校验体系里被明确引用并说明其角色。

### Existing files already created in this feature work

- `docs/ORCHESTRATION.md` — 总调度规则真源。
- `docs/INCIDENT_WORKFLOW.md` — incident 场景真源。
- `docs/SKILL_ARCHITECTURE.md` — skill 架构真源。
- `docs/ORCHESTRATOR_PROMPT_CONTRACT.md` — prompt 协议真源。
- `docs/superpowers/specs/2026-04-17-un9flow-consistency-validation-design.md` — 当前已确认的统一校验体系设计规格。

### New files to create

- `docs/superpowers/plans/2026-04-17-un9flow-consistency-validation-foundation.md` — 当前 implementation plan。
- `docs/CONSISTENCY_VALIDATION.md` — 统一校验体系总文档。
- `docs/templates/consistency-review-checklist.md` — 一轮人工一致性 review 的执行清单。
- `docs/templates/validation-findings.md` — 记录 L1/L2/L3 失败与关闭状态的模板。

### Optional follow-up files (only if scope expands later)

- 自动校验脚本
- CI 校验器
- host-specific 校验流程文档
- 更多案例模板

当前计划默认**不**创建 optional files；这一轮只建立文档与模板基线。

---

### Task 1: 建立统一校验体系总文档

**Files:**
- Create: `docs/CONSISTENCY_VALIDATION.md`
- Modify: `README.md`
- Test: `docs/CONSISTENCY_VALIDATION.md`, `README.md`

- [ ] **Step 1: 写出统一校验真源缺口清单**

```md
当前缺口：
- 仓库已有 docs / skills / templates / routing matrix，但没有一个统一文档说明谁是主真源、谁只做映射、谁负责验证。
- 当前 review 结论依赖聊天与临时判断，缺少固定的失败等级与处理动作定义。
- README 还没有把统一校验体系作为正式文档入口列出来。
```

- [ ] **Step 2: 运行检查，确认当前还没有 `docs/CONSISTENCY_VALIDATION.md`**

Run: `ls docs && grep -n "CONSISTENCY_VALIDATION.md" README.md`
Expected: `docs` 下不存在该文件，README 中无该路径

- [ ] **Step 3: 创建 `docs/CONSISTENCY_VALIDATION.md` 初版文档**

```md
# un9flow Consistency Validation

## 目标

建立 docs 为主真源的统一一致性校验体系，使 docs / skills / templates / routing cases / 过程文档可以在同一套规则下被检查、分级与收口。

## 对象分层

### Level 1: docs 真源层
- `docs/ORCHESTRATION.md`
- `docs/INCIDENT_WORKFLOW.md`
- `docs/SKILL_ARCHITECTURE.md`
- `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`

### Level 2: 正式 skills 映射层
- `skills/orchestration/SKILL.md`
- `skills/incident-investigation/SKILL.md`
- `skills/bringup-path/SKILL.md`
- `skills/design-safety-review/SKILL.md`
- `skills/evidence-pack/SKILL.md`
- `skills/incident-review/SKILL.md`

### Level 3: 模板层
- checklist 模板
- artifact 模板
- routing matrix 模板

### Level 4: 案例层
- routing cases
- 路由矩阵实例

### Level 5: 过程文档层
- `docs/superpowers/specs/*.md`
- `docs/superpowers/plans/*.md`

## 主真源规则
- 主真源只在 docs 层
- skills 层只能映射，不得反向定义规则
- 模板 / 案例 / 过程文档只允许继承或验证，不允许发明新规则

## 每层校验职责
- docs：规则完整性
- skills：真源映射正确性
- 模板：结构可承载性
- 案例：路由可解释性与回归稳定性
- 过程文档：历史一致性

## 失败等级
### L1 阻断级
- 破坏真源、层级、路由或控制信号一致性

### L2 重要级
- 不会立刻破坏真源，但会让后续实现偏航

### L3 整理级
- 不直接影响规则正确性，偏文档整洁度

## 处理动作
- L1：必须先修，未修不得继续
- L2：原则上本轮修；若不修必须记录为 concern
- L3：可顺手修，不阻断流程

## 校验顺序
1. docs 真源层
2. skills 映射层
3. 模板层
4. 案例层
5. 过程文档层

## 当前明确不做
- 自动校验脚本
- CI 校验器
- host-specific 校验流程
```

- [ ] **Step 4: 在 `README.md` 中加入统一校验体系入口**

```md
- `docs/CONSISTENCY_VALIDATION.md`：docs / skills / templates / cases / 过程文档的统一一致性校验真源
```

- [ ] **Step 5: 运行结构检查**

Run: `ls docs && grep -n "CONSISTENCY_VALIDATION.md" README.md docs/CONSISTENCY_VALIDATION.md`
Expected: 新文档存在，README 与文档正文可检出新路径

- [ ] **Step 6: Commit**

```bash
git add README.md docs/CONSISTENCY_VALIDATION.md
git commit -m "docs: add consistency validation baseline"
```

---

### Task 2: 建立 review checklist 与 findings 模板

**Files:**
- Create: `docs/templates/consistency-review-checklist.md`
- Create: `docs/templates/validation-findings.md`
- Test: `docs/templates/consistency-review-checklist.md`, `docs/templates/validation-findings.md`

- [ ] **Step 1: 写出模板缺口清单**

```md
当前缺口：
- 缺少一个可以直接执行一轮人工一致性 review 的清单模板。
- 缺少一个可以记录 L1/L2/L3、修复状态与残留风险的 findings 模板。
```

- [ ] **Step 2: 运行检查，确认当前模板尚不存在**

Run: `ls docs/templates && git ls-files "docs/templates/consistency-review-checklist.md" "docs/templates/validation-findings.md"`
Expected: 两个模板都不存在

- [ ] **Step 3: 创建 `docs/templates/consistency-review-checklist.md`**

```md
# consistency-review-checklist

## review scope
- 

## docs 真源层
- [ ] `ORCHESTRATION.md` 规则边界清楚
- [ ] `INCIDENT_WORKFLOW.md` 未越权重写总规则
- [ ] `SKILL_ARCHITECTURE.md` 与正式 skill 文件一致
- [ ] `ORCHESTRATOR_PROMPT_CONTRACT.md` 未重写场景边界
- [ ] `README.md` 入口文档不越权定义规则
- [ ] `docs/ROADMAP.md` 派生文档不引入冲突口径
- [ ] `docs/WORKFLOW.md` 工作流说明不重写场景真源
- [ ] `docs/PLATFORMS.md` 平台文档不越权扩张 host 承诺

## skills 映射层
- [ ] 正式 skill 文件未越权重写真源
- [ ] 总入口只承接，不重写真源
- [ ] 子入口与辅助 skill 边界清楚

## 模板层
- [ ] 字段完整
- [ ] 允许值与真源一致
- [ ] 模板可直接填写

## 案例层
- [ ] 典型 case 覆盖足够
- [ ] 路由可解释
- [ ] 与当前真源一致

## 过程文档层
- [ ] spec 未保留旧规则
- [ ] plan 未保留旧字段
- [ ] 不会误导后续实现

## overall result
- [ ] 通过
- [ ] 带 concern 通过
- [ ] 不通过
```

- [ ] **Step 4: 创建 `docs/templates/validation-findings.md`**

```md
# validation-findings

## finding id
- 

## level
- 仅允许：L1 / L2 / L3

## file
- 

## issue
- 

## impact
- 

## required action
- 

## status
- 仅允许：open / fixed / accepted concern
- `L1` 只能在 `fixed` 后关闭，不允许标记为 `accepted concern`

## owner
- 

## notes
- 
```

- [ ] **Step 5: 运行结构检查**

Run: `ls docs/templates && grep -n "overall result\|L1 / L2 / L3\|accepted concern" docs/templates/consistency-review-checklist.md docs/templates/validation-findings.md`
Expected: 两个新模板存在，关键字段可检出

- [ ] **Step 6: Commit**

```bash
git add docs/templates/consistency-review-checklist.md docs/templates/validation-findings.md
git commit -m "docs: add validation review templates"
```

---

### Task 3: 同步 roadmap 与现有模板定位

**Files:**
- Modify: `docs/ROADMAP.md`
- Modify: `docs/templates/skill-routing-matrix.md`
- Test: `docs/ROADMAP.md`, `docs/templates/skill-routing-matrix.md`

- [ ] **Step 1: 写出同步缺口清单**

```md
当前缺口：
- roadmap 还没有把统一校验体系写成明确的文档基线。
- `skill-routing-matrix.md` 已存在，但其在统一校验体系中的角色还未被正式标为“案例层模板”。
```

- [ ] **Step 2: 修改 `docs/ROADMAP.md`**

```md
在 v4 合适位置增补：
- 落地 `docs/CONSISTENCY_VALIDATION.md`
- 增加 `consistency-review-checklist.md`
- 增加 `validation-findings.md`
- `skill-routing-matrix.md` 作为案例层模板继续复用
```

- [ ] **Step 3: 在 `docs/templates/skill-routing-matrix.md` 顶部增加角色说明**

```md
补一句：
- 本模板在统一校验体系中作为案例层模板，用于验证路由规则是否能解释真实输入。
```

- [ ] **Step 4: 运行一致性检查**

Run: `grep -n "CONSISTENCY_VALIDATION.md\|consistency-review-checklist\|validation-findings\|案例层模板" docs/ROADMAP.md docs/templates/skill-routing-matrix.md`
Expected: roadmap 与模板都命中新定位

- [ ] **Step 5: Commit**

```bash
git add docs/ROADMAP.md docs/templates/skill-routing-matrix.md
git commit -m "docs: align roadmap with validation layer"
```

---

### Task 4: 自审、验证与收口

**Files:**
- Modify: `README.md` (如需微调)
- Modify: `docs/CONSISTENCY_VALIDATION.md` (如需微调)
- Modify: `docs/ROADMAP.md` (如需微调)
- Modify: `docs/templates/consistency-review-checklist.md` (如需微调)
- Modify: `docs/templates/validation-findings.md` (如需微调)
- Modify: `docs/templates/skill-routing-matrix.md` (如需微调)
- Test: 上述全部文档

- [ ] **Step 1: 运行 placeholder 扫描**

Run: `grep -R -n "TODO\|TBD\|implement later\|fill in details" README.md docs/CONSISTENCY_VALIDATION.md docs/ROADMAP.md docs/templates`
Expected: 新文档中不应出现占位词

- [ ] **Step 2: 运行校验体系术语一致性检查**

Run: `grep -R -n "L1\|L2\|L3\|docs 真源层\|skills 映射层\|模板层\|案例层\|过程文档层" README.md docs`
Expected: 分层与失败等级术语在 docs 中一致

- [ ] **Step 3: 运行模板一致性检查**

Run: `grep -R -n "accepted concern\|overall result\|案例层模板\|L1 / L2 / L3" docs/templates`
Expected: 新模板与 routing matrix 角色一致

- [ ] **Step 4: 运行最小文档集合检查**

Run: `ls docs && ls docs/templates && ls docs/superpowers/specs && ls docs/superpowers/plans`
Expected: `CONSISTENCY_VALIDATION.md`、两个新模板、当前新 spec、新 plan 都存在

- [ ] **Step 5: 运行 git diff 范围审核**

Run: `git diff -- README.md docs/CONSISTENCY_VALIDATION.md docs/ROADMAP.md docs/templates/consistency-review-checklist.md docs/templates/validation-findings.md docs/templates/skill-routing-matrix.md docs/superpowers/specs/2026-04-17-un9flow-consistency-validation-design.md docs/superpowers/plans/2026-04-17-un9flow-consistency-validation-foundation.md`
Expected: 改动集中在计划内文档，无无关文件

- [ ] **Step 6: 如发现问题，做最小修正**

```md
允许的修正类型：
- 统一术语拼写
- 删除重复段落
- 修正文档结构性错误
- 调整模板字段与角色说明不一致问题
- 调整失败等级与处理动作描述不一致问题
```

- [ ] **Step 7: 重新运行关键检查确认收口**

Run: `grep -R -n "CONSISTENCY_VALIDATION.md\|consistency-review-checklist\|validation-findings\|L1\|案例层模板" README.md docs && git diff --stat`
Expected: grep 命中稳定，diff 只显示计划内文档

- [ ] **Step 8: Commit**

```bash
git add README.md docs/CONSISTENCY_VALIDATION.md docs/ROADMAP.md docs/templates/consistency-review-checklist.md docs/templates/validation-findings.md docs/templates/skill-routing-matrix.md docs/superpowers/plans/2026-04-17-un9flow-consistency-validation-foundation.md
git commit -m "docs: finalize consistency validation baseline"
```

---

## Self-Review

### Spec coverage

- 规格第 2 节对象分层与真源关系：Task 1 覆盖
- 规格第 3 节每层校验职责：Task 1 覆盖
- 规格第 4 节失败等级与处理动作：Task 1、Task 2 覆盖
- 规格第 5 节文档与模板落点：Task 1、Task 2、Task 3 覆盖
- 规格第 6 节最终落点与实现顺序：Task 1、Task 2、Task 3 覆盖

### Placeholder scan

本计划没有使用 “TBD / TODO / implement later / similar to Task N” 作为执行步骤占位语，所有步骤都包含明确文件、命令或文档内容。

### Type consistency

计划中统一使用以下关键名词：

- 主真源层：docs 真源层
- 映射层：skills 映射层
- 模板层：templates
- 案例层：routing cases / `skill-routing-matrix`
- 过程文档层：spec / plan
- 失败等级：L1 / L2 / L3

未使用冲突命名。