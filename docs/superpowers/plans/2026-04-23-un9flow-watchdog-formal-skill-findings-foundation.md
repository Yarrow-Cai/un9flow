# Watchdog Formal Skill Findings Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 un9flow 补齐 watchdog / timeout 正式专项 skill、findings 模板，以及它们与方法真源、一致性校验、路线图之间的最小闭环。

**Architecture:** 本轮继续沿 docs 为主真源的路线推进：先新增 watchdog formal skill 和 findings 模板，再把 `docs/WATCHDOG_TIMEOUT_AUDIT.md`、`docs/CONSISTENCY_VALIDATION.md` 与 `tools/validate_consistency.py` 扩展到能识别它们。现有 `.github/workflows/consistency-validation.yml` 不改结构，继续通过运行 `python tools/validate_consistency.py` 把新对象自动纳入 PR / main 门禁。

**Tech Stack:** Markdown, Python 3, GitHub Actions（existing）, git, Claude Code

---

## File Structure

### Existing files to modify

- `docs/WATCHDOG_TIMEOUT_AUDIT.md` — 补充对 watchdog formal skill 与 findings 的回指，并固定方法真源 / skill / findings / pack / checklist 的分工关系。
- `docs/CONSISTENCY_VALIDATION.md` — 增加 watchdog formal skill 与 findings 的一致性规则。
- `tools/validate_consistency.py` — 增加 watchdog formal skill 与 findings 模板的存在性、回指和边界检查。
- `docs/ROADMAP.md` — 把 v5 中“正式 skill / findings / CI 集成”收窄成已落地基线或更精确的剩余项。
- `README.md`（仅当需要）— 若新增对象需要对外入口，则补最小入口说明。
- `docs/DESIGN_SAFETY_REVIEW.md`（仅当需要）— 若 formal skill 需要在主场景文档中显式挂接，再做最小补充。

### Existing files to read but not modify

- `skills/timing-watchdog-auditor/SKILL.md` — watchdog 相关 `Domain Specialist` skill，继续作为执行核心。
- `docs/templates/timing-watchdog-audit-pack.md` — 完整 specialist 输出模板。
- `docs/templates/watchdog-timeout-audit-checklist.md` — watchdog 专项 checklist。
- `.github/workflows/consistency-validation.yml` — 现有最小门禁 workflow，本计划不改变其结构。

### New files to create

- `skills/watchdog-timeout-audit/SKILL.md` — watchdog / timeout 正式专项 skill。
- `docs/templates/watchdog-timeout-audit-findings.md` — watchdog / timeout 轻量 findings 模板。
- `docs/superpowers/plans/2026-04-23-un9flow-watchdog-formal-skill-findings-foundation.md` — 当前 implementation plan。

### No new CI/workflow files

本计划不新增新的 GitHub workflow，也不新增独立 watchdog 报告生成器。

---

### Task 1: 先把 watchdog formal skill 与 findings 规则写成失败校验

**Files:**
- Modify: `docs/CONSISTENCY_VALIDATION.md`
- Modify: `tools/validate_consistency.py`
- Test: `tools/validate_consistency.py`

- [ ] **Step 1: 在 `docs/CONSISTENCY_VALIDATION.md` 增加 watchdog formal skill / findings 规则**

```md
在 watchdog / timeout 相关规则段下补充明确约束：

- `skills/watchdog-timeout-audit/SKILL.md` 是 watchdog / timeout 的正式专项 skill 入口，不作为新的主场景，也不作为新的 `Domain Specialist`。
- `skills/watchdog-timeout-audit/SKILL.md` 必须回指：
  - `docs/WATCHDOG_TIMEOUT_AUDIT.md`
  - `docs/templates/timing-watchdog-audit-pack.md`
  - `docs/templates/watchdog-timeout-audit-findings.md`
- `docs/templates/watchdog-timeout-audit-findings.md` 是 watchdog / timeout 的轻量 findings 模板。
- `docs/templates/watchdog-timeout-audit-findings.md` 必须回指：
  - `docs/WATCHDOG_TIMEOUT_AUDIT.md`
  - `skills/watchdog-timeout-audit/SKILL.md`
- `docs/WATCHDOG_TIMEOUT_AUDIT.md` 必须补充对 watchdog formal skill 与 findings 的回指。
```

- [ ] **Step 2: 在 `tools/validate_consistency.py` 增加 watchdog formal skill / findings 失败检查**

```python
# 在 check_skills() 中加入 watchdog formal skill 文件存在性与边界检查
watchdog_formal_label = "skills/watchdog-timeout-audit/SKILL.md"
watchdog_formal_path = ROOT / "skills" / "watchdog-timeout-audit" / "SKILL.md"
watchdog_formal_content = _read_text(watchdog_formal_path)
if watchdog_formal_content is None:
    findings.append(
        Finding(
            level="L1",
            category="skills",
            file=watchdog_formal_label,
            summary="watchdog formal skill 缺失或无法读取。",
            why_it_matters="若 watchdog / timeout 没有正式专项 skill 入口，v5 的 formal skill / findings / CI 集成就无法落地。",
            suggested_action="创建 skills/watchdog-timeout-audit/SKILL.md 并确保 UTF-8 可读。",
        )
    )
else:
    missing_watchdog_formal_refs = _find_missing_semantics(
        watchdog_formal_content,
        {
            "watchdog method ref": "docs/WATCHDOG_TIMEOUT_AUDIT.md",
            "watchdog pack ref": "docs/templates/timing-watchdog-audit-pack.md",
            "watchdog findings ref": "docs/templates/watchdog-timeout-audit-findings.md",
        },
    )
    if missing_watchdog_formal_refs:
        findings.append(
            Finding(
                level="L2",
                category="skills",
                file=watchdog_formal_label,
                summary=f"watchdog formal skill 缺少真源或模板回指：{', '.join(missing_watchdog_formal_refs)}。",
                why_it_matters="formal skill 若不回指方法真源、pack 与 findings，专项入口与收口物之间就无法形成闭环。",
                suggested_action="在 skills/watchdog-timeout-audit/SKILL.md 中补齐对 WATCHDOG_TIMEOUT_AUDIT、timing-watchdog-audit-pack 和 watchdog-timeout-audit-findings 的引用。",
            )
        )

    has_not_scenario = "不是新的主场景" in watchdog_formal_content or "不作为新的主场景" in watchdog_formal_content
    has_not_specialist = "不是新的 `Domain Specialist`" in watchdog_formal_content or "不作为新的 `Domain Specialist`" in watchdog_formal_content or "不是新的 Domain Specialist" in watchdog_formal_content
    if not (has_not_scenario and has_not_specialist):
        findings.append(
            Finding(
                level="L2",
                category="skills",
                file=watchdog_formal_label,
                summary="watchdog formal skill 缺少主场景 / specialist 边界声明。",
                why_it_matters="若不明确声明 watchdog formal skill 不是新的主场景且不是新的 Domain Specialist，入口层和 specialist 层就会混层。",
                suggested_action="在 skills/watchdog-timeout-audit/SKILL.md 中明确声明其不是新的主场景，也不是新的 Domain Specialist。",
            )
        )

# 在 check_templates() 中加入 watchdog findings 模板检查
watchdog_findings_label = "docs/templates/watchdog-timeout-audit-findings.md"
watchdog_findings_path = ROOT / "docs" / "templates" / "watchdog-timeout-audit-findings.md"
watchdog_findings_content = _read_text(watchdog_findings_path)
if watchdog_findings_content is None:
    findings.append(
        Finding(
            level="L1",
            category="templates",
            file=watchdog_findings_label,
            summary="watchdog findings 模板缺失或无法读取。",
            why_it_matters="若 watchdog / timeout 没有轻量 findings 模板，专项问题清单就无法稳定落表，也无法被 consistency / CI 纳管。",
            suggested_action="创建 docs/templates/watchdog-timeout-audit-findings.md 并确保 UTF-8 可读。",
        )
    )
else:
    missing_watchdog_findings_refs = _find_missing_semantics(
        watchdog_findings_content,
        {
            "watchdog method ref": "docs/WATCHDOG_TIMEOUT_AUDIT.md",
            "watchdog formal skill ref": "skills/watchdog-timeout-audit/SKILL.md",
        },
    )
    if missing_watchdog_findings_refs:
        findings.append(
            Finding(
                level="L2",
                category="templates",
                file=watchdog_findings_label,
                summary=f"watchdog findings 模板缺少方法真源或 formal skill 回指：{', '.join(missing_watchdog_findings_refs)}。",
                why_it_matters="若 findings 模板不回指方法真源与 formal skill，专项入口、方法边界与问题清单就无法形成单一真源关系。",
                suggested_action="在 docs/templates/watchdog-timeout-audit-findings.md 中补齐对 WATCHDOG_TIMEOUT_AUDIT 与 skills/watchdog-timeout-audit/SKILL.md 的引用。",
            )
        )

# 在 check_docs() 中加入 WATCHDOG_TIMEOUT_AUDIT 对 formal skill/findings 的回指检查
if watchdog_timeout_content is not None:
    missing_watchdog_formal_doc_refs = _find_missing_semantics(
        watchdog_timeout_content,
        {
            "watchdog formal skill ref": "skills/watchdog-timeout-audit/SKILL.md",
            "watchdog findings ref": "docs/templates/watchdog-timeout-audit-findings.md",
        },
    )
    if missing_watchdog_formal_doc_refs:
        findings.append(
            Finding(
                level="L2",
                category="docs",
                file=watchdog_timeout_label,
                summary=f"watchdog 方法真源缺少 formal skill / findings 回指：{', '.join(missing_watchdog_formal_doc_refs)}。",
                why_it_matters="方法真源若不回指 formal skill 与 findings，watchdog 专项入口和轻量收口物就无法被稳定约束。",
                suggested_action="在 docs/WATCHDOG_TIMEOUT_AUDIT.md 中补齐对 skills/watchdog-timeout-audit/SKILL.md 和 docs/templates/watchdog-timeout-audit-findings.md 的引用。",
            )
        )
```

- [ ] **Step 3: 运行 CLI，确认 watchdog formal skill / findings 规则先失败**

Run: `python tools/validate_consistency.py`
Expected: `Validation result: FAIL`，且至少出现指向以下对象的 findings：
- `skills/watchdog-timeout-audit/SKILL.md`
- `docs/templates/watchdog-timeout-audit-findings.md`
- `docs/WATCHDOG_TIMEOUT_AUDIT.md`

---

### Task 2: 新增 watchdog formal skill 与 findings 模板并让校验转绿

**Files:**
- Create: `skills/watchdog-timeout-audit/SKILL.md`
- Create: `docs/templates/watchdog-timeout-audit-findings.md`
- Modify: `docs/WATCHDOG_TIMEOUT_AUDIT.md`
- Test: `tools/validate_consistency.py`

- [ ] **Step 1: 创建 `skills/watchdog-timeout-audit/SKILL.md`**

```md
---
name: watchdog-timeout-audit
description: Run focused watchdog and timeout audits as a formal watchdog specialty entry without acting as a new scenario or domain specialist.
---

# watchdog-timeout-audit

## 目标
- 面向 watchdog / timeout 专项审计，快速收口时间保护、喂狗路径、阻塞风险、reset 链与 failsafe 收敛问题。

## 适用边界
- 适用于当前已知主要问题集中在 timeout / watchdog / reset / feed-path / blocking / starvation 风险时。
- 默认首先服务 `design-safety-review`。
- 不作为新的主场景，不参与总路由竞争。
- 不是新的 `Domain Specialist`，不替代 `timing-watchdog-auditor`。

## 最小输入要求
- 当前审计对象说明
- timeout / watchdog 相关设计或实现信息
- reset / 卡顿 / 调度异常相关证据
- 当前风险边界

## 默认依赖
- 专项方法真源：`docs/WATCHDOG_TIMEOUT_AUDIT.md`
- 执行核心：`skills/timing-watchdog-auditor/SKILL.md`
- 完整输出模板：`docs/templates/timing-watchdog-audit-pack.md`
- 轻量 findings 模板：`docs/templates/watchdog-timeout-audit-findings.md`

## 输出
- `timing-watchdog-audit-pack`
- `watchdog-timeout-audit-findings`

## 不负责什么
- 不作为新的主场景
- 不作为新的 `Domain Specialist`
- 不替代 `incident-investigation`
- 不直接给出系统级根因裁决
```

- [ ] **Step 2: 创建 `docs/templates/watchdog-timeout-audit-findings.md`**

```md
# watchdog-timeout-audit-findings

- 方法真源：`docs/WATCHDOG_TIMEOUT_AUDIT.md`
- formal skill：`skills/watchdog-timeout-audit/SKILL.md`

## audit scope
- 项目/模块:
- 审计对象版本:
- 审计时间:
- 审计人:
- 备注:

## findings

### finding-001
- section / audit dimension:
- finding:
- evidence:
- risk:
- severity:
- blocking:
- next action:
- owner:
- verification status:
```

- [ ] **Step 3: 在 `docs/WATCHDOG_TIMEOUT_AUDIT.md` 补 formal skill / findings 回指与分工说明**

```md
在“与 specialist / 模板 / 主场景的关系”段补充：
- 正式专项 skill：`skills/watchdog-timeout-audit/SKILL.md`
- 轻量 findings 模板：`docs/templates/watchdog-timeout-audit-findings.md`

并补充分工：
- `docs/templates/watchdog-timeout-audit-checklist.md` 负责逐项审计执行提示。
- `docs/templates/timing-watchdog-audit-pack.md` 负责完整 specialist 输出。
- `docs/templates/watchdog-timeout-audit-findings.md` 负责专项问题清单化收口。
```

- [ ] **Step 4: 运行 CLI，确认 watchdog formal skill / findings 校验通过**

Run: `python tools/validate_consistency.py`
Expected: `Validation result: PASS`

---

### Task 3: 同步路线图并把 formal skill / findings 纳入现有门禁语义

**Files:**
- Modify: `docs/ROADMAP.md`
- Modify: `README.md`（如需入口）
- Test: `docs/ROADMAP.md`
- Test: `README.md`
- Test: `tools/validate_consistency.py`

- [ ] **Step 1: 在 `docs/ROADMAP.md` 收窄 watchdog 未完成项或标记已落地基线**

```md
将：
- [ ] 看门狗与超时策略正式 skill / findings / CI 集成留待后续阶段扩展

改成更精确状态，例如：
- [x] 看门狗与超时策略 formal skill / findings 基线已落地：`skills/watchdog-timeout-audit/SKILL.md` 与 `docs/templates/watchdog-timeout-audit-findings.md` 已纳入现有 consistency / CI 门禁
- [ ] 更重型 watchdog 专项 workflow / 自动报告能力留待后续阶段扩展
```

- [ ] **Step 2: 如需要，在 `README.md` 增加 watchdog formal skill / findings 入口**

```md
- `skills/watchdog-timeout-audit/SKILL.md`：watchdog / timeout 正式专项 skill 入口（非主场景、非 Domain Specialist）
- `docs/templates/watchdog-timeout-audit-findings.md`：watchdog / timeout 轻量 findings 模板
```

- [ ] **Step 3: 运行最小文本检查**

Run: `grep -n "watchdog-timeout-audit" README.md docs/ROADMAP.md docs/WATCHDOG_TIMEOUT_AUDIT.md skills/watchdog-timeout-audit/SKILL.md docs/templates/watchdog-timeout-audit-findings.md`
Expected: 若 README 被修改，则 5 个文件都命中；若 README 未修改，则其余 4 个文件命中且 `ROADMAP` 已更新

- [ ] **Step 4: 再跑一次 consistency CLI，确认现有门禁已覆盖新增对象**

Run: `python tools/validate_consistency.py`
Expected: `Validation result: PASS`

- [ ] **Step 5: 提交本轮 formal skill / findings 基线**

```bash
git add docs/WATCHDOG_TIMEOUT_AUDIT.md docs/CONSISTENCY_VALIDATION.md docs/ROADMAP.md README.md skills/watchdog-timeout-audit/SKILL.md docs/templates/watchdog-timeout-audit-findings.md tools/validate_consistency.py
git commit -m "feat: add watchdog formal skill findings"
```

---

## Verification Notes

- 本计划不新增 GitHub workflow；CI 集成的实现方式就是让现有 `consistency-validation.yml` 通过扩展后的 `tools/validate_consistency.py` 覆盖新对象。
- findings 模板只做轻量问题清单，不替代 `timing-watchdog-audit-pack.md`。
- formal skill 明确不是新的主场景，也不是新的 `Domain Specialist`；若实现中出现这类漂移，必须回退。