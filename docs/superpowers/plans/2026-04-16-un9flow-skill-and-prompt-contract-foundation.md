# un9flow Skill And Prompt Contract Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 un9flow 建立“总入口 skill + 三子入口 skill + 辅助 skill”的方法文档基线，并同步定义 orchestrator prompt 契约文档基线。

**Architecture:** 这一轮仍以文档实现为主，不创建可执行 skill 代码。核心做法是新增 `docs/SKILL_ARCHITECTURE.md` 与 `docs/ORCHESTRATOR_PROMPT_CONTRACT.md` 两类方法文档，然后同步调整 `README.md`、`docs/ROADMAP.md`、`docs/ORCHESTRATION.md`，让 skill 入口规范与调度协议边界分层清楚，并为后续 `skills/*/SKILL.md` 落地提供统一骨架。

**Tech Stack:** Markdown, git, Claude Code, un9flow 文档仓库

---

## File Structure

### Existing files to modify

- `README.md` — 顶层导航与演进顺序入口，需要把 `docs/SKILL_ARCHITECTURE.md`、`docs/ORCHESTRATOR_PROMPT_CONTRACT.md` 纳入主文档集合，并说明它们与 `docs/ORCHESTRATION.md` 的关系。
- `docs/ORCHESTRATION.md` — 总调度文档，需要收紧到“总调度规则”，避免吞掉未来 prompt 契约文档职责。
- `docs/ROADMAP.md` — 需要把“正式 skill 文档”从泛化目标推进到 skill 架构文档与 prompt 契约文档基线。

### Existing files already created in this feature work

- `docs/superpowers/specs/2026-04-16-un9flow-skill-and-prompt-contract-design.md` — 当前已确认的设计规格。
- `docs/ORCHESTRATION.md` — 现有总调度文档，将在本计划中与 prompt 契约文档做职责切分。
- `docs/INCIDENT_WORKFLOW.md` — 现有 incident 场景文档，后续正式 skill 设计将把它作为场景参考而不是直接改造成 SKILL.md。

### New files to create

- `docs/superpowers/plans/2026-04-16-un9flow-skill-and-prompt-contract-foundation.md` — 当前 implementation plan。
- `docs/SKILL_ARCHITECTURE.md` — 解释总入口、三子入口、辅助 skill 的结构关系与文档骨架。
- `docs/ORCHESTRATOR_PROMPT_CONTRACT.md` — 定义 orchestrator prompt 的输入协议、输出协议、控制信号、硬约束与扩展点。
- `docs/templates/skill-boundary-checklist.md` — skill 文档编写时的边界检查模板。
- `docs/templates/prompt-contract-checklist.md` — prompt 契约编写与审查模板。

### Optional follow-up files (only if docs become too dense during implementation)

- `skills/orchestration/SKILL.md` — 只有在本轮范围升级为直接落正式 skill 文件时才创建。
- `skills/incident-investigation/SKILL.md`
- `skills/bringup-path/SKILL.md`
- `skills/design-safety-review/SKILL.md`
- `skills/evidence-pack/SKILL.md`
- `skills/incident-review/SKILL.md`

当前计划默认**不**创建 optional files；这一轮先把方法与协议讲清，再进入真正的 `SKILL.md` 实现。

---

### Task 1: 建立 skill 架构文档骨架

**Files:**
- Create: `docs/SKILL_ARCHITECTURE.md`
- Create: `docs/templates/skill-boundary-checklist.md`
- Modify: `README.md`
- Test: `docs/SKILL_ARCHITECTURE.md`, `docs/templates/skill-boundary-checklist.md`, `README.md`

- [ ] **Step 1: 写出 skill 架构入口缺口清单**

```md
当前缺口：
- 仓库已有 ORCHESTRATION 总调度文档，但没有 skill 层入口版图文档
- README 无法直接说明“总入口 + 三子入口 + 辅助 skill”的关系
- 没有专门用于检查 skill 边界是否写对的模板
```

- [ ] **Step 2: 运行检查，确认当前还没有 `docs/SKILL_ARCHITECTURE.md`**

Run: `ls docs && grep -n "SKILL_ARCHITECTURE.md" README.md`
Expected: `docs` 目录下不存在 `SKILL_ARCHITECTURE.md`，README 中无该路径

- [ ] **Step 3: 创建 `docs/SKILL_ARCHITECTURE.md` 初版文档**

```md
# un9flow Skill Architecture

## 目标

把“总入口 skill + 三子入口 skill + 辅助 skill”的方法边界固定为可复用、可审查、可继续落成正式 `SKILL.md` 的文档基线。

## skill 版图

### 总入口
- skill 层的 orchestrator 入口
- 负责跨场景裁决、统一进入总调度

### 三个子入口
- `incident-investigation`
- `bringup-path`
- `design-safety-review`

### 辅助 skill
- `evidence-pack`
- `incident-review`

## 总入口职责
1. 接收不明确或跨场景请求
2. 判断是否进入显式场景或交给总调度
3. 调用 orchestrator prompt 契约
4. 输出统一路由结果与下一步动作建议

## 子入口职责
1. 声明场景边界
2. 规范最小输入要求
3. 组织场景内初始 Artifact
4. 约束场景内默认 Phase / specialist / Artifact

## 辅助 skill 职责
- 不参与总路由竞争
- 只在特定场景内被显式调用或由主入口引导调用

## 文档骨架建议

### 总入口 `SKILL.md`
- 目标
- 适用情况
- 裁决原则
- 输出骨架
- 不负责什么
- 与子入口的关系

### 子入口 `SKILL.md`
- 目标
- 适用边界
- 最小输入要求
- 默认 Phase 骨架
- 默认 specialist 偏向
- 主要 Artifact
- 与总入口 / prompt 契约的关系

### 辅助 skill `SKILL.md`
- 目标
- 仅适用于哪个场景
- 输入要求
- 输出 Artifact
- 何时返回主场景 skill
- 不参与全局路由
```

- [ ] **Step 4: 创建 `docs/templates/skill-boundary-checklist.md`**

```md
# skill-boundary-checklist

## skill name
- 

## skill type
- 仅允许：总入口 / 场景入口 / 辅助 skill

## goal
- 

## in-scope
- 

## out-of-scope
- 

## minimum inputs
- 

## main artifacts
- 

## relation to orchestrator
- 

## relation to other skills
- 
```

- [ ] **Step 5: 在 `README.md` 中加入 skill 架构文档入口**

```md
- `docs/SKILL_ARCHITECTURE.md`：总入口、三子入口与辅助 skill 的结构关系
```

- [ ] **Step 6: 运行结构检查**

Run: `ls docs && ls docs/templates && grep -n "SKILL_ARCHITECTURE.md\|skill-boundary-checklist" README.md docs/SKILL_ARCHITECTURE.md`
Expected: 新文档与模板存在，README 与 `docs/SKILL_ARCHITECTURE.md` 能检出新路径

- [ ] **Step 7: Commit**

```bash
git add README.md docs/SKILL_ARCHITECTURE.md docs/templates/skill-boundary-checklist.md
git commit -m "docs: add skill architecture baseline"
```

---

### Task 2: 建立 orchestrator prompt 契约文档骨架

**Files:**
- Create: `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`
- Create: `docs/templates/prompt-contract-checklist.md`
- Modify: `docs/ORCHESTRATION.md`
- Test: `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`, `docs/templates/prompt-contract-checklist.md`, `docs/ORCHESTRATION.md`

- [ ] **Step 1: 写出 prompt 契约缺口清单**

```md
当前缺口：
- ORCHESTRATION 文档承担了总调度规则，但还没有独立协议文档来承载 prompt 输入/输出协议
- 没有专门用于检查 prompt 契约是否越权或字段漂移的模板
```

- [ ] **Step 2: 运行检查，确认当前还没有 `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`**

Run: `ls docs && grep -n "ORCHESTRATOR_PROMPT_CONTRACT.md" README.md docs/ORCHESTRATION.md`
Expected: `docs` 目录下不存在该文件

- [ ] **Step 3: 创建 `docs/ORCHESTRATOR_PROMPT_CONTRACT.md` 初版文档**

```md
# un9flow Orchestrator Prompt Contract

## 目标

把 orchestrator / scenario prompt 的统一协议层固定下来，使 prompt 不重写 skill 边界，也不越权重写总调度规则。

## 输入协议

### Case Input
- 用户目标
- 原始症状
- 当前约束
- 当前给定证据

### Normalized Case
- `stated_goal`
- `observed_symptoms`
- `evidence_inventory`
- `current_risk_state`
- `system_stage`
- `missing_evidence`

### Routing Context
- 已候选 scenario
- 当前主路由
- 当前已有 phase
- 当前已有 specialist 输出
- 当前是否已有 review 结果

### Control Context
- 是否允许继续
- 是否必须补证据
- 是否已触发换轨
- 是否已触发升级
- 是否已满足 review gate 条件

## 输出协议

### Routing Result
- `primary_scenario`
- `secondary_candidates`
- `routing_rationale`

### Phase Plan
- phase 顺序
- 被跳过的 phase
- 被补充的 phase
- 排序原因

### Dispatch Plan
- specialist 列表
- dispatch reason
- expected artifacts

### Control Result
- `control_signal`
- `next_actions`
- `unresolved_gaps`

## 硬约束
1. 不允许跳过 risk framing
2. 不允许把用户措辞直接当主路由
3. 不允许把 `Scenario / Phase / Domain Specialist / Artifact` 混成一层
4. 不允许证据不足时给高置信根因
5. 不允许跳过 review gate 直接收口
6. 不允许让场景内调度器越权承担总路由裁决

## 场景扩展点
- 场景子 prompt 可以细化 Artifact
- 场景子 prompt 可以补强 specialist 偏向
- 场景子 prompt 不可重写总路由规则
- 场景子 prompt 不可改写总控制信号协议
```

- [ ] **Step 4: 创建 `docs/templates/prompt-contract-checklist.md`**

```md
# prompt-contract-checklist

## prompt name
- 

## prompt scope
- 仅允许：总调度 / 场景子 prompt

## input protocol
- 

## output protocol
- 

## control signals used
- 

## hard constraints inherited
- 

## fields allowed to extend
- 

## fields forbidden to override
- 
```

- [ ] **Step 5: 在 `docs/ORCHESTRATION.md` 中收紧职责说明**

```md
补一句：
- `docs/ORCHESTRATOR_PROMPT_CONTRACT.md` 负责 prompt 的输入/输出协议与硬约束；`docs/ORCHESTRATION.md` 保持总调度规则主文档。
```

- [ ] **Step 6: 运行结构检查**

Run: `ls docs && ls docs/templates && grep -n "ORCHESTRATOR_PROMPT_CONTRACT.md\|prompt-contract-checklist" docs/ORCHESTRATION.md docs/ORCHESTRATOR_PROMPT_CONTRACT.md`
Expected: 新文档与模板存在，ORCHESTRATION 可检出 prompt 契约文档入口

- [ ] **Step 7: Commit**

```bash
git add docs/ORCHESTRATION.md docs/ORCHESTRATOR_PROMPT_CONTRACT.md docs/templates/prompt-contract-checklist.md
git commit -m "docs: add orchestrator prompt contract baseline"
```

---

### Task 3: 同步 README 与 roadmap 到 skill/prompt 双轨视角

**Files:**
- Modify: `README.md`
- Modify: `docs/ROADMAP.md`
- Test: `README.md`, `docs/ROADMAP.md`

- [ ] **Step 1: 写出双轨叙事缺口清单**

```md
当前缺口：
- README 还没有明确 skill 架构文档与 prompt 契约文档的分工
- ROADMAP 中“正式 skill 文档”仍偏泛化，尚未拆成 skill 架构与 prompt 契约两条基线
```

- [ ] **Step 2: 运行检查，确认 `README.md` / `docs/ROADMAP.md` 尚未完整体现双轨文档落点**

Run: `grep -n "SKILL_ARCHITECTURE.md\|ORCHESTRATOR_PROMPT_CONTRACT.md\|正式 skill 文档" README.md docs/ROADMAP.md`
Expected: 命中不足或为空

- [ ] **Step 3: 修改 `README.md`**

```md
补充：
- `docs/SKILL_ARCHITECTURE.md` 负责入口规范
- `docs/ORCHESTRATOR_PROMPT_CONTRACT.md` 负责调度协议
- `docs/ORCHESTRATION.md` 负责总调度规则
```

- [ ] **Step 4: 修改 `docs/ROADMAP.md`**

```md
在合适位置增补：
- 正式 skill 文档前，先落 skill 架构文档与 prompt 契约文档基线
- 总入口 / 三子入口 / 辅助 skill 的方法边界先于正式 `SKILL.md`
- orchestrator prompt 协议先于 host 绑定 prompt 文件
```

- [ ] **Step 5: 运行一致性检查**

Run: `grep -n "SKILL_ARCHITECTURE.md\|ORCHESTRATOR_PROMPT_CONTRACT.md\|入口规范\|调度协议" README.md docs/ROADMAP.md`
Expected: 两个文件都能检出双轨分工说明

- [ ] **Step 6: Commit**

```bash
git add README.md docs/ROADMAP.md
git commit -m "docs: align roadmap with skill and prompt layers"
```

---

### Task 4: 自审、验证与收口

**Files:**
- Modify: `README.md` (如需微调)
- Modify: `docs/ORCHESTRATION.md` (如需微调)
- Modify: `docs/ROADMAP.md` (如需微调)
- Modify: `docs/SKILL_ARCHITECTURE.md` (如需微调)
- Modify: `docs/ORCHESTRATOR_PROMPT_CONTRACT.md` (如需微调)
- Modify: `docs/templates/skill-boundary-checklist.md` (如需微调)
- Modify: `docs/templates/prompt-contract-checklist.md` (如需微调)
- Test: 上述全部文档

- [ ] **Step 1: 运行 placeholder 扫描**

Run: `grep -R -n "TODO\|TBD\|implement later\|fill in details" README.md docs/ORCHESTRATION.md docs/ROADMAP.md docs/SKILL_ARCHITECTURE.md docs/ORCHESTRATOR_PROMPT_CONTRACT.md docs/templates`
Expected: 新文档中不应出现占位词

- [ ] **Step 2: 运行 skill / prompt 术语一致性检查**

Run: `grep -R -n "incident-investigation\|bringup-path\|design-safety-review\|evidence-pack\|incident-review\|SKILL_ARCHITECTURE\|ORCHESTRATOR_PROMPT_CONTRACT" README.md docs`
Expected: skill 名称与新文档路径拼写一致

- [ ] **Step 3: 运行分层术语一致性检查**

Run: `grep -R -n "Scenario\|Phase\|Domain Specialist\|Artifact\|Orchestrator" README.md AGENTS.md docs`
Expected: 命名纪律一致，且 skill 架构文档不重写调度协议

- [ ] **Step 4: 运行最小文档集合检查**

Run: `ls docs && ls docs/templates && ls docs/superpowers/specs && ls docs/superpowers/plans`
Expected: `SKILL_ARCHITECTURE.md`、`ORCHESTRATOR_PROMPT_CONTRACT.md`、2 个新模板、新 spec、新 plan 都存在

- [ ] **Step 5: 运行 git diff 范围审核**

Run: `git diff -- README.md docs/ORCHESTRATION.md docs/ROADMAP.md docs/SKILL_ARCHITECTURE.md docs/ORCHESTRATOR_PROMPT_CONTRACT.md docs/templates/skill-boundary-checklist.md docs/templates/prompt-contract-checklist.md docs/superpowers/specs/2026-04-16-un9flow-skill-and-prompt-contract-design.md docs/superpowers/plans/2026-04-16-un9flow-skill-and-prompt-contract-foundation.md`
Expected: 改动集中在计划内文档，无无关文件

- [ ] **Step 6: 如发现问题，做最小修正**

```md
允许的修正类型：
- 统一术语拼写
- 删除重复段落
- 修正文档结构性错误
- 把入口规范和调度协议混写的内容拆回对应文档
- 调整模板标题与用途不一致问题
```

- [ ] **Step 7: 重新运行关键检查确认收口**

Run: `grep -R -n "SKILL_ARCHITECTURE.md\|ORCHESTRATOR_PROMPT_CONTRACT.md\|Scenario\|incident-investigation" README.md AGENTS.md docs && git diff --stat`
Expected: grep 命中稳定，diff 只显示计划内文档

- [ ] **Step 8: Commit**

```bash
git add README.md docs/ORCHESTRATION.md docs/ROADMAP.md docs/SKILL_ARCHITECTURE.md docs/ORCHESTRATOR_PROMPT_CONTRACT.md docs/templates/skill-boundary-checklist.md docs/templates/prompt-contract-checklist.md docs/superpowers/plans/2026-04-16-un9flow-skill-and-prompt-contract-foundation.md
git commit -m "docs: finalize skill and prompt contract baseline"
```

---

## Self-Review

### Spec coverage

- 规格第 2 节 skill 版图结构：Task 1 覆盖
- 规格第 3 节总入口与子入口职责切分：Task 1 覆盖
- 规格第 4 节正式 `SKILL.md` 骨架：Task 1 覆盖
- 规格第 5 节 orchestrator prompt 契约骨架：Task 2 覆盖
- 规格第 6 节 skill 与 prompt 的配合关系：Task 1、Task 2、Task 3 覆盖
- 规格第 7 节最终落点：Task 1、Task 2、Task 3 覆盖

### Placeholder scan

本计划没有使用 “TBD / TODO / implement later / similar to Task N” 作为执行步骤占位语，所有步骤都包含明确文件、命令或文档内容。

### Type consistency

计划中统一使用以下关键名词：

- 总入口 skill：`orchestration`
- 子入口 skill：`incident-investigation`、`bringup-path`、`design-safety-review`
- 辅助 skill：`evidence-pack`、`incident-review`
- 方法文档：`docs/SKILL_ARCHITECTURE.md`
- 协议文档：`docs/ORCHESTRATOR_PROMPT_CONTRACT.md`

未使用冲突命名。