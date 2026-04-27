# Claude Code Explicit Prune Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 `tools/sync_claude_code_skills.py` 增加 `--prune`，让脚本在显式触发和受控边界下删除 stale target 的 `skills/**/SKILL.md` 文件。

**Architecture:** 本轮只做显式 prune 动作层，不做删除建议扩展、回收站、undo、空目录清理、docs/templates/cases 清理或自动 prune。脚本继续保持六层分工：inspect 盘点 source→target、dry-run 预演动作、sync 执行同步、stale-check 识别 stale、prune-advice 给最小建议、prune 才是真正动作层。所有删除都必须显式触发、逐项打印、统一 summary。

**Tech Stack:** Python 3, pathlib, argparse, shutil, git, unittest, Claude Code

---

## File Structure

### Existing files to modify

- `tools/sync_claude_code_skills.py` — 增加 `--prune` 模式与受控删除逻辑。
- `tools/test_sync_claude_code_skills.py` — 增加 prune 的最小行为测试。
- `docs/CLAUDE_CODE_SETUP.md` — 把 prune 登记为“显式手动清理 stale target”的下一层动作。
- `docs/CONSISTENCY_VALIDATION.md`（如需要最小规则登记）— 若要把 prune 边界纳入现有规则，则补最小约束。
- `docs/ROADMAP.md`（如需要阶段落地记录）— 若要把 explicit prune 记为下一阶段落地点，则补最小路线图记录。

### Existing files to read but not modify

- `docs/CLAUDE_CODE_HOST.md`
- `docs/PLATFORMS.md`
- `skills/**/SKILL.md`

### New files to create

- `docs/superpowers/plans/2026-04-25-un9flow-claude-code-explicit-prune-foundation.md` — 当前 implementation plan。

### No directory cleanup

本计划不删除空目录，不做回收站、undo、trash 或自动 clean。

---

### Task 1: 给同步脚本增加 `--prune` 模式

**Files:**
- Modify: `tools/sync_claude_code_skills.py`
- Modify: `tools/test_sync_claude_code_skills.py`
- Test: `tools/sync_claude_code_skills.py`
- Test: `tools/test_sync_claude_code_skills.py`

- [ ] **Step 1: 在参数解析中增加 `--prune`，并与 `--inspect`、`--dry-run`、`--stale-check`、`--prune-advice`、`--force`、`--only` 互斥**

```python
parser.add_argument(
    "--prune",
    action="store_true",
    help="Delete stale target SKILL.md files under the managed skills/ tree.",
)
```

并在主入口中加入：

```python
if args.prune and args.inspect:
    print("Cannot combine --prune and --inspect.", file=sys.stderr)
    return 2
if args.prune and args.dry_run:
    print("Cannot combine --prune and --dry-run.", file=sys.stderr)
    return 2
if args.prune and args.stale_check:
    print("Cannot combine --prune and --stale-check.", file=sys.stderr)
    return 2
if args.prune and args.prune_advice:
    print("Cannot combine --prune and --prune-advice.", file=sys.stderr)
    return 2
if args.prune and args.force:
    print("Cannot combine --prune and --force.", file=sys.stderr)
    return 2
if args.prune and args.only is not None:
    print("Cannot combine --prune and --only.", file=sys.stderr)
    return 2
```

- [ ] **Step 2: 增加 prune 执行函数，只删除 stale 的 `SKILL.md` 文件**

```python
def prune_skill_files(source_skill_files: list[Path], target_root: Path) -> int:
    target_skill_files = discover_target_skill_files(target_root)
    managed_targets = {
        target_path_for(skill_file, target_root).resolve() for skill_file in source_skill_files
    }

    pruned = 0
    skipped = 0
    failed = 0

    for target_skill_file in target_skill_files:
        resolved_target = target_skill_file.resolve()
        if resolved_target in managed_targets:
            print(f"SKIPPED {display_path(target_skill_file)}: managed")
            skipped += 1
            continue

        try:
            target_skill_file.unlink()
        except OSError as exc:
            print(f"FAILED {display_path(target_skill_file)}: {exc}", file=sys.stderr)
            failed += 1
            continue

        print(f"PRUNED {display_path(target_skill_file)}")
        pruned += 1

    print(f"SUMMARY: pruned {pruned}, skipped {skipped}, failed {failed}")
    return 0 if failed == 0 else 1
```

- [ ] **Step 3: 保持删除范围只限 stale 的 `skills/**/SKILL.md` 文件本身**

```python
# 不增加 rmtree / 空目录删除 / docs/templates/cases 删除逻辑
```

- [ ] **Step 4: 在主入口中接入 prune 分支**

```python
if args.prune:
    return prune_skill_files(source_skill_files=all_skill_files, target_root=target_root)
```

- [ ] **Step 5: 增加最小测试覆盖**

```python
def test_prune_removes_only_stale_skill_files(self) -> None:
    ...

def test_prune_keeps_managed_skill_files(self) -> None:
    ...

def test_prune_conflicts_with_prune_advice(self) -> None:
    ...
```

- [ ] **Step 6: 运行空目标 prune 验收**

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --prune`
Expected:
- `SUMMARY: pruned 0, skipped 0, failed 0`
- 不报错

- [ ] **Step 7: 运行 stale 目标 prune 验收**

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --force`
Run: `python -c "from pathlib import Path; stale = Path('.claude-sync-preview/skills/old-skill'); stale.mkdir(parents=True, exist_ok=True); (stale / 'SKILL.md').write_text('# stale', encoding='utf-8'); print('OK')"`
Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --prune`
Expected:
- `PRUNED .claude-sync-preview/skills/old-skill/SKILL.md`
- `SUMMARY: pruned 1, skipped 12, failed 0`
- `old-skill/SKILL.md` 不再存在
- 其他 managed `SKILL.md` 仍存在

- [ ] **Step 8: 运行互斥参数验收**

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --prune --inspect`
Expected: 非零退出码，stderr 包含 `Cannot combine --prune and --inspect.`

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --prune --dry-run`
Expected: 非零退出码，stderr 包含 `Cannot combine --prune and --dry-run.`

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --prune --stale-check`
Expected: 非零退出码，stderr 包含 `Cannot combine --prune and --stale-check.`

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --prune --prune-advice`
Expected: 非零退出码，stderr 包含 `Cannot combine --prune and --prune-advice.`

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --prune --force`
Expected: 非零退出码，stderr 包含 `Cannot combine --prune and --force.`

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --prune --only orchestration`
Expected: 非零退出码，stderr 包含 `Cannot combine --prune and --only.`

- [ ] **Step 9: 运行测试套件**

Run: `python tools/test_sync_claude_code_skills.py`
Expected: 全部测试通过

- [ ] **Step 10: 清理临时目录**

Run: `python -c "from pathlib import Path; import shutil; target = Path('.claude-sync-preview'); shutil.rmtree(target) if target.exists() else None; print('OK')"`
Expected: `OK`

- [ ] **Step 11: 提交 explicit prune 实现**

```bash
git add tools/sync_claude_code_skills.py tools/test_sync_claude_code_skills.py
git commit -m "feat: add explicit prune mode"
```

---

### Task 2: 让 setup 文档承认 prune 是显式动作层

**Files:**
- Modify: `docs/CLAUDE_CODE_SETUP.md`
- Test: `docs/CLAUDE_CODE_SETUP.md`

- [ ] **Step 1: 在 setup 文档中增加 prune 回指**

```md
- `python tools/sync_claude_code_skills.py --target-root <path> --prune`：在显式触发下清理 stale 的 `skills/**/SKILL.md` 目标文件。
```

- [ ] **Step 2: 明确 prune 的边界**

```md
- `--prune`：显式动作层，只删除 stale 的 `SKILL.md` 目标文件。
- 当前不删除空目录，也不删除非 `SKILL.md` 对象。
```

- [ ] **Step 3: 运行最小文本检查，确认 setup 文档已登记 prune**

Run: `python -c "from pathlib import Path; text = Path('docs/CLAUDE_CODE_SETUP.md').read_text(encoding='utf-8'); required = ['--prune', '只删除 stale 的 `SKILL.md`', '不删除空目录']; missing = [item for item in required if item not in text]; print('OK' if not missing else missing)"`
Expected: `OK`

- [ ] **Step 4: 提交 setup 文档同步**

```bash
git add docs/CLAUDE_CODE_SETUP.md
git commit -m "docs: register explicit prune"
```

---

### Task 3: 视需要把 validation / roadmap 同步到 prune 动作层

**Files:**
- Modify: `docs/CONSISTENCY_VALIDATION.md`
- Modify: `docs/ROADMAP.md`
- Test: `docs/CONSISTENCY_VALIDATION.md`
- Test: `docs/ROADMAP.md`

- [ ] **Step 1: 在 `docs/CONSISTENCY_VALIDATION.md` 增加 explicit prune 边界规则（若决定纳入）**

```md
18. `tools/sync_claude_code_skills.py --prune` 只允许删除 stale 的 `skills/**/SKILL.md` 文件本身。
19. `--prune` 不得删除空目录，不得删除非 `SKILL.md` 对象。
20. `--prune` 必须与 `--inspect`、`--dry-run`、`--stale-check`、`--prune-advice`、`--force`、`--only` 互斥。
```

- [ ] **Step 2: 在 `docs/ROADMAP.md` 增加 explicit prune 落地记录（若决定落路线图）**

```md
## v15 - Claude Code explicit prune

目标：在显式触发和受控边界下，删除 stale 的 `skills/**/SKILL.md` 目标文件。

计划方向：
- [x] `--prune` 已落地
- [x] prune 已固定为显式动作层
- [x] prune 只删除 stale 的 `SKILL.md` 文件本身，不删除空目录
```

- [ ] **Step 3: 运行最小文本检查，确认相关文档都命中 prune 语义**

Run: `python -c "from pathlib import Path; files = ['docs/CLAUDE_CODE_SETUP.md']; missing = [file for file in files if '--prune' not in Path(file).read_text(encoding='utf-8')]; print('OK' if not missing else missing)"`
Expected: `OK`

- [ ] **Step 4: 提交规则与路线图同步（若本任务实施）**

```bash
git add docs/CONSISTENCY_VALIDATION.md docs/ROADMAP.md
git commit -m "docs: register explicit prune"
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

- [ ] **Step 2: 运行空目标 prune 验收**

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --prune`
Expected: `SUMMARY: pruned 0, skipped 0, failed 0`

- [ ] **Step 3: 运行 stale 目标 prune 验收**

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --force`
Run: `python -c "from pathlib import Path; stale = Path('.claude-sync-preview/skills/old-skill'); stale.mkdir(parents=True, exist_ok=True); (stale / 'SKILL.md').write_text('# stale', encoding='utf-8'); print('OK')"`
Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --prune`
Expected:
- `PRUNED .claude-sync-preview/skills/old-skill/SKILL.md`
- `SUMMARY: pruned 1, skipped 12, failed 0`
- `old-skill/SKILL.md` 不存在
- managed 目标仍存在

- [ ] **Step 4: 运行互斥参数验收**

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --prune --inspect`
Expected: 非零退出码，stderr 包含 `Cannot combine --prune and --inspect.`

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --prune --dry-run`
Expected: 非零退出码，stderr 包含 `Cannot combine --prune and --dry-run.`

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --prune --stale-check`
Expected: 非零退出码，stderr 包含 `Cannot combine --prune and --stale-check.`

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --prune --prune-advice`
Expected: 非零退出码，stderr 包含 `Cannot combine --prune and --prune-advice.`

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --prune --force`
Expected: 非零退出码，stderr 包含 `Cannot combine --prune and --force.`

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --prune --only orchestration`
Expected: 非零退出码，stderr 包含 `Cannot combine --prune and --only.`

- [ ] **Step 5: 运行测试套件**

Run: `python tools/test_sync_claude_code_skills.py`
Expected: 全部测试通过

- [ ] **Step 6: 清理临时目录**

Run: `python -c "from pathlib import Path; import shutil; target = Path('.claude-sync-preview'); shutil.rmtree(target) if target.exists() else None; print('OK')"`
Expected: `OK`

- [ ] **Step 7: 提交 explicit prune foundation 基线**

```bash
git add tools/sync_claude_code_skills.py tools/test_sync_claude_code_skills.py docs/CLAUDE_CODE_SETUP.md docs/CONSISTENCY_VALIDATION.md docs/ROADMAP.md
git commit -m "feat: add explicit prune mode"
```

---

## Self-Review

- **Spec coverage:** 本计划覆盖了 `--prune` 实现、setup 文档同步、视需要的 validation/roadmap 同步，以及空目标/stale 目标/互斥参数的最终验收。
- **Placeholder scan:** 已移除 `TBD`、`TODO`、`implement later`、`appropriate` 等占位措辞；涉及代码与文档改动的步骤都给了明确代码骨架和验证命令。
- **Type consistency:** 统一使用 `--prune` 作为动作层模式，统一只删除 stale 的 `SKILL.md` 文件本身，统一保持与 `--inspect`、`--dry-run`、`--stale-check`、`--prune-advice`、`--force`、`--only` 的互斥规则。
