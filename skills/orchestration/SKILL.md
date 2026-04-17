# orchestration

## 目标
- 作为总入口 skill，接收模糊请求、跨场景请求或显式总调度请求，并把请求接入总调度外壳。
- 按 `docs/ORCHESTRATOR_PROMPT_CONTRACT.md` 的字段边界承接输入与输出，保证请求进入总路由链路。

## 进入条件

### 自动路由模式
- 用户请求场景不清，缺乏单场景决断证据。
- 用户请求触及多个场景边界（例如现象解释与设计复核并存）。
- 系统尚未具备直接落入单一场景的最小判定条件。

### 显式总调度模式
- 用户明确要求“先走总调度 / 先做统一编排 / 让 orchestrator 判定场景”。
- 用户要求比较多个场景路径、对比主路由方案。

## 裁决原则

1. **证据特征优先**：以 `evidence` 特征和可验证缺口为主导，避免按措辞猜测场景。
2. **建立中 vs 退化中**：先确认系统阶段为“建立中”还是“退化中”，再进入对应场景策略。
3. **解释现象 vs 复核方案**：先判定请求主目标是“解释现象”还是“复核方案”，再决定最先发起的场景主线。
4. **冲突时选最可执行场景**：多场景信号同强时，优先选择当前可直接推进且可闭环的场景。

## 输出骨架

### Routing Result
- `primary_scenario`
- `secondary_candidates`
- `routing_rationale`

### Phase Plan
- `phase_sequence`
- `skipped_phases`
- `inserted_phases`
- `ordering_rationale`

### Dispatch Plan
- `specialist_list`
- `dispatch_reason`
- `expected_artifacts`

### Control Result
- `control_signal`
- `next_actions`
- `unresolved_gaps`

## 不负责什么
- 不重写场景专属 Artifact 细节。
- 不代替场景内调度器做具体 specialist 选择与内部细化。
- 不重写 `docs/ORCHESTRATOR_PROMPT_CONTRACT.md` 的协议字段与硬约束。

## 与子入口关系
- 总入口在上层：`orchestration` 先做裁决与承接。
- 三个主场景在下层：`incident-investigation`、`bringup-path`、`design-safety-review`。
- `incident` 辅助 skill 挂在 `incident-investigation` 场景下（仅场景内协作，不参与总路由竞争）。

## 参考文档
- `docs/ORCHESTRATION.md`
- `docs/ORCHESTRATOR_PROMPT_CONTRACT.md`
- `docs/SKILL_ARCHITECTURE.md`

## Claude Code 宿主附录

- 在 Claude Code 下，可作为总入口 skill 使用。
- 用户请求场景不清、跨场景或显式要求总调度时优先进入本 skill。
- 入口只负责进入与承接，不临时发明新的路由原则。