# un9flow Consistency CLI Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 un9flow 建立第一代本地可运行的一致性校验 CLI，覆盖 docs / skills / templates / routing cases / 过程文档，并输出人类 review 友好的 findings。

**Architecture:** 第一版先实现单入口 Python CLI `tools/validate_consistency.py`，内部按五层对象拆成 5 个检查器，但仍先保持单文件实现。脚本统一返回 findings 结构，并按 L1 / L2 / L3 分段输出，最终以 0 / 1 / 2 三档退出码反映当前仓库的一致性状态。

**Tech Stack:** Python 3, Markdown, git, Claude Code, un9flow 文档仓库

---

## File Structure

### Existing files to read/validate against

- `docs/CONSISTENCY_VALIDATION.md` — 统一校验体系真源，定义五层对象、L1/L2/L3 和处理动作。
- `docs/ORCHESTRATION.md` — 总调度规则真源。
- `docs/INCIDENT_WORKFLOW.md` — incident 场景真源。
- `docs/SKILL_ARCHITECTURE.md` — skill 架构真源。
- `docs/ORCHESTRATOR_PROMPT_CONTRACT.md` — prompt 协议真源。
- `docs/templates/*.md` — 模板层与案例层对象。
- `skills/**/SKILL.md` — 正式 skills 映射层对象。
- `docs/superpowers/specs/*.md` / `docs/superpowers/plans/*.md` — 过程文档层对象。

### New files to create

- `docs/superpowers/plans/2026-04-17-un9flow-consistency-cli-foundation.md` — 当前 implementation plan。
- `tools/validate_consistency.py` — 第一版单入口 Python 一致性校验 CLI。

### Optional follow-up files (only if complexity grows)

- `tools/validation/__init__.py`
- `tools/validation/check_docs.py`
- `tools/validation/check_skills.py`
- `tools/validation/check_templates.py`
- `tools/validation/check_routing_cases.py`
- `tools/validation/check_process_docs.py`

当前计划默认**不**创建 optional files；第一版先单文件实现。

---

### Task 1: 建立统一 findings 结构与 CLI 主流程

**Files:**
- Create: `tools/validate_consistency.py`
- Test: `tools/validate_consistency.py`

- [ ] **Step 1: 写出 CLI 骨架缺口清单**

```md
当前缺口：
- 仓库已有统一校验文档与模板，但没有实际可运行的本地校验器
- 需要一个统一 findings 数据结构承接五个检查器
- 需要固定的输出流程和退出码策略
```

- [ ] **Step 2: 运行检查，确认当前还没有 `tools/validate_consistency.py`**

Run: `ls tools 2>/dev/null || true && git ls-files "tools/validate_consistency.py"`
Expected: 无该文件

- [ ] **Step 3: 创建 `tools/validate_consistency.py` 的主骨架**

```python
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, List
import sys

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Finding:
    level: str
    category: str
    file: str
    summary: str
    why_it_matters: str
    suggested_action: str


def check_docs() -> list[Finding]:
    return []


def check_skills() -> list[Finding]:
    return []


def check_templates() -> list[Finding]:
    return []


def check_routing_cases() -> list[Finding]:
    return []


def check_process_docs() -> list[Finding]:
    return []


def group_findings(findings: list[Finding], level: str) -> list[Finding]:
    return [finding for finding in findings if finding.level == level]


def print_section(title: str, findings: list[Finding]) -> None:
    print(title)
    if not findings:
        print("- None")
        return
    for finding in findings:
        print(f"- [{finding.level}][{finding.category}] {finding.file}")
        print(f"  Summary: {finding.summary}")
        print(f"  Why it matters: {finding.why_it_matters}")
        print(f"  Suggested action: {finding.suggested_action}")


def compute_exit_code(findings: list[Finding]) -> int:
    has_l1 = any(f.level == "L1" for f in findings)
    has_l2 = any(f.level == "L2" for f in findings)
    if has_l1:
        return 1
    if has_l2:
        return 2
    return 0


def main() -> int:
    checks: list[Callable[[], list[Finding]]] = [
        check_docs,
        check_skills,
        check_templates,
        check_routing_cases,
        check_process_docs,
    ]

    findings: list[Finding] = []
    for check in checks:
        findings.extend(check())

    print("Validation scope:")
    print("- docs")
    print("- skills")
    print("- templates")
    print("- routing_cases")
    print("- process_docs")
    print()

    print_section("[L1] Blocking issues", group_findings(findings, "L1"))
    print()
    print_section("[L2] Important issues", group_findings(findings, "L2"))
    print()
    print_section("[L3] Cleanup issues", group_findings(findings, "L3"))
    print()

    exit_code = compute_exit_code(findings)
    print(f"Validation result: {'PASS' if exit_code == 0 else 'FAIL'}")
    print(f"- L1: {len(group_findings(findings, 'L1'))}")
    print(f"- L2: {len(group_findings(findings, 'L2'))}")
    print(f"- L3: {len(group_findings(findings, 'L3'))}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: 运行主骨架检查**

Run: `python tools/validate_consistency.py`
Expected: 输出 Validation scope、L1/L2/L3 三段和 Validation result；当前因为检查器全空，应返回 exit code 0

- [ ] **Step 5: Commit**

```bash
git add tools/validate_consistency.py
git commit -m "feat: add consistency validation cli skeleton"
```

---

### Task 2: 实现 docs / skills / templates 三个检查器

**Files:**
- Modify: `tools/validate_consistency.py`
- Test: `tools/validate_consistency.py`

- [ ] **Step 1: 写出第一批检查器目标清单**

```md
优先实现：
- docs 真源层：术语与真源边界检查
- skills 映射层：总入口/子入口/辅助 skill 越权检查
- 模板层：字段与允许值检查
```

- [ ] **Step 2: 实现 docs 检查器的最小规则**

```python
def check_docs() -> list[Finding]:
    findings: list[Finding] = []
    orchestration = (ROOT / "docs" / "ORCHESTRATION.md").read_text(encoding="utf-8")
    incident = (ROOT / "docs" / "INCIDENT_WORKFLOW.md").read_text(encoding="utf-8")
    skill_arch = (ROOT / "docs" / "SKILL_ARCHITECTURE.md").read_text(encoding="utf-8")
    prompt_contract = (ROOT / "docs" / "ORCHESTRATOR_PROMPT_CONTRACT.md").read_text(encoding="utf-8")

    required_terms = ["Scenario", "Phase", "Domain Specialist", "Artifact"]
    for term in required_terms:
        if term not in orchestration:
            findings.append(Finding(
                level="L1",
                category="docs",
                file="docs/ORCHESTRATION.md",
                summary=f"缺少术语 {term}",
                why_it_matters="主真源术语集合不完整会破坏全仓库一致性。",
                suggested_action=f"把 {term} 补回 ORCHESTRATION 真源定义。",
            ))

    if "incident-orchestrator" in orchestration and "场景内调度器示例" not in orchestration:
        findings.append(Finding(
            level="L1",
            category="docs",
            file="docs/ORCHESTRATION.md",
            summary="incident-orchestrator 角色未收紧为场景内示例",
            why_it_matters="会把场景内调度器误写成总路由唯一名字。",
            suggested_action="明确 incident-orchestrator 仅是 incident 场景内调度器示例。",
        ))

    if "docs/ORCHESTRATOR_PROMPT_CONTRACT.md" not in orchestration:
        findings.append(Finding(
            level="L2",
            category="docs",
            file="docs/ORCHESTRATION.md",
            summary="总调度文档未回指 prompt 契约文档",
            why_it_matters="总规则与协议边界可能再次混写。",
            suggested_action="补上对 ORCHESTRATOR_PROMPT_CONTRACT.md 的明确引用。",
        ))

    return findings
```

- [ ] **Step 3: 实现 skills 检查器的最小规则**

```python
def check_skills() -> list[Finding]:
    findings: list[Finding] = []
    orchestration_skill = (ROOT / "skills" / "orchestration" / "SKILL.md").read_text(encoding="utf-8")
    evidence_pack = (ROOT / "skills" / "evidence-pack" / "SKILL.md").read_text(encoding="utf-8")
    incident_review = (ROOT / "skills" / "incident-review" / "SKILL.md").read_text(encoding="utf-8")

    if "入口路由摘要" not in orchestration_skill:
        findings.append(Finding(
            level="L1",
            category="skills",
            file="skills/orchestration/SKILL.md",
            summary="总入口 skill 缺少路由摘要",
            why_it_matters="总入口无法和总真源形成摘要映射关系。",
            suggested_action="补上入口路由摘要小节。",
        ))

    if "不参与全局主路由竞争" not in evidence_pack:
        findings.append(Finding(
            level="L1",
            category="skills",
            file="skills/evidence-pack/SKILL.md",
            summary="evidence-pack 未声明退出全局主路由竞争",
            why_it_matters="辅助 skill 会越权抢入口。",
            suggested_action="补上不参与全局主路由竞争的限制。",
        ))

    if "不替代 `design-safety-review`" not in incident_review:
        findings.append(Finding(
            level="L2",
            category="skills",
            file="skills/incident-review/SKILL.md",
            summary="incident-review 与 design-safety-review 的边界不够清楚",
            why_it_matters="辅助 review skill 容易漂移成通用 review。",
            suggested_action="补上不替代 design-safety-review 的说明。",
        ))

    return findings
```

- [ ] **Step 4: 实现 templates 检查器的最小规则**

```python
def check_templates() -> list[Finding]:
    findings: list[Finding] = []
    findings_template = (ROOT / "docs" / "templates" / "validation-findings.md").read_text(encoding="utf-8")
    review_template = (ROOT / "docs" / "templates" / "consistency-review-checklist.md").read_text(encoding="utf-8")
    routing_matrix = (ROOT / "docs" / "templates" / "skill-routing-matrix.md").read_text(encoding="utf-8")

    if "L1 / L2 / L3" not in findings_template:
        findings.append(Finding(
            level="L1",
            category="templates",
            file="docs/templates/validation-findings.md",
            summary="validation-findings 模板缺少固定失败等级集合",
            why_it_matters="会破坏 findings 分级的一致性。",
            suggested_action="补上 L1 / L2 / L3 的固定允许值。",
        ))

    if "案例层模板" not in routing_matrix:
        findings.append(Finding(
            level="L2",
            category="templates",
            file="docs/templates/skill-routing-matrix.md",
            summary="routing matrix 模板未声明案例层角色",
            why_it_matters="模板角色不清会影响后续校验分层。",
            suggested_action="补一句说明其为案例层模板。",
        ))

    if "overall result" not in review_template:
        findings.append(Finding(
            level="L2",
            category="templates",
            file="docs/templates/consistency-review-checklist.md",
            summary="review checklist 缺少总体结论字段",
            why_it_matters="人工 review 结果无法稳定留痕。",
            suggested_action="补上 overall result 段。",
        ))

    return findings
```

- [ ] **Step 5: 运行第一批检查器验证**

Run: `python tools/validate_consistency.py`
Expected: 至少能输出 docs / skills / templates 三类 findings，且无语法错误；若当前仓库存在问题，应按 L1/L2/L3 正确分组输出

- [ ] **Step 6: Commit**

```bash
git add tools/validate_consistency.py
git commit -m "feat: add layered validation checks"
```

---

### Task 3: 实现 routing cases / process docs 检查器

**Files:**
- Modify: `tools/validate_consistency.py`
- Test: `tools/validate_consistency.py`

- [ ] **Step 1: 写出第二批检查器目标清单**

```md
补齐：
- routing cases 检查器
- process docs 检查器
```

- [ ] **Step 2: 实现 routing cases 检查器的最小规则**

```python
def check_routing_cases() -> list[Finding]:
    findings: list[Finding] = []
    routing_matrix = (ROOT / "docs" / "templates" / "skill-routing-matrix.md").read_text(encoding="utf-8")

    if "route decision" not in routing_matrix or "route type" not in routing_matrix:
        findings.append(Finding(
            level="L1",
            category="routing_cases",
            file="docs/templates/skill-routing-matrix.md",
            summary="routing matrix 缺少关键字段",
            why_it_matters="案例层无法稳定记录 route 判定。",
            suggested_action="补齐 route decision / route type。",
        ))

    if "incident 语义上下文" not in routing_matrix:
        findings.append(Finding(
            level="L2",
            category="routing_cases",
            file="docs/templates/skill-routing-matrix.md",
            summary="辅助 skill 的 incident 语义约束缺失",
            why_it_matters="evidence-pack / incident-review 可能被误写成全局路由结果。",
            suggested_action="补上 incident 语义上下文约束。",
        ))

    return findings
```

- [ ] **Step 3: 实现 process docs 检查器的最小规则**

```python
def check_process_docs() -> list[Finding]:
    findings: list[Finding] = []
    spec_dir = ROOT / "docs" / "superpowers" / "specs"
    plan_dir = ROOT / "docs" / "superpowers" / "plans"

    for path in list(spec_dir.glob("*.md")) + list(plan_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if "incident-orchestrator" in text and "场景内调度器示例" not in text and "场景内调度器" not in text:
            findings.append(Finding(
                level="L2",
                category="process_docs",
                file=str(path.relative_to(ROOT)).replace('\\', '/'),
                summary="过程文档中的 incident-orchestrator 角色表述可能落后于真源",
                why_it_matters="会误导后续实现继续使用旧层级关系。",
                suggested_action="把 incident-orchestrator 收紧为场景内调度器示例。",
            ))

        if "fallback-route-assumption-invalid" in text or "upgrade-to-incident-investigation" in text:
            pass

    return findings
```

- [ ] **Step 4: 运行全量检查器验证**

Run: `python tools/validate_consistency.py`
Expected: 五类检查器都参与输出；退出码按 L1/L2 情况返回 0/1/2 之一

- [ ] **Step 5: Commit**

```bash
git add tools/validate_consistency.py
git commit -m "feat: check routing cases and process docs"
```

---

### Task 4: 自审、验证与收口

**Files:**
- Modify: `tools/validate_consistency.py` (如需微调)
- Test: `tools/validate_consistency.py`

- [ ] **Step 1: 运行 placeholder 扫描**

Run: `grep -n "TODO\|TBD\|implement later\|fill in details" tools/validate_consistency.py`
Expected: 脚本中不应残留占位词

- [ ] **Step 2: 运行 Python 语法检查**

Run: `python -m py_compile tools/validate_consistency.py`
Expected: 无输出，退出码 0

- [ ] **Step 3: 运行脚本并记录退出码**

Run: `python tools/validate_consistency.py; echo EXIT:$?`
Expected: 输出 Validation scope / findings / Validation result，并打印 `EXIT:0`、`EXIT:1` 或 `EXIT:2`

- [ ] **Step 4: 检查 findings 结构是否完整**

Run: `grep -n "class Finding\|level: str\|category: str\|file: str\|summary: str\|why_it_matters: str\|suggested_action: str" tools/validate_consistency.py`
Expected: Finding 数据结构完整定义

- [ ] **Step 5: 检查退出码策略是否一致**

Run: `grep -n "return 1\|return 2\|return 0\|has_l1\|has_l2" tools/validate_consistency.py`
Expected: 退出码逻辑与设计一致

- [ ] **Step 6: 如发现问题，做最小修正**

```md
允许的修正类型：
- 统一 findings 字段命名
- 修正检查器分类或输出顺序
- 修正退出码逻辑
- 修正路径定位错误
```

- [ ] **Step 7: 重新运行关键检查确认收口**

Run: `python -m py_compile tools/validate_consistency.py && python tools/validate_consistency.py; echo EXIT:$?`
Expected: 语法检查通过，脚本稳定输出结果并返回 0/1/2

- [ ] **Step 8: Commit**

```bash
git add tools/validate_consistency.py
git commit -m "feat: finalize consistency validation cli baseline"
```

---

## Self-Review

### Spec coverage

- 规格第 2 节 CLI 整体结构：Task 1 覆盖
- 规格第 3 节五个检查器：Task 2、Task 3 覆盖
- 规格第 4 节统一 findings 结构：Task 1 覆盖
- 规格第 5 节输出流程与退出码：Task 1、Task 4 覆盖
- 规格第 6 节最终落点与实现顺序：Task 1、Task 2、Task 3 覆盖

### Placeholder scan

本计划没有使用 “TBD / TODO / implement later / similar to Task N” 作为执行步骤占位语，所有步骤都包含明确文件、命令或代码内容。

### Type consistency

计划中统一使用以下关键名词：

- CLI 入口：`tools/validate_consistency.py`
- 检查器：`check_docs` / `check_skills` / `check_templates` / `check_routing_cases` / `check_process_docs`
- findings 字段：`level` / `category` / `file` / `summary` / `why_it_matters` / `suggested_action`
- 退出码：`0` / `1` / `2`

未使用冲突命名。