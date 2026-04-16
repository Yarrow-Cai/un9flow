# un9flow Orchestrator Routing Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 un9flow 建立三场景并列的 orchestrator 文档基线，把主路由、Phase 装配、specialist 分派、控制信号和 prompt 契约骨架落到可维护文档中。

**Architecture:** 这一轮仍以文档实现为主，不创建可执行 agent 或 skill 代码。核心做法是新增 `docs/ORCHESTRATION.md` 作为总调度文档，再同步调整 `README.md`、`docs/ROADMAP.md`、`docs/PLATFORMS.md`、`docs/INCIDENT_WORKFLOW.md`，让 incident 场景文档与总调度文档分工清楚，并把 orchestrator 规则固定成后续 prompt / SKILL.md 可直接引用的规范结构。

**Tech Stack:** Markdown, git, Claude Code, un9flow 文档仓库

---

## File Structure

### Existing files to modify

- `README.md` — 顶层导航与演进顺序入口，需要把 `docs/ORCHESTRATION.md` 纳入主文档集合，并说明它与 `docs/INCIDENT_WORKFLOW.md` 的分工。
- `docs/INCIDENT_WORKFLOW.md` — 保持 incident 场景专属文档，需要删去已上升为总调度规则的共性内容，改为引用 `docs/ORCHESTRATION.md`。
- `docs/ROADMAP.md` — 需要把 v1/v2/v4 中与 orchestrator 规则直接相关的目标更新为 `ORCHESTRATION.md` 视角。
- `docs/PLATFORMS.md` — 需要补一条说明：host 接入最终应面向 orchestrator 总文档和 scenario 文档分层，而不是只绑定 incident 文档。

### Existing files already created in this feature work

- `docs/superpowers/specs/2026-04-16-un9flow-orchestrator-routing-design.md` — 当前已确认的 orchestrator 设计规格。
- `docs/INCIDENT_WORKFLOW.md` — 现有 incident 场景专属文档，将在本计划中瘦身并改成场景文档。

### New files to create

- `docs/superpowers/plans/2026-04-16-un9flow-orchestrator-routing-foundation.md` — 当前 implementation plan。
- `docs/ORCHESTRATION.md` — orchestrator 总调度文档，承接三场景主路由、Phase 装配、specialist 分派、控制信号与 prompt 契约骨架。
- `docs/templates/orchestrator-routing-matrix.md` — 路由验证矩阵模板，用于后续 case-by-case 校验主路由、换轨与升级。
- `docs/templates/orchestrator-dispatch-plan.md` — specialist 分派计划模板。

### Optional follow-up files (only if docs become too dense during implementation)

- `docs/orchestration/prompt-contract.md` — 若 prompt 契约骨架在 `docs/ORCHESTRATION.md` 中过长，可拆出单独文档。
- `docs/orchestration/control-signals.md` — 若控制信号与换轨规则过长，可拆出单独文档。

当前计划默认**不**创建 optional files；只有当 `docs/ORCHESTRATION.md` 职责明显过载时才允许拆分。

---

### Task 1: 建立总调度文档骨架

**Files:**
- Create: `docs/ORCHESTRATION.md`
- Create: `docs/templates/orchestrator-routing-matrix.md`
- Create: `docs/templates/orchestrator-dispatch-plan.md`
- Modify: `README.md`
- Test: `docs/ORCHESTRATION.md`, `README.md`, `docs/templates/orchestrator-routing-matrix.md`, `docs/templates/orchestrator-dispatch-plan.md`

- [ ] **Step 1: 写出顶层导航缺口清单**

> 当前文档保持任务最小改动，但统一术语中明确：
> - `incident-orchestrator` 是 `incident-investigation` 场景内调度器示例；
> - 三场景共用的是总调度外壳（`docs/ORCHESTRATION.md`）。

```md
当前缺口：
- 仓库还没有总调度文档入口
- README 顶层导航只能看到 incident 场景文档，看不到 orchestrator 总外壳
- 模板目录缺少 routing matrix 和 dispatch plan 两类 orchestrator 模板
```

- [ ] **Step 2: 运行检查，确认当前还没有 `docs/ORCHESTRATION.md`**

Run: `ls docs && grep -n "ORCHESTRATION.md" README.md`
Expected: `docs` 目录下不存在 `ORCHESTRATION.md`，README 中无该路径

- [ ] **Step 3: 创建 `docs/ORCHESTRATION.md` 初版文档**

```md
# un9flow Orchestration

## 目标

把三场景并列的 orchestrator 总调度规则固定为可复用、可审查、可继续写成 prompt 契约的文档基线。

## 适用场景

- `incident-investigation`
- `bringup-path`
- `design-safety-review`

## 总外壳职责

1. 输入归一化
2. 主路由判定
3. Phase 装配
4. specialist 分派
5. 回退 / 升级 / 换轨 / 收敛控制

## 五层执行结构

```text
Scenario -> Orchestrator -> Phase -> Domain Specialist -> Artifact / Review
```

说明：
- `Scenario / Phase / Domain Specialist / Artifact` 是命名纪律
- `Orchestrator` 是执行拓扑中的调度角色

## 主路由判定

- 证据特征优先
- 系统建立中 vs 退化中
- 解释现象 vs 复核方案
- 冲突时优先下一步最可执行场景

## 默认场景骨架

### incident-investigation
- `hazard-analysis -> link-diagnostics -> deterministic-foundation -> failsafe-validation`

### bringup-path
- `hazard-analysis -> deterministic-foundation -> link-diagnostics -> failsafe-validation`

### design-safety-review
- `hazard-analysis -> deterministic-foundation -> failsafe-validation -> link-diagnostics（按需补）`

## 控制信号

- `continue-current-route`
- `fallback-for-more-evidence`
- `fallback-route-assumption-invalid`
- `fallback-specialist-explanation-failed`
- `fallback-reorder-specialists`
- `reroute-to-bringup-path`
- `reroute-to-incident-investigation`
- `upgrade-to-design-safety-review`
- `upgrade-to-incident-investigation`
- `enter-review-gate`

## prompt 契约骨架

### 输入段
1. case input
2. normalized case
3. routing context
4. control context

### 输出段
1. routing result
2. phase plan
3. dispatch plan
4. control result
```

- [ ] **Step 4: 创建 `docs/templates/orchestrator-routing-matrix.md`**

```md
# orchestrator-routing-matrix

## case id
- 

## input summary
- 

## evidence profile
- 

## primary scenario
- 

## secondary candidates
- 

## routing rationale
- 

## expected phase backbone
- 

## expected specialists
- 

## expected control signal
- 
```

- [ ] **Step 5: 创建 `docs/templates/orchestrator-dispatch-plan.md`**

```md
# orchestrator-dispatch-plan

## scenario
- 

## phase plan
- 

## dispatch items
- phase:
  specialist:
  dispatch reason:
  expected artifacts:

## unresolved gaps
- 

## next control signal
- 
```

- [ ] **Step 6: 在 `README.md` 中加入总调度文档入口**

```md
- `docs/ORCHESTRATION.md`：三场景并列的 orchestrator 总调度规则
- `docs/INCIDENT_WORKFLOW.md`：incident 场景专属工作流文档
- `docs/templates/`：incident 与 orchestrator 所需模板
```

- [ ] **Step 7: 更新 `README.md` 仓库结构块**

```text
├── ORCHESTRATION.md
...
│   ├── orchestrator-routing-matrix.md
│   └── orchestrator-dispatch-plan.md
```

- [ ] **Step 8: 运行文档结构检查**

Run: `ls docs && ls docs/templates && grep -n "ORCHESTRATION.md\|orchestrator-routing-matrix\|orchestrator-dispatch-plan" README.md docs/ORCHESTRATION.md`
Expected: 新文档与模板存在，README 与 `docs/ORCHESTRATION.md` 可检出新路径

- [ ] **Step 9: Commit**

```bash
git add README.md docs/ORCHESTRATION.md docs/templates/orchestrator-routing-matrix.md docs/templates/orchestrator-dispatch-plan.md
git commit -m "docs: add orchestration documentation baseline"
```

---

### Task 2: 把 orchestrator 规则从 incident 文档中解耦出来

**Files:**
- Modify: `docs/INCIDENT_WORKFLOW.md`
- Modify: `docs/ORCHESTRATION.md`
- Test: `docs/INCIDENT_WORKFLOW.md`, `docs/ORCHESTRATION.md`

- [ ] **Step 1: 写出职责冲突清单**

```md
当前缺口：
- `docs/INCIDENT_WORKFLOW.md` 同时承载 incident 场景规则和总调度规则
- 三场景主路由、控制信号、prompt 契约骨架应该上升到总调度文档
- incident 文档应保留 incident 专属默认链与证据流转，不继续承载总外壳
```

- [ ] **Step 2: 运行检查，确认 `docs/INCIDENT_WORKFLOW.md` 当前仍包含总调度内容**

Run: `grep -n "bringup-path\|design-safety-review\|prompt 契约\|控制信号" docs/INCIDENT_WORKFLOW.md`
Expected: 命中总调度相关内容，证明需要拆分

- [ ] **Step 3: 在 `docs/ORCHESTRATION.md` 补齐三场景主路由规则**

> 与 `incident-orchestrator` 角色划分一致：仅覆盖 `incident-investigation` 的场景内示例；总路由控制信号与主 routing 规则在总调度文档统一。

> `incident-orchestrator` 只对应 `incident-investigation` 的场景内调度器示例；总路由与总控制信号在总调度文档统一定义。

```md
## 三场景主路由判定

### incident-investigation
- 系统原本可运行，现在出现异常
- 当前问题更像解释现象、缩小故障半径、寻找根因
- 掉线、CRC 错误、偶发复位、状态卡死、watchdog 异常、采样异常、寄存器异常、failsafe 未收敛

### bringup-path
- 系统 / 板卡 / 链路尚未建立稳定运行基线
- 当前目标是首次拉通、初始化、上电、建立确定性运行基线
- 新板、新链路、新模块、初始化失败、首次通信建立失败、配置序列未验证

### design-safety-review
- 当前没有活跃故障排查压力
- 当前目标是审查设计、验证安全边界和收敛路径
- review、audit、safety、failsafe、limp-home、timeout strategy、watchdog strategy、state machine safety
```

- [ ] **Step 4: 在 `docs/ORCHESTRATION.md` 补齐 Phase 装配与 specialist 默认分派**

> Phase / specialist 定位延续为总调度外壳的场景级规则；`incident-orchestrator` 仍为 incident 场景内分派模板示例。

```md
## Phase 装配与 specialist 默认分派

### incident-investigation
- `hazard-analysis -> link-diagnostics -> deterministic-foundation -> failsafe-validation`
- 默认 specialist：`signal-path-tracer`、`register-state-auditor`、`state-machine-tracer`、`timing-watchdog-auditor`、`failsafe-convergence-reviewer`

### bringup-path
- `hazard-analysis -> deterministic-foundation -> link-diagnostics -> failsafe-validation`
- 默认 specialist：`register-state-auditor`、`state-machine-tracer`、`timing-watchdog-auditor`、`signal-path-tracer`、`failsafe-convergence-reviewer`

### design-safety-review
- `hazard-analysis -> deterministic-foundation -> failsafe-validation -> link-diagnostics（按需补）`
- 默认 specialist：`state-machine-tracer`、`timing-watchdog-auditor`、`failsafe-convergence-reviewer`、`register-state-auditor`、`signal-path-tracer`（按需）
```

- [ ] **Step 5: 在 `docs/ORCHESTRATION.md` 补齐回退 / 升级 / 换轨 / 收敛规则**

> 控制信号统一为 10 个：
> - `continue-current-route`
> - `fallback-for-more-evidence`
> - `fallback-route-assumption-invalid`
> - `fallback-specialist-explanation-failed`
> - `fallback-reorder-specialists`
> - `reroute-to-bringup-path`
> - `reroute-to-incident-investigation`
> - `upgrade-to-design-safety-review`
> - `upgrade-to-incident-investigation`
> - `enter-review-gate`

```md
## 控制规则

### 回退
- 证据不足回退
- 路由假设失效回退
- specialist 解释失败回退

### 升级
- `incident-investigation -> design-safety-review`
- `bringup-path -> design-safety-review`
- `design-safety-review -> incident-investigation`

### 换轨
- 目标未变，但主路由判定需要纠正

### 收敛
- 当前主假设能解释主要 observed symptoms
- 未解释项已显式标记
- Artifact 足以支撑 review / 复测 / 复盘
```

- [ ] **Step 6: 在 `docs/INCIDENT_WORKFLOW.md` 缩回 incident 专属内容**

> 保留 incident 场景内视图，避免将 `incident-orchestrator` 当作全局总编排唯一名称；必要处强调其为场景内调度器示例。

```md
在文档中补一句：
- 与三场景共用的 orchestrator 总调度规则，统一见 `docs/ORCHESTRATION.md`

保留：
- incident 专属证据流转
- incident 默认 Phase 骨架
- incident 默认 specialist
- incident Artifact

删除或改写：
- 不再在 incident 文档中单独承载 bringup-path / design-safety-review 的共性总规则
```

- [ ] **Step 7: 运行边界检查**

Run: `grep -n "bringup-path\|design-safety-review\|prompt 契约\|控制信号" docs/INCIDENT_WORKFLOW.md docs/ORCHESTRATION.md`
Expected: 这些内容主要集中在 `docs/ORCHESTRATION.md`，`docs/INCIDENT_WORKFLOW.md` 只保留必要引用

- [ ] **Step 8: Commit**

```bash
git add docs/ORCHESTRATION.md docs/INCIDENT_WORKFLOW.md
git commit -m "docs: separate orchestration from incident workflow"
```

---

### Task 3: 同步 roadmap 与平台接入叙事到 orchestrator 视角

**Files:**
- Modify: `docs/ROADMAP.md`
- Modify: `docs/PLATFORMS.md`
- Modify: `README.md`
- Test: `docs/ROADMAP.md`, `docs/PLATFORMS.md`, `README.md`

- [ ] **Step 1: 写出叙事偏差清单**

```md
当前缺口：
- roadmap 仍偏 incident-first 主线，没有显式写出 orchestrator 总文档落点
- platforms 只写 host 接入优先级，未写 orchestrator / scenario 双文档分层
- README 缺少对 ORCHESTRATION.md 的角色说明
```

- [ ] **Step 2: 运行检查，确认三文件尚未完整体现 orchestrator 文档落点**

Run: `grep -n "ORCHESTRATION.md\|orchestrator 总调度\|路由验证矩阵" README.md docs/ROADMAP.md docs/PLATFORMS.md`
Expected: 命中不足或为空，证明需要补充

- [ ] **Step 3: 修改 `docs/ROADMAP.md`**

```md
## v1 - incident-first 规格定义
- 增补：落地 `docs/ORCHESTRATION.md` 作为总调度文档

## v2 - incident pipeline skill 化
- 增补：以 orchestrator 规则文档为上层，scenario 文档为下层

## v4 - 生成与校验体系
- 增补：路由验证矩阵模板与 orchestrator dispatch plan 模板
```

- [ ] **Step 4: 修改 `docs/PLATFORMS.md`**

```md
补一句：
- host 接入最终应同时面向总调度文档（`docs/ORCHESTRATION.md`）与场景文档（如 `docs/INCIDENT_WORKFLOW.md`），而不是只绑定单一 scenario 文档
```

- [ ] **Step 5: 修改 `README.md`**

```md
补一句：
- `docs/ORCHESTRATION.md` 负责总调度规则，`docs/INCIDENT_WORKFLOW.md` 负责 incident 场景专属闭环
```

- [ ] **Step 6: 运行一致性检查**

Run: `grep -n "ORCHESTRATION.md\|incident workflow\|orchestrator 总调度\|路由验证矩阵" README.md docs/ROADMAP.md docs/PLATFORMS.md`
Expected: 三个文件都能检出 orchestrator 文档落点或等价说明

- [ ] **Step 7: Commit**

```bash
git add README.md docs/ROADMAP.md docs/PLATFORMS.md
git commit -m "docs: align roadmap with orchestration layer"
```

---

### Task 4: 自审、验证与收口

**Files:**
- Modify: `README.md` (如需微调)
- Modify: `docs/INCIDENT_WORKFLOW.md` (如需微调)
- Modify: `docs/ORCHESTRATION.md` (如需微调)
- Modify: `docs/ROADMAP.md` (如需微调)
- Modify: `docs/PLATFORMS.md` (如需微调)
- Modify: `docs/templates/orchestrator-routing-matrix.md` (如需微调)
- Modify: `docs/templates/orchestrator-dispatch-plan.md` (如需微调)
- Test: 上述全部文档

- [ ] **Step 1: 运行 placeholder 扫描**

Run: `grep -R -n "TODO\|TBD\|implement later\|fill in details" README.md docs/INCIDENT_WORKFLOW.md docs/ORCHESTRATION.md docs/ROADMAP.md docs/PLATFORMS.md docs/templates`
Expected: 新文档中不应出现占位词

- [ ] **Step 2: 运行 orchestrator 术语一致性检查**

Run: `grep -R -n "incident-investigation\|bringup-path\|design-safety-review\|incident-orchestrator\|signal-path-tracer\|register-state-auditor\|state-machine-tracer\|timing-watchdog-auditor\|failsafe-convergence-reviewer" README.md docs`
Expected: 三场景与 specialist 名称拼写一致

- [ ] **Step 3: 运行分层术语一致性检查**

Run: `grep -R -n "Scenario\|Phase\|Domain Specialist\|Artifact\|Orchestrator" README.md AGENTS.md docs`
Expected: 命名纪律一致，且能区分五层执行结构与四层命名纪律

- [ ] **Step 4: 运行最小文档集合检查**

Run: `ls docs && ls docs/templates && ls docs/superpowers/specs && ls docs/superpowers/plans`
Expected: `ORCHESTRATION.md`、2 个新模板、新 spec、新 plan 都存在

- [ ] **Step 5: 运行 git diff 范围审核**

Run: `git diff -- README.md docs/INCIDENT_WORKFLOW.md docs/ORCHESTRATION.md docs/ROADMAP.md docs/PLATFORMS.md docs/templates/orchestrator-routing-matrix.md docs/templates/orchestrator-dispatch-plan.md docs/superpowers/specs/2026-04-16-un9flow-orchestrator-routing-design.md docs/superpowers/plans/2026-04-16-un9flow-orchestrator-routing-foundation.md`
Expected: 改动集中在计划内文档，无无关文件

- [ ] **Step 6: 如发现问题，做最小修正**

```md
允许的修正类型：
- 统一术语拼写
- 删除重复段落
- 把总调度规则从场景文档移回总文档
- 修正文档结构性错误
- 调整模板标题与模板路径不一致问题
```

- [ ] **Step 7: 重新运行关键检查确认收口**

Run: `grep -R -n "ORCHESTRATION.md\|Scenario\|Domain Specialist\|incident-orchestrator" README.md AGENTS.md docs && git diff --stat`
Expected: grep 命中稳定，diff 只显示计划内文档

- [ ] **Step 8: Commit**

```bash
git add README.md docs/INCIDENT_WORKFLOW.md docs/ORCHESTRATION.md docs/ROADMAP.md docs/PLATFORMS.md docs/templates/orchestrator-routing-matrix.md docs/templates/orchestrator-dispatch-plan.md docs/superpowers/plans/2026-04-16-un9flow-orchestrator-routing-foundation.md
git commit -m "docs: finalize orchestration documentation baseline"
```

---

## Self-Review

### Spec coverage

- 规格第 2 节 orchestrator 总外壳：Task 1 与 Task 2 覆盖
- 规格第 3 节三场景主路由：Task 2 覆盖
- 规格第 4 节 Phase 装配与 specialist 分派：Task 2 覆盖
- 规格第 5 节回退 / 升级 / 换轨：Task 2 覆盖
- 规格第 6 节伪代码骨架：Task 2 覆盖
- 规格第 7 节 prompt 契约骨架与文档落点：Task 1、Task 2、Task 3 覆盖
- 规格第 8 节最终结论：通过 Task 1-4 的文档收敛共同落地

### Placeholder scan

本计划没有使用 “TBD / TODO / implement later / similar to Task N” 作为执行步骤占位语，所有步骤都包含明确文件、命令或文档内容。

### Type consistency

计划中统一使用以下关键名词：

- Scenarios: `incident-investigation`, `bringup-path`, `design-safety-review`
- Orchestrator: `incident-orchestrator`（仅为 incident 场景内调度器示例；总层为总调度外壳）
- Domain Specialists: `signal-path-tracer`, `register-state-auditor`, `state-machine-tracer`, `timing-watchdog-auditor`, `failsafe-convergence-reviewer`
- Artifacts: `incident-summary`, `evidence-package`, `incident-diagnosis-pack`, `incident-review-memo`

未使用冲突命名。