# Claude Code Stale Target Detect Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 `tools/sync_claude_code_skills.py` 增加 `--stale-check`，让脚本在不删除任何文件的前提下识别目标目录中的 stale skill。

**Architecture:** 本轮只做 stale target detect / report，不做 prune 建议或删除动作。脚本新增一个 target-centric 的只读模式 `--stale-check`，专门扫描目标目录中的 `skills/**/SKILL.md`，并与当前仓库正式 `skills/**/SKILL.md` 集合对比，输出 `managed / stale` 两类状态。文档只做最小同步，确保 setup、validation、roadmap 能承认这是一种风险识别能力，而不是删除能力。

**Tech Stack:** Python 3, pathlib, argparse, shutil, git, Claude Code

---

## File Structure

### Existing files to modify

- `tools/sync_claude_code_skills.py` — 增加 `--stale-check` 模式与对应输出。
- `docs/CLAUDE_CODE_SETUP.md` — 把 stale target detect 记为“先识别 stale target 再决定后续动作”的安全辅助能力。
- `docs/CONSISTENCY_VALIDATION.md`（如需要最小规则登记）— 若要把 stale-check 边界纳入现有规则，则补最小约束。
- `docs/ROADMAP.md`（如需要阶段落地记录）— 若要把 stale target detect 记为下一阶段落地点，则补最小路线图记录。

### Existing files to read but not modify

- `docs/CLAUDE_CODE_HOST.md`
- `docs/PLATFORMS.md`
- `skills/**/SKILL.md`

### New files to create

- `docs/superpowers/plans/2026-04-25-un9flow-claude-code-stale-target-detect-foundation.md` — 当前 implementation plan。

### No prune/delete actions

本计划不新增删除、prune、clean 或建议删除逻辑。

---

### Task 1: 给同步脚本增加 `--stale-check` 模式

**Files:**
- Modify: `tools/sync_claude_code_skills.py`
- Test: `tools/sync_claude_code_skills.py`

- [ ] **Step 1: 在参数解析中增加 `--stale-check`，并与 `--inspect`、`--dry-run`、`--force`、`--only` 互斥**

```python
parser.add_argument(
    "--stale-check",
    action="store_true",
    help="Report stale target skills without writing, creating, or deleting files.",
)
```

并在主入口中加入：

```python
if args.stale_check and args.inspect:
    print("Cannot combine --stale-check and --inspect.", file=sys.stderr)
    return 2
if args.stale_check and args.dry_run:
    print("Cannot combine --stale-check and --dry-run.", file=sys.stderr)
    return 2
if args.stale_check and args.force:
    print("Cannot combine --stale-check and --force.", file=sys.stderr)
    return 2
if args.stale_check and args.only:
    print("Cannot combine --stale-check and --only.", file=sys.stderr)
    return 2
```

- [ ] **Step 2: 增加目标目录扫描函数，只扫描目标下的 `skills/**/SKILL.md`**

```python
def discover_target_skill_files(target_root: Path) -> list[Path]:
    skills_root = target_root / "skills"
    if not skills_root.exists():
        return []
    return sorted(path for path in skills_root.rglob("SKILL.md") if path.is_file())
```

- [ ] **Step 3: 增加 source / target 比对逻辑，输出 `managed / stale`**

```python
def stale_check_skill_files(source_skill_files: list[Path], target_root: Path) -> int:
    target_skill_files = discover_target_skill_files(target_root)
    managed_skill_names = {skill_name_for(path) for path in source_skill_files}

    print("STALE-CHECK")
    print(f"TARGET ROOT: {display_path(target_root)}")
    print(f"FOUND TARGET SKILLS: {len(target_skill_files)}")
    print(f"CURRENT SOURCE SKILLS: {len(managed_skill_names)}")

    managed = 0
    stale = 0

    for target_file in target_skill_files:
        skill_name = target_file.parent.name
        status = "managed" if skill_name in managed_skill_names else "stale"
        if status == "managed":
            managed += 1
        else:
            stale += 1
        print(f"- {skill_name}")
        print(f"  target: {display_path(target_file)}")
        print(f"  status: {status}")

    print("SUMMARY")
    print(f"- total: {len(target_skill_files)}")
    print(f"- managed: {managed}")
    print(f"- stale: {stale}")
    return 0
```

- [ ] **Step 4: 在主入口中接入 stale-check 分支**

```python
if args.stale_check:
    return stale_check_skill_files(skill_files, target_root)
```

- [ ] **Step 5: 运行 stale-check 验收（空目标）**

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --stale-check`
Expected:
- `STALE-CHECK`
- `FOUND TARGET SKILLS: 0`
- `CURRENT SOURCE SKILLS: 12`
- `SUMMARY`
- `managed: 0`
- `stale: 0`

- [ ] **Step 6: 运行互斥参数验收**

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --stale-check --inspect`
Expected: 非零退出码，stderr 包含 `Cannot combine --stale-check and --inspect.`

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --stale-check --dry-run`
Expected: 非零退出码，stderr 包含 `Cannot combine --stale-check and --dry-run.`

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --stale-check --force`
Expected: 非零退出码，stderr 包含 `Cannot combine --stale-check and --force.`

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --stale-check --only orchestration`
Expected: 非零退出码，stderr 包含 `Cannot combine --stale-check and --only.`

- [ ] **Step 7: 提交 stale-check 实现**

```bash
git add tools/sync_claude_code_skills.py
git commit -m "feat: add stale target detection"
```

---

### Task 2: 让 setup 文档承认 stale-check 是安全辅助动作

**Files:**
- Modify: `docs/CLAUDE_CODE_SETUP.md`
- Test: `docs/CLAUDE_CODE_SETUP.md`

- [ ] **Step 1: 在 setup 文档中增加 stale-check 回指**

```md
- `python tools/sync_claude_code_skills.py --target-root <path> --stale-check`：用于识别目标目录中哪些 skill 仍受管、哪些已经 stale。
```

- [ ] **Step 2: 明确 stale-check 的边界**

```md
- `--stale-check`：只做 stale 目标识别与报告。
- 当前不提供 prune 建议，也不执行删除。
```

- [ ] **Step 3: 运行最小文本检查，确认 setup 文档已登记 stale-check**

Run: `python -c "from pathlib import Path; text = Path('docs/CLAUDE_CODE_SETUP.md').read_text(encoding='utf-8'); required = ['--stale-check', 'stale', '不执行删除']; missing = [item for item in required if item not in text]; print('OK' if not missing else missing)"`
Expected: `OK`

- [ ] **Step 4: 提交 setup 文档同步**

```bash
git add docs/CLAUDE_CODE_SETUP.md
git commit -m "docs: register stale target check"
```

---

### Task 3: 视需要把 validation / roadmap 同步到 stale-check

**Files:**
- Modify: `docs/CONSISTENCY_VALIDATION.md`
- Modify: `docs/ROADMAP.md`
- Test: `docs/CONSISTENCY_VALIDATION.md`
- Test: `docs/ROADMAP.md`

- [ ] **Step 1: 在 `docs/CONSISTENCY_VALIDATION.md` 增加 stale-check 边界规则（若决定纳入）**

```md
11. `tools/sync_claude_code_skills.py --stale-check` 只允许扫描目标目录中的 `skills/**/SKILL.md`。
12. stale-check 只允许输出 `managed / stale` 状态，不得提供 prune 建议或执行删除。
13. `--stale-check` 必须与 `--inspect`、`--dry-run`、`--force`、`--only` 互斥。
```

- [ ] **Step 2: 在 `docs/ROADMAP.md` 增加 stale target detect 落地记录（若决定落路线图）**

```md
## v13 - Claude Code stale target detect

目标：在不删除任何文件的前提下，识别目标目录里哪些 skill 已经 stale。

计划方向：
- [x] `--stale-check` 已落地
- [x] stale-check 已固定为 target-centric 只读模式
- [x] stale-check 输出已固定为 managed / stale 与 summary
```

- [ ] **Step 3: 运行最小文本检查，确认相关文档都命中 stale-check 语义**

Run: `python -c "from pathlib import Path; files = ['docs/CLAUDE_CODE_SETUP.md']; missing = [file for file in files if '--stale-check' not in Path(file).read_text(encoding='utf-8')]; print('OK' if not missing else missing)"`
Expected: `OK`

- [ ] **Step 4: 提交规则与路线图同步（若本任务实施）**

```bash
git add docs/CONSISTENCY_VALIDATION.md docs/ROADMAP.md
git commit -m "docs: register stale target check"
```

---

### Task 4: 做端到端验收

**Files:**
- Test: `tools/sync_claude_code_skills.py`
- Test: `docs/CLAUDE_CODE_SETUP.md`
- Test: `tools/validate_consistency.py`

- [ ] **Step 1: 运行 consistency validation 最终验收**

Run: `python tools/validate_consistency.py`
Expected: `Validation result: PASS`

- [ ] **Step 2: 运行空目标 stale-check 验收**

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --stale-check`
Expected:
- `STALE-CHECK`
- `FOUND TARGET SKILLS: 0`
- `CURRENT SOURCE SKILLS: 12`
- `SUMMARY`
- `managed: 0`
- `stale: 0`

- [ ] **Step 3: 运行带目标 stale-check 验收**

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --force`
Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --stale-check`
Expected:
- `FOUND TARGET SKILLS: 12`
- 12 项均为 `managed`
- `stale: 0`

- [ ] **Step 4: 构造一个 stale 目标并复查**

Run: `python -c "from pathlib import Path; stale = Path('.claude-sync-preview/skills/old-skill'); stale.mkdir(parents=True, exist_ok=True); (stale / 'SKILL.md').write_text('# stale', encoding='utf-8'); print('OK')"`
Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --stale-check`
Expected:
- 额外出现一项 `old-skill`
- `status: stale`
- `stale: 1`

- [ ] **Step 5: 运行互斥参数验收**

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --stale-check --inspect`
Expected: 非零退出码，stderr 包含 `Cannot combine --stale-check and --inspect.`

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --stale-check --dry-run`
Expected: 非零退出码，stderr 包含 `Cannot combine --stale-check and --dry-run.`

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --stale-check --force`
Expected: 非零退出码，stderr 包含 `Cannot combine --stale-check and --force.`

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --stale-check --only orchestration`
Expected: 非零退出码，stderr 包含 `Cannot combine --stale-check and --only.`

- [ ] **Step 6: 清理临时目录**

Run: `python -c "from pathlib import Path; import shutil; target = Path('.claude-sync-preview'); shutil.rmtree(target) if target.exists() else None; print('OK')"`
Expected: `OK`

- [ ] **Step 7: 提交 stale target detect foundation 基线**

```bash
git add tools/sync_claude_code_skills.py docs/CLAUDE_CODE_SETUP.md docs/CONSISTENCY_VALIDATION.md docs/ROADMAP.md
git commit -m "feat: add stale target detection"
```

---

## Self-Review

- **Spec coverage:** 本计划覆盖了 `--stale-check` 实现、setup 文档同步、视需要的 validation/roadmap 同步，以及空目标/非空目标/stale 目标/互斥参数的最终验收。
- **Placeholder scan:** 已移除 `TBD`、`TODO`、`implement later`、`appropriate` 等占位措辞；涉及代码与文档改动的步骤都给了明确代码骨架和验证命令。
- **Type consistency:** 统一使用 `--stale-check` 作为只读 target-centric 模式，统一使用 `managed / stale` 作为状态分类，统一保持与 `--inspect`、`--dry-run`、`--force`、`--only` 的互斥规则。
