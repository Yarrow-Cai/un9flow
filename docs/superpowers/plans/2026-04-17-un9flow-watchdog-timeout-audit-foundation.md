# un9flow Watchdog Timeout Audit Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 un9flow 建立 `design-safety-review` 下的 watchdog / timeout 专项审计方法文档与可执行 checklist 模板基线。

**Architecture:** 这一轮仍以文档与模板为主，不扩正式 skill 文件、不写自动校验脚本。核心做法是新增 `docs/WATCHDOG_TIMEOUT_AUDIT.md` 作为专项方法真源，再新增 `docs/templates/watchdog-timeout-audit-checklist.md` 作为可填写模板；同时让 README / ROADMAP 能感知这一专项能力已经成为 v5 的第一个可执行切口。

**Tech Stack:** Markdown, git, Claude Code, un9flow 文档仓库

---

## File Structure

### Existing files to modify

- `README.md` — 顶层导航需补入 watchdog / timeout 专项方法文档与 checklist 模板入口。
- `docs/ROADMAP.md` — 需要把 v5 中 watchdog / timeout 审计从纯计划项推进到已落地方法基线的状态表达。

### Existing files already created in this feature work

- `docs/ORCHESTRATION.md` — 总调度规则主文档，其中 `design-safety-review` 已定义为审查风险边界、收敛路径和 timeout / watchdog / failsafe 的场景。
- `docs/superpowers/specs/2026-04-17-un9flow-watchdog-timeout-audit-design.md` — 当前已确认的 watchdog / timeout 专项方法规格。

### New files to create

- `docs/superpowers/plans/2026-04-17-un9flow-watchdog-timeout-audit-foundation.md` — 当前 implementation plan。
- `docs/WATCHDOG_TIMEOUT_AUDIT.md` — watchdog / timeout 专项方法真源文档。
- `docs/templates/watchdog-timeout-audit-checklist.md` — 将 6 组检查项落成可填写 checklist 的模板。

### Optional follow-up files (only if scope expands later)

- 专项 findings 模板
- 专项正式 skill 文件
- 专项自动校验脚本
- 专项 CI 门禁

当前计划默认**不**创建 optional files；这一轮只落方法文档与 checklist。

---

### Task 1: 建立 watchdog / timeout 方法真源文档

**Files:**
- Create: `docs/WATCHDOG_TIMEOUT_AUDIT.md`
- Modify: `README.md`
- Test: `docs/WATCHDOG_TIMEOUT_AUDIT.md`, `README.md`

- [x] **Step 1: 写出专项方法真源缺口清单**

```md
当前缺口：
- 现有体系已有总调度、skill 架构、prompt 契约和一致性校验，但还缺一个真正体现 embedded 专项深度的 audit 方法真源。
- v5 已列出 watchdog / timeout 审计方向，但仓库中还没有对应的专项方法文档。
- README 无法把该能力作为当前已落地的专项入口暴露出来。
```

- [x] **Step 2: 运行检查，确认当前还没有 `docs/WATCHDOG_TIMEOUT_AUDIT.md`**

Run: `ls docs && grep -n "WATCHDOG_TIMEOUT_AUDIT.md" README.md`
Expected: `docs` 目录下不存在该文件，README 中无该路径

- [x] **Step 3: 创建 `docs/WATCHDOG_TIMEOUT_AUDIT.md` 初版文档**

```md
# un9flow Watchdog Timeout Audit

## 目标

把 watchdog / timeout 审计能力固定为 `design-safety-review` 下的专项方法真源，用于审查系统是否具备可解释、可验证、可收敛的时间保护机制。

## 定位与边界

### 它属于什么
- `design-safety-review` 下的专项能力
- 围绕时间保护与复位收敛机制展开的审计方法
- 用于验证系统在异常条件下是否能阻止继续错下去

### 它不属于什么
- 不是独立主场景
- 不是通用性能分析
- 不是任意异常排障入口
- 不是所有保护逻辑的大杂烩

## 审计对象范围
1. timeout 触发源
2. 计时基线
3. 喂狗路径
4. 阻塞 / 饥饿风险
5. 复位链
6. failsafe 收敛

## 核心检查项骨架

### 1. timeout definition
- timeout 由谁定义
- 单位和基准是否明确
- 默认值是否有依据

### 2. timing baseline
- 时基来源
- 时基是否单一且可解释
- 计时是否受阻塞影响

### 3. watchdog feed path
- 谁在喂狗
- 喂狗发生在什么条件下
- 喂狗是全局健康证明还是局部成功证明
- 是否存在假健康设计

### 4. blocking / starvation risk
- 长时间阻塞路径
- 长时间不退出路径
- 调度 / 饥饿风险
- timeout 与 watchdog 是否可能因此失效

### 5. reset chain
- watchdog 到 reset 的路径是否闭合
- reset 后进入什么状态
- reset 后是否回默认安全态
- sticky flag / noinit / backup 状态是否可能导致危险回返

### 6. failsafe convergence
- timeout / watchdog 触发后是否存在明确定义的收敛路径
- 收敛到哪里
- 是否存在危险中间态
- 是否会继续冒险运行

## 每组检查项的输出结构
- `finding`
- `evidence`
- `risk`
- `next action`

## 关键边界句
> watchdog / timeout 审计能力的核心，不是解释“哪里坏了”，而是验证“时间保护机制是否足以在坏掉时阻止系统继续错下去”。
```

- [x] **Step 4: 在 `README.md` 中加入专项方法入口**

```md
- `docs/WATCHDOG_TIMEOUT_AUDIT.md`：`design-safety-review` 下的 watchdog / timeout 专项审计方法真源
```

- [x] **Step 5: 运行结构检查**

Run: `ls docs && grep -n "WATCHDOG_TIMEOUT_AUDIT.md" README.md docs/WATCHDOG_TIMEOUT_AUDIT.md`
Expected: 新文档存在，README 与文档正文都能检出新路径

- [ ] **Step 6: Commit**

```bash
git add README.md docs/WATCHDOG_TIMEOUT_AUDIT.md
git commit -m "docs: add watchdog timeout audit guide"
```

---

### Task 2: 建立 watchdog / timeout checklist 模板

**Files:**
- Create: `docs/templates/watchdog-timeout-audit-checklist.md`
- Test: `docs/templates/watchdog-timeout-audit-checklist.md`

- [x] **Step 1: 写出 checklist 模板缺口清单**

```md
当前缺口：
- 虽然已有专项方法设计，但还没有一份可直接填写的 checklist 来承接 6 组检查项。
- 需要一个足够轻但又能沉淀 finding / evidence / risk / next action 的模板。
```

- [x] **Step 2: 运行检查，确认当前还没有 `watchdog-timeout-audit-checklist.md`**

Run: `ls docs/templates && git ls-files "docs/templates/watchdog-timeout-audit-checklist.md"`
Expected: 当前不存在该模板

- [x] **Step 3: 创建 `docs/templates/watchdog-timeout-audit-checklist.md`**

```md
# watchdog-timeout-audit-checklist

## audit scope
- 

## 1. timeout definition
- finding:
- evidence:
- risk:
- next action:

## 2. timing baseline
- finding:
- evidence:
- risk:
- next action:

## 3. watchdog feed path
- finding:
- evidence:
- risk:
- next action:

## 4. blocking / starvation risk
- finding:
- evidence:
- risk:
- next action:

## 5. reset chain
- finding:
- evidence:
- risk:
- next action:

## 6. failsafe convergence
- finding:
- evidence:
- risk:
- next action:

## blocking items
- 

## recommended actions
- 
```

- [x] **Step 4: 运行结构检查**

Run: `grep -n "timeout definition\|timing baseline\|watchdog feed path\|blocking / starvation risk\|reset chain\|failsafe convergence\|blocking items\|recommended actions" docs/templates/watchdog-timeout-audit-checklist.md`
Expected: 六组检查项与收口段都能检出

- [ ] **Step 5: Commit**

```bash
git add docs/templates/watchdog-timeout-audit-checklist.md
git commit -m "docs: add watchdog timeout audit checklist"
```

---

### Task 3: 同步 roadmap 到 watchdog 专项基线

**Files:**
- Modify: `docs/ROADMAP.md`
- Test: `docs/ROADMAP.md`

- [x] **Step 1: 写出 roadmap 同步缺口清单**

```md
当前缺口：
- roadmap 里的 watchdog / timeout 审计仍停留在纯计划项，没有反映专项方法文档和 checklist 已落地的基线状态。
```

- [x] **Step 2: 在 `docs/ROADMAP.md` 同步 v5 状态**

```md
在 v5 合适位置增补：
- 已落地 `docs/WATCHDOG_TIMEOUT_AUDIT.md` 作为专项方法真源
- 已落地 `docs/templates/watchdog-timeout-audit-checklist.md` 作为专项 checklist 模板
- 正式 skill / findings / CI 留待后续阶段扩展
```

- [x] **Step 3: 运行一致性检查**

Run: `grep -n "WATCHDOG_TIMEOUT_AUDIT.md\|watchdog-timeout-audit-checklist.md" docs/ROADMAP.md`
Expected: roadmap 命中专项文档与模板基线

- [ ] **Step 4: Commit**

```bash
git add docs/ROADMAP.md
git commit -m "docs: align roadmap with watchdog timeout audit"
```

---

### Task 4: 自审、验证与收口

**Files:**
- Modify: `README.md` (如需微调)
- Modify: `docs/WATCHDOG_TIMEOUT_AUDIT.md` (如需微调)
- Modify: `docs/ROADMAP.md` (如需微调)
- Modify: `docs/templates/watchdog-timeout-audit-checklist.md` (如需微调)
- Test: 上述全部文档

- [x] **Step 1: 运行 placeholder 扫描**

Run: `grep -R -n "TODO\|TBD\|implement later\|fill in details" README.md docs/WATCHDOG_TIMEOUT_AUDIT.md docs/ROADMAP.md docs/templates/watchdog-timeout-audit-checklist.md`
Expected: 新文档中不应出现占位词

- [x] **Step 2: 运行专项术语一致性检查**

Run: `grep -R -n "watchdog\|timeout\|failsafe\|reset chain\|timing baseline\|watchdog feed path" README.md docs/WATCHDOG_TIMEOUT_AUDIT.md docs/ROADMAP.md docs/templates/watchdog-timeout-audit-checklist.md`
Expected: 关键审计术语在四份文件中拼写一致

- [x] **Step 3: 运行最小文档集合检查**

Run: `ls docs && ls docs/templates && ls docs/superpowers/specs && ls docs/superpowers/plans`
Expected: `WATCHDOG_TIMEOUT_AUDIT.md`、专项 checklist、本轮新 spec、本轮新 plan 都存在

- [x] **Step 4: 运行 git diff 范围审核**

Run: `git diff -- README.md docs/WATCHDOG_TIMEOUT_AUDIT.md docs/ROADMAP.md docs/templates/watchdog-timeout-audit-checklist.md docs/superpowers/specs/2026-04-17-un9flow-watchdog-timeout-audit-design.md docs/superpowers/plans/2026-04-17-un9flow-watchdog-timeout-audit-foundation.md`
Expected: 改动集中在计划内文档，无无关文件

- [x] **Step 5: 如发现问题，做最小修正**

```md
允许的修正类型：
- 统一术语拼写
- 删除重复段落
- 修正文档结构性错误
- 调整 checklist 字段与方法真源不一致的问题
```

- [x] **Step 6: 重新运行关键检查确认收口**

Run: `grep -R -n "WATCHDOG_TIMEOUT_AUDIT.md\|watchdog-timeout-audit-checklist\|watchdog\|timeout" README.md docs && git diff --stat`
Expected: grep 命中稳定，diff 只显示计划内文档

- [ ] **Step 7: Commit**

```bash
git add README.md docs/WATCHDOG_TIMEOUT_AUDIT.md docs/ROADMAP.md docs/templates/watchdog-timeout-audit-checklist.md docs/superpowers/plans/2026-04-17-un9flow-watchdog-timeout-audit-foundation.md
git commit -m "docs: finalize watchdog timeout audit baseline"
```

---

## Self-Review

### Spec coverage

- 规格第 2 节定位与边界：Task 1 覆盖
- 规格第 3 节核心检查项骨架：Task 1 与 Task 2 覆盖
- 规格第 4 节输出结构：Task 2 覆盖
- 规格第 5 节落点与实现顺序：Task 1、Task 2、Task 3 覆盖

### Placeholder scan

本计划没有使用 “TBD / TODO / implement later / similar to Task N” 作为执行步骤占位语，所有步骤都包含明确文件、命令或文档内容。

### Type consistency

计划中统一使用以下关键名词：

- 专项方法真源：`docs/WATCHDOG_TIMEOUT_AUDIT.md`
- 专项 checklist 模板：`docs/templates/watchdog-timeout-audit-checklist.md`
- 核心检查组：`timeout definition` / `timing baseline` / `watchdog feed path` / `blocking / starvation risk` / `reset chain` / `failsafe convergence`
- 输出结构：`finding` / `evidence` / `risk` / `next action`

未使用冲突命名。