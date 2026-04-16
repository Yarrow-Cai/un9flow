# un9flow Orchestrator Prompt Contract

## 目标

固定 orchestrator / scenario prompt 的统一协议层：定义输入/输出字段、控制信号和硬约束，防止 prompt 在执行中重写 skill 边界，也不越权改写总调度规则。

## 输入协议

### Case Input

- `用户目标`
- `原始症状`
- `当前约束`
- `当前给定证据`

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
  - `control_signal` 允许值统一沿用 `docs/ORCHESTRATION.md` 的 canonical 列表，不得新增未定义信号。
- `next_actions`
- `unresolved_gaps`

## 硬约束

1. 不允许跳过 risk framing。
2. 不允许把用户措辞直接当主路由。
3. 不允许把 `Scenario / Phase / Domain Specialist / Artifact` 混成一层。
4. 不允许证据不足时给高置信根因。
5. 不允许跳过 review gate 直接收口。
6. 不允许让场景内调度器越权承担总路由裁决。

## 场景扩展点

- 场景子 prompt 可以细化 Artifact。
- 场景子 prompt 可以补强 specialist 偏向。
- 场景子 prompt 不可重写总路由规则。
- 场景子 prompt 不可改写总控制信号协议。
