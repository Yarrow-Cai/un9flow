# un9flow bringup-path truth source design

## 背景

当前仓库已经完成：

- `incident-investigation` 场景真源
- `design-safety-review` 场景真源
- `docs/ORCHESTRATION.md` 中三场景总调度外壳
- `docs/templates/daisy-chain-isospi-afe-bringup-template.md` 作为 bring-up 相关专项模板
- `docs/cases/power-board-bringup-example.md` 作为 bring-up 相关 example

但 `bringup-path` 仍主要停留在总调度文档中的预留场景位置，尚未拥有与 `docs/INCIDENT_WORKFLOW.md`、`docs/DESIGN_SAFETY_REVIEW.md` 对等的正式场景真源文档。这导致 bring-up 场景虽然已有模板和 example，却缺少稳定的场景层边界、phase 骨架、specialist 装配与主 artifact 收口规则。

## 目标

新增正式场景真源：

- `docs/BRINGUP_PATH.md`

把 `bringup-path` 从“总调度中的预留场景”升级为正式场景真源，并以 `isoSPI / AFE bring-up` 作为该场景下的第一个 canonical bring-up 子焦点。

## 非目标

本轮明确不做：

- 不新增新的 `Domain Specialist`
- 不把 `isoSPI / AFE bring-up` 升格为独立主场景
- 不并行引入多个 canonical bring-up 子焦点
- 不在本轮同步扩新的模板生成器、generation regression 或 CI 接线
- 不把 example 或模板提升为真源

## 总体方案

采用“场景真源先行，专项模板挂靠其下”的方式：

1. 新增 `docs/BRINGUP_PATH.md` 作为 bring-up 场景真源
2. 将 `isoSPI / AFE bring-up` 固定为 `bringup-path` 下的第一个 canonical 子焦点
3. 让现有专项模板与 example 继续各司其职：
   - 模板承载专项执行骨架
   - example 承载实例演示
   - 场景真源承载规则定义

这样可以让 bring-up 层级关系与现有 `incident-investigation` / `design-safety-review` 保持对齐，同时避免由模板或案例反向定义场景。

## 文档分工

### `docs/ORCHESTRATION.md`

继续负责三场景总调度规则与高层路由，不下沉具体 bring-up 的执行骨架。

### `docs/BRINGUP_PATH.md`

新增并承担 bringup-path 场景真源职责，负责定义：

- 进入边界与换轨条件
- 默认 phase backbone
- 默认 specialist 装配
- 主 artifact 收口方式
- canonical 子焦点挂接关系
- completion / handoff gate

### `docs/DOMAIN_SPECIALIST_CONTRACTS.md`

继续负责 specialist 的输入 / 输出契约，不直接承担 bring-up 场景编排规则。

### `docs/templates/daisy-chain-isospi-afe-bringup-template.md`

继续作为 `bringup-path` 下 `isoSPI / AFE bring-up` 子焦点的专项模板，用于承载专项执行内容，而不是定义场景本身。

### `docs/cases/power-board-bringup-example.md`

继续作为 bring-up 场景的 example，用于演示真实 bring-up 任务如何落地，不承担真源职责。

## `docs/BRINGUP_PATH.md` 建议章节结构

建议至少固定以下章节：

1. `## 进入边界与换轨`
2. `## 默认 Phase 骨架`
3. `## 默认 specialist 装配`
4. `## 主 Artifact 与 specialist 输出对齐`
5. `## canonical bring-up 子焦点`
6. `## Review Gate / Completion Gate`

这些章节与 `docs/INCIDENT_WORKFLOW.md`、`docs/DESIGN_SAFETY_REVIEW.md` 的场景真源职责保持同层级对齐，但内容围绕 bring-up 特有节奏展开。

## 进入边界与换轨

`bringup-path` 应被定义为：

- 面向板级 bring-up、链路拉通、初始化连通性确认与受控观测的问题场景
- 优先处理“是否具备最小可通信 / 可观测 / 可推进条件”的问题

并明确换轨规则：

- 若问题已经明显转为故障定位、证据归因与故障链解释，应换到 `incident-investigation`
- 若问题已经明显转为设计边界、失效策略、保护策略与设计安全复核，应换到 `design-safety-review`
- 若输入边界不清或多个场景同时竞争，应回交 `docs/ORCHESTRATION.md` 对应的总入口路由逻辑

## 默认 Phase backbone

建议 bringup-path 固定 4 段默认 phase：

1. `bringup-entry-check`
2. `link-readiness`
3. `controlled-observation`
4. `stabilization-and-handoff`

### `bringup-entry-check`

目标：确认当前问题属于 bring-up 语义，而不是 incident 或 design review。形成首轮 bring-up 边界与测量计划。

### `link-readiness`

目标：确认链路是否具备最小可通信条件。典型检查项包括供电、时钟、复位、物理链路与接口初始化。

### `controlled-observation`

目标：在受控前提下读状态、抓返回、缩小故障面，把“不通 / 不稳 / 不一致”区分开，而不是一上来强求完整根因归因。

### `stabilization-and-handoff`

目标：判断是否已达到“最小跑通”，并决定：

- 可以结束当前 bring-up 回合
- 继续下一轮 bring-up
- 换轨到 `incident-investigation`
- 换轨到 `design-safety-review`

## 默认 specialist 装配

### 默认参与 specialist

建议默认参与：

- `signal-path-tracer`
- `register-state-auditor`
- `timing-watchdog-auditor`

其中：

- `signal-path-tracer` 用于梳理通信链、控制链、观测链
- `register-state-auditor` 用于核对初始化状态、配置寄存器、状态位与异常位
- `timing-watchdog-auditor` 以 bring-up 语义下的轻参与形式检查 reset / timeout / poll / wait 是否破坏 bring-up 节奏

### 按需参与 specialist

建议按需参与：

- `state-machine-tracer`
- `failsafe-convergence-reviewer`

只有当 bring-up 流程明确进入状态机推进分析，或已触及保护 / 降级 / 安全收敛行为时，再纳入这些 specialist。

原则是：bring-up 默认不做最重装配，只保留最能支撑链路拉通与受控观测的 specialist。

## 主 Artifact 收口

建议 bring-up 场景新增并固定一个主收口产物：

- `bringup-path-summary`

它至少收口：

- 当前 bring-up 边界
- 已验证通过的链路段
- 仍未闭合的故障面或不确定面
- 下一步测量建议
- 是否建议换轨

specialist 输出的 pack / note 作为其支撑证据，而不让场景结果散落在多个平级文档中。

## canonical bring-up 子焦点

在 `docs/BRINGUP_PATH.md` 中明确：

- `isoSPI / AFE bring-up` 是 `bringup-path` 下第一个 canonical bring-up 子焦点

并固定回指：

- `docs/templates/daisy-chain-isospi-afe-bringup-template.md`
- `docs/cases/power-board-bringup-example.md`

关系约束应当是：

- `docs/BRINGUP_PATH.md` 定义场景层规则
- `docs/templates/daisy-chain-isospi-afe-bringup-template.md` 承载 `isoSPI / AFE bring-up` 的专项执行结构
- `docs/cases/power-board-bringup-example.md` 作为 bring-up 场景实例

模板负责承载专项执行内容，example 负责展示实例，二者都不反向定义场景真源。

## Review Gate / Completion Gate

`docs/BRINGUP_PATH.md` 应明确区分：

- “最小跑通”
- “阶段性稳定”
- “应换轨处理”

至少应允许以下收口结论：

1. 当前 bring-up 目标已经达到最小连通 / 最小可观测状态，可以结束本轮
2. 当前 bring-up 已有部分进展，但仍需下一轮 bring-up，不能宣称完成
3. 当前问题已超出 bring-up 语义，应换轨至 `incident-investigation`
4. 当前问题已触及设计安全 / 保护策略 / 架构边界，应换轨至 `design-safety-review`

## 建议的后续实施范围

后续实现若基于本设计推进，建议最小触达这些文件：

- 新增：`docs/BRINGUP_PATH.md`
- 修改：`docs/ORCHESTRATION.md`
- 修改：`docs/CONSISTENCY_VALIDATION.md`
- 视需要修改：`docs/PLATFORMS.md`、`README.md`
- 视需要修改：`skills/bringup-path/SKILL.md`

但本设计本身不要求同步扩张模板生成、golden regression 或新的 specialist 线。

## 验收标准

当以下条件同时满足时，可认为 bringup-path 真源化基线完成：

- 仓库存在 `docs/BRINGUP_PATH.md`
- 该文档与 `docs/INCIDENT_WORKFLOW.md`、`docs/DESIGN_SAFETY_REVIEW.md` 处于同层级场景真源角色
- 文档中明确了进入边界、默认 phase backbone、默认 specialist 装配、主 artifact 收口与 completion / handoff gate
- 文档中明确 `isoSPI / AFE bring-up` 为第一个 canonical 子焦点
- 现有专项模板与 example 被正确回指并保持各自边界，不反向定义场景
- 一致性校验文档与总调度文档对该新场景的角色说明完成同步
