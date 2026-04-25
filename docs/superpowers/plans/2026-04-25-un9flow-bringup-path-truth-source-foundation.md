# Bringup-Path Truth Source Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 un9flow 增加正式的 `docs/BRINGUP_PATH.md` 场景真源，并把 `isoSPI / AFE bring-up` 钉为该场景下的第一个 canonical 子焦点。

**Architecture:** 本轮以“场景真源先行，专项模板挂靠其下”为主线，新增 `docs/BRINGUP_PATH.md` 作为 bring-up 场景真源，再同步 `docs/ORCHESTRATION.md`、`docs/CONSISTENCY_VALIDATION.md` 与 `skills/bringup-path/SKILL.md` 的角色说明，使总调度、场景真源、specialist 契约、专项模板与 example 各归其位。现有 `docs/templates/daisy-chain-isospi-afe-bringup-template.md` 与 `docs/cases/power-board-bringup-example.md` 保持模板 / example 角色，不反向定义场景。

**Tech Stack:** Markdown, Python 3, git, Claude Code

---

## File Structure

### Existing files to modify

- `docs/ORCHESTRATION.md` — 把 bringup-path 从总调度中的预留场景，升级为有正式场景真源承接的场景入口。
- `docs/CONSISTENCY_VALIDATION.md` — 增加 bringup-path 场景真源规则与回指要求。
- `skills/bringup-path/SKILL.md` — 收紧为对 `docs/BRINGUP_PATH.md` 的 skill 映射，不再单独承担场景真源语义。
- `docs/ROADMAP.md` — 新增下一阶段 bringup-path 真源化基线的落地记录。
- `README.md`（如需要最小入口）— 若要把新场景真源暴露为文档入口，则补最小入口。

### Existing files to read but not modify

- `docs/templates/daisy-chain-isospi-afe-bringup-template.md`
- `docs/cases/power-board-bringup-example.md`
- `docs/INCIDENT_WORKFLOW.md`
- `docs/DESIGN_SAFETY_REVIEW.md`
- `docs/DOMAIN_SPECIALIST_CONTRACTS.md`
- `docs/PLATFORMS.md`

### New files to create

- `docs/BRINGUP_PATH.md` — bringup-path 正式场景真源文档。
- `docs/superpowers/plans/2026-04-25-un9flow-bringup-path-truth-source-foundation.md` — 当前 implementation plan。

### No new scripts/workflows

本计划不新增新的 specialist、生成器、golden regression 或 GitHub workflow。

---

### Task 1: 先把 bringup-path 场景真源文档写出来

**Files:**
- Create: `docs/BRINGUP_PATH.md`
- Test: `docs/BRINGUP_PATH.md`

- [ ] **Step 1: 运行检查，确认当前还没有 `docs/BRINGUP_PATH.md`**

Run: `git ls-files "docs/BRINGUP_PATH.md"`
Expected: 无输出

- [ ] **Step 2: 创建 `docs/BRINGUP_PATH.md` 文档骨架**

```md
# bringup-path

## 目标
- 面向板级 bring-up、链路拉通、初始化连通性确认与受控观测，先建立最小可通信 / 可观测 / 可推进基线，再决定继续 bring-up 还是换轨。

## 进入边界与换轨
- 适用：系统 / 板卡 / 链路尚未建立稳定运行基线。
- 适用：首次拉通、重复建立、初始化失败、最小通信条件未确认。
- 换轨到 `incident-investigation`：问题已经明显转为故障定位、证据归因与故障链解释。
- 换轨到 `design-safety-review`：问题已经明显转为设计边界、保护策略、失效策略与设计安全复核。
- 无法判断场景时回交 `docs/ORCHESTRATION.md` 的总入口路由。

## 默认 Phase 骨架
1. `bringup-entry-check`
2. `link-readiness`
3. `controlled-observation`
4. `stabilization-and-handoff`

## 默认 specialist 装配
### 默认参与
- `signal-path-tracer`
- `register-state-auditor`
- `timing-watchdog-auditor`

### 按需参与
- `state-machine-tracer`
- `failsafe-convergence-reviewer`

## 主 Artifact 与 specialist 输出对齐
- 主收口 Artifact：`bringup-path-summary`
- specialist 的 pack / note 只作为支撑证据，不直接取代场景主收口。

## canonical bring-up 子焦点
- `isoSPI / AFE bring-up` 是 `bringup-path` 下第一个 canonical bring-up 子焦点。
- 对应专项模板：`docs/templates/daisy-chain-isospi-afe-bringup-template.md`
- 对应 example：`docs/cases/power-board-bringup-example.md`

## Review Gate / Completion Gate
- 可以结束本轮：已达到最小连通 / 最小可观测状态。
- 继续下一轮 bring-up：已有部分进展但未达到稳定收口。
- 升级 / 换轨到 `incident-investigation`。
- 升级 / 换轨到 `design-safety-review`。
```

- [ ] **Step 3: 运行最小文本检查，确认 6 个主段全部落地**

Run: `python -c "from pathlib import Path; text = Path('docs/BRINGUP_PATH.md').read_text(encoding='utf-8'); required = ['## 进入边界与换轨', '## 默认 Phase 骨架', '## 默认 specialist 装配', '## 主 Artifact 与 specialist 输出对齐', '## canonical bring-up 子焦点', '## Review Gate / Completion Gate']; missing = [item for item in required if item not in text]; print('OK' if not missing else missing)"`
Expected: `OK`

- [ ] **Step 4: 运行最小文本检查，确认 canonical 子焦点回指已存在**

Run: `python -c "from pathlib import Path; text = Path('docs/BRINGUP_PATH.md').read_text(encoding='utf-8'); required = ['isoSPI / AFE bring-up', 'docs/templates/daisy-chain-isospi-afe-bringup-template.md', 'docs/cases/power-board-bringup-example.md']; missing = [item for item in required if item not in text]; print('OK' if not missing else missing)"`
Expected: `OK`

- [ ] **Step 5: 提交 bringup-path 场景真源文档**

```bash
git add docs/BRINGUP_PATH.md
git commit -m "feat: add bringup-path truth source"
```

---

### Task 2: 把总调度文档切换到新的 bringup-path 真源分工

**Files:**
- Modify: `docs/ORCHESTRATION.md`
- Test: `docs/ORCHESTRATION.md`
- Test: `docs/BRINGUP_PATH.md`

- [ ] **Step 1: 在 `docs/ORCHESTRATION.md` 的适用场景或场景骨架说明中补对 `docs/BRINGUP_PATH.md` 的回指**

```md
- `bringup-path` 的场景内执行骨架、默认 phase backbone、specialist 装配与 completion gate 见 `docs/BRINGUP_PATH.md`。
```

- [ ] **Step 2: 收紧 `bringup-path` 的默认 phase / specialist 描述，使其保持总调度层口径**

```md
将 `bringup-path` 段落改成“总调度层默认偏向”式表述，例如：
- `bringup-path`
  - 场景真源：`docs/BRINGUP_PATH.md`
  - 默认偏向：先建立 deterministic 基线与最小可通信条件，再做受控观测与换轨判断。
```

- [ ] **Step 3: 运行最小文本检查，确认总调度文档已回指新真源**

Run: `python -c "from pathlib import Path; text = Path('docs/ORCHESTRATION.md').read_text(encoding='utf-8'); print('OK' if 'docs/BRINGUP_PATH.md' in text else 'missing')"`
Expected: `OK`

- [ ] **Step 4: 提交总调度文档同步**

```bash
git add docs/ORCHESTRATION.md
git commit -m "docs: align orchestration with bringup truth source"
```

---

### Task 3: 收紧 bringup-path skill 到“映射层”角色

**Files:**
- Modify: `skills/bringup-path/SKILL.md`
- Test: `skills/bringup-path/SKILL.md`
- Test: `docs/BRINGUP_PATH.md`

- [ ] **Step 1: 在 `skills/bringup-path/SKILL.md` 增加对 `docs/BRINGUP_PATH.md` 的显式回指**

```md
- 场景真源：`docs/BRINGUP_PATH.md`
```

- [ ] **Step 2: 把 skill 中与场景真源重复定义的部分改写为映射语气**

```md
将类似“默认 Phase 骨架”“默认 specialist 偏向”“主要 Artifact”改写为：
- 默认执行骨架遵循 `docs/BRINGUP_PATH.md`
- 默认 specialist 装配遵循 `docs/BRINGUP_PATH.md`
- 主收口 Artifact 遵循 `docs/BRINGUP_PATH.md`
```

- [ ] **Step 3: 保留并收紧 isoSPI / AFE bring-up 模板挂接说明**

```md
- 对于 `isoSPI / AFE bring-up`，优先使用 `docs/templates/daisy-chain-isospi-afe-bringup-template.md` 作为 `docs/BRINGUP_PATH.md` 下的专项模板。
```

- [ ] **Step 4: 运行最小文本检查，确认 skill 已回指 bringup-path 真源与专项模板**

Run: `python -c "from pathlib import Path; text = Path('skills/bringup-path/SKILL.md').read_text(encoding='utf-8'); required = ['docs/BRINGUP_PATH.md', 'docs/templates/daisy-chain-isospi-afe-bringup-template.md']; missing = [item for item in required if item not in text]; print('OK' if not missing else missing)"`
Expected: `OK`

- [ ] **Step 5: 提交 skill 映射收紧**

```bash
git add skills/bringup-path/SKILL.md
git commit -m "docs: map bringup skill to truth source"
```

---

### Task 4: 把 consistency validation 与 roadmap 同步到新场景

**Files:**
- Modify: `docs/CONSISTENCY_VALIDATION.md`
- Modify: `docs/ROADMAP.md`
- Modify: `README.md`
- Test: `docs/CONSISTENCY_VALIDATION.md`
- Test: `docs/ROADMAP.md`
- Test: `README.md`

- [ ] **Step 1: 在 `docs/CONSISTENCY_VALIDATION.md` 增加 bringup-path 场景真源规则**

```md
### Bringup-path 场景真源规则

1. `docs/BRINGUP_PATH.md` 是 `bringup-path` 的正式场景真源文档。
2. `docs/BRINGUP_PATH.md` 必须回指：
   - `docs/ORCHESTRATION.md`
   - `docs/DOMAIN_SPECIALIST_CONTRACTS.md`
   - `docs/templates/daisy-chain-isospi-afe-bringup-template.md`
   - `docs/cases/power-board-bringup-example.md`
3. `skills/bringup-path/SKILL.md` 必须回指 `docs/BRINGUP_PATH.md`。
4. `docs/templates/daisy-chain-isospi-afe-bringup-template.md` 与 `docs/cases/power-board-bringup-example.md` 不得反向承担场景真源职责。
```

- [ ] **Step 2: 在 `docs/ROADMAP.md` 增加下一阶段 bringup-path 真源化落地记录**

```md
## v7 - bringup-path 场景真源化

目标：把 bringup-path 从总调度中的预留场景升级为正式场景真源。

计划方向：
- [x] `docs/BRINGUP_PATH.md` 已落地为正式场景真源
- [x] `isoSPI / AFE bring-up` 已固定为首个 canonical 子焦点
- [x] bringup-path skill 已收紧为映射层，不再单独承担场景真源职责
```

- [ ] **Step 3: 在 `README.md` 增加 bringup-path 真源入口（若当前 README 已集中暴露 docs 真源）**

```md
- `docs/BRINGUP_PATH.md`：`bringup-path` 的正式场景真源，定义 bring-up 进入边界、phase backbone、specialist 装配与 completion gate
```

- [ ] **Step 4: 运行最小文本检查，确认 3 个入口文档都命中新真源**

Run: `python -c "from pathlib import Path; files = ['docs/CONSISTENCY_VALIDATION.md', 'docs/ROADMAP.md', 'README.md']; missing = [file for file in files if 'docs/BRINGUP_PATH.md' not in Path(file).read_text(encoding='utf-8')]; print('OK' if not missing else missing)"`
Expected: `OK`

- [ ] **Step 5: 提交规则、路线图与入口同步**

```bash
git add docs/CONSISTENCY_VALIDATION.md docs/ROADMAP.md README.md
git commit -m "docs: register bringup truth source"
```

---

### Task 5: 做端到端验收

**Files:**
- Test: `tools/validate_consistency.py`
- Test: `docs/BRINGUP_PATH.md`
- Test: `docs/ORCHESTRATION.md`
- Test: `skills/bringup-path/SKILL.md`

- [ ] **Step 1: 运行 consistency validation 最终验收**

Run: `python tools/validate_consistency.py`
Expected: `Validation result: PASS`

- [ ] **Step 2: 运行真源回指最小检查**

Run: `python -c "from pathlib import Path; text = Path('docs/BRINGUP_PATH.md').read_text(encoding='utf-8'); required = ['docs/ORCHESTRATION.md', 'docs/DOMAIN_SPECIALIST_CONTRACTS.md', 'docs/templates/daisy-chain-isospi-afe-bringup-template.md', 'docs/cases/power-board-bringup-example.md']; missing = [item for item in required if item not in text]; print('OK' if not missing else missing)"`
Expected: `OK`

- [ ] **Step 3: 运行 skill 映射最小检查**

Run: `python -c "from pathlib import Path; text = Path('skills/bringup-path/SKILL.md').read_text(encoding='utf-8'); required = ['docs/BRINGUP_PATH.md', 'docs/templates/daisy-chain-isospi-afe-bringup-template.md']; missing = [item for item in required if item not in text]; print('OK' if not missing else missing)"`
Expected: `OK`

- [ ] **Step 4: 提交 bringup-path 真源化基线**

```bash
git add docs/BRINGUP_PATH.md docs/ORCHESTRATION.md skills/bringup-path/SKILL.md docs/CONSISTENCY_VALIDATION.md docs/ROADMAP.md README.md
git commit -m "feat: add bringup-path truth source"
```

---

## Self-Review

- **Spec coverage:** 本计划覆盖了新建 `docs/BRINGUP_PATH.md`、同步总调度文档、收紧 bringup-path skill 映射层角色、增加 consistency validation 规则、同步 roadmap/README 入口，以及最终 consistency validation 与文本回指验收。
- **Placeholder scan:** 已移除 `TBD`、`TODO`、`implement later`、`appropriate` 等占位措辞；涉及改文档的步骤都给了明确文本骨架和验证命令。
- **Type consistency:** 统一使用 `docs/BRINGUP_PATH.md` 作为场景真源路径，统一使用 `isoSPI / AFE bring-up` 作为首个 canonical 子焦点，统一使用 `bringup-path-summary` 作为主收口 Artifact 名称。
