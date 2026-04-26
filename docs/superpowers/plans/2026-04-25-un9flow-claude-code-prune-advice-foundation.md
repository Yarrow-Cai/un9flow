# Claude Code Prune Advice Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 `tools/sync_claude_code_skills.py` 增加 `--prune-advice`，在不删除任何文件的前提下，对 stale target 给出最小清理建议。

**Architecture:** 本轮只做 prune advice 的只读建议层，不做删除、不输出删除命令、不和 `--only` 叠加，也不扩展到 docs/templates/cases。脚本保持现有五层语义分工：inspect 盘点 source→target、dry-run 预演动作、sync 执行写入、stale-check 识别 stale、prune-advice 针对 stale 给出 `consider-cleanup` 最小建议。

**Tech Stack:** Python 3, pathlib, argparse, shutil, git, unittest, Claude Code

---

## File Structure

### Existing files to modify

- `tools/sync_claude_code_skills.py` — 增加 `--prune-advice` 模式与输出。
- `tools/test_sync_claude_code_skills.py` — 增加 prune advice 的最小行为测试。
- `docs/CLAUDE_CODE_SETUP.md` — 把 prune advice 登记为“先识别 stale target，再考虑是否手动清理”的辅助动作。
- `docs/CONSISTENCY_VALIDATION.md`（如需要最小规则登记）— 若要把 prune advice 边界纳入现有规则，则补最小约束。
- `docs/ROADMAP.md`（如需要阶段落地记录）— 若要把 prune advice 记为下一阶段落地点，则补最小路线图记录。

### Existing files to read but not modify

- `docs/CLAUDE_CODE_HOST.md`
- `docs/PLATFORMS.md`
- `skills/**/SKILL.md`

### New files to create

- `docs/superpowers/plans/2026-04-25-un9flow-claude-code-prune-advice-foundation.md` — 当前 implementation plan。

### No deletion behavior

本计划不新增 prune、delete、clean 或任何自动删除动作。

---

### Task 1: 给同步脚本增加 `--prune-advice` 模式

**Files:**
- Modify: `tools/sync_claude_code_skills.py`
- Modify: `tools/test_sync_claude_code_skills.py`
- Test: `tools/sync_claude_code_skills.py`
- Test: `tools/test_sync_claude_code_skills.py`

- [ ] **Step 1: 在参数解析中增加 `--prune-advice`，并与 `--stale-check`、`--inspect`、`--dry-run`、`--force`、`--only` 互斥**

```python
parser.add_argument(
    "--prune-advice",
    action="store_true",
    help="Report stale target skills that can be considered for manual cleanup.",
)
```

并在主入口中加入：

```python
if args.prune_advice and args.stale_check:
    print("Cannot combine --prune-advice and --stale-check.", file=sys.stderr)
    return 2
if args.prune_advice and args.inspect:
    print("Cannot combine --prune-advice and --inspect.", file=sys.stderr)
    return 2
if args.prune_advice and args.dry_run:
    print("Cannot combine --prune-advice and --dry-run.", file=sys.stderr)
    return 2
if args.prune_advice and args.force:
    print("Cannot combine --prune-advice and --force.", file=sys.stderr)
    return 2
if args.prune_advice and args.only is not None:
    print("Cannot combine --prune-advice and --only.", file=sys.stderr)
    return 2
```

- [ ] **Step 2: 增加 prune advice 输出函数，只列出 stale 对象**

```python
def prune_advice_skill_files(source_skill_files: list[Path], target_root: Path) -> int:
    target_skill_files = discover_target_skill_files(target_root)
    managed_targets = {
        target_path_for(skill_file, target_root).resolve() for skill_file in source_skill_files
    }

    stale_targets = [
        target_skill_file
        for target_skill_file in target_skill_files
        if target_skill_file.resolve() not in managed_targets
    ]

    print("PRUNE-ADVICE")
    print(f"TARGET ROOT: {display_path(target_root)}")
    print(f"TOTAL TARGET SKILLS: {len(target_skill_files)}")
    print(f"STALE TARGETS: {len(stale_targets)}")

    for stale_target in stale_targets:
        print(f"- {stale_target.parent.name}")
        print(f"  target: {display_path(stale_target)}")
        print("  status: stale")
        print("  advice: consider-cleanup")

    print("SUMMARY")
    print(f"- total: {len(target_skill_files)}")
    print(f"- stale: {len(stale_targets)}")
    print(f"- consider-cleanup: {len(stale_targets)}")
    return 0
```

- [ ] **Step 3: 在主入口中接入 prune-advice 分支**

```python
if args.prune_advice:
    return prune_advice_skill_files(source_skill_files=all_skill_files, target_root=target_root)
```

- [ ] **Step 4: 增加最小测试覆盖**

```python
def test_prune_advice_reports_only_stale_targets(self) -> None:
    ...

def test_prune_advice_conflicts_with_stale_check(self) -> None:
    ...

def test_prune_advice_conflicts_with_only(self) -> None:
    ...
```

- [ ] **Step 5: 运行 prune-advice 空目标验收**

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --prune-advice`
Expected:
- `PRUNE-ADVICE`
- `TOTAL TARGET SKILLS: 0`
- `STALE TARGETS: 0`
- `SUMMARY`
- `stale: 0`
- `consider-cleanup: 0`

- [ ] **Step 6: 运行 prune-advice stale 目标验收**

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --force`
Run: `python -c "from pathlib import Path; stale = Path('.claude-sync-preview/skills/old-skill'); stale.mkdir(parents=True, exist_ok=True); (stale / 'SKILL.md').write_text('# stale', encoding='utf-8'); print('OK')"`
Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --prune-advice`
Expected:
- `PRUNE-ADVICE`
- 只列出 `old-skill`
- `status: stale`
- `advice: consider-cleanup`
- `STALE TARGETS: 1`
- `consider-cleanup: 1`

- [ ] **Step 7: 运行互斥参数验收**

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --prune-advice --stale-check`
Expected: 非零退出码，stderr 包含 `Cannot combine --prune-advice and --stale-check.`

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --prune-advice --inspect`
Expected: 非零退出码，stderr 包含 `Cannot combine --prune-advice and --inspect.`

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --prune-advice --dry-run`
Expected: 非零退出码，stderr 包含 `Cannot combine --prune-advice and --dry-run.`

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --prune-advice --force`
Expected: 非零退出码，stderr 包含 `Cannot combine --prune-advice and --force.`

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --prune-advice --only orchestration`
Expected: 非零退出码，stderr 包含 `Cannot combine --prune-advice and --only.`

- [ ] **Step 8: 运行测试套件**

Run: `python tools/test_sync_claude_code_skills.py`
Expected: 全部测试通过

- [ ] **Step 9: 清理临时目录**

Run: `python -c "from pathlib import Path; import shutil; target = Path('.claude-sync-preview'); shutil.rmtree(target) if target.exists() else None; print('OK')"`
Expected: `OK`

- [ ] **Step 10: 提交 prune advice 实现**

```bash
git add tools/sync_claude_code_skills.py tools/test_sync_claude_code_skills.py
git commit -m "feat: add prune advice mode"
```

---

### Task 2: 让 setup 文档承认 prune advice 是下一层安全建议

**Files:**
- Modify: `docs/CLAUDE_CODE_SETUP.md`
- Test: `docs/CLAUDE_CODE_SETUP.md`

- [ ] **Step 1: 在 setup 文档中增加 prune advice 回指**

```md
- `python tools/sync_claude_code_skills.py --target-root <path> --prune-advice`：用于列出 stale 目标中可考虑清理的对象。
```

- [ ] **Step 2: 明确 prune advice 的边界**

```md
- `--prune-advice`：只给出 `consider-cleanup` 最小建议。
- 当前不输出删除命令，也不执行删除。
```

- [ ] **Step 3: 运行最小文本检查，确认 setup 文档已登记 prune advice**

Run: `python -c "from pathlib import Path; text = Path('docs/CLAUDE_CODE_SETUP.md').read_text(encoding='utf-8'); required = ['--prune-advice', 'consider-cleanup', '不执行删除']; missing = [item for item in required if item not in text]; print('OK' if not missing else missing)"`
Expected: `OK`

- [ ] **Step 4: 提交 setup 文档同步**

```bash
git add docs/CLAUDE_CODE_SETUP.md
git commit -m "docs: register prune advice"
```

---

### Task 3: 视需要把 validation / roadmap 同步到 prune advice

**Files:**
- Modify: `docs/CONSISTENCY_VALIDATION.md`
- Modify: `docs/ROADMAP.md`
- Test: `docs/CONSISTENCY_VALIDATION.md`
- Test: `docs/ROADMAP.md`

- [ ] **Step 1: 在 `docs/CONSISTENCY_VALIDATION.md` 增加 prune advice 边界规则（若决定纳入）**

```md
15. `tools/sync_claude_code_skills.py --prune-advice` 只允许对 stale 对象输出最小建议，不得重复列出 managed 清单。
16. prune advice 只允许输出 `advice: consider-cleanup`，不得输出删除命令、不得执行删除。
17. `--prune-advice` 必须与 `--stale-check`、`--inspect`、`--dry-run`、`--force`、`--only` 互斥。
```

- [ ] **Step 2: 在 `docs/ROADMAP.md` 增加 prune advice 落地记录（若决定落路线图）**

```md
## v14 - Claude Code prune advice

目标：在不执行删除的前提下，为 stale 目标给出最小清理建议。

计划方向：
- [x] `--prune-advice` 已落地
- [x] prune advice 只聚焦 stale 对象
- [x] `consider-cleanup` 最小建议已固定
```

- [ ] **Step 3: 运行最小文本检查，确认相关文档都命中 prune advice 语义**

Run: `python -c "from pathlib import Path; files = ['docs/CLAUDE_CODE_SETUP.md']; missing = [file for file in files if '--prune-advice' not in Path(file).read_text(encoding='utf-8')]; print('OK' if not missing else missing)"`
Expected: `OK`

- [ ] **Step 4: 提交规则与路线图同步（若本任务实施）**

```bash
git add docs/CONSISTENCY_VALIDATION.md docs/ROADMAP.md
git commit -m "docs: register prune advice"
```

---

### Task 4: 做端到端验收

**Files:**
- Test: `tools/sync_claude_code_skills.py`
- Test: `tools/test_sync_claude_code_skills.py`
- Test: `docs/CLAUDE_CODE_SETUP.md`
- Test: `tools/validate_consistency.py`

- [ ] **Step 1: 运行 consistency validation 最终验收**

Run: `python tools/validate_consistency.py`
Expected: `Validation result: PASS`

- [ ] **Step 2: 运行空目标 prune advice 验收**

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --prune-advice`
Expected:
- `PRUNE-ADVICE`
- `TOTAL TARGET SKILLS: 0`
- `STALE TARGETS: 0`
- `SUMMARY`
- `consider-cleanup: 0`

- [ ] **Step 3: 运行 stale 目标 prune advice 验收**

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --force`
Run: `python -c "from pathlib import Path; stale = Path('.claude-sync-preview/skills/old-skill'); stale.mkdir(parents=True, exist_ok=True); (stale / 'SKILL.md').write_text('# stale', encoding='utf-8'); print('OK')"`
Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --prune-advice`
Expected:
- 只列出 `old-skill`
- `status: stale`
- `advice: consider-cleanup`
- `STALE TARGETS: 1`
- `consider-cleanup: 1`

- [ ] **Step 4: 运行互斥参数验收**

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --prune-advice --stale-check`
Expected: 非零退出码，stderr 包含 `Cannot combine --prune-advice and --stale-check.`

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --prune-advice --inspect`
Expected: 非零退出码，stderr 包含 `Cannot combine --prune-advice and --inspect.`

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --prune-advice --dry-run`
Expected: 非零退出码，stderr 包含 `Cannot combine --prune-advice and --dry-run.`

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --prune-advice --force`
Expected: 非零退出码，stderr 包含 `Cannot combine --prune-advice and --force.`

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --prune-advice --only orchestration`
Expected: 非零退出码，stderr 包含 `Cannot combine --prune-advice and --only.`

- [ ] **Step 5: 运行测试套件**

Run: `python tools/test_sync_claude_code_skills.py`
Expected: 全部测试通过

- [ ] **Step 6: 清理临时目录**

Run: `python -c "from pathlib import Path; import shutil; target = Path('.claude-sync-preview'); shutil.rmtree(target) if target.exists() else None; print('OK')"`
Expected: `OK`

- [ ] **Step 7: 提交 prune advice foundation 基线**

```bash
git add tools/sync_claude_code_skills.py tools/test_sync_claude_code_skills.py docs/CLAUDE_CODE_SETUP.md docs/CONSISTENCY_VALIDATION.md docs/ROADMAP.md
git commit -m "feat: add prune advice mode"
```

---

## Self-Review

- **Spec coverage:** 本计划覆盖了 `--prune-advice` 实现、setup 文档同步、视需要的 validation/roadmap 同步，以及空目标/stale 目标/互斥参数的最终验收。
- **Placeholder scan:** 已移除 `TBD`、`TODO`、`implement later`、`appropriate` 等占位措辞；涉及代码与文档改动的步骤都给了明确代码骨架和验证命令。
- **Type consistency:** 统一使用 `--prune-advice` 作为建议层模式，统一只对 stale 对象输出 `advice: consider-cleanup`，统一保持与 `--stale-check`、`--inspect`、`--dry-run`、`--force`、`--only` 的互斥规则。
