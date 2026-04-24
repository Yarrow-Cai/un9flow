# BMS End-to-End Example Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 un9flow 增加第一份 v6 端到端 BMS 方法链示例，使用一个“菊花链 AFE 首次拉通后节点枚举不稳定”的场景串起 bring-up → incident → watchdog → design-safety-review。

**Architecture:** 本轮不拆成大量案例文件，而是新增一个主案例文档 `docs/cases/bms-daisy-chain-afe-end-to-end-example.md`，用正文串起方法链切换，并在文中嵌入关键 artifact 摘要块。当前 `.github/workflows/consistency-validation.yml` 不改结构，且本轮默认不为该示例增加新的专门校验器；目标是先让 v6 第一份示例具备可阅读、可展示、可归档的最低完整度。

**Tech Stack:** Markdown, git, Claude Code

---

## File Structure

### Existing files to modify

- `docs/ROADMAP.md` — 把“示例 BMS 方法论用法”从未开始推进为已落地基线。
- `README.md`（如需入口）— 若该示例需要对外可发现入口，则补最小入口说明。

### Existing files to read but not modify

- `skills/bringup-path/SKILL.md`
- `skills/incident-investigation/SKILL.md`
- `skills/watchdog-timeout-audit/SKILL.md`
- `docs/DESIGN_SAFETY_REVIEW.md`
- `docs/templates/daisy-chain-isospi-afe-bringup-template.md`
- `docs/templates/watchdog-timeout-audit-findings.md`
- `docs/templates/watchdog-timeout-audit-report.md`
- `docs/cases/incident-workflow-routing-regression.md`
- `docs/cases/incident-workflow-dispatch-regression.md`

### New files to create

- `docs/cases/bms-daisy-chain-afe-end-to-end-example.md` — v6 第一份端到端 BMS 方法链主案例文档。
- `docs/superpowers/plans/2026-04-24-un9flow-bms-end-to-end-example-foundation.md` — 当前 implementation plan。

### No new scripts/workflows

本计划不新增新的脚本、报告生成器或 GitHub workflow。

---

### Task 1: 先创建端到端主案例文档主体

**Files:**
- Create: `docs/cases/bms-daisy-chain-afe-end-to-end-example.md`
- Test: `docs/cases/bms-daisy-chain-afe-end-to-end-example.md`

- [ ] **Step 1: 写出案例缺口清单**

```md
当前缺口：
- v6 还没有真正意义上的端到端方法链示例。
- 当前仓库虽已有 bring-up / incident / watchdog / design-safety-review 对象，但缺少一份能说明“何时切场景、何时切专项、每一步产出什么”的完整样例。
- 需要先用一个足够真实、足够小的 BMS 场景把方法链串起来。
```

- [ ] **Step 2: 运行检查，确认当前还没有该案例文件**

Run: `git ls-files "docs/cases/bms-daisy-chain-afe-end-to-end-example.md"`
Expected: 无输出

- [ ] **Step 3: 创建 `docs/cases/bms-daisy-chain-afe-end-to-end-example.md`**

```md
# BMS Daisy-Chain AFE End-to-End Example

## case overview
- 系统背景:
- 当前硬件阶段:
- 初始现象:
- 为什么这是个典型 BMS 问题:

## bring-up path usage
- 为什么先走 `bringup-path`:
- 使用的输入:
- 建立的基线:
- 哪些信号说明问题已超出纯 bring-up 动作:

### bringup-baseline 摘要
- 关键 bring-up 条件:
- 关键观测点:
- 当前结论:

### link-qualification-log 摘要
- 建链步骤:
- 枚举结果:
- 不稳定现象:

## incident handoff
- 为什么升级到 `incident-investigation`:
- evidence 如何被整理:
- 进入的 specialist:

## watchdog / timeout specialty
- 为什么进入 `watchdog-timeout-audit`:
- findings 如何形成:
- report 如何收口:

### watchdog-timeout-audit-findings 摘要
- finding-001:
- finding-002:

### watchdog-timeout-audit-report 摘要
- audit summary:
- key findings:
- recommended actions:

## design safety review handoff
- 为什么问题已触到设计边界:
- 哪些内容进入 `design-safety-review`:
- 如何解释风险边界与收敛策略:

### risk-boundary-note 摘要
- 当前风险边界:
- 已确认项:
- 未确认项:

## final outcome
- 当前确认了什么:
- 仍未确认什么:
- 下一步建议是什么:
- 这条方法链证明了什么:
```

- [ ] **Step 4: 运行最小文本检查，确认 6 个主段全部落地**

Run: `grep -n "case overview\|bring-up path usage\|incident handoff\|watchdog / timeout specialty\|design safety review handoff\|final outcome" docs/cases/bms-daisy-chain-afe-end-to-end-example.md`
Expected: 6 个主段全部命中

---

### Task 2: 给案例补最小入口说明

**Files:**
- Modify: `README.md`
- Test: `README.md`

- [ ] **Step 1: 在 `README.md` 增加案例入口**

```md
- `docs/cases/bms-daisy-chain-afe-end-to-end-example.md`：v6 第一份端到端 BMS 方法链示例，串起 bring-up → incident → watchdog → design-safety-review
```

- [ ] **Step 2: 运行最小文本检查**

Run: `grep -n "bms-daisy-chain-afe-end-to-end-example" README.md docs/cases/bms-daisy-chain-afe-end-to-end-example.md`
Expected: README 与案例文档均命中该文件名

---

### Task 3: 同步 ROADMAP 并确认案例已被路线图与入口文档引用

**Files:**
- Modify: `docs/ROADMAP.md`
- Test: `docs/ROADMAP.md`
- Test: `README.md`
- Test: `docs/cases/bms-daisy-chain-afe-end-to-end-example.md`

- [ ] **Step 1: 在 `docs/ROADMAP.md` 把“示例 BMS 方法论用法”标记为已落地基线**

```md
将：
- [ ] 示例 BMS 方法论用法

改成：
- [x] 示例 BMS 方法论用法已落地：`docs/cases/bms-daisy-chain-afe-end-to-end-example.md` 作为 v6 第一份端到端示例
```

- [ ] **Step 2: 运行最小文本检查，确认案例已被入口文档与路线图引用**

Run: `grep -n "bms-daisy-chain-afe-end-to-end-example" README.md docs/ROADMAP.md docs/cases/bms-daisy-chain-afe-end-to-end-example.md`
Expected: 3 个文件都命中该案例文件名

- [ ] **Step 3: 提交 BMS 端到端示例基线**

```bash
git add docs/cases/bms-daisy-chain-afe-end-to-end-example.md README.md docs/ROADMAP.md
git commit -m "feat: add bms end-to-end example"
```

---

## Verification Notes

- 本计划不新增脚本或专门校验器；当前目标是让 v6 第一份示例文档落地并能被入口文档与路线图发现。
- 该案例必须始终保持“端到端方法链示例”定位；若实现中膨胀成完整系统文档、培训教材或十几个独立案例包，必须回退。