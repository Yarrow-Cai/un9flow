# Template Generation Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 un9flow 建立“共享生成约定 + 薄包装脚本”的最小模板生成体系，先接入 watchdog report、incident case bundle 与 v6 示例骨架。

**Architecture:** 本轮不做大一统平台，而是新增 `docs/TEMPLATE_GENERATION.md` 作为生成约定真源，新增 `tools/generation_core.py` 作为最小共享内核，然后让现有生成脚本逐步接入这个内核。现有 `.github/workflows/consistency-validation.yml` 不改结构，继续只跑 `python tools/validate_consistency.py`，用以纳管生成体系对象与关系，不直接在 CI 中执行生成器。

**Tech Stack:** Markdown, Python 3, GitHub Actions（existing）, git, Claude Code

---

## File Structure

### Existing files to modify

- `docs/CONSISTENCY_VALIDATION.md` — 增加模板生成体系对象的一致性规则。
- `tools/validate_consistency.py` — 增加 `TEMPLATE_GENERATION.md`、`generation_core.py` 及各生成脚本回指关系的检查。
- `tools/generate_incident_case_bundle.py` — 改造成薄包装脚本，显式回指生成约定与共享内核。
- `tools/generate_watchdog_timeout_audit_report.py` — 改造成薄包装脚本，显式回指生成约定与共享内核。
- `docs/ROADMAP.md` — 把“模板生成体系与更完整回归校验”推进为已落地生成体系基线，并保留回归校验增强项。

### Existing files to read but not modify

- `docs/templates/watchdog-timeout-audit-report.md`
- `docs/templates/watchdog-timeout-audit-findings.md`
- `docs/templates/timing-watchdog-audit-pack.md`
- `docs/templates/skill-routing-matrix.md`
- `docs/templates/orchestrator-dispatch-plan.md`
- `docs/cases/*.md`

### New files to create

- `docs/TEMPLATE_GENERATION.md` — 模板生成约定真源文档。
- `tools/generation_core.py` — 共享生成内核。
- `docs/superpowers/plans/2026-04-24-un9flow-template-generation-foundation.md` — 当前 implementation plan。

### No new CI/workflow files

本计划不新增新的 GitHub workflow，也不在本轮引入 golden files / snapshot 回归。

---

### Task 1: 先把模板生成体系规则写成失败校验

**Files:**
- Modify: `docs/CONSISTENCY_VALIDATION.md`
- Modify: `tools/validate_consistency.py`
- Test: `tools/validate_consistency.py`

- [ ] **Step 1: 在 `docs/CONSISTENCY_VALIDATION.md` 增加模板生成体系规则**

```md
在 docs / tools / 过程文档相关规则段补充：

- `docs/TEMPLATE_GENERATION.md` 是模板生成体系的约定真源。
- `tools/generation_core.py` 是共享生成内核。
- 对于被纳入生成体系的脚本（如 `tools/generate_incident_case_bundle.py`、`tools/generate_watchdog_timeout_audit_report.py`），必须显式回指：
  - `docs/TEMPLATE_GENERATION.md`
  - `tools/generation_core.py`
  - 自己服务的模板/对象
- 首批接入对象必须能说明：
  - 输入是什么
  - 输出是什么
  - 输出是单文件还是 bundle
```

- [ ] **Step 2: 在 `tools/validate_consistency.py` 增加模板生成体系失败检查**

```python
# 在 docs 检查中加入 TEMPLATE_GENERATION 真源文档
if (ROOT / "docs" / "TEMPLATE_GENERATION.md").read_text(encoding="utf-8") if (ROOT / "docs" / "TEMPLATE_GENERATION.md").exists() else None is None:
    findings.append(
        Finding(
            level="L1",
            category="docs",
            file="docs/TEMPLATE_GENERATION.md",
            summary="模板生成约定真源缺失或无法读取。",
            why_it_matters="若缺少模板生成约定真源，生成器之间的输入/输出/命名规则就无法形成统一基线。",
            suggested_action="创建 docs/TEMPLATE_GENERATION.md 并确保 UTF-8 可读。",
        )
    )

# 在 process/tools 检查中加入 generation_core
if _read_text(ROOT / "tools" / "generation_core.py") is None:
    findings.append(
        Finding(
            level="L1",
            category="process_docs",
            file="tools/generation_core.py",
            summary="共享生成内核缺失或无法读取。",
            why_it_matters="若没有 generation_core，共性生成逻辑就仍然散落在各脚本中，无法形成最小生成体系。",
            suggested_action="创建 tools/generation_core.py 并确保 UTF-8 可读。",
        )
    )

# 检查现有生成脚本回指 generation docs/core/target object
for label, required_terms in {
    "tools/generate_incident_case_bundle.py": ("TEMPLATE_GENERATION", "generation_core", "incident"),
    "tools/generate_watchdog_timeout_audit_report.py": ("TEMPLATE_GENERATION", "generation_core", "watchdog-timeout-audit-report"),
}.items():
    content = _read_text(ROOT / Path(label))
    if content is None:
        continue
    missing_terms = [term for term in required_terms if term not in content]
    if missing_terms:
        findings.append(
            Finding(
                level="L2",
                category="process_docs",
                file=label,
                summary=f"生成脚本缺少体系锚点：{', '.join(missing_terms)}。",
                why_it_matters="若生成脚本不显式声明自己服务的对象以及与 generation core / generation docs 的关系，体系化生成规则就无法稳定校验。",
                suggested_action="在生成脚本顶部或说明段补齐 TEMPLATE_GENERATION、generation_core 与目标对象锚点。",
            )
        )
```

- [ ] **Step 3: 运行 CLI，确认模板生成体系规则先失败**

Run: `python tools/validate_consistency.py`
Expected: `Validation result: FAIL`，并至少出现以下对象相关 finding：
- `docs/TEMPLATE_GENERATION.md`
- `tools/generation_core.py`
- 至少一个生成脚本的体系锚点缺口

---

### Task 2: 新增生成约定真源与共享内核，并让生成器最小接入

**Files:**
- Create: `docs/TEMPLATE_GENERATION.md`
- Create: `tools/generation_core.py`
- Modify: `tools/generate_incident_case_bundle.py`
- Modify: `tools/generate_watchdog_timeout_audit_report.py`
- Test: `tools/validate_consistency.py`

- [ ] **Step 1: 创建 `docs/TEMPLATE_GENERATION.md`**

```md
# un9flow Template Generation

## 目标
- 为可生成对象提供统一输入/输出与命名约定。

## 首批接入对象
- watchdog report（单文件）
- incident case bundle（bundle）
- v6 example skeleton（单文件骨架，后续接入）

## 输入最小集合
- source template
- structured inputs
- output target path

## 输出约定
- 单文件输出：直接写入目标 markdown
- bundle 输出：写入目标目录并生成 README

## 缺字段处理
- 缺少必填输入时直接失败
- 缺少可选输入时保留空缺占位，不自动发明内容

## 生成器责任
- 每个生成脚本必须显式声明：
  - 自己服务的对象
  - 依赖 `tools/generation_core.py`
  - 遵循 `docs/TEMPLATE_GENERATION.md`
```

- [ ] **Step 2: 创建 `tools/generation_core.py`**

```python
from __future__ import annotations

from pathlib import Path


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def write_text(path: str | Path, content: str) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")


def replace_fields(template_text: str, replacements: dict[str, str]) -> str:
    rendered = template_text
    for key, value in replacements.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", value)
    return rendered
```

- [ ] **Step 3: 在 `tools/generate_watchdog_timeout_audit_report.py` 顶部补体系锚点并最小接入 core**

```python
"""Generate watchdog-timeout-audit-report.

Generation contract: docs/TEMPLATE_GENERATION.md
Shared core: tools/generation_core.py
Target object: watchdog-timeout-audit-report
"""

from generation_core import read_text, write_text
```

并把原先本地文件读写换成 `read_text` / `write_text` 调用。

- [ ] **Step 4: 在 `tools/generate_incident_case_bundle.py` 顶部补体系锚点并最小接入 core**

```python
"""Generate incident case bundle.

Generation contract: docs/TEMPLATE_GENERATION.md
Shared core: tools/generation_core.py
Target object: incident case bundle
"""

from generation_core import read_text, write_text
```

并把模板读写替换为 `read_text` / `write_text` 的最小共用调用。

- [ ] **Step 5: 运行 CLI，确认模板生成体系校验通过**

Run: `python tools/validate_consistency.py`
Expected: `Validation result: PASS`

---

### Task 3: 同步 ROADMAP 并把生成体系基线纳入当前描述

**Files:**
- Modify: `docs/ROADMAP.md`
- Test: `docs/ROADMAP.md`
- Test: `docs/TEMPLATE_GENERATION.md`
- Test: `tools/generation_core.py`
- Test: `tools/validate_consistency.py`

- [ ] **Step 1: 在 `docs/ROADMAP.md` 把“模板生成体系与更完整回归校验”拆成已完成基线 + 后续项**

```md
将：
- [ ] 模板生成体系与更完整回归校验

改成：
- [x] 模板生成体系基线已落地：`docs/TEMPLATE_GENERATION.md` 与 `tools/generation_core.py` 已建立共享约定与最小内核
- [ ] 更完整的输出回归校验（golden files / snapshot / output regression）留待后续阶段扩展
```

- [ ] **Step 2: 运行最小文本检查**

Run: `grep -n "TEMPLATE_GENERATION\|generation_core\|输出回归" docs/ROADMAP.md docs/TEMPLATE_GENERATION.md tools/generation_core.py`
Expected: 3 个文件都能命中对应关键字

- [ ] **Step 3: 再跑一次 consistency CLI，确认现有门禁已覆盖生成体系对象**

Run: `python tools/validate_consistency.py`
Expected: `Validation result: PASS`

- [ ] **Step 4: 提交模板生成体系基线**

```bash
git add docs/TEMPLATE_GENERATION.md tools/generation_core.py tools/generate_incident_case_bundle.py tools/generate_watchdog_timeout_audit_report.py docs/CONSISTENCY_VALIDATION.md tools/validate_consistency.py docs/ROADMAP.md
git commit -m "feat: add template generation foundation"
```

---

## Verification Notes

- 本计划不在本轮把所有模板都接进生成体系；只验证共享约定 + 共享内核 + 两个现有生成脚本的最小接入。
- 本计划不在 CI 中执行所有生成器；当前目标是让 consistency / 现有 workflow 认识这些对象。
- 后续若要接入 v6 示例骨架生成或做 golden files 回归，应在下一轮单独规划。