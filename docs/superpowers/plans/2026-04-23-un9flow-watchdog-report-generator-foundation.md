# Watchdog Report Generator Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 un9flow 增加一个本地 watchdog 自动报告生成器，读取 findings 为主、pack 为补充，输出填充后的 watchdog 报告文档，并将该生成器对象纳入现有方法真源、一致性校验与路线图语义中。

**Architecture:** 本轮不新增新的 workflow 或自动裁决器，而是在现有 `watchdog-timeout-audit-report` 模板之上新增一个本地 Python 生成脚本 `tools/generate_watchdog_timeout_audit_report.py`。脚本只做结构化汇总：主输入是 `watchdog-timeout-audit-findings.md`，补充输入是 `timing-watchdog-audit-pack.md`，输出一份 markdown 报告；现有 `.github/workflows/consistency-validation.yml` 继续不改结构，仍通过 `python tools/validate_consistency.py` 自动纳管新增对象。

**Tech Stack:** Python 3, Markdown, GitHub Actions（existing）, git, Claude Code

---

## File Structure

### Existing files to modify

- `docs/WATCHDOG_TIMEOUT_AUDIT.md` — 补充对 watchdog 报告生成器脚本的回指，并明确 report 模板与生成器的关系。
- `docs/CONSISTENCY_VALIDATION.md` — 增加 watchdog 报告生成器脚本的一致性规则。
- `tools/validate_consistency.py` — 增加 watchdog 报告生成器脚本的存在性与回指检查。
- `docs/ROADMAP.md` — 把“真正的自动报告生成器”从未开始推进到已落地基线。
- `README.md`（仅当需要）— 若 watchdog 报告生成器需要对外入口，则补最小入口说明。

### Existing files to read but not modify

- `docs/templates/watchdog-timeout-audit-report.md` — 最终专项报告模板。
- `docs/templates/watchdog-timeout-audit-findings.md` — 主输入模板。
- `docs/templates/timing-watchdog-audit-pack.md` — 补充输入模板。
- `skills/watchdog-timeout-audit/SKILL.md` — watchdog formal skill，继续作为 watchdog 专项入口。
- `.github/workflows/consistency-validation.yml` — 现有最小门禁 workflow，本计划不改变其结构。

### New files to create

- `tools/generate_watchdog_timeout_audit_report.py` — watchdog 自动报告生成器。
- `docs/superpowers/plans/2026-04-23-un9flow-watchdog-report-generator-foundation.md` — 当前 implementation plan。

### No new CI/workflow files

本计划不新增新的 GitHub workflow，也不新增自动风险分级引擎或自动裁决器。

---

### Task 1: 先把 watchdog 报告生成器规则写成失败校验

**Files:**
- Modify: `docs/CONSISTENCY_VALIDATION.md`
- Modify: `tools/validate_consistency.py`
- Test: `tools/validate_consistency.py`

- [ ] **Step 1: 在 `docs/CONSISTENCY_VALIDATION.md` 增加 watchdog 报告生成器规则**

```md
在 watchdog / timeout 相关规则段下补充明确约束：

- `tools/generate_watchdog_timeout_audit_report.py` 是 watchdog 自动报告生成器脚本。
- `tools/generate_watchdog_timeout_audit_report.py` 必须显式依赖：
  - `docs/templates/watchdog-timeout-audit-findings.md`
  - `docs/templates/timing-watchdog-audit-pack.md`
  - `docs/templates/watchdog-timeout-audit-report.md`
- `tools/generate_watchdog_timeout_audit_report.py` 必须体现：
  - findings 为主输入
  - pack 为补充输入
  - 输出为 markdown 报告文件
- `docs/WATCHDOG_TIMEOUT_AUDIT.md` 必须补充对 watchdog 报告生成器脚本的回指。
```

- [ ] **Step 2: 在 `tools/validate_consistency.py` 增加 watchdog 报告生成器失败检查**

```python
# 在 docs 检查中加入 WATCHDOG_TIMEOUT_AUDIT 对生成器脚本的回指检查
if watchdog_timeout_content is not None and "tools/generate_watchdog_timeout_audit_report.py" not in watchdog_timeout_content:
    findings.append(
        Finding(
            level="L2",
            category="docs",
            file=watchdog_timeout_label,
            summary="watchdog 方法真源缺少报告生成器脚本回指。",
            why_it_matters="方法真源若不回指 watchdog 报告生成器脚本，report 模板与自动生成能力之间就无法形成稳定映射。",
            suggested_action="在 docs/WATCHDOG_TIMEOUT_AUDIT.md 中补齐 tools/generate_watchdog_timeout_audit_report.py 的引用。",
        )
    )

# 在 process/tools 层增加生成器脚本检查
generator_label = "tools/generate_watchdog_timeout_audit_report.py"
generator_path = ROOT / "tools" / "generate_watchdog_timeout_audit_report.py"
generator_content = _read_text(generator_path)
if generator_content is None:
    findings.append(
        Finding(
            level="L1",
            category="process_docs",
            file=generator_label,
            summary="watchdog 报告生成器脚本缺失或无法读取。",
            why_it_matters="若缺少实际生成器脚本，watchdog 自动报告能力仍停留在模板层，无法真正把 findings + pack 汇总成报告。",
            suggested_action="创建 tools/generate_watchdog_timeout_audit_report.py 并确保 UTF-8 可读。",
        )
    )
else:
    missing_generator_refs = _find_missing_semantics(
        generator_content,
        {
            "findings input ref": "watchdog-timeout-audit-findings",
            "pack input ref": "timing-watchdog-audit-pack",
            "report output ref": "watchdog-timeout-audit-report",
        },
    )
    if missing_generator_refs:
        findings.append(
            Finding(
                level="L2",
                category="process_docs",
                file=generator_label,
                summary=f"watchdog 报告生成器脚本缺少输入/输出锚点：{', '.join(missing_generator_refs)}。",
                why_it_matters="若脚本不显式体现 findings 为主输入、pack 为补充输入以及 report 输出，自动报告能力的边界就会重新变得不可判定。",
                suggested_action="在 tools/generate_watchdog_timeout_audit_report.py 中补齐 findings、pack、report 三类输入输出锚点。",
            )
        )
```

- [ ] **Step 3: 运行 CLI，确认 watchdog 报告生成器规则先失败**

Run: `python tools/validate_consistency.py`
Expected: `Validation result: FAIL`，且至少出现指向以下对象的 findings：
- `tools/generate_watchdog_timeout_audit_report.py`
- `docs/WATCHDOG_TIMEOUT_AUDIT.md`

---

### Task 2: 新增 watchdog 报告生成器脚本并让校验转绿

**Files:**
- Create: `tools/generate_watchdog_timeout_audit_report.py`
- Modify: `docs/WATCHDOG_TIMEOUT_AUDIT.md`
- Test: `tools/validate_consistency.py`

- [ ] **Step 1: 创建 `tools/generate_watchdog_timeout_audit_report.py`**

```python
from pathlib import Path
import argparse

REPORT_TEMPLATE_HEADER = "# watchdog-timeout-audit-report"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_section(text: str, heading: str) -> str:
    marker = f"## {heading}"
    if marker not in text:
        return ""
    tail = text.split(marker, 1)[1]
    next_heading_index = tail.find("\n## ")
    if next_heading_index == -1:
        return tail.strip()
    return tail[:next_heading_index].strip()


def generate_report(findings_text: str, pack_text: str) -> str:
    key_findings = extract_section(findings_text, "findings")
    evidence_highlights = extract_section(pack_text, "evidence used") if pack_text else ""
    verification_gaps = extract_section(pack_text, "unresolved gaps") if pack_text else ""
    recommended_actions = "- action-001:\n- action-002:"
    if "next action:" in findings_text:
        recommended_actions = "\n".join(
            line for line in findings_text.splitlines() if "next action:" in line or line.strip().startswith("-")
        ).strip() or recommended_actions

    return f"""# watchdog-timeout-audit-report

- 方法真源：`docs/WATCHDOG_TIMEOUT_AUDIT.md`
- 主输入：`docs/templates/watchdog-timeout-audit-findings.md`
- 补充输入：`docs/templates/timing-watchdog-audit-pack.md`

## audit summary
- 审计对象:
- 审计范围:
- 总体结论:
- 当前总体风险等级:

## key findings
{key_findings}

## evidence highlights
{evidence_highlights or '- timing baseline:\n- watchdog feed path:\n- blocking / starvation:\n- reset chain:\n- failsafe convergence:\n- ISR / main loop conflict:'}

## risk assessment
- confirmed risks:
- unresolved risks:
- impact on bring-up / release / safety review:

## recommended actions
{recommended_actions}

## verification gaps
{verification_gaps or '- gap-001:\n- gap-002:'}
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--findings", required=True)
    parser.add_argument("--pack", required=False)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    findings_path = Path(args.findings)
    pack_path = Path(args.pack) if args.pack else None
    output_path = Path(args.output)

    findings_text = read_text(findings_path)
    pack_text = read_text(pack_path) if pack_path is not None else ""
    report_text = generate_report(findings_text, pack_text)
    output_path.write_text(report_text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: 在 `docs/WATCHDOG_TIMEOUT_AUDIT.md` 补生成器脚本回指**

```md
在与模板 / skill / 主场景的关系段或分工段补充：
- 报告生成器脚本：`tools/generate_watchdog_timeout_audit_report.py`

并说明：
- 该脚本以 `watchdog-timeout-audit-findings` 为主输入、`timing-watchdog-audit-pack` 为补充输入，生成最终 watchdog 报告。
```

- [ ] **Step 3: 运行 CLI，确认 watchdog 报告生成器校验通过**

Run: `python tools/validate_consistency.py`
Expected: `Validation result: PASS`

---

### Task 3: 同步路线图并把报告生成器纳入现有门禁语义

**Files:**
- Modify: `docs/ROADMAP.md`
- Modify: `README.md`（如需入口）
- Test: `docs/ROADMAP.md`
- Test: `README.md`
- Test: `tools/validate_consistency.py`

- [ ] **Step 1: 在 `docs/ROADMAP.md` 把 watchdog 自动报告生成器标记为已落地基线**

```md
将：
- [ ] 更重型 watchdog 专项 workflow / 真正的自动报告生成器留待后续阶段扩展

改成更精确状态，例如：
- [x] watchdog 自动报告生成器基线已落地：`tools/generate_watchdog_timeout_audit_report.py` 已接入现有对象体系并受 consistency / CI 门禁约束
- [ ] 更重型 watchdog 专项 workflow 仍留待后续阶段扩展
```

- [ ] **Step 2: 如需要，在 `README.md` 增加 watchdog 报告生成器入口**

```md
- `tools/generate_watchdog_timeout_audit_report.py`：以 findings 为主输入、pack 为补充输入的 watchdog 自动报告生成器
```

- [ ] **Step 3: 运行最小文本检查**

Run: `grep -n "generate_watchdog_timeout_audit_report" README.md docs/ROADMAP.md docs/WATCHDOG_TIMEOUT_AUDIT.md tools/generate_watchdog_timeout_audit_report.py`
Expected: 若 README 被修改，则 4 个文件都命中；若 README 未修改，则其余 3 个文件命中且 `ROADMAP` 已更新

- [ ] **Step 4: 再跑一次 consistency CLI，确认现有门禁已覆盖新增对象**

Run: `python tools/validate_consistency.py`
Expected: `Validation result: PASS`

- [ ] **Step 5: 提交本轮 watchdog 报告生成器基线**

```bash
git add docs/WATCHDOG_TIMEOUT_AUDIT.md docs/CONSISTENCY_VALIDATION.md docs/ROADMAP.md README.md tools/generate_watchdog_timeout_audit_report.py tools/validate_consistency.py
git commit -m "feat: add watchdog report generator"
```

---

## Verification Notes

- 本计划不新增 GitHub workflow；报告生成器在 CI 层的实现方式，是让现有 `consistency-validation.yml` 通过扩展后的 `tools/validate_consistency.py` 覆盖生成器对象。
- 生成器不是自动风险判定器，也不替代 findings / pack / report 模板。
- findings 仍是主输入，pack 仍是补充输入；若实现中出现反向依赖或角色混淆，必须回退。