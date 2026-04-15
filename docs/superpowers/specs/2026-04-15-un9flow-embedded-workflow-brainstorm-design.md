# un9flow × gstack × 嵌入式工作流头脑风暴设计稿

日期：2026-04-15
主题：围绕 un9flow 的嵌入式开发工作流，结合 gstack，补充规划中的 skill / agent 版图与演进路径

## 1. 设计结论摘要

本次设计采用如下总体方向：

- 采用 **Orchestrator + Specialists** 架构，而不是纯 skill-only 或纯 review-centric 结构
- 将 **gstack** 作为编排思想参考，而不是命名体系或话术模板来源
- 采用 **上层 phase 调度 + 下层 domain specialist + scenario 入口** 的分层方式
- 第一条优先打穿的端到端场景是 **incident-investigation（故障排查）**
- 第一版由 **agent 主导** 内部拆解、phase 推进与 specialist 分派，skill 主要承担入口、交互与结构化输出包装

一句话总结：

> un9flow 的第一阶段，不是全面 skill 化，而是先围绕 incident-investigation 打通一条由 scenario 入口、orchestrator 调度、phase 骨架、domain specialist 和 artifact 输出组成的嵌入式故障排查工作流。

---

## 2. 五层版图结构

建议将 un9flow 的未来能力版图固定为五层：

```text
Scenario 入口
  -> Orchestrator
    -> Phase 骨架
      -> Domain Specialist
        -> Artifact / Review 输出
```

### 2.1 Scenario 入口层

这一层面向用户任务意图，而不是方法论名词。

建议第一批场景入口：

- `incident-investigation`
- `bringup-path`
- `design-safety-review`
- `pre-release-validation`

其中第一版只要求真正打穿 `incident-investigation`。

### 2.2 Orchestrator 层

建议顶层保留总调度思路，但第一阶段具体化为：

- `incident-orchestrator`

职责：

1. 识别当前案例的主问题类型
2. 决定 phase 推进顺序
3. 分派 specialist
4. 合并输出物
5. 管理置信度、回退与升级决策

限制：

- 不直接吞掉 specialist 的专业判断
- 不绕过 review gate 直接输出高置信根因结论

### 2.3 Phase 骨架层

这一层保持 un9flow 已有主干不改名：

- `hazard-analysis`
- `deterministic-foundation`
- `link-diagnostics`
- `failsafe-validation`

但 phase 不再只是文档章节，而是 orchestrator 可调度的骨架节点。

不同 scenario 可以使用不同推进顺序。例如：

- 新功能 / 新板卡 bring-up：
  `hazard -> deterministic -> link -> failsafe`
- 已有系统问题排查：
  `hazard -> link -> failsafe -> deterministic`

这与现有 `docs/WORKFLOW.md` 保持一致，但从“方法建议”提升为“编排结构”。

### 2.4 Domain Specialist 层

这一层按证据域和分析动作拆，不按岗位人格拆。

建议第一批围绕 incident-investigation 规划以下 specialist：

- `signal-path-tracer`
- `register-state-auditor`
- `state-machine-tracer`
- `timing-watchdog-auditor`
- `failsafe-convergence-reviewer`

扩展阶段再考虑：

- `hazard-reviewer`
- `fault-injection-planner`
- `power-stage-safety-reviewer`
- `isolation-link-diagnostics`
- `keil-linker-layout-auditor`

### 2.5 Artifact / Review 输出层

输出层必须是显式工件层，而不是“顺手附带一段分析文字”。

建议第一批最低标准输出物：

- `incident-summary`
- `evidence-inventory`
- `register-bitfield-map`
- `segmented-failure-path`
- `timeout-watchdog-risk-table`
- `incident-diagnosis-pack`
- `incident-review-memo`
- `failsafe-convergence-note`

核心要求：输出物可检查、可复盘、可二次 review。

---

## 3. 第一批可运行版图

第一批不追求完整覆盖 un9flow 全部未来能力，而是围绕故障排查场景构建最小闭环。

### 3.1 顶层 orchestrator

- `incident-orchestrator`

### 3.2 第一批 scenario skill

- `incident-investigation`
- `evidence-pack`
- `incident-review`

### 3.3 第一批 domain specialist

#### `signal-path-tracer`
负责采样链路、通信链路、控制链路、板级输入到状态变化传播路径的分段定位。

输出：

- `segmented-failure-path`
- `observability-point-list`
- `path-suspicion-ranking`

#### `register-state-auditor`
负责关键寄存器配置、位域含义、默认值与运行态差异分析。

输出：

- `register-bitfield-map`
- `register-anomaly-list`
- `config-mismatch-note`

#### `state-machine-tracer`
负责状态迁移错误、卡死分支、无超时退出路径与默认安全态缺口分析。

输出：

- `state-transition-chain`
- `stuck-state-list`
- `safety-state-gap-note`

#### `timing-watchdog-auditor`
负责节拍、timeout、watchdog、ISR / 主循环职责边界分析。

输出：

- `timeout-watchdog-risk-table`
- `isr-mainloop-conflict-note`
- `timing-instability-hypothesis`

#### `failsafe-convergence-reviewer`
负责异常后收敛路径、降级策略、safe-off / limp-home / degrade 行为复核。

输出：

- `failsafe-convergence-note`
- `unsafe-persistence-risk`
- `convergence-expectation-check`

### 3.4 第一批最小闭环

```text
incident-investigation
  -> incident-orchestrator
    -> 1..N specialists
      -> incident-diagnosis-pack
        -> incident-review
```

目标不是“功能很多”，而是“已经是一条真实可闭环的 incident workflow”。

---

## 4. 借鉴 gstack 的方式

### 4.1 借用内容

un9flow 建议借用 gstack 的三类能力：

1. **工作流分层**：从单个 skill 转向有接力关系的流程网络
2. **specialist 编排机制**：由 orchestrator 管理路由、节奏与回退
3. **输出物驱动闭环**：每一步沉淀可复查工件，而不是只留下聊天记录

### 4.2 不借用内容

un9flow 不建议继承以下内容：

- gstack 的产品化话术和创业叙事
- 通用软件工程用语替代嵌入式硬边界语言
- 强岗位人格化 specialist 设计
- 偏 Web / SaaS 的默认流程世界观

### 4.3 约束性结论

可用一句话定义 gstack 在 un9flow 中的位置：

> gstack 提供 workflow orchestration 的方法启发，un9flow 保留 embedded-first 的语义、证据模型和输出工件。

更短的口号是：

> 借编排，不借人格；借闭环，不借话术。

---

## 5. 第一版 incident-investigation 工作流

建议将第一版 `incident-investigation` 固化为如下可解释工作流：

```text
Incident Intake
  -> Hazard Framing
    -> Path Localization
      -> Deterministic Audit
        -> Convergence Check
          -> Incident Review
```

### 5.1 Incident Intake

入口 skill：`incident-investigation`

目标：

- 将用户描述从聊天语言整理为工程语言
- 形成 incident case
- 建立初始风险判断与证据清单

输出：

- `incident-summary`
- `evidence-inventory`
- `missing-evidence-list`
- `initial-risk-note`

若输入混乱，则先进入 `evidence-pack`。

### 5.2 Hazard Framing

即使是问题排查，也必须先判断：

- 最坏后果是什么
- 当前是否 unsafe but running
- 现在优先止损还是继续定位
- 哪些实验边界禁止突破

这一阶段可调用：

- `failsafe-convergence-reviewer`
- `timing-watchdog-auditor`

输出：

- `hazard-framing-note`
- `no-go-conditions`
- `safe-to-investigate-decision`

### 5.3 Path Localization

优先通过 `signal-path-tracer` 缩小故障半径。

目标：

- 判断故障卡在哪一段路径
- 列出最值得验证的观测点
- 对怀疑区段排序

输出：

- `segmented-failure-path`
- `observability-point-list`
- `path-suspicion-ranking`

### 5.4 Deterministic Audit

按故障表现选择 specialist：

- 配置异常倾向 -> `register-state-auditor`
- 状态迁移异常倾向 -> `state-machine-tracer`
- 超时 / 复位 / 饥饿倾向 -> `timing-watchdog-auditor`

目标：

- 找出确定性结构中的缺口
- 确认状态、寄存器、时序是否与设计一致

输出：

- `deterministic-gap-list`
- `register-anomaly-map`
- `state-transition-fault-chain`
- `timeout-watchdog-risk-table`

### 5.5 Convergence Check

候选根因出现后，必须回头复核：

- 是否真正解释了 observed symptoms
- 是否解释了为什么系统没有按预期安全收敛
- 修复后是否存在收敛预期
- 是否还有未解释的替代故障路径

这一阶段可调用：

- `failsafe-convergence-reviewer`
- 必要时回调 `signal-path-tracer` / `state-machine-tracer`

输出：

- `root-cause-confidence`
- `unresolved-alternative-paths`
- `convergence-expectation`

### 5.6 Incident Review Gate

通过 `incident-review` 做 second opinion。

目标：

- 检查是否漏证据、跳步骤、过早收敛
- 检查建议是否突破安全边界
- 判断是否需要升级为 safety review / design review

输出：

- `incident-review-memo`
- `confidence-gap-summary`
- `recommended-next-action`

---

## 6. 第一版 skill / agent 输入输出契约

### 6.1 `incident-investigation` skill

**输入**

- 故障现象
- 触发条件
- 影响范围
- 已知日志 / 寄存器 / 波形 / 状态描述
- 当前风险等级认知
- 当前是否已进入安全态

**职责**

- 形成 incident case
- 判断是否可直接启动分析
- 不直接承担深度根因分析

**输出**

- `incident-summary`
- `evidence-inventory`
- `missing-evidence-list`
- `initial-risk-note`

### 6.2 `evidence-pack` skill

**输入**

- 杂乱描述
- 截图 / 日志摘要 / 寄存器列表 / 链路现象 / 实验记录

**职责**

- 整理证据来源、时间点、可信度与缺口
- 生成可供 specialist 消费的证据包

**输出**

- `evidence-pack`
- `evidence-gap-note`

### 6.3 `incident-orchestrator` agent

**输入**

- `incident-summary`
- `evidence-pack`
- `initial-risk-note`

**职责**

- 选择 phase 顺序
- 选择 specialist
- 合并输出与管理置信度
- 控制回退、补证据、升级与 review gate

**输出**

- `phase-plan`
- `specialist-dispatch-list`
- `incident-diagnosis-pack`
- `next-step-decision`

### 6.4 `signal-path-tracer` agent

**输入**

- 症状描述
- 通信 / 采样 / 控制路径信息
- 波形观测点或链路状态证据

**输出**

- `segmented-failure-path`
- `observability-point-list`
- `path-suspicion-ranking`

### 6.5 `register-state-auditor` agent

**输入**

- 寄存器快照
- 关键配置项
- 默认值 / 目标值 / 异常现象

**输出**

- `register-bitfield-map`
- `register-anomaly-list`
- `config-mismatch-note`

### 6.6 `state-machine-tracer` agent

**输入**

- 状态定义
- 转移条件
- 当前症状对应的状态表现
- 超时 / 退出条件

**输出**

- `state-transition-chain`
- `stuck-state-list`
- `safety-state-gap-note`

### 6.7 `timing-watchdog-auditor` agent

**输入**

- 节拍信息
- ISR / main loop 责任划分
- timeout / watchdog 行为
- 复位 / 卡顿 / 偶发失效证据

**输出**

- `timeout-watchdog-risk-table`
- `isr-mainloop-conflict-note`
- `timing-instability-hypothesis`

### 6.8 `failsafe-convergence-reviewer` agent

**输入**

- 当前故障链假设
- 当前安全态信息
- 降级 / 停机 / limp-home 行为

**输出**

- `failsafe-convergence-note`
- `unsafe-persistence-risk`
- `convergence-expectation-check`

### 6.9 `incident-review` skill / review agent

对外入口建议保持为 `incident-review` skill，内部由 review agent 执行 second opinion。

**输入**

- `incident-diagnosis-pack`
- 各 specialist 输出物
- 当前置信度和未解释项

**职责**

- second opinion
- 检查漏证据、跳步、过早结论和越界建议

**输出**

- `incident-review-memo`
- `confidence-gap-summary`
- `recommended-next-action`

### 6.10 统一契约规则

所有 specialist 建议统一遵守以下规则：

1. 只对自己的证据域负责
2. 输出必须结构化
3. 必须说明置信度与未解释项
4. 结论必须能回链到证据

---

## 7. 命名与分层规则

建议补充一套明确命名规则，避免后续层级混乱。

### 7.1 Scenario
面向用户任务入口。

示例：

- `incident-investigation`
- `design-safety-review`

### 7.2 Phase
面向方法论骨架。

示例：

- `hazard-analysis`
- `deterministic-foundation`

### 7.3 Domain Specialist
面向证据域和分析动作。

示例：

- `register-state-auditor`
- `state-machine-tracer`

### 7.4 Artifact
面向可审计输出物。

示例：

- `register-bitfield-map`
- `incident-diagnosis-pack`

这四层必须严格区分，避免出现：

- skill 像 phase
- agent 像 artifact
- scenario 与 domain 混层

---

## 8. 对现有 roadmap 的重排建议

### 8.1 v1 - incident-first 规格定义

将当前“能力域定义”收敛为：

- 定义 `incident-investigation` 场景规格
- 定义 `incident-orchestrator` 职责边界
- 定义 5 个 specialist 的输入 / 输出契约
- 定义第一批 artifact 模板
- 固化 scenario / phase / domain / artifact 命名规则

### 8.2 v2 - incident pipeline skill 化

按如下顺序推进：

1. `incident-investigation`
2. `evidence-pack`
3. `incident-review`
4. `incident-orchestrator` 的调度规则
5. 5 个 domain specialist

目标是跑通第一条 embedded incident workflow，而不是堆很多 SKILL.md。

### 8.3 v3 - host 接入

策略：

- 优先按 gstack-compatible first 方式组织
- 优先服务 Claude Code / gstack 风格 host
- OpenClaw 先预留为外层调度，不抢第一版焦点
- 在核心 workflow 稳定前，不急于抽象 multi-host 通用层

这里的 gstack-compatible first，指优先兼容其 workflow orchestration 思路、Claude Code / skill 入口习惯与后续目录组织方式，不等于复用 gstack 命名、人格化 specialist 或直接继承安装器。

### 8.4 v4 - 生成与校验体系

在语义稳定后再做：

- specialist 输出模板生成
- incident case 文档模板
- 命名一致性检查
- phase / scenario / domain 引用校验
- 示例任务回归测试

### 8.5 v5 - 嵌入式专用能力外扩

在 incident pipeline 跑稳后，逐步扩展到：

- `hazard-reviewer`
- `fault-injection-planner`
- `bringup-orchestrator`
- `watchdog-timeout-strategy-review`
- `Keil Scatter / Linker auditor`
- `isoSPI / AFE link specialist`

这类扩展应从 incident 工作流自然生长，而不是另起炉灶。

---

## 9. 范围边界

为了保证第一版稳定，本设计明确不追求：

- 一键全自动根因定位
- 多 specialist 无约束并发分析
- 第一版就覆盖 bring-up / safety / release 全场景
- 没有证据链支撑的高置信结论
- 先做平台分发，再补核心工作流

第一版的成功标准是：

- 场景入口明确
- orchestrator 边界明确
- specialist 契约明确
- 输出物结构明确
- review gate 明确
- 能形成真实的 incident workflow 闭环

---

## 10. 最终结论

本次 brainstorm 产出的推荐方向是：

> 以 incident-investigation 为第一条打穿场景，建立“scenario 入口 -> orchestrator -> phase 骨架 -> domain specialist -> artifact / review 输出”的五层 embedded workflow 体系；借鉴 gstack 的编排思想与闭环方法，但保持 un9flow 的 embedded-first 语义、证据模型和工件导向。
