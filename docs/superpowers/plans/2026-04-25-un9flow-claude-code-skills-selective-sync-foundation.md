# Claude Code Selective Skills Sync Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 `tools/sync_claude_code_skills.py` 增加 `--only <skill-name>`，让同步器能精确点名只处理某一个正式 skill。

**Architecture:** 本轮只做按 skill name 精确过滤的第一轮 selective sync，不做多值过滤、按组过滤、模式匹配或 exclude。`--only` 被定义为过滤参数，而不是独立模式：它在 inspect / dry-run / sync 三种模式之前统一缩小对象集合；若 skill 名不存在，则硬失败并列出可用值。

**Tech Stack:** Python 3, pathlib, argparse, shutil, git, Claude Code

---

## File Structure

### Existing files to modify

- `tools/sync_claude_code_skills.py` — 增加 `--only <skill-name>` 精确过滤能力。
- `docs/CLAUDE_CODE_SETUP.md` — 把 selective sync 记为“最小可控同步”的下一步能力。
- `docs/CONSISTENCY_VALIDATION.md`（如需要最小规则登记）— 若要把 `--only` 的精确匹配边界纳入现有规则，则补最小约束。
- `docs/ROADMAP.md`（如需要阶段落地记录）— 若要把 selective sync 记为下一阶段落地点，则补最小路线图记录。

### Existing files to read but not modify

- `docs/CLAUDE_CODE_HOST.md`
- `docs/PLATFORMS.md`
- `skills/**/SKILL.md`

### New files to create

- `docs/superpowers/plans/2026-04-25-un9flow-claude-code-skills-selective-sync-foundation.md` — 当前 implementation plan。

### No advanced filters

本计划不新增多个 `--only`、逗号列表、按组过滤、路径模式过滤或 exclude 逻辑。

---

### Task 1: 给同步脚本增加 `--only <skill-name>`

**Files:**
- Modify: `tools/sync_claude_code_skills.py`
- Test: `tools/sync_claude_code_skills.py`

- [ ] **Step 1: 在参数解析中增加 `--only`**

```python
parser.add_argument(
    "--only",
    help="Sync exactly one skill directory name, such as orchestration or bringup-path.",
)
```

- [ ] **Step 2: 增加可用 skill 名提取函数**

```python
def available_skill_names(skill_files: list[Path]) -> list[str]:
    return sorted({skill_file.parent.name for skill_file in skill_files})
```

- [ ] **Step 3: 增加精确过滤函数**

```python
def filter_skill_files(skill_files: list[Path], only: str | None) -> list[Path]:
    if only is None:
        return skill_files

    filtered = [skill_file for skill_file in skill_files if skill_file.parent.name == only]
    if filtered:
        return filtered

    available = ", ".join(available_skill_names(skill_files))
    raise ValueError(f"Unknown skill: {only}\nAvailable skills: {available}")
```

- [ ] **Step 4: 在主入口中接入 `--only` 过滤**

```python
skill_files = discover_skill_files()
try:
    skill_files = filter_skill_files(skill_files, args.only)
except ValueError as exc:
    print(str(exc), file=sys.stderr)
    return 2
```

- [ ] **Step 5: 运行 selective inspect 验证**

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --inspect --only orchestration`
Expected:
- `FOUND 1 skills`
- 只出现 `skills/orchestration/SKILL.md`
- `SUMMARY` 中 `total: 1`

- [ ] **Step 6: 运行 selective dry-run 验证**

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --dry-run --only orchestration`
Expected:
- `DRY-RUN`
- `FOUND 1 skills`
- 只出现 `skills/orchestration/SKILL.md`

- [ ] **Step 7: 运行 selective sync 验证**

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --only orchestration --force`
Expected:
- 只输出一条 `SYNCED skills/orchestration/SKILL.md -> ...`
- `SUMMARY: synced 1, skipped 0, failed 0`

- [ ] **Step 8: 运行未知 skill 硬失败验证**

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --only does-not-exist --dry-run`
Expected:
- 非零退出码
- stderr 包含 `Unknown skill: does-not-exist`
- stderr 包含 `Available skills:`

- [ ] **Step 9: 运行全量模式回归检查**

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --dry-run`
Expected:
- 仍输出 `FOUND 12 skills`
- 仍保持全量 12-skill 行为

- [ ] **Step 10: 清理临时目录**

Run: `python -c "from pathlib import Path; import shutil; target = Path('.claude-sync-preview'); shutil.rmtree(target) if target.exists() else None; print('OK')"`
Expected: `OK`

- [ ] **Step 11: 提交 selective sync 实现**

```bash
git add tools/sync_claude_code_skills.py
git commit -m "feat: add selective skill sync"
```

---

### Task 2: 让 setup 文档承认 `--only` 是最小可控同步能力

**Files:**
- Modify: `docs/CLAUDE_CODE_SETUP.md`
- Test: `docs/CLAUDE_CODE_SETUP.md`

- [ ] **Step 1: 在 setup 文档中增加 `--only` 回指**

```md
- `python tools/sync_claude_code_skills.py --target-root <path> --only <skill-name> --dry-run`：用于精确点名单个正式 skill 的预演同步。
```

- [ ] **Step 2: 明确 `--only` 的边界**

```md
- `--only` 第一轮只支持按 skill 目录名精确过滤一个 skill。
- 当前不支持多个 `--only`、按组过滤、路径模式过滤或 exclude。
```

- [ ] **Step 3: 运行最小文本检查，确认 setup 文档已登记 `--only`**

Run: `python -c "from pathlib import Path; text = Path('docs/CLAUDE_CODE_SETUP.md').read_text(encoding='utf-8'); required = ['--only <skill-name>', '精确过滤一个 skill', '不支持多个 `--only`']; missing = [item for item in required if item not in text]; print('OK' if not missing else missing)"`
Expected: `OK`

- [ ] **Step 4: 提交 setup 文档同步**

```bash
git add docs/CLAUDE_CODE_SETUP.md
git commit -m "docs: register selective sync"
```

---

### Task 3: 视需要把 validation / roadmap 同步到 selective sync

**Files:**
- Modify: `docs/CONSISTENCY_VALIDATION.md`
- Modify: `docs/ROADMAP.md`
- Test: `docs/CONSISTENCY_VALIDATION.md`
- Test: `docs/ROADMAP.md`

- [ ] **Step 1: 在 `docs/CONSISTENCY_VALIDATION.md` 增加 selective sync 边界规则（若决定纳入）**

```md
8. `tools/sync_claude_code_skills.py --only <skill-name>` 只允许按 skill 目录名精确匹配一个正式 skill。
9. `--only` 不得支持多个值、按组过滤、路径模式过滤或 exclude。
10. 未命中的 skill 名必须硬失败并显式输出可用 skill 列表。
```

- [ ] **Step 2: 在 `docs/ROADMAP.md` 增加 selective sync 落地记录（若决定落路线图）**

```md
## v12 - Claude Code selective skills sync

目标：让 skills-only 同步脚本能精确点名只处理某一个正式 skill。

计划方向：
- [x] `--only <skill-name>` 已落地
- [x] `--only` 已在 inspect / dry-run / sync 三种模式下生效
- [x] 不存在的 skill 会硬失败并给出可用值列表
```

- [ ] **Step 3: 运行最小文本检查，确认相关文档都命中 `--only` 语义**

Run: `python -c "from pathlib import Path; files = ['docs/CLAUDE_CODE_SETUP.md']; optional = ['docs/CONSISTENCY_VALIDATION.md', 'docs/ROADMAP.md']; missing = [file for file in files if '--only' not in Path(file).read_text(encoding='utf-8')]; print('OK' if not missing else missing)"`
Expected: `OK`

- [ ] **Step 4: 提交规则与路线图同步（若本任务实施）**

```bash
git add docs/CONSISTENCY_VALIDATION.md docs/ROADMAP.md
git commit -m "docs: register selective sync"
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

- [ ] **Step 2: 运行 selective inspect 验收**

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --inspect --only orchestration`
Expected:
- `FOUND 1 skills`
- 只出现 `skills/orchestration/SKILL.md`
- `SUMMARY` 中 `total: 1`

- [ ] **Step 3: 运行 selective dry-run 验收**

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --dry-run --only orchestration`
Expected:
- `DRY-RUN`
- `FOUND 1 skills`
- 只输出 `orchestration` 对应计划

- [ ] **Step 4: 运行 selective sync 验收**

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --only orchestration --force`
Expected:
- 只输出一条 `SYNCED ...`
- `SUMMARY: synced 1, skipped 0, failed 0`

- [ ] **Step 5: 运行未知 skill 验收**

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --only does-not-exist --dry-run`
Expected:
- 非零退出码
- `Unknown skill: does-not-exist`
- `Available skills:`

- [ ] **Step 6: 运行全量模式回归检查**

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --dry-run`
Expected:
- 仍输出 `FOUND 12 skills`
- 不带 `--only` 时全量行为不被破坏

- [ ] **Step 7: 清理临时目录**

Run: `python -c "from pathlib import Path; import shutil; target = Path('.claude-sync-preview'); shutil.rmtree(target) if target.exists() else None; print('OK')"`
Expected: `OK`

- [ ] **Step 8: 提交 selective sync foundation 基线**

```bash
git add tools/sync_claude_code_skills.py docs/CLAUDE_CODE_SETUP.md docs/CONSISTENCY_VALIDATION.md docs/ROADMAP.md
git commit -m "feat: add selective skill sync"
```

---

## Self-Review

- **Spec coverage:** 本计划覆盖了 `--only <skill-name>` 实现、setup 文档同步、视需要的 validation/roadmap 同步，以及 selective inspect / dry-run / sync / unknown skill / full-mode regression 的最终验收。
- **Placeholder scan:** 已移除 `TBD`、`TODO`、`implement later`、`appropriate` 等占位措辞；涉及代码与文档改动的步骤都给了明确代码骨架和验证命令。
- **Type consistency:** 统一使用 `--only <skill-name>` 作为过滤参数，统一规定精确 skill 名匹配，统一保持 inspect / dry-run / sync 三种模式不变，只缩小对象集合。
