# ISR Mainloop Conflict Extension Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 ISR / main loop 职责冲突检查正式收编进 `timing-watchdog-auditor` 能力线，固定其文档归属、Artifact 证据要求与一致性校验规则。

**Architecture:** 这不是新 specialist，也不是新场景；实现方式是先在 `docs/CONSISTENCY_VALIDATION.md` 和 `tools/validate_consistency.py` 中把“ISR 冲突属于 timing-watchdog 线”写成失败规则，再补 `docs/WATCHDOG_TIMEOUT_AUDIT.md`、`skills/timing-watchdog-auditor/SKILL.md`、`docs/templates/timing-watchdog-audit-pack.md` 与 `docs/DOMAIN_SPECIALIST_CONTRACTS.md` 的专属段落。最后用 CLI 和一个“无新 specialist 名称”的文本检查一起收口。

**Tech Stack:** Markdown, Python 3, git, Claude Code, existing consistency CLI

---

## File Structure

### Existing files to modify

- `docs/CONSISTENCY_VALIDATION.md` — 记录 ISR / main loop 冲突属于 timing-watchdog 线内专项扩展，而不是新 specialist。
- `tools/validate_consistency.py` — 增加 watchdog 方法文档、skill、template、contract 对 ISR 冲突锚点的检查。
- `docs/WATCHDOG_TIMEOUT_AUDIT.md` — 新增 ISR / main loop 职责冲突专项小节。
- `skills/timing-watchdog-auditor/SKILL.md` — 新增线内专项扩展说明。
- `docs/templates/timing-watchdog-audit-pack.md` — 把 `isr-mainloop-conflict-note` 的证据要求写硬。
- `docs/DOMAIN_SPECIALIST_CONTRACTS.md` — 明确 `isr-mainloop-conflict-note` 归属 `timing-watchdog-auditor`，不拆成新 specialist。
- `docs/ROADMAP.md` — 把 v5 中的 ISR / 主循环职责冲突检查改为已落地专项扩展。

### Existing files to read but not modify

- `docs/INCIDENT_WORKFLOW.md` — 当前已把 `isr-mainloop-conflict-note` 放在 `timing-watchdog-auditor` 输出下。
- `docs/DESIGN_SAFETY_REVIEW.md` — `failsafe-check-matrix` 已吸收 `isr-mainloop-conflict-note`，作为上游场景边界依据。

### New files to create

- `docs/superpowers/plans/2026-04-22-un9flow-isr-mainloop-conflict-extension.md` — 当前 implementation plan。

---

### Task 1: 先把 ISR / main loop 冲突归属写成失败校验

**Files:**
- Modify: `docs/CONSISTENCY_VALIDATION.md`
- Modify: `tools/validate_consistency.py`
- Test: `tools/validate_consistency.py`

- [ ] **Step 1: 在 `docs/CONSISTENCY_VALIDATION.md` 增加 ISR 归属规则**

```md
补充到 docs / skills / 模板规则中的明确约束：

- `isr-mainloop-conflict-note` 是 `timing-watchdog-auditor` 的 canonical Artifact，不单独派生新的 `Domain Specialist`。
- `docs/WATCHDOG_TIMEOUT_AUDIT.md` 必须显式包含 ISR / main loop 职责冲突专项说明。
- `skills/timing-watchdog-auditor/SKILL.md` 必须显式声明 ISR / main loop 冲突检查属于该能力线内的专项扩展。
- `docs/templates/timing-watchdog-audit-pack.md` 必须给 `isr-mainloop-conflict-note` 提供专属证据字段。
- `docs/DOMAIN_SPECIALIST_CONTRACTS.md` 必须说明该 Artifact 归属 `timing-watchdog-auditor`，不拆成新 specialist。
```

- [ ] **Step 2: 在 `tools/validate_consistency.py` 增加 ISR 归属失败检查**

```python
# 在 check_docs() 中加入 watchdog 方法文档的 ISR 专项检查
if watchdog_doc_content is not None and "ISR / main loop 职责冲突" not in watchdog_doc_content:
    findings.append(
        Finding(
            level="L2",
            category="docs",
            file="docs/WATCHDOG_TIMEOUT_AUDIT.md",
            summary="watchdog 方法真源缺少 ISR / main loop 职责冲突专项段。",
            why_it_matters="若 watchdog 方法文档不显式覆盖 ISR / main loop 冲突，后续实现很容易把该检查漂成新的 specialist 或散落到别的场景。",
            suggested_action="在 docs/WATCHDOG_TIMEOUT_AUDIT.md 中加入 ISR / main loop 职责冲突专项小节。",
        )
    )

# 在 check_skills() 中加入 timing-watchdog 对 ISR 专项扩展的声明检查
if timing_watchdog_content is not None and "线内专项扩展" not in timing_watchdog_content:
    findings.append(
        Finding(
            level="L2",
            category="skills",
            file="skills/timing-watchdog-auditor/SKILL.md",
            summary="timing-watchdog-auditor 缺少线内专项扩展段。",
            why_it_matters="若 skill 不声明 ISR / main loop 冲突属于线内专项扩展，使用者就可能继续把它误解成新的 specialist。",
            suggested_action="在 skills/timing-watchdog-auditor/SKILL.md 中加入“线内专项扩展”段，并明确 ISR / main loop 冲突归属该能力线。",
        )
    )

# 在 check_templates() 中加入 timing pack 的 ISR 专属证据字段检查
if label == "docs/templates/timing-watchdog-audit-pack.md":
    missing_isr_pack_fields = [
        field
        for field in (
            "- ISR 侧职责:",
            "- main loop 侧职责:",
            "- 被破坏的确定性约束:",
            "- 可能导致的 reset / timeout / 饥饿风险:",
            "- 仍缺的证据:",
        )
        if field not in content
    ]
    if missing_isr_pack_fields:
        findings.append(
            Finding(
                level="L2",
                category="templates",
                file=label,
                summary=f"isr-mainloop-conflict-note 缺少专属证据字段：{', '.join(missing_isr_pack_fields)}。",
                why_it_matters="若 ISR 冲突输出没有专属证据字段，reviewer 无法判断冲突发生在哪一侧、破坏了什么约束、会造成什么后果。",
                suggested_action="在 docs/templates/timing-watchdog-audit-pack.md 的 isr-mainloop-conflict-note 下补齐 ISR 侧职责、main loop 侧职责、被破坏的确定性约束、风险后果与仍缺证据字段。",
            )
        )

# 在 check_docs() 中加入 contract 对 ISR 归属的说明检查
domain_contracts_content = docs_content.get("docs/DOMAIN_SPECIALIST_CONTRACTS.md")
if domain_contracts_content is not None and "不得拆成新的 specialist" not in domain_contracts_content:
    findings.append(
        Finding(
            level="L2",
            category="docs",
            file="docs/DOMAIN_SPECIALIST_CONTRACTS.md",
            summary="Domain Specialist 契约真源未声明 ISR 冲突 Artifact 不拆成新 specialist。",
            why_it_matters="若 contract 真源不把 ISR 冲突明确绑定到 timing-watchdog-auditor，能力边界后续仍会漂移。",
            suggested_action="在 docs/DOMAIN_SPECIALIST_CONTRACTS.md 的 timing-watchdog-auditor 段中补充 isr-mainloop-conflict-note 归属说明。",
        )
    )
```

- [ ] **Step 3: 运行 CLI，确认 ISR 归属规则先失败**

Run: `python tools/validate_consistency.py`
Expected: `Validation result: FAIL`，并出现指向 `docs/WATCHDOG_TIMEOUT_AUDIT.md`、`skills/timing-watchdog-auditor/SKILL.md`、`docs/templates/timing-watchdog-audit-pack.md`、`docs/DOMAIN_SPECIALIST_CONTRACTS.md` 的 L2 findings

---

### Task 2: 把 ISR / main loop 冲突正式收编进 timing-watchdog 线

**Files:**
- Modify: `docs/WATCHDOG_TIMEOUT_AUDIT.md`
- Modify: `skills/timing-watchdog-auditor/SKILL.md`
- Modify: `docs/templates/timing-watchdog-audit-pack.md`
- Modify: `docs/DOMAIN_SPECIALIST_CONTRACTS.md`
- Test: `tools/validate_consistency.py`

- [ ] **Step 1: 在 `docs/WATCHDOG_TIMEOUT_AUDIT.md` 加入 ISR / main loop 专项小节**

```md
## ISR / main loop 职责冲突

### 审计重点
- ISR 必须保持短、快、可退出；不得承担长阻塞、完整状态推进或无边界重试。
- main loop 只能消费已归一化事件；不得承担依赖硬实时保证却没有固定节拍约束的关键动作。
- 若 watchdog feed path 位于 ISR 或空转路径，必须直接记为假健康风险。
- 若冲突会导致 timeout 检查失真、喂狗责任漂移或 reset 链解释中断，必须升级为阻断项。

### 最低输出
- `isr-mainloop-conflict-note` 至少回答：
  - ISR 侧越权动作是什么
  - main loop 侧缺口是什么
  - 被破坏的确定性约束是什么
  - 可能导致的 reset / timeout / 饥饿风险是什么
  - 仍缺哪些证据
```

- [ ] **Step 2: 在 `skills/timing-watchdog-auditor/SKILL.md` 增加线内专项扩展段**

```md
## 线内专项扩展
- `ISR / main loop` 职责冲突检查属于 `timing-watchdog-auditor` 线内专项扩展，不单独派生新的 `Domain Specialist`。
- 当异常表现为 reset、喂狗不稳、timeout 失真、节拍抖动或“系统失活但仍能喂狗”时，必须优先通过 `isr-mainloop-conflict-note` 收口，而不是新造入口名。
```

- [ ] **Step 3: 在 `docs/templates/timing-watchdog-audit-pack.md` 把 `isr-mainloop-conflict-note` 写成可复核结构**

```md
### isr-mainloop-conflict-note
- ISR 侧职责:
- main loop 侧职责:
- 被破坏的确定性约束:
- 可能导致的 reset / timeout / 饥饿风险:
- 仍缺的证据:
```

- [ ] **Step 4: 在 `docs/DOMAIN_SPECIALIST_CONTRACTS.md` 明确 Artifact 归属**

```md
#### 输出 Artifact
- `timeout-watchdog-risk-table`：超时与 watchdog 风险项表
- `isr-mainloop-conflict-note`：ISR 与主循环职责冲突说明；该 Artifact 归属 `timing-watchdog-auditor`，不得拆成新的 specialist
- `timing-instability-hypothesis`：时序不稳定假设与验证入口
```

- [ ] **Step 5: 运行 CLI，确认 ISR 归属检查通过**

Run: `python tools/validate_consistency.py`
Expected: `Validation result: PASS`

---

### Task 3: 同步 roadmap，并确认没有长出新的 specialist 名称

**Files:**
- Modify: `docs/ROADMAP.md`
- Test: `docs/ROADMAP.md`
- Test: `docs/WATCHDOG_TIMEOUT_AUDIT.md`
- Test: `skills/timing-watchdog-auditor/SKILL.md`

- [ ] **Step 1: 在 `docs/ROADMAP.md` 把 ISR / 主循环职责冲突检查改为已落地扩展**

```md
- [x] ISR / 主循环职责冲突检查已作为 `timing-watchdog-auditor` 线内专项扩展固化，沿 `Domain Specialist` 与 `Artifact` 主线延展
```

- [ ] **Step 2: 运行文本检查，确认 ISR 冲突锚点都落在 timing-watchdog 线下**

Run: `grep -n "ISR / main loop\|isr-mainloop-conflict-note\|timing-watchdog-auditor" docs/WATCHDOG_TIMEOUT_AUDIT.md skills/timing-watchdog-auditor/SKILL.md docs/templates/timing-watchdog-audit-pack.md docs/DOMAIN_SPECIALIST_CONTRACTS.md docs/ROADMAP.md`
Expected: 5 个文件都能命中 `isr-mainloop-conflict-note` 或 `ISR / main loop` 与 `timing-watchdog-auditor`

- [ ] **Step 3: 运行“没有新 specialist 名称”的检查**

Run: `grep -R -n "isr-mainloop-conflict-checker\|isr-mainloop-specialist\|ISR-specialist" docs skills tools || true`
Expected: 无输出

- [ ] **Step 4: 再跑一次 consistency CLI，确认全仓仍为绿色**

Run: `python tools/validate_consistency.py`
Expected: `Validation result: PASS`

- [ ] **Step 5: 提交 ISR / main loop 冲突专项扩展**

```bash
git add docs/CONSISTENCY_VALIDATION.md tools/validate_consistency.py docs/WATCHDOG_TIMEOUT_AUDIT.md skills/timing-watchdog-auditor/SKILL.md docs/templates/timing-watchdog-audit-pack.md docs/DOMAIN_SPECIALIST_CONTRACTS.md docs/ROADMAP.md
git commit -m "docs: fold isr conflict checks into timing watchdog"
```

---

## Verification Notes

- 本计划不允许创建新 specialist 名称；所有文本检查都要证明 ISR / main loop 冲突仍然属于 `timing-watchdog-auditor`。
- 若 `2026-04-22-un9flow-timing-watchdog-closure.md` 还没执行，先执行它，再执行本计划；两份计划都会改 `docs/WATCHDOG_TIMEOUT_AUDIT.md`、`docs/CONSISTENCY_VALIDATION.md` 与 `tools/validate_consistency.py`。
- 不修改 `.github/workflows/consistency-validation.yml`；现有门禁会自动运行扩展后的 CLI 规则。
