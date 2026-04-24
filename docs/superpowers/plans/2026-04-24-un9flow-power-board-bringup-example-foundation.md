# Power Board Bring-up Example Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 un9flow 增加第二份 v6 端到端示例，使用一个“功率板首次上电后预充完成但 PWM 输出建立不稳定”的场景展示 `bringup-path` 的实际用法。

**Architecture:** 本轮不拆成多文件案例包，而是新增一个主案例文档 `docs/cases/power-board-bringup-example.md`，用正文串起安全基线、bring-up 动作、控制建立与升级判断，并嵌入少量关键 artifact 摘要。当前 `.github/workflows/consistency-validation.yml` 不改结构，且本轮默认不为该示例增加新的专门校验器；目标是先让 v6 第二份案例具备可阅读、可展示、可归档的最低完整度。

**Tech Stack:** Markdown, git, Claude Code

---

## File Structure

### Existing files to modify

- `docs/ROADMAP.md` — 把“示例功率板 bring-up 流程”从未开始推进为已落地基线。
- `README.md`（如需入口）— 若该示例需要对外可发现入口，则补最小入口说明。

### Existing files to read but not modify

- `skills/bringup-path/SKILL.md`
- `docs/templates/daisy-chain-isospi-afe-bringup-template.md`
- `docs/cases/bms-daisy-chain-afe-end-to-end-example.md`
- `docs/DESIGN_SAFETY_REVIEW.md`

### New files to create

- `docs/cases/power-board-bringup-example.md` — v6 第二份端到端功率板 bring-up 主案例文档。
- `docs/superpowers/plans/2026-04-24-un9flow-power-board-bringup-example-foundation.md` — 当前 implementation plan。

### No new scripts/workflows

本计划不新增新的脚本、数据包或 GitHub workflow。

---

### Task 1: 先创建功率板 bring-up 主案例文档主体

**Files:**
- Create: `docs/cases/power-board-bringup-example.md`
- Test: `docs/cases/power-board-bringup-example.md`

- [ ] **Step 1: 写出案例缺口清单**

```md
当前缺口：
- v6 还缺一份明显偏功率板 bring-up 的端到端示例。
- 当前仓库虽已有 bringup-path 与链路类 bring-up 模板，但缺少一个说明“安全基线 → 控制建立 → 升级判断”如何串起来的功率板样例。
- 需要先用一个范围可控的功率板场景证明 bringup-path 在功率板问题里的实际用法。
```

- [ ] **Step 2: 运行检查，确认当前还没有该案例文件**

Run: `git ls-files "docs/cases/power-board-bringup-example.md"`
Expected: 无输出

- [ ] **Step 3: 创建 `docs/cases/power-board-bringup-example.md`**

```md
# Power Board Bring-up Example

## case overview
- 系统背景:
- 当前硬件阶段:
- 初始现象:
- 为什么这是典型 bring-up 问题:

## safety baseline
- 供电条件:
- 预充条件:
- 关键联锁:
- 默认安全态:
- 禁止动作:

## bring-up path usage
- 为什么当前仍属于 `bringup-path`:
- 建立了什么 baseline:
- 哪些步骤已打通:
- 哪些步骤仍不稳定:

### bringup-baseline 摘要
- 当前安全前提:
- 当前基线结论:
- 不稳定项:

### link-qualification-log 摘要
- bring-up 步骤:
- 关键波形/状态:
- 当前记录结论:

## control establishment
- 预充完成后如何逐步建立 PWM / 驱动输出:
- 观察哪些信号:
- 如何判断“控制未建立”还是“建立了但不稳定”:

### initial-diagnosis-conclusion 摘要
- 当前判断:
- 临时限制:
- 下一步建议:

## escalation decision
- 什么时候继续留在 bring-up:
- 什么时候升级到 `incident-investigation`:
- 什么时候升级到 `design-safety-review`:

## final outcome
- 当前确认了什么:
- 哪些问题还没闭合:
- 下一步建议是什么:
```

- [ ] **Step 4: 运行最小文本检查，确认 6 个主段全部落地**

Run: `grep -n "case overview\|safety baseline\|bring-up path usage\|control establishment\|escalation decision\|final outcome" docs/cases/power-board-bringup-example.md`
Expected: 6 个主段全部命中

---

### Task 2: 给案例补最小入口说明

**Files:**
- Modify: `README.md`
- Test: `README.md`

- [ ] **Step 1: 在 `README.md` 增加案例入口**

```md
- `docs/cases/power-board-bringup-example.md`：v6 第二份功率板 bring-up 流程示例，展示安全基线、控制建立与升级判断
```

- [ ] **Step 2: 运行最小文本检查**

Run: `grep -n "power-board-bringup-example" README.md docs/cases/power-board-bringup-example.md`
Expected: README 与案例文档均命中该文件名

---

### Task 3: 同步 ROADMAP 并确认案例已被路线图与入口文档引用

**Files:**
- Modify: `docs/ROADMAP.md`
- Test: `docs/ROADMAP.md`
- Test: `README.md`
- Test: `docs/cases/power-board-bringup-example.md`

- [ ] **Step 1: 在 `docs/ROADMAP.md` 把“示例功率板 bring-up 流程”标记为已落地基线**

```md
将：
- [ ] 示例功率板 bring-up 流程

改成：
- [x] 示例功率板 bring-up 流程已落地：`docs/cases/power-board-bringup-example.md` 作为 v6 第二份端到端示例
```

- [ ] **Step 2: 运行最小文本检查，确认案例已被入口文档与路线图引用**

Run: `grep -n "power-board-bringup-example" README.md docs/ROADMAP.md docs/cases/power-board-bringup-example.md`
Expected: 3 个文件都命中该案例文件名

- [ ] **Step 3: 提交功率板 bring-up 示例基线**

```bash
git add docs/cases/power-board-bringup-example.md README.md docs/ROADMAP.md
git commit -m "feat: add power board bringup example"
```

---

## Verification Notes

- 本计划不新增脚本或专门校验器；当前目标是让 v6 第二份示例文档落地并能被入口文档与路线图发现。
- 该案例必须始终保持“功率板 bring-up 示例”定位；若实现中膨胀成完整功率电子教程或多文件案例包，必须回退。