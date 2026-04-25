# Claude Code Setup Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 un9flow 增加 `docs/CLAUDE_CODE_SETUP.md`，把 Claude Code 从“如何消费仓库”的说明推进到“如何最小把仓库接起来”的 setup 骨架说明。

**Architecture:** 本轮只做 Claude Code 最小 setup 真源，不做自动安装器、自动同步、一键 setup、多 host setup 或分发系统。新增 `docs/CLAUDE_CODE_SETUP.md` 后，由它固定 setup 前提、最小 setup 对象、最小 setup 步骤、setup 后验证与当前明确不做，再同步 `docs/CLAUDE_CODE_HOST.md`、`README.md`，并视需要登记到 `docs/CONSISTENCY_VALIDATION.md` 与 `docs/ROADMAP.md`。

**Tech Stack:** Markdown, Python 3, git, Claude Code

---

## File Structure

### Existing files to modify

- `docs/CLAUDE_CODE_HOST.md` — 增加对 `docs/CLAUDE_CODE_SETUP.md` 的回指，明确 host 与 setup 的分工。
- `README.md` — 暴露 `docs/CLAUDE_CODE_SETUP.md` 为仓库入口之一。
- `docs/CONSISTENCY_VALIDATION.md`（如需要最小规则登记）— 若要把 setup 真源纳入现有 docs 真源受控对象，则补最小规则约束。
- `docs/ROADMAP.md`（如需要阶段落地记录）— 若要把 Claude Code setup foundation 记为下一阶段落地点，则补最小路线图记录。

### Existing files to read but not modify

- `docs/PLATFORMS.md`
- `docs/SKILL_ARCHITECTURE.md`
- `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`
- `docs/ORCHESTRATION.md`
- `tools/validate_consistency.py`
- `tools/run_generation_regression.py`

### New files to create

- `docs/CLAUDE_CODE_SETUP.md` — Claude Code 的最小 setup 真源。
- `docs/superpowers/plans/2026-04-25-un9flow-claude-code-setup-foundation.md` — 当前 implementation plan。

### No new scripts/workflows

本计划不新增自动安装器、目录同步脚本、一键 setup 或新的 GitHub workflow。

---

### Task 1: 先创建 Claude Code setup 真源文档

**Files:**
- Create: `docs/CLAUDE_CODE_SETUP.md`
- Test: `docs/CLAUDE_CODE_SETUP.md`

- [ ] **Step 1: 运行检查，确认当前还没有 `docs/CLAUDE_CODE_SETUP.md`**

Run: `git ls-files "docs/CLAUDE_CODE_SETUP.md"`
Expected: 无输出

- [ ] **Step 2: 创建 `docs/CLAUDE_CODE_SETUP.md` 文档骨架**

```md
# Claude Code Setup

## 目标
- 说明如何在 Claude Code 环境下最小把本仓库接起来，而不是重新定义方法论、host 消费语义或调度协议。

## setup 前提
- 本地已获取仓库完整内容
- 正式 `skills/**/SKILL.md` 存在
- Python 环境可运行 `tools/validate_consistency.py` 与 `tools/run_generation_regression.py`

## 最小 setup 对象
### 必须关心的对象
- `skills/**/SKILL.md`
- `docs/CLAUDE_CODE_HOST.md`
- `docs/SKILL_ARCHITECTURE.md`
- `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`
- `docs/ORCHESTRATION.md`
- `tools/validate_consistency.py`
- `tools/run_generation_regression.py`

### 可选关心的对象
- `docs/INCIDENT_WORKFLOW.md`
- `docs/BRINGUP_PATH.md`
- `docs/DESIGN_SAFETY_REVIEW.md`
- `docs/WATCHDOG_TIMEOUT_AUDIT.md`
- `docs/REGISTER_STATE_AUDIT.md`
- `docs/templates/**`
- `docs/cases/**`

### 当前明确不属于 setup 的对象
- 自动安装器
- 自动目录同步脚本
- 多 host setup
- 分发包 / 发布产物
- CI 平台配置自动注入
- 外部平台专用目录映射

## 最小 setup 步骤
1. 准备仓库
2. 确认正式入口来自 `skills/**/SKILL.md`
3. 确认规则支撑文档
4. 运行最小验证：
   - `python tools/validate_consistency.py`
   - `python tools/run_generation_regression.py --check`
5. 从总入口或三个主场景 skill 开始消费

## setup 后验证
- 本地存在正式 `skills/**/SKILL.md`
- Claude Code host 真源与关键 docs 可读
- consistency validation 通过
- generation regression check 通过
- `README.md` / `docs/PLATFORMS.md` / `docs/CLAUDE_CODE_HOST.md` / `docs/CLAUDE_CODE_SETUP.md` 之间入口关系可追溯

## 当前明确不做
- 不自动复制 skill 到宿主目录
- 不自动生成 Claude Code 本地配置
- 不自动注入 slash command
- 不自动处理跨仓库映射
- 不提供一键 setup
- 不保证 setup 文档之外的 host 也成立

## 与其他文档的关系
- host 接入语义问题回 `docs/CLAUDE_CODE_HOST.md`
- 平台战略与非承诺边界问题回 `docs/PLATFORMS.md`
- skill 入口边界问题回 `docs/SKILL_ARCHITECTURE.md`
- prompt 协议问题回 `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`
```

- [ ] **Step 3: 运行最小文本检查，确认 7 个主段全部落地**

Run: `python -c "from pathlib import Path; text = Path('docs/CLAUDE_CODE_SETUP.md').read_text(encoding='utf-8'); required = ['## 目标', '## setup 前提', '## 最小 setup 对象', '## 最小 setup 步骤', '## setup 后验证', '## 当前明确不做', '## 与其他文档的关系']; missing = [item for item in required if item not in text]; print('OK' if not missing else missing)"`
Expected: `OK`

- [ ] **Step 4: 运行最小文本检查，确认 setup 边界与验证命令已存在**

Run: `python -c "from pathlib import Path; text = Path('docs/CLAUDE_CODE_SETUP.md').read_text(encoding='utf-8'); required = ['skills/**/SKILL.md', 'docs/CLAUDE_CODE_HOST.md', 'tools/validate_consistency.py', 'tools/run_generation_regression.py --check', '自动安装器', '多 host setup']; missing = [item for item in required if item not in text]; print('OK' if not missing else missing)"`
Expected: `OK`

- [ ] **Step 5: 提交 Claude Code setup 真源文档**

```bash
git add docs/CLAUDE_CODE_SETUP.md
git commit -m "feat: add Claude Code setup guide"
```

---

### Task 2: 把 Claude Code host 文档切换到新的 setup 真源分工

**Files:**
- Modify: `docs/CLAUDE_CODE_HOST.md`
- Test: `docs/CLAUDE_CODE_HOST.md`
- Test: `docs/CLAUDE_CODE_SETUP.md`

- [ ] **Step 1: 在 `docs/CLAUDE_CODE_HOST.md` 中增加对 `docs/CLAUDE_CODE_SETUP.md` 的显式回指**

```md
- Claude Code 的最小 setup 前提、setup 对象、setup 步骤与 setup 后验证详见 `docs/CLAUDE_CODE_SETUP.md`。
```

- [ ] **Step 2: 收紧 host 文档中的 setup 语气，使其保持“如何消费”的角色**

```md
把 `docs/CLAUDE_CODE_HOST.md` 中任何接近安装说明的句子收紧为：
- host 文档负责说明“怎么理解并消费”
- setup 真源负责说明“怎么最小接起来”
```

- [ ] **Step 3: 运行最小文本检查，确认 host 文档已回指 setup 真源**

Run: `python -c "from pathlib import Path; text = Path('docs/CLAUDE_CODE_HOST.md').read_text(encoding='utf-8'); print('OK' if 'docs/CLAUDE_CODE_SETUP.md' in text else 'missing')"`
Expected: `OK`

- [ ] **Step 4: 提交 host 文档同步**

```bash
git add docs/CLAUDE_CODE_HOST.md
git commit -m "docs: align host guide with setup guide"
```

---

### Task 3: 把 README 暴露为 Claude Code setup 真源入口

**Files:**
- Modify: `README.md`
- Test: `README.md`
- Test: `docs/CLAUDE_CODE_SETUP.md`

- [ ] **Step 1: 在 `README.md` 的入口列表中增加 `docs/CLAUDE_CODE_SETUP.md`**

```md
- `docs/CLAUDE_CODE_SETUP.md`：Claude Code 的最小 setup 真源，定义 setup 前提、最小 setup 对象、最小步骤与 setup 后验证
```

- [ ] **Step 2: 运行最小文本检查，确认 README 已暴露 setup 真源入口**

Run: `python -c "from pathlib import Path; files = ['README.md', 'docs/CLAUDE_CODE_SETUP.md']; missing = [file for file in files if 'docs/CLAUDE_CODE_SETUP.md' not in Path(file).read_text(encoding='utf-8') and file == 'README.md']; print('OK' if not missing else missing)"`
Expected: `OK`

- [ ] **Step 3: 提交 README 入口同步**

```bash
git add README.md
git commit -m "docs: expose Claude Code setup guide"
```

---

### Task 4: 视需要把 consistency validation 与 roadmap 同步到 setup 真源

**Files:**
- Modify: `docs/CONSISTENCY_VALIDATION.md`
- Modify: `docs/ROADMAP.md`
- Test: `docs/CONSISTENCY_VALIDATION.md`
- Test: `docs/ROADMAP.md`

- [ ] **Step 1: 在 `docs/CONSISTENCY_VALIDATION.md` 增加 Claude Code setup 真源规则（若决定纳入）**

```md
### Claude Code setup 真源规则

1. `docs/CLAUDE_CODE_SETUP.md` 是 Claude Code 的最小 setup 真源文档。
2. `docs/CLAUDE_CODE_SETUP.md` 必须回指：
   - `docs/CLAUDE_CODE_HOST.md`
   - `docs/PLATFORMS.md`
   - `docs/SKILL_ARCHITECTURE.md`
   - `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`
3. `docs/CLAUDE_CODE_SETUP.md` 必须明确：
   - setup 前提
   - 最小 setup 对象
   - 最小 setup 步骤
   - setup 后验证
   - 当前明确不做
```

- [ ] **Step 2: 在 `docs/ROADMAP.md` 增加下一阶段 Claude Code setup foundation 记录（若决定落路线图）**

```md
## v9 - Claude Code setup 骨架

目标：把 Claude Code 从“如何消费仓库”的说明推进到“如何最小把仓库接起来”的 setup 骨架说明。

计划方向：
- [x] `docs/CLAUDE_CODE_SETUP.md` 已落地为最小 setup 真源
- [x] setup 对象边界已固定为必须关心 / 可选关心 / 明确不属于 setup 三类
- [x] 最小 setup 步骤与 setup 后验证标准已被显式固定
```

- [ ] **Step 3: 运行最小文本检查，确认相关文档都命中新 setup 真源**

Run: `python -c "from pathlib import Path; files = ['docs/CLAUDE_CODE_HOST.md', 'README.md']; missing = [file for file in files if 'docs/CLAUDE_CODE_SETUP.md' not in Path(file).read_text(encoding='utf-8')]; print('OK' if not missing else missing)"`
Expected: `OK`

- [ ] **Step 4: 提交规则与路线图同步（若本任务实施）**

```bash
git add docs/CONSISTENCY_VALIDATION.md docs/ROADMAP.md
git commit -m "docs: register Claude Code setup guide"
```

---

### Task 5: 做端到端验收

**Files:**
- Test: `tools/validate_consistency.py`
- Test: `docs/CLAUDE_CODE_SETUP.md`
- Test: `docs/CLAUDE_CODE_HOST.md`
- Test: `README.md`

- [ ] **Step 1: 运行 consistency validation 最终验收**

Run: `python tools/validate_consistency.py`
Expected: `Validation result: PASS`

- [ ] **Step 2: 运行 Claude Code setup 回指最小检查**

Run: `python -c "from pathlib import Path; text = Path('docs/CLAUDE_CODE_SETUP.md').read_text(encoding='utf-8'); required = ['docs/CLAUDE_CODE_HOST.md', 'docs/PLATFORMS.md', 'docs/SKILL_ARCHITECTURE.md', 'docs/ORCHESTRATOR_PROMPT_CONTRACT.md', 'tools/validate_consistency.py', 'tools/run_generation_regression.py --check']; missing = [item for item in required if item not in text]; print('OK' if not missing else missing)"`
Expected: `OK`

- [ ] **Step 3: 运行 host 与 README 最小检查**

Run: `python -c "from pathlib import Path; files = ['docs/CLAUDE_CODE_HOST.md', 'README.md']; missing = [file for file in files if 'docs/CLAUDE_CODE_SETUP.md' not in Path(file).read_text(encoding='utf-8')]; print('OK' if not missing else missing)"`
Expected: `OK`

- [ ] **Step 4: 提交 Claude Code setup foundation 基线**

```bash
git add docs/CLAUDE_CODE_SETUP.md docs/CLAUDE_CODE_HOST.md README.md docs/CONSISTENCY_VALIDATION.md docs/ROADMAP.md
git commit -m "feat: add Claude Code setup guide"
```

---

## Self-Review

- **Spec coverage:** 本计划覆盖了新建 `docs/CLAUDE_CODE_SETUP.md`、同步 `docs/CLAUDE_CODE_HOST.md` 分工、暴露 README 入口、视需要登记 consistency validation / roadmap，以及最终 consistency validation 与最小文本验收。
- **Placeholder scan:** 已移除 `TBD`、`TODO`、`implement later`、`appropriate` 等占位措辞；涉及文档改动的步骤都给了明确文本骨架和验证命令。
- **Type consistency:** 统一使用 `docs/CLAUDE_CODE_SETUP.md` 作为 setup 真源路径，统一使用“必须关心 / 可选关心 / 明确不属于 setup”三类对象边界，统一以 `python tools/validate_consistency.py` 与 `python tools/run_generation_regression.py --check` 作为最小验证路径。
