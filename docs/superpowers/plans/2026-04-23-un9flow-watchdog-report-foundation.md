# Watchdog Report Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 un9flow 补齐 watchdog / timeout 自动报告模板，并把它纳入现有方法真源、一致性校验与路线图语义中。

**Architecture:** 本轮不做新的 workflow 或自动裁决器，只新增 `watchdog-timeout-audit-report` 模板，再把 `docs/WATCHDOG_TIMEOUT_AUDIT.md`、`docs/CONSISTENCY_VALIDATION.md` 与 `tools/validate_consistency.py` 扩展到能识别这个最终报告载体。现有 `.github/workflows/consistency-validation.yml` 继续不改结构，仍通过 `python tools/validate_consistency.py` 自动纳管新增对象。

**Tech Stack:** Markdown, Python 3, GitHub Actions（existing）, git, Claude Code

---

## File Structure

### Existing files to modify

- `docs/WATCHDOG_TIMEOUT_AUDIT.md` — 补充对 watchdog report 模板的回指，并固定 checklist / findings / pack / report 的分工关系。
- `docs/CONSISTENCY_VALIDATION.md` — 增加 watchdog report 模板的一致性规则。
- `tools/validate_consistency.py` — 增加 watchdog report 模板的存在性、回指与结构检查。
- `docs/ROADMAP.md` — 把“更重型 watchdog 专项 workflow / 自动报告能力”收窄成已落地自动报告基线与剩余项。
- `README.md`（仅当需要）— 若 watchdog report 模板需要对外入口，则补最小入口说明。

### Existing files to read but not modify

- `skills/watchdog-timeout-audit/SKILL.md` — watchdog formal skill，继续作为 watchdog 专项入口。
- `docs/templates/watchdog-timeout-audit-findings.md` — watchdog 轻量 findings 模板，作为主输入。
- `docs/templates/timing-watchdog-audit-pack.md` — 完整 specialist 输出模板，作为补充输入。
- `docs/templates/watchdog-timeout-audit-checklist.md` — 继续承担执行提示，不作为自动报告主输入。
- `.github/workflows/consistency-validation.yml` — 现有最小门禁 workflow，本计划不改变其结构。

### New files to create

- `docs/templates/watchdog-timeout-audit-report.md` — watchdog / timeout 自动报告模板。
- `docs/superpowers/plans/2026-04-23-un9flow-watchdog-report-foundation.md` — 当前 implementation plan。

### No new CI/workflow files

本计划不新增新的 GitHub workflow，也不新增自动风险判定器或报告生成脚本。

---

### Task 1: 先把 watchdog report 规则写成失败校验

**Files:**
- Modify: `docs/CONSISTENCY_VALIDATION.md`
- Modify: `tools/validate_consistency.py`
- Test: `tools/validate_consistency.py`

- [ ] **Step 1: 在 `docs/CONSISTENCY_VALIDATION.md` 增加 watchdog report 规则**

```md
在 watchdog / timeout 相关规则段下补充明确约束：

- `docs/templates/watchdog-timeout-audit-report.md` 是 watchdog / timeout 的最终专项报告模板。
- `docs/templates/watchdog-timeout-audit-report.md` 必须回指：
  - `docs/WATCHDOG_TIMEOUT_AUDIT.md`
  - `docs/templates/watchdog-timeout-audit-findings.md`
  - `docs/templates/timing-watchdog-audit-pack.md`
- `docs/templates/watchdog-timeout-audit-report.md` 必须包含固定结构段：
  - `audit summary`
  - `key findings`
  - `evidence highlights`
  - `risk assessment`
  - `recommended actions`
  - `verification gaps`
- `docs/WATCHDOG_TIMEOUT_AUDIT.md` 必须补充对 watchdog report 模板的回指。
```

- [ ] **Step 2: 在 `tools/validate_consistency.py` 增加 watchdog report 失败检查**

```python
# 在 check_templates() 中加入 watchdog report 模板检查
watchdog_report_label = "docs/templates/watchdog-timeout-audit-report.md"
watchdog_report_path = ROOT / "docs" / "templates" / "watchdog-timeout-audit-report.md"
watchdog_report_content = _read_text(watchdog_report_path)
if watchdog_report_content is None:
    findings.append(
        Finding(
            level="L1",
            category="templates",
            file=watchdog_report_label,
            summary="watchdog report 模板缺失或无法读取。",
            why_it_matters="若 watchdog / timeout 没有最终专项报告模板，专项输出就无法从 findings / pack 进一步收口成可归档的报告载体。",
            suggested_action="创建 docs/templates/watchdog-timeout-audit-report.md 并确保 UTF-8 可读。",
        )
    )
else:
    missing_watchdog_report_refs = _find_missing_semantics(
        watchdog_report_content,
        {
            "watchdog method ref": "docs/WATCHDOG_TIMEOUT_AUDIT.md",
            "watchdog findings ref": "docs/templates/watchdog-timeout-audit-findings.md",
            "watchdog pack ref": "docs/templates/timing-watchdog-audit-pack.md",
        },
    )
    if missing_watchdog_report_refs:
        findings.append(
            Finding(
                level="L2",
                category="templates",
                file=watchdog_report_label,
                summary=f"watchdog report 模板缺少方法真源或输入模板回指：{', '.join(missing_watchdog_report_refs)}。",
                why_it_matters="若 report 模板不回指方法真源、findings 与 pack，自动报告对象就无法被稳定映射到现有 watchdog 闭环上。",
                suggested_action="在 docs/templates/watchdog-timeout-audit-report.md 中补齐对 WATCHDOG_TIMEOUT_AUDIT、watchdog findings 与 timing-watchdog-audit-pack 的引用。",
            )
        )

    missing_watchdog_report_sections = _find_missing_semantics(
        watchdog_report_content,
        {
            "audit summary": "## audit summary",
            "key findings": "## key findings",
            "evidence highlights": "## evidence highlights",
            "risk assessment": "## risk assessment",
            "recommended actions": "## recommended actions",
            "verification gaps": "## verification gaps",
        },
    )
    if missing_watchdog_report_sections:
        findings.append(
            Finding(
                level="L2",
                category="templates",
                file=watchdog_report_label,
                summary=f"watchdog report 模板缺少固定结构段：{', '.join(missing_watchdog_report_sections)}。",
                why_it_matters="若 report 模板没有固定结构段，专项报告就会退化成自由文本，无法稳定承接 findings 与 pack 的收口结果。",
                suggested_action="在 docs/templates/watchdog-timeout-audit-report.md 中补齐 audit summary、key findings、evidence highlights、risk assessment、recommended actions 与 verification gaps 段。",
            )
        )

# 在 check_docs() 中加入 WATCHDOG_TIMEOUT_AUDIT 对 report 模板的回指检查
if watchdog_timeout_content is not None and "docs/templates/watchdog-timeout-audit-report.md" not in watchdog_timeout_content:
    findings.append(
        Finding(
            level="L2",
            category="docs",
            file=watchdog_timeout_label,
            summary="watchdog 方法真源缺少 report 模板回指。",
            why_it_matters="方法真源若不回指最终报告模板，watchdog 自动报告对象就无法与 checklist / findings / pack 一起形成稳定分层。",
            suggested_action="在 docs/WATCHDOG_TIMEOUT_AUDIT.md 中补齐 docs/templates/watchdog-timeout-audit-report.md 的引用。",
        )
    )
```

- [ ] **Step 3: 运行 CLI，确认 watchdog report 规则先失败**

Run: `python tools/validate_consistency.py`
Expected: `Validation result: FAIL`，且至少出现指向以下对象的 findings：
- `docs/templates/watchdog-timeout-audit-report.md`
- `docs/WATCHDOG_TIMEOUT_AUDIT.md`

---

### Task 2: 新增 watchdog report 模板并让校验转绿

**Files:**
- Create: `docs/templates/watchdog-timeout-audit-report.md`
- Modify: `docs/WATCHDOG_TIMEOUT_AUDIT.md`
- Test: `tools/validate_consistency.py`

- [ ] **Step 1: 创建 `docs/templates/watchdog-timeout-audit-report.md`**

```md
# watchdog-timeout-audit-report

- 方法真源：`docs/WATCHDOG_TIMEOUT_AUDIT.md`
- 主输入：`docs/templates/watchdog-timeout-audit-findings.md`
- 补充输入：`docs/templates/timing-watchdog-audit-pack.md`

## audit summary
- 审计对象:
- 审计范围:
- 总体结论:
- 当前总体风险等级:

## key findings
- blocking items:
- high priority findings:
- immediate concerns:

## evidence highlights
- timing baseline:
- watchdog feed path:
- blocking / starvation:
- reset chain:
- failsafe convergence:
- ISR / main loop conflict:

## risk assessment
- confirmed risks:
- unresolved risks:
- impact on bring-up / release / safety review:

## recommended actions
- action-001:
- action-002:

## verification gaps
- gap-001:
- gap-002:
```

- [ ] **Step 2: 在 `docs/WATCHDOG_TIMEOUT_AUDIT.md` 补 report 模板回指与分工说明**

```md
在“与 specialist / 模板 / 主场景的关系”段补充：
- 最终专项报告模板：`docs/templates/watchdog-timeout-audit-report.md`

并补充分工：
- `docs/templates/watchdog-timeout-audit-report.md` 负责把 findings 与 pack 收束成可交付、可审查、可归档的专项报告。
```

- [ ] **Step 3: 运行 CLI，确认 watchdog report 校验通过**

Run: `python tools/validate_consistency.py`
Expected: `Validation result: PASS`

---

### Task 3: 同步路线图并把自动报告模板纳入现有门禁语义

**Files:**
- Modify: `docs/ROADMAP.md`
- Modify: `README.md`（如需入口）
- Test: `docs/ROADMAP.md`
- Test: `README.md`
- Test: `tools/validate_consistency.py`

- [ ] **Step 1: 在 `docs/ROADMAP.md` 收窄 watchdog 自动报告剩余项或标记已落地基线**

```md
将：
- [ ] 更重型 watchdog 专项 workflow / 自动报告能力留待后续阶段扩展

改成更精确状态，例如：
- [x] watchdog 自动报告模板基线已落地：`docs/templates/watchdog-timeout-audit-report.md` 已纳入现有 consistency / CI 门禁
- [ ] 更重型 watchdog 专项 workflow / 真正的自动报告生成器留待后续阶段扩展
```

- [ ] **Step 2: 如需要，在 `README.md` 增加 watchdog report 模板入口**

```md
- `docs/templates/watchdog-timeout-audit-report.md`：watchdog / timeout 最终专项报告模板
```

- [ ] **Step 3: 运行最小文本检查**

Run: `grep -n "watchdog-timeout-audit-report" README.md docs/ROADMAP.md docs/WATCHDOG_TIMEOUT_AUDIT.md docs/templates/watchdog-timeout-audit-report.md`
Expected: 若 README 被修改，则 4 个文件都命中；若 README 未修改，则其余 3 个文件命中且 `ROADMAP` 已更新

- [ ] **Step 4: 再跑一次 consistency CLI，确认现有门禁已覆盖新增对象**

Run: `python tools/validate_consistency.py`
Expected: `Validation result: PASS`

- [ ] **Step 5: 提交本轮 watchdog report 基线**

```bash
git add docs/WATCHDOG_TIMEOUT_AUDIT.md docs/CONSISTENCY_VALIDATION.md docs/ROADMAP.md README.md docs/templates/watchdog-timeout-audit-report.md tools/validate_consistency.py
git commit -m "feat: add watchdog audit report"
```

---

## Verification Notes

- 本计划不新增 GitHub workflow；自动报告能力在 CI 层的实现方式，是让现有 `consistency-validation.yml` 通过扩展后的 `tools/validate_consistency.py` 覆盖 report 模板对象。
- 报告模板只是最终载体，不是自动风险判定器，也不替代 findings / pack / checklist。
- findings 仍是主输入，pack 仍是补充输入；若实现中出现反向依赖或角色混淆，必须回退。