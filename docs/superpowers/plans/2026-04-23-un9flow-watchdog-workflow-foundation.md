# Watchdog Workflow Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 un9flow 增加一个 watchdog / timeout 专项 workflow 真源文档，并把它纳入现有对象链、一致性校验与路线图语义中。

**Architecture:** 本轮不新增新的主场景、specialist 或 GitHub workflow，而是新增 `docs/WATCHDOG_TIMEOUT_WORKFLOW.md` 作为流程真源，把 checklist → pack → findings → report 的顺序、gate 和分工写死。现有 `.github/workflows/consistency-validation.yml` 继续不改结构，仍通过 `python tools/validate_consistency.py` 自动纳管新增 workflow 文档。

**Tech Stack:** Markdown, Python 3, GitHub Actions（existing）, git, Claude Code

---

## File Structure

### Existing files to modify

- `skills/watchdog-timeout-audit/SKILL.md` — 补充对 workflow 真源的回指，并说明该 workflow 默认服务关系。
- `docs/WATCHDOG_TIMEOUT_AUDIT.md` — 补充对 workflow 真源的回指，并明确方法真源与流程真源的分工。
- `docs/CONSISTENCY_VALIDATION.md` — 增加 watchdog workflow 文档的一致性规则。
- `tools/validate_consistency.py` — 增加 watchdog workflow 文档的存在性、回指和边界检查。
- `docs/ROADMAP.md` — 把“更重型 watchdog 专项 workflow”从未开始推进为已落地基线。
- `README.md`（仅当需要）— 若 workflow 文档需要对外入口，则补最小入口说明。

### Existing files to read but not modify

- `docs/templates/watchdog-timeout-audit-checklist.md`
- `docs/templates/timing-watchdog-audit-pack.md`
- `docs/templates/watchdog-timeout-audit-findings.md`
- `docs/templates/watchdog-timeout-audit-report.md`
- `tools/generate_watchdog_timeout_audit_report.py`
- `.github/workflows/consistency-validation.yml`

### New files to create

- `docs/WATCHDOG_TIMEOUT_WORKFLOW.md` — watchdog / timeout 流程真源文档。
- `docs/superpowers/plans/2026-04-23-un9flow-watchdog-workflow-foundation.md` — 当前 implementation plan。

### No new CI/workflow files

本计划不新增新的 GitHub workflow，也不引入新的执行脚本或批量流水线。

---

### Task 1: 先把 watchdog workflow 规则写成失败校验

**Files:**
- Modify: `docs/CONSISTENCY_VALIDATION.md`
- Modify: `tools/validate_consistency.py`
- Test: `tools/validate_consistency.py`

- [ ] **Step 1: 在 `docs/CONSISTENCY_VALIDATION.md` 增加 watchdog workflow 规则**

```md
在 watchdog / timeout 相关规则段下补充明确约束：

- `docs/WATCHDOG_TIMEOUT_WORKFLOW.md` 是 watchdog / timeout 的流程真源文档。
- `docs/WATCHDOG_TIMEOUT_WORKFLOW.md` 必须回指：
  - `docs/WATCHDOG_TIMEOUT_AUDIT.md`
  - `skills/watchdog-timeout-audit/SKILL.md`
  - `docs/templates/watchdog-timeout-audit-checklist.md`
  - `docs/templates/timing-watchdog-audit-pack.md`
  - `docs/templates/watchdog-timeout-audit-findings.md`
  - `docs/templates/watchdog-timeout-audit-report.md`
  - `tools/generate_watchdog_timeout_audit_report.py`
- `docs/WATCHDOG_TIMEOUT_WORKFLOW.md` 必须显式声明：
  - 不是新的主场景
  - 不是新的 `Domain Specialist`
  - 默认服务 `design-safety-review`
  - 可被 `incident-investigation` / `bringup-path` 复用
  - 固定顺序：checklist → pack → findings → report
```

- [ ] **Step 2: 在 `tools/validate_consistency.py` 增加 watchdog workflow 失败检查**

```python
# 在 docs 检查中加入 watchdog workflow 文档检查
watchdog_workflow_label = "docs/WATCHDOG_TIMEOUT_WORKFLOW.md"
watchdog_workflow_path = ROOT / "docs" / "WATCHDOG_TIMEOUT_WORKFLOW.md"
watchdog_workflow_content = _read_text(watchdog_workflow_path)
if watchdog_workflow_content is None:
    findings.append(
        Finding(
            level="L1",
            category="docs",
            file=watchdog_workflow_label,
            summary="watchdog workflow 真源文档缺失或无法读取。",
            why_it_matters="若缺少 watchdog 流程真源，checklist / pack / findings / report 之间就仍然只是对象齐全，而不是流程齐全。",
            suggested_action="创建 docs/WATCHDOG_TIMEOUT_WORKFLOW.md 并确保 UTF-8 可读。",
        )
    )
else:
    missing_watchdog_workflow_refs = _find_missing_semantics(
        watchdog_workflow_content,
        {
            "watchdog audit doc ref": "docs/WATCHDOG_TIMEOUT_AUDIT.md",
            "watchdog formal skill ref": "skills/watchdog-timeout-audit/SKILL.md",
            "watchdog checklist ref": "docs/templates/watchdog-timeout-audit-checklist.md",
            "watchdog pack ref": "docs/templates/timing-watchdog-audit-pack.md",
            "watchdog findings ref": "docs/templates/watchdog-timeout-audit-findings.md",
            "watchdog report ref": "docs/templates/watchdog-timeout-audit-report.md",
            "watchdog report generator ref": "tools/generate_watchdog_timeout_audit_report.py",
        },
    )
    if missing_watchdog_workflow_refs:
        findings.append(
            Finding(
                level="L2",
                category="docs",
                file=watchdog_workflow_label,
                summary=f"watchdog workflow 真源缺少对象回指：{', '.join(missing_watchdog_workflow_refs)}。",
                why_it_matters="若 workflow 文档不回指 watchdog 对象链，流程真源就无法稳定约束现有对象的执行顺序与分工。",
                suggested_action="在 docs/WATCHDOG_TIMEOUT_WORKFLOW.md 中补齐方法真源、formal skill、checklist、pack、findings、report 与 generator 的引用。",
            )
        )

    missing_watchdog_workflow_semantics = _find_missing_semantics(
        watchdog_workflow_content,
        {
            "not a scenario": "不是新的主场景",
            "not a domain specialist": "不是新的 `Domain Specialist`",
            "design safety review": "design-safety-review",
            "incident investigation": "incident-investigation",
            "bringup path": "bringup-path",
            "ordered flow": "checklist → pack → findings → report",
        },
    )
    if missing_watchdog_workflow_semantics:
        findings.append(
            Finding(
                level="L2",
                category="docs",
                file=watchdog_workflow_label,
                summary=f"watchdog workflow 真源缺少边界或流程语义：{', '.join(missing_watchdog_workflow_semantics)}。",
                why_it_matters="若 workflow 文档不显式声明边界、默认服务关系与固定顺序，watchdog 专项流程就无法形成单一真源。",
                suggested_action="在 docs/WATCHDOG_TIMEOUT_WORKFLOW.md 中补齐主场景/Domain Specialist 边界、design-safety-review 默认服务关系、incident/bringup 复用关系和 checklist → pack → findings → report 的固定顺序。",
            )
        )
```

- [ ] **Step 3: 运行 CLI，确认 watchdog workflow 规则先失败**

Run: `python tools/validate_consistency.py`
Expected: `Validation result: FAIL`，且至少出现指向以下对象的 findings：
- `docs/WATCHDOG_TIMEOUT_WORKFLOW.md`

---

### Task 2: 新增 workflow 真源并让校验转绿

**Files:**
- Create: `docs/WATCHDOG_TIMEOUT_WORKFLOW.md`
- Modify: `skills/watchdog-timeout-audit/SKILL.md`
- Modify: `docs/WATCHDOG_TIMEOUT_AUDIT.md`
- Test: `tools/validate_consistency.py`

- [ ] **Step 1: 创建 `docs/WATCHDOG_TIMEOUT_WORKFLOW.md`**

```md
# un9flow Watchdog Timeout Workflow

## 目标
- 把 watchdog / timeout 专项执行固定成可重复、可审查的流程骨架，而不是只保留分散对象。

## 定位与边界
- 不是新的主场景。
- 不是新的 `Domain Specialist`。
- 默认挂在 `watchdog-timeout-audit` formal skill 下。
- 默认服务 `design-safety-review`。
- 可被 `incident-investigation` 与 `bringup-path` 复用。
- 不替代主场景总路由。

## 固定输出顺序
- checklist
- pack
- findings
- report

## Phase 1: scope framing
- 输入：当前审计目标、当前风险边界、最小证据集、当前主场景语义
- 输出：checklist 起始状态、当前 audit scope

## Phase 2: specialist execution
- 执行核心：`timing-watchdog-auditor`
- 输出：`timing-watchdog-audit-pack`

## Gate A: evidence sufficiency
- 证据不足：回补证据，不进入正式报告生成
- 证据足够：进入 findings consolidation

## Phase 3: findings consolidation
- 输出：`watchdog-timeout-audit-findings`

## Phase 4: report generation
- 执行核心：`tools/generate_watchdog_timeout_audit_report.py`
- 输入：findings 为主输入，pack 为补充输入
- 输出：`watchdog-timeout-audit-report`

## Gate B: completion / escalation
- 未闭合：升级到 `incident-investigation` 或 `design-safety-review`
- 已收口：允许归档专项报告

## 相关对象回指
- 方法真源：`docs/WATCHDOG_TIMEOUT_AUDIT.md`
- formal skill：`skills/watchdog-timeout-audit/SKILL.md`
- checklist：`docs/templates/watchdog-timeout-audit-checklist.md`
- pack：`docs/templates/timing-watchdog-audit-pack.md`
- findings：`docs/templates/watchdog-timeout-audit-findings.md`
- report：`docs/templates/watchdog-timeout-audit-report.md`
- report generator：`tools/generate_watchdog_timeout_audit_report.py`
```

- [ ] **Step 2: 在 `skills/watchdog-timeout-audit/SKILL.md` 补 workflow 真源回指**

```md
在默认依赖或与真源文档关系中补充：
- 流程真源：`docs/WATCHDOG_TIMEOUT_WORKFLOW.md`
```

- [ ] **Step 3: 在 `docs/WATCHDOG_TIMEOUT_AUDIT.md` 补 workflow 真源分工说明**

```md
在关系/分工段补充：
- 流程真源：`docs/WATCHDOG_TIMEOUT_WORKFLOW.md`
- `docs/WATCHDOG_TIMEOUT_AUDIT.md` 负责回答“审什么”。
- `docs/WATCHDOG_TIMEOUT_WORKFLOW.md` 负责回答“怎么跑”。
```

- [ ] **Step 4: 运行 CLI，确认 watchdog workflow 校验通过**

Run: `python tools/validate_consistency.py`
Expected: `Validation result: PASS`

---

### Task 3: 同步路线图并把 workflow 真源纳入现有门禁语义

**Files:**
- Modify: `docs/ROADMAP.md`
- Modify: `README.md`（如需入口）
- Test: `docs/ROADMAP.md`
- Test: `README.md`
- Test: `tools/validate_consistency.py`

- [ ] **Step 1: 在 `docs/ROADMAP.md` 把 watchdog workflow 标记为已落地基线**

```md
将：
- [ ] 更重型 watchdog 专项 workflow 仍留待后续阶段扩展

改成：
- [x] 更重型 watchdog 专项 workflow 已落地：`docs/WATCHDOG_TIMEOUT_WORKFLOW.md` 已把 checklist → pack → findings → report 固定为专项执行骨架
```

- [ ] **Step 2: 如需要，在 `README.md` 增加 workflow 真源入口**

```md
- `docs/WATCHDOG_TIMEOUT_WORKFLOW.md`：watchdog / timeout 专项执行流程真源，固定 checklist → pack → findings → report 的顺序与 gate
```

- [ ] **Step 3: 运行最小文本检查**

Run: `grep -n "WATCHDOG_TIMEOUT_WORKFLOW" README.md docs/ROADMAP.md docs/WATCHDOG_TIMEOUT_AUDIT.md docs/WATCHDOG_TIMEOUT_WORKFLOW.md skills/watchdog-timeout-audit/SKILL.md`
Expected: 若 README 被修改，则 5 个文件都命中；若 README 未修改，则其余 4 个文件命中且 `ROADMAP` 已更新

- [ ] **Step 4: 再跑一次 consistency CLI，确认现有门禁已覆盖新增 workflow 文档**

Run: `python tools/validate_consistency.py`
Expected: `Validation result: PASS`

- [ ] **Step 5: 提交本轮 watchdog workflow 基线**

```bash
git add docs/WATCHDOG_TIMEOUT_WORKFLOW.md docs/WATCHDOG_TIMEOUT_AUDIT.md docs/CONSISTENCY_VALIDATION.md docs/ROADMAP.md README.md skills/watchdog-timeout-audit/SKILL.md tools/validate_consistency.py
git commit -m "feat: add watchdog workflow"
```

---

## Verification Notes

- 本计划不新增新的 GitHub workflow；本轮目标是新增 watchdog 流程真源并纳入现有 consistency / CI。
- `WATCHDOG_TIMEOUT_WORKFLOW.md` 必须始终保持“流程真源”定位，不替代方法真源、specialist 或主场景总路由。
- 若实现中把 workflow 写成新的主场景或新的 `Domain Specialist`，必须回退。