# OpenClaw Host Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 un9flow 增加 `docs/OPENCLAW_HOST.md`，把 OpenClaw 从平台预留位推进为角色已定义的外层调度真源。

**Architecture:** 本轮只做 OpenClaw 外层调度真源，不做桥接脚本、协议工程或可执行接入。新增 `docs/OPENCLAW_HOST.md` 后，由它固定 OpenClaw 作为外层调度包裹者的角色边界、可负责动作、不负责动作、与内部总调度与正式 skill 入口的关系；再同步 `docs/PLATFORMS.md`、视需要同步 `README.md` 与 `docs/CONSISTENCY_VALIDATION.md`，让平台战略层与入口层都能回指这份新真源。

**Tech Stack:** Markdown, git, Claude Code

---

## File Structure

### Existing files to modify

- `docs/PLATFORMS.md` — 把 OpenClaw 从平台预留位推进到有正式真源回指的外层调度 host。
- `README.md`（如需要最小入口）— 若要把 `docs/OPENCLAW_HOST.md` 暴露为仓库入口，则补最小入口说明。
- `docs/CONSISTENCY_VALIDATION.md`（如需要最小规则登记）— 若要把 OpenClaw host 真源纳入现有 docs 真源受控对象，则补最小规则约束。
- `docs/ROADMAP.md`（如需要阶段落地记录）— 若要把 OpenClaw host foundation 记为下一阶段落地点，则补最小路线图记录。

### Existing files to read but not modify

- `docs/ORCHESTRATION.md`
- `docs/SKILL_ARCHITECTURE.md`
- `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`
- `docs/INCIDENT_WORKFLOW.md`
- `docs/BRINGUP_PATH.md`
- `docs/DESIGN_SAFETY_REVIEW.md`
- `skills/orchestration/SKILL.md`

### New files to create

- `docs/OPENCLAW_HOST.md` — OpenClaw 外层调度真源文档。
- `docs/superpowers/plans/2026-04-25-un9flow-openclaw-host-foundation.md` — 当前 implementation plan。

### No executable host bridge

本计划不新增 OpenClaw 桥接脚本、安装器、接入清单生成器或 host-to-host runtime。

---

### Task 1: 先创建 OpenClaw 外层调度真源文档

**Files:**
- Create: `docs/OPENCLAW_HOST.md`
- Test: `docs/OPENCLAW_HOST.md`

- [ ] **Step 1: 运行检查，确认当前还没有 `docs/OPENCLAW_HOST.md`**

Run: `git ls-files "docs/OPENCLAW_HOST.md"`
Expected: 无输出

- [ ] **Step 2: 创建 `docs/OPENCLAW_HOST.md` 文档骨架**

```md
# OpenClaw Host

## 目标
- 说明 OpenClaw 作为外层调度器时，在 un9flow 体系中的角色边界，而不是重写场景规则或调度协议。

## 外层调度定位
- OpenClaw 是仓库外层的调度包裹者，而不是仓库内部规则的拥有者。
- OpenClaw 决定“是否进入 un9flow”，但不接管 un9flow 内部三场景主判定权。

## 可负责的动作
- 外部请求承接
- 是否进入 un9flow 的高层决策
- 外部上下文最小归一化
- 将 un9flow 的结果回交给外层宿主链

## 不负责的动作
- 不重写 `docs/ORCHESTRATION.md`
- 不直接发明新场景
- 不篡改 `docs/INCIDENT_WORKFLOW.md`
- 不篡改 `docs/BRINGUP_PATH.md`
- 不篡改 `docs/DESIGN_SAFETY_REVIEW.md`
- 不重写正式 `skills/**/SKILL.md` 的入口含义

## 与仓库内总调度的关系
- OpenClaw 负责外层承接。
- `docs/ORCHESTRATION.md` 负责仓库内部三场景总调度规则。
- 一旦进入 un9flow，内部主路由与 phase / specialist / artifact 主线由仓库真源决定。

## 与场景真源和 skill 的关系
- 默认优先交给 `skills/orchestration/SKILL.md`。
- 只有在证据极明确时，才考虑直接交给主场景入口。
- OpenClaw 只能选择调用，不重写正式 skill 入口的意义。

## 当前明确不承诺
- 当前不代表已完成 OpenClaw 可执行接入
- 不代表已有 OpenClaw 安装器或桥接脚本
- 不代表已定义完整外层 API / schema
- 不代表当前仓库已支持 OpenClaw 直连运行
- 不代表 OpenClaw 已拥有仓库内部规则解释权
```

- [ ] **Step 3: 运行最小文本检查，确认 7 个主段全部落地**

Run: `python -c "from pathlib import Path; text = Path('docs/OPENCLAW_HOST.md').read_text(encoding='utf-8'); required = ['## 目标', '## 外层调度定位', '## 可负责的动作', '## 不负责的动作', '## 与仓库内总调度的关系', '## 与场景真源和 skill 的关系', '## 当前明确不承诺']; missing = [item for item in required if item not in text]; print('OK' if not missing else missing)"`
Expected: `OK`

- [ ] **Step 4: 运行最小文本检查，确认关键关系锚点已存在**

Run: `python -c "from pathlib import Path; text = Path('docs/OPENCLAW_HOST.md').read_text(encoding='utf-8'); required = ['docs/ORCHESTRATION.md', 'docs/INCIDENT_WORKFLOW.md', 'docs/BRINGUP_PATH.md', 'docs/DESIGN_SAFETY_REVIEW.md', 'skills/orchestration/SKILL.md']; missing = [item for item in required if item not in text]; print('OK' if not missing else missing)"`
Expected: `OK`

- [ ] **Step 5: 提交 OpenClaw host 真源文档**

```bash
git add docs/OPENCLAW_HOST.md
git commit -m "feat: add OpenClaw host guide"
```

---

### Task 2: 把平台战略文档切换到新的 OpenClaw host 真源分工

**Files:**
- Modify: `docs/PLATFORMS.md`
- Test: `docs/PLATFORMS.md`
- Test: `docs/OPENCLAW_HOST.md`

- [ ] **Step 1: 在 `docs/PLATFORMS.md` 中增加对 `docs/OPENCLAW_HOST.md` 的显式回指**

```md
- OpenClaw 作为外层调度预留位的角色边界与非承诺范围详见 `docs/OPENCLAW_HOST.md`。
```

- [ ] **Step 2: 收紧 OpenClaw 在平台文档中的描述，使其保持战略层口径**

```md
将 OpenClaw 的表述保持为“外层调度预留位”，避免在 `docs/PLATFORMS.md` 中继续承担角色细节、交接关系或协议字段细节。
```

- [ ] **Step 3: 运行最小文本检查，确认平台文档已回指新真源**

Run: `python -c "from pathlib import Path; text = Path('docs/PLATFORMS.md').read_text(encoding='utf-8'); print('OK' if 'docs/OPENCLAW_HOST.md' in text else 'missing')"`
Expected: `OK`

- [ ] **Step 4: 提交平台文档同步**

```bash
git add docs/PLATFORMS.md
git commit -m "docs: align platforms with OpenClaw host guide"
```

---

### Task 3: 视需要把 README / validation / roadmap 同步到 OpenClaw 真源

**Files:**
- Modify: `README.md`
- Modify: `docs/CONSISTENCY_VALIDATION.md`
- Modify: `docs/ROADMAP.md`
- Test: `README.md`
- Test: `docs/CONSISTENCY_VALIDATION.md`
- Test: `docs/ROADMAP.md`

- [ ] **Step 1: 在 `README.md` 中增加 OpenClaw host 入口（若决定暴露）**

```md
- `docs/OPENCLAW_HOST.md`：OpenClaw 外层调度真源，定义其与 un9flow 内部总调度、场景真源与 skill 的关系边界
```

- [ ] **Step 2: 在 `docs/CONSISTENCY_VALIDATION.md` 增加 OpenClaw host 真源规则（若决定纳入）**

```md
### OpenClaw host 真源规则

1. `docs/OPENCLAW_HOST.md` 是 OpenClaw 外层调度真源文档。
2. `docs/OPENCLAW_HOST.md` 必须回指：
   - `docs/PLATFORMS.md`
   - `docs/ORCHESTRATION.md`
   - `docs/INCIDENT_WORKFLOW.md`
   - `docs/BRINGUP_PATH.md`
   - `docs/DESIGN_SAFETY_REVIEW.md`
   - `skills/orchestration/SKILL.md`
3. `docs/OPENCLAW_HOST.md` 必须明确：
   - 外层调度定位
   - 可负责的动作
   - 不负责的动作
   - 当前明确不承诺
```

- [ ] **Step 3: 在 `docs/ROADMAP.md` 增加 OpenClaw host foundation 记录（若决定落路线图）**

```md
## v16 - OpenClaw 外层调度真源

目标：把 OpenClaw 从平台预留位推进为角色已定义的外层调度真源。

计划方向：
- [x] `docs/OPENCLAW_HOST.md` 已落地为外层调度真源
- [x] OpenClaw 可负责与不负责的动作已被显式固定
- [x] OpenClaw 与仓库内总调度、场景真源与正式 skill 的关系已被固定
```

- [ ] **Step 4: 运行最小文本检查，确认相关文档都命中新真源**

Run: `python -c "from pathlib import Path; files = ['docs/PLATFORMS.md']; optional = ['README.md', 'docs/CONSISTENCY_VALIDATION.md', 'docs/ROADMAP.md']; missing = [file for file in files if 'docs/OPENCLAW_HOST.md' not in Path(file).read_text(encoding='utf-8')]; print('OK' if not missing else missing)"`
Expected: `OK`

- [ ] **Step 5: 提交入口、规则与路线图同步（若本任务实施）**

```bash
git add README.md docs/CONSISTENCY_VALIDATION.md docs/ROADMAP.md
git commit -m "docs: register OpenClaw host guide"
```

---

### Task 4: 做端到端验收

**Files:**
- Test: `docs/OPENCLAW_HOST.md`
- Test: `docs/PLATFORMS.md`
- Test: `tools/validate_consistency.py`

- [ ] **Step 1: 运行 consistency validation 最终验收**

Run: `python tools/validate_consistency.py`
Expected: `Validation result: PASS`

- [ ] **Step 2: 运行 OpenClaw host 文档结构检查**

Run: `python -c "from pathlib import Path; text = Path('docs/OPENCLAW_HOST.md').read_text(encoding='utf-8'); required = ['## 目标', '## 外层调度定位', '## 可负责的动作', '## 不负责的动作', '## 与仓库内总调度的关系', '## 与场景真源和 skill 的关系', '## 当前明确不承诺']; missing = [item for item in required if item not in text]; print('OK' if not missing else missing)"`
Expected: `OK`

- [ ] **Step 3: 运行 OpenClaw 关系锚点检查**

Run: `python -c "from pathlib import Path; text = Path('docs/OPENCLAW_HOST.md').read_text(encoding='utf-8'); required = ['docs/ORCHESTRATION.md', 'docs/INCIDENT_WORKFLOW.md', 'docs/BRINGUP_PATH.md', 'docs/DESIGN_SAFETY_REVIEW.md', 'skills/orchestration/SKILL.md']; missing = [item for item in required if item not in text]; print('OK' if not missing else missing)"`
Expected: `OK`

- [ ] **Step 4: 提交 OpenClaw host foundation 基线**

```bash
git add docs/OPENCLAW_HOST.md docs/PLATFORMS.md README.md docs/CONSISTENCY_VALIDATION.md docs/ROADMAP.md
git commit -m "feat: add OpenClaw host guide"
```

---

## Self-Review

- **Spec coverage:** 本计划覆盖了新建 `docs/OPENCLAW_HOST.md`、同步平台文档、视需要同步 README/CONSISTENCY_VALIDATION/ROADMAP，以及最终 consistency validation 与最小文本验收。
- **Placeholder scan:** 已移除 `TBD`、`TODO`、`implement later`、`appropriate` 等占位措辞；涉及文档改动的步骤都给了明确文本骨架和验证命令。
- **Type consistency:** 统一使用 `docs/OPENCLAW_HOST.md` 作为 OpenClaw 外层调度真源路径，统一使用“可负责动作 / 不负责动作 / 与总调度关系 / 与场景真源和 skill 关系 / 当前明确不承诺”作为角色边界骨架。
