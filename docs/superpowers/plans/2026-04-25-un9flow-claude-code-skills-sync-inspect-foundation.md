# Claude Code Skills Sync Inspect Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 `tools/sync_claude_code_skills.py` 增加 `--inspect` 模式，让技能同步器在真正执行前能静态盘点当前状态。

**Architecture:** 本轮只做 inspect 增强，不做 selective sync、prune、docs 同步、多 host inspect 或 JSON manifest。脚本形成三种清晰模式：inspect、dry-run、sync；其中 inspect 只做状态盘点，dry-run 继续做动作预演，sync 继续做真实同步。文档只做最小同步，确保 setup 文档能承认 inspect 是“先盘点再执行”的辅助动作。

**Tech Stack:** Python 3, pathlib, argparse, shutil, git, Claude Code

---

## File Structure

### Existing files to modify

- `tools/sync_claude_code_skills.py` — 增加 `--inspect` 模式与对应输出。
- `docs/CLAUDE_CODE_SETUP.md` — 把 inspect 纳入 setup 验证 / 辅助动作说明。
- `docs/CONSISTENCY_VALIDATION.md`（如需要最小规则登记）— 若要把 inspect 模式边界纳入现有规则，则补最小约束。
- `docs/ROADMAP.md`（如需要阶段落地记录）— 若要把 inspect 增强记为下一阶段落地点，则补最小路线图记录。

### Existing files to read but not modify

- `docs/CLAUDE_CODE_HOST.md`
- `docs/PLATFORMS.md`
- `docs/SKILL_ARCHITECTURE.md`
- `skills/**/SKILL.md`

### New files to create

- `docs/superpowers/plans/2026-04-25-un9flow-claude-code-skills-sync-inspect-foundation.md` — 当前 implementation plan。

### No new sync scopes

本计划不新增 docs / templates / cases / golden / regression 同步范围。

---

### Task 1: 给同步脚本增加 `--inspect` 模式

**Files:**
- Modify: `tools/sync_claude_code_skills.py`
- Test: `tools/sync_claude_code_skills.py`

- [ ] **Step 1: 在参数解析中增加 `--inspect`，并与 `--dry-run`、`--force` 互斥**

```python
parser.add_argument(
    "--inspect",
    action="store_true",
    help="Inspect discovered skills and target status without writing files.",
)
```

并在主入口中加入：

```python
if args.inspect and args.dry_run:
    print("Cannot combine --inspect and --dry-run.", file=sys.stderr)
    return 2
if args.inspect and args.force:
    print("Cannot combine --inspect and --force.", file=sys.stderr)
    return 2
```

- [ ] **Step 2: 增加 inspect 所需的数据结构与状态函数**

```python
def inspect_status_for(destination: Path) -> str:
    return "exists" if destination.exists() else "missing"
```

- [ ] **Step 3: 实现 inspect 输出函数**

```python
def inspect_skill_files(skill_files: list[Path], target_root: Path) -> int:
    if not skill_files:
        print("No skill files found.", file=sys.stderr)
        return 2

    print("INSPECT")
    print(f"SOURCE ROOT: {display_path(SKILLS_ROOT.relative_to(ROOT))}")
    print(f"TARGET ROOT: {display_path(target_root)}")
    print(f"FOUND {len(skill_files)} skills")
    print()

    existing = 0
    missing = 0

    for skill_file in skill_files:
        destination = target_path_for(skill_file, target_root)
        status = inspect_status_for(destination)
        if status == "exists":
            existing += 1
        else:
            missing += 1

        print(f"- {skill_file.parent.name}")
        print(f"  source: {display_path(skill_file.relative_to(ROOT))}")
        print(f"  target: {display_path(destination)}")
        print(f"  status: {status}")
        print()

    print("SUMMARY")
    print(f"- total: {len(skill_files)}")
    print(f"- existing: {existing}")
    print(f"- missing: {missing}")
    return 0
```

- [ ] **Step 4: 在主入口中接入 inspect 分支**

```python
if args.inspect:
    return inspect_skill_files(skill_files, target_root)
```

- [ ] **Step 5: 运行 inspect 验证**

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --inspect`
Expected:
- 输出 `INSPECT`
- 输出 `SOURCE ROOT: skills`
- 输出 `TARGET ROOT: .claude-sync-preview`
- 输出 `FOUND 12 skills`
- 每项包含 `source` / `target` / `status`
- summary 包含 `total` / `existing` / `missing`

- [ ] **Step 6: 运行互斥参数验证**

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --inspect --dry-run`
Expected: 非零退出码，stderr 包含 `Cannot combine --inspect and --dry-run.`

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --inspect --force`
Expected: 非零退出码，stderr 包含 `Cannot combine --inspect and --force.`

- [ ] **Step 7: 提交 inspect 模式实现**

```bash
git add tools/sync_claude_code_skills.py
git commit -m "feat: add inspect mode to skills sync"
```

---

### Task 2: 让 setup 文档承认 inspect 是“先盘点再执行”的动作

**Files:**
- Modify: `docs/CLAUDE_CODE_SETUP.md`
- Test: `docs/CLAUDE_CODE_SETUP.md`

- [ ] **Step 1: 在 setup 文档中增加 inspect 回指**

```md
- `python tools/sync_claude_code_skills.py --target-root <path> --inspect`：用于在执行同步前盘点 skill 来源、目标路径与当前目标状态。
```

- [ ] **Step 2: 保持与 dry-run 的职责分工清楚**

```md
- `--inspect`：先看当前状态。
- `--dry-run`：预演将执行的 copy 动作。
```

- [ ] **Step 3: 运行最小文本检查，确认 setup 文档已回指 inspect 与 dry-run 分工**

Run: `python -c "from pathlib import Path; text = Path('docs/CLAUDE_CODE_SETUP.md').read_text(encoding='utf-8'); required = ['--inspect', '--dry-run', '先看当前状态', '预演将执行的 copy 动作']; missing = [item for item in required if item not in text]; print('OK' if not missing else missing)"`
Expected: `OK`

- [ ] **Step 4: 提交 setup 文档同步**

```bash
git add docs/CLAUDE_CODE_SETUP.md
git commit -m "docs: register inspect mode"
```

---

### Task 3: 视需要把 validation / roadmap 同步到 inspect 增强

**Files:**
- Modify: `docs/CONSISTENCY_VALIDATION.md`
- Modify: `docs/ROADMAP.md`
- Test: `docs/CONSISTENCY_VALIDATION.md`
- Test: `docs/ROADMAP.md`

- [ ] **Step 1: 在 `docs/CONSISTENCY_VALIDATION.md` 增加 inspect 模式边界规则（若决定纳入）**

```md
6. `tools/sync_claude_code_skills.py --inspect` 只允许做静态盘点：
   - 不写文件
   - 不创建目录
   - 不执行复制
7. `--inspect` 与 `--dry-run`、`--force` 必须互斥。
```

- [ ] **Step 2: 在 `docs/ROADMAP.md` 增加 inspect 增强落地记录（若决定落路线图）**

```md
## v11 - Claude Code skills sync inspect 增强

目标：让 skills-only 同步脚本在真正执行前能静态盘点当前状态。

计划方向：
- [x] `--inspect` 模式已落地
- [x] inspect / dry-run / sync 三段能力已被显式分离
- [x] inspect 输出结构已固定为头部摘要 / 逐项清单 / 尾部 summary
```

- [ ] **Step 3: 运行最小文本检查，确认相关文档都命中 inspect 语义**

Run: `python -c "from pathlib import Path; files = ['docs/CLAUDE_CODE_SETUP.md']; optional = ['docs/CONSISTENCY_VALIDATION.md', 'docs/ROADMAP.md']; missing = [file for file in files if '--inspect' not in Path(file).read_text(encoding='utf-8')]; print('OK' if not missing else missing)"`
Expected: `OK`

- [ ] **Step 4: 提交规则与路线图同步（若本任务实施）**

```bash
git add docs/CONSISTENCY_VALIDATION.md docs/ROADMAP.md
git commit -m "docs: register inspect sync mode"
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

- [ ] **Step 2: 运行 inspect 模式验收**

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --inspect`
Expected:
- `INSPECT`
- `SOURCE ROOT: skills`
- `TARGET ROOT: .claude-sync-preview`
- `FOUND 12 skills`
- 每项包含 `source` / `target` / `status`
- `SUMMARY`

- [ ] **Step 3: 运行互斥参数验收**

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --inspect --dry-run`
Expected: 非零退出码，stderr 包含 `Cannot combine --inspect and --dry-run.`

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --inspect --force`
Expected: 非零退出码，stderr 包含 `Cannot combine --inspect and --force.`

- [ ] **Step 4: 运行既有模式回归检查**

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --dry-run`
Expected: 仍输出 `DRY-RUN` / `FOUND 12 skills` / `PLAN COPY ...`

- [ ] **Step 5: 清理临时目录（若有）**

Run: `python -c "from pathlib import Path; import shutil; target = Path('.claude-sync-preview'); shutil.rmtree(target) if target.exists() else None; print('OK')"`
Expected: `OK`

- [ ] **Step 6: 提交 Claude Code skills sync inspect foundation 基线**

```bash
git add tools/sync_claude_code_skills.py docs/CLAUDE_CODE_SETUP.md docs/CONSISTENCY_VALIDATION.md docs/ROADMAP.md
git commit -m "feat: add inspect mode to skills sync"
```

---

## Self-Review

- **Spec coverage:** 本计划覆盖了 `--inspect` 模式实现、setup 文档同步、视需要的 validation/roadmap 同步，以及 inspect / dry-run / sync 三段能力的最终验收。
- **Placeholder scan:** 已移除 `TBD`、`TODO`、`implement later`、`appropriate` 等占位措辞；涉及代码与文档改动的步骤都给了明确代码骨架和验证命令。
- **Type consistency:** 统一使用 `tools/sync_claude_code_skills.py` 作为脚本路径，统一使用 `--inspect`、`--dry-run`、`--force` 的互斥关系，统一以 `INSPECT` / `SUMMARY` 作为 inspect 输出骨架。
