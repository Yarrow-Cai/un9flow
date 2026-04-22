---
name: orchestration
description: Route ambiguous, cross-scenario, or explicit orchestration requests into the un9flow top-level orchestration flow.
---

# orchestration

## 目标
- 作为总入口 skill，接收模糊请求、跨场景请求或显式总调度请求，并把请求接入总调度外壳。
- 按 `docs/ORCHESTRATOR_PROMPT_CONTRACT.md` 的字段边界承接输入与输出，保证请求进入总路由链路。

## 入口路由摘要
- 显式主场景且证据一致时直进子入口。
- 模糊、交叉、跨场景或显式总调度请求时先走 `orchestration`。
- 辅助 skill 不参与全局首路由竞争，仅在 incident 语义上下文中允许显式进入。
- 具体优先级与例外以 `docs/ORCHESTRATION.md` 为准。

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
