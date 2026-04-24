# Generation Regression Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 un9flow 的两个已声明生成对象建立最小且严格的 golden-file 输出回归基线，并接入现有 CI 门禁。

**Architecture:** 本轮继续沿用 `docs/TEMPLATE_GENERATION.md` 作为生成约定真源、现有两个生成器作为执行入口，并新增一条独立但最小的 generation regression 线。输入样例与 golden 输出分离存放，统一由 `tools/run_generation_regression.py` 调度；本地允许显式 `--update-golden`，CI 永远只做 check-only 校验。

**Tech Stack:** Markdown, Python 3.11, GitHub Actions（existing）, git, Claude Code

---

## File Structure

### Existing files to modify

- `docs/CONSISTENCY_VALIDATION.md` — 增加 generation regression 的职责定位与最小门禁说明。
- `docs/ROADMAP.md` — 将 v4 中“更完整的输出回归校验”更新为已落地。
- `.github/workflows/consistency-validation.yml` — 在现有 workflow 中追加 generation regression check 步骤。

### Existing files to read but not modify

- `docs/TEMPLATE_GENERATION.md`
- `tools/generate_watchdog_timeout_audit_report.py`
- `tools/generate_incident_case_bundle.py`
- `tools/generation_core.py`
- `docs/templates/watchdog-timeout-audit-findings.md`
- `docs/templates/timing-watchdog-audit-pack.md`
- `docs/templates/skill-routing-matrix.md`
- `docs/templates/orchestrator-dispatch-plan.md`
- `docs/templates/incident-summary.md`
- `docs/templates/evidence-package.md`
- `docs/templates/incident-diagnosis-pack.md`
- `docs/templates/incident-review-memo.md`

### New files to create

- `docs/golden-inputs/watchdog-timeout-audit-report/minimal/findings.md`
- `docs/golden-inputs/watchdog-timeout-audit-report/minimal/pack.md`
- `docs/golden-inputs/incident-case-bundle/minimal/case-metadata.md`
- `docs/golden-outputs/watchdog-timeout-audit-report/minimal/watchdog-timeout-audit-report.md`
- `docs/golden-outputs/incident-case-bundle/minimal/README.md`
- `docs/golden-outputs/incident-case-bundle/minimal/01-skill-routing-matrix.md`
- `docs/golden-outputs/incident-case-bundle/minimal/02-orchestrator-dispatch-plan.md`
- `docs/golden-outputs/incident-case-bundle/minimal/03-incident-summary.md`
- `docs/golden-outputs/incident-case-bundle/minimal/04-evidence-package.md`
- `docs/golden-outputs/incident-case-bundle/minimal/05-incident-diagnosis-pack.md`
- `docs/golden-outputs/incident-case-bundle/minimal/06-incident-review-memo.md`
- `tools/run_generation_regression.py`
- `docs/superpowers/plans/2026-04-24-generation-regression-foundation.md`

### No new test framework

本计划不引入 pytest / snapshot 框架，也不新增独立 workflow 文件；只使用 Python 脚本与现有 GitHub Actions workflow。

---

### Task 1: 先写 generation regression runner 的失败校验

**Files:**
- Create: `tools/run_generation_regression.py`
- Test: `tools/run_generation_regression.py`

- [ ] **Step 1: 创建只包含 CLI 骨架和“样例缺失即失败”的 runner**

```python
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_OBJECTS = (
    "watchdog-timeout-audit-report",
    "incident-case-bundle",
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run generation regression checks.")
    parser.add_argument("--object", choices=ALLOWED_OBJECTS)
    parser.add_argument("--case", default=None)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--update-golden", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    selected_case = args.case or "minimal"
    selected_object = args.object or "watchdog-timeout-audit-report"
    sample_dir = ROOT / "docs" / "golden-inputs" / selected_object / selected_case
    if not sample_dir.exists():
        print(f"Missing golden input sample: {sample_dir}", file=sys.stderr)
        return 2
    print("placeholder")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: 运行最小命令，确认在样例不存在时先失败**

Run: `python tools/run_generation_regression.py --object watchdog-timeout-audit-report --case minimal --check`
Expected: FAIL，stderr 包含 `Missing golden input sample:`

- [ ] **Step 3: 提交 runner 骨架**

```bash
git add tools/run_generation_regression.py
git commit -m "test: add failing generation regression runner skeleton"
```

---

### Task 2: 为 watchdog report 建立最小 golden 输入与 golden 输出

**Files:**
- Create: `docs/golden-inputs/watchdog-timeout-audit-report/minimal/findings.md`
- Create: `docs/golden-inputs/watchdog-timeout-audit-report/minimal/pack.md`
- Create: `docs/golden-outputs/watchdog-timeout-audit-report/minimal/watchdog-timeout-audit-report.md`
- Test: `tools/generate_watchdog_timeout_audit_report.py`

- [ ] **Step 1: 写入 watchdog minimal findings 样例**

```md
# watchdog-timeout-audit-findings

## audit summary
- 主循环喂狗依赖单一通信分支，超时退化路径不完整。

## key findings
- `feed_watchdog()` 仅在 CAN 正常时调用。
- 超时恢复与 failsafe 进入条件未对齐。

## risk assessment
- 可能出现通信中断后看门狗复位先于受控降级。

## recommended actions
- 将喂狗前提从“通信成功”改为“主循环活性 + 安全条件成立”。

## verification gaps
- 缺少故障注入日志与 reset 前最后一次调度证据。
```

- [ ] **Step 2: 写入 watchdog minimal pack 样例**

```md
# timing-watchdog-audit-pack

## evidence used
- `main_loop.c`: watchdog feed path
- `can_timeout.c`: bus-off timeout handling
- `diag_log.txt`: reset before failsafe transition
```

- [ ] **Step 3: 用现有生成器生成一次 golden 候选输出**

Run: `python tools/generate_watchdog_timeout_audit_report.py --findings docs/golden-inputs/watchdog-timeout-audit-report/minimal/findings.md --pack docs/golden-inputs/watchdog-timeout-audit-report/minimal/pack.md --output docs/golden-outputs/watchdog-timeout-audit-report/minimal/watchdog-timeout-audit-report.md`
Expected: PASS，生成 `watchdog-timeout-audit-report.md`

- [ ] **Step 4: 读取生成出的 golden 文件并核对固定段落存在**

Run: `python -c "from pathlib import Path; text = Path('docs/golden-outputs/watchdog-timeout-audit-report/minimal/watchdog-timeout-audit-report.md').read_text(encoding='utf-8'); required = ['## audit summary', '## key findings', '## evidence highlights', '## risk assessment', '## recommended actions', '## verification gaps']; missing = [item for item in required if item not in text]; print('OK' if not missing else missing)"`
Expected: `OK`

- [ ] **Step 5: 提交 watchdog golden 样例**

```bash
git add docs/golden-inputs/watchdog-timeout-audit-report/minimal/findings.md docs/golden-inputs/watchdog-timeout-audit-report/minimal/pack.md docs/golden-outputs/watchdog-timeout-audit-report/minimal/watchdog-timeout-audit-report.md
git commit -m "test: add watchdog generation golden sample"
```

---

### Task 3: 为 incident case bundle 建立最小 golden 输入与 golden 输出

**Files:**
- Create: `docs/golden-inputs/incident-case-bundle/minimal/case-metadata.md`
- Create: `docs/golden-outputs/incident-case-bundle/minimal/README.md`
- Create: `docs/golden-outputs/incident-case-bundle/minimal/01-skill-routing-matrix.md`
- Create: `docs/golden-outputs/incident-case-bundle/minimal/02-orchestrator-dispatch-plan.md`
- Create: `docs/golden-outputs/incident-case-bundle/minimal/03-incident-summary.md`
- Create: `docs/golden-outputs/incident-case-bundle/minimal/04-evidence-package.md`
- Create: `docs/golden-outputs/incident-case-bundle/minimal/05-incident-diagnosis-pack.md`
- Create: `docs/golden-outputs/incident-case-bundle/minimal/06-incident-review-memo.md`
- Test: `tools/generate_incident_case_bundle.py`

- [ ] **Step 1: 写入 incident bundle minimal metadata 样例**

```md
# case metadata

- case id: `case-001`
- case title: `Minimal incident routing regression`
- primary scenario: `incident-investigation`
```

- [ ] **Step 2: 用现有生成器生成 bundle golden 候选输出**

Run: `python tools/generate_incident_case_bundle.py case-001 --title "Minimal incident routing regression" --scenario incident-investigation --output-root docs/golden-outputs/incident-case-bundle --force`
Expected: PASS，生成目录 `docs/golden-outputs/incident-case-bundle/case-001/`

- [ ] **Step 3: 把生成目录重命名为 `minimal/` 作为固定 golden root**

Run: `python -c "from pathlib import Path; import shutil; src = Path('docs/golden-outputs/incident-case-bundle/case-001'); dst = Path('docs/golden-outputs/incident-case-bundle/minimal'); shutil.rmtree(dst, ignore_errors=True); shutil.move(str(src), str(dst))"`
Expected: PASS，生成目录为 `docs/golden-outputs/incident-case-bundle/minimal/`

- [ ] **Step 4: 校验 bundle 中文件集合严格完整**

Run: `python -c "from pathlib import Path; expected = sorted(['README.md', '01-skill-routing-matrix.md', '02-orchestrator-dispatch-plan.md', '03-incident-summary.md', '04-evidence-package.md', '05-incident-diagnosis-pack.md', '06-incident-review-memo.md']); actual = sorted(path.name for path in Path('docs/golden-outputs/incident-case-bundle/minimal').iterdir() if path.is_file()); print('OK' if actual == expected else {'expected': expected, 'actual': actual})"`
Expected: `OK`

- [ ] **Step 5: 提交 incident bundle golden 样例**

```bash
git add docs/golden-inputs/incident-case-bundle/minimal/case-metadata.md docs/golden-outputs/incident-case-bundle/minimal/README.md docs/golden-outputs/incident-case-bundle/minimal/01-skill-routing-matrix.md docs/golden-outputs/incident-case-bundle/minimal/02-orchestrator-dispatch-plan.md docs/golden-outputs/incident-case-bundle/minimal/03-incident-summary.md docs/golden-outputs/incident-case-bundle/minimal/04-evidence-package.md docs/golden-outputs/incident-case-bundle/minimal/05-incident-diagnosis-pack.md docs/golden-outputs/incident-case-bundle/minimal/06-incident-review-memo.md
git commit -m "test: add incident bundle generation golden sample"
```

---

### Task 4: 实现 check-only 比对与 `--update-golden`

**Files:**
- Modify: `tools/run_generation_regression.py`
- Test: `tools/run_generation_regression.py`

- [ ] **Step 1: 为 watchdog report 实现单文件严格比对**

```python
def compare_file(actual_path: Path, golden_path: Path) -> list[str]:
    if not golden_path.exists():
        return [f"Missing golden file: {golden_path}"]
    actual_text = actual_path.read_text(encoding="utf-8")
    golden_text = golden_path.read_text(encoding="utf-8")
    if actual_text == golden_text:
        return []
    return [f"Content mismatch: {golden_path}"]
```

- [ ] **Step 2: 为 incident bundle 实现目录结构与内容严格比对**

```python
def compare_bundle(actual_dir: Path, golden_dir: Path) -> list[str]:
    expected_files = sorted(path.relative_to(golden_dir).as_posix() for path in golden_dir.rglob('*') if path.is_file())
    actual_files = sorted(path.relative_to(actual_dir).as_posix() for path in actual_dir.rglob('*') if path.is_file())
    if actual_files != expected_files:
        return [f"Bundle file set mismatch: expected={expected_files}, actual={actual_files}"]
    mismatches: list[str] = []
    for relative_name in expected_files:
        actual_text = (actual_dir / relative_name).read_text(encoding='utf-8')
        golden_text = (golden_dir / relative_name).read_text(encoding='utf-8')
        if actual_text != golden_text:
            mismatches.append(f"Bundle content mismatch: {relative_name}")
    return mismatches
```

- [ ] **Step 3: 为两个对象补上生成与分发逻辑，并默认执行 check-only**

```python
if args.update_golden and args.check:
    print("Cannot combine --check and --update-golden", file=sys.stderr)
    return 2
mode = "update" if args.update_golden else "check"
print(f"Running generation regression in {mode} mode")
```

并在对象分发中使用：

```python
if object_name == "watchdog-timeout-audit-report":
    # 调用 generate_watchdog_timeout_audit_report.py 生成临时文件
elif object_name == "incident-case-bundle":
    # 调用 generate_incident_case_bundle.py 生成临时目录
```

- [ ] **Step 4: 运行 watchdog check-only regression**

Run: `python tools/run_generation_regression.py --object watchdog-timeout-audit-report --case minimal --check`
Expected: PASS，stdout 包含 `PASS watchdog-timeout-audit-report/minimal`

- [ ] **Step 5: 运行 incident bundle check-only regression**

Run: `python tools/run_generation_regression.py --object incident-case-bundle --case minimal --check`
Expected: PASS，stdout 包含 `PASS incident-case-bundle/minimal`

- [ ] **Step 6: 运行全量 check-only regression**

Run: `python tools/run_generation_regression.py --check`
Expected: PASS，stdout 包含两个对象的 PASS 结果

- [ ] **Step 7: 运行 watchdog `--update-golden` 验证显式更新路径可用**

Run: `python tools/run_generation_regression.py --object watchdog-timeout-audit-report --case minimal --update-golden`
Expected: PASS，stdout 包含 `UPDATED watchdog-timeout-audit-report/minimal`

- [ ] **Step 8: 提交 regression runner 完整实现**

```bash
git add tools/run_generation_regression.py
git commit -m "feat: add generation regression runner"
```

---

### Task 5: 接入文档与 CI 门禁

**Files:**
- Modify: `docs/CONSISTENCY_VALIDATION.md`
- Modify: `docs/ROADMAP.md`
- Modify: `.github/workflows/consistency-validation.yml`
- Test: `tools/validate_consistency.py`
- Test: `tools/run_generation_regression.py`

- [ ] **Step 1: 在 `docs/CONSISTENCY_VALIDATION.md` 增加 generation regression 职责定位**

```md
## generation regression 补充约定

- generation regression 用于校验“给定输入 → 生成输出”是否稳定。
- 首批仅覆盖：
  - `watchdog-timeout-audit-report`
  - `incident case bundle`
- golden files 可在本地显式刷新，但 CI 仅允许 check-only。
- generation regression 不替代 consistency validation；两者并列服务 docs 真源。
```

- [ ] **Step 2: 在 `docs/ROADMAP.md` 将 v4 输出回归项标记为已完成**

```md
- [x] 更完整的输出回归校验基线已落地：golden files first、最小 regression runner、watchdog report / incident case bundle 输出稳定性校验已接入
```

- [ ] **Step 3: 在现有 workflow 中追加 generation regression check 步骤**

```yaml
      - name: Run generation regression
        if: steps.changes.outputs.has_relevant_changes == 'true'
        run: python tools/run_generation_regression.py --check
```

把这个步骤放在 `Run consistency validation` 之后，`Skip consistency validation when no relevant changes` 之前。

- [ ] **Step 4: 运行 consistency validation，确认文档与对象关系仍通过**

Run: `python tools/validate_consistency.py`
Expected: `Validation result: PASS`

- [ ] **Step 5: 重新运行 generation regression 全量校验**

Run: `python tools/run_generation_regression.py --check`
Expected: PASS

- [ ] **Step 6: 提交文档与 CI 接入**

```bash
git add docs/CONSISTENCY_VALIDATION.md docs/ROADMAP.md .github/workflows/consistency-validation.yml
git commit -m "ci: enforce generation regression checks"
```

---

### Task 6: 做一次端到端验收

**Files:**
- Test: `tools/validate_consistency.py`
- Test: `tools/run_generation_regression.py`
- Test: `.github/workflows/consistency-validation.yml`

- [ ] **Step 1: 运行 consistency validation 最终验收**

Run: `python tools/validate_consistency.py`
Expected: `Validation result: PASS`

- [ ] **Step 2: 运行 generation regression 最终验收**

Run: `python tools/run_generation_regression.py --check`
Expected: PASS，且两个对象都打印 PASS

- [ ] **Step 3: 检查 workflow 文件已包含两条门禁命令**

Run: `python -c "from pathlib import Path; text = Path('.github/workflows/consistency-validation.yml').read_text(encoding='utf-8'); required = ['python tools/validate_consistency.py', 'python tools/run_generation_regression.py --check']; missing = [item for item in required if item not in text]; print('OK' if not missing else missing)"`
Expected: `OK`

- [ ] **Step 4: 提交最终验收结果**

```bash
git add tools/run_generation_regression.py docs/golden-inputs docs/golden-outputs docs/CONSISTENCY_VALIDATION.md docs/ROADMAP.md .github/workflows/consistency-validation.yml
git commit -m "feat: add generation regression foundation"
```

---

## Self-Review

- **Spec coverage:** 本计划覆盖了 spec 中的范围限制、目录布局、CLI 形态、`--update-golden` 边界、单文件 / bundle 严格比对、失败输出定位、本地与 CI 分工，以及 roadmap/consistency 文档与 CI 接入。
- **Placeholder scan:** 已移除 `TBD`、`TODO`、`later`、`appropriate` 等占位措辞；每个代码步骤都给了明确代码或命令。
- **Type consistency:** 对象名统一为 `watchdog-timeout-audit-report` 与 `incident-case-bundle`；runner 文件路径、golden 路径、CLI 参数名在所有任务中保持一致。
