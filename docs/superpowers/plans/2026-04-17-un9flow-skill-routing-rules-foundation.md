# un9flow Skill Routing Rules Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 un9flow 已落地的正式 `SKILL.md` 文件建立统一的入口路由规则文档基线，明确总入口优先级、子入口直进边界与辅助 skill 受控进入条件。

**Architecture:** 这一轮仍以文档实现为主，不新增 skill，不写自动路由脚本。核心做法是把入口路由规则完整落入 `docs/ORCHESTRATION.md`，再同步 `skills/orchestration/SKILL.md` 的路由摘要，并给主场景与辅助 skill 文件补齐“何时允许进入 / 何时不得误进 / 何时必须退回主链”的边界说明。

**Tech Stack:** Markdown, git, Claude Code, un9flow 文档仓库

---

## File Structure

### Existing files to modify

- `docs/ORCHESTRATION.md` — 总入口路由规则的真源，需要补齐混合优先、入口矩阵、辅助 skill 受控进入与禁止规则。
- `skills/orchestration/SKILL.md` — 总入口 skill 摘要文档，需要补齐入口路由摘要与进入条件分流规则。
- `skills/incident-investigation/SKILL.md` — 需要补齐“允许直进 / 不该误进 / 何时回到总入口”的场景边界说明。
- `skills/bringup-path/SKILL.md` — 同上，补齐直进条件与误进禁止。
- `skills/design-safety-review/SKILL.md` — 同上，补齐直进条件与误进禁止。
- `skills/evidence-pack/SKILL.md` — 需要补齐“只可显式进入或主链受控进入”的限制。
- `skills/incident-review/SKILL.md` — 需要补齐“只可显式进入或 review gate 前进入”的限制。

### Existing files already created in this feature work

- `docs/superpowers/specs/2026-04-17-un9flow-skill-routing-rules-design.md` — 当前已确认的 skill 路由规则设计规格。
- `docs/ORCHESTRATION.md` — 当前总调度规则主文档。
- `skills/orchestration/SKILL.md` — 当前总入口正式 skill 文件。
- `skills/incident-investigation/SKILL.md` / `skills/bringup-path/SKILL.md` / `skills/design-safety-review/SKILL.md` — 当前三主场景正式 skill 文件。
- `skills/evidence-pack/SKILL.md` / `skills/incident-review/SKILL.md` — 当前 incident 辅助 skill 文件。

### New files to create

- `docs/superpowers/plans/2026-04-17-un9flow-skill-routing-rules-foundation.md` — 当前 implementation plan。
- `docs/templates/skill-routing-matrix.md` — skill 路由判定矩阵模板，用于记录“直进 / 总入口 / 辅助进入”的案例。

### Optional follow-up files (only if scope expands later)

- `docs/host-routing.md` — 只有当后续开始写 host-specific routing 逻辑时才创建。
- 自动路由脚本 / 生成器 / 校验器 — 本轮明确不做。

当前计划默认**不**创建 optional files；这一轮只写规则文档与 skill 边界。

---

### Task 1: 固化总入口路由规则真源

**Files:**
- Create: `docs/templates/skill-routing-matrix.md`
- Modify: `docs/ORCHESTRATION.md`
- Modify: `skills/orchestration/SKILL.md`
- Test: `docs/ORCHESTRATION.md`, `docs/templates/skill-routing-matrix.md`, `skills/orchestration/SKILL.md`

- [ ] **Step 1: 写出总入口路由缺口清单**

```md
当前缺口：
- 总入口 routing 原则已存在，但还没有明确写成“混合优先”的完整真源
- 缺少直进 / 总入口 / 辅助进入的判定矩阵模板
- `skills/orchestration/SKILL.md` 还没有把这些规则收敛成路由摘要
```

- [ ] **Step 2: 运行检查，确认当前还没有 `docs/templates/skill-routing-matrix.md`**

Run: `ls docs/templates && git ls-files "docs/templates/skill-routing-matrix.md"`
Expected: 目录中不存在 `skill-routing-matrix.md`

- [ ] **Step 3: 在 `docs/ORCHESTRATION.md` 增加“入口路由优先级”小节**

```md
## 入口路由优先级

核心原则：
- 明确场景时直进子入口
- 模糊、交叉或跨场景请求时先走总入口 `orchestration`
- 辅助 skill 不参与全局首路由竞争

优先级顺序：
1. 显式总调度请求 -> `orchestration`
2. 显式主场景且证据一致
3. 模糊 / 交叉 / 跨场景 -> `orchestration`
4. 显式辅助 skill 点名（仅在 incident 语义上下文中成立）
5. 低置信度判断时，宁可走总入口，不误塞子入口
```

- [ ] **Step 4: 在 `docs/ORCHESTRATION.md` 增加“辅助 skill 受控进入规则”小节**

```md
## 辅助 skill 受控进入规则

### evidence-pack
- 只允许：
  1. 用户显式要求先整理证据 / 补证据
  2. incident 主链明确要求先补证据
- 禁止：
  - 参与全局主路由竞争
  - 单独充当 incident 主入口
  - 在没有 incident 语义时被误当成通用证据整理器
  - 直接输出根因结论

### incident-review
- 只允许：
  1. 用户显式要求复核当前 incident 结论
  2. incident 主链已经形成初步结论，准备进入 review gate
- 禁止：
  - 参与全局主路由竞争
  - 充当通用 review / audit skill
  - 替代 design-safety-review
  - 在证据链明显不足时给“通过”结论
```

- [ ] **Step 5: 创建 `docs/templates/skill-routing-matrix.md`**

```md
# skill-routing-matrix

## case id
- 

## user phrasing
- 

## evidence profile
- 

## route decision
- 仅允许：`orchestration` / `incident-investigation` / `bringup-path` / `design-safety-review` / `evidence-pack` / `incident-review`
- 约束：`evidence-pack` / `incident-review` 仅在 incident 语义上下文中允许填写为 route decision

## why this route
- 

## why not others
- 

## route type
- 仅允许：直进子入口 / 先走总入口 / 辅助 skill 受控进入
```

- [ ] **Step 6: 在 `skills/orchestration/SKILL.md` 补“入口路由摘要”**

```md
## 入口路由摘要
- 明确场景时直进子入口
- 模糊、交叉或跨场景请求时先走 `orchestration`
- 辅助 skill 不参与全局首路由竞争
- 具体总规则与矩阵以 `docs/ORCHESTRATION.md` 为准
```

- [ ] **Step 7: 运行一致性检查**

Run: `grep -n "混合优先\|辅助 skill\|入口路由优先级\|skill-routing-matrix" docs/ORCHESTRATION.md skills/orchestration/SKILL.md docs/templates/skill-routing-matrix.md`
Expected: 三文件都能命中新加规则或模板路径

- [ ] **Step 8: Commit**

```bash
git add docs/ORCHESTRATION.md docs/templates/skill-routing-matrix.md skills/orchestration/SKILL.md
git commit -m "docs: define skill routing baseline"
```

---

### Task 2: 给三个主场景 skill 补齐直进边界

**Files:**
- Modify: `skills/incident-investigation/SKILL.md`
- Modify: `skills/bringup-path/SKILL.md`
- Modify: `skills/design-safety-review/SKILL.md`
- Test: 三个主场景 skill 文件

- [ ] **Step 1: 写出三主场景边界缺口清单**

```md
当前缺口：
- 三个主场景文件有场景边界，但还没明确“何时允许直进 / 何时不该误进 / 何时应回总入口”
```

- [ ] **Step 2: 在 `skills/incident-investigation/SKILL.md` 补直进边界段**

```md
## 直进边界
- 允许直进：
  - 系统原本可运行
  - 当前有运行期异常
  - 目标是解释现象、缩小故障半径、定位根因
- 不该误进：
  - 系统尚未建立稳定运行基线
  - 当前其实是设计评审而非 active incident
- 应回总入口：
  - incident / bringup / review 场景交叉且无法直接裁决时
```

- [ ] **Step 3: 在 `skills/bringup-path/SKILL.md` 补直进边界段**

```md
## 直进边界
- 允许直进：
  - 系统 / 板卡 / 链路尚未建立稳定运行基线
  - 当前目标是首次拉通、初始化、建立确定性基线
- 不该误进：
  - 既有系统运行期退化异常
  - 用户其实在做设计审查
- 应回总入口：
  - 无法判断“建立中”还是“退化中”时
```

- [ ] **Step 4: 在 `skills/design-safety-review/SKILL.md` 补直进边界段**

```md
## 直进边界
- 允许直进：
  - 当前无活跃故障排查压力
  - 目标是审查风险边界、收敛路径、timeout / watchdog / failsafe 策略
- 不该误进：
  - 当前存在 active incident 症状链
  - 当前其实处于 bring-up 首次拉通阶段
- 应回总入口：
  - 用户目标与证据特征明显冲突时
```

- [ ] **Step 5: 运行一致性检查**

Run: `grep -n "直进边界\|允许直进\|不该误进\|应回总入口" skills/incident-investigation/SKILL.md skills/bringup-path/SKILL.md skills/design-safety-review/SKILL.md`
Expected: 三个文件都命中四类边界说明

- [ ] **Step 6: Commit**

```bash
git add skills/incident-investigation/SKILL.md skills/bringup-path/SKILL.md skills/design-safety-review/SKILL.md
git commit -m "docs: add direct-entry rules for scenario skills"
```

---

### Task 3: 给 incident 辅助 skill 补齐受控进入规则

**Files:**
- Modify: `skills/evidence-pack/SKILL.md`
- Modify: `skills/incident-review/SKILL.md`
- Test: 两个辅助 skill 文件

- [ ] **Step 1: 写出辅助 skill 入口缺口清单**

```md
当前缺口：
- 两个辅助 skill 已经定义目标，但还没明确“只能显式进入或主链受控进入”
```

- [ ] **Step 2: 在 `skills/evidence-pack/SKILL.md` 补受控进入规则**

```md
## 进入限制
- 只允许：
  1. 用户显式要求先整理证据 / 补证据
  2. incident 主链明确要求先补证据
- 不允许：
  - 参与全局主路由竞争
  - 充当通用证据整理器
  - 直接给根因结论
```

- [ ] **Step 3: 在 `skills/incident-review/SKILL.md` 补受控进入规则**

```md
## 进入限制
- 只允许：
  1. 用户显式要求复核 incident 结论
  2. incident 主链进入 review gate 前触发
- 不允许：
  - 参与全局主路由竞争
  - 充当通用 review / audit skill
  - 替代 design-safety-review
```

- [ ] **Step 4: 运行一致性检查**

Run: `grep -n "进入限制\|只允许\|不允许" skills/evidence-pack/SKILL.md skills/incident-review/SKILL.md`
Expected: 两个文件都命中对应限制段

- [ ] **Step 5: Commit**

```bash
git add skills/evidence-pack/SKILL.md skills/incident-review/SKILL.md
git commit -m "docs: constrain auxiliary skill entry rules"
```

---

### Task 4: 自审、验证与收口

**Files:**
- Modify: `docs/ORCHESTRATION.md` (如需微调)
- Modify: `skills/orchestration/SKILL.md` (如需微调)
- Modify: `skills/incident-investigation/SKILL.md` (如需微调)
- Modify: `skills/bringup-path/SKILL.md` (如需微调)
- Modify: `skills/design-safety-review/SKILL.md` (如需微调)
- Modify: `skills/evidence-pack/SKILL.md` (如需微调)
- Modify: `skills/incident-review/SKILL.md` (如需微调)
- Modify: `docs/templates/skill-routing-matrix.md` (如需微调)
- Test: 上述全部文档

- [ ] **Step 1: 运行 placeholder 扫描**

Run: `grep -R -n "TODO\|TBD\|implement later\|fill in details" docs skills`
Expected: 新文档中不应出现占位词

- [ ] **Step 2: 运行 skill 路由术语一致性检查**

Run: `grep -R -n "orchestration\|incident-investigation\|bringup-path\|design-safety-review\|evidence-pack\|incident-review" docs skills`
Expected: skill 名称在 docs / skills 中拼写一致

- [ ] **Step 3: 运行分层术语一致性检查**

Run: `grep -R -n "Scenario\|Phase\|Domain Specialist\|Artifact\|Orchestrator" docs skills`
Expected: 命名纪律一致，skill 文件不重写总调度协议

- [ ] **Step 4: 运行最小文档集合检查**

Run: `ls skills && ls docs && ls docs/templates && ls docs/superpowers/specs && ls docs/superpowers/plans`
Expected: 正式 skill 文件、routing matrix、新 spec、新 plan 都存在

- [ ] **Step 5: 运行 git diff 范围审核**

Run: `git diff -- docs/ORCHESTRATION.md skills/orchestration/SKILL.md skills/incident-investigation/SKILL.md skills/bringup-path/SKILL.md skills/design-safety-review/SKILL.md skills/evidence-pack/SKILL.md skills/incident-review/SKILL.md docs/templates/skill-routing-matrix.md docs/superpowers/specs/2026-04-17-un9flow-skill-routing-rules-design.md docs/superpowers/plans/2026-04-17-un9flow-skill-routing-rules-foundation.md`
Expected: 改动集中在计划内文档，无无关文件

- [ ] **Step 6: 如发现问题，做最小修正**

```md
允许的修正类型：
- 统一术语拼写
- 删除重复段落
- 修正文档结构性错误
- 把总规则从场景 skill 移回 `docs/ORCHESTRATION.md`
- 调整辅助 skill 的进入限制边界
```

- [ ] **Step 7: 重新运行关键检查确认收口**

Run: `grep -R -n "混合优先\|直进边界\|进入限制\|skill-routing-matrix" docs skills && git diff --stat`
Expected: grep 命中稳定，diff 只显示计划内文档

- [ ] **Step 8: Commit**

```bash
git add docs/ORCHESTRATION.md skills/orchestration/SKILL.md skills/incident-investigation/SKILL.md skills/bringup-path/SKILL.md skills/design-safety-review/SKILL.md skills/evidence-pack/SKILL.md skills/incident-review/SKILL.md docs/templates/skill-routing-matrix.md docs/superpowers/plans/2026-04-17-un9flow-skill-routing-rules-foundation.md
git commit -m "docs: finalize skill routing rule baseline"
```

---

## Self-Review

### Spec coverage

- 规格第 2 节入口路由判定规则：Task 1 覆盖
- 规格第 3 节路由示例矩阵：Task 1 覆盖
- 规格第 4 节辅助 skill 受控进入：Task 3 覆盖
- 规格第 5 节文档落点方式：Task 1、Task 2、Task 3 覆盖
- 规格第 6 节最终落点与实现顺序：Task 1、Task 2、Task 3 覆盖

### Placeholder scan

本计划没有使用 “TBD / TODO / implement later / similar to Task N” 作为执行步骤占位语，所有步骤都包含明确文件、命令或文档内容。

### Type consistency

计划中统一使用以下关键名词：

- 总入口：`orchestration`
- 主场景：`incident-investigation`、`bringup-path`、`design-safety-review`
- incident 辅助：`evidence-pack`、`incident-review`
- 真源总文档：`docs/ORCHESTRATION.md`
- 路由矩阵模板：`docs/templates/skill-routing-matrix.md`

未使用冲突命名。