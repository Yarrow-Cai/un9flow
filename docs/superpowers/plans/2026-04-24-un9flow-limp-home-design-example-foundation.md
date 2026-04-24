# Limp Home Design Example Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 un9flow 增加一份挂在 `design-safety-review` 语义下、但落在 `docs/cases/` 中的 limp-home 设计说明示例，并同步最小入口与路线图状态。

**Architecture:** 本轮不写完整 safety case、运行时恢复脚本或全量验证计划，而是新增主文档 `docs/cases/limp-home-design-example.md`，用正文固定进入条件、保留能力、禁止能力、风险边界、退出条件与验证点。当前 `.github/workflows/consistency-validation.yml` 不改结构，且本轮默认不为该示例增加新的专门校验器；目标是先让 v6 这份设计说明案例具备可阅读、可展示、可归档的最低完整度。

**Tech Stack:** Markdown, git, Claude Code

---

## File Structure

### Existing files to modify

- `docs/ROADMAP.md` — 把“示例 limp-home 设计说明”从未开始推进为已落地基线。
- `README.md`（如需入口）— 若该示例需要对外可发现入口，则补最小入口说明。

### Existing files to read but not modify

- `docs/DESIGN_SAFETY_REVIEW.md`
- `docs/WATCHDOG_TIMEOUT_AUDIT.md`
- `docs/WATCHDOG_TIMEOUT_WORKFLOW.md`
- `docs/templates/watchdog-timeout-audit-findings.md`
- `docs/templates/watchdog-timeout-audit-report.md`
- `docs/cases/bms-daisy-chain-afe-end-to-end-example.md`
- `docs/cases/power-board-bringup-example.md`
- `docs/cases/fault-injection-report-example.md`

### New files to create

- `docs/cases/limp-home-design-example.md` — limp-home 设计说明主案例文档。
- `docs/superpowers/plans/2026-04-24-un9flow-limp-home-design-example-foundation.md` — 当前 implementation plan。

### No new scripts/workflows

本计划不新增新的脚本、控制逻辑实现或 GitHub workflow。

---

### Task 1: 先创建 limp-home 设计说明主体

**Files:**
- Create: `docs/cases/limp-home-design-example.md`
- Test: `docs/cases/limp-home-design-example.md`

- [ ] **Step 1: 写出案例缺口清单**

```md
当前缺口：
- v6 还没有一份明确偏受限运行策略设计的示例。
- 当前仓库虽已有 bring-up、incident、watchdog、report 等对象，但缺少一份说明“在部分故障下如何保留有限能力”的设计型文档。
- 需要先用一个范围可控的 limp-home 场景，把进入条件、保留能力、禁止能力、风险边界与退出条件讲清楚。
```

- [ ] **Step 2: 运行检查，确认当前还没有该案例文件**

Run: `git ls-files "docs/cases/limp-home-design-example.md"`
Expected: 无输出

- [ ] **Step 3: 创建 `docs/cases/limp-home-design-example.md`**

```md
# Limp Home Design Example

## scenario background
- 系统背景:
- 当前故障模型:
- 为什么需要 limp-home:
- 不进入 limp-home 会发生什么:

## entry conditions
- 哪些故障允许进入 limp-home:
- 哪些故障不允许进入 limp-home:
- 进入前必须满足哪些最小安全条件:

## retained capabilities
- 基本运行能力:
- 受限输出能力:
- 最小观测 / 通信能力:
- 必要告警能力:

## degraded / disabled capabilities
- 高风险动作:
- 高功率输出:
- 某些自动恢复行为:
- 某些非关键功能:

## risk boundary
- limp-home 下仍然接受哪些风险:
- 明确不接受哪些风险:
- 为什么这样的边界仍可接受:

### risk-boundary-note 摘要
- 当前可接受项:
- 当前不可接受项:
- 审查依据:

## exit conditions
- 什么时候允许退出 limp-home:
- 谁来判定退出:
- 是否允许自动退出:
- 是否必须人工确认:

## verification points
- 进入行为:
- 保留能力行为:
- 降级行为:
- 退出行为:
- 边界是否被破坏:
```

- [ ] **Step 4: 运行最小文本检查，确认 7 个主段全部落地**

Run: `grep -n "scenario background\|entry conditions\|retained capabilities\|degraded / disabled capabilities\|risk boundary\|exit conditions\|verification points" docs/cases/limp-home-design-example.md`
Expected: 7 个主段全部命中

---

### Task 2: 给案例补最小入口说明

**Files:**
- Modify: `README.md`
- Test: `README.md`

- [ ] **Step 1: 在 `README.md` 增加案例入口**

```md
- `docs/cases/limp-home-design-example.md`：`design-safety-review` 语义下的 limp-home 设计说明示例，展示进入条件、保留能力、禁止能力、风险边界与退出条件
```

- [ ] **Step 2: 运行最小文本检查**

Run: `grep -n "limp-home-design-example" README.md docs/cases/limp-home-design-example.md`
Expected: README 与案例文档均命中该文件名

---

### Task 3: 同步 ROADMAP 并确认案例已被路线图与入口文档引用

**Files:**
- Modify: `docs/ROADMAP.md`
- Test: `docs/ROADMAP.md`
- Test: `README.md`
- Test: `docs/cases/limp-home-design-example.md`

- [ ] **Step 1: 在 `docs/ROADMAP.md` 把“示例 limp-home 设计说明”标记为已落地基线**

```md
将：
- [ ] 示例 limp-home 设计说明

改成：
- [x] 示例 limp-home 设计说明已落地：`docs/cases/limp-home-design-example.md` 作为 design-safety-review 语义的设计说明示例
```

- [ ] **Step 2: 运行最小文本检查，确认案例已被入口文档与路线图引用**

Run: `grep -n "limp-home-design-example" README.md docs/ROADMAP.md docs/cases/limp-home-design-example.md`
Expected: 3 个文件都命中该案例文件名

- [ ] **Step 3: 提交 limp-home 设计说明示例基线**

```bash
git add docs/cases/limp-home-design-example.md README.md docs/ROADMAP.md
git commit -m "feat: add limp-home design example"
```

---

## Verification Notes

- 本计划不新增脚本或 safety case 文档；当前目标是让 limp-home 设计说明示例落地并能被入口文档与路线图发现。
- 该案例必须始终保持“设计说明示例”定位；若实现中膨胀成完整 safety case、运行时代码说明或大而全设计手册，必须回退。