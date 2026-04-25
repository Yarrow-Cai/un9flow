# Claude Code Skills Sync Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 un9flow 增加 `tools/sync_claude_code_skills.py`，把正式 `skills/**/SKILL.md` 入口同步到 Claude Code 消费目录骨架。

**Architecture:** 本轮只做 skills-only 的最小同步脚本，不做 docs / templates / cases / golden 同步，也不做安装器、多 host 同步器或分发系统。脚本通过发现 `skills/**/SKILL.md`、按来源相对路径镜像到 `--target-root`、支持 `--dry-run` 与 `--force`，把“文档真源 → 最小可执行骨架”第一次真正落地。

**Tech Stack:** Python 3, pathlib, argparse, shutil, git, Claude Code

---

## File Structure

### Existing files to modify

- `docs/CLAUDE_CODE_SETUP.md` — 把 skills-only 同步脚本登记为第一批可执行 setup 落点。
- `docs/CLAUDE_CODE_HOST.md`（如需要最小同步器入口说明）— 若需要显式说明“直接消费层”的同步器，则做最小补充。
- `docs/CONSISTENCY_VALIDATION.md`（如需要最小规则登记）— 若要把同步脚本纳入现有 docs 真源受控对象，则补最小规则约束。
- `docs/ROADMAP.md`（如需要阶段落地记录）— 若要把 skills-only 同步器记为下一阶段落地点，则补最小路线图记录。

### Existing files to read but not modify

- `docs/PLATFORMS.md`
- `docs/SKILL_ARCHITECTURE.md`
- `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`
- `docs/CLAUDE_CODE_HOST.md`
- `docs/CLAUDE_CODE_SETUP.md`
- `skills/**/SKILL.md`

### New files to create

- `tools/sync_claude_code_skills.py` — Claude Code skills-only 最小同步脚本。
- `docs/superpowers/plans/2026-04-25-un9flow-claude-code-skills-sync-foundation.md` — 当前 implementation plan。

### No new installers/workflows

本计划不新增自动安装器、自动目录同步系统、多 host 分支逻辑或新的 GitHub workflow。

---

### Task 1: 先创建 skills-only 同步脚本骨架

**Files:**
- Create: `tools/sync_claude_code_skills.py`
- Test: `tools/sync_claude_code_skills.py`

- [ ] **Step 1: 运行检查，确认当前还没有 `tools/sync_claude_code_skills.py`**

Run: `git ls-files "tools/sync_claude_code_skills.py"`
Expected: 无输出

- [ ] **Step 2: 创建脚本骨架，支持 `--target-root`、`--dry-run`、`--force`**

```python
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Sync skills/**/SKILL.md into a Claude Code target root."
    )
    parser.add_argument("--target-root", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    return parser
```

- [ ] **Step 3: 实现 skill 发现逻辑，只接受 `skills/**/SKILL.md`**

```python
def discover_skill_files() -> list[Path]:
    return sorted(path for path in SKILLS_ROOT.rglob("SKILL.md") if path.is_file())
```

- [ ] **Step 4: 实现目标路径镜像规则**

```python
def target_path_for(skill_file: Path, target_root: Path) -> Path:
    relative_path = skill_file.relative_to(ROOT)
    return target_root / relative_path
```

- [ ] **Step 5: 实现 dry-run / force / summary 最小行为**

```python
def sync_skill_files(skill_files: list[Path], target_root: Path, dry_run: bool, force: bool) -> int:
    if not skill_files:
        print("No skill files found.", file=sys.stderr)
        return 2

    if dry_run:
        print("DRY-RUN")
        print(f"FOUND {len(skill_files)} skills")

    synced = 0
    skipped = 0
    failed = 0

    for skill_file in skill_files:
        destination = target_path_for(skill_file, target_root)
        if dry_run:
            print(f"PLAN COPY {skill_file.relative_to(ROOT)} -> {destination}")
            continue
        if destination.exists() and not force:
            print(f"SKIPPED {skill_file.relative_to(ROOT)} -> {destination}", file=sys.stderr)
            skipped += 1
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(skill_file, destination)
        print(f"SYNCED {skill_file.relative_to(ROOT)} -> {destination}")
        synced += 1

    print(f"SUMMARY: synced {synced}, skipped {skipped}, failed {failed}")
    return 0 if failed == 0 else 1
```

- [ ] **Step 6: 实现主入口**

```python
def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    target_root = Path(args.target_root).resolve()
    skill_files = discover_skill_files()
    return sync_skill_files(skill_files, target_root, args.dry_run, args.force)


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 7: 运行 dry-run 验证，确认只发现并计划同步正式 `skills/**/SKILL.md`**

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --dry-run`
Expected:
- 输出 `DRY-RUN`
- 输出 `FOUND 12 skills`
- 每条计划路径均形如 `skills/<name>/SKILL.md -> <target-root>/skills/<name>/SKILL.md`
- 不出现 `docs/`、`templates/`、`cases/` 路径

- [ ] **Step 8: 提交同步脚本骨架**

```bash
git add tools/sync_claude_code_skills.py
git commit -m "feat: add Claude Code skills sync script"
```

---

### Task 2: 让 setup 文档承认这个脚本是第一批可执行落点

**Files:**
- Modify: `docs/CLAUDE_CODE_SETUP.md`
- Test: `docs/CLAUDE_CODE_SETUP.md`

- [ ] **Step 1: 在 `docs/CLAUDE_CODE_SETUP.md` 中增加对同步脚本的回指**

```md
- `tools/sync_claude_code_skills.py`：用于把正式 `skills/**/SKILL.md` 入口同步到 Claude Code 消费目录骨架。
```

- [ ] **Step 2: 在 setup 后验证中增加 dry-run 检查**

```md
- `python tools/sync_claude_code_skills.py --target-root <path> --dry-run` 可输出稳定同步计划，且仅覆盖 `skills/**/SKILL.md`。
```

- [ ] **Step 3: 运行最小文本检查，确认 setup 文档已回指同步脚本**

Run: `python -c "from pathlib import Path; text = Path('docs/CLAUDE_CODE_SETUP.md').read_text(encoding='utf-8'); required = ['tools/sync_claude_code_skills.py', '--dry-run', 'skills/**/SKILL.md']; missing = [item for item in required if item not in text]; print('OK' if not missing else missing)"`
Expected: `OK`

- [ ] **Step 4: 提交 setup 文档同步**

```bash
git add docs/CLAUDE_CODE_SETUP.md
git commit -m "docs: register skills sync script"
```

---

### Task 3: 视需要把 host / validation / roadmap 同步到脚本落点

**Files:**
- Modify: `docs/CLAUDE_CODE_HOST.md`
- Modify: `docs/CONSISTENCY_VALIDATION.md`
- Modify: `docs/ROADMAP.md`
- Test: `docs/CLAUDE_CODE_HOST.md`
- Test: `docs/CONSISTENCY_VALIDATION.md`
- Test: `docs/ROADMAP.md`

- [ ] **Step 1: 在 `docs/CLAUDE_CODE_HOST.md` 中补最小脚本入口说明（若决定补）**

```md
- 直接消费层的第一批可执行落点是 `tools/sync_claude_code_skills.py`，用于把正式 `skills/**/SKILL.md` 同步到目标消费目录骨架。
```

- [ ] **Step 2: 在 `docs/CONSISTENCY_VALIDATION.md` 增加脚本边界规则（若决定纳入）**

```md
### Claude Code skills-only 同步脚本规则

1. `tools/sync_claude_code_skills.py` 只允许处理 `skills/**/SKILL.md`。
2. 不得同步 docs / templates / cases / golden / regression 文件。
3. 必须支持：
   - `--target-root`
   - `--dry-run`
   - `--force`
4. 目标路径必须按来源相对路径稳定镜像。
```

- [ ] **Step 3: 在 `docs/ROADMAP.md` 增加下一阶段脚本落地记录（若决定落路线图）**

```md
## v10 - Claude Code skills-only 同步骨架

目标：把正式 `skills/**/SKILL.md` 入口同步到 Claude Code 消费目录骨架，形成第一条最小可执行 host 接入动作。

计划方向：
- [x] `tools/sync_claude_code_skills.py` 已落地为最小同步脚本
- [x] 目标目录结构已固定为来源相对路径镜像
- [x] dry-run / force / summary 最小行为已被显式固定
```

- [ ] **Step 4: 运行最小文本检查，确认相关文档都命中同步脚本**

Run: `python -c "from pathlib import Path; files = ['docs/CLAUDE_CODE_SETUP.md']; optional = ['docs/CLAUDE_CODE_HOST.md', 'docs/CONSISTENCY_VALIDATION.md', 'docs/ROADMAP.md']; missing = [file for file in files if 'tools/sync_claude_code_skills.py' not in Path(file).read_text(encoding='utf-8')]; print('OK' if not missing else missing)"`
Expected: `OK`

- [ ] **Step 5: 提交文档与规则同步（若本任务实施）**

```bash
git add docs/CLAUDE_CODE_HOST.md docs/CONSISTENCY_VALIDATION.md docs/ROADMAP.md
git commit -m "docs: register skills sync foundation"
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

- [ ] **Step 2: 运行同步脚本 dry-run 验收**

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --dry-run`
Expected:
- `DRY-RUN`
- `FOUND 12 skills`
- 只出现 `skills/**/SKILL.md` 的同步计划

- [ ] **Step 3: 运行真实同步验收到临时目录**

Run: `python tools/sync_claude_code_skills.py --target-root .claude-sync-preview --force`
Expected:
- 多条 `SYNCED ...`
- `SUMMARY: synced 12, skipped 0, failed 0`

- [ ] **Step 4: 运行目标目录检查**

Run: `python -c "from pathlib import Path; root = Path('.claude-sync-preview/skills'); files = sorted(path.relative_to(root).as_posix() for path in root.rglob('SKILL.md')); print(files)"`
Expected: 输出 12 个 `<skill-name>/SKILL.md`，且不含 docs/templates/cases 路径

- [ ] **Step 5: 清理临时验收目录**

Run: `python -c "from pathlib import Path; import shutil; target = Path('.claude-sync-preview'); shutil.rmtree(target) if target.exists() else None; print('OK')"`
Expected: `OK`

- [ ] **Step 6: 提交 Claude Code skills sync foundation 基线**

```bash
git add tools/sync_claude_code_skills.py docs/CLAUDE_CODE_SETUP.md docs/CLAUDE_CODE_HOST.md docs/CONSISTENCY_VALIDATION.md docs/ROADMAP.md
git commit -m "feat: add Claude Code skills sync script"
```

---

## Self-Review

- **Spec coverage:** 本计划覆盖了新建 `tools/sync_claude_code_skills.py`、同步 setup 文档、视需要同步 host/validation/roadmap，以及 dry-run / force / summary 的最终验收。
- **Placeholder scan:** 已移除 `TBD`、`TODO`、`implement later`、`appropriate` 等占位措辞；涉及代码与文档改动的步骤都给了明确代码骨架和验证命令。
- **Type consistency:** 统一使用 `tools/sync_claude_code_skills.py` 作为脚本路径，统一使用 `skills/**/SKILL.md` 作为唯一同步对象，统一使用 `--target-root`、`--dry-run`、`--force` 三个 CLI 参数。
