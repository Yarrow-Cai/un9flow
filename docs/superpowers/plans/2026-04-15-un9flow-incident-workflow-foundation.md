# un9flow Incident Workflow Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 un9flow 从“只有方法论文档”推进到“围绕 incident-investigation 的第一版可实现规格基线”，补齐 incident-first 工作流、skill/agent 契约、命名分层规则与 roadmap 重排。

**Architecture:** 先不实现可执行 skill 或 agent 代码，而是先把文档结构调整为可落地的 incident-first 体系。实现上以文档为主：用一份设计 spec 固化总体版图，用现有 README / WORKFLOW / ROADMAP / PLATFORMS / AGENTS 文档同步反映第一版 incident workflow、scenario/phase/domain/artifact 分层和 gstack-compatible first 的接入策略。

**Tech Stack:** Markdown, git, Claude Code, un9flow 文档仓库

---

## File Structure

### Existing files to modify

- `README.md` — 项目对外总览；需要从“能力域命名”升级为“incident-first 工作流优先”的当前阶段描述。
- `AGENTS.md` — 仓库内协作约束；需要补充 scenario / phase / domain / artifact 分层使用规则，以及 incident-first 文档同步要求。
- `docs/WORKFLOW.md` — 方法论工作流；需要从纯 phase 描述扩展为“phase 作为 orchestrator 骨架”的解释，并补上 incident-investigation 的执行链。
- `docs/ROADMAP.md` — 版本路线图；需要把 v1-v5 从概念型能力域定义，重排为 incident-first 的落地顺序。
- `docs/PLATFORMS.md` — 平台接入方向；需要补充 gstack-compatible first 的含义与第一版 host 优先级。

### Existing files already created in this feature work

- `docs/superpowers/specs/2026-04-15-un9flow-embedded-workflow-brainstorm-design.md` — 已确认的设计规格，是后续所有改动的依据。

### New files to create

- `docs/superpowers/plans/2026-04-15-un9flow-incident-workflow-foundation.md` — 当前 implementation plan。
- `docs/INCIDENT_WORKFLOW.md` — 第一版 incident-investigation 工作流专项文档，承接 design spec 中的 scenario/orchestrator/specialist/artifact 契约，避免把过多实现细节塞进 `docs/WORKFLOW.md`。
- `docs/templates/incident-summary.md` — incident 输入与输出模板。
- `docs/templates/evidence-pack.md` — evidence-pack 模板。
- `docs/templates/incident-diagnosis-pack.md` — orchestrator 汇总输出模板。
- `docs/templates/incident-review-memo.md` — review gate 输出模板。

### Optional follow-up files (only if docs become too dense during implementation)

- `docs/agents/incident-orchestrator.md` — 如果 `docs/INCIDENT_WORKFLOW.md` 过于臃肿，可拆出 orchestrator 契约文档。
- `docs/agents/specialists.md` — 如果 specialist 契约过长，可拆出单独文档。

当前计划默认**不**创建 optional files；只有在文档职责明显失衡时才允许拆分。

---

### Task 1: 建立 incident-first 文档骨架

**Files:**
- Create: `docs/INCIDENT_WORKFLOW.md`
- Create: `docs/templates/incident-summary.md`
- Create: `docs/templates/evidence-pack.md`
- Create: `docs/templates/incident-diagnosis-pack.md`
- Create: `docs/templates/incident-review-memo.md`
- Modify: `README.md`
- Modify: `docs/WORKFLOW.md`
- Test: `README.md`, `docs/WORKFLOW.md`, `docs/INCIDENT_WORKFLOW.md`

- [ ] **Step 1: 写出 README 当前阶段描述的 failing diff 清单**

```md
当前 README 缺口：
- 仍主要描述“规划中的能力域”，没有把 incident-investigation 写成第一条打穿场景
- 没有说明五层结构：scenario -> orchestrator -> phase -> specialist -> artifact
- 没有指向 incident 工作流专项文档
```

- [ ] **Step 2: 运行最小检查，确认 README 里还没有 incident-first 表述**

Run: `grep -n "incident-investigation\|incident workflow\|orchestrator" README.md`
Expected: 无匹配或只有新 spec 链接缺失，证明缺口存在

- [ ] **Step 3: 在 `README.md` 中加入 incident-first 当前阶段说明**

```md
## 当前阶段重点

当前阶段不追求一次性铺开全部 skills，而是优先围绕
`incident-investigation` 打通第一条嵌入式故障排查工作流。

该工作流采用五层结构：

```text
Scenario 入口 -> Orchestrator -> Phase 骨架 -> Domain Specialist -> Artifact / Review 输出
```

这意味着当前版本的核心目标是：

- 先固化 incident-investigation 场景规格
- 先定义 incident-orchestrator 的调度职责
- 先定义第一批 specialist 契约与输出模板
- 再进入正式 skill 化与 host 接入

详见：
- `docs/WORKFLOW.md`
- `docs/INCIDENT_WORKFLOW.md`
- `docs/ROADMAP.md`
```

- [ ] **Step 4: 运行检查，确认 README 已包含 incident-first 文字**

Run: `grep -n "incident-investigation\|五层结构\|incident-orchestrator" README.md`
Expected: 至少 3 处匹配，定位到新增段落

- [ ] **Step 5: 写出 `docs/WORKFLOW.md` 的 failing diff 清单**

```md
当前 WORKFLOW 缺口：
- phase 仍是纯线性方法章节
- 没有说明 phase 是 orchestrator 可调度骨架
- 没有显式写出 incident-investigation 的执行链
```

- [ ] **Step 6: 运行检查，确认 `docs/WORKFLOW.md` 尚未包含 incident 工作流章节**

Run: `grep -n "Incident Intake\|incident-investigation\|orchestrator" docs/WORKFLOW.md`
Expected: 无匹配

- [ ] **Step 7: 在 `docs/WORKFLOW.md` 增加 incident-investigation 工作流节**

```md
## incident-investigation 执行链

对于“已有系统问题排查”，默认采用以下 incident workflow：

```text
Incident Intake -> Hazard Framing -> Path Localization -> Deterministic Audit -> Convergence Check -> Incident Review
```

说明：

- Scenario 入口：`incident-investigation`
- 调度核心：`incident-orchestrator`
- Phase 仍沿用 `hazard-analysis` / `deterministic-foundation` /
  `link-diagnostics` / `failsafe-validation`
- Domain specialist 负责具体证据分析，不由 orchestrator 吞并
- 最终必须产出 reviewable artifacts，而不是只给一段聊天结论
```

- [ ] **Step 8: 运行检查，确认 `docs/WORKFLOW.md` 已包含 incident 工作流链**

Run: `grep -n "Incident Intake\|Incident Review\|incident-orchestrator" docs/WORKFLOW.md`
Expected: 命中新加章节

- [ ] **Step 9: 创建 `docs/INCIDENT_WORKFLOW.md` 初版文档**

```md
# incident-investigation 工作流

## 目标

把嵌入式故障排查固定为一条以风险边界、证据路径和收敛复核为核心的工作流。

## 五层结构

```text
Scenario -> Orchestrator -> Phase -> Specialist -> Artifact / Review
```

## Scenario 入口

- `incident-investigation`
- `evidence-pack`
- `incident-review`

## Orchestrator

- `incident-orchestrator`
- 负责 phase 顺序、specialist 分派、输出汇总、升级与回退决策

## 第一批 specialist

- `signal-path-tracer`
- `register-state-auditor`
- `state-machine-tracer`
- `timing-watchdog-auditor`
- `failsafe-convergence-reviewer`

## incident workflow

```text
Incident Intake -> Hazard Framing -> Path Localization -> Deterministic Audit -> Convergence Check -> Incident Review
```

## 最低标准输出物

- `incident-summary`
- `evidence-inventory`
- `register-bitfield-map`
- `segmented-failure-path`
- `timeout-watchdog-risk-table`
- `incident-diagnosis-pack`
- `incident-review-memo`
- `failsafe-convergence-note`
```

- [ ] **Step 10: 创建 `docs/templates/incident-summary.md`**

```md
# incident-summary

## 现象
- 

## 触发条件
- 

## 影响范围
- 

## 当前风险判断
- 

## 当前是否已进入安全态
- 

## 缺失证据
- 
```

- [ ] **Step 11: 创建 `docs/templates/evidence-pack.md`**

```md
# evidence-pack

## symptoms
- 

## conditions
- 

## observed signals
- 

## register snapshots
- 

## timing clues
- 

## safety status
- 

## evidence gaps
- 
```

- [ ] **Step 12: 创建 `docs/templates/incident-diagnosis-pack.md`**

```md
# incident-diagnosis-pack

## phase plan
- 

## specialist dispatch list
- 

## primary hypothesis
- 

## confidence
- 

## unresolved alternative paths
- 

## next-step decision
- 
```

- [ ] **Step 13: 创建 `docs/templates/incident-review-memo.md`**

```md
# incident-review-memo

## reviewed artifacts
- 

## confidence gaps
- 

## skipped evidence or steps
- 

## safety boundary concerns
- 

## recommended next action
- 
```

- [ ] **Step 14: 运行文档结构检查**

Run: `ls docs && ls docs/templates && grep -n "incident-investigation" README.md docs/WORKFLOW.md docs/INCIDENT_WORKFLOW.md`
Expected: 新文件存在，3 个文档都能搜到 `incident-investigation`

- [ ] **Step 15: Commit**

```bash
git add README.md docs/WORKFLOW.md docs/INCIDENT_WORKFLOW.md docs/templates/incident-summary.md docs/templates/evidence-pack.md docs/templates/incident-diagnosis-pack.md docs/templates/incident-review-memo.md
git commit -m "docs: add incident workflow foundation"
```

---

### Task 2: 固化 skill / agent / artifact 契约与命名分层

**Files:**
- Modify: `docs/INCIDENT_WORKFLOW.md`
- Modify: `AGENTS.md`
- Test: `docs/INCIDENT_WORKFLOW.md`, `AGENTS.md`

- [ ] **Step 1: 写出契约层缺口清单**

```md
当前缺口：
- AGENTS.md 说明了文档与风格要求，但没写 scenario / phase / domain / artifact 分层纪律
- INCIDENT_WORKFLOW 需要补全每个入口与 specialist 的输入 / 输出契约
```

- [ ] **Step 2: 运行检查，确认 `AGENTS.md` 尚未定义四层命名规则**

Run: `grep -n "Scenario\|Domain Specialist\|Artifact" AGENTS.md`
Expected: 无匹配或不成体系

- [ ] **Step 3: 在 `docs/INCIDENT_WORKFLOW.md` 增加 skill / agent 契约节**

```md
## skill / agent 契约

### `incident-investigation`
输入：故障现象、触发条件、影响范围、已知证据、风险认知、安全态状态
输出：`incident-summary`、`evidence-inventory`、`missing-evidence-list`、`initial-risk-note`

### `evidence-pack`
输入：杂乱证据、日志摘要、寄存器快照、波形描述、实验记录
输出：`evidence-pack`、`evidence-gap-note`

### `incident-orchestrator`
输入：`incident-summary`、`evidence-pack`、`initial-risk-note`
输出：`phase-plan`、`specialist-dispatch-list`、`incident-diagnosis-pack`、`next-step-decision`

### `signal-path-tracer`
输出：`segmented-failure-path`、`observability-point-list`、`path-suspicion-ranking`

### `register-state-auditor`
输出：`register-bitfield-map`、`register-anomaly-list`、`config-mismatch-note`

### `state-machine-tracer`
输出：`state-transition-chain`、`stuck-state-list`、`safety-state-gap-note`

### `timing-watchdog-auditor`
输出：`timeout-watchdog-risk-table`、`isr-mainloop-conflict-note`、`timing-instability-hypothesis`

### `failsafe-convergence-reviewer`
输出：`failsafe-convergence-note`、`unsafe-persistence-risk`、`convergence-expectation-check`

### `incident-review`
输出：`incident-review-memo`、`confidence-gap-summary`、`recommended-next-action`
```

- [ ] **Step 4: 在 `docs/INCIDENT_WORKFLOW.md` 增加命名与分层规则节**

```md
## 命名与分层规则

- Scenario：用户任务入口，例如 `incident-investigation`
- Phase：方法论骨架，例如 `hazard-analysis`
- Domain Specialist：证据域与分析动作，例如 `register-state-auditor`
- Artifact：可审计输出物，例如 `register-bitfield-map`

规则：
- 不让 skill 伪装成 phase
- 不让 agent 命名成 artifact
- 不把 scenario 和 domain 混成一层
```

- [ ] **Step 5: 在 `AGENTS.md` 增加文档协作规则**

```md
## incident-first 分层纪律

涉及 un9flow 后续 skill / agent 设计时，统一使用四层命名：

- Scenario：任务入口
- Phase：方法论骨架
- Domain Specialist：证据域分析单元
- Artifact：可审计输出物

编写或修改文档时：
- 不要把 phase 名称当作用户入口名
- 不要让 orchestrator 吞掉 specialist 的专业判断
- 不要只写抽象结论，必须明确输出物
- 涉及 incident-investigation 时，优先同步 `docs/INCIDENT_WORKFLOW.md`
```

- [ ] **Step 6: 运行检查，确认 2 个文件都包含统一术语**

Run: `grep -n "Scenario\|Phase\|Domain Specialist\|Artifact" docs/INCIDENT_WORKFLOW.md AGENTS.md`
Expected: 两个文件都命中四类术语

- [ ] **Step 7: 运行一致性检查**

Run: `grep -n "incident-orchestrator\|signal-path-tracer\|register-state-auditor\|incident-review" docs/INCIDENT_WORKFLOW.md AGENTS.md`
Expected: `docs/INCIDENT_WORKFLOW.md` 命中全部关键名词，`AGENTS.md` 至少命中 incident-first 纪律段

- [ ] **Step 8: Commit**

```bash
git add docs/INCIDENT_WORKFLOW.md AGENTS.md
git commit -m "docs: define incident skill and agent contracts"
```

---

### Task 3: 重排 roadmap 与平台接入叙事

**Files:**
- Modify: `docs/ROADMAP.md`
- Modify: `docs/PLATFORMS.md`
- Modify: `README.md`
- Test: `docs/ROADMAP.md`, `docs/PLATFORMS.md`, `README.md`

- [ ] **Step 1: 写出 roadmap failing diff 清单**

```md
当前 roadmap 缺口：
- v1 仍是抽象能力域定义，没有 incident-first 规格化目标
- v2 没有按 incident pipeline 顺序拆解
- v3 没有解释 gstack-compatible first 的准确边界
```

- [ ] **Step 2: 运行检查，确认 `docs/ROADMAP.md` 还没有 incident-first 表述**

Run: `grep -n "incident-investigation\|incident-first\|gstack-compatible first" docs/ROADMAP.md`
Expected: 无匹配

- [ ] **Step 3: 修改 `docs/ROADMAP.md` 的 v1-v5 内容**

```md
## v1 - incident-first 规格定义

目标：先把第一条可运行工作流的边界钉死。

计划方向：
- [ ] 定义 `incident-investigation` 场景规格
- [ ] 定义 `incident-orchestrator` 职责边界
- [ ] 定义 5 个 specialist 的输入 / 输出契约
- [ ] 定义第一批 artifact 模板
- [ ] 固化 scenario / phase / domain / artifact 命名规则

## v2 - incident pipeline skill 化

目标：把第一条 embedded incident workflow 做成真正可接入的能力链。

计划方向：
- [ ] `incident-investigation`
- [ ] `evidence-pack`
- [ ] `incident-review`
- [ ] `incident-orchestrator` 调度规则
- [ ] 5 个 domain specialist
```

- [ ] **Step 4: 修改 `docs/PLATFORMS.md`，写清 gstack-compatible first 的边界**

```md
## 第一版接入优先级

第一版采用 **gstack-compatible first** 策略。

这里的含义是：
- 优先兼容 workflow orchestration 思路
- 优先兼容 Claude Code / skill 入口习惯
- 优先考虑后续目录组织和 host 接入方式

这里不意味着：
- 复用 gstack 命名
- 复制岗位人格化 specialist
- 直接继承 gstack 安装器

第一版 host 优先级：
1. Claude Code
2. gstack 风格 skill 编排环境
3. OpenClaw 作为外层调度预留
4. 其他 host 在核心 workflow 稳定后推进
```

- [ ] **Step 5: 在 `README.md` 中同步 roadmap 与平台重点**

```md
## 演进顺序

- v1：incident-first 规格定义
- v2：incident pipeline skill 化
- v3：host 接入
- v4：模板生成与一致性校验
- v5：嵌入式专用能力外扩

当前优先级不是多 host 分发，而是先把第一条 incident workflow 讲清、定稳、再技能化。
```

- [ ] **Step 6: 运行检查，确认 3 个文件叙事一致**

Run: `grep -n "incident-first\|gstack-compatible first\|Claude Code" README.md docs/ROADMAP.md docs/PLATFORMS.md`
Expected: 三个文件均有命中，且 `docs/PLATFORMS.md` 明确列出 host 优先级

- [ ] **Step 7: 人工对照 spec 做 coverage check**

```md
核对项：
- spec 第 2 节五层结构 -> README / INCIDENT_WORKFLOW / AGENTS
- spec 第 5 节 incident workflow -> WORKFLOW / INCIDENT_WORKFLOW
- spec 第 7 节命名规则 -> INCIDENT_WORKFLOW / AGENTS
- spec 第 8 节 roadmap 重排 -> ROADMAP / PLATFORMS / README

若发现某节无对应落点，先补文档再继续。
```

- [ ] **Step 8: Commit**

```bash
git add README.md docs/ROADMAP.md docs/PLATFORMS.md
git commit -m "docs: align roadmap with incident-first rollout"
```

---

### Task 4: 自审、验证与收口

**Files:**
- Modify: `README.md` (如需微调)
- Modify: `AGENTS.md` (如需微调)
- Modify: `docs/WORKFLOW.md` (如需微调)
- Modify: `docs/ROADMAP.md` (如需微调)
- Modify: `docs/PLATFORMS.md` (如需微调)
- Modify: `docs/INCIDENT_WORKFLOW.md` (如需微调)
- Test: 全部上述文档

- [ ] **Step 1: 运行 placeholder 扫描**

Run: `grep -R -n "TODO\|TBD\|implement later\|fill in details" README.md AGENTS.md docs`
Expected: 只允许命中已有 roadmap 计划项中的语义性 TODO；不允许命中新写文档里的占位语

- [ ] **Step 2: 运行 incident 术语一致性检查**

Run: `grep -R -n "incident-investigation\|incident-orchestrator\|signal-path-tracer\|register-state-auditor\|state-machine-tracer\|timing-watchdog-auditor\|failsafe-convergence-reviewer\|incident-review" README.md AGENTS.md docs`
Expected: 所有关键名词拼写一致，无变体冲突

- [ ] **Step 3: 运行分层术语一致性检查**

Run: `grep -R -n "Scenario\|Phase\|Domain Specialist\|Artifact" AGENTS.md docs`
Expected: `AGENTS.md` 与 incident 相关文档对四层术语使用一致

- [ ] **Step 4: 运行最小文档集合检查**

Run: `ls docs && ls docs/templates && ls docs/superpowers/specs && ls docs/superpowers/plans`
Expected: `INCIDENT_WORKFLOW.md`、4 个模板、spec、plan 都存在

- [ ] **Step 5: 运行 git diff 审核改动范围**

Run: `git diff -- README.md AGENTS.md docs/WORKFLOW.md docs/ROADMAP.md docs/PLATFORMS.md docs/INCIDENT_WORKFLOW.md docs/templates/incident-summary.md docs/templates/evidence-pack.md docs/templates/incident-diagnosis-pack.md docs/templates/incident-review-memo.md docs/superpowers/specs/2026-04-15-un9flow-embedded-workflow-brainstorm-design.md docs/superpowers/plans/2026-04-15-un9flow-incident-workflow-foundation.md`
Expected: 只包含本计划要求的文档改动，无无关文件

- [ ] **Step 6: 如检查发现术语或职责冲突，做最小修正**

```md
允许的修正类型：
- 统一术语拼写
- 删除重复段落
- 把抽象表述改成约束 / 输出物表述
- 把过载段落迁移到 `docs/INCIDENT_WORKFLOW.md`
```

- [ ] **Step 7: 重新运行关键检查确认修正生效**

Run: `grep -R -n "incident-investigation\|incident-orchestrator\|Scenario\|Artifact" README.md AGENTS.md docs && git diff --stat`
Expected: grep 命中稳定，`git diff --stat` 仅显示目标文档

- [ ] **Step 8: Commit**

```bash
git add README.md AGENTS.md docs/WORKFLOW.md docs/ROADMAP.md docs/PLATFORMS.md docs/INCIDENT_WORKFLOW.md docs/templates/incident-summary.md docs/templates/evidence-pack.md docs/templates/incident-diagnosis-pack.md docs/templates/incident-review-memo.md docs/superpowers/plans/2026-04-15-un9flow-incident-workflow-foundation.md
git commit -m "docs: finalize incident workflow documentation baseline"
```

---

## Self-Review

### Spec coverage

- 规格第 2 节五层结构：Task 1 与 Task 2 覆盖
- 规格第 3 节第一批可运行版图：Task 1 与 Task 2 覆盖
- 规格第 4 节 gstack 映射边界：Task 3 覆盖
- 规格第 5 节 incident workflow：Task 1 覆盖
- 规格第 6 节 skill / agent 契约：Task 2 覆盖
- 规格第 7 节命名与分层：Task 2 覆盖
- 规格第 8 节 roadmap 重排：Task 3 覆盖
- 规格第 9 节范围边界：Task 4 覆盖
- 规格第 10 节总结：通过 Task 1-4 的文档收敛共同落地

### Placeholder scan

本计划没有使用 “TBD / TODO / implement later / similar to Task N” 这类占位语作为执行步骤，所有步骤都包含明确文件、命令或文档内容。

### Type consistency

计划中统一使用以下关键名词：

- Scenario: `incident-investigation`
- Orchestrator: `incident-orchestrator`
- Specialists: `signal-path-tracer`, `register-state-auditor`, `state-machine-tracer`, `timing-watchdog-auditor`, `failsafe-convergence-reviewer`
- Review entry: `incident-review`

未使用冲突命名。
