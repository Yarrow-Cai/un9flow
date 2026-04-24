# Fault Injection Report Example Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 un9flow 增加一份 incident 语义的故障注入报告示例，展示注入目标、观察行为、evidence 收口、watchdog findings / report 收口以及结论边界。

**Architecture:** 本轮不构建实验数据库或自动化故障注入平台，而是新增一个主案例文档 `docs/cases/fault-injection-report-example.md`，用正文串起“注入 → 观察 → incident 解释 → watchdog 专项收口 → 结论边界”。当前 `.github/workflows/consistency-validation.yml` 不改结构，且本轮默认不为该示例增加新的专门校验器；目标是先让 v6 下一份示例具备可阅读、可展示、可归档的最低完整度。

**Tech Stack:** Markdown, git, Claude Code

---

## File Structure

### Existing files to modify

- `docs/ROADMAP.md` — 把“示例故障注入报告”从未开始推进为已落地基线。
- `README.md`（如需入口）— 若该示例需要对外可发现入口，则补最小入口说明。

### Existing files to read but not modify

- `skills/incident-investigation/SKILL.md`
- `skills/watchdog-timeout-audit/SKILL.md`
- `docs/templates/watchdog-timeout-audit-findings.md`
- `docs/templates/watchdog-timeout-audit-report.md`
- `tools/generate_watchdog_timeout_audit_report.py`
- `docs/cases/bms-daisy-chain-afe-end-to-end-example.md`
- `docs/cases/power-board-bringup-example.md`

### New files to create

- `docs/cases/fault-injection-report-example.md` — incident 语义的故障注入报告主案例文档。
- `docs/superpowers/plans/2026-04-24-un9flow-fault-injection-report-example-foundation.md` — 当前 implementation plan。

### No new scripts/workflows

本计划不新增新的脚本、实验数据库或 GitHub workflow。

---

### Task 1: 先创建故障注入报告主案例文档主体

**Files:**
- Create: `docs/cases/fault-injection-report-example.md`
- Test: `docs/cases/fault-injection-report-example.md`

- [ ] **Step 1: 写出案例缺口清单**

```md
当前缺口：
- v6 还没有一份明确偏故障注入结果收口的示例。
- 当前仓库虽已有 incident / watchdog / findings / report / generator，但缺少一份说明“注入了什么、观察到什么、如何收口”的报告型案例。
- 需要先用一个范围可控的注入场景证明 evidence → specialist → findings → report 的收口链条是可用的。
```

- [ ] **Step 2: 运行检查，确认当前还没有该案例文件**

Run: `git ls-files "docs/cases/fault-injection-report-example.md"`
Expected: 无输出

- [ ] **Step 3: 创建 `docs/cases/fault-injection-report-example.md`**

```md
# Fault Injection Report Example

## case overview
- 被测对象:
- 注入目标:
- 初始风险假设:
- 为什么做这次故障注入:

## injection setup
- 注入方式:
- 注入时机:
- 注入范围:
- 当前约束与安全边界:
- 停止条件:
- 最小复现实验骨架:
  - 注入执行入口:
  - 时间基准对齐:
  - 观察窗口:
  - 恢复 / 未恢复 / 需要升级的判定门槛:

## observed behavior
- timeout:
- 重试:
- 节点失联:
- reset:
- watchdog 行为:
- 是否进入安全态:

### evidence-package 摘要
- 输入证据:
- 时间窗口:
- 关键观测:

## incident interpretation
- 为什么它属于 `incident-investigation`:
- evidence 如何整理:
- 哪些 specialist 被调用:
- 哪些初始假设被保留或排除:

## watchdog / report synthesis
- findings 如何形成:
- report 如何收口:
- 哪些风险已确认:
- 哪些风险仍未闭合:

### watchdog-timeout-audit-findings 摘要
- finding-001:
- finding-002:

### watchdog-timeout-audit-report 摘要
- audit summary:
- key findings:
- recommended actions:

## final outcome
- 本次故障注入证明了什么:
- 哪些边界被验证了:
- 哪些地方还需要补试验:
- 下一步建议是什么:
```

- [ ] **Step 4: 运行最小文本检查，确认 6 个主段全部落地**

Run: `grep -n "case overview\|injection setup\|observed behavior\|incident interpretation\|watchdog / report synthesis\|final outcome" docs/cases/fault-injection-report-example.md`
Expected: 6 个主段全部命中

---

### Task 2: 给案例补最小入口说明

**Files:**
- Modify: `README.md`
- Test: `README.md`

- [ ] **Step 1: 在 `README.md` 增加案例入口**

```md
- `docs/cases/fault-injection-report-example.md`：incident 语义的故障注入报告示例，展示注入、观察、findings / report 收口与结论边界
```

- [ ] **Step 2: 运行最小文本检查**

Run: `grep -n "fault-injection-report-example" README.md docs/cases/fault-injection-report-example.md`
Expected: README 命中，案例文件存在并可读取；若案例文档正文顺带命中该文件名也可接受，但不作为必须条件。

---

### Task 3: 同步 ROADMAP 并确认案例已被路线图与入口文档引用

**Files:**
- Modify: `docs/ROADMAP.md`
- Test: `docs/ROADMAP.md`
- Test: `README.md`
- Test: `docs/cases/fault-injection-report-example.md`

- [ ] **Step 1: 在 `docs/ROADMAP.md` 把“示例故障注入报告”标记为已落地基线**

```md
将：
- [ ] 示例故障注入报告

改成：
- [x] 示例故障注入报告已落地：`docs/cases/fault-injection-report-example.md` 作为 incident 语义的报告型示例
```

- [ ] **Step 2: 运行最小文本检查，确认案例已被入口文档与路线图引用**

Run: `grep -n "fault-injection-report-example" README.md docs/ROADMAP.md docs/cases/fault-injection-report-example.md`
Expected: README 与 ROADMAP 命中；案例文件存在并可读取。若案例文档正文顺带命中该文件名也可接受，但不作为必须条件。

- [ ] **Step 3: 提交故障注入报告示例基线**

```bash
git add docs/cases/fault-injection-report-example.md README.md docs/ROADMAP.md
git commit -m "feat: add fault injection report example"
```

---

## Verification Notes

- 本计划不新增脚本或实验数据库；当前目标是让 incident 语义的故障注入报告示例落地并能被入口文档与路线图发现。
- 该案例必须始终保持“报告型示例”定位；若实现中膨胀成完整测试计划、safety case 或大量原始实验文件，必须回退。