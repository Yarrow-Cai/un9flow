# Claude Code Host Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 un9flow 增加 `docs/CLAUDE_CODE_HOST.md`，把 Claude Code 固定为第一个有正式接入真源说明的 host。

**Architecture:** 本轮只做 Claude Code first 的最小 host 接入骨架，不做自动安装器、目录生成器或一键分发。新增 `docs/CLAUDE_CODE_HOST.md` 后，由它解释 Claude Code 视角下的目录映射、最小接入步骤、当前可消费能力与不承诺边界，再同步 `docs/PLATFORMS.md` 与 `README.md`，让平台战略层与入口层都能回指这份接入真源。

**Tech Stack:** Markdown, Python 3, git, Claude Code

---

## File Structure

### Existing files to modify

- `docs/PLATFORMS.md` — 把 Claude Code 从平台方向说明推进到有专门接入真源回指的首个 host。
- `README.md` — 暴露 `docs/CLAUDE_CODE_HOST.md` 为仓库入口之一。
- `docs/CONSISTENCY_VALIDATION.md`（如需要最小规则登记）— 若要把 Claude Code host 接入真源纳入现有 docs 真源受控对象，则补最小规则约束。
- `docs/ROADMAP.md`（如需要阶段落地记录）— 若要把 Claude Code host foundation 记为下一阶段落地点，则补最小路线图记录。

### Existing files to read but not modify

- `docs/SKILL_ARCHITECTURE.md`
- `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`
- `docs/ORCHESTRATION.md`
- `skills/orchestration/SKILL.md`
- `skills/incident-investigation/SKILL.md`
- `skills/bringup-path/SKILL.md`
- `skills/design-safety-review/SKILL.md`
- `skills/watchdog-timeout-audit/SKILL.md`

### New files to create

- `docs/CLAUDE_CODE_HOST.md` — Claude Code 的最小 host 接入真源。
- `docs/superpowers/plans/2026-04-25-un9flow-claude-code-host-foundation.md` — 当前 implementation plan。

### No new scripts/workflows

本计划不新增自动安装器、目录映射脚本、distribution pipeline 或新的 GitHub workflow。

---

### Task 1: 先创建 Claude Code host 接入真源文档

**Files:**
- Create: `docs/CLAUDE_CODE_HOST.md`
- Test: `docs/CLAUDE_CODE_HOST.md`

- [ ] **Step 1: 运行检查，确认当前还没有 `docs/CLAUDE_CODE_HOST.md`**

Run: `git ls-files "docs/CLAUDE_CODE_HOST.md"`
Expected: 无输出

- [ ] **Step 2: 创建 `docs/CLAUDE_CODE_HOST.md` 文档骨架**

```md
# Claude Code Host

## 目标
- 说明 Claude Code 如何消费本仓库，而不是重新定义方法论、场景边界或调度协议。

## 宿主定位
- Claude Code 是当前仓库首个 host 接入锚点。
- 当前文档只定义 Claude Code 维度下的最小接入骨架。
- 这不代表多 host 接入已经完成。

## 目录映射
### 直接消费层
- `skills/**/SKILL.md`

### 真源支撑层
- `docs/ORCHESTRATION.md`
- `docs/SKILL_ARCHITECTURE.md`
- `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`
- `docs/INCIDENT_WORKFLOW.md`
- `docs/DESIGN_SAFETY_REVIEW.md`
- `docs/BRINGUP_PATH.md`
- `docs/DOMAIN_SPECIALIST_CONTRACTS.md`
- `docs/TEMPLATE_GENERATION.md`
- `docs/CONSISTENCY_VALIDATION.md`

### 模板 / 案例 / 回归支撑层
- `docs/templates/**`
- `docs/cases/**`
- `docs/golden-inputs/**`
- `docs/golden-outputs/**`
- `tools/run_generation_regression.py`

## 最小接入步骤
1. 准备仓库内容
2. 确定直接消费对象是 `skills/**/SKILL.md`
3. 优先从 `orchestration` 或三主场景入口开始消费
4. 按 `docs/ORCHESTRATION.md`、`docs/SKILL_ARCHITECTURE.md`、`docs/ORCHESTRATOR_PROMPT_CONTRACT.md` 约束运行
5. 需要验证时使用 `tools/validate_consistency.py` 与 `tools/run_generation_regression.py --check`

## 当前可消费能力
- `orchestration`
- `incident-investigation`
- `bringup-path`
- `design-safety-review`
- `evidence-pack`
- `incident-review`
- `signal-path-tracer`
- `register-state-auditor`
- `state-machine-tracer`
- `timing-watchdog-auditor`
- `failsafe-convergence-reviewer`
- `watchdog-timeout-audit`

## 当前明确不承诺
- 不提供自动安装器
- 不提供自动目录映射脚本
- 不提供一键分发
- 不承诺多 host 接入一致性
- 不承诺当前仓库已是 Claude Code 官方可发布发行包
- `docs/**` 真源不会自动转化为宿主可执行入口，仍以正式 `skills/**/SKILL.md` 为直接消费入口

## 与其他文档的关系
- 平台战略问题回 `docs/PLATFORMS.md`
- skill 入口边界问题回 `docs/SKILL_ARCHITECTURE.md`
- prompt 协议问题回 `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`
```

- [ ] **Step 3: 运行最小文本检查，确认 7 个主段全部落地**

Run: `python -c "from pathlib import Path; text = Path('docs/CLAUDE_CODE_HOST.md').read_text(encoding='utf-8'); required = ['## 目标', '## 宿主定位', '## 目录映射', '## 最小接入步骤', '## 当前可消费能力', '## 当前明确不承诺', '## 与其他文档的关系']; missing = [item for item in required if item not in text]; print('OK' if not missing else missing)"`
Expected: `OK`

- [ ] **Step 4: 运行最小文本检查，确认目录分层与核心回指已存在**

Run: `python -c "from pathlib import Path; text = Path('docs/CLAUDE_CODE_HOST.md').read_text(encoding='utf-8'); required = ['skills/**/SKILL.md', 'docs/PLATFORMS.md', 'docs/SKILL_ARCHITECTURE.md', 'docs/ORCHESTRATOR_PROMPT_CONTRACT.md', 'tools/validate_consistency.py', 'tools/run_generation_regression.py --check']; missing = [item for item in required if item not in text]; print('OK' if not missing else missing)"`
Expected: `OK`

- [ ] **Step 5: 提交 Claude Code host 真源文档**

```bash
git add docs/CLAUDE_CODE_HOST.md
git commit -m "feat: add Claude Code host guide"
```

---

### Task 2: 把平台战略文档切换到新的 Claude Code host 真源分工

**Files:**
- Modify: `docs/PLATFORMS.md`
- Test: `docs/PLATFORMS.md`
- Test: `docs/CLAUDE_CODE_HOST.md`

- [ ] **Step 1: 在 `docs/PLATFORMS.md` 中增加对 `docs/CLAUDE_CODE_HOST.md` 的显式回指**

```md
- Claude Code 的最小接入骨架、目录映射、当前可消费能力与非承诺边界详见 `docs/CLAUDE_CODE_HOST.md`。
```

- [ ] **Step 2: 收紧 Claude Code 在平台文档中的描述，使其保持战略层口径**

```md
将 Claude Code 的表述改成“首个 host 锚点与优先落地对象”，避免在 `docs/PLATFORMS.md` 中继续承担接入步骤与目录映射细节。
```

- [ ] **Step 3: 运行最小文本检查，确认平台文档已回指新真源**

Run: `python -c "from pathlib import Path; text = Path('docs/PLATFORMS.md').read_text(encoding='utf-8'); print('OK' if 'docs/CLAUDE_CODE_HOST.md' in text else 'missing')"`
Expected: `OK`

- [ ] **Step 4: 提交平台文档同步**

```bash
git add docs/PLATFORMS.md
git commit -m "docs: align platforms with Claude Code host guide"
```

---

### Task 3: 把 README 暴露为 Claude Code host 真源入口

**Files:**
- Modify: `README.md`
- Test: `README.md`
- Test: `docs/CLAUDE_CODE_HOST.md`

- [ ] **Step 1: 在 `README.md` 的仓库内容或入口列表中增加 `docs/CLAUDE_CODE_HOST.md`**

```md
- `docs/CLAUDE_CODE_HOST.md`：Claude Code 的最小 host 接入真源，定义目录映射、最小接入步骤、当前可消费能力与不承诺边界
```

- [ ] **Step 2: 运行最小文本检查，确认 README 已暴露 Claude Code host 真源入口**

Run: `python -c "from pathlib import Path; files = ['README.md', 'docs/CLAUDE_CODE_HOST.md']; missing = [file for file in files if 'docs/CLAUDE_CODE_HOST.md' not in Path(file).read_text(encoding='utf-8') and file == 'README.md']; print('OK' if not missing else missing)"`
Expected: `OK`

- [ ] **Step 3: 提交 README 入口同步**

```bash
git add README.md
git commit -m "docs: expose Claude Code host guide"
```

---

### Task 4: 视需要把 consistency validation 与 roadmap 同步到新 host 真源

**Files:**
- Modify: `docs/CONSISTENCY_VALIDATION.md`
- Modify: `docs/ROADMAP.md`
- Test: `docs/CONSISTENCY_VALIDATION.md`
- Test: `docs/ROADMAP.md`

- [ ] **Step 1: 在 `docs/CONSISTENCY_VALIDATION.md` 增加 Claude Code host 文档受控规则（若决定纳入）**

```md
### Claude Code host 接入真源规则

1. `docs/CLAUDE_CODE_HOST.md` 是 Claude Code 的最小 host 接入真源文档。
2. `docs/CLAUDE_CODE_HOST.md` 必须回指：
   - `docs/PLATFORMS.md`
   - `docs/SKILL_ARCHITECTURE.md`
   - `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`
3. `docs/CLAUDE_CODE_HOST.md` 必须明确：
   - 直接消费层
   - 真源支撑层
   - 模板 / 案例 / 回归支撑层
   - 当前可消费能力
   - 当前明确不承诺
```

- [ ] **Step 2: 在 `docs/ROADMAP.md` 增加下一阶段 Claude Code host foundation 记录（若决定落路线图）**

```md
## v8 - Claude Code host 接入骨架

目标：把 Claude Code 从当前优先 host 的文档说明对象推进为第一个有正式接入真源说明的 host。

计划方向：
- [x] `docs/CLAUDE_CODE_HOST.md` 已落地为最小 host 接入真源
- [x] Claude Code 视角下的目录映射已固定为三层
- [x] 当前可消费能力与不承诺边界已被显式固定
```

- [ ] **Step 3: 运行最小文本检查，确认相关文档都命中新真源**

Run: `python -c "from pathlib import Path; files = ['docs/PLATFORMS.md', 'README.md']; optional = ['docs/CONSISTENCY_VALIDATION.md', 'docs/ROADMAP.md']; missing = [file for file in files if 'docs/CLAUDE_CODE_HOST.md' not in Path(file).read_text(encoding='utf-8')]; print('OK' if not missing else missing)"`
Expected: `OK`

- [ ] **Step 4: 提交规则与路线图同步（若本任务实施）**

```bash
git add docs/CONSISTENCY_VALIDATION.md docs/ROADMAP.md
git commit -m "docs: register Claude Code host guide"
```

---

### Task 5: 做端到端验收

**Files:**
- Test: `tools/validate_consistency.py`
- Test: `docs/CLAUDE_CODE_HOST.md`
- Test: `docs/PLATFORMS.md`
- Test: `README.md`

- [ ] **Step 1: 运行 consistency validation 最终验收**

Run: `python tools/validate_consistency.py`
Expected: `Validation result: PASS`

- [ ] **Step 2: 运行 Claude Code host 回指最小检查**

Run: `python -c "from pathlib import Path; text = Path('docs/CLAUDE_CODE_HOST.md').read_text(encoding='utf-8'); required = ['docs/PLATFORMS.md', 'docs/SKILL_ARCHITECTURE.md', 'docs/ORCHESTRATOR_PROMPT_CONTRACT.md', 'skills/**/SKILL.md']; missing = [item for item in required if item not in text]; print('OK' if not missing else missing)"`
Expected: `OK`

- [ ] **Step 3: 运行平台与入口最小检查**

Run: `python -c "from pathlib import Path; files = ['docs/PLATFORMS.md', 'README.md']; missing = [file for file in files if 'docs/CLAUDE_CODE_HOST.md' not in Path(file).read_text(encoding='utf-8')]; print('OK' if not missing else missing)"`
Expected: `OK`

- [ ] **Step 4: 提交 Claude Code host foundation 基线**

```bash
git add docs/CLAUDE_CODE_HOST.md docs/PLATFORMS.md README.md docs/CONSISTENCY_VALIDATION.md docs/ROADMAP.md
git commit -m "feat: add Claude Code host guide"
```

---

## Self-Review

- **Spec coverage:** 本计划覆盖了新建 `docs/CLAUDE_CODE_HOST.md`、同步平台战略文档、暴露 README 入口、视需要登记 consistency validation / roadmap，以及最终 consistency validation 与最小文本验收。
- **Placeholder scan:** 已移除 `TBD`、`TODO`、`implement later`、`appropriate` 等占位措辞；涉及文档改动的步骤都给了明确文本骨架和验证命令。
- **Type consistency:** 统一使用 `docs/CLAUDE_CODE_HOST.md` 作为 host 接入真源路径，统一使用“直接消费层 / 真源支撑层 / 模板-案例-回归支撑层”三层结构，统一以 `skills/**/SKILL.md` 作为 Claude Code 直接消费入口表述。
