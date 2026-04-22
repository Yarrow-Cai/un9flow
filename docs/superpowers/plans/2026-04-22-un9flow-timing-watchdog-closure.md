# Timing Watchdog Closure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 `timing-watchdog-auditor` 收束成一条可复用、可校验、可纳管的 v5 专项能力线。

**Architecture:** docs 继续作为主真源，先把 watchdog 专项方法文档与 specialist / template 的映射规则写进 `docs/CONSISTENCY_VALIDATION.md`，再把对应检查落进 `tools/validate_consistency.py`。随后用最小文档改动把 `docs/WATCHDOG_TIMEOUT_AUDIT.md`、`skills/timing-watchdog-auditor/SKILL.md` 和 `docs/templates/timing-watchdog-audit-pack.md` 补到能通过新校验的状态；GitHub Action 继续复用现有 `.github/workflows/consistency-validation.yml`，无需改 workflow 架构。

**Tech Stack:** Markdown, Python 3, GitHub Actions（existing）, git, Claude Code

---

## File Structure

### Existing files to modify

- `docs/CONSISTENCY_VALIDATION.md` — 新增 specialist 方法真源与 skill / template 映射规则。
- `tools/validate_consistency.py` — 增加 watchdog 专项方法真源、skill 引用、template 引用的一致性检查。
- `docs/WATCHDOG_TIMEOUT_AUDIT.md` — 补齐它与 `timing-watchdog-auditor`、`docs/templates/timing-watchdog-audit-pack.md`、`docs/DESIGN_SAFETY_REVIEW.md` 的映射关系。
- `skills/timing-watchdog-auditor/SKILL.md` — 补充 watchdog 方法真源与 pack 模板回指。
- `docs/templates/timing-watchdog-audit-pack.md` — 补充 watchdog 方法真源回指。

### Existing files to read but not modify

- `docs/DOMAIN_SPECIALIST_CONTRACTS.md` — `timing-watchdog-auditor` 的契约真源。
- `docs/DESIGN_SAFETY_REVIEW.md` — watchdog 专项方法的主场景归属。
- `docs/INCIDENT_WORKFLOW.md` — watchdog specialist 在 incident 场景中的 Artifact 落点。
- `.github/workflows/consistency-validation.yml` — 已有最小 CI 门禁；本计划只依赖它运行 CLI，不改 workflow 结构。

### New files to create

- `docs/superpowers/plans/2026-04-22-un9flow-timing-watchdog-closure.md` — 当前 implementation plan。

### No new runtime files

本计划不新增新的 Python 模块、不新增新的 template 文件、不新增新的 workflow 文件。

---

### Task 1: 先把 watchdog 映射规则写成失败校验

**Files:**
- Modify: `docs/CONSISTENCY_VALIDATION.md`
- Modify: `tools/validate_consistency.py`
- Test: `tools/validate_consistency.py`

- [ ] **Step 1: 在 `docs/CONSISTENCY_VALIDATION.md` 补入 specialist 方法真源规则**

```md
## 每层校验职责

- **docs：规则完整性与 host 对齐约束**
- **skills：真源映射正确性**
- **模板：结构可承载性**
- **案例：路由可解释性与回归稳定性**
- **过程文档：历史一致性**

补充到 docs / skills / 模板规则段中的明确约束：

- specialist 方法真源文档（如 `docs/WATCHDOG_TIMEOUT_AUDIT.md`、`docs/REGISTER_STATE_AUDIT.md`）属于 docs 层受控对象。
- 若某条 `Domain Specialist` 存在独立方法真源，则该文档必须回指：
  - `docs/DOMAIN_SPECIALIST_CONTRACTS.md`
  - 至少一个复用它的主场景文档
  - 对应的 `docs/templates/*-pack.md`
- 对应 `skills/**/SKILL.md` 必须回指该方法真源。
- 对应 `docs/templates/*-pack.md` 必须回指该方法真源。
```

- [ ] **Step 2: 在 `tools/validate_consistency.py` 加入 watchdog 专项失败检查**

```python
# 在 constrained_docs 元组中加入 watchdog 方法真源
constrained_docs = (
    "README.md",
    "docs/ROADMAP.md",
    "docs/WORKFLOW.md",
    "docs/PLATFORMS.md",
    "docs/WATCHDOG_TIMEOUT_AUDIT.md",
)

# 在 check_docs() 中加入 watchdog 文档映射检查
watchdog_doc_label = "docs/WATCHDOG_TIMEOUT_AUDIT.md"
watchdog_doc_content = docs_content.get(watchdog_doc_label)
if watchdog_doc_content is not None:
    missing_watchdog_doc_refs = _find_missing_semantics(
        watchdog_doc_content,
        {
            "domain contracts ref": "docs/DOMAIN_SPECIALIST_CONTRACTS.md",
            "design safety review ref": "docs/DESIGN_SAFETY_REVIEW.md",
            "timing watchdog pack ref": "docs/templates/timing-watchdog-audit-pack.md",
        },
    )
    if missing_watchdog_doc_refs:
        findings.append(
            Finding(
                level="L2",
                category="docs",
                file=watchdog_doc_label,
                summary=f"watchdog 专项方法真源缺少映射锚点：{', '.join(missing_watchdog_doc_refs)}。",
                why_it_matters="watchdog 方法文档若不回指 specialist 契约、主场景真源与 pack 模板，就会再次退化成孤立说明文档。",
                suggested_action="在 docs/WATCHDOG_TIMEOUT_AUDIT.md 中补齐对 DOMAIN_SPECIALIST_CONTRACTS、DESIGN_SAFETY_REVIEW 与 timing-watchdog-audit-pack 的引用。",
            )
        )

# 在 check_skills() 的 specialist 循环之后加入 timing-watchdog 专项检查
timing_watchdog_label = "skills/timing-watchdog-auditor/SKILL.md"
timing_watchdog_content = skill_contents.get(timing_watchdog_label)
if timing_watchdog_content is not None:
    missing_timing_watchdog_refs = _find_missing_semantics(
        timing_watchdog_content,
        {
            "watchdog method ref": "docs/WATCHDOG_TIMEOUT_AUDIT.md",
            "timing watchdog pack ref": "docs/templates/timing-watchdog-audit-pack.md",
        },
    )
    if missing_timing_watchdog_refs:
        findings.append(
            Finding(
                level="L2",
                category="skills",
                file=timing_watchdog_label,
                summary=f"timing-watchdog-auditor 缺少专项真源回指：{', '.join(missing_timing_watchdog_refs)}。",
                why_it_matters="若 specialist skill 不回指 watchdog 方法真源与 pack 模板，使用者就无法判断它消费什么规则、产出什么承载物。",
                suggested_action="在 skills/timing-watchdog-auditor/SKILL.md 中补齐对 docs/WATCHDOG_TIMEOUT_AUDIT.md 与 docs/templates/timing-watchdog-audit-pack.md 的引用。",
            )
        )

# 在 check_templates() 的 specialist_pack_templates 循环中加入方法真源要求
if label == "docs/templates/timing-watchdog-audit-pack.md" and "docs/WATCHDOG_TIMEOUT_AUDIT.md" not in content:
    findings.append(
        Finding(
            level="L2",
            category="templates",
            file=label,
            summary="timing-watchdog-audit-pack 缺少 watchdog 方法真源回指。",
            why_it_matters="若 pack 模板不回指 watchdog 方法真源，模板层就无法稳定承接该专项能力的检查语义。",
            suggested_action="在 docs/templates/timing-watchdog-audit-pack.md 顶部补充 docs/WATCHDOG_TIMEOUT_AUDIT.md 引用。",
        )
    )
```

- [ ] **Step 3: 运行 CLI，确认新规则先失败**

Run: `python tools/validate_consistency.py`
Expected: `Validation result: FAIL`，并至少出现 3 条 L2 findings，分别指向 `docs/WATCHDOG_TIMEOUT_AUDIT.md`、`skills/timing-watchdog-auditor/SKILL.md`、`docs/templates/timing-watchdog-audit-pack.md`

---

### Task 2: 用最小文档改动让 watchdog 映射规则转绿

**Files:**
- Modify: `docs/WATCHDOG_TIMEOUT_AUDIT.md`
- Modify: `skills/timing-watchdog-auditor/SKILL.md`
- Modify: `docs/templates/timing-watchdog-audit-pack.md`
- Test: `tools/validate_consistency.py`

- [ ] **Step 1: 在 `docs/WATCHDOG_TIMEOUT_AUDIT.md` 加入映射关系段**

```md
## 与 specialist / 模板 / 主场景的关系

- specialist 契约真源：`docs/DOMAIN_SPECIALIST_CONTRACTS.md`
- 对应 `Domain Specialist`：`timing-watchdog-auditor`
- 对应输出模板：`docs/templates/timing-watchdog-audit-pack.md`
- 主要复用主场景：`docs/DESIGN_SAFETY_REVIEW.md`

职责分工固定为：
- 本文档回答“审什么、为什么审、失败态是什么”。
- `docs/templates/timing-watchdog-audit-pack.md` 回答“本次 dispatch 实际产出了什么、证据链是什么、下一步建议是什么”。
```

- [ ] **Step 2: 在 `skills/timing-watchdog-auditor/SKILL.md` 补齐专项真源回指**

```md
## 与真源文档的关系
- specialist 契约真源见 `docs/DOMAIN_SPECIALIST_CONTRACTS.md`
- 场景内交接边界见 `docs/INCIDENT_WORKFLOW.md`
- 总调度与 phase / dispatch 规则见 `docs/ORCHESTRATION.md`
- 专项方法真源见 `docs/WATCHDOG_TIMEOUT_AUDIT.md`
- 对应输出模板见 `docs/templates/timing-watchdog-audit-pack.md`
```

- [ ] **Step 3: 在 `docs/templates/timing-watchdog-audit-pack.md` 顶部补入方法真源回指**

```md
# timing-watchdog-audit-pack

- 模板定位：`timing-watchdog-auditor` 的输出模板，承接 `timeout-watchdog-risk-table`、`isr-mainloop-conflict-note` 与 `timing-instability-hypothesis`。
- 适用契约：`docs/DOMAIN_SPECIALIST_CONTRACTS.md`
- 方法真源：`docs/WATCHDOG_TIMEOUT_AUDIT.md`
```

- [ ] **Step 4: 运行 CLI，确认 watchdog 映射检查通过**

Run: `python tools/validate_consistency.py`
Expected: `Validation result: PASS`

- [ ] **Step 5: 提交这一条闭环改动**

```bash
git add docs/CONSISTENCY_VALIDATION.md tools/validate_consistency.py docs/WATCHDOG_TIMEOUT_AUDIT.md skills/timing-watchdog-auditor/SKILL.md docs/templates/timing-watchdog-audit-pack.md
git commit -m "docs: close timing watchdog specialist mapping"
```

---

## Verification Notes

- 本计划的“测试”就是让 `tools/validate_consistency.py` 先因为新规则失败，再因为文档映射补齐而通过。
- 不修改 `.github/workflows/consistency-validation.yml`；只要本地 CLI 通过，现有 PR / main 门禁就会自动继承这些新规则。
- 若同时在做 ISR 专项扩展，先完成本计划，再执行 `2026-04-22-un9flow-isr-mainloop-conflict-extension.md`，避免对 `docs/WATCHDOG_TIMEOUT_AUDIT.md` 和 `tools/validate_consistency.py` 产生无意义冲突。
