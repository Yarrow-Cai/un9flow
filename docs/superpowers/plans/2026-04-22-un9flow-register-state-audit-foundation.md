# Register State Audit Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 `register-state-auditor` 补齐独立方法真源、skill/template 映射和一致性校验基线，让寄存器审计成为第二条稳定的 v5 embedded specialist 能力线。

**Architecture:** 先把寄存器审计方法真源的规则写进 `docs/CONSISTENCY_VALIDATION.md` 并在 `tools/validate_consistency.py` 中形成失败校验，再创建 `docs/REGISTER_STATE_AUDIT.md` 并同步 skill、template、README、ROADMAP。实现顺序固定为“先加失败规则，再补文档与映射，再跑 CLI 转绿”，避免把新文档写成不受校验约束的第二套真源。

**Tech Stack:** Markdown, Python 3, git, Claude Code, existing consistency CLI

---

## File Structure

### Existing files to modify

- `docs/CONSISTENCY_VALIDATION.md` — 把 register 专项方法真源纳入 docs 层一致性规则。
- `tools/validate_consistency.py` — 增加 `docs/REGISTER_STATE_AUDIT.md`、`skills/register-state-auditor/SKILL.md`、`docs/templates/register-state-audit-pack.md`、`README.md` 之间的一致性检查。
- `skills/register-state-auditor/SKILL.md` — 补充寄存器审计方法真源与 pack 模板回指。
- `docs/templates/register-state-audit-pack.md` — 补充方法真源回指与更硬的证据字段。
- `README.md` — 顶层目录清单新增 `docs/REGISTER_STATE_AUDIT.md` 入口。
- `docs/ROADMAP.md` — 把 v5 中“寄存器审计能力”从未开始推进到已落地方法基线。

### New files to create

- `docs/superpowers/plans/2026-04-22-un9flow-register-state-audit-foundation.md` — 当前 implementation plan。
- `docs/REGISTER_STATE_AUDIT.md` — 寄存器审计方法真源。

### Existing files to read but not modify

- `docs/DOMAIN_SPECIALIST_CONTRACTS.md` — `register-state-auditor` 的输入 / 输出契约。
- `docs/INCIDENT_WORKFLOW.md` — register artifacts 在 incident 场景中的落点。
- `docs/DESIGN_SAFETY_REVIEW.md` — register audit 在 design review 场景中的默认 specialist 角色。

---

### Task 1: 先把 register 方法真源规则写成失败校验

**Files:**
- Modify: `docs/CONSISTENCY_VALIDATION.md`
- Modify: `tools/validate_consistency.py`
- Test: `tools/validate_consistency.py`

- [ ] **Step 1: 在 `docs/CONSISTENCY_VALIDATION.md` 明确 register 方法真源规则**

```md
补充到 docs / skills / 模板约束中的明确规则：

- `docs/REGISTER_STATE_AUDIT.md` 属于 `register-state-auditor` 的方法真源文档。
- `docs/REGISTER_STATE_AUDIT.md` 必须回指：
  - `docs/DOMAIN_SPECIALIST_CONTRACTS.md`
  - `docs/INCIDENT_WORKFLOW.md`
  - `docs/DESIGN_SAFETY_REVIEW.md`
  - `docs/templates/register-state-audit-pack.md`
- `skills/register-state-auditor/SKILL.md` 必须回指 `docs/REGISTER_STATE_AUDIT.md`。
- `docs/templates/register-state-audit-pack.md` 必须回指 `docs/REGISTER_STATE_AUDIT.md`。
- `README.md` 必须把 `docs/REGISTER_STATE_AUDIT.md` 暴露为仓库内文档入口之一。
```

- [ ] **Step 2: 在 `tools/validate_consistency.py` 加入 register 失败检查**

```python
# 在 constrained_docs 元组中加入 register 方法真源
constrained_docs = (
    "README.md",
    "docs/ROADMAP.md",
    "docs/WORKFLOW.md",
    "docs/PLATFORMS.md",
    "docs/WATCHDOG_TIMEOUT_AUDIT.md",
    "docs/REGISTER_STATE_AUDIT.md",
)

# 在 check_docs() 中加入 README 对 register 方法真源的入口检查
if readme_content is not None and "docs/REGISTER_STATE_AUDIT.md" not in readme_content:
    findings.append(
        Finding(
            level="L2",
            category="docs",
            file="README.md",
            summary="缺少 docs/REGISTER_STATE_AUDIT.md 的入口引用。",
            why_it_matters="README 若不暴露寄存器审计方法真源，使用者很难发现 register-state-auditor 的稳定方法边界。",
            suggested_action="在 README.md 的文档清单中加入 docs/REGISTER_STATE_AUDIT.md。",
        )
    )

# 在 check_docs() 中加入 register 方法真源映射检查
register_doc_label = "docs/REGISTER_STATE_AUDIT.md"
register_doc_content = docs_content.get(register_doc_label)
if register_doc_content is not None:
    missing_register_doc_refs = _find_missing_semantics(
        register_doc_content,
        {
            "domain contracts ref": "docs/DOMAIN_SPECIALIST_CONTRACTS.md",
            "incident workflow ref": "docs/INCIDENT_WORKFLOW.md",
            "design safety review ref": "docs/DESIGN_SAFETY_REVIEW.md",
            "register pack ref": "docs/templates/register-state-audit-pack.md",
        },
    )
    if missing_register_doc_refs:
        findings.append(
            Finding(
                level="L2",
                category="docs",
                file=register_doc_label,
                summary=f"register 方法真源缺少映射锚点：{', '.join(missing_register_doc_refs)}。",
                why_it_matters="寄存器审计方法若不回指 contract、场景真源和 pack 模板，就无法稳定成为第二条 specialist 能力线。",
                suggested_action="在 docs/REGISTER_STATE_AUDIT.md 中补齐 DOMAIN_SPECIALIST_CONTRACTS、INCIDENT_WORKFLOW、DESIGN_SAFETY_REVIEW 与 register-state-audit-pack 的引用。",
            )
        )

# 在 check_skills() 中加入 register skill 对方法真源的回指检查
register_skill_label = "skills/register-state-auditor/SKILL.md"
register_skill_content = skill_contents.get(register_skill_label)
if register_skill_content is not None and "docs/REGISTER_STATE_AUDIT.md" not in register_skill_content:
    findings.append(
        Finding(
            level="L2",
            category="skills",
            file=register_skill_label,
            summary="register-state-auditor 缺少寄存器审计方法真源回指。",
            why_it_matters="specialist skill 若不回指 register 方法真源，使用者就无法判断其证据规则和输出约束来自哪里。",
            suggested_action="在 skills/register-state-auditor/SKILL.md 中加入 docs/REGISTER_STATE_AUDIT.md 引用。",
        )
    )

# 在 check_templates() 中加入 register pack 对方法真源的回指检查
if label == "docs/templates/register-state-audit-pack.md" and "docs/REGISTER_STATE_AUDIT.md" not in content:
    findings.append(
        Finding(
            level="L2",
            category="templates",
            file=label,
            summary="register-state-audit-pack 缺少寄存器审计方法真源回指。",
            why_it_matters="若 pack 模板不回指 register 方法真源，模板层就无法稳定承接寄存器审计规则。",
            suggested_action="在 docs/templates/register-state-audit-pack.md 顶部补充 docs/REGISTER_STATE_AUDIT.md 引用。",
        )
    )
```

- [ ] **Step 3: 运行 CLI，确认 register 相关规则先失败**

Run: `python tools/validate_consistency.py`
Expected: `Validation result: FAIL`，至少出现指向 `README.md`、`skills/register-state-auditor/SKILL.md`、`docs/templates/register-state-audit-pack.md` 的 L2 findings；若 `docs/REGISTER_STATE_AUDIT.md` 尚不存在，还应出现该文件缺失或无法读取的 finding

---

### Task 2: 创建 `docs/REGISTER_STATE_AUDIT.md` 并补齐 skill / template 映射

**Files:**
- Create: `docs/REGISTER_STATE_AUDIT.md`
- Modify: `skills/register-state-auditor/SKILL.md`
- Modify: `docs/templates/register-state-audit-pack.md`
- Test: `tools/validate_consistency.py`

- [ ] **Step 1: 创建 `docs/REGISTER_STATE_AUDIT.md`**

```md
# un9flow Register State Audit

## 目标

把寄存器审计能力固定为 `register-state-auditor` 的方法真源，用于审查默认值、目标值、当前值、复位后值与关键位语义之间是否存在可复核的配置偏移与确定性缺口。

## 定位与边界

### 它属于什么
- `register-state-auditor` 的专项方法真源
- 面向寄存器快照、关键使能位、保护位与复位返回路径的审计方法
- 用于回答“寄存器层是否存在配置偏移、位语义误判或复位残留风险”

### 它不属于什么
- 不是新的 `Scenario`
- 不是链路分段定位器
- 不是完整状态机迁移分析器
- 不是直接给出系统级根因定论的裁决器

## 核心检查项

### 1. reset-value baseline
- 默认值 / 目标值 / 当前值 / 复位后值是否齐全
- 是否能定位每个值来自规格、初始化代码、在线配置还是故障快照

### 2. enable and protection chain
- 关键使能位、保护位、屏蔽位、旁路位是否形成单向可解释链
- 是否存在“保护未开但系统以为已开”的假安全状态

### 3. sticky and latched semantics
- sticky flag、latch、write-clear、shadow register 的位语义是否明确
- 是否把“未清除”误判成“实时仍在触发”

### 4. config mismatch and init gap
- 初始化顺序、覆盖顺序、在线参数写入顺序是否造成配置偏移
- 是否存在只在 warm reset / brownout 后出现的残留配置缺口

### 5. reset-return risk
- 复位后寄存器与关键外设是否回到预期安全态
- 哪些寄存器必须清零、保留、重载，是否有明确规则

## 输出结构
- `register-bitfield-map`
- `register-anomaly-list`
- `config-mismatch-note`

## 与 specialist / 模板 / 场景的关系
- specialist 契约真源：`docs/DOMAIN_SPECIALIST_CONTRACTS.md`
- incident 场景边界：`docs/INCIDENT_WORKFLOW.md`
- design review 复用场景：`docs/DESIGN_SAFETY_REVIEW.md`
- 对应输出模板：`docs/templates/register-state-audit-pack.md`
```

- [ ] **Step 2: 在 `skills/register-state-auditor/SKILL.md` 增加方法真源回指**

```md
## 与真源文档的关系
- specialist 契约真源见 `docs/DOMAIN_SPECIALIST_CONTRACTS.md`
- 场景内交接边界见 `docs/INCIDENT_WORKFLOW.md`
- 总调度与 phase / dispatch 规则见 `docs/ORCHESTRATION.md`
- 专项方法真源见 `docs/REGISTER_STATE_AUDIT.md`
- 对应输出模板见 `docs/templates/register-state-audit-pack.md`
```

- [ ] **Step 3: 在 `docs/templates/register-state-audit-pack.md` 加强方法与证据锚点**

```md
# register-state-audit-pack

- 模板定位：`register-state-auditor` 的输出模板，承接 `register-bitfield-map`、`register-anomaly-list` 与 `config-mismatch-note`。
- 适用契约：`docs/DOMAIN_SPECIALIST_CONTRACTS.md`
- 方法真源：`docs/REGISTER_STATE_AUDIT.md`

## evidence used
- 寄存器快照:
- 关键配置项 / 使能位:
- 默认值 / 目标值 / 当前值 / 复位后值:
- sticky / latch / write-clear / shadow 语义:
- 复位 / 保护 / 时序证据:
- 相关上游 Artifact:
```

- [ ] **Step 4: 运行 CLI，确认 register 映射检查通过**

Run: `python tools/validate_consistency.py`
Expected: `Validation result: PASS`

---

### Task 3: 同步 README 与 ROADMAP，让 register 能力对外可见

**Files:**
- Modify: `README.md`
- Modify: `docs/ROADMAP.md`
- Test: `README.md`
- Test: `docs/ROADMAP.md`

- [ ] **Step 1: 在 `README.md` 的当前仓库内容中加入 register 方法文档入口**

```md
- `docs/REGISTER_STATE_AUDIT.md`：`register-state-auditor` 的寄存器审计方法真源，固定默认值 / 目标值 / 当前值 / 复位后值、位语义与复位返回风险的复核方式
```

- [ ] **Step 2: 在 `docs/ROADMAP.md` 把寄存器审计能力改为已落地基线**

```md
- [x] 寄存器审计能力基线已落地：`docs/REGISTER_STATE_AUDIT.md` 作为方法真源，`docs/templates/register-state-audit-pack.md` 作为 specialist pack 模板
```

- [ ] **Step 3: 运行最小文本检查，确认入口与路线图状态都已更新**

Run: `grep -n "REGISTER_STATE_AUDIT.md" README.md docs/ROADMAP.md skills/register-state-auditor/SKILL.md docs/templates/register-state-audit-pack.md`
Expected: 4 个文件都命中 `REGISTER_STATE_AUDIT.md`

- [ ] **Step 4: 再跑一次 consistency CLI，确认整条 register 线转绿**

Run: `python tools/validate_consistency.py`
Expected: `Validation result: PASS`

- [ ] **Step 5: 提交寄存器审计基线**

```bash
git add docs/CONSISTENCY_VALIDATION.md tools/validate_consistency.py docs/REGISTER_STATE_AUDIT.md skills/register-state-auditor/SKILL.md docs/templates/register-state-audit-pack.md README.md docs/ROADMAP.md
git commit -m "docs: add register state audit baseline"
```

---

## Verification Notes

- 本计划的完成标准不是“写了一个新文档”，而是：新文档、skill、template、README 入口与 consistency CLI 全部对齐。
- 如果 `2026-04-22-un9flow-timing-watchdog-closure.md` 已经先落地，执行本计划时要小心保留其中对 `docs/CONSISTENCY_VALIDATION.md` 和 `tools/validate_consistency.py` 的 watchdog 规则，不要回滚掉。
- 这份计划不新增新的 workflow 文件；现有 `.github/workflows/consistency-validation.yml` 会自动继承新的 register 校验逻辑。
