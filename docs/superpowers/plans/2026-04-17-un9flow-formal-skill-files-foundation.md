# un9flow Formal Skill Files Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 un9flow 落第一批正式 `skills/*/SKILL.md` 文件，形成“总入口 + 三主场景 + incident 辅助”可直接使用的 skill 文档基线。

**Architecture:** 这一轮开始真正落地 skill 文件，但仍不写自动生成脚本、安装器或 host-specific 变体。做法是先创建 `skills/orchestration/`、三个主场景目录和两个 incident 辅助目录，各目录先只放一个 `SKILL.md`；正文保持方法论文档风格，文末再加一小节 Claude Code 宿主附录，使方法边界与宿主约束分层清楚。

**Tech Stack:** Markdown, git, Claude Code, un9flow 文档仓库

---

## File Structure

### Existing files to modify

- `README.md` — 顶层导航与仓库结构需要纳入 `skills/` 目录及第一批正式 skill 文件。
- `docs/SKILL_ARCHITECTURE.md` — 需要把“建议的 skill 版图”收束为已落地的第一批正式 skill 文件集合，并说明当前目录落点。
- `docs/ROADMAP.md` — 需要把“正式 skill 文档”从泛化目标推进为第一批 skill 文件已落地/后续补强的表述。

### Existing files already created in this feature work

- `docs/SKILL_ARCHITECTURE.md` — 已定义总入口、三子入口与辅助 skill 的方法边界。
- `docs/ORCHESTRATOR_PROMPT_CONTRACT.md` — 已定义 orchestrator prompt 的输入/输出协议与控制约束。
- `docs/ORCHESTRATION.md` — 已定义总调度规则。
- `docs/INCIDENT_WORKFLOW.md` — 已定义 incident 场景专属工作流与辅助链。
- `docs/superpowers/specs/2026-04-17-un9flow-formal-skill-files-design.md` — 当前已确认的正式 skill 文件设计规格。

### New files to create

- `docs/superpowers/plans/2026-04-17-un9flow-formal-skill-files-foundation.md` — 当前 implementation plan。
- `skills/orchestration/SKILL.md` — 总入口 skill 正式文件。
- `skills/incident-investigation/SKILL.md` — incident 主场景 skill 正式文件。
- `skills/bringup-path/SKILL.md` — bringup 主场景 skill 正式文件。
- `skills/design-safety-review/SKILL.md` — design-safety-review 主场景 skill 正式文件。
- `skills/evidence-pack/SKILL.md` — incident 辅助 skill：主动找证据 / 补证据。
- `skills/incident-review/SKILL.md` — incident 辅助 skill：证据链复核。

### Optional follow-up files (only if scope expands later)

- `skills/README.md` — 只有在需要专门索引所有 skill 时才创建。
- `skills/<name>/examples.md` — 只有在某个 skill 必须附带大量示例时才创建。
- host-specific skill variants — 本轮明确不做。

当前计划默认**不**创建 optional files；这一轮只落 `SKILL.md` 文件本体。

---

### Task 1: 落总入口 `skills/orchestration/SKILL.md`

**Files:**
- Create: `skills/orchestration/SKILL.md`
- Modify: `README.md`
- Test: `skills/orchestration/SKILL.md`, `README.md`

- [ ] **Step 1: 写出总入口落地缺口清单**

```md
当前缺口：
- skill 架构文档已经定义总入口，但仓库中还没有正式 `skills/orchestration/SKILL.md`
- README 还无法把用户直接带到总入口正式文件
- 总入口的双模式（自动路由 / 显式总调度）尚未以正式 skill 文件表达
```

- [ ] **Step 2: 运行检查，确认当前还没有 `skills/orchestration/SKILL.md`**

Run: `ls skills 2>/dev/null || true && git ls-files "skills/orchestration/SKILL.md"`
Expected: `skills/` 不存在或不存在 `skills/orchestration/SKILL.md`

- [ ] **Step 3: 创建 `skills/orchestration/SKILL.md` 初版文件**

```md
# orchestration

## 目标

作为总入口 skill，接收模糊请求、跨场景请求或显式总调度请求，并把请求接入总调度外壳。

## 进入条件

### 自动路由模式
- 用户请求场景不清
- 输入同时包含多个场景信号
- 需要先做总调度裁决

### 显式总调度模式
- 用户明确要求先走总调度
- 用户希望先拿到路由结果、Phase 骨架和 dispatch plan

## 裁决原则
- 证据特征优先
- 建立中 vs 退化中
- 解释现象 vs 复核方案
- 冲突时选择最可执行场景

## 输出骨架
- `Routing Result`
- `Phase Plan`
- `Dispatch Plan`
- `Control Result`

## 不负责什么
- 不重写场景专属 Artifact 细节
- 不代替场景内调度器
- 不重写 `docs/ORCHESTRATOR_PROMPT_CONTRACT.md` 的协议

## 与子入口的关系
- 总入口在上层
- 三个主场景在下层
- incident 辅助 skill 挂在 incident 场景下

## 参考文档
- `docs/ORCHESTRATION.md`
- `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`
- `docs/SKILL_ARCHITECTURE.md`

## Claude Code 宿主附录
- 在 Claude Code 下可作为总入口 skill 使用
- 用户请求场景不清、跨场景或显式要求总调度时优先进入本 skill
- 入口只负责进入与承接，不临时发明新的路由原则
```

- [ ] **Step 4: 在 `README.md` 中加入总入口 skill 路径**

```md
- `skills/orchestration/SKILL.md`：总入口 skill，承接模糊请求、跨场景请求与显式总调度请求
```

- [ ] **Step 5: 运行结构检查**

Run: `ls skills/orchestration && grep -n "skills/orchestration/SKILL.md\|总入口 skill" README.md skills/orchestration/SKILL.md`
Expected: `skills/orchestration/SKILL.md` 存在，README 与文件正文都能命中新路径

- [ ] **Step 6: Commit**

```bash
git add README.md skills/orchestration/SKILL.md
git commit -m "docs: add orchestration skill file"
```

---

### Task 2: 落三个主场景 `SKILL.md`

**Files:**
- Create: `skills/incident-investigation/SKILL.md`
- Create: `skills/bringup-path/SKILL.md`
- Create: `skills/design-safety-review/SKILL.md`
- Modify: `docs/SKILL_ARCHITECTURE.md`
- Test: `skills/incident-investigation/SKILL.md`, `skills/bringup-path/SKILL.md`, `skills/design-safety-review/SKILL.md`, `docs/SKILL_ARCHITECTURE.md`

- [ ] **Step 1: 写出三主场景落地缺口清单**

```md
当前缺口：
- 三个主场景还只有方法文档和 spec，没有正式 skill 文件
- `SKILL_ARCHITECTURE.md` 还停留在“建议骨架”，需要同步到已落地文件
- 三份文件必须采用统一主骨架 + 场景特化段
```

- [ ] **Step 2: 运行检查，确认三主场景文件尚未存在**

Run: `git ls-files "skills/incident-investigation/SKILL.md" "skills/bringup-path/SKILL.md" "skills/design-safety-review/SKILL.md"`
Expected: 无输出

- [ ] **Step 3: 创建 `skills/incident-investigation/SKILL.md`**

```md
# incident-investigation

## 目标

面向现网或验收阶段的异常闭环，解释现象、缩小故障半径并形成可复核的 incident 证据链。

## 适用边界
- 系统原本可运行，现在出现异常
- 当前目标是解释现象、缩小故障半径、定位根因
- 不用于从零建立基线
- 不替代完整设计评审

## 最小输入要求
- 当前症状
- 触发条件
- 影响范围
- 已知证据
- 当前安全态判断

## 默认 Phase 骨架
- `hazard-analysis`
- `link-diagnostics`
- `deterministic-foundation`
- `failsafe-validation`

## 默认 specialist 偏向
- `signal-path-tracer`
- `register-state-auditor`
- `state-machine-tracer`
- `timing-watchdog-auditor`
- `failsafe-convergence-reviewer`

## 主要 Artifact
- `incident-summary`
- `evidence-inventory`
- `evidence-package`
- `incident-diagnosis-pack`
- `incident-review-memo`

## 证据流转与收敛说明
- `evidence-pack` 负责主动找证据 / 补证据
- `incident-review` 负责证据链复核
- `incident-orchestrator` 只承担 incident 场景内调度

## 不负责什么
- 不负责把系统从零拉通
- 不负责替代 design-safety-review

## 与总入口 / prompt 契约的关系
- 场景边界以本文件为准
- 总调度规则以 `docs/ORCHESTRATION.md` 为准
- prompt 协议以 `docs/ORCHESTRATOR_PROMPT_CONTRACT.md` 为准

## Claude Code 宿主附录
- 当用户明确要排查运行期异常时，可直接进入本 skill
```

- [ ] **Step 4: 创建 `skills/bringup-path/SKILL.md`**

```md
# bringup-path

## 目标

面向新板、新链路、新模块的首次拉通与重复建立过程，先建立确定性基线，再验证链路拉通。

## 适用边界
- 系统尚未建立稳定运行基线
- 当前任务是初始化、上电、首次通信建立、配置序列验证
- 不用于解释现网退化异常

## 最小输入要求
- 当前系统阶段
- 板卡 / 模块信息
- 当前初始化状态
- 已知链路状态
- 当前约束与风险边界

## 默认 Phase 骨架
- `hazard-analysis`
- `deterministic-foundation`
- `link-diagnostics`
- `failsafe-validation`

## 默认 specialist 偏向
- `register-state-auditor`
- `state-machine-tracer`
- `timing-watchdog-auditor`
- `signal-path-tracer`
- `failsafe-convergence-reviewer`

## 主要 Artifact
- bringup 相关基线工件
- 链路拉通记录
- 初始诊断结论

## 建立基线优先说明
- 先建立确定性基线
- 再验证链路拉通
- 再进入异常验证与安全收敛检查

## 不负责什么
- 不把所有运行期异常都当 incident 解释
- 不在未建立基线前给过度诊断结论

## 与总入口 / prompt 契约的关系
- 场景边界以本文件为准
- 总调度规则以 `docs/ORCHESTRATION.md` 为准
- prompt 协议以 `docs/ORCHESTRATOR_PROMPT_CONTRACT.md` 为准

## Claude Code 宿主附录
- 当用户明确要求 bring-up 路径时，可直接进入本 skill
```

- [ ] **Step 5: 创建 `skills/design-safety-review/SKILL.md`**

```md
# design-safety-review

## 目标

面向设计阶段的风险边界、收敛路径、timeout / watchdog / failsafe 策略复核。

## 适用边界
- 当前无活跃故障排查压力
- 当前目标是复核设计、安全边界和收敛策略
- 不替代 active incident 排障

## 最小输入要求
- 设计目标
- 当前方案说明
- 状态机 / timeout / failsafe 约束
- 当前风险边界

## 默认 Phase 骨架
- `hazard-analysis`
- `deterministic-foundation`
- `failsafe-validation`
- `link-diagnostics`（按需补）

## 默认 specialist 偏向
- `state-machine-tracer`
- `timing-watchdog-auditor`
- `failsafe-convergence-reviewer`
- `register-state-auditor`
- `signal-path-tracer`（按需）

## 主要 Artifact
- review 结论
- 风险边界结论
- 收敛策略结论

## 方案复核与边界审查说明
- 审风险边界
- 审状态收敛
- 审 timeout / watchdog / failsafe
- 审设计是否可验证

## 不负责什么
- 不替代活跃故障排查
- 不在缺乏证据时充当 incident 根因定位器

## 与总入口 / prompt 契约的关系
- 场景边界以本文件为准
- 总调度规则以 `docs/ORCHESTRATION.md` 为准
- prompt 协议以 `docs/ORCHESTRATOR_PROMPT_CONTRACT.md` 为准

## Claude Code 宿主附录
- 当用户明确要求审设计、安全边界或收敛策略时，可直接进入本 skill
```

- [ ] **Step 6: 在 `docs/SKILL_ARCHITECTURE.md` 中同步正式文件落点**

```md
补充：
- 第一批正式 skill 文件已落点：
  - `skills/orchestration/SKILL.md`
  - `skills/incident-investigation/SKILL.md`
  - `skills/bringup-path/SKILL.md`
  - `skills/design-safety-review/SKILL.md`
```

- [ ] **Step 7: 运行一致性检查**

Run: `grep -n "skills/orchestration/SKILL.md\|skills/incident-investigation/SKILL.md\|skills/bringup-path/SKILL.md\|skills/design-safety-review/SKILL.md" docs/SKILL_ARCHITECTURE.md skills/*/SKILL.md`
Expected: 四个正式文件存在，且 `docs/SKILL_ARCHITECTURE.md` 已同步路径

- [ ] **Step 8: Commit**

```bash
git add docs/SKILL_ARCHITECTURE.md skills/orchestration/SKILL.md skills/incident-investigation/SKILL.md skills/bringup-path/SKILL.md skills/design-safety-review/SKILL.md
git commit -m "docs: add core scenario skill files"
```

---

### Task 3: 落 incident 辅助 `SKILL.md`

**Files:**
- Create: `skills/evidence-pack/SKILL.md`
- Create: `skills/incident-review/SKILL.md`
- Modify: `docs/INCIDENT_WORKFLOW.md`
- Test: `skills/evidence-pack/SKILL.md`, `skills/incident-review/SKILL.md`, `docs/INCIDENT_WORKFLOW.md`

- [ ] **Step 1: 写出辅助 skill 落地缺口清单**

```md
当前缺口：
- incident 辅助层还只有方法文档，没有正式 skill 文件
- evidence-pack 的“主动找证据 / 补证据”特征需要正式落到 skill 文件
- incident-review 的“证据链复核”边界需要正式落到 skill 文件
```

- [ ] **Step 2: 运行检查，确认辅助 skill 文件尚未存在**

Run: `git ls-files "skills/evidence-pack/SKILL.md" "skills/incident-review/SKILL.md"`
Expected: 无输出

- [ ] **Step 3: 创建 `skills/evidence-pack/SKILL.md`**

```md
# evidence-pack

## 目标

作为 incident 辅助 skill，主动识别证据缺口、推动下一轮取证，并形成可供主场景继续消费的 `evidence-package`。

## 仅适用于哪个场景
- 主要服务 `incident-investigation`
- 不参与全局主路由

## 何时应使用
- 输入混乱
- 当前证据不足以进入 incident 主链
- specialist 输出提示需要先补证据

## 输入要求
- 当前已有症状
- 当前已有日志 / 快照 / 波形 / 寄存器信息
- 当前约束
- 当前风险边界

## 核心动作
- 盘点已有证据
- 标记缺失证据
- 生成优先级排序的取证建议
- 形成 `evidence-package`

## 输出 Artifact
- `evidence-package`
- `evidence-gap-note`
- `evidence-acquisition-plan`

## 何时返回主场景
- 当证据包足以被 `incident-orchestrator` 消费时，返回 `incident-investigation`

## 不负责什么
- 不给根因结论
- 不替代总路由
- 不替代 specialist 深度分析

## Claude Code 宿主附录
- 当用户证据混乱、证据不足或主动要求先补证据时，可直接进入本 skill
```

- [ ] **Step 4: 创建 `skills/incident-review/SKILL.md`**

```md
# incident-review

## 目标

作为 incident 辅助 skill，对当前 incident 结论做 second opinion 与收口前复核。

## 仅适用于哪个场景
- 主要服务 `incident-investigation`
- 不作为总 review skill

## 何时应使用
- 根因已初步形成
- 准备进入 review gate
- 需要 second opinion

## 输入要求
- `incident-diagnosis-pack`
- 各 specialist 输出
- 当前未解释项
- 当前风险判断

## 输出 Artifact
- `incident-review-memo`
- `confidence-gap-summary`
- `recommended-next-action`

## 何时返回主场景
- 若 review 发现缺口，退回 `incident-investigation`
- 若 review 通过，允许进入收口

## 不负责什么
- 不替代总调度
- 不替代 `design-safety-review`
- 不在证据明显不足时硬给批准

## Claude Code 宿主附录
- 当 incident 已形成初步结论、需要证据链复核时，可进入本 skill
```

- [ ] **Step 5: 在 `docs/INCIDENT_WORKFLOW.md` 中同步正式辅助 skill 文件落点**

```md
补充：
- `skills/evidence-pack/SKILL.md`
- `skills/incident-review/SKILL.md`
```

- [ ] **Step 6: 运行一致性检查**

Run: `grep -n "skills/evidence-pack/SKILL.md\|skills/incident-review/SKILL.md\|主动识别证据缺口\|second opinion" docs/INCIDENT_WORKFLOW.md skills/evidence-pack/SKILL.md skills/incident-review/SKILL.md`
Expected: 两个正式文件存在，incident 文档已同步文件落点

- [ ] **Step 7: Commit**

```bash
git add docs/INCIDENT_WORKFLOW.md skills/evidence-pack/SKILL.md skills/incident-review/SKILL.md
git commit -m "docs: add incident support skill files"
```

---

### Task 4: 自审、验证与收口

**Files:**
- Modify: `README.md` (如需微调)
- Modify: `docs/SKILL_ARCHITECTURE.md` (如需微调)
- Modify: `docs/INCIDENT_WORKFLOW.md` (如需微调)
- Modify: `skills/orchestration/SKILL.md` (如需微调)
- Modify: `skills/incident-investigation/SKILL.md` (如需微调)
- Modify: `skills/bringup-path/SKILL.md` (如需微调)
- Modify: `skills/design-safety-review/SKILL.md` (如需微调)
- Modify: `skills/evidence-pack/SKILL.md` (如需微调)
- Modify: `skills/incident-review/SKILL.md` (如需微调)
- Test: 上述全部文档

- [x] **Step 1: 运行 placeholder 扫描**

Run: `grep -R -n "TODO\|TBD\|implement later\|fill in details" README.md docs skills`
Expected: 新文档中不应出现占位词

- [x] **Step 2: 运行 skill 文件术语一致性检查**

Run: `grep -R -n "incident-investigation\|bringup-path\|design-safety-review\|evidence-pack\|incident-review\|orchestration" README.md docs skills`
Expected: skill 名称在 README / docs / skills 目录中拼写一致

- [x] **Step 3: 运行分层术语一致性检查**

Run: `grep -R -n "Scenario\|Phase\|Domain Specialist\|Artifact\|Orchestrator" README.md AGENTS.md docs skills`
Expected: 命名纪律一致，且 skill 文件不重写总调度协议

- [x] **Step 4: 运行最小文档集合检查**

Run: `ls skills && ls skills/orchestration && ls skills/incident-investigation && ls skills/bringup-path && ls skills/design-safety-review && ls skills/evidence-pack && ls skills/incident-review && ls docs && ls docs/templates && ls docs/superpowers/specs && ls docs/superpowers/plans`
Expected: 6 个正式 skill 文件、新 spec、新 plan 都存在

- [x] **Step 5: 运行 git diff 范围审核**

Run: `git diff -- README.md docs/SKILL_ARCHITECTURE.md docs/INCIDENT_WORKFLOW.md skills/orchestration/SKILL.md skills/incident-investigation/SKILL.md skills/bringup-path/SKILL.md skills/design-safety-review/SKILL.md skills/evidence-pack/SKILL.md skills/incident-review/SKILL.md docs/superpowers/specs/2026-04-17-un9flow-formal-skill-files-design.md docs/superpowers/plans/2026-04-17-un9flow-formal-skill-files-foundation.md`
Expected: 改动集中在计划内文档，无无关文件

- [x] **Step 6: 如发现问题，做最小修正**

```md
允许的修正类型：
- 统一术语拼写
- 删除重复段落
- 修正文档结构性错误
- 把总调度规则从 skill 文件移回 docs/ORCHESTRATION.md
- 调整技能正文与 Claude Code 宿主附录边界
```

- [x] **Step 7: 重新运行关键检查确认收口**

Run: `grep -R -n "skills/orchestration/SKILL.md\|skills/incident-investigation/SKILL.md\|skills/evidence-pack/SKILL.md\|Scenario\|incident-investigation" README.md AGENTS.md docs skills && git diff --stat`
Expected: grep 命中稳定，diff 只显示计划内文档

- [ ] **Step 8: Commit**

```bash
git add README.md docs/SKILL_ARCHITECTURE.md docs/INCIDENT_WORKFLOW.md skills/orchestration/SKILL.md skills/incident-investigation/SKILL.md skills/bringup-path/SKILL.md skills/design-safety-review/SKILL.md skills/evidence-pack/SKILL.md skills/incident-review/SKILL.md docs/superpowers/plans/2026-04-17-un9flow-formal-skill-files-foundation.md
git commit -m "docs: finalize formal skill file baseline"
```

---

## Self-Review

### Spec coverage

- 规格第 2 节正式 skill 文件版图：Task 1、Task 2、Task 3 覆盖
- 规格第 3 节总入口骨架：Task 1 覆盖
- 规格第 4 节三主场景骨架：Task 2 覆盖
- 规格第 5 节 incident 辅助 skill：Task 3 覆盖
- 规格第 6 节实现顺序：Task 1、Task 2、Task 3 覆盖

### Placeholder scan

本计划没有使用 “TBD / TODO / implement later / similar to Task N” 作为执行步骤占位语，所有步骤都包含明确文件、命令或文档内容。

### Type consistency

计划中统一使用以下关键名词：

- 总入口 skill：`orchestration`
- 主场景 skill：`incident-investigation`、`bringup-path`、`design-safety-review`
- incident 辅助 skill：`evidence-pack`、`incident-review`
- 文档基线：`docs/SKILL_ARCHITECTURE.md`、`docs/ORCHESTRATOR_PROMPT_CONTRACT.md`

未使用冲突命名。